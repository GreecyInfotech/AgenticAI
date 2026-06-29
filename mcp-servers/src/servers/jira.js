import { createMcpServer } from '../common/create-server.js';

const PORT = process.env.MCP_JIRA_PORT || 8506;
const tickets = [];

createMcpServer({
  name: 'jira',
  description: 'Jira integration for escalation and case management',
  port: PORT,
  tools: [
    {
      name: 'create_ticket',
      description: 'Create a Jira escalation ticket',
      inputSchema: {
        type: 'object',
        properties: {
          customerId: { type: 'string' },
          summary: { type: 'string' },
          priority: { type: 'string' },
          queue: { type: 'string' }
        },
        required: ['summary']
      },
      handler: async (input) => {
        const ticket = {
          ticketId: `JIRA-${Date.now()}`,
          key: `BFSI-${tickets.length + 1001}`,
          status: 'OPEN',
          createdAt: new Date().toISOString(),
          ...input
        };
        tickets.push(ticket);
        return ticket;
      }
    },
    {
      name: 'get_ticket',
      description: 'Get ticket by ID or key',
      inputSchema: { type: 'object', properties: { ticketId: { type: 'string' } }, required: ['ticketId'] },
      handler: async ({ ticketId }) => {
        const ticket = tickets.find(t => t.ticketId === ticketId || t.key === ticketId);
        return ticket ?? { ticketId, status: 'NOT_FOUND' };
      }
    },
    {
      name: 'list_open_tickets',
      description: 'List open escalation tickets',
      inputSchema: { type: 'object', properties: { queue: { type: 'string' } } },
      handler: async ({ queue }) => {
        let open = tickets.filter(t => t.status === 'OPEN');
        if (queue) open = open.filter(t => t.queue === queue);
        return { count: open.length, tickets: open };
      }
    }
  ]
});
