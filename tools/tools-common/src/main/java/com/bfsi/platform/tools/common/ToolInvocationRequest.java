package com.bfsi.platform.tools.common;

import java.util.HashMap;
import java.util.Map;

public class ToolInvocationRequest {

    private String requestId;
    private String serverId;
    private String toolName;
    private Map<String, Object> arguments = new HashMap<>();

    public String getRequestId() { return requestId; }
    public void setRequestId(String requestId) { this.requestId = requestId; }
    public String getServerId() { return serverId; }
    public void setServerId(String serverId) { this.serverId = serverId; }
    public String getToolName() { return toolName; }
    public void setToolName(String toolName) { this.toolName = toolName; }
    public Map<String, Object> getArguments() { return arguments; }
    public void setArguments(Map<String, Object> arguments) {
        this.arguments = arguments != null ? arguments : new HashMap<>();
    }
}
