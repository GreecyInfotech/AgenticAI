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
public class DocumentIngestionService {

    private static final int CHUNK_SIZE = 500;
    private static final int CHUNK_OVERLAP = 50;

    private final EmbeddingClient embeddingClient;
    private final VectorStore vectorStore;
    private final KnowledgeCorpus corpus;

    public DocumentIngestionService(EmbeddingClient embeddingClient,
                                    VectorStore vectorStore,
                                    KnowledgeCorpus corpus) {
        this.embeddingClient = embeddingClient;
        this.vectorStore = vectorStore;
        this.corpus = corpus;
    }

    public IngestResponse ingest(IngestRequest request) {
        long start = System.currentTimeMillis();
        String requestId = request.getRequestId() != null
            ? request.getRequestId()
            : UUID.randomUUID().toString();

        int docs = 0;
        int chunks = 0;

        for (DocumentInput doc : request.getDocuments()) {
            String docId = doc.getDocumentId() != null
                ? doc.getDocumentId()
                : UUID.randomUUID().toString();
            List<String> parts = chunkText(doc.getContent());
            int idx = 0;
            for (String part : parts) {
                String chunkId = docId + "-" + idx++;
                List<Double> embedding = embeddingClient.embed(part);
                vectorStore.upsert(new VectorStore.StoredChunk(
                    chunkId,
                    docId,
                    doc.getAgentType(),
                    doc.getTitle(),
                    part,
                    embedding,
                    doc.getMetadata()
                ));
                chunks++;
            }
            docs++;
        }

        IngestResponse response = new IngestResponse();
        response.setRequestId(requestId);
        response.setDocumentsIngested(docs);
        response.setChunksCreated(chunks);
        response.setLatencyMs(System.currentTimeMillis() - start);
        return response;
    }

    public void seedIfEmpty() {
        if (vectorStore.chunkCountsByAgent().values().stream().anyMatch(c -> c > 0)) {
            return;
        }
        ingest(corpus.buildSeedCorpus());
    }

    public List<CollectionInfo> listCollections() {
        List<CollectionInfo> collections = new ArrayList<>();
        for (AgentType type : AgentType.values()) {
            collections.add(new CollectionInfo(
                type,
                RetrievalService.collectionId(type),
                corpus.descriptionFor(type),
                vectorStore.countDocuments(type),
                vectorStore.countChunks(type)
            ));
        }
        return collections;
    }

    static List<String> chunkText(String text) {
        List<String> chunks = new ArrayList<>();
        if (text == null || text.isBlank()) return chunks;
        int start = 0;
        while (start < text.length()) {
            int end = Math.min(text.length(), start + CHUNK_SIZE);
            chunks.add(text.substring(start, end).trim());
            if (end >= text.length()) break;
            start = end - CHUNK_OVERLAP;
        }
        return chunks;
    }
}
