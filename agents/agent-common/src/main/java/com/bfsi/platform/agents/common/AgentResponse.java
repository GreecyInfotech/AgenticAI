package com.bfsi.platform.agents.common;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class AgentResponse {

    private String requestId;
    private AgentType agentType;
    private AgentStatus status;
    private String message;
    private Map<String, Object> data = new HashMap<>();
    private List<AgentType> nextAgents = new ArrayList<>();
    private double confidence;
    private boolean requiresEscalation;
    private List<AuditEntry> auditTrail = new ArrayList<>();

    public static AgentResponse success(AgentType type, String requestId, String message) {
        AgentResponse response = new AgentResponse();
        response.setAgentType(type);
        response.setRequestId(requestId);
        response.setStatus(AgentStatus.SUCCESS);
        response.setMessage(message);
        response.setConfidence(1.0);
        return response;
    }

    public static AgentResponse pending(AgentType type, String requestId, String message) {
        AgentResponse response = new AgentResponse();
        response.setAgentType(type);
        response.setRequestId(requestId);
        response.setStatus(AgentStatus.PENDING);
        response.setMessage(message);
        return response;
    }

    public static AgentResponse failed(AgentType type, String requestId, String message) {
        AgentResponse response = new AgentResponse();
        response.setAgentType(type);
        response.setRequestId(requestId);
        response.setStatus(AgentStatus.FAILED);
        response.setMessage(message);
        return response;
    }

    public String getRequestId() {
        return requestId;
    }

    public void setRequestId(String requestId) {
        this.requestId = requestId;
    }

    public AgentType getAgentType() {
        return agentType;
    }

    public void setAgentType(AgentType agentType) {
        this.agentType = agentType;
    }

    public AgentStatus getStatus() {
        return status;
    }

    public void setStatus(AgentStatus status) {
        this.status = status;
    }

    public String getMessage() {
        return message;
    }

    public void setMessage(String message) {
        this.message = message;
    }

    public Map<String, Object> getData() {
        return data;
    }

    public void setData(Map<String, Object> data) {
        this.data = data != null ? data : new HashMap<>();
    }

    public List<AgentType> getNextAgents() {
        return nextAgents;
    }

    public void setNextAgents(List<AgentType> nextAgents) {
        this.nextAgents = nextAgents != null ? nextAgents : new ArrayList<>();
    }

    public double getConfidence() {
        return confidence;
    }

    public void setConfidence(double confidence) {
        this.confidence = confidence;
    }

    public boolean isRequiresEscalation() {
        return requiresEscalation;
    }

    public void setRequiresEscalation(boolean requiresEscalation) {
        this.requiresEscalation = requiresEscalation;
    }

    public List<AuditEntry> getAuditTrail() {
        return auditTrail;
    }

    public void setAuditTrail(List<AuditEntry> auditTrail) {
        this.auditTrail = auditTrail != null ? auditTrail : new ArrayList<>();
    }

    public AgentResponse withData(String key, Object value) {
        this.data.put(key, value);
        return this;
    }

    public AgentResponse withNextAgent(AgentType agent) {
        this.nextAgents.add(agent);
        return this;
    }
}
