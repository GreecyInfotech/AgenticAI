package com.bfsi.platform.orchestrator;

import com.bfsi.platform.agents.common.AgentResponse;
import com.bfsi.platform.agents.common.OrchestrationResult;
import com.bfsi.platform.messaging.common.EventTypes;
import com.bfsi.platform.messaging.common.PlatformEvent;
import com.bfsi.platform.messaging.common.PlatformTopics;
import com.bfsi.platform.messaging.kafka.EventPublisher;
import org.springframework.stereotype.Service;

import java.util.HashMap;
import java.util.Map;
import java.util.stream.Collectors;

@Service
public class OrchestrationEventPublisher {

    private final EventPublisher eventPublisher;

    public OrchestrationEventPublisher(EventPublisher eventPublisher) {
        this.eventPublisher = eventPublisher;
    }

    public void publishCompleted(OrchestrationResult result) {
        PlatformEvent event = PlatformEvent.of(
                EventTypes.ORCHESTRATION_COMPLETED,
                "orchestrator",
                result.requestId()
        );
        event.withPayload("agentCount", result.agentResponses().size());
        event.withPayload("finalAgent", result.finalResponse().getAgentType().name());
        event.withPayload("status", result.finalResponse().getStatus().name());
        event.withPayload("requiresEscalation", result.finalResponse().isRequiresEscalation());
        eventPublisher.publish(PlatformTopics.ORCHESTRATION, event);

        for (AgentResponse response : result.agentResponses()) {
            publishAgentDecision(result.requestId(), response);
        }
    }

    private void publishAgentDecision(String requestId, AgentResponse response) {
        PlatformEvent event = PlatformEvent.of(
                EventTypes.AGENT_PROCESSED,
                "orchestrator",
                requestId
        );
        Map<String, Object> payload = new HashMap<>();
        payload.put("agentType", response.getAgentType().name());
        payload.put("status", response.getStatus().name());
        payload.put("confidence", response.getConfidence());
        payload.put("message", response.getMessage());
        payload.put("nextAgents", response.getNextAgents().stream()
                .map(Enum::name)
                .collect(Collectors.toList()));
        event.setPayload(payload);
        eventPublisher.publish(PlatformTopics.AGENT_DECISIONS, event);
    }
}
