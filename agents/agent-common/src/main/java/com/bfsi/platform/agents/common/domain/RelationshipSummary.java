package com.bfsi.platform.agents.common.domain;

public record RelationshipSummary(
        int totalProducts,
        String relationshipManager,
        String loyaltyTier,
        int tenureYears
) {
}
