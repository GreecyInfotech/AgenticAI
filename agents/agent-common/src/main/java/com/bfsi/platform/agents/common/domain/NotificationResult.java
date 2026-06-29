package com.bfsi.platform.agents.common.domain;

import java.time.Instant;

public record NotificationResult(
        String notificationId,
        String channel,
        String recipient,
        String status,
        String templateId,
        Instant sentAt
) {
}
