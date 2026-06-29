package com.bfsi.platform.aigateway.router;

import com.bfsi.platform.aigateway.provider.AzureOpenAiProperties;
import com.bfsi.platform.aigateway.provider.OpenAiProperties;
import org.springframework.boot.actuate.health.Health;
import org.springframework.boot.actuate.health.HealthIndicator;
import org.springframework.stereotype.Component;

@Component
public class AiGatewayHealthIndicator implements HealthIndicator {

  private final OpenAiProperties openAiProperties;
  private final AzureOpenAiProperties azureProperties;
  private final ModelRoutingProperties routingProperties;

  public AiGatewayHealthIndicator(OpenAiProperties openAiProperties,
                                  AzureOpenAiProperties azureProperties,
                                  ModelRoutingProperties routingProperties) {
    this.openAiProperties = openAiProperties;
    this.azureProperties = azureProperties;
    this.routingProperties = routingProperties;
  }

  @Override
  public Health health() {
    boolean openAi = openAiProperties.isConfigured();
    boolean azure = azureProperties.isConfigured();
    boolean mock = routingProperties.isAllowMock();

    if (!openAi && !azure && !mock) {
      return Health.down()
          .withDetail("openai", "not configured")
          .withDetail("azureOpenAi", "not configured")
          .withDetail("mock", "disabled")
          .build();
    }

    return Health.up()
        .withDetail("openai", openAi ? "configured" : "not configured")
        .withDetail("azureOpenAi", azure ? "configured" : "not configured")
        .withDetail("mock", mock ? "enabled" : "disabled")
        .withDetail("defaultModel", routingProperties.getDefaultChatModel())
        .build();
  }
}
