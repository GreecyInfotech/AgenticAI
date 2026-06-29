package com.bfsi.platform.agents.common.domain;

import java.math.BigDecimal;
import java.util.List;

public record LoanEligibility(
        String applicationId,
        String customerId,
        boolean eligible,
        BigDecimal maxLoanAmount,
        BigDecimal recommendedRate,
        int recommendedTenureMonths,
        List<String> eligibleProducts,
        List<String> rejectionReasons
) {
}
