package com.bfsi.platform.agents.common;

/**
 * All domain agents in the BFSI platform.
 */
public enum AgentType {
    INTENT("intent-agent", "Detect user intent and route requests"),
    CUSTOMER("customer-agent", "Customer profile, account details, relationship summary"),
    KYC("kyc-agent", "Identity verification and document validation"),
    AML("aml-agent", "Anti-money laundering checks"),
    FRAUD("fraud-agent", "Transaction and identity fraud detection"),
    LOAN("loan-agent", "Loan eligibility and recommendation"),
    UNDERWRITING("underwriting-agent", "Insurance underwriting analysis"),
    CLAIM("claim-agent", "Claims validation and processing"),
    COMPLIANCE("compliance-agent", "Regulatory policy checks"),
    AUDIT("audit-agent", "Immutable audit trail and AI decision logging"),
    RECOMMENDATION("recommendation-agent", "Personalized financial product recommendations"),
    PORTFOLIO("portfolio-agent", "Investment and wealth advisory"),
    ESCALATION("escalation-agent", "Human handoff for complex cases"),
    NOTIFICATION("notification-agent", "Email, SMS, push notifications");

    private final String serviceName;
    private final String description;

    AgentType(String serviceName, String description) {
        this.serviceName = serviceName;
        this.description = description;
    }

    public String getServiceName() {
        return serviceName;
    }

    public String getDescription() {
        return description;
    }
}
