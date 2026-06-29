package com.bfsi.platform.agents.common.registry;

import com.bfsi.platform.agents.common.AgentType;

public record AgentRegistration(
        AgentType type,
        String serviceName,
        String baseUrl,
        int port,
        String healthEndpoint,
        boolean healthy
) {
}
