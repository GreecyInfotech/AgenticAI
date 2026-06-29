package com.bfsi.platform.agents.common.domain;

import java.time.Instant;

public record EscalationTicket(
        String ticketId,
        String customerId,
        String priority,
        String queue,
        String reason,
        String assignedTeam,
        Instant createdAt,
        Instant slaDeadline
) {
}
