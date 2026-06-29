package com.bfsi.platform.agents.common.domain;

import com.bfsi.platform.agents.common.AgentType;

public record IntentClassification(
        String intent,
        AgentType targetAgent,
        double confidence,
        String reasoning
) {
}
