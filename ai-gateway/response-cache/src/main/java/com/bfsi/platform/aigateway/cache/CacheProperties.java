package com.bfsi.platform.aigateway.cache;

import org.springframework.boot.context.properties.ConfigurationProperties;

@ConfigurationProperties(prefix = "ai.cache")
public class CacheProperties {

  private boolean enabled = true;
  private boolean useRedis = false;
  private long ttlSeconds = 3600;
  private String keyPrefix = "ai-gateway:";

  public boolean isEnabled() { return enabled; }
  public void setEnabled(boolean enabled) { this.enabled = enabled; }
  public boolean isUseRedis() { return useRedis; }
  public void setUseRedis(boolean useRedis) { this.useRedis = useRedis; }
  public long getTtlSeconds() { return ttlSeconds; }
  public void setTtlSeconds(long ttlSeconds) { this.ttlSeconds = ttlSeconds; }
  public String getKeyPrefix() { return keyPrefix; }
  public void setKeyPrefix(String keyPrefix) { this.keyPrefix = keyPrefix; }
}
