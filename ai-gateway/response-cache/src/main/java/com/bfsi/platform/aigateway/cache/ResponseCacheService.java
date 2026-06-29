package com.bfsi.platform.aigateway.cache;

import com.bfsi.platform.aigateway.common.ChatCompletionRequest;
import com.bfsi.platform.aigateway.common.ChatCompletionResponse;
import com.bfsi.platform.aigateway.common.EmbeddingRequest;
import com.bfsi.platform.aigateway.common.EmbeddingResponse;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.springframework.data.redis.core.StringRedisTemplate;
import org.springframework.stereotype.Service;

import java.nio.charset.StandardCharsets;
import java.security.MessageDigest;
import java.time.Duration;
import java.util.HexFormat;
import java.util.Map;
import java.util.Optional;
import java.util.concurrent.ConcurrentHashMap;

@Service
public class ResponseCacheService {

  private static final Logger log = LoggerFactory.getLogger(ResponseCacheService.class);

  private final CacheProperties properties;
  private final ObjectMapper objectMapper;
  private final Optional<StringRedisTemplate> redis;
  private final Map<String, CacheEntry> memoryCache = new ConcurrentHashMap<>();

  public ResponseCacheService(CacheProperties properties,
                              ObjectMapper objectMapper,
                              Optional<StringRedisTemplate> redis) {
    this.properties = properties;
    this.objectMapper = objectMapper;
    this.redis = redis;
  }

  public Optional<ChatCompletionResponse> getChat(String key) {
    return get(key, ChatCompletionResponse.class);
  }

  public void putChat(String key, ChatCompletionResponse response) {
    put(key, response);
  }

  public Optional<EmbeddingResponse> getEmbedding(String key) {
    return get(key, EmbeddingResponse.class);
  }

  public void putEmbedding(String key, EmbeddingResponse response) {
    put(key, response);
  }

  public String chatKey(ChatCompletionRequest request, String model) {
    String raw = model + "|" + request.getTemperature() + "|" + request.getPromptTemplateId()
        + "|" + request.getMessages().toString();
    return properties.getKeyPrefix() + "chat:" + hash(raw);
  }

  public String embeddingKey(EmbeddingRequest request, String model) {
    return properties.getKeyPrefix() + "embed:" + hash(model + "|" + request.getInput());
  }

  private <T> Optional<T> get(String key, Class<T> type) {
    if (!properties.isEnabled()) return Optional.empty();

    if (redis.isPresent()) {
      try {
        String value = redis.get().opsForValue().get(key);
        if (value != null) {
          try {
            T result = objectMapper.readValue(value, type);
            if (result instanceof ChatCompletionResponse c) c.setCached(true);
            if (result instanceof EmbeddingResponse e) e.setCached(true);
            return Optional.of(result);
          } catch (JsonProcessingException ignored) {
            return Optional.empty();
          }
        }
      } catch (Exception ex) {
        log.warn("Redis cache read failed, falling back to memory: {}", ex.getMessage());
      }
    }

    CacheEntry entry = memoryCache.get(key);
    if (entry != null && !entry.isExpired()) {
      try {
        T result = objectMapper.readValue(entry.value(), type);
        if (result instanceof ChatCompletionResponse c) c.setCached(true);
        if (result instanceof EmbeddingResponse e) e.setCached(true);
        return Optional.of(result);
      } catch (JsonProcessingException ignored) {
        return Optional.empty();
      }
    }
    return Optional.empty();
  }

  private void put(String key, Object value) {
    if (!properties.isEnabled()) return;
    try {
      String json = objectMapper.writeValueAsString(value);
      if (redis.isPresent()) {
        try {
          redis.get().opsForValue().set(key, json, Duration.ofSeconds(properties.getTtlSeconds()));
          return;
        } catch (Exception ex) {
          log.warn("Redis cache write failed, falling back to memory: {}", ex.getMessage());
        }
      }
      memoryCache.put(key, new CacheEntry(json, System.currentTimeMillis() + properties.getTtlSeconds() * 1000));
    } catch (JsonProcessingException ignored) {
      // skip cache write
    }
  }

  private String hash(String input) {
    try {
      byte[] digest = MessageDigest.getInstance("SHA-256").digest(input.getBytes(StandardCharsets.UTF_8));
      return HexFormat.of().formatHex(digest).substring(0, 32);
    } catch (Exception e) {
      return Integer.toHexString(input.hashCode());
    }
  }

  private record CacheEntry(String value, long expiresAt) {
    boolean isExpired() {
      return System.currentTimeMillis() > expiresAt;
    }
  }
}
