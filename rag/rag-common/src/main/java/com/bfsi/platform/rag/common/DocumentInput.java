package com.bfsi.platform.rag.common;

import com.bfsi.platform.agents.common.AgentType;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;

import java.util.HashMap;
import java.util.Map;

public class DocumentInput {

    private String documentId;

    @NotNull
    private AgentType agentType;

    @NotBlank
    private String title;

    @NotBlank
    private String content;

    private Map<String, Object> metadata = new HashMap<>();

    public String getDocumentId() { return documentId; }
    public void setDocumentId(String documentId) { this.documentId = documentId; }
    public AgentType getAgentType() { return agentType; }
    public void setAgentType(AgentType agentType) { this.agentType = agentType; }
    public String getTitle() { return title; }
    public void setTitle(String title) { this.title = title; }
    public String getContent() { return content; }
    public void setContent(String content) { this.content = content; }
    public Map<String, Object> getMetadata() { return metadata; }
    public void setMetadata(Map<String, Object> metadata) {
        this.metadata = metadata != null ? metadata : new HashMap<>();
    }
}
