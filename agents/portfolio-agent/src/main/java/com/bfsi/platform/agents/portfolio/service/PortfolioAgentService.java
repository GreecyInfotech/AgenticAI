package com.bfsi.platform.agents.portfolio.service;

import com.bfsi.platform.agents.common.*;
import com.bfsi.platform.agents.common.domain.AssetAllocation;
import com.bfsi.platform.agents.common.domain.PortfolioAnalysis;
import org.springframework.stereotype.Service;

import java.math.BigDecimal;
import java.util.List;
import java.util.Set;
import java.util.UUID;

@Service
public class PortfolioAgentService extends AbstractBfsiAgent {

    @Override
    public AgentType getType() {
        return AgentType.PORTFOLIO;
    }

    @Override
    public AgentCapabilities getCapabilities() {
        return new AgentCapabilities(
                AgentType.PORTFOLIO,
                "1.0.0",
                Set.of("portfolio_analysis", "rebalancing", "wealth_advisory"),
                List.of("customerId"),
                false
        );
    }

    @Override
    public AgentResponse process(AgentRequest request) {
        String customerId = request.getCustomerId() != null ? request.getCustomerId() : "UNKNOWN";
        String riskProfile = request.getPayload().getOrDefault("riskProfile", "MODERATE").toString();

        List<AssetAllocation> allocations = List.of(
                new AssetAllocation("EQUITY", BigDecimal.valueOf(45), BigDecimal.valueOf(2_250_000)),
                new AssetAllocation("DEBT", BigDecimal.valueOf(30), BigDecimal.valueOf(1_500_000)),
                new AssetAllocation("GOLD", BigDecimal.valueOf(10), BigDecimal.valueOf(500_000)),
                new AssetAllocation("REAL_ESTATE", BigDecimal.valueOf(10), BigDecimal.valueOf(500_000)),
                new AssetAllocation("CASH", BigDecimal.valueOf(5), BigDecimal.valueOf(250_000))
        );

        List<String> recommendations = buildAdvisory(riskProfile, allocations);

        PortfolioAnalysis analysis = new PortfolioAnalysis(
                "PORT-" + UUID.randomUUID().toString().substring(0, 8),
                customerId,
                BigDecimal.valueOf(5_000_000),
                BigDecimal.valueOf(12.5),
                riskProfile,
                allocations,
                recommendations
        );

        AgentResponse response = buildResponse(request, AgentStatus.SUCCESS,
                "Portfolio analysis complete — total value ₹50,00,000");
        response.setConfidence(0.86);
        response.withData("portfolioAnalysis", analysis);
        routeTo(response, AgentType.RECOMMENDATION, AgentType.AUDIT);
        return response;
    }

    private List<String> buildAdvisory(String riskProfile, List<AssetAllocation> allocations) {
        return switch (riskProfile.toUpperCase()) {
            case "AGGRESSIVE" -> List.of(
                    "Increase equity allocation to 60% for higher growth potential",
                    "Consider international diversification via global funds"
            );
            case "CONSERVATIVE" -> List.of(
                    "Shift 10% from equity to debt for capital preservation",
                    "Explore government securities for stable returns"
            );
            default -> List.of(
                    "Portfolio is well-balanced for moderate risk profile",
                    "Consider SIP in index funds for rupee-cost averaging",
                    "Review gold allocation given current market conditions"
            );
        };
    }
}
