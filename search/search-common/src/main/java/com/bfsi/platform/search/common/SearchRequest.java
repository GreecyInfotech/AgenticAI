package com.bfsi.platform.search.common;

import jakarta.validation.constraints.Max;
import jakarta.validation.constraints.Min;
import jakarta.validation.constraints.NotBlank;

public class SearchRequest {

    @NotBlank
    private String query;
    private String indexType = "documents";
    private String customerId;
    private String agentType;
    @Min(1) @Max(50)
    private int size = 10;

    public String getQuery() { return query; }
    public void setQuery(String query) { this.query = query; }
    public String getIndexType() { return indexType; }
    public void setIndexType(String indexType) { this.indexType = indexType; }
    public String getCustomerId() { return customerId; }
    public void setCustomerId(String customerId) { this.customerId = customerId; }
    public String getAgentType() { return agentType; }
    public void setAgentType(String agentType) { this.agentType = agentType; }
    public int getSize() { return size; }
    public void setSize(int size) { this.size = size; }
}
