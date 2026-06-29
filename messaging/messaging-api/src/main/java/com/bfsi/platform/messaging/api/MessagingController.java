package com.bfsi.platform.messaging.api;

import com.bfsi.platform.messaging.common.PlatformEvent;
import com.bfsi.platform.messaging.common.PlatformTopics;
import com.bfsi.platform.messaging.kafka.EventPublisher;
import com.bfsi.platform.messaging.kafka.KafkaClientProperties;
import jakarta.validation.Valid;
import jakarta.validation.constraints.NotBlank;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/api/v1")
public class MessagingController {

    private final EventPublisher eventPublisher;
    private final KafkaClientProperties kafkaProperties;
    private final EventMetricsService metricsService;

    public MessagingController(EventPublisher eventPublisher,
                             KafkaClientProperties kafkaProperties,
                             EventMetricsService metricsService) {
        this.eventPublisher = eventPublisher;
        this.kafkaProperties = kafkaProperties;
        this.metricsService = metricsService;
    }

    @GetMapping("/health")
    public ResponseEntity<Map<String, Object>> health() {
        return ResponseEntity.ok(Map.of(
                "status", "UP",
                "service", "messaging-api",
                "kafkaEnabled", eventPublisher.isEnabled(),
                "bootstrapServers", kafkaProperties.getBootstrapServers(),
                "eventsProcessed", metricsService.getProcessedCount()
        ));
    }

    @GetMapping("/topics")
    public ResponseEntity<List<Map<String, String>>> topics() {
        return ResponseEntity.ok(List.of(
                topic(PlatformTopics.ORCHESTRATION, "Orchestration lifecycle events"),
                topic(PlatformTopics.AGENT_DECISIONS, "Agent decision audit stream"),
                topic(PlatformTopics.AUDIT, "Immutable audit log events"),
                topic(PlatformTopics.NOTIFICATIONS, "Outbound notification requests"),
                topic(PlatformTopics.SEARCH_INDEX, "Search index pipeline events")
        ));
    }

    @PostMapping("/publish")
    public ResponseEntity<Map<String, String>> publish(@Valid @RequestBody PublishRequest request) {
        PlatformEvent event = PlatformEvent.of(request.getEventType(), "messaging-api", request.getCorrelationId());
        event.setCustomerId(request.getCustomerId());
        event.setSessionId(request.getSessionId());
        event.setPayload(request.getPayload());
        eventPublisher.publish(request.getTopic(), event);
        return ResponseEntity.ok(Map.of(
                "eventId", event.getEventId(),
                "topic", request.getTopic(),
                "status", eventPublisher.isEnabled() ? "PUBLISHED" : "NOOP"
        ));
    }

    private static Map<String, String> topic(String name, String description) {
        return Map.of("name", name, "description", description);
    }

    public static class PublishRequest {
        @NotBlank
        private String topic;
        @NotBlank
        private String eventType;
        private String correlationId;
        private String customerId;
        private String sessionId;
        private Map<String, Object> payload = Map.of();

        public String getTopic() { return topic; }
        public void setTopic(String topic) { this.topic = topic; }
        public String getEventType() { return eventType; }
        public void setEventType(String eventType) { this.eventType = eventType; }
        public String getCorrelationId() { return correlationId; }
        public void setCorrelationId(String correlationId) { this.correlationId = correlationId; }
        public String getCustomerId() { return customerId; }
        public void setCustomerId(String customerId) { this.customerId = customerId; }
        public String getSessionId() { return sessionId; }
        public void setSessionId(String sessionId) { this.sessionId = sessionId; }
        public Map<String, Object> getPayload() { return payload; }
        public void setPayload(Map<String, Object> payload) { this.payload = payload; }
    }
}
