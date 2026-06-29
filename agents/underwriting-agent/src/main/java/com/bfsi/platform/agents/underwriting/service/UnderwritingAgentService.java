package com.bfsi.platform.agents.underwriting.service;

import com.bfsi.platform.agents.common.*;
import com.bfsi.platform.agents.common.domain.UnderwritingDecision;
import org.springframework.stereotype.Service;

import java.math.BigDecimal;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.UUID;

@Service
public class UnderwritingAgentService extends AbstractBfsiAgent {

    @Override
    public AgentType getType() {
        return AgentType.UNDERWRITING;
    }

    @Override
    public AgentCapabilities getCapabilities() {
        return new AgentCapabilities(
                AgentType.UNDERWRITING,
                "1.0.0",
                Set.of("risk_assessment", "premium_calculation", "coverage_analysis"),
                List.of("customerId", "policyId"),
                false
        );
    }

    @Override
    public AgentResponse process(AgentRequest request) {
        String policyId = request.getPayload().getOrDefault("policyId",
                "POL-" + UUID.randomUUID().toString().substring(0, 8)).toString();
        String applicantId = request.getCustomerId() != null ? request.getCustomerId() : "UNKNOWN";
        int age = extractInt(request.getPayload(), "age", 35);
        String healthStatus = request.getPayload().getOrDefault("healthStatus", "GOOD").toString();

        List<String> conditions = new ArrayList<>();
        List<String> exclusions = new ArrayList<>();
        boolean requiresManualReview = false;
        String decision;

        if (age > 65) {
            decision = "CONDITIONAL_APPROVAL";
            conditions.add("Annual health check-up required");
            requiresManualReview = true;
        } else if ("POOR".equalsIgnoreCase(healthStatus)) {
            decision = "DECLINED";
            exclusions.add("Pre-existing conditions excluded");
        } else {
            decision = "APPROVED";
        }

        BigDecimal basePremium = BigDecimal.valueOf(25_000);
        if (age > 50) {
            basePremium = basePremium.multiply(BigDecimal.valueOf(1.5));
        }

        UnderwritingDecision uwDecision = new UnderwritingDecision(
                "UW-" + UUID.randomUUID().toString().substring(0, 8),
                policyId,
                applicantId,
                decision,
                basePremium,
                "COMPREHENSIVE",
                conditions,
                exclusions,
                requiresManualReview
        );

        AgentStatus status = "DECLINED".equals(decision) ? AgentStatus.REJECTED
                : requiresManualReview ? AgentStatus.PENDING : AgentStatus.SUCCESS;

        AgentResponse response = buildResponse(request, status,
                "Underwriting decision: " + decision);
        response.setConfidence(0.85);
        response.withData("underwritingDecision", uwDecision);

        if (requiresManualReview) {
            response.setRequiresEscalation(true);
            routeTo(response, AgentType.ESCALATION, AgentType.COMPLIANCE, AgentType.AUDIT);
        } else {
            routeTo(response, AgentType.COMPLIANCE, AgentType.AUDIT);
        }
        return response;
    }

    private int extractInt(Map<String, Object> payload, String key, int defaultVal) {
        return payload.containsKey(key) ? Integer.parseInt(payload.get(key).toString()) : defaultVal;
    }
}
