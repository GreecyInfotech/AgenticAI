package com.bfsi.platform.agents.common.domain;

import java.math.BigDecimal;
import java.util.List;

public record ClaimAssessment(
        String claimId,
        String policyId,
        String status,
        BigDecimal approvedAmount,
        boolean coverageValid,
        List<String> requiredDocuments,
        List<String> denialReasons
) {
}
