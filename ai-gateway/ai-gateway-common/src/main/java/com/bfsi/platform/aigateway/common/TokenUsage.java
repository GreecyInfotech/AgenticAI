package com.bfsi.platform.aigateway.common;

public record TokenUsage(int promptTokens, int completionTokens, int totalTokens) {
  public static TokenUsage of(int prompt, int completion) {
    return new TokenUsage(prompt, completion, prompt + completion);
  }
}
