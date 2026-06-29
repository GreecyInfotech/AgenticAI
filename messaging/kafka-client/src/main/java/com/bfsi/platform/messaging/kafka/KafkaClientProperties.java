package com.bfsi.platform.messaging.kafka;

import org.springframework.boot.context.properties.ConfigurationProperties;

@ConfigurationProperties(prefix = "messaging.kafka")
public class KafkaClientProperties {

    private boolean enabled = false;
    private String bootstrapServers = "localhost:9092";
    private String clientId = "bfsi-platform";
    private String consumerGroup = "bfsi-platform-consumers";
    private int retries = 3;

    public boolean isEnabled() { return enabled; }
    public void setEnabled(boolean enabled) { this.enabled = enabled; }
    public String getBootstrapServers() { return bootstrapServers; }
    public void setBootstrapServers(String bootstrapServers) { this.bootstrapServers = bootstrapServers; }
    public String getClientId() { return clientId; }
    public void setClientId(String clientId) { this.clientId = clientId; }
    public String getConsumerGroup() { return consumerGroup; }
    public void setConsumerGroup(String consumerGroup) { this.consumerGroup = consumerGroup; }
    public int getRetries() { return retries; }
    public void setRetries(int retries) { this.retries = retries; }
}
