package com.bfsi.platform.rag.common;

import com.bfsi.platform.agents.common.AgentType;

import java.util.ArrayList;
import java.util.List;

public class RetrievalResponse {

    private String requestId;
    private AgentType agentType;
    private String query;
    private String collection;
    private List<RetrievedChunk> chunks = new ArrayList<>();
    private long latencyMs;

    public String getRequestId() { return requestId; }
    public void setRequestId(String requestId) { this.requestId = requestId; }
    public AgentType getAgentType() { return agentType; }
    public void setAgentType(AgentType agentType) { this.agentType = agentType; }
    public String getQuery() { return query; }
    public void setQuery(String query) { this.query = query; }
    public String getCollection() { return collection; }
    public void setCollection(String collection) { this.collection = collection; }
    public List<RetrievedChunk> getChunks() { return chunks; }
    public void setChunks(List<RetrievedChunk> chunks) {
        this.chunks = chunks != null ? chunks : new ArrayList<>();
    }
    public long getLatencyMs() { return latencyMs; }
    public void setLatencyMs(long latencyMs) { this.latencyMs = latencyMs; }
}
