package com.bfsi.platform.aigateway.provider;

import org.springframework.boot.context.properties.ConfigurationProperties;

@ConfigurationProperties(prefix = "ai.providers.azure-openai")
public class AzureOpenAiProperties {

  private boolean enabled = false;
  private String endpoint = "";
  private String apiKey = "";
  private String deployment = "";
  private String apiVersion = "2024-08-01-preview";
  private int timeoutSeconds = 60;

  public boolean isEnabled() { return enabled; }
  public void setEnabled(boolean enabled) { this.enabled = enabled; }
  public String getEndpoint() { return endpoint; }
  public void setEndpoint(String endpoint) { this.endpoint = endpoint; }
  public String getApiKey() { return apiKey; }
  public void setApiKey(String apiKey) { this.apiKey = apiKey; }
  public String getDeployment() { return deployment; }
  public void setDeployment(String deployment) { this.deployment = deployment; }
  public String getApiVersion() { return apiVersion; }
  public void setApiVersion(String apiVersion) { this.apiVersion = apiVersion; }
  public int getTimeoutSeconds() { return timeoutSeconds; }
  public void setTimeoutSeconds(int timeoutSeconds) { this.timeoutSeconds = timeoutSeconds; }

  public boolean isConfigured() {
    return enabled && endpoint != null && !endpoint.isBlank()
        && apiKey != null && !apiKey.isBlank()
        && deployment != null && !deployment.isBlank();
  }
}
