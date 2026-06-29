package com.bfsi.platform.aigateway.cache;

import org.springframework.boot.autoconfigure.condition.ConditionalOnProperty;
import org.springframework.boot.context.properties.EnableConfigurationProperties;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.data.redis.connection.RedisConnectionFactory;
import org.springframework.data.redis.core.StringRedisTemplate;

import java.util.Optional;

@Configuration
@EnableConfigurationProperties(CacheProperties.class)
public class ResponseCacheConfig {

  @Bean
  @ConditionalOnProperty(prefix = "ai.cache", name = "use-redis", havingValue = "true")
  StringRedisTemplate stringRedisTemplate(RedisConnectionFactory factory) {
    return new StringRedisTemplate(factory);
  }

  @Bean
  @ConditionalOnProperty(prefix = "ai.cache", name = "use-redis", havingValue = "true")
  Optional<StringRedisTemplate> optionalRedisTemplate(StringRedisTemplate template) {
    return Optional.of(template);
  }

  @Bean
  @ConditionalOnProperty(prefix = "ai.cache", name = "use-redis", havingValue = "false", matchIfMissing = true)
  Optional<StringRedisTemplate> emptyRedisTemplate() {
    return Optional.empty();
  }
}
