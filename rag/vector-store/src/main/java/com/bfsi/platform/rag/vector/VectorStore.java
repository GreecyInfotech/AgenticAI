package com.bfsi.platform.rag.vector;

import com.bfsi.platform.agents.common.AgentType;

import java.util.List;
import java.util.Map;

public interface VectorStore {

    void upsert(StoredChunk chunk);

    List<ScoredChunk> search(AgentType agentType, List<Double> queryEmbedding, int topK, double minScore);

    int countChunks(AgentType agentType);

    int countDocuments(AgentType agentType);

    Map<AgentType, Integer> chunkCountsByAgent();

    void clear();

    default List<ScoredChunk> keywordSearch(AgentType agentType, String query, int topK) {
        return List.of();
    }

    record StoredChunk(
        String chunkId,
        String documentId,
        AgentType agentType,
        String title,
        String content,
        List<Double> embedding,
        Map<String, Object> metadata
    ) {}

    record ScoredChunk(StoredChunk chunk, double score) {}
}
