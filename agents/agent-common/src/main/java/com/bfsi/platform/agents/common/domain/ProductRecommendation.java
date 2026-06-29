package com.bfsi.platform.agents.common.domain;

import java.math.BigDecimal;
import java.util.List;

public record ProductRecommendation(
        String recommendationId,
        String customerId,
        List<RecommendedProduct> products,
        String rationale
) {
}
