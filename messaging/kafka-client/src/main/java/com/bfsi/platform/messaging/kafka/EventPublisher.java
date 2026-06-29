package com.bfsi.platform.messaging.kafka;

import com.bfsi.platform.messaging.common.PlatformEvent;

public interface EventPublisher {

    void publish(String topic, PlatformEvent event);

    boolean isEnabled();
}
