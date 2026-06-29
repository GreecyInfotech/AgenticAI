package com.bfsi.platform.messaging.kafka;

import com.bfsi.platform.messaging.common.PlatformEvent;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.kafka.core.KafkaTemplate;

public class KafkaEventPublisher implements EventPublisher {

    private static final Logger log = LoggerFactory.getLogger(KafkaEventPublisher.class);

    private final KafkaTemplate<String, String> kafkaTemplate;
    private final ObjectMapper objectMapper;

    public KafkaEventPublisher(KafkaTemplate<String, String> kafkaTemplate, ObjectMapper objectMapper) {
        this.kafkaTemplate = kafkaTemplate;
        this.objectMapper = objectMapper;
    }

    @Override
    public void publish(String topic, PlatformEvent event) {
        try {
            String json = objectMapper.writeValueAsString(event);
            String key = event.getCorrelationId() != null ? event.getCorrelationId() : event.getEventId();
            kafkaTemplate.send(topic, key, json);
            log.debug("Published {} to topic {}", event.getEventType(), topic);
        } catch (Exception e) {
            log.warn("Failed to publish event {} to {}: {}", event.getEventType(), topic, e.getMessage());
        }
    }

    @Override
    public boolean isEnabled() {
        return true;
    }
}
