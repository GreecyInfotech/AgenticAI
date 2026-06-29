package com.bfsi.platform.bff.common.dto;

import jakarta.validation.constraints.NotBlank;
import java.util.HashMap;
import java.util.Map;

public class ChatRequest {

    private String requestId;
    private String sessionId;

    @NotBlank
    private String message;

    private String customerId;
    private Map<String, Object> context = new HashMap<>();

    public String getRequestId() { return requestId; }
    public void setRequestId(String requestId) { this.requestId = requestId; }
    public String getSessionId() { return sessionId; }
    public void setSessionId(String sessionId) { this.sessionId = sessionId; }
    public String getMessage() { return message; }
    public void setMessage(String message) { this.message = message; }
    public String getCustomerId() { return customerId; }
    public void setCustomerId(String customerId) { this.customerId = customerId; }
    public Map<String, Object> getContext() { return context; }
    public void setContext(Map<String, Object> context) { this.context = context != null ? context : new HashMap<>(); }
}
