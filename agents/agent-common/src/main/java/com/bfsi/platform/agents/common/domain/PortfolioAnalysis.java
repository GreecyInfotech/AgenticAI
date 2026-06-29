package com.bfsi.platform.agents.common.domain;

import java.math.BigDecimal;
import java.util.List;

public record PortfolioAnalysis(
        String portfolioId,
        String customerId,
        BigDecimal totalValue,
        BigDecimal ytdReturn,
        String riskProfile,
        List<AssetAllocation> allocations,
        List<String> recommendations
) {
}
