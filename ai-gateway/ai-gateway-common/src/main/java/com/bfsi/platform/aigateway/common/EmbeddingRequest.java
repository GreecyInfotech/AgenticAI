package com.bfsi.platform.aigateway.common;

import jakarta.validation.constraints.NotBlank;
import java.util.HashMap;
import java.util.Map;

public class EmbeddingRequest {

  private String requestId;

  private String model;
  private String agentType;

  @NotBlank
  private String input;

  private Map<String, Object> metadata = new HashMap<>();

  public String getRequestId() { return requestId; }
  public void setRequestId(String requestId) { this.requestId = requestId; }
  public String getModel() { return model; }
  public void setModel(String model) { this.model = model; }
  public String getAgentType() { return agentType; }
  public void setAgentType(String agentType) { this.agentType = agentType; }
  public String getInput() { return input; }
  public void setInput(String input) { this.input = input; }
  public Map<String, Object> getMetadata() { return metadata; }
  public void setMetadata(Map<String, Object> metadata) {
    this.metadata = metadata != null ? metadata : new HashMap<>();
  }
}
