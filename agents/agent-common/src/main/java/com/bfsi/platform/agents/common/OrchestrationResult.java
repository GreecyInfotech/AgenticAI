package com.bfsi.platform.agents.common;

import java.util.List;

public record OrchestrationResult(
        String requestId,
        List<AgentResponse> agentResponses,
        AgentResponse finalResponse
) {
}
