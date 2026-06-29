package com.bfsi.platform.agents.common;

import java.util.Arrays;
import java.util.List;

public abstract class AbstractBfsiAgent implements BfsiAgent {

    protected AgentResponse buildResponse(AgentRequest request, AgentStatus status, String message) {
        AgentResponse response = new AgentResponse();
        response.setRequestId(request.getRequestId());
        response.setAgentType(getType());
        response.setStatus(status);
        response.setMessage(message);
        response.getAuditTrail().add(AuditEntry.of(getType(), "PROCESS", status.name(), 1.0));
        attachRagContext(request, response);
        return response;
    }

    protected void attachRagContext(AgentRequest request, AgentResponse response) {
        if (request.getContext() == null) return;
        Object chunks = request.getContext().get("ragChunks");
        if (chunks != null) {
            response.withData("ragChunks", chunks);
        }
        Object insight = request.getContext().get("ragInsight");
        if (insight != null) {
            response.withData("ragInsight", insight);
        }
        Object collection = request.getContext().get("ragCollection");
        if (collection != null) {
            response.withData("ragCollection", collection);
        }
    }

    protected void routeTo(AgentResponse response, AgentType... agents) {
        response.setNextAgents(Arrays.asList(agents));
    }
}
