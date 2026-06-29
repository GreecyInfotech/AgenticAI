package com.bfsi.platform.agents.common.domain;

import java.math.BigDecimal;

public record AssetAllocation(
        String assetClass,
        BigDecimal percentage,
        BigDecimal value
) {
}
