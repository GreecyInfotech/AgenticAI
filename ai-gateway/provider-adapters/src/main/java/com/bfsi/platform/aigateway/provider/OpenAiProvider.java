package com.bfsi.platform.aigateway.provider;

import com.bfsi.platform.aigateway.common.*;
import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.node.ArrayNode;
import com.fasterxml.jackson.databind.node.ObjectNode;
import org.springframework.boot.autoconfigure.condition.ConditionalOnProperty;
import org.springframework.http.*;
import org.springframework.stereotype.Component;
import org.springframework.web.client.RestTemplate;

import java.util.*;

@Component
@ConditionalOnProperty(prefix = "ai.providers.openai", name = "enabled", havingValue = "true", matchIfMissing = true)
public class OpenAiProvider implements LlmProvider {

  private static final Set<String> CHAT_MODELS = Set.of(
      "gpt-4o", "gpt-4o-mini", "gpt-4-turbo", "gpt-3.5-turbo"
  );
  private static final Set<String> EMBEDDING_MODELS = Set.of(
      "text-embedding-3-small", "text-embedding-3-large", "text-embedding-ada-002"
  );

  private final OpenAiProperties properties;
  private final RestTemplate restTemplate;
  private final ObjectMapper objectMapper;

  public OpenAiProvider(OpenAiProperties properties, RestTemplate restTemplate, ObjectMapper objectMapper) {
    this.properties = properties;
    this.restTemplate = restTemplate;
    this.objectMapper = objectMapper;
  }

  @Override
  public ModelProvider provider() {
    return ModelProvider.OPENAI;
  }

  @Override
  public boolean supports(String model) {
    if (!properties.isConfigured()) {
      return false;
    }
    return CHAT_MODELS.contains(model) || EMBEDDING_MODELS.contains(model);
  }

  @Override
  public ChatCompletionResponse chat(ChatCompletionRequest request, String resolvedModel) {
  if (!properties.isConfigured()) {
      throw new GatewayException("PROVIDER_NOT_CONFIGURED", "OpenAI API key is not configured");
    }

    ObjectNode body = objectMapper.createObjectNode();
    body.put("model", resolvedModel);
    body.put("temperature", request.getTemperature());
    body.put("max_tokens", request.getMaxTokens());
    ArrayNode messages = body.putArray("messages");
    for (ChatMessage msg : request.getMessages()) {
      ObjectNode m = messages.addObject();
      m.put("role", msg.role());
      m.put("content", msg.content());
    }

    JsonNode response = post("/chat/completions", body);
    JsonNode choice = response.path("choices").get(0);
    String content = choice.path("message").path("content").asText();
    JsonNode usage = response.path("usage");

    ChatCompletionResponse result = new ChatCompletionResponse();
    result.setId(response.path("id").asText());
    result.setModel(resolvedModel);
    result.setProvider(ModelProvider.OPENAI);
    result.setContent(content);
    result.setTokenUsage(TokenUsage.of(
        usage.path("prompt_tokens").asInt(),
        usage.path("completion_tokens").asInt()
    ));
    return result;
  }

  @Override
  public EmbeddingResponse embed(EmbeddingRequest request, String resolvedModel) {
    if (!properties.isConfigured()) {
      throw new GatewayException("PROVIDER_NOT_CONFIGURED", "OpenAI API key is not configured");
    }

    ObjectNode body = objectMapper.createObjectNode();
    body.put("model", resolvedModel);
    body.put("input", request.getInput());

    JsonNode response = post("/embeddings", body);
    JsonNode embeddingNode = response.path("data").get(0).path("embedding");
    List<Double> vector = new ArrayList<>();
    embeddingNode.forEach(n -> vector.add(n.asDouble()));

    EmbeddingResponse result = new EmbeddingResponse();
    result.setModel(resolvedModel);
    result.setProvider(ModelProvider.OPENAI);
    result.setEmbedding(vector);
    result.setTokenUsage(TokenUsage.of(response.path("usage").path("prompt_tokens").asInt(), 0));
    return result;
  }

  private JsonNode post(String path, ObjectNode body) {
    HttpHeaders headers = new HttpHeaders();
    headers.setContentType(MediaType.APPLICATION_JSON);
    headers.setBearerAuth(properties.getApiKey());
    try {
      ResponseEntity<String> response = restTemplate.exchange(
          properties.getBaseUrl() + path,
          HttpMethod.POST,
          new HttpEntity<>(body.toString(), headers),
          String.class
      );
      return objectMapper.readTree(response.getBody());
    } catch (org.springframework.web.client.HttpStatusCodeException ex) {
      throw new GatewayException("PROVIDER_ERROR",
          "OpenAI API error (" + ex.getStatusCode().value() + "): " + ex.getResponseBodyAsString());
    } catch (Exception e) {
      throw new GatewayException("PROVIDER_ERROR", "OpenAI request failed: " + e.getMessage());
    }
  }
}
