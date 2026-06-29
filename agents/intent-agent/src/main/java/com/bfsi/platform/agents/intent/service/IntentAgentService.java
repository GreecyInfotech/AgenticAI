package com.bfsi.platform.agents.intent.service;

import com.bfsi.platform.agents.common.*;
import com.bfsi.platform.agents.common.domain.IntentClassification;
import org.springframework.stereotype.Service;

import java.util.*;

@Service
public class IntentAgentService extends AbstractBfsiAgent {

    private static final Map<String, AgentType> INTENT_ROUTES = Map.ofEntries(
            Map.entry("account_balance", AgentType.CUSTOMER),
            Map.entry("profile", AgentType.CUSTOMER),
            Map.entry("customer_info", AgentType.CUSTOMER),
            Map.entry("kyc", AgentType.KYC),
            Map.entry("identity", AgentType.KYC),
            Map.entry("verify_document", AgentType.KYC),
            Map.entry("aml", AgentType.AML),
            Map.entry("sanctions", AgentType.AML),
            Map.entry("money_laundering", AgentType.AML),
            Map.entry("fraud", AgentType.FRAUD),
            Map.entry("suspicious", AgentType.FRAUD),
            Map.entry("loan", AgentType.LOAN),
            Map.entry("mortgage", AgentType.LOAN),
            Map.entry("credit", AgentType.LOAN),
            Map.entry("underwriting", AgentType.UNDERWRITING),
            Map.entry("insurance", AgentType.UNDERWRITING),
            Map.entry("policy", AgentType.UNDERWRITING),
            Map.entry("claim", AgentType.CLAIM),
            Map.entry("file_claim", AgentType.CLAIM),
            Map.entry("compliance", AgentType.COMPLIANCE),
            Map.entry("regulation", AgentType.COMPLIANCE),
            Map.entry("gdpr", AgentType.COMPLIANCE),
            Map.entry("rbi", AgentType.COMPLIANCE),
            Map.entry("audit", AgentType.AUDIT),
            Map.entry("recommend", AgentType.RECOMMENDATION),
            Map.entry("product", AgentType.RECOMMENDATION),
            Map.entry("portfolio", AgentType.PORTFOLIO),
            Map.entry("investment", AgentType.PORTFOLIO),
            Map.entry("wealth", AgentType.PORTFOLIO),
            Map.entry("escalate", AgentType.ESCALATION),
            Map.entry("human", AgentType.ESCALATION),
            Map.entry("notify", AgentType.NOTIFICATION),
            Map.entry("notification", AgentType.NOTIFICATION)
    );

    @Override
    public AgentType getType() {
        return AgentType.INTENT;
    }

    @Override
    public AgentCapabilities getCapabilities() {
        return new AgentCapabilities(
                AgentType.INTENT,
                "1.0.0",
                Set.of("classify", "route"),
                List.of(),
                false
        );
    }

    @Override
    public AgentResponse process(AgentRequest request) {
        IntentClassification classification = classify(request.getUserMessage());
        AgentResponse response = buildResponse(request, AgentStatus.SUCCESS,
                "Intent classified as: " + classification.intent());
        response.setConfidence(classification.confidence());
        response.withData("classification", classification);
        response.withData("targetAgent", classification.targetAgent().name());
        routeTo(response, classification.targetAgent());

        if (classification.confidence() < 0.6) {
            response.setRequiresEscalation(true);
            response.withNextAgent(AgentType.ESCALATION);
        }
        return response;
    }

    private IntentClassification classify(String message) {
        String normalized = message.toLowerCase(Locale.ROOT);
        String bestIntent = "general_inquiry";
        AgentType target = AgentType.CUSTOMER;
        double bestScore = 0.3;

        for (Map.Entry<String, AgentType> entry : INTENT_ROUTES.entrySet()) {
            if (normalized.contains(entry.getKey())) {
                double score = 0.75 + (entry.getKey().length() * 0.01);
                if (score > bestScore) {
                    bestScore = Math.min(score, 0.98);
                    bestIntent = entry.getKey();
                    target = entry.getValue();
                }
            }
        }

        return new IntentClassification(
                bestIntent,
                target,
                bestScore,
                "Matched keyword '" + bestIntent + "' to " + target.getServiceName()
        );
    }
}
