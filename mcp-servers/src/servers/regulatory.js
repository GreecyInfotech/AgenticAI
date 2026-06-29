import { createMcpServer } from '../common/create-server.js';

const PORT = process.env.MCP_REGULATORY_PORT || 8504;

const REGULATIONS = {
  RBI: {
    name: 'Reserve Bank of India Guidelines',
    rules: ['KYC Master Direction 2016', 'Fair Practices Code', 'Digital Lending Guidelines 2022']
  },
  AML: {
    name: 'Prevention of Money Laundering Act 2002',
    rules: ['Customer Due Diligence', 'Suspicious Transaction Reporting', 'Record Keeping 5 years']
  },
  GDPR: {
    name: 'EU General Data Protection Regulation',
    rules: ['Right to erasure', 'Data breach notification 72h', 'Consent management']
  },
  IRDAI: {
    name: 'Insurance Regulatory and Development Authority',
    rules: ['Policyholder protection', 'Claims settlement 30 days', 'Solvency requirements']
  }
};

createMcpServer({
  name: 'regulatory',
  description: 'Regulatory policy lookup for RBI, AML, GDPR, IRDAI',
  port: PORT,
  tools: [
    {
      name: 'lookup_regulation',
      description: 'Look up regulations by framework code (RBI, AML, GDPR, IRDAI)',
      inputSchema: { type: 'object', properties: { framework: { type: 'string' } }, required: ['framework'] },
      handler: async ({ framework }) => {
        const key = framework.toUpperCase();
        const reg = REGULATIONS[key];
        if (!reg) return { found: false, framework, message: 'Framework not found' };
        return { found: true, framework: key, ...reg };
      }
    },
    {
      name: 'check_compliance',
      description: 'Check if an action complies with a regulatory framework',
      inputSchema: {
        type: 'object',
        properties: { framework: { type: 'string' }, action: { type: 'string' } },
        required: ['framework', 'action']
      },
      handler: async ({ framework, action }) => {
        const violations = [];
        const lower = action.toLowerCase();
        if (framework.toUpperCase() === 'GDPR' && lower.includes('data breach')) {
          violations.push('GDPR Article 33: Breach notification required within 72 hours');
        }
        if (framework.toUpperCase() === 'AML' && lower.includes('offshore')) {
          violations.push('PMLA: Enhanced due diligence required for offshore transactions');
        }
        return {
          framework,
          action,
          compliant: violations.length === 0,
          violations,
          checkedAt: new Date().toISOString()
        };
      }
    },
    {
      name: 'list_frameworks',
      description: 'List all supported regulatory frameworks',
      inputSchema: { type: 'object', properties: {} },
      handler: async () => ({ frameworks: Object.keys(REGULATIONS) })
    }
  ]
});
