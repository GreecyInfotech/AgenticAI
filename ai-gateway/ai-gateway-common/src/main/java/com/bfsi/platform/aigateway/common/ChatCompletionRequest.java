package com.bfsi.platform.aigateway.common;

import jakarta.validation.constraints.NotEmpty;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class ChatCompletionRequest {

  private String requestId;

  private String sessionId;
  private String customerId;
  private String agentType;
  private String model;
  private String promptTemplateId;
  private Double temperature = 0.7;
  private Integer maxTokens = 2048;
  private boolean cacheEnabled = true;

  @NotEmpty
  private List<ChatMessage> messages;

  private Map<String, String> promptVariables = new HashMap<>();
  private Map<String, Object> metadata = new HashMap<>();

  public String getRequestId() { return requestId; }
  public void setRequestId(String requestId) { this.requestId = requestId; }
  public String getSessionId() { return sessionId; }
  public void setSessionId(String sessionId) { this.sessionId = sessionId; }
  public String getCustomerId() { return customerId; }
  public void setCustomerId(String customerId) { this.customerId = customerId; }
  public String getAgentType() { return agentType; }
  public void setAgentType(String agentType) { this.agentType = agentType; }
  public String getModel() { return model; }
  public void setModel(String model) { this.model = model; }
  public String getPromptTemplateId() { return promptTemplateId; }
  public void setPromptTemplateId(String promptTemplateId) { this.promptTemplateId = promptTemplateId; }
  public Double getTemperature() { return temperature; }
  public void setTemperature(Double temperature) { this.temperature = temperature; }
  public Integer getMaxTokens() { return maxTokens; }
  public void setMaxTokens(Integer maxTokens) { this.maxTokens = maxTokens; }
  public boolean isCacheEnabled() { return cacheEnabled; }
  public void setCacheEnabled(boolean cacheEnabled) { this.cacheEnabled = cacheEnabled; }
  public List<ChatMessage> getMessages() { return messages; }
  public void setMessages(List<ChatMessage> messages) { this.messages = messages; }
  public Map<String, String> getPromptVariables() { return promptVariables; }
  public void setPromptVariables(Map<String, String> promptVariables) {
    this.promptVariables = promptVariables != null ? promptVariables : new HashMap<>();
  }
  public Map<String, Object> getMetadata() { return metadata; }
  public void setMetadata(Map<String, Object> metadata) {
    this.metadata = metadata != null ? metadata : new HashMap<>();
  }
}
