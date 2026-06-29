package com.bfsi.platform.bff.common.client;

import com.bfsi.platform.agents.common.AgentRequest;
import com.bfsi.platform.bff.common.dto.ChatRequest;
import com.bfsi.platform.bff.common.dto.ChatResponse;
import com.bfsi.platform.agents.common.OrchestrationResult;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;
import org.springframework.web.client.RestTemplate;

import java.util.UUID;

@Component
public class OrchestratorClient {

    private final RestTemplate restTemplate;
    private final String orchestratorUrl;

    public OrchestratorClient(RestTemplate restTemplate,
                              @Value("${bff.orchestrator.url:http://localhost:8200}") String orchestratorUrl) {
        this.restTemplate = restTemplate;
        this.orchestratorUrl = orchestratorUrl;
    }

    public ChatResponse chat(ChatRequest chatRequest) {
        AgentRequest agentRequest = new AgentRequest();
        agentRequest.setRequestId(chatRequest.getRequestId() != null
                ? chatRequest.getRequestId() : UUID.randomUUID().toString());
        agentRequest.setSessionId(chatRequest.getSessionId());
        agentRequest.setCustomerId(chatRequest.getCustomerId());
        agentRequest.setUserMessage(chatRequest.getMessage());
        agentRequest.setContext(chatRequest.getContext());

        OrchestrationResult result = restTemplate.postForObject(
                orchestratorUrl + "/api/v1/orchestrate", agentRequest, OrchestrationResult.class);

        ChatResponse response = new ChatResponse();
        response.setRequestId(result.requestId());
        response.setAgentTrail(result.agentResponses());
        if (result.finalResponse() != null) {
            response.setReply(result.finalResponse().getMessage());
            response.setStatus(result.finalResponse().getStatus().name());
            response.setRequiresEscalation(result.finalResponse().isRequiresEscalation());
        }
        return response;
    }
}
