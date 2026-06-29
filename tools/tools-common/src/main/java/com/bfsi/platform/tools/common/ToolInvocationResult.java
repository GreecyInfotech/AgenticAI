package com.bfsi.platform.tools.common;

import java.util.HashMap;
import java.util.Map;

public class ToolInvocationResult {

    private String requestId;
    private String serverId;
    private String toolName;
    private boolean success;
    private Map<String, Object> data = new HashMap<>();
    private String error;
    private long latencyMs;

    public static ToolInvocationResult ok(String serverId, String toolName, Map<String, Object> data, long latencyMs) {
        ToolInvocationResult result = new ToolInvocationResult();
        result.setServerId(serverId);
        result.setToolName(toolName);
        result.setSuccess(true);
        result.setData(data);
        result.setLatencyMs(latencyMs);
        return result;
    }

    public static ToolInvocationResult failed(String serverId, String toolName, String error, long latencyMs) {
        ToolInvocationResult result = new ToolInvocationResult();
        result.setServerId(serverId);
        result.setToolName(toolName);
        result.setSuccess(false);
        result.setError(error);
        result.setLatencyMs(latencyMs);
        return result;
    }

    public String getRequestId() { return requestId; }
    public void setRequestId(String requestId) { this.requestId = requestId; }
    public String getServerId() { return serverId; }
    public void setServerId(String serverId) { this.serverId = serverId; }
    public String getToolName() { return toolName; }
    public void setToolName(String toolName) { this.toolName = toolName; }
    public boolean isSuccess() { return success; }
    public void setSuccess(boolean success) { this.success = success; }
    public Map<String, Object> getData() { return data; }
    public void setData(Map<String, Object> data) {
        this.data = data != null ? data : new HashMap<>();
    }
    public String getError() { return error; }
    public void setError(String error) { this.error = error; }
    public long getLatencyMs() { return latencyMs; }
    public void setLatencyMs(long latencyMs) { this.latencyMs = latencyMs; }
}
