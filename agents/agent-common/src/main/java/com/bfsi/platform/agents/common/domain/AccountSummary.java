package com.bfsi.platform.agents.common.domain;

import java.math.BigDecimal;

public record AccountSummary(
        String accountId,
        String accountType,
        String currency,
        BigDecimal balance,
        String status
) {
}
