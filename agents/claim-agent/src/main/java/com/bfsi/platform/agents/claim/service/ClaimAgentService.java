package com.bfsi.platform.agents.claim.service;

import com.bfsi.platform.agents.common.*;
import com.bfsi.platform.agents.common.domain.ClaimAssessment;
import org.springframework.stereotype.Service;

import java.math.BigDecimal;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.UUID;

@Service
public class ClaimAgentService extends AbstractBfsiAgent {

    @Override
    public AgentType getType() {
        return AgentType.CLAIM;
    }

    @Override
    public AgentCapabilities getCapabilities() {
        return new AgentCapabilities(
                AgentType.CLAIM,
                "1.0.0",
                Set.of("fnol_intake", "coverage_validation", "claim_adjudication"),
                List.of("customerId", "policyId"),
                false
        );
    }

    @Override
    public AgentResponse process(AgentRequest request) {
        String claimId = "CLM-" + UUID.randomUUID().toString().substring(0, 8);
        String policyId = request.getPayload().getOrDefault("policyId", "POL-UNKNOWN").toString();
        BigDecimal claimAmount = extractAmount(request.getPayload());
        String claimType = request.getPayload().getOrDefault("claimType", "GENERAL").toString();

        List<String> requiredDocs = new ArrayList<>();
        List<String> denialReasons = new ArrayList<>();
        boolean coverageValid = true;

        switch (claimType.toUpperCase()) {
            case "HEALTH" -> requiredDocs.addAll(List.of("MEDICAL_BILLS", "DISCHARGE_SUMMARY", "PRESCRIPTION"));
            case "AUTO" -> requiredDocs.addAll(List.of("POLICE_REPORT", "REPAIR_ESTIMATE", "PHOTOS"));
            case "PROPERTY" -> requiredDocs.addAll(List.of("DAMAGE_ASSESSMENT", "INVOICE", "PHOTOS"));
            default -> requiredDocs.add("CLAIM_FORM");
        }

        if (claimAmount.compareTo(BigDecimal.valueOf(5_000_000)) > 0) {
            coverageValid = false;
            denialReasons.add("Claim amount exceeds policy coverage limit");
        }

        String status = coverageValid ? "UNDER_REVIEW" : "DENIED";
        BigDecimal approvedAmount = coverageValid ? claimAmount.multiply(BigDecimal.valueOf(0.85)) : BigDecimal.ZERO;

        ClaimAssessment assessment = new ClaimAssessment(
                claimId, policyId, status, approvedAmount, coverageValid, requiredDocs, denialReasons
        );

        AgentStatus agentStatus = coverageValid ? AgentStatus.PENDING : AgentStatus.REJECTED;
        AgentResponse response = buildResponse(request, agentStatus,
                coverageValid ? "Claim submitted for review" : "Claim denied — coverage invalid");
        response.setConfidence(0.83);
        response.withData("claimAssessment", assessment);

        if (coverageValid) {
            routeTo(response, AgentType.UNDERWRITING, AgentType.FRAUD, AgentType.AUDIT);
        } else {
            routeTo(response, AgentType.NOTIFICATION, AgentType.AUDIT);
        }
        return response;
    }

    private BigDecimal extractAmount(Map<String, Object> payload) {
        return payload.containsKey("claimAmount")
                ? new BigDecimal(payload.get("claimAmount").toString())
                : BigDecimal.valueOf(100_000);
    }
}
