package com.bfsi.platform.agents.fraud.service;

import com.bfsi.platform.agents.common.*;
import com.bfsi.platform.agents.common.domain.FraudAssessment;
import org.springframework.stereotype.Service;

import java.math.BigDecimal;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.UUID;

@Service
public class FraudAgentService extends AbstractBfsiAgent {

    @Override
    public AgentType getType() {
        return AgentType.FRAUD;
    }

    @Override
    public AgentCapabilities getCapabilities() {
        return new AgentCapabilities(
                AgentType.FRAUD,
                "1.0.0",
                Set.of("transaction_fraud", "identity_fraud", "velocity_check", "device_fingerprint"),
                List.of("customerId"),
                false
        );
    }

    @Override
    public AgentResponse process(AgentRequest request) {
        String transactionId = request.getPayload().getOrDefault("transactionId",
                "TXN-" + UUID.randomUUID().toString().substring(0, 8)).toString();
        List<String> indicators = detectFraudIndicators(request);
        BigDecimal fraudScore = calculateFraudScore(indicators);

        String riskLevel = fraudScore.compareTo(BigDecimal.valueOf(70)) >= 0 ? "CRITICAL"
                : fraudScore.compareTo(BigDecimal.valueOf(40)) >= 0 ? "HIGH"
                : fraudScore.compareTo(BigDecimal.valueOf(20)) >= 0 ? "MEDIUM" : "LOW";
        boolean blocked = fraudScore.compareTo(BigDecimal.valueOf(70)) >= 0;
        String recommendation = blocked ? "BLOCK_TRANSACTION" : "ALLOW_WITH_MONITORING";

        FraudAssessment assessment = new FraudAssessment(
                "FRAUD-" + UUID.randomUUID().toString().substring(0, 8),
                transactionId,
                riskLevel,
                fraudScore,
                indicators,
                blocked,
                recommendation
        );

        AgentStatus status = blocked ? AgentStatus.REJECTED
                : "HIGH".equals(riskLevel) ? AgentStatus.PENDING : AgentStatus.SUCCESS;

        AgentResponse response = buildResponse(request, status,
                "Fraud assessment: " + riskLevel + " risk (score: " + fraudScore + ")");
        response.setConfidence(0.91);
        response.withData("fraudAssessment", assessment);

        if (blocked || "HIGH".equals(riskLevel)) {
            response.setRequiresEscalation(true);
            routeTo(response, AgentType.ESCALATION, AgentType.AML, AgentType.AUDIT);
        } else {
            routeTo(response, AgentType.AUDIT);
        }
        return response;
    }

    private List<String> detectFraudIndicators(AgentRequest request) {
        List<String> indicators = new ArrayList<>();
        String msg = request.getUserMessage().toLowerCase();
        Map<String, Object> payload = request.getPayload();

        if (msg.contains("unusual") || msg.contains("unauthorized")) {
            indicators.add("UNUSUAL_ACTIVITY_PATTERN");
        }
        if (payload.containsKey("newDevice") && Boolean.TRUE.equals(payload.get("newDevice"))) {
            indicators.add("NEW_DEVICE_LOGIN");
        }
        if (payload.containsKey("velocityExceeded") && Boolean.TRUE.equals(payload.get("velocityExceeded"))) {
            indicators.add("TRANSACTION_VELOCITY_EXCEEDED");
        }
        if (payload.containsKey("geoMismatch") && Boolean.TRUE.equals(payload.get("geoMismatch"))) {
            indicators.add("GEOGRAPHIC_MISMATCH");
        }
        if (indicators.isEmpty()) {
            indicators.add("NO_ANOMALIES_DETECTED");
        }
        return indicators;
    }

    private BigDecimal calculateFraudScore(List<String> indicators) {
        BigDecimal score = BigDecimal.ZERO;
        for (String indicator : indicators) {
            switch (indicator) {
                case "UNUSUAL_ACTIVITY_PATTERN" -> score = score.add(BigDecimal.valueOf(30));
                case "NEW_DEVICE_LOGIN" -> score = score.add(BigDecimal.valueOf(15));
                case "TRANSACTION_VELOCITY_EXCEEDED" -> score = score.add(BigDecimal.valueOf(40));
                case "GEOGRAPHIC_MISMATCH" -> score = score.add(BigDecimal.valueOf(35));
                case "NO_ANOMALIES_DETECTED" -> score = BigDecimal.valueOf(5);
                default -> score = score.add(BigDecimal.valueOf(10));
            }
        }
        return score.min(BigDecimal.valueOf(100));
    }
}
