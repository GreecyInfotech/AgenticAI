package com.bfsi.platform.rag.vector;

import com.bfsi.platform.agents.common.AgentType;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.boot.autoconfigure.condition.ConditionalOnProperty;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.stereotype.Component;

import java.util.*;
import java.util.stream.Collectors;

@Component
@ConditionalOnProperty(prefix = "rag.vector", name = "store", havingValue = "pgvector")
public class PgVectorStore implements VectorStore {

    private static final Logger log = LoggerFactory.getLogger(PgVectorStore.class);

    private final JdbcTemplate jdbc;
    private final InMemoryVectorStore fallback = new InMemoryVectorStore();
    private volatile boolean pgAvailable = true;

    public PgVectorStore(JdbcTemplate jdbcTemplate) {
        this.jdbc = jdbcTemplate;
        initSchema();
    }

    private void initSchema() {
        try {
            jdbc.execute("CREATE EXTENSION IF NOT EXISTS vector");
            jdbc.execute("""
                CREATE TABLE IF NOT EXISTS rag_chunks (
                    chunk_id VARCHAR(64) PRIMARY KEY,
                    document_id VARCHAR(64) NOT NULL,
                    agent_type VARCHAR(32) NOT NULL,
                    title TEXT,
                    content TEXT NOT NULL,
                    embedding vector(1536),
                    metadata JSONB DEFAULT '{}',
                    created_at TIMESTAMPTZ DEFAULT NOW()
                )
                """);
            jdbc.execute("CREATE INDEX IF NOT EXISTS idx_rag_chunks_agent ON rag_chunks(agent_type)");
        } catch (Exception e) {
            log.warn("pgvector init failed, using in-memory fallback: {}", e.getMessage());
            pgAvailable = false;
        }
    }

    @Override
    public void upsert(StoredChunk chunk) {
        if (!pgAvailable) {
            fallback.upsert(chunk);
            return;
        }
        try {
            String vector = toPgVector(chunk.embedding());
            jdbc.update("""
                INSERT INTO rag_chunks (chunk_id, document_id, agent_type, title, content, embedding, metadata)
                VALUES (?, ?, ?, ?, ?, ?::vector, ?::jsonb)
                ON CONFLICT (chunk_id) DO UPDATE SET
                    content = EXCLUDED.content,
                    embedding = EXCLUDED.embedding,
                    title = EXCLUDED.title
                """,
                chunk.chunkId(), chunk.documentId(), chunk.agentType().name(),
                chunk.title(), chunk.content(), vector, "{}"
            );
        } catch (Exception e) {
            log.warn("pgvector upsert failed: {}", e.getMessage());
            fallback.upsert(chunk);
        }
    }

    @Override
    public List<ScoredChunk> search(AgentType agentType, List<Double> queryEmbedding, int topK, double minScore) {
        if (!pgAvailable) {
            return fallback.search(agentType, queryEmbedding, topK, minScore);
        }
        try {
            String vector = toPgVector(queryEmbedding);
            return jdbc.query("""
                SELECT chunk_id, document_id, agent_type, title, content,
                       1 - (embedding <=> ?::vector) AS score
                FROM rag_chunks
                WHERE agent_type = ?
                ORDER BY embedding <=> ?::vector
                LIMIT ?
                """,
                (rs, rowNum) -> {
                    double score = rs.getDouble("score");
                    StoredChunk chunk = new StoredChunk(
                        rs.getString("chunk_id"),
                        rs.getString("document_id"),
                        AgentType.valueOf(rs.getString("agent_type")),
                        rs.getString("title"),
                        rs.getString("content"),
                        queryEmbedding,
                        Map.of()
                    );
                    return new ScoredChunk(chunk, score);
                },
                vector, agentType.name(), vector, topK
            ).stream().filter(sc -> sc.score() >= minScore).collect(Collectors.toList());
        } catch (Exception e) {
            log.warn("pgvector search failed: {}", e.getMessage());
            return fallback.search(agentType, queryEmbedding, topK, minScore);
        }
    }

    @Override
    public int countChunks(AgentType agentType) {
        if (!pgAvailable) return fallback.countChunks(agentType);
        try {
            Integer count = jdbc.queryForObject(
                "SELECT COUNT(*) FROM rag_chunks WHERE agent_type = ?",
                Integer.class, agentType.name());
            return count != null ? count : 0;
        } catch (Exception e) {
            return fallback.countChunks(agentType);
        }
    }

    @Override
    public int countDocuments(AgentType agentType) {
        if (!pgAvailable) return fallback.countDocuments(agentType);
        try {
            Integer count = jdbc.queryForObject(
                "SELECT COUNT(DISTINCT document_id) FROM rag_chunks WHERE agent_type = ?",
                Integer.class, agentType.name());
            return count != null ? count : 0;
        } catch (Exception e) {
            return fallback.countDocuments(agentType);
        }
    }

    @Override
    public Map<AgentType, Integer> chunkCountsByAgent() {
        if (!pgAvailable) return fallback.chunkCountsByAgent();
        Map<AgentType, Integer> counts = new EnumMap<>(AgentType.class);
        for (AgentType type : AgentType.values()) {
            counts.put(type, countChunks(type));
        }
        return counts;
    }

    @Override
    public void clear() {
        fallback.clear();
        if (pgAvailable) {
            try {
                jdbc.execute("TRUNCATE rag_chunks");
            } catch (Exception ignored) {}
        }
    }

    @Override
    public List<ScoredChunk> keywordSearch(AgentType agentType, String query, int topK) {
        return fallback.keywordSearch(agentType, query, topK);
    }

    private static String toPgVector(List<Double> embedding) {
        return "[" + embedding.stream().map(String::valueOf).collect(Collectors.joining(",")) + "]";
    }
}
