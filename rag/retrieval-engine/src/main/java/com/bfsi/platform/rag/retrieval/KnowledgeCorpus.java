package com.bfsi.platform.rag.retrieval;

import com.bfsi.platform.agents.common.AgentType;
import com.bfsi.platform.rag.common.DocumentInput;
import com.bfsi.platform.rag.common.IngestRequest;
import org.springframework.stereotype.Component;

import java.util.ArrayList;
import java.util.EnumMap;
import java.util.List;
import java.util.Map;

@Component
public class KnowledgeCorpus {

    private static final Map<AgentType, String> DESCRIPTIONS = Map.ofEntries(
        Map.entry(AgentType.INTENT, "Intent taxonomy and agent routing rules"),
        Map.entry(AgentType.CUSTOMER, "Customer FAQs and self-service policies"),
        Map.entry(AgentType.KYC, "RBI KYC Master Direction and identity verification"),
        Map.entry(AgentType.AML, "PMLA Act, PEP screening, and STR guidance"),
        Map.entry(AgentType.FRAUD, "Fraud typologies and transaction monitoring"),
        Map.entry(AgentType.LOAN, "RBI fair lending and loan eligibility policies"),
        Map.entry(AgentType.UNDERWRITING, "IRDAI underwriting and risk assessment"),
        Map.entry(AgentType.CLAIM, "Claims adjudication and coverage procedures"),
        Map.entry(AgentType.COMPLIANCE, "RBI, IRDAI, GDPR, and PMLA regulatory corpus"),
        Map.entry(AgentType.AUDIT, "AI decision audit logging standards"),
        Map.entry(AgentType.RECOMMENDATION, "Product suitability and recommendation rules"),
        Map.entry(AgentType.PORTFOLIO, "Wealth management and SEBI advisory guidelines"),
        Map.entry(AgentType.ESCALATION, "Human handoff playbooks and SLA policies"),
        Map.entry(AgentType.NOTIFICATION, "Regulatory customer communication templates")
    );

    private static final Map<AgentType, String> KNOWLEDGE = buildKnowledge();

    public String descriptionFor(AgentType type) {
        return DESCRIPTIONS.getOrDefault(type, "BFSI knowledge base");
    }

    public IngestRequest buildSeedCorpus() {
        IngestRequest request = new IngestRequest();
        request.setRequestId("seed-corpus-v1");
        List<DocumentInput> docs = new ArrayList<>();
        for (AgentType type : AgentType.values()) {
            DocumentInput doc = new DocumentInput();
            doc.setAgentType(type);
            doc.setDocumentId("seed-" + type.name().toLowerCase());
            doc.setTitle(DESCRIPTIONS.get(type));
            doc.setContent(KNOWLEDGE.get(type));
            docs.add(doc);
        }
        request.setDocuments(docs);
        return request;
    }

    private static Map<AgentType, String> buildKnowledge() {
        Map<AgentType, String> k = new EnumMap<>(AgentType.class);

        k.put(AgentType.INTENT,
            "Intent classification routes customer queries to domain agents. Loan keywords: home loan, personal loan, EMI, mortgage. "
            + "KYC keywords: identity, document, PAN, Aadhaar, verification. AML keywords: sanctions, PEP, suspicious transaction. "
            + "Fraud keywords: unauthorized, stolen card, velocity. Claim keywords: insurance claim, coverage, hospitalization. "
            + "Compliance keywords: RBI, GDPR, regulation, breach. Portfolio keywords: investment, mutual fund, rebalancing. "
            + "Low confidence below 0.6 triggers escalation to human agent.");

        k.put(AgentType.CUSTOMER,
            "Customer self-service policies: Account balance inquiries require customer ID verification. Profile updates need OTP authentication. "
            + "Product information covers savings accounts (3.5-4% interest), fixed deposits (6-7%), and recurring deposits. "
            + "Branch services include cheque book requests, address change, and nominee updates per RBI guidelines. "
            + "Digital banking support covers UPI, NEFT, RTGS, and IMPS transaction status. Complaint resolution SLA is 7 business days.");

        k.put(AgentType.KYC,
            "RBI KYC Master Direction 2016 requires identity verification for all account holders. Acceptable documents: PAN card (mandatory), "
            + "Aadhaar (voluntary with consent), passport, voter ID, driving license. Video KYC permitted for low-risk customers. "
            + "Periodic KYC update required every 2 years for high-risk, 10 years for low-risk. CKYC registry integration mandatory. "
            + "Non-resident Indians require passport and overseas address proof. Minor accounts need guardian KYC.");

        k.put(AgentType.AML,
            "Prevention of Money Laundering Act (PMLA) 2002 requires Customer Due Diligence (CDD) and Enhanced Due Diligence (EDD) for high-risk. "
            + "PEP screening against UN, OFAC, EU sanctions lists. Suspicious Transaction Reports (STR) filed within 7 days to FIU-IND. "
            + "Cash transactions above INR 10 lakhs require reporting. Structuring detection: multiple transactions below threshold. "
            + "Wire transfers to high-risk jurisdictions trigger enhanced screening. Record retention minimum 5 years.");

        k.put(AgentType.FRAUD,
            "Fraud detection monitors velocity (max 5 transactions per hour), geolocation mismatch, device fingerprint changes, and amount anomalies. "
            + "Card-not-present fraud: 3D Secure mandatory above INR 2000. Account takeover indicators: password reset + immediate large transfer. "
            + "Mule account patterns: rapid in-out transfers within 24 hours. Synthetic identity fraud: mismatched PAN-Aadhaar linkage. "
            + "Real-time block recommended when fraud score exceeds 0.85. Customer notification within 30 minutes of confirmed fraud.");

        k.put(AgentType.LOAN,
            "RBI fair lending practices prohibit discrimination based on gender, religion, or caste. Home loan eligibility: minimum credit score 650, "
            + "maximum EMI 50% of net monthly income, LTV ratio up to 80% for amounts below 30 lakhs. Personal loan: max 24x monthly salary, "
            + "interest rates 10.5-18% based on credit profile. Prepayment penalty capped at 2% per RBI circular. "
            + "Loan rejection reasons must be communicated within 30 days. Co-applicant income can be clubbed for eligibility.");

        k.put(AgentType.UNDERWRITING,
            "IRDAI underwriting guidelines require risk-based premium calculation. Life insurance: medical examination mandatory above 50 lakhs sum assured. "
            + "Health insurance: pre-existing disease waiting period max 48 months. Motor insurance: IDV depreciation per IRDAI schedule. "
            + "Smoker loading up to 50% on life premiums. Occupation class 1-4 risk categorization. "
            + "Reinsurance mandatory when sum assured exceeds company retention limit. Policy rejection must cite specific exclusion clause.");

        k.put(AgentType.CLAIM,
            "Claims processing SLA: intimation within 24 hours, survey within 48 hours, settlement within 30 days. Health claims require "
            + "hospital bills, discharge summary, and policy copy. Motor claims: FIR mandatory for theft, photographs for accident. "
            + "Life insurance death claims: death certificate, policy bond, nominee ID proof. Fraud indicators: claim within 30 days of policy inception, "
            + "inconsistent medical records. Partial rejection requires detailed reasoning per IRDAI Protection of Policyholders' Interests Regulations.");

        k.put(AgentType.COMPLIANCE,
            "Regulatory compliance framework covers RBI banking regulations, IRDAI insurance norms, SEBI investment advisory, GDPR data protection, "
            + "and PMLA anti-money laundering. Data breach under GDPR Article 33 requires notification within 72 hours. "
            + "Cross-border data transfer requires RBI approval under FEMA. AI governance: model decisions must be explainable and auditable. "
            + "Fair lending: no algorithmic bias in credit decisions. Consent management for marketing communications per TRAI DND regulations.");

        k.put(AgentType.AUDIT,
            "AI decision audit trail must capture: request ID, agent type, input parameters, decision outcome, confidence score, timestamp, and model version. "
            + "Audit logs retained minimum 7 years per RBI cybersecurity framework. Immutable storage recommended. "
            + "Regulatory examination readiness: produce audit trail within 24 hours. PII must be masked in audit logs. "
            + "Escalation events require separate audit category. Quarterly audit review of AI agent decisions mandatory.");

        k.put(AgentType.RECOMMENDATION,
            "Product recommendation must follow suitability assessment per SEBI guidelines. Risk profiling: conservative, moderate, aggressive categories. "
            + "Mutual fund recommendations require KYC and risk profile completion. Insurance cross-sell only after needs analysis. "
            + "Prohibited: recommending high-risk products to conservative investors. Commission disclosure mandatory. "
            + "Cooling-off period of 15 days for unit-linked insurance plans. Compare minimum 3 products before recommendation.");

        k.put(AgentType.PORTFOLIO,
            "Portfolio advisory per SEBI RIA regulations requires registration. Asset allocation: equity 30-70% based on risk profile and age. "
            + "Rebalancing trigger when allocation drifts 5% from target. Tax harvesting opportunities in equity LTCG above 1 lakh exemption. "
            + "Diversification across minimum 5 sectors. ESG funds available for sustainable investing preference. "
            + "SIP recommendations based on goal-based planning: retirement, education, home purchase.");

        k.put(AgentType.ESCALATION,
            "Escalation triggers: confidence below 0.6, customer explicitly requests human agent, compliance violation detected, fraud score above 0.85, "
            + "or regulatory matter requiring licensed professional. SLA: acknowledge within 15 minutes, assign within 2 hours, resolve within 24 hours. "
            + "Priority levels: P1 critical (fraud, data breach), P2 high (loan rejection appeal), P3 medium (general complaint). "
            + "Handoff package includes full conversation history, agent trail, and customer profile summary.");

        k.put(AgentType.NOTIFICATION,
            "Customer notification templates per regulatory requirements. Transaction alerts: SMS/email within 5 minutes of debit/credit. "
            + "Loan approval/rejection notification within 24 hours. KYC expiry reminder 30 days before due date. "
            + "Marketing communications require explicit opt-in per TRAI regulations. Data breach notification template per GDPR Article 34. "
            + "Claim status updates at each processing stage. Multi-language support for Hindi, English, and regional languages.");

        return k;
    }
}
