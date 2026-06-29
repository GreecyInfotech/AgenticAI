package com.bfsi.platform.tools.bindings;

import com.bfsi.platform.tools.common.ToolExecutor;
import com.bfsi.platform.tools.common.ToolInvocationResult;
import org.springframework.stereotype.Component;

import java.util.Map;

@Component
public class AuditTools extends AbstractToolBinding {

    private static final String SERVER = "postgres";

    public AuditTools(ToolExecutor executor) {
        super(executor);
    }

    public ToolInvocationResult logAuditEntry(String requestId, String agentType, String action,
                                              String decision, Map<String, Object> metadata) {
        return call(SERVER, "log_audit_entry", Map.of(
            "requestId", requestId,
            "agentType", agentType,
            "action", action,
            "decision", decision,
            "metadata", metadata != null ? metadata : Map.of()
        ));
    }

    public ToolInvocationResult getAuditTrail(String requestId) {
        return call(SERVER, "get_audit_trail", args("requestId", requestId));
    }

    public ToolInvocationResult queryRecords(String table, Map<String, Object> filter) {
        return call(SERVER, "query_records", Map.of("table", table, "filter", filter != null ? filter : Map.of()));
    }
}
