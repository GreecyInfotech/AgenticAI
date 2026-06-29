package com.bfsi.platform.agents.common.domain;

import java.time.LocalDate;
import java.util.List;

public record KycVerificationResult(
        String verificationId,
        String customerId,
        String status,
        double confidenceScore,
        List<DocumentCheck> documentChecks,
        List<String> flags,
        LocalDate verifiedAt
) {
}
