package com.bfsi.platform.agents.common.domain;

import java.math.BigDecimal;
import java.util.List;

public record FraudAssessment(
        String assessmentId,
        String transactionId,
        String riskLevel,
        BigDecimal fraudScore,
        List<String> indicators,
        boolean blocked,
        String recommendation
) {
}
