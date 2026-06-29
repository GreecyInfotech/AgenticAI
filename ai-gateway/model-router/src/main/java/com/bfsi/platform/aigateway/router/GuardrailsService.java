package com.bfsi.platform.aigateway.router;

import com.bfsi.platform.aigateway.common.ChatCompletionRequest;
import com.bfsi.platform.aigateway.common.ChatMessage;
import com.bfsi.platform.aigateway.common.EmbeddingRequest;
import com.bfsi.platform.aigateway.common.GatewayException;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.regex.Pattern;

@Service
public class GuardrailsService {

  private static final Pattern PAN_PATTERN = Pattern.compile("\\b[A-Z]{5}[0-9]{4}[A-Z]\\b");
  private static final Pattern AADHAAR_PATTERN = Pattern.compile("\\b\\d{4}[\\s-]?\\d{4}[\\s-]?\\d{4}\\b");
  private static final List<String> INJECTION_PATTERNS = List.of(
      "ignore previous instructions",
      "disregard all prior",
      "you are now",
      "jailbreak",
      "system prompt override"
  );

  public void validate(ChatCompletionRequest request) {
    for (ChatMessage msg : request.getMessages()) {
      checkContent(msg.content());
    }
    if (request.getPromptVariables() != null) {
      request.getPromptVariables().values().forEach(this::checkContent);
    }
  }

  public void validateEmbedding(EmbeddingRequest request) {
    checkContent(request.getInput());
  }

  private void checkContent(String content) {
    if (content == null) return;

    String lower = content.toLowerCase();
    for (String pattern : INJECTION_PATTERNS) {
      if (lower.contains(pattern)) {
        throw new GatewayException("GUARDRAIL_VIOLATION",
            "Prompt rejected: potential injection pattern detected");
      }
    }

    if (PAN_PATTERN.matcher(content).find()) {
      throw new GatewayException("PII_DETECTED",
          "Request contains unmasked PAN. Mask PII before sending to LLM.");
    }
    if (AADHAAR_PATTERN.matcher(content).find()) {
      throw new GatewayException("PII_DETECTED",
          "Request contains unmasked Aadhaar number. Mask PII before sending to LLM.");
    }
  }
}
