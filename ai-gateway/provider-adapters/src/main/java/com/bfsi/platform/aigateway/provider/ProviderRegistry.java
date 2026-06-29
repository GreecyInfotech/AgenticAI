package com.bfsi.platform.aigateway.provider;

import com.bfsi.platform.aigateway.common.GatewayException;
import com.bfsi.platform.aigateway.common.LlmProvider;
import com.bfsi.platform.aigateway.common.ModelProvider;
import org.springframework.stereotype.Component;

import java.util.List;

@Component
public class ProviderRegistry {

  private final List<LlmProvider> providers;
  private final MockLlmProvider mockProvider;

  public ProviderRegistry(List<LlmProvider> providers, MockLlmProvider mockProvider) {
    this.providers = providers;
    this.mockProvider = mockProvider;
  }

  public LlmProvider resolve(String model, ModelProvider preferred) {
    if (preferred != null) {
      for (LlmProvider p : providers) {
        if (p.provider() == preferred && p.supports(model)) {
          return p;
        }
      }
    }
    for (LlmProvider p : providers) {
      if (p.provider() != ModelProvider.MOCK && p.supports(model)) {
        return p;
      }
    }
    return mockProvider;
  }

  public LlmProvider requireProvider(String model, ModelProvider preferred) {
    LlmProvider provider = resolve(model, preferred);
    if (provider.provider() == ModelProvider.MOCK) {
      throw new GatewayException("NO_PROVIDER", "No configured provider supports model: " + model);
    }
    return provider;
  }

  public List<LlmProvider> all() {
    return providers;
  }
}
