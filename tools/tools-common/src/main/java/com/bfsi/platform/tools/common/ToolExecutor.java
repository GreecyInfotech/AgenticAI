package com.bfsi.platform.tools.common;

import java.util.Map;

public interface ToolExecutor {

    ToolInvocationResult invoke(String serverId, String toolName, Map<String, Object> arguments);
}
