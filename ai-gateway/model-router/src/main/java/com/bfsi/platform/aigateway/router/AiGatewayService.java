package com.bfsi.platform.aigateway.router;

import com.bfsi.platform.aigateway.cache.ResponseCacheService;
import com.bfsi.platform.aigateway.common.*;
import com.bfsi.platform.aigateway.prompt.PromptRouterService;
import com.bfsi.platform.aigateway.provider.ProviderRegistry;
import com.bfsi.platform.aigateway.token.TokenBudgetService;
import com.bfsi.platform.aigateway.token.TokenUsageTracker;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.UUID;

@Service
public class AiGatewayService {

  private final ModelRouterService modelRouter;
  private final PromptRouterService promptRouter;
  private final TokenBudgetService tokenBudget;
  private final TokenUsageTracker usageTracker;
  private final ResponseCacheService cache;
  private final GuardrailsService guardrails;
  private final ModelRoutingProperties routingProperties;
  private final ProviderRegistry providerRegistry;

  public AiGatewayService(ModelRouterService modelRouter,
                          PromptRouterService promptRouter,
                          TokenBudgetService tokenBudget,
                          TokenUsageTracker usageTracker,
                          ResponseCacheService cache,
                          GuardrailsService guardrails,
                          ModelRoutingProperties routingProperties,
                          ProviderRegistry providerRegistry) {
    this.modelRouter = modelRouter;
    this.promptRouter = promptRouter;
    this.tokenBudget = tokenBudget;
    this.usageTracker = usageTracker;
    this.cache = cache;
    this.guardrails = guardrails;
    this.routingProperties = routingProperties;
    this.providerRegistry = providerRegistry;
  }

  public ChatCompletionResponse chat(ChatCompletionRequest request) {
    long start = System.currentTimeMillis();
    if (request.getRequestId() == null || request.getRequestId().isBlank()) {
      request.setRequestId(UUID.randomUUID().toString());
    }

    guardrails.validate(request);
    List<ChatMessage> messages = promptRouter.applyTemplate(request);
    request.setMessages(messages);
    tokenBudget.validateRequest(request);

    String model = modelRouter.resolveChatModel(request);

    if (request.isCacheEnabled()) {
      String cacheKey = cache.chatKey(request, model);
      var cached = cache.getChat(cacheKey);
      if (cached.isPresent()) {
        ChatCompletionResponse hit = cached.get();
        hit.setRequestId(request.getRequestId());
        hit.setLatencyMs(System.currentTimeMillis() - start);
        return hit;
      }
    }

    LlmProvider provider = selectProvider(model);
    ChatCompletionResponse response = provider.chat(request, model);
    response.setRequestId(request.getRequestId());
    response.setPromptTemplateId(request.getPromptTemplateId());
    response.setLatencyMs(System.currentTimeMillis() - start);

    tokenBudget.recordUsage(request.getSessionId(), response.getTokenUsage());
    usageTracker.record(model, response.getTokenUsage());

    if (request.isCacheEnabled()) {
      cache.putChat(cache.chatKey(request, model), response);
    }
    return response;
  }

  public EmbeddingResponse embed(EmbeddingRequest request) {
    long start = System.currentTimeMillis();
    if (request.getRequestId() == null || request.getRequestId().isBlank()) {
      request.setRequestId(UUID.randomUUID().toString());
    }

    guardrails.validateEmbedding(request);
    String model = modelRouter.resolveEmbeddingModel(request);

    String cacheKey = cache.embeddingKey(request, model);
    var cached = cache.getEmbedding(cacheKey);
    if (cached.isPresent()) {
      EmbeddingResponse hit = cached.get();
      hit.setRequestId(request.getRequestId());
      hit.setLatencyMs(System.currentTimeMillis() - start);
      return hit;
    }

    LlmProvider provider = selectProvider(model);
    EmbeddingResponse response = provider.embed(request, model);
    response.setRequestId(request.getRequestId());
    response.setLatencyMs(System.currentTimeMillis() - start);

    usageTracker.record(model, response.getTokenUsage());
    cache.putEmbedding(cache.embeddingKey(request, model), response);
    return response;
  }

  private LlmProvider selectProvider(String model) {
    ModelProvider preferred = modelRouter.resolveProvider(model);
    LlmProvider provider = providerRegistry.resolve(model, preferred);
    if (provider.provider() == ModelProvider.MOCK && !routingProperties.isAllowMock()) {
      throw new GatewayException("NO_PROVIDER", "No configured provider supports model: " + model);
    }
    return provider;
  }
}
