package com.bfsi.platform.aigateway.common;

public class ChatCompletionResponse {

  private String requestId;
  private String id;
  private String model;
  private ModelProvider provider;
  private String content;
  private TokenUsage tokenUsage;
  private boolean cached;
  private String promptTemplateId;
  private long latencyMs;

  public String getRequestId() { return requestId; }
  public void setRequestId(String requestId) { this.requestId = requestId; }
  public String getId() { return id; }
  public void setId(String id) { this.id = id; }
  public String getModel() { return model; }
  public void setModel(String model) { this.model = model; }
  public ModelProvider getProvider() { return provider; }
  public void setProvider(ModelProvider provider) { this.provider = provider; }
  public String getContent() { return content; }
  public void setContent(String content) { this.content = content; }
  public TokenUsage getTokenUsage() { return tokenUsage; }
  public void setTokenUsage(TokenUsage tokenUsage) { this.tokenUsage = tokenUsage; }
  public boolean isCached() { return cached; }
  public void setCached(boolean cached) { this.cached = cached; }
  public String getPromptTemplateId() { return promptTemplateId; }
  public void setPromptTemplateId(String promptTemplateId) { this.promptTemplateId = promptTemplateId; }
  public long getLatencyMs() { return latencyMs; }
  public void setLatencyMs(long latencyMs) { this.latencyMs = latencyMs; }
}
