package com.bfsi.platform.aigateway.token;

import com.bfsi.platform.aigateway.common.ChatCompletionRequest;
import com.bfsi.platform.aigateway.common.ChatMessage;
import com.bfsi.platform.aigateway.common.GatewayException;
import com.bfsi.platform.aigateway.common.TokenUsage;
import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.stereotype.Component;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.atomic.AtomicLong;

@Service
public class TokenBudgetService {

  private final TokenBudgetProperties properties;
  private final TokenEstimator estimator;
  private final Map<String, AtomicLong> sessionUsage = new ConcurrentHashMap<>();

  public TokenBudgetService(TokenBudgetProperties properties, TokenEstimator estimator) {
    this.properties = properties;
    this.estimator = estimator;
  }

  public void validateRequest(ChatCompletionRequest request) {
    int estimated = estimator.estimateMessages(request.getMessages());
    if (estimated > properties.getMaxPromptTokens()) {
      throw new GatewayException("TOKEN_LIMIT_EXCEEDED",
          "Estimated prompt tokens (" + estimated + ") exceeds limit (" + properties.getMaxPromptTokens() + ")");
    }
    if (request.getMaxTokens() != null && request.getMaxTokens() > properties.getMaxCompletionTokens()) {
      throw new GatewayException("TOKEN_LIMIT_EXCEEDED",
          "Requested max_tokens exceeds limit (" + properties.getMaxCompletionTokens() + ")");
    }
    if (request.getSessionId() != null) {
      long used = sessionUsage.computeIfAbsent(request.getSessionId(), k -> new AtomicLong()).get();
      if (used + estimated > properties.getMaxSessionTokens()) {
        throw new GatewayException("SESSION_TOKEN_LIMIT",
            "Session token budget exceeded for session: " + request.getSessionId());
      }
    }
  }

  public void recordUsage(String sessionId, TokenUsage usage) {
    if (sessionId != null && usage != null) {
      sessionUsage.computeIfAbsent(sessionId, k -> new AtomicLong())
          .addAndGet(usage.totalTokens());
    }
  }

  public long getSessionUsage(String sessionId) {
    AtomicLong counter = sessionUsage.get(sessionId);
    return counter != null ? counter.get() : 0;
  }
}

@Component
class TokenEstimator {

  int estimateMessages(List<ChatMessage> messages) {
    return messages.stream().mapToInt(m -> estimate(m.content())).sum();
  }

  int estimate(String text) {
    if (text == null || text.isBlank()) return 0;
    return Math.max(1, text.length() / 4);
  }
}
