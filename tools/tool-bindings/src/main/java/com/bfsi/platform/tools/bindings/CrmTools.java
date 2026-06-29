package com.bfsi.platform.tools.bindings;

import com.bfsi.platform.tools.common.ToolExecutor;
import com.bfsi.platform.tools.common.ToolInvocationResult;
import org.springframework.stereotype.Component;

import java.util.Map;

@Component
public class CrmTools extends AbstractToolBinding {

    private static final String SERVER = "crm";

    public CrmTools(ToolExecutor executor) {
        super(executor);
    }

    public ToolInvocationResult getCustomerProfile(String customerId) {
        return call(SERVER, "get_customer_profile", args("customerId", customerId));
    }

    public ToolInvocationResult getRelationshipSummary(String customerId) {
        return call(SERVER, "get_relationship_summary", args("customerId", customerId));
    }

    public ToolInvocationResult searchCustomers(String query) {
        return call(SERVER, "search_customers", args("query", query));
    }
}
