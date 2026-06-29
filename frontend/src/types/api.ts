export type AgentStatus = 'SUCCESS' | 'PENDING' | 'FAILED';

export type AgentType =
  | 'INTENT'
  | 'CUSTOMER'
  | 'KYC'
  | 'AML'
  | 'FRAUD'
  | 'LOAN'
  | 'UNDERWRITING'
  | 'CLAIM'
  | 'COMPLIANCE'
  | 'AUDIT'
  | 'RECOMMENDATION'
  | 'PORTFOLIO'
  | 'ESCALATION'
  | 'NOTIFICATION';

export interface ChatRequest {
  requestId?: string;
  sessionId?: string;
  message: string;
  customerId?: string;
  context?: Record<string, unknown>;
}

export interface AgentResponse {
  requestId?: string;
  agentType?: AgentType;
  status?: AgentStatus;
  message?: string;
  data?: Record<string, unknown>;
  nextAgents?: AgentType[];
  confidence?: number;
  requiresEscalation?: boolean;
}

export interface ChatResponse {
  requestId: string;
  reply: string;
  status: string;
  requiresEscalation: boolean;
  agentTrail?: AgentResponse[];
}

export interface CaseResponse {
  requestId: string;
  status: string;
  reply: string;
  requiresEscalation: boolean;
}

export interface AgentRegistration {
  type: AgentType;
  serviceName: string;
  baseUrl: string;
  port: number;
  healthEndpoint: string;
  healthy: boolean;
}

export interface PlatformHealth {
  orchestrator: string;
  registry: string;
  status: string;
}

export interface ChatMessage {
  id: string;
  role: 'user' | 'assistant' | 'system';
  content: string;
  timestamp: Date;
  agentTrail?: AgentResponse[];
  requiresEscalation?: boolean;
  status?: string;
}

export type Persona = 'customer' | 'employee' | 'admin';
