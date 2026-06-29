package com.bfsi.platform.messaging.kafka;

import com.bfsi.platform.messaging.common.PlatformEvent;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class NoOpEventPublisher implements EventPublisher {

    private static final Logger log = LoggerFactory.getLogger(NoOpEventPublisher.class);

    @Override
    public void publish(String topic, PlatformEvent event) {
        log.debug("Kafka disabled — dropping event {} on topic {}", event.getEventType(), topic);
    }

    @Override
    public boolean isEnabled() {
        return false;
    }
}
