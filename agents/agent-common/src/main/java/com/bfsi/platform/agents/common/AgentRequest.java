package com.bfsi.platform.agents.common;

import jakarta.validation.constraints.NotBlank;
import java.util.HashMap;
import java.util.Map;

public class AgentRequest {

    @NotBlank
    private String requestId;

    private String sessionId;
    private String customerId;
    private AgentType targetAgent;

    @NotBlank
    private String userMessage;

    private Map<String, Object> context = new HashMap<>();
    private Map<String, Object> payload = new HashMap<>();

    public String getRequestId() {
        return requestId;
    }

    public void setRequestId(String requestId) {
        this.requestId = requestId;
    }

    public String getSessionId() {
        return sessionId;
    }

    public void setSessionId(String sessionId) {
        this.sessionId = sessionId;
    }

    public String getCustomerId() {
        return customerId;
    }

    public void setCustomerId(String customerId) {
        this.customerId = customerId;
    }

    public AgentType getTargetAgent() {
        return targetAgent;
    }

    public void setTargetAgent(AgentType targetAgent) {
        this.targetAgent = targetAgent;
    }

    public String getUserMessage() {
        return userMessage;
    }

    public void setUserMessage(String userMessage) {
        this.userMessage = userMessage;
    }

    public Map<String, Object> getContext() {
        return context;
    }

    public void setContext(Map<String, Object> context) {
        this.context = context != null ? context : new HashMap<>();
    }

    public Map<String, Object> getPayload() {
        return payload;
    }

    public void setPayload(Map<String, Object> payload) {
        this.payload = payload != null ? payload : new HashMap<>();
    }
}
