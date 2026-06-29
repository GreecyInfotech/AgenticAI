package com.bfsi.platform.aigateway.provider;

import org.springframework.boot.context.properties.ConfigurationProperties;

@ConfigurationProperties(prefix = "ai.providers.openai")
public class OpenAiProperties {

  private boolean enabled = true;
  private String apiKey = "";
  private String baseUrl = "https://api.openai.com/v1";
  private int timeoutSeconds = 60;

  public boolean isEnabled() { return enabled; }
  public void setEnabled(boolean enabled) { this.enabled = enabled; }
  public String getApiKey() { return apiKey; }
  public void setApiKey(String apiKey) { this.apiKey = apiKey; }
  public String getBaseUrl() { return baseUrl; }
  public void setBaseUrl(String baseUrl) { this.baseUrl = baseUrl; }
  public int getTimeoutSeconds() { return timeoutSeconds; }
  public void setTimeoutSeconds(int timeoutSeconds) { this.timeoutSeconds = timeoutSeconds; }

  public boolean isConfigured() {
    return enabled && apiKey != null && !apiKey.isBlank();
  }
}
