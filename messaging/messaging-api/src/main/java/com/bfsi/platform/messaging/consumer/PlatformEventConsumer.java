package com.bfsi.platform.messaging.consumer;

import com.bfsi.platform.messaging.api.EventMetricsService;
import com.bfsi.platform.messaging.common.PlatformTopics;
import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.boot.autoconfigure.condition.ConditionalOnProperty;
import org.springframework.kafka.annotation.KafkaListener;
import org.springframework.stereotype.Component;

@Component
@ConditionalOnProperty(prefix = "messaging.kafka", name = "enabled", havingValue = "true")
public class PlatformEventConsumer {

    private static final Logger log = LoggerFactory.getLogger(PlatformEventConsumer.class);

    private final ObjectMapper objectMapper;
    private final EventMetricsService metricsService;

    public PlatformEventConsumer(ObjectMapper objectMapper, EventMetricsService metricsService) {
        this.objectMapper = objectMapper;
        this.metricsService = metricsService;
    }

    @KafkaListener(topics = PlatformTopics.ORCHESTRATION, groupId = "${messaging.kafka.consumer-group}")
    public void onOrchestration(String message) {
        handle(PlatformTopics.ORCHESTRATION, message);
    }

    @KafkaListener(topics = PlatformTopics.AGENT_DECISIONS, groupId = "${messaging.kafka.consumer-group}")
    public void onAgentDecision(String message) {
        handle(PlatformTopics.AGENT_DECISIONS, message);
    }

    @KafkaListener(topics = PlatformTopics.AUDIT, groupId = "${messaging.kafka.consumer-group}")
    public void onAudit(String message) {
        handle(PlatformTopics.AUDIT, message);
    }

    private void handle(String topic, String message) {
        try {
            JsonNode node = objectMapper.readTree(message);
            String eventType = node.path("eventType").asText("unknown");
            String correlationId = node.path("correlationId").asText("");
            log.info("Consumed {} from {} correlationId={}", eventType, topic, correlationId);
            metricsService.recordProcessed();
        } catch (Exception e) {
            log.warn("Failed to process message on {}: {}", topic, e.getMessage());
        }
    }
}
