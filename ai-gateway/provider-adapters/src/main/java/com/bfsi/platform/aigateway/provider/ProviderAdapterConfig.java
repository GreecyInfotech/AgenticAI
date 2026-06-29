package com.bfsi.platform.aigateway.provider;

import org.springframework.boot.context.properties.EnableConfigurationProperties;
import org.springframework.boot.web.client.RestTemplateBuilder;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.client.RestTemplate;

import java.time.Duration;

@Configuration
@EnableConfigurationProperties({OpenAiProperties.class, AzureOpenAiProperties.class})
public class ProviderAdapterConfig {

  @Bean
  RestTemplate providerRestTemplate(RestTemplateBuilder builder, OpenAiProperties openAi) {
    return builder
        .setConnectTimeout(Duration.ofSeconds(openAi.getTimeoutSeconds()))
        .setReadTimeout(Duration.ofSeconds(openAi.getTimeoutSeconds()))
        .build();
  }
}
