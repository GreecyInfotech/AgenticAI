package com.bfsi.platform.rag.common;

import com.bfsi.platform.agents.common.AgentType;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;

public class RetrievalRequest {

    private String requestId;

    @NotNull
    private AgentType agentType;

    @NotBlank
    private String query;

    private int topK = 5;
    private double minScore = 0.0;

    public String getRequestId() { return requestId; }
    public void setRequestId(String requestId) { this.requestId = requestId; }
    public AgentType getAgentType() { return agentType; }
    public void setAgentType(AgentType agentType) { this.agentType = agentType; }
    public String getQuery() { return query; }
    public void setQuery(String query) { this.query = query; }
    public int getTopK() { return topK; }
    public void setTopK(int topK) { this.topK = topK; }
    public double getMinScore() { return minScore; }
    public void setMinScore(double minScore) { this.minScore = minScore; }
}
