package com.bfsi.platform.agents.common;

import java.util.List;
import java.util.Set;

public record AgentCapabilities(
        AgentType type,
        String version,
        Set<String> supportedIntents,
        List<String> requiredContextKeys,
        boolean supportsStreaming
) {
}
