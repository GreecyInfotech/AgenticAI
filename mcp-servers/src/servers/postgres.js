import { createMcpServer } from '../common/create-server.js';

const PORT = process.env.MCP_POSTGRES_PORT || 8503;

const auditStore = [];

createMcpServer({
  name: 'postgres',
  description: 'PostgreSQL data access for audit trails and platform records',
  port: PORT,
  tools: [
    {
      name: 'log_audit_entry',
      description: 'Persist an immutable audit log entry',
      inputSchema: {
        type: 'object',
        properties: {
          requestId: { type: 'string' },
          agentType: { type: 'string' },
          action: { type: 'string' },
          decision: { type: 'string' },
          metadata: { type: 'object' }
        },
        required: ['requestId', 'agentType', 'action', 'decision']
      },
      handler: async (input) => {
        const entry = {
          auditId: `AUD-${Date.now()}`,
          ...input,
          timestamp: new Date().toISOString(),
          immutable: true
        };
        auditStore.push(entry);
        return { stored: true, entry, totalEntries: auditStore.length };
      }
    },
    {
      name: 'get_audit_trail',
      description: 'Retrieve audit trail by request ID',
      inputSchema: { type: 'object', properties: { requestId: { type: 'string' } }, required: ['requestId'] },
      handler: async ({ requestId }) => ({
        requestId,
        entries: auditStore.filter(e => e.requestId === requestId)
      })
    },
    {
      name: 'query_records',
      description: 'Query platform records (in-memory store; wire to Postgres in production)',
      inputSchema: {
        type: 'object',
        properties: { table: { type: 'string' }, filter: { type: 'object' } },
        required: ['table']
      },
      handler: async ({ table, filter = {} }) => ({
        table,
        filter,
        rows: table === 'audit_log' ? auditStore : [],
        note: 'Connect to POSTGRES_HOST for production persistence'
      })
    }
  ]
});
