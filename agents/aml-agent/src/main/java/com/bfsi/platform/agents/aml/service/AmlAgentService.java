package com.bfsi.platform.agents.aml.service;

import com.bfsi.platform.agents.common.*;
import com.bfsi.platform.agents.common.domain.AmlScreeningResult;
import org.springframework.stereotype.Service;

import java.math.BigDecimal;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.UUID;

@Service
public class AmlAgentService extends AbstractBfsiAgent {

    @Override
    public AgentType getType() {
        return AgentType.AML;
    }

    @Override
    public AgentCapabilities getCapabilities() {
        return new AgentCapabilities(
                AgentType.AML,
                "1.0.0",
                Set.of("screen_customer", "transaction_monitoring", "pep_check", "sanctions_screening"),
                List.of("customerId"),
                false
        );
    }

    @Override
    public AgentResponse process(AgentRequest request) {
        String customerId = request.getCustomerId() != null ? request.getCustomerId() : "UNKNOWN";
        BigDecimal amount = extractAmount(request.getPayload());
        List<String> alerts = new ArrayList<>();

        boolean pepMatch = false;
        boolean sanctionsMatch = false;
        BigDecimal riskScore = BigDecimal.valueOf(15);

        if (amount.compareTo(BigDecimal.valueOf(1_000_000)) > 0) {
            alerts.add("HIGH_VALUE_TRANSACTION");
            riskScore = riskScore.add(BigDecimal.valueOf(35));
        }
        if (request.getUserMessage().toLowerCase().contains("offshore")) {
            alerts.add("OFFSHORE_JURISDICTION_FLAG");
            riskScore = riskScore.add(BigDecimal.valueOf(25));
        }

        String riskLevel = riskScore.compareTo(BigDecimal.valueOf(50)) >= 0 ? "HIGH"
                : riskScore.compareTo(BigDecimal.valueOf(30)) >= 0 ? "MEDIUM" : "LOW";
        String recommendation = riskLevel.equals("HIGH") ? "FILE_SAR_AND_BLOCK"
                : riskLevel.equals("MEDIUM") ? "ENHANCED_DUE_DILIGENCE" : "PROCEED";

        AmlScreeningResult result = new AmlScreeningResult(
                "AML-" + UUID.randomUUID().toString().substring(0, 8),
                customerId,
                riskLevel,
                pepMatch,
                sanctionsMatch,
                alerts,
                riskScore,
                recommendation
        );

        AgentStatus status = "HIGH".equals(riskLevel) ? AgentStatus.REJECTED
                : "MEDIUM".equals(riskLevel) ? AgentStatus.PENDING : AgentStatus.SUCCESS;

        AgentResponse response = buildResponse(request, status,
                "AML screening complete — risk level: " + riskLevel);
        response.setConfidence(0.88);
        response.withData("amlResult", result);

        if ("HIGH".equals(riskLevel)) {
            response.setRequiresEscalation(true);
            routeTo(response, AgentType.ESCALATION, AgentType.COMPLIANCE, AgentType.AUDIT);
        } else if ("MEDIUM".equals(riskLevel)) {
            routeTo(response, AgentType.COMPLIANCE, AgentType.AUDIT);
        } else {
            routeTo(response, AgentType.AUDIT);
        }
        return response;
    }

    private BigDecimal extractAmount(Map<String, Object> payload) {
        if (payload.containsKey("amount")) {
            return new BigDecimal(payload.get("amount").toString());
        }
        return BigDecimal.valueOf(50_000);
    }
}
