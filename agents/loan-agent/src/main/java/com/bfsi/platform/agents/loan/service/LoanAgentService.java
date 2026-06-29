package com.bfsi.platform.agents.loan.service;

import com.bfsi.platform.agents.common.*;
import com.bfsi.platform.agents.common.domain.LoanEligibility;
import org.springframework.stereotype.Service;

import java.math.BigDecimal;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.UUID;

@Service
public class LoanAgentService extends AbstractBfsiAgent {

    @Override
    public AgentType getType() {
        return AgentType.LOAN;
    }

    @Override
    public AgentCapabilities getCapabilities() {
        return new AgentCapabilities(
                AgentType.LOAN,
                "1.0.0",
                Set.of("eligibility_check", "loan_recommendation", "emi_calculator"),
                List.of("customerId"),
                false
        );
    }

    @Override
    public AgentResponse process(AgentRequest request) {
        String customerId = request.getCustomerId() != null ? request.getCustomerId() : "UNKNOWN";
        BigDecimal requestedAmount = extractAmount(request.getPayload(), "requestedAmount", BigDecimal.valueOf(500_000));
        int creditScore = extractInt(request.getPayload(), "creditScore", 750);
        BigDecimal monthlyIncome = extractAmount(request.getPayload(), "monthlyIncome", BigDecimal.valueOf(120_000));

        List<String> rejectionReasons = new ArrayList<>();
        boolean eligible = true;

        if (creditScore < 600) {
            eligible = false;
            rejectionReasons.add("Credit score below minimum threshold (600)");
        }
        BigDecimal maxEmi = monthlyIncome.multiply(BigDecimal.valueOf(0.5));
        BigDecimal estimatedEmi = requestedAmount.multiply(BigDecimal.valueOf(0.012));
        if (estimatedEmi.compareTo(maxEmi) > 0) {
            eligible = false;
            rejectionReasons.add("EMI exceeds 50% of monthly income");
        }

        BigDecimal maxLoan = eligible ? monthlyIncome.multiply(BigDecimal.valueOf(60)) : BigDecimal.ZERO;
        List<String> products = eligible
                ? List.of("HOME_LOAN", "PERSONAL_LOAN", "AUTO_LOAN")
                : List.of();

        LoanEligibility eligibility = new LoanEligibility(
                "LOAN-" + UUID.randomUUID().toString().substring(0, 8),
                customerId,
                eligible,
                maxLoan,
                BigDecimal.valueOf(8.75),
                240,
                products,
                rejectionReasons
        );

        AgentResponse response = buildResponse(request,
                eligible ? AgentStatus.SUCCESS : AgentStatus.REJECTED,
                eligible ? "Customer is eligible for loan products" : "Customer is not eligible");
        response.setConfidence(0.87);
        response.withData("loanEligibility", eligibility);

        if (eligible) {
            routeTo(response, AgentType.UNDERWRITING, AgentType.RECOMMENDATION, AgentType.AUDIT);
        } else {
            routeTo(response, AgentType.RECOMMENDATION, AgentType.AUDIT);
        }
        return response;
    }

    private BigDecimal extractAmount(Map<String, Object> payload, String key, BigDecimal defaultVal) {
        return payload.containsKey(key) ? new BigDecimal(payload.get(key).toString()) : defaultVal;
    }

    private int extractInt(Map<String, Object> payload, String key, int defaultVal) {
        return payload.containsKey(key) ? Integer.parseInt(payload.get(key).toString()) : defaultVal;
    }
}
