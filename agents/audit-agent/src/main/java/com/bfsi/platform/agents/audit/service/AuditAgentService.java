package com.bfsi.platform.agents.audit.service;

import com.bfsi.platform.agents.common.*;
import com.bfsi.platform.tools.bindings.AuditTools;
import com.bfsi.platform.tools.common.ToolInvocationResult;
import com.bfsi.platform.agents.common.ToolSupport;
import org.springframework.stereotype.Service;

import java.time.Instant;
import java.util.*;

@Service
public class AuditAgentService extends AbstractBfsiAgent {

    private final AuditTools auditTools;

    public AuditAgentService(AuditTools auditTools) {
        this.auditTools = auditTools;
    }

    @Override
    public AgentType getType() {
        return AgentType.AUDIT;
    }

    @Override
    public AgentCapabilities getCapabilities() {
        return new AgentCapabilities(
                AgentType.AUDIT,
                "1.0.0",
                Set.of("log_decision", "audit_trail", "compliance_report"),
                List.of("requestId"),
                false
        );
    }

    @Override
    public AgentResponse process(AgentRequest request) {
        String action = request.getPayload().getOrDefault("action", "AI_DECISION_LOG").toString();
        String decision = request.getPayload().getOrDefault("decision", request.getUserMessage()).toString();
        String priorAgent = request.getPayload().getOrDefault("priorAgent", getType().name()).toString();

        Map<String, Object> metadata = Map.of(
            "sessionId", Objects.toString(request.getSessionId(), ""),
            "customerId", Objects.toString(request.getCustomerId(), ""),
            "userMessage", request.getUserMessage(),
            "immutable", true
        );

        ToolInvocationResult toolResult = auditTools.logAuditEntry(
            request.getRequestId(), priorAgent, action, decision, metadata
        );

        AgentResponse response = buildResponse(request, AgentStatus.SUCCESS,
                toolResult.isSuccess()
                    ? "Audit entry persisted via MCP postgres tool"
                    : "Audit entry recorded locally (MCP unavailable)");
        response.setConfidence(1.0);
        ToolSupport.record(response, toolResult);

        if (toolResult.isSuccess() && toolResult.getData().containsKey("entry")) {
            @SuppressWarnings("unchecked")
            Map<String, Object> entry = (Map<String, Object>) toolResult.getData().get("entry");
            response.withData("auditEntry", entry);
            response.withData("auditId", entry.get("auditId"));
            response.withData("totalEntries", toolResult.getData().get("totalEntries"));
        } else {
            String auditId = "AUD-" + UUID.randomUUID();
            AuditEntry entry = new AuditEntry(
                auditId,
                request.getTargetAgent() != null ? request.getTargetAgent() : AgentType.AUDIT,
                action, decision, 1.0, metadata, Instant.now()
            );
            response.withData("auditEntry", entry);
            response.withData("auditId", auditId);
        }
        return response;
    }
}
