package com.bfsi.platform.search.common;

import jakarta.validation.constraints.NotBlank;
import java.time.Instant;
import java.util.HashMap;
import java.util.Map;

public class SearchDocument {

    private String id;
    @NotBlank
    private String title;
    @NotBlank
    private String content;
    private String indexType = "documents";
    private String customerId;
    private String agentType;
    private String source;
    private Instant indexedAt = Instant.now();
    private Map<String, Object> metadata = new HashMap<>();

    public String getId() { return id; }
    public void setId(String id) { this.id = id; }
    public String getTitle() { return title; }
    public void setTitle(String title) { this.title = title; }
    public String getContent() { return content; }
    public void setContent(String content) { this.content = content; }
    public String getIndexType() { return indexType; }
    public void setIndexType(String indexType) { this.indexType = indexType; }
    public String getCustomerId() { return customerId; }
    public void setCustomerId(String customerId) { this.customerId = customerId; }
    public String getAgentType() { return agentType; }
    public void setAgentType(String agentType) { this.agentType = agentType; }
    public String getSource() { return source; }
    public void setSource(String source) { this.source = source; }
    public Instant getIndexedAt() { return indexedAt; }
    public void setIndexedAt(Instant indexedAt) { this.indexedAt = indexedAt; }
    public Map<String, Object> getMetadata() { return metadata; }
    public void setMetadata(Map<String, Object> metadata) { this.metadata = metadata != null ? metadata : new HashMap<>(); }
}
