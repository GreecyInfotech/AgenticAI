package com.bfsi.platform.rag.retrieval;

import com.bfsi.platform.agents.common.AgentType;
import com.bfsi.platform.rag.common.*;
import com.bfsi.platform.rag.embedding.EmbeddingClient;
import com.bfsi.platform.rag.vector.VectorStore;
import org.springframework.stereotype.Service;

import java.util.ArrayList;
import java.util.List;
import java.util.UUID;

@Service
public class RetrievalService {

    private final EmbeddingClient embeddingClient;
    private final VectorStore vectorStore;
    private final DocumentIngestionService ingestionService;

    public RetrievalService(EmbeddingClient embeddingClient,
                            VectorStore vectorStore,
                            DocumentIngestionService ingestionService) {
        this.embeddingClient = embeddingClient;
        this.vectorStore = vectorStore;
        this.ingestionService = ingestionService;
    }

    public RetrievalResponse retrieve(RetrievalRequest request) {
        long start = System.currentTimeMillis();
        String requestId = request.getRequestId() != null
            ? request.getRequestId()
            : UUID.randomUUID().toString();

        AgentType agentType = request.getAgentType();
        List<Double> queryEmbedding = embeddingClient.embed(request.getQuery());

        List<VectorStore.ScoredChunk> results = vectorStore.search(
            agentType, queryEmbedding, request.getTopK(), request.getMinScore()
        );

        if (results.isEmpty()) {
            results = vectorStore.keywordSearch(agentType, request.getQuery(), request.getTopK());
        }

        // Keyword boost for hybrid-like retrieval
        results = applyKeywordBoost(request.getQuery(), results);

        RetrievalResponse response = new RetrievalResponse();
        response.setRequestId(requestId);
        response.setAgentType(agentType);
        response.setQuery(request.getQuery());
        response.setCollection(collectionId(agentType));
        response.setLatencyMs(System.currentTimeMillis() - start);

        List<RetrievedChunk> chunks = new ArrayList<>();
        for (VectorStore.ScoredChunk scored : results) {
            VectorStore.StoredChunk stored = scored.chunk();
            RetrievedChunk chunk = new RetrievedChunk(
                stored.chunkId(),
                stored.documentId(),
                stored.agentType(),
                stored.title(),
                stored.content(),
                scored.score()
            );
            chunk.setMetadata(stored.metadata());
            chunks.add(chunk);
        }
        response.setChunks(chunks);
        return response;
    }

    public IngestResponse ingest(IngestRequest request) {
        return ingestionService.ingest(request);
    }

    public List<CollectionInfo> listCollections() {
        return ingestionService.listCollections();
    }

    private List<VectorStore.ScoredChunk> applyKeywordBoost(String query, List<VectorStore.ScoredChunk> results) {
        if (query == null || query.isBlank()) return results;
        String[] terms = query.toLowerCase().split("\\s+");
        return results.stream()
            .map(sc -> {
                String text = (sc.chunk().title() + " " + sc.chunk().content()).toLowerCase();
                double boost = 0;
                for (String term : terms) {
                    if (term.length() > 2 && text.contains(term)) {
                        boost += 0.05;
                    }
                }
                return new VectorStore.ScoredChunk(sc.chunk(), Math.min(1.0, sc.score() + boost));
            })
            .sorted((a, b) -> Double.compare(b.score(), a.score()))
            .toList();
    }

    static String collectionId(AgentType agentType) {
        return "agent-" + agentType.name().toLowerCase();
    }
}
