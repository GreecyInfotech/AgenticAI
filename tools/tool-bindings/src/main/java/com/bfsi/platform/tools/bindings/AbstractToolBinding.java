package com.bfsi.platform.tools.bindings;

import com.bfsi.platform.tools.common.ToolExecutor;
import com.bfsi.platform.tools.common.ToolInvocationResult;

import java.util.HashMap;
import java.util.Map;

abstract class AbstractToolBinding {

    protected final ToolExecutor executor;

    protected AbstractToolBinding(ToolExecutor executor) {
        this.executor = executor;
    }

    protected ToolInvocationResult call(String serverId, String toolName, Map<String, Object> args) {
        return executor.invoke(serverId, toolName, args != null ? args : Map.of());
    }

    protected Map<String, Object> args(String key, Object value) {
        Map<String, Object> map = new HashMap<>();
        map.put(key, value);
        return map;
    }

    protected Map<String, Object> args(Map<String, Object> map) {
        return map != null ? map : Map.of();
    }
}
