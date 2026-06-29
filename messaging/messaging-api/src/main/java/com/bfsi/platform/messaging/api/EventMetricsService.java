package com.bfsi.platform.messaging.api;

import org.springframework.stereotype.Service;

import java.util.concurrent.atomic.AtomicLong;

@Service
public class EventMetricsService {

    private final AtomicLong processedCount = new AtomicLong();

    public void recordProcessed() {
        processedCount.incrementAndGet();
    }

    public long getProcessedCount() {
        return processedCount.get();
    }
}
