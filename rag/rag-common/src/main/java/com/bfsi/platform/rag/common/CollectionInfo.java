package com.bfsi.platform.rag.common;

import com.bfsi.platform.agents.common.AgentType;

public class CollectionInfo {

    private AgentType agentType;
    private String collectionId;
    private String description;
    private int documentCount;
    private int chunkCount;

    public CollectionInfo() {}

    public CollectionInfo(AgentType agentType, String collectionId, String description,
                          int documentCount, int chunkCount) {
        this.agentType = agentType;
        this.collectionId = collectionId;
        this.description = description;
        this.documentCount = documentCount;
        this.chunkCount = chunkCount;
    }

    public AgentType getAgentType() { return agentType; }
    public void setAgentType(AgentType agentType) { this.agentType = agentType; }
    public String getCollectionId() { return collectionId; }
    public void setCollectionId(String collectionId) { this.collectionId = collectionId; }
    public String getDescription() { return description; }
    public void setDescription(String description) { this.description = description; }
    public int getDocumentCount() { return documentCount; }
    public void setDocumentCount(int documentCount) { this.documentCount = documentCount; }
    public int getChunkCount() { return chunkCount; }
    public void setChunkCount(int chunkCount) { this.chunkCount = chunkCount; }
}
