import { createMcpServer } from '../common/create-server.js';

const PORT = process.env.MCP_CRM_PORT || 8502;

createMcpServer({
  name: 'crm',
  description: 'Customer relationship management and 360-degree view',
  port: PORT,
  tools: [
    {
      name: 'get_customer_profile',
      description: 'Get full customer profile by customer ID',
      inputSchema: { type: 'object', properties: { customerId: { type: 'string' } }, required: ['customerId'] },
      handler: async ({ customerId }) => ({
        customerId,
        fullName: 'Rajesh Kumar',
        email: 'rajesh.kumar@email.com',
        phone: '+91-9876543210',
        segment: 'PREMIUM',
        riskRating: 'LOW',
        customerSince: '2018-03-15',
        loyaltyTier: 'GOLD'
      })
    },
    {
      name: 'get_relationship_summary',
      description: 'Get customer relationship and product holdings summary',
      inputSchema: { type: 'object', properties: { customerId: { type: 'string' } }, required: ['customerId'] },
      handler: async ({ customerId }) => ({
        customerId,
        totalProducts: 5,
        relationshipManager: 'Priya Sharma',
        loyaltyTier: 'GOLD',
        tenureYears: 7,
        products: ['Savings', 'Current Account', 'Fixed Deposit', 'Credit Card', 'Insurance']
      })
    },
    {
      name: 'search_customers',
      description: 'Search customers by name, email, or phone',
      inputSchema: { type: 'object', properties: { query: { type: 'string' } }, required: ['query'] },
      handler: async ({ query }) => ({
        query,
        results: [
          { customerId: 'CUST-12345', fullName: 'Rajesh Kumar', email: 'rajesh.kumar@email.com', matchScore: 0.95 },
          { customerId: 'CUST-67890', fullName: 'Rajesh Singh', email: 'rajesh.singh@email.com', matchScore: 0.72 }
        ]
      })
    }
  ]
});
