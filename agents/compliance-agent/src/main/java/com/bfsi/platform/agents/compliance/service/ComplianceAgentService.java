package com.bfsi.platform.agents.compliance.service;

import com.bfsi.platform.agents.common.*;
import com.bfsi.platform.agents.common.domain.ComplianceCheck;
import com.bfsi.platform.tools.bindings.RegulatoryTools;
import com.bfsi.platform.tools.common.ToolInvocationResult;
import com.bfsi.platform.agents.common.ToolSupport;
import org.springframework.stereotype.Service;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.UUID;

@Service
public class ComplianceAgentService extends AbstractBfsiAgent {

    private static final Map<String, String> REGULATIONS = Map.of(
            "rbi", "RBI",
            "aml", "AML",
            "gdpr", "GDPR",
            "kyc", "RBI",
            "insurance", "IRDAI"
    );

    private final RegulatoryTools regulatoryTools;

    public ComplianceAgentService(RegulatoryTools regulatoryTools) {
        this.regulatoryTools = regulatoryTools;
    }

    @Override
    public AgentType getType() {
        return AgentType.COMPLIANCE;
    }

    @Override
    public AgentCapabilities getCapabilities() {
        return new AgentCapabilities(
                AgentType.COMPLIANCE,
                "1.0.0",
                Set.of("regulatory_check", "policy_validation", "breach_detection"),
                List.of("customerId"),
                false
        );
    }

    @Override
    public AgentResponse process(AgentRequest request) {
        String framework = detectRegulation(request.getUserMessage());
        ToolInvocationResult lookup = regulatoryTools.lookupRegulation(framework);
        ToolInvocationResult check = regulatoryTools.checkCompliance(framework, request.getUserMessage());

        List<String> violations = new ArrayList<>();
        List<String> recommendations = new ArrayList<>();
        boolean compliant = true;
        String severity = "LOW";

        if (check.isSuccess()) {
            compliant = Boolean.TRUE.equals(check.getData().get("compliant"));
            Object v = check.getData().get("violations");
            if (v instanceof List<?> list) {
                list.forEach(item -> violations.add(item.toString()));
            }
            if (!compliant) severity = violations.stream().anyMatch(s -> s.toLowerCase().contains("breach"))
                ? "CRITICAL" : "HIGH";
        } else {
            violations.addAll(ruleBasedViolations(request.getUserMessage()));
            compliant = violations.isEmpty();
            if (!compliant) severity = "HIGH";
        }

        if (!violations.isEmpty()) {
            recommendations.add("Initiate compliance review workflow");
        } else {
            recommendations.add("No action required — regulatory check passed");
        }

        ComplianceCheck complianceCheck = new ComplianceCheck(
                "COMP-" + UUID.randomUUID().toString().substring(0, 8),
                lookup.isSuccess() ? lookup.getData().getOrDefault("name", framework).toString() : framework,
                compliant,
                violations,
                recommendations,
                severity
        );

        AgentStatus status = compliant ? AgentStatus.SUCCESS : AgentStatus.PENDING;
        AgentResponse response = buildResponse(request, status,
                "Compliance check against " + complianceCheck.regulation());
        response.setConfidence(0.90);
        response.withData("complianceCheck", complianceCheck);
        ToolSupport.record(response, lookup);
        ToolSupport.record(response, check);

        if (!compliant) {
            response.setRequiresEscalation(true);
            routeTo(response, AgentType.ESCALATION, AgentType.AUDIT);
        } else {
            routeTo(response, AgentType.AUDIT);
        }
        return response;
    }

    private List<String> ruleBasedViolations(String message) {
        List<String> violations = new ArrayList<>();
        String lower = message.toLowerCase();
        if (lower.contains("data breach")) {
            violations.add("Potential data breach — GDPR Article 33 notification required within 72 hours");
        }
        if (lower.contains("cross border")) {
            violations.add("Cross-border transfer requires RBI approval under FEMA");
        }
        return violations;
    }

    private String detectRegulation(String message) {
        String lower = message.toLowerCase();
        for (Map.Entry<String, String> entry : REGULATIONS.entrySet()) {
            if (lower.contains(entry.getKey())) {
                return entry.getValue();
            }
        }
        return "RBI";
    }
}
