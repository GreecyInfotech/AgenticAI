import { createMcpServer } from '../common/create-server.js';

const PORT = process.env.MCP_EMAIL_PORT || 8505;
const sentMessages = [];

createMcpServer({
  name: 'email',
  description: 'Email and SMS notification delivery',
  port: PORT,
  tools: [
    {
      name: 'send_email',
      description: 'Send an email notification',
      inputSchema: {
        type: 'object',
        properties: {
          to: { type: 'string' },
          subject: { type: 'string' },
          body: { type: 'string' },
          templateId: { type: 'string' }
        },
        required: ['to', 'subject', 'body']
      },
      handler: async (input) => {
        const msg = {
          notificationId: `EMAIL-${Date.now()}`,
          channel: 'EMAIL',
          status: 'SENT',
          sentAt: new Date().toISOString(),
          ...input
        };
        sentMessages.push(msg);
        return msg;
      }
    },
    {
      name: 'send_sms',
      description: 'Send an SMS notification',
      inputSchema: {
        type: 'object',
        properties: { to: { type: 'string' }, message: { type: 'string' } },
        required: ['to', 'message']
      },
      handler: async ({ to, message }) => {
        const msg = {
          notificationId: `SMS-${Date.now()}`,
          channel: 'SMS',
          to,
          message,
          status: 'SENT',
          sentAt: new Date().toISOString()
        };
        sentMessages.push(msg);
        return msg;
      }
    },
    {
      name: 'get_delivery_status',
      description: 'Get notification delivery status by ID',
      inputSchema: { type: 'object', properties: { notificationId: { type: 'string' } }, required: ['notificationId'] },
      handler: async ({ notificationId }) => {
        const msg = sentMessages.find(m => m.notificationId === notificationId);
        return msg ?? { notificationId, status: 'NOT_FOUND' };
      }
    }
  ]
});
