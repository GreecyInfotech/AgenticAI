package com.bfsi.platform.aigateway.router;

import org.springframework.boot.context.properties.ConfigurationProperties;

import java.util.HashMap;
import java.util.Map;

@ConfigurationProperties(prefix = "ai.routing")
public class ModelRoutingProperties {

  private String defaultChatModel = "gpt-4o";
  private String defaultEmbeddingModel = "text-embedding-3-small";
  private String azureDeployment = "";
  private boolean allowMock = true;
  private Map<String, String> agentModels = new HashMap<>();

  public ModelRoutingProperties() {
    agentModels.put("INTENT", "gpt-4o-mini");
    agentModels.put("KYC", "gpt-4o");
    agentModels.put("AML", "gpt-4o");
    agentModels.put("FRAUD", "gpt-4o");
    agentModels.put("COMPLIANCE", "gpt-4o");
    agentModels.put("LOAN", "gpt-4o-mini");
    agentModels.put("UNDERWRITING", "gpt-4o");
    agentModels.put("CLAIM", "gpt-4o");
    agentModels.put("RECOMMENDATION", "gpt-4o-mini");
    agentModels.put("PORTFOLIO", "gpt-4o");
  }

  public String getDefaultChatModel() { return defaultChatModel; }
  public void setDefaultChatModel(String defaultChatModel) { this.defaultChatModel = defaultChatModel; }
  public String getDefaultEmbeddingModel() { return defaultEmbeddingModel; }
  public void setDefaultEmbeddingModel(String defaultEmbeddingModel) { this.defaultEmbeddingModel = defaultEmbeddingModel; }
  public String getAzureDeployment() { return azureDeployment; }
  public void setAzureDeployment(String azureDeployment) { this.azureDeployment = azureDeployment; }
  public boolean isAllowMock() { return allowMock; }
  public void setAllowMock(boolean allowMock) { this.allowMock = allowMock; }
  public Map<String, String> getAgentModels() { return agentModels; }
  public void setAgentModels(Map<String, String> agentModels) { this.agentModels = agentModels; }
}
