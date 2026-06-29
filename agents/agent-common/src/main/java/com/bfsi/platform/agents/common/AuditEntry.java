package com.bfsi.platform.agents.common;

import java.time.Instant;
import java.util.Map;

public record AuditEntry(
        String entryId,
        AgentType agentType,
        String action,
        String decision,
        double confidence,
        Map<String, Object> metadata,
        Instant timestamp
) {
    public static AuditEntry of(AgentType agent, String action, String decision, double confidence) {
        return new AuditEntry(
                java.util.UUID.randomUUID().toString(),
                agent,
                action,
                decision,
                confidence,
                Map.of(),
                Instant.now()
        );
    }
}
