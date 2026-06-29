package com.bfsi.platform.tools.bindings;

import com.bfsi.platform.tools.common.ToolExecutor;
import com.bfsi.platform.tools.common.ToolInvocationResult;
import org.springframework.stereotype.Component;

import java.util.Map;

@Component
public class CoreBankingTools extends AbstractToolBinding {

    private static final String SERVER = "core-banking";

    public CoreBankingTools(ToolExecutor executor) {
        super(executor);
    }

    public ToolInvocationResult getAccountBalance(String accountId) {
        return call(SERVER, "get_account_balance", args("accountId", accountId));
    }

    public ToolInvocationResult getCustomerAccounts(String customerId) {
        return call(SERVER, "get_customer_accounts", args("customerId", customerId));
    }

    public ToolInvocationResult getTransactionHistory(String accountId, int limit) {
        return call(SERVER, "get_transaction_history", Map.of("accountId", accountId, "limit", limit));
    }

    public ToolInvocationResult transferFunds(String fromAccount, String toAccount, double amount) {
        return call(SERVER, "transfer_funds", Map.of(
            "fromAccount", fromAccount,
            "toAccount", toAccount,
            "amount", amount
        ));
    }
}
