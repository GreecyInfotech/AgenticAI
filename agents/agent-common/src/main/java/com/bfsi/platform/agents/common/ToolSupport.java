package com.bfsi.platform.agents.common;

import com.bfsi.platform.tools.common.ToolContextKeys;
import com.bfsi.platform.tools.common.ToolInvocationResult;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public final class ToolSupport {

    private ToolSupport() {}

    public static void record(AgentResponse response, ToolInvocationResult result) {
        if (response == null || result == null) return;

        @SuppressWarnings("unchecked")
        List<Map<String, Object>> invocations = (List<Map<String, Object>>) response.getData()
            .computeIfAbsent(ToolContextKeys.INVOCATIONS, k -> new ArrayList<>());

        Map<String, Object> entry = new HashMap<>();
        entry.put("serverId", result.getServerId());
        entry.put("toolName", result.getToolName());
        entry.put("success", result.isSuccess());
        entry.put("latencyMs", result.getLatencyMs());
        if (result.isSuccess()) {
            entry.put("data", result.getData());
        } else {
            entry.put("error", result.getError());
        }
        invocations.add(entry);
    }
}
