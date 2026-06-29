package com.bfsi.platform.tools.bindings;

import com.bfsi.platform.tools.common.ToolExecutor;
import com.bfsi.platform.tools.common.ToolInvocationResult;
import org.springframework.stereotype.Component;

import java.util.Map;

@Component
public class EscalationTools extends AbstractToolBinding {

    private static final String SERVER = "jira";

    public EscalationTools(ToolExecutor executor) {
        super(executor);
    }

    public ToolInvocationResult createTicket(String customerId, String summary, String priority, String queue) {
        return call(SERVER, "create_ticket", Map.of(
            "customerId", customerId != null ? customerId : "",
            "summary", summary,
            "priority", priority != null ? priority : "P3_NORMAL",
            "queue", queue != null ? queue : "GENERAL_SUPPORT"
        ));
    }

    public ToolInvocationResult getTicket(String ticketId) {
        return call(SERVER, "get_ticket", args("ticketId", ticketId));
    }

    public ToolInvocationResult listOpenTickets(String queue) {
        return call(SERVER, "list_open_tickets", queue != null ? args("queue", queue) : Map.of());
    }
}
