package com.bfsi.platform.aigateway.token;

import org.springframework.boot.context.properties.ConfigurationProperties;

@ConfigurationProperties(prefix = "ai.token")
public class TokenBudgetProperties {

  private int maxPromptTokens = 8192;
  private int maxCompletionTokens = 4096;
  private int maxSessionTokens = 100_000;

  public int getMaxPromptTokens() { return maxPromptTokens; }
  public void setMaxPromptTokens(int maxPromptTokens) { this.maxPromptTokens = maxPromptTokens; }
  public int getMaxCompletionTokens() { return maxCompletionTokens; }
  public void setMaxCompletionTokens(int maxCompletionTokens) { this.maxCompletionTokens = maxCompletionTokens; }
  public int getMaxSessionTokens() { return maxSessionTokens; }
  public void setMaxSessionTokens(int maxSessionTokens) { this.maxSessionTokens = maxSessionTokens; }
}
