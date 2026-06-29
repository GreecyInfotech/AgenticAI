package com.bfsi.platform.agents.common.domain;

import java.math.BigDecimal;

public record RecommendedProduct(
        String productId,
        String productName,
        String category,
        BigDecimal matchScore,
        String reason
) {
}
