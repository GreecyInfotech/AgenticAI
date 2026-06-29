import { createMcpServer } from '../common/create-server.js';

const PORT = process.env.MCP_CORE_BANKING_PORT || 8501;

createMcpServer({
  name: 'core-banking',
  description: 'Core banking accounts, balances, and transactions',
  port: PORT,
  tools: [
    {
      name: 'get_account_balance',
      description: 'Get account balance by account ID',
      inputSchema: { type: 'object', properties: { accountId: { type: 'string' } }, required: ['accountId'] },
      handler: async ({ accountId }) => ({
        accountId,
        balance: 245000.50,
        currency: 'INR',
        status: 'ACTIVE',
        lastUpdated: new Date().toISOString()
      })
    },
    {
      name: 'get_customer_accounts',
      description: 'List all accounts for a customer',
      inputSchema: { type: 'object', properties: { customerId: { type: 'string' } }, required: ['customerId'] },
      handler: async ({ customerId }) => ({
        customerId,
        accounts: [
          { accountId: 'ACC-001', type: 'SAVINGS', balance: 245000.50, currency: 'INR' },
          { accountId: 'ACC-002', type: 'CURRENT', balance: 1250000.00, currency: 'INR' },
          { accountId: 'ACC-003', type: 'FIXED_DEPOSIT', balance: 500000.00, currency: 'INR' }
        ]
      })
    },
    {
      name: 'get_transaction_history',
      description: 'Get recent transactions for an account',
      inputSchema: {
        type: 'object',
        properties: { accountId: { type: 'string' }, limit: { type: 'number' } },
        required: ['accountId']
      },
      handler: async ({ accountId, limit = 5 }) => ({
        accountId,
        transactions: Array.from({ length: limit }, (_, i) => ({
          txnId: `TXN-${1000 + i}`,
          type: i % 2 === 0 ? 'CREDIT' : 'DEBIT',
          amount: (i + 1) * 5000,
          currency: 'INR',
          description: i % 2 === 0 ? 'Salary credit' : 'UPI payment',
          date: new Date(Date.now() - i * 86400000).toISOString()
        }))
      })
    },
    {
      name: 'transfer_funds',
      description: 'Initiate an internal fund transfer',
      inputSchema: {
        type: 'object',
        properties: {
          fromAccountId: { type: 'string' },
          toAccountId: { type: 'string' },
          amount: { type: 'number' }
        },
        required: ['fromAccountId', 'toAccountId', 'amount']
      },
      handler: async ({ fromAccountId, toAccountId, amount }) => ({
        transferId: `TRF-${Date.now()}`,
        fromAccountId,
        toAccountId,
        amount,
        status: 'PENDING_APPROVAL',
        message: 'Transfer initiated for processing'
      })
    }
  ]
});
