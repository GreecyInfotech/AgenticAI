package com.bfsi.platform.aigateway.provider;

import com.bfsi.platform.aigateway.common.*;
import org.springframework.stereotype.Component;

import java.nio.charset.StandardCharsets;
import java.security.MessageDigest;
import java.util.*;
import java.util.stream.Collectors;

@Component
public class MockLlmProvider implements LlmProvider {

  @Override
  public ModelProvider provider() {
    return ModelProvider.MOCK;
  }

  @Override
  public boolean supports(String model) {
    return true;
  }

  @Override
  public ChatCompletionResponse chat(ChatCompletionRequest request, String resolvedModel) {
    String userMsg = request.getMessages().stream()
        .filter(m -> "user".equalsIgnoreCase(m.role()))
        .map(ChatMessage::content)
        .reduce((a, b) -> b)
        .orElse("");

    String content = "[MOCK %s] Processed BFSI request for agent=%s: %s".formatted(
        resolvedModel,
        request.getAgentType() != null ? request.getAgentType() : "GENERAL",
        userMsg.length() > 200 ? userMsg.substring(0, 200) + "..." : userMsg
    );

    int promptTokens = estimateTokens(request.getMessages());
    ChatCompletionResponse response = new ChatCompletionResponse();
    response.setId("mock-chat-" + UUID.randomUUID());
    response.setModel(resolvedModel);
    response.setProvider(ModelProvider.MOCK);
    response.setContent(content);
    response.setTokenUsage(TokenUsage.of(promptTokens, estimateTokens(content)));
    return response;
  }

  @Override
  public EmbeddingResponse embed(EmbeddingRequest request, String resolvedModel) {
    List<Double> vector = pseudoEmbedding(request.getInput(), 1536);
    EmbeddingResponse response = new EmbeddingResponse();
    response.setModel(resolvedModel);
    response.setProvider(ModelProvider.MOCK);
    response.setEmbedding(vector);
    response.setTokenUsage(TokenUsage.of(estimateTokens(request.getInput()), 0));
    return response;
  }

  private int estimateTokens(String text) {
    return Math.max(1, text.length() / 4);
  }

  private int estimateTokens(List<ChatMessage> messages) {
    return messages.stream().mapToInt(m -> estimateTokens(m.content())).sum();
  }

  private List<Double> pseudoEmbedding(String input, int dimensions) {
    try {
      byte[] hash = MessageDigest.getInstance("SHA-256").digest(input.getBytes(StandardCharsets.UTF_8));
      List<Double> vector = new ArrayList<>(dimensions);
      for (int i = 0; i < dimensions; i++) {
        vector.add((hash[i % hash.length] & 0xFF) / 255.0 - 0.5);
      }
      double norm = Math.sqrt(vector.stream().mapToDouble(v -> v * v).sum());
      return vector.stream().map(v -> v / norm).collect(Collectors.toList());
    } catch (Exception e) {
      return Collections.nCopies(dimensions, 0.0);
    }
  }
}
