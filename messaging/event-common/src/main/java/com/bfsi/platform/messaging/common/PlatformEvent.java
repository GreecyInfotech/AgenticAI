package com.bfsi.platform.messaging.common;

import com.fasterxml.jackson.annotation.JsonInclude;

import java.time.Instant;
import java.util.HashMap;
import java.util.Map;
import java.util.UUID;

@JsonInclude(JsonInclude.Include.NON_NULL)
public class PlatformEvent {

    private String eventId = UUID.randomUUID().toString();
    private String eventType;
    private String source;
    private Instant timestamp = Instant.now();
    private String correlationId;
    private String customerId;
    private String sessionId;
    private Map<String, Object> payload = new HashMap<>();

    public static PlatformEvent of(String eventType, String source, String correlationId) {
        PlatformEvent event = new PlatformEvent();
        event.setEventType(eventType);
        event.setSource(source);
        event.setCorrelationId(correlationId);
        return event;
    }

    public String getEventId() { return eventId; }
    public void setEventId(String eventId) { this.eventId = eventId; }
    public String getEventType() { return eventType; }
    public void setEventType(String eventType) { this.eventType = eventType; }
    public String getSource() { return source; }
    public void setSource(String source) { this.source = source; }
    public Instant getTimestamp() { return timestamp; }
    public void setTimestamp(Instant timestamp) { this.timestamp = timestamp; }
    public String getCorrelationId() { return correlationId; }
    public void setCorrelationId(String correlationId) { this.correlationId = correlationId; }
    public String getCustomerId() { return customerId; }
    public void setCustomerId(String customerId) { this.customerId = customerId; }
    public String getSessionId() { return sessionId; }
    public void setSessionId(String sessionId) { this.sessionId = sessionId; }
    public Map<String, Object> getPayload() { return payload; }
    public void setPayload(Map<String, Object> payload) { this.payload = payload != null ? payload : new HashMap<>(); }

    public PlatformEvent withPayload(String key, Object value) {
        this.payload.put(key, value);
        return this;
    }
}
