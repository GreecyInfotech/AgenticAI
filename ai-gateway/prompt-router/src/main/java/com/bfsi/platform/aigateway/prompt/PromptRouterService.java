package com.bfsi.platform.aigateway.prompt;

import com.bfsi.platform.aigateway.common.ChatCompletionRequest;
import com.bfsi.platform.aigateway.common.ChatMessage;
import com.bfsi.platform.aigateway.common.GatewayException;
import com.bfsi.platform.aigateway.common.PromptTemplate;
import jakarta.annotation.PostConstruct;
import org.springframework.stereotype.Service;

import java.util.*;
import java.util.concurrent.ConcurrentHashMap;

@Service
public class PromptRouterService {

  private final Map<String, PromptTemplate> templates = new ConcurrentHashMap<>();

  @PostConstruct
  void init() {
    registerDefaults();
  }

  public PromptTemplate getTemplate(String templateId) {
    PromptTemplate template = templates.get(templateId);
    if (template == null) {
      throw new GatewayException("PROMPT_NOT_FOUND", "Prompt template not found: " + templateId);
    }
    return template;
  }

  public List<PromptTemplate> listTemplates() {
    return templates.values().stream()
        .sorted(Comparator.comparing(PromptTemplate::id))
        .toList();
  }

  public String resolveTemplateId(ChatCompletionRequest request) {
    if (request.getPromptTemplateId() != null && !request.getPromptTemplateId().isBlank()) {
      return request.getPromptTemplateId();
    }
    if (request.getAgentType() != null) {
      String byAgent = "agent-" + request.getAgentType().toLowerCase();
      if (templates.containsKey(byAgent)) {
        return byAgent;
      }
    }
    return "bfsi-general";
  }

  public List<ChatMessage> applyTemplate(ChatCompletionRequest request) {
    String templateId = resolveTemplateId(request);
    PromptTemplate template = getTemplate(templateId);
    request.setPromptTemplateId(templateId);

    String systemPrompt = substitute(template.systemPrompt(), request.getPromptVariables());
    String userPrompt = template.userPromptTemplate() != null
        ? substitute(template.userPromptTemplate(), request.getPromptVariables())
        : null;

    List<ChatMessage> messages = new ArrayList<>();
    messages.add(new ChatMessage("system", systemPrompt));

    if (userPrompt != null && !userPrompt.isBlank()) {
      messages.add(new ChatMessage("user", userPrompt));
    }

    for (ChatMessage msg : request.getMessages()) {
      if (!"system".equalsIgnoreCase(msg.role())) {
        messages.add(msg);
      }
    }
    return messages;
  }

  private String substitute(String template, Map<String, String> variables) {
    String result = template;
    for (Map.Entry<String, String> entry : variables.entrySet()) {
      result = result.replace("{{" + entry.getKey() + "}}", entry.getValue());
    }
    return result;
  }

  private void registerDefaults() {
    templates.put("bfsi-general", new PromptTemplate(
        "bfsi-general", "BFSI General Assistant", "GENERAL",
        "You are a compliant BFSI AI assistant. Follow RBI, AML, and GDPR guidelines. Never disclose PII without verification.",
        null, "1.0"
    ));
    templates.put("agent-intent", new PromptTemplate(
        "agent-intent", "Intent Classification", "INTENT",
        "Classify the user intent and map to the correct BFSI agent. Respond with intent, confidence, and target agent.",
        "User message: {{message}}", "1.0"
    ));
    templates.put("agent-kyc", new PromptTemplate(
        "agent-kyc", "KYC Verification", "KYC",
        "You are a KYC verification specialist. Validate identity documents per RBI KYC Master Direction.",
        "Customer ID: {{customerId}}\nDocuments: {{documents}}", "1.0"
    ));
    templates.put("agent-aml", new PromptTemplate(
        "agent-aml", "AML Screening", "AML",
        "You are an AML analyst. Screen for PEP, sanctions, and suspicious transaction patterns per PMLA Act.",
        "Customer ID: {{customerId}}\nTransaction: {{transaction}}", "1.0"
    ));
    templates.put("agent-fraud", new PromptTemplate(
        "agent-fraud", "Fraud Detection", "FRAUD",
        "You are a fraud detection analyst. Identify transaction anomalies, device fingerprint mismatches, and velocity violations.",
        "Transaction ID: {{transactionId}}\nContext: {{context}}", "1.0"
    ));
    templates.put("agent-loan", new PromptTemplate(
        "agent-loan", "Loan Eligibility", "LOAN",
        "You are a loan advisor. Assess eligibility based on credit score, income, and RBI fair lending practices.",
        "Customer ID: {{customerId}}\nRequested amount: {{amount}}", "1.0"
    ));
    templates.put("agent-compliance", new PromptTemplate(
        "agent-compliance", "Compliance Check", "COMPLIANCE",
        "You are a regulatory compliance officer. Check actions against RBI, IRDAI, GDPR, and PMLA frameworks.",
        "Regulation: {{regulation}}\nAction: {{action}}", "1.0"
    ));
    templates.put("agent-underwriting", new PromptTemplate(
        "agent-underwriting", "Insurance Underwriting", "UNDERWRITING",
        "You are an insurance underwriter. Assess risk, calculate premium, and determine coverage per IRDAI guidelines.",
        "Applicant: {{applicantId}}\nPolicy type: {{policyType}}", "1.0"
    ));
    templates.put("agent-claim", new PromptTemplate(
        "agent-claim", "Claims Processing", "CLAIM",
        "You are a claims adjuster. Validate coverage, assess claim amount, and identify fraud indicators.",
        "Claim ID: {{claimId}}\nPolicy ID: {{policyId}}", "1.0"
    ));
    templates.put("agent-recommendation", new PromptTemplate(
        "agent-recommendation", "Product Recommendation", "RECOMMENDATION",
        "You are a financial product advisor. Recommend suitable products based on customer segment and needs.",
        "Customer segment: {{segment}}\nNeeds: {{needs}}", "1.0"
    ));
    templates.put("agent-portfolio", new PromptTemplate(
        "agent-portfolio", "Portfolio Advisory", "PORTFOLIO",
        "You are a wealth management advisor. Analyze portfolio allocation and provide rebalancing recommendations.",
        "Customer ID: {{customerId}}\nRisk profile: {{riskProfile}}", "1.0"
    ));
  }
}
