package com.bfsi.platform.aigateway.token;

import org.springframework.boot.context.properties.EnableConfigurationProperties;
import org.springframework.context.annotation.Configuration;

@Configuration
@EnableConfigurationProperties(TokenBudgetProperties.class)
public class TokenManagerConfig {
}
