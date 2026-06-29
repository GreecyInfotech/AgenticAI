package com.bfsi.platform.rag.common;

import com.bfsi.platform.agents.common.AgentType;

import java.util.HashMap;
import java.util.Map;

public class RetrievedChunk {

    private String chunkId;
    private String documentId;
    private AgentType agentType;
    private String title;
    private String content;
    private double score;
    private Map<String, Object> metadata = new HashMap<>();

    public RetrievedChunk() {}

    public RetrievedChunk(String chunkId, String documentId, AgentType agentType,
                          String title, String content, double score) {
        this.chunkId = chunkId;
        this.documentId = documentId;
        this.agentType = agentType;
        this.title = title;
        this.content = content;
        this.score = score;
    }

    public String getChunkId() { return chunkId; }
    public void setChunkId(String chunkId) { this.chunkId = chunkId; }
    public String getDocumentId() { return documentId; }
    public void setDocumentId(String documentId) { this.documentId = documentId; }
    public AgentType getAgentType() { return agentType; }
    public void setAgentType(AgentType agentType) { this.agentType = agentType; }
    public String getTitle() { return title; }
    public void setTitle(String title) { this.title = title; }
    public String getContent() { return content; }
    public void setContent(String content) { this.content = content; }
    public double getScore() { return score; }
    public void setScore(double score) { this.score = score; }
    public Map<String, Object> getMetadata() { return metadata; }
    public void setMetadata(Map<String, Object> metadata) {
        this.metadata = metadata != null ? metadata : new HashMap<>();
    }
}
