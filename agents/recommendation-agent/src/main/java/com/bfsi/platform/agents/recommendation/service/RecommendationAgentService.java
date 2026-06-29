package com.bfsi.platform.agents.recommendation.service;

import com.bfsi.platform.agents.common.*;
import com.bfsi.platform.agents.common.domain.ProductRecommendation;
import com.bfsi.platform.agents.common.domain.RecommendedProduct;
import org.springframework.stereotype.Service;

import java.math.BigDecimal;
import java.util.List;
import java.util.Set;
import java.util.UUID;

@Service
public class RecommendationAgentService extends AbstractBfsiAgent {

    @Override
    public AgentType getType() {
        return AgentType.RECOMMENDATION;
    }

    @Override
    public AgentCapabilities getCapabilities() {
        return new AgentCapabilities(
                AgentType.RECOMMENDATION,
                "1.0.0",
                Set.of("product_recommendation", "cross_sell", "upsell"),
                List.of("customerId"),
                false
        );
    }

    @Override
    public AgentResponse process(AgentRequest request) {
        String customerId = request.getCustomerId() != null ? request.getCustomerId() : "UNKNOWN";
        String segment = request.getPayload().getOrDefault("segment", "PREMIUM").toString();

        List<RecommendedProduct> products = buildRecommendations(segment, request.getUserMessage());

        ProductRecommendation recommendation = new ProductRecommendation(
                "REC-" + UUID.randomUUID().toString().substring(0, 8),
                customerId,
                products,
                "Recommendations based on customer segment (" + segment + ") and stated needs"
        );

        AgentResponse response = buildResponse(request, AgentStatus.SUCCESS,
                "Generated " + products.size() + " product recommendations");
        response.setConfidence(0.82);
        response.withData("recommendation", recommendation);
        routeTo(response, AgentType.NOTIFICATION, AgentType.AUDIT);
        return response;
    }

    private List<RecommendedProduct> buildRecommendations(String segment, String message) {
        String lower = message.toLowerCase();
        if (lower.contains("invest") || lower.contains("wealth")) {
            return List.of(
                    new RecommendedProduct("MF-001", "Equity Growth Fund", "MUTUAL_FUND",
                            BigDecimal.valueOf(0.92), "High growth potential aligned with investment intent"),
                    new RecommendedProduct("FD-002", "Tax Saver FD", "FIXED_DEPOSIT",
                            BigDecimal.valueOf(0.78), "Tax-efficient fixed income option")
            );
        }
        if (lower.contains("insurance") || lower.contains("protect")) {
            return List.of(
                    new RecommendedProduct("INS-001", "Term Life Plus", "INSURANCE",
                            BigDecimal.valueOf(0.89), "Comprehensive life coverage"),
                    new RecommendedProduct("INS-002", "Health Shield", "INSURANCE",
                            BigDecimal.valueOf(0.85), "Family health protection plan")
            );
        }
        return List.of(
                new RecommendedProduct("CC-001", "Platinum Credit Card", "CREDIT_CARD",
                        BigDecimal.valueOf(0.88), "Premium benefits for " + segment + " segment"),
                new RecommendedProduct("PL-001", "Personal Loan Express", "LOAN",
                        BigDecimal.valueOf(0.75), "Quick disbursement with competitive rates"),
                new RecommendedProduct("SA-001", "High Yield Savings", "SAVINGS",
                        BigDecimal.valueOf(0.70), "Enhanced interest rate for premium customers")
        );
    }
}
