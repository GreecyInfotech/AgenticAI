package com.bfsi.platform.aigateway.common;

import java.util.List;

public class EmbeddingResponse {

  private String requestId;
  private String model;
  private ModelProvider provider;
  private List<Double> embedding;
  private TokenUsage tokenUsage;
  private boolean cached;
  private long latencyMs;

  public String getRequestId() { return requestId; }
  public void setRequestId(String requestId) { this.requestId = requestId; }
  public String getModel() { return model; }
  public void setModel(String model) { this.model = model; }
  public ModelProvider getProvider() { return provider; }
  public void setProvider(ModelProvider provider) { this.provider = provider; }
  public List<Double> getEmbedding() { return embedding; }
  public void setEmbedding(List<Double> embedding) { this.embedding = embedding; }
  public TokenUsage getTokenUsage() { return tokenUsage; }
  public void setTokenUsage(TokenUsage tokenUsage) { this.tokenUsage = tokenUsage; }
  public boolean isCached() { return cached; }
  public void setCached(boolean cached) { this.cached = cached; }
  public long getLatencyMs() { return latencyMs; }
  public void setLatencyMs(long latencyMs) { this.latencyMs = latencyMs; }
}
