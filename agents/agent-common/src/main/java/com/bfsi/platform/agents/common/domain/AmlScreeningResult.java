package com.bfsi.platform.agents.common.domain;

import java.math.BigDecimal;
import java.util.List;

public record AmlScreeningResult(
        String screeningId,
        String customerId,
        String riskLevel,
        boolean pepMatch,
        boolean sanctionsMatch,
        List<String> alerts,
        BigDecimal riskScore,
        String recommendation
) {
}
