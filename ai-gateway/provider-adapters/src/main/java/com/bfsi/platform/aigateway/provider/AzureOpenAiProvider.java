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
@ConditionalOnProperty(prefix = "ai.providers.azure-openai", name = "enabled", havingValue = "true")
public class AzureOpenAiProvider implements LlmProvider {

  private final AzureOpenAiProperties properties;
  private final RestTemplate restTemplate;
  private final ObjectMapper objectMapper;

  public AzureOpenAiProvider(AzureOpenAiProperties properties, RestTemplate restTemplate, ObjectMapper objectMapper) {
    this.properties = properties;
    this.restTemplate = restTemplate;
    this.objectMapper = objectMapper;
  }

  @Override
  public ModelProvider provider() {
    return ModelProvider.AZURE_OPENAI;
  }

  @Override
  public boolean supports(String model) {
    if (!properties.isConfigured()) {
      return false;
    }
    return properties.getDeployment().equals(model) || model.startsWith("azure-");
  }

  @Override
  public ChatCompletionResponse chat(ChatCompletionRequest request, String resolvedModel) {
    if (!properties.isConfigured()) {
      throw new GatewayException("PROVIDER_NOT_CONFIGURED", "Azure OpenAI is not configured");
    }

    ObjectNode body = objectMapper.createObjectNode();
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
    JsonNode usage = response.path("usage");

    ChatCompletionResponse result = new ChatCompletionResponse();
    result.setId(response.path("id").asText());
    result.setModel(properties.getDeployment());
    result.setProvider(ModelProvider.AZURE_OPENAI);
    result.setContent(choice.path("message").path("content").asText());
    result.setTokenUsage(TokenUsage.of(
        usage.path("prompt_tokens").asInt(),
        usage.path("completion_tokens").asInt()
    ));
    return result;
  }

  @Override
  public EmbeddingResponse embed(EmbeddingRequest request, String resolvedModel) {
    if (!properties.isConfigured()) {
      throw new GatewayException("PROVIDER_NOT_CONFIGURED", "Azure OpenAI is not configured");
    }

    ObjectNode body = objectMapper.createObjectNode();
    body.put("input", request.getInput());

    JsonNode response = post("/embeddings", body);
    List<Double> vector = new ArrayList<>();
    response.path("data").get(0).path("embedding").forEach(n -> vector.add(n.asDouble()));

    EmbeddingResponse result = new EmbeddingResponse();
    result.setModel(properties.getDeployment());
    result.setProvider(ModelProvider.AZURE_OPENAI);
    result.setEmbedding(vector);
    result.setTokenUsage(TokenUsage.of(response.path("usage").path("prompt_tokens").asInt(), 0));
    return result;
  }

  private JsonNode post(String path, ObjectNode body) {
    String base = properties.getEndpoint().replaceAll("/$", "");
    String url = base + "/openai/deployments/" + properties.getDeployment() + path
        + "?api-version=" + properties.getApiVersion();

    HttpHeaders headers = new HttpHeaders();
    headers.setContentType(MediaType.APPLICATION_JSON);
    headers.set("api-key", properties.getApiKey());

    try {
      ResponseEntity<String> response = restTemplate.exchange(
          url, HttpMethod.POST, new HttpEntity<>(body.toString(), headers), String.class
      );
      return objectMapper.readTree(response.getBody());
    } catch (org.springframework.web.client.HttpStatusCodeException ex) {
      throw new GatewayException("PROVIDER_ERROR",
          "Azure OpenAI API error (" + ex.getStatusCode().value() + "): " + ex.getResponseBodyAsString());
    } catch (Exception e) {
      throw new GatewayException("PROVIDER_ERROR", "Azure OpenAI request failed: " + e.getMessage());
    }
  }
}
