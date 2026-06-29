package com.bfsi.platform.aigateway.router;

import com.bfsi.platform.aigateway.common.*;
import com.bfsi.platform.aigateway.provider.ProviderRegistry;
import org.springframework.stereotype.Service;

import java.util.*;

@Service
public class ModelRouterService {

  private final ModelRoutingProperties routingProperties;
  private final ProviderRegistry providerRegistry;

  public ModelRouterService(ModelRoutingProperties routingProperties, ProviderRegistry providerRegistry) {
    this.routingProperties = routingProperties;
    this.providerRegistry = providerRegistry;
  }

  public String resolveChatModel(ChatCompletionRequest request) {
    if (request.getModel() != null && !request.getModel().isBlank()) {
      return request.getModel();
    }
    if (request.getAgentType() != null) {
      String agentModel = routingProperties.getAgentModels().get(request.getAgentType().toUpperCase());
      if (agentModel != null) return agentModel;
    }
    return routingProperties.getDefaultChatModel();
  }

  public String resolveEmbeddingModel(EmbeddingRequest request) {
    if (request.getModel() != null && !request.getModel().isBlank()) {
      return request.getModel();
    }
    return routingProperties.getDefaultEmbeddingModel();
  }

  public ModelProvider resolveProvider(String model) {
    if (model.startsWith("azure-") || model.equals(routingProperties.getAzureDeployment())) {
      return ModelProvider.AZURE_OPENAI;
    }
    return routingProperties.isAllowMock() ? null : ModelProvider.OPENAI;
  }

  public LlmProvider selectProvider(String model, boolean requireLive) {
    ModelProvider preferred = resolveProvider(model);
    if (requireLive && !routingProperties.isAllowMock()) {
      return providerRegistry.requireProvider(model, preferred);
    }
    return providerRegistry.resolve(model, preferred);
  }

  public List<ModelInfo> listModels() {
    List<ModelInfo> models = new ArrayList<>();
    models.add(new ModelInfo("gpt-4o", "GPT-4o", ModelProvider.OPENAI, TaskType.CHAT, 128_000));
    models.add(new ModelInfo("gpt-4o-mini", "GPT-4o Mini", ModelProvider.OPENAI, TaskType.CHAT, 128_000));
    models.add(new ModelInfo("text-embedding-3-small", "Embedding 3 Small", ModelProvider.OPENAI, TaskType.EMBEDDING, 8191));
    if (routingProperties.isAllowMock()) {
      models.add(new ModelInfo("mock-bfsi", "Mock BFSI Model", ModelProvider.MOCK, TaskType.CHAT, 32_000));
    }
    if (routingProperties.getAzureDeployment() != null && !routingProperties.getAzureDeployment().isBlank()) {
      models.add(new ModelInfo(routingProperties.getAzureDeployment(), "Azure Deployment",
          ModelProvider.AZURE_OPENAI, TaskType.CHAT, 128_000));
    }
    return models;
  }
}
