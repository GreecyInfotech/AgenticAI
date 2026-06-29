package com.bfsi.platform.aigateway.token;

import com.bfsi.platform.aigateway.common.TokenUsage;
import org.springframework.stereotype.Service;

import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.atomic.AtomicLong;

@Service
public class TokenUsageTracker {

  private final AtomicLong totalPromptTokens = new AtomicLong();
  private final AtomicLong totalCompletionTokens = new AtomicLong();
  private final AtomicLong totalRequests = new AtomicLong();
  private final Map<String, AtomicLong> byModel = new ConcurrentHashMap<>();

  public void record(String model, TokenUsage usage) {
    if (usage == null) return;
    totalPromptTokens.addAndGet(usage.promptTokens());
    totalCompletionTokens.addAndGet(usage.completionTokens());
    totalRequests.incrementAndGet();
    byModel.computeIfAbsent(model, k -> new AtomicLong()).addAndGet(usage.totalTokens());
  }

  public Map<String, Object> snapshot() {
    return Map.of(
        "totalRequests", totalRequests.get(),
        "totalPromptTokens", totalPromptTokens.get(),
        "totalCompletionTokens", totalCompletionTokens.get(),
        "totalTokens", totalPromptTokens.get() + totalCompletionTokens.get(),
        "byModel", byModel.entrySet().stream()
            .collect(java.util.stream.Collectors.toMap(Map.Entry::getKey, e -> e.getValue().get()))
    );
  }
}
