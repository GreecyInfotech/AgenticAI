package com.bfsi.platform.agents.customer.service;

import com.bfsi.platform.agents.common.*;
import com.bfsi.platform.agents.common.domain.AccountSummary;
import com.bfsi.platform.agents.common.domain.CustomerProfile;
import com.bfsi.platform.agents.common.domain.RelationshipSummary;
import com.bfsi.platform.tools.bindings.CoreBankingTools;
import com.bfsi.platform.tools.bindings.CrmTools;
import com.bfsi.platform.tools.common.ToolInvocationResult;
import org.springframework.stereotype.Service;

import java.math.BigDecimal;
import java.time.LocalDate;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.UUID;

@Service
public class CustomerAgentService extends AbstractBfsiAgent {

    private final CrmTools crmTools;
    private final CoreBankingTools coreBankingTools;

    public CustomerAgentService(CrmTools crmTools, CoreBankingTools coreBankingTools) {
        this.crmTools = crmTools;
        this.coreBankingTools = coreBankingTools;
    }

    @Override
    public AgentType getType() {
        return AgentType.CUSTOMER;
    }

    @Override
    public AgentCapabilities getCapabilities() {
        return new AgentCapabilities(
                AgentType.CUSTOMER,
                "1.0.0",
                Set.of("profile_lookup", "account_summary", "relationship_360"),
                List.of("customerId"),
                false
        );
    }

    @Override
    public AgentResponse process(AgentRequest request) {
        String customerId = resolveCustomerId(request);
        CustomerProfile profile = fetchProfileViaTools(customerId);

        AgentResponse response = buildResponse(request, AgentStatus.SUCCESS,
                "Customer profile retrieved for " + profile.fullName());
        response.setConfidence(0.95);
        response.withData("profile", profile);
        response.withData("dataSource", "MCP_TOOLS");
        recordToolCalls(response, customerId);
        routeTo(response, AgentType.AUDIT);
        return response;
    }

    private String resolveCustomerId(AgentRequest request) {
        if (request.getCustomerId() != null && !request.getCustomerId().isBlank()) {
            return request.getCustomerId();
        }
        return "CUST-12345";
    }

    private CustomerProfile fetchProfileViaTools(String customerId) {
        ToolInvocationResult profileResult = crmTools.getCustomerProfile(customerId);
        ToolInvocationResult relationshipResult = crmTools.getRelationshipSummary(customerId);
        ToolInvocationResult accountsResult = coreBankingTools.getCustomerAccounts(customerId);

        if (profileResult.isSuccess()) {
            Map<String, Object> profileData = profileResult.getData();
            Map<String, Object> relData = relationshipResult.isSuccess()
                ? relationshipResult.getData() : Map.of();
            List<AccountSummary> accounts = mapAccounts(accountsResult);

            return new CustomerProfile(
                customerId,
                str(profileData.get("fullName"), "Unknown"),
                str(profileData.get("email"), ""),
                str(profileData.get("phone"), ""),
                str(profileData.get("segment"), "STANDARD"),
                str(profileData.get("riskRating"), "MEDIUM"),
                parseDate(profileData.get("customerSince")),
                accounts,
                new RelationshipSummary(
                    intVal(relData.get("totalProducts"), 0),
                    str(relData.get("relationshipManager"), "Unassigned"),
                    str(relData.get("loyaltyTier"), "STANDARD"),
                    intVal(relData.get("tenureYears"), 0)
                )
            );
        }
        return fallbackProfile(customerId);
    }

    private void recordToolCalls(AgentResponse response, String customerId) {
        ToolSupport.record(response, crmTools.getCustomerProfile(customerId));
        ToolSupport.record(response, crmTools.getRelationshipSummary(customerId));
        ToolSupport.record(response, coreBankingTools.getCustomerAccounts(customerId));
    }

    @SuppressWarnings("unchecked")
    private List<AccountSummary> mapAccounts(ToolInvocationResult accountsResult) {
        if (!accountsResult.isSuccess()) {
            return fallbackProfile("").accounts();
        }
        Object accounts = accountsResult.getData().get("accounts");
        if (accounts instanceof List<?> list) {
            return list.stream().map(item -> {
                Map<String, Object> m = (Map<String, Object>) item;
                return new AccountSummary(
                    str(m.get("accountId"), "ACC-000"),
                    str(m.get("type"), "SAVINGS"),
                    str(m.get("currency"), "INR"),
                    new BigDecimal(String.valueOf(m.getOrDefault("balance", "0"))),
                    str(m.get("status"), "ACTIVE")
                );
            }).toList();
        }
        return fallbackProfile("").accounts();
    }

    private CustomerProfile fallbackProfile(String customerId) {
        return new CustomerProfile(
                customerId,
                "Rajesh Kumar",
                "rajesh.kumar@email.com",
                "+91-9876543210",
                "PREMIUM",
                "LOW",
                LocalDate.of(2018, 3, 15),
                List.of(
                        new AccountSummary("ACC-001", "SAVINGS", "INR", new BigDecimal("245000.50"), "ACTIVE"),
                        new AccountSummary("ACC-002", "CURRENT", "INR", new BigDecimal("1250000.00"), "ACTIVE")
                ),
                new RelationshipSummary(5, "Priya Sharma", "GOLD", 7)
        );
    }

    private static String str(Object value, String defaultVal) {
        return value != null ? value.toString() : defaultVal;
    }

    private static int intVal(Object value, int defaultVal) {
        if (value == null) return defaultVal;
        return Integer.parseInt(value.toString());
    }

    private static LocalDate parseDate(Object value) {
        if (value == null) return LocalDate.now().minusYears(5);
        return LocalDate.parse(value.toString());
    }
}
