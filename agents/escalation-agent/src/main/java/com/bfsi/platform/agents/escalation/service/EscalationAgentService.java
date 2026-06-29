package com.bfsi.platform.agents.escalation.service;

import com.bfsi.platform.agents.common.*;
import com.bfsi.platform.agents.common.domain.EscalationTicket;
import com.bfsi.platform.tools.bindings.EscalationTools;
import com.bfsi.platform.tools.common.ToolInvocationResult;
import com.bfsi.platform.agents.common.ToolSupport;
import org.springframework.stereotype.Service;

import java.time.Instant;
import java.time.temporal.ChronoUnit;
import java.util.List;
import java.util.Map;
import java.util.Set;

@Service
public class EscalationAgentService extends AbstractBfsiAgent {

    private final EscalationTools escalationTools;

    public EscalationAgentService(EscalationTools escalationTools) {
        this.escalationTools = escalationTools;
    }

    @Override
    public AgentType getType() {
        return AgentType.ESCALATION;
    }

    @Override
    public AgentCapabilities getCapabilities() {
        return new AgentCapabilities(
                AgentType.ESCALATION,
                "1.0.0",
                Set.of("human_handoff", "case_creation", "sla_management"),
                List.of("customerId"),
                false
        );
    }

    @Override
    public AgentResponse process(AgentRequest request) {
        String customerId = request.getCustomerId() != null ? request.getCustomerId() : "UNKNOWN";
        String reason = request.getPayload().getOrDefault("reason", request.getUserMessage()).toString();
        String priority = determinePriority(reason, request);
        String queue = mapQueue(reason);

        ToolInvocationResult toolResult = escalationTools.createTicket(
            customerId, reason, priority, queue
        );

        EscalationTicket ticket;
        if (toolResult.isSuccess()) {
            Map<String, Object> data = toolResult.getData();
            ticket = new EscalationTicket(
                str(data.get("ticketId"), "ESC-LOCAL"),
                customerId,
                priority,
                queue,
                reason,
                mapTeam(reason),
                Instant.now(),
                Instant.now().plus(slaHours(priority), ChronoUnit.HOURS)
            );
        } else {
            ticket = new EscalationTicket(
                "ESC-FALLBACK",
                customerId,
                priority,
                queue,
                reason,
                mapTeam(reason),
                Instant.now(),
                Instant.now().plus(slaHours(priority), ChronoUnit.HOURS)
            );
        }

        AgentResponse response = buildResponse(request, AgentStatus.ESCALATED,
                "Case escalated to " + ticket.assignedTeam() + " — ticket " + ticket.ticketId());
        response.setConfidence(1.0);
        response.setRequiresEscalation(true);
        response.withData("escalationTicket", ticket);
        if (toolResult.isSuccess()) {
            response.withData("jiraKey", toolResult.getData().get("key"));
        }
        ToolSupport.record(response, toolResult);
        routeTo(response, AgentType.NOTIFICATION, AgentType.AUDIT);
        return response;
    }

    private String determinePriority(String reason, AgentRequest request) {
        String lower = reason.toLowerCase();
        if (lower.contains("fraud") || lower.contains("breach") || lower.contains("critical")) {
            return "P1_CRITICAL";
        }
        if (request.getContext().containsKey("requiresEscalation")
                && Boolean.TRUE.equals(request.getContext().get("requiresEscalation"))) {
            return "P2_HIGH";
        }
        return "P3_NORMAL";
    }

    private String mapQueue(String reason) {
        String lower = reason.toLowerCase();
        if (lower.contains("fraud")) return "FRAUD_INVESTIGATION";
        if (lower.contains("compliance") || lower.contains("regulation")) return "COMPLIANCE_REVIEW";
        if (lower.contains("claim")) return "CLAIMS_ADJUSTMENT";
        if (lower.contains("loan")) return "CREDIT_REVIEW";
        return "GENERAL_SUPPORT";
    }

    private String mapTeam(String reason) {
        String lower = reason.toLowerCase();
        if (lower.contains("fraud")) return "Fraud Operations";
        if (lower.contains("compliance")) return "Compliance Team";
        if (lower.contains("claim")) return "Claims Specialists";
        if (lower.contains("loan") || lower.contains("credit")) return "Credit Underwriters";
        return "Customer Relations";
    }

    private int slaHours(String priority) {
        return switch (priority) {
            case "P1_CRITICAL" -> 2;
            case "P2_HIGH" -> 8;
            default -> 24;
        };
    }

    private static String str(Object value, String defaultVal) {
        return value != null ? value.toString() : defaultVal;
    }
}
