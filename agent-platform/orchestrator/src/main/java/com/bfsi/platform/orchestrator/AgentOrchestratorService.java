package com.bfsi.platform.orchestrator;

import com.bfsi.platform.agents.common.AgentRequest;
import com.bfsi.platform.agents.common.AgentResponse;
import com.bfsi.platform.agents.common.AgentType;
import com.bfsi.platform.agents.common.OrchestrationResult;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

import java.util.*;

@Service
public class AgentOrchestratorService {

    private final RestTemplate restTemplate;
    private final Map<AgentType, String> agentUrls;
    private final RagClient ragClient;
    private final OrchestrationEventPublisher eventPublisher;

    public AgentOrchestratorService(
            RestTemplate restTemplate,
            RagClient ragClient,
            OrchestrationEventPublisher eventPublisher,
            @Value("${agents.host:localhost}") String agentHost) {
        this.restTemplate = restTemplate;
        this.ragClient = ragClient;
        this.eventPublisher = eventPublisher;
        this.agentUrls = buildAgentUrls(agentHost);
    }

    private Map<AgentType, String> buildAgentUrls(String host) {
        Map<AgentType, String> urls = new EnumMap<>(AgentType.class);
        int port = 8401;
        for (AgentType type : AgentType.values()) {
            urls.put(type, "http://" + host + ":" + port++);
        }
        return urls;
    }

    public OrchestrationResult orchestrate(AgentRequest request) {
        List<AgentResponse> responses = new ArrayList<>();
        String requestId = request.getRequestId() != null
                ? request.getRequestId()
                : UUID.randomUUID().toString();
        request.setRequestId(requestId);

        AgentResponse intentResponse = invokeAgent(AgentType.INTENT, request);
        responses.add(intentResponse);

        AgentType target = resolveTarget(intentResponse, request);
        if (target != AgentType.INTENT) {
            request.setTargetAgent(target);
            ragClient.enrichRequest(request, target);
            AgentResponse domainResponse = invokeAgent(target, request);
            responses.add(domainResponse);

            for (AgentType nextAgent : domainResponse.getNextAgents()) {
                if (nextAgent == AgentType.AUDIT || nextAgent == AgentType.NOTIFICATION) {
                    AgentRequest followUp = copyForFollowUp(request, domainResponse);
                    responses.add(invokeAgent(nextAgent, followUp));
                }
            }

            if (domainResponse.isRequiresEscalation()) {
                AgentRequest escalationRequest = copyForFollowUp(request, domainResponse);
                escalationRequest.getContext().put("requiresEscalation", true);
                responses.add(invokeAgent(AgentType.ESCALATION, escalationRequest));
            }
        }

        OrchestrationResult result = new OrchestrationResult(requestId, responses, responses.get(responses.size() - 1));
        eventPublisher.publishCompleted(result);
        return result;
    }

    private AgentType resolveTarget(AgentResponse intentResponse, AgentRequest request) {
        if (request.getTargetAgent() != null) {
            return request.getTargetAgent();
        }
        if (!intentResponse.getNextAgents().isEmpty()) {
            return intentResponse.getNextAgents().getFirst();
        }
        Object target = intentResponse.getData().get("targetAgent");
        if (target != null) {
            return AgentType.valueOf(target.toString());
        }
        return AgentType.CUSTOMER;
    }

    private AgentRequest copyForFollowUp(AgentRequest original, AgentResponse prior) {
        AgentRequest followUp = new AgentRequest();
        followUp.setRequestId(original.getRequestId());
        followUp.setSessionId(original.getSessionId());
        followUp.setCustomerId(original.getCustomerId());
        followUp.setUserMessage(original.getUserMessage());
        followUp.setContext(new HashMap<>(original.getContext()));
        followUp.getPayload().put("priorAgent", prior.getAgentType().name());
        followUp.getPayload().put("priorDecision", prior.getStatus().name());
        followUp.getPayload().put("action", "AI_DECISION_LOG");
        followUp.getPayload().put("decision", prior.getMessage());
        followUp.getPayload().put("confidence", prior.getConfidence());
        return followUp;
    }

    private AgentResponse invokeAgent(AgentType type, AgentRequest request) {
        String url = agentUrls.get(type) + "/api/v1/agent/process";
        return restTemplate.postForObject(url, request, AgentResponse.class);
    }
}
