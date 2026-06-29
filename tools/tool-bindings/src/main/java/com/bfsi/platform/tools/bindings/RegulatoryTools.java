package com.bfsi.platform.tools.bindings;

import com.bfsi.platform.tools.common.ToolExecutor;
import com.bfsi.platform.tools.common.ToolInvocationResult;
import org.springframework.stereotype.Component;

import java.util.Map;

@Component
public class RegulatoryTools extends AbstractToolBinding {

    private static final String SERVER = "regulatory";

    public RegulatoryTools(ToolExecutor executor) {
        super(executor);
    }

    public ToolInvocationResult lookupRegulation(String framework) {
        return call(SERVER, "lookup_regulation", args("framework", framework));
    }

    public ToolInvocationResult checkCompliance(String framework, String action) {
        return call(SERVER, "check_compliance", Map.of("framework", framework, "action", action));
    }

    public ToolInvocationResult listFrameworks() {
        return call(SERVER, "list_frameworks", Map.of());
    }
}
