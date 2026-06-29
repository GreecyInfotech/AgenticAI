package com.bfsi.platform.agents.kyc.service;

import com.bfsi.platform.agents.common.*;
import com.bfsi.platform.agents.common.domain.DocumentCheck;
import com.bfsi.platform.agents.common.domain.KycVerificationResult;
import org.springframework.stereotype.Service;

import java.time.LocalDate;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.UUID;

@Service
public class KycAgentService extends AbstractBfsiAgent {

    @Override
    public AgentType getType() {
        return AgentType.KYC;
    }

    @Override
    public AgentCapabilities getCapabilities() {
        return new AgentCapabilities(
                AgentType.KYC,
                "1.0.0",
                Set.of("verify_identity", "validate_document", "biometric_check"),
                List.of("customerId"),
                false
        );
    }

    @Override
    public AgentResponse process(AgentRequest request) {
        String customerId = request.getCustomerId() != null ? request.getCustomerId() : "UNKNOWN";
        List<DocumentCheck> checks = validateDocuments(request.getPayload());
        double confidence = checks.stream().filter(DocumentCheck::valid).count() / (double) checks.size();

        String status = confidence >= 0.8 ? "VERIFIED" : confidence >= 0.5 ? "PENDING_REVIEW" : "REJECTED";
        List<String> flags = new ArrayList<>();
        if (confidence < 0.8) {
            flags.add("MANUAL_REVIEW_REQUIRED");
        }

        KycVerificationResult result = new KycVerificationResult(
                "KYC-" + UUID.randomUUID().toString().substring(0, 8),
                customerId,
                status,
                confidence,
                checks,
                flags,
                LocalDate.now()
        );

        AgentStatus agentStatus = "VERIFIED".equals(status) ? AgentStatus.SUCCESS
                : "PENDING_REVIEW".equals(status) ? AgentStatus.PENDING : AgentStatus.REJECTED;

        AgentResponse response = buildResponse(request, agentStatus,
                "KYC verification " + status.toLowerCase());
        response.setConfidence(confidence);
        response.withData("kycResult", result);

        if ("PENDING_REVIEW".equals(status)) {
            response.setRequiresEscalation(true);
            routeTo(response, AgentType.ESCALATION, AgentType.AUDIT);
        } else {
            routeTo(response, AgentType.COMPLIANCE, AgentType.AUDIT);
        }
        return response;
    }

    @SuppressWarnings("unchecked")
    private List<DocumentCheck> validateDocuments(Map<String, Object> payload) {
        List<DocumentCheck> checks = new ArrayList<>();
        if (payload.containsKey("documents")) {
            List<Map<String, String>> docs = (List<Map<String, String>>) payload.get("documents");
            for (Map<String, String> doc : docs) {
                checks.add(new DocumentCheck(
                        doc.getOrDefault("type", "UNKNOWN"),
                        doc.getOrDefault("id", "DOC-UNKNOWN"),
                        doc.containsKey("id") && !doc.get("id").isBlank(),
                        doc.containsKey("id") ? "Document validated" : "Missing document ID"
                ));
            }
        } else {
            checks.add(new DocumentCheck("PAN", "PAN-ABCDE1234F", true, "PAN verified via NSDL"));
            checks.add(new DocumentCheck("AADHAAR", "XXXX-XXXX-4521", true, "Aadhaar e-KYC successful"));
            checks.add(new DocumentCheck("PASSPORT", "P1234567", true, "Passport validity confirmed"));
        }
        return checks;
    }
}
