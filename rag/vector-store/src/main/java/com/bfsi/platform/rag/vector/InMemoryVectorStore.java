package com.bfsi.platform.rag.vector;

import com.bfsi.platform.agents.common.AgentType;
import org.springframework.boot.autoconfigure.condition.ConditionalOnProperty;
import org.springframework.context.annotation.Primary;
import org.springframework.stereotype.Component;

import java.util.*;
import java.util.concurrent.ConcurrentHashMap;
import java.util.stream.Collectors;

@Component
@Primary
@ConditionalOnProperty(prefix = "rag.vector", name = "store", havingValue = "memory", matchIfMissing = true)
public class InMemoryVectorStore implements VectorStore {

    private final Map<String, StoredChunk> chunks = new ConcurrentHashMap<>();

    @Override
    public void upsert(StoredChunk chunk) {
        chunks.put(chunk.chunkId(), chunk);
    }

    @Override
    public List<ScoredChunk> search(AgentType agentType, List<Double> queryEmbedding, int topK, double minScore) {
        return chunks.values().stream()
            .filter(c -> c.agentType() == agentType)
            .map(c -> new ScoredChunk(c, cosineSimilarity(queryEmbedding, c.embedding())))
            .filter(sc -> sc.score() >= minScore)
            .sorted(Comparator.comparingDouble(ScoredChunk::score).reversed())
            .limit(topK)
            .collect(Collectors.toList());
    }

    @Override
    public int countChunks(AgentType agentType) {
        return (int) chunks.values().stream().filter(c -> c.agentType() == agentType).count();
    }

    @Override
    public int countDocuments(AgentType agentType) {
        return (int) chunks.values().stream()
            .filter(c -> c.agentType() == agentType)
            .map(StoredChunk::documentId)
            .distinct()
            .count();
    }

    @Override
    public Map<AgentType, Integer> chunkCountsByAgent() {
        Map<AgentType, Integer> counts = new EnumMap<>(AgentType.class);
        for (AgentType type : AgentType.values()) {
            counts.put(type, countChunks(type));
        }
        return counts;
    }

    @Override
    public void clear() {
        chunks.clear();
    }

    @Override
    public List<ScoredChunk> keywordSearch(AgentType agentType, String query, int topK) {
        if (query == null || query.isBlank()) return List.of();
        String[] terms = query.toLowerCase().split("\\s+");
        return chunks.values().stream()
            .filter(c -> c.agentType() == agentType)
            .map(c -> {
                String text = (c.title() + " " + c.content()).toLowerCase();
                int hits = 0;
                for (String term : terms) {
                    if (term.length() > 2 && text.contains(term)) hits++;
                }
                return new ScoredChunk(c, hits * 0.2);
            })
            .filter(sc -> sc.score() > 0)
            .sorted(Comparator.comparingDouble(ScoredChunk::score).reversed())
            .limit(topK)
            .collect(Collectors.toList());
    }

    static double cosineSimilarity(List<Double> a, List<Double> b) {
        if (a == null || b == null || a.isEmpty() || b.isEmpty()) {
            return 0;
        }
        int len = Math.min(a.size(), b.size());
        double dot = 0, normA = 0, normB = 0;
        for (int i = 0; i < len; i++) {
            dot += a.get(i) * b.get(i);
            normA += a.get(i) * a.get(i);
            normB += b.get(i) * b.get(i);
        }
        if (normA == 0 || normB == 0) return 0;
        return dot / (Math.sqrt(normA) * Math.sqrt(normB));
    }
}
