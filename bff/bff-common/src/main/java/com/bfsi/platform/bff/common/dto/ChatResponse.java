package com.bfsi.platform.bff.common.dto;

import com.bfsi.platform.agents.common.AgentResponse;
import java.util.List;

public class ChatResponse {

    private String requestId;
    private String reply;
    private String status;
    private boolean requiresEscalation;
    private List<AgentResponse> agentTrail;

    public String getRequestId() { return requestId; }
    public void setRequestId(String requestId) { this.requestId = requestId; }
    public String getReply() { return reply; }
    public void setReply(String reply) { this.reply = reply; }
    public String getStatus() { return status; }
    public void setStatus(String status) { this.status = status; }
    public boolean isRequiresEscalation() { return requiresEscalation; }
    public void setRequiresEscalation(boolean requiresEscalation) { this.requiresEscalation = requiresEscalation; }
    public List<AgentResponse> getAgentTrail() { return agentTrail; }
    public void setAgentTrail(List<AgentResponse> agentTrail) { this.agentTrail = agentTrail; }
}
