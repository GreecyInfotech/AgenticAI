package com.bfsi.platform.agents.common.domain;

import java.math.BigDecimal;
import java.util.List;

public record UnderwritingDecision(
        String decisionId,
        String policyId,
        String applicantId,
        String decision,
        BigDecimal premium,
        String coverageLevel,
        List<String> conditions,
        List<String> exclusions,
        boolean requiresManualReview
) {
}
