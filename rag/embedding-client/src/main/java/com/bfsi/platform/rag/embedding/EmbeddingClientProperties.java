package com.bfsi.platform.rag.embedding;

import org.springframework.boot.context.properties.ConfigurationProperties;

@ConfigurationProperties(prefix = "rag.embedding")
public class EmbeddingClientProperties {

    private String aiGatewayUrl = "http://localhost:8300";
    private String model = "text-embedding-3-small";
    private int dimensions = 1536;
    private int timeoutSeconds = 30;
    private boolean fallbackToLocal = true;

    public String getAiGatewayUrl() { return aiGatewayUrl; }
    public void setAiGatewayUrl(String aiGatewayUrl) { this.aiGatewayUrl = aiGatewayUrl; }
    public String getModel() { return model; }
    public void setModel(String model) { this.model = model; }
    public int getDimensions() { return dimensions; }
    public void setDimensions(int dimensions) { this.dimensions = dimensions; }
    public int getTimeoutSeconds() { return timeoutSeconds; }
    public void setTimeoutSeconds(int timeoutSeconds) { this.timeoutSeconds = timeoutSeconds; }
    public boolean isFallbackToLocal() { return fallbackToLocal; }
    public void setFallbackToLocal(boolean fallbackToLocal) { this.fallbackToLocal = fallbackToLocal; }
}
