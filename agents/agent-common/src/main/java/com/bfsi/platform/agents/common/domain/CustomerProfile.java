package com.bfsi.platform.agents.common.domain;

import java.time.LocalDate;
import java.util.List;

public record CustomerProfile(
        String customerId,
        String fullName,
        String email,
        String phone,
        String segment,
        String riskRating,
        LocalDate customerSince,
        List<AccountSummary> accounts,
        RelationshipSummary relationship
) {
}
