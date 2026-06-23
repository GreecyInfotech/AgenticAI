export interface Vessel {
  id: string;
  name: string;
  imo: string;
  eta: string;
  etd: string;
  berth: string;
  status: 'approaching' | 'berthed' | 'departed' | 'scheduled';
  teu_capacity: number;
}

export interface Container {
  id: string;
  type: string;
  location: string;
  status: 'available' | 'in_transit' | 'held' | 'customs_hold';
  vessel_id?: string;
  weight_kg?: number;
}

export interface AgentRequest {
  query: string;
  context?: Record<string, unknown>;
  session_id?: string;
}

export interface AgentResponse {
  answer: string;
  tools_used: string[];
  confidence: number;
  session_id?: string;
  metadata?: Record<string, unknown>;
}

export interface KPI {
  name: string;
  value: number;
  unit: string;
  trend: 'up' | 'down' | 'stable';
  change_pct: number;
}

export interface CustomsDeclaration {
  id: string;
  vessel_id: string;
  status: 'pending' | 'in_review' | 'cleared' | 'held';
  risk_score: number;
  submitted_at: string;
}

export interface Invoice {
  id: string;
  customer: string;
  amount: number;
  currency: string;
  status: 'draft' | 'pending' | 'paid' | 'overdue';
  due_date: string;
}

export type UserRole = 'admin' | 'operator' | 'customs_officer' | 'executive' | 'maintenance';

export interface AuthUser {
  userId: string;
  email: string;
  roles: UserRole[];
}

export const AGENT_REGISTRY = {
  vessel: { name: 'vessel-agent', port: 8100, domain: 'vessel' },
  container: { name: 'container-agent', port: 8101, domain: 'container' },
  customs: { name: 'customs-agent', port: 8102, domain: 'customs' },
  billing: { name: 'billing-agent', port: 8103, domain: 'billing' },
  maintenance: { name: 'maintenance-agent', port: 8104, domain: 'maintenance' },
  incident: { name: 'incident-agent', port: 8105, domain: 'incident' },
  planning: { name: 'planning-agent', port: 8106, domain: 'planning' },
  safety: { name: 'safety-agent', port: 8107, domain: 'safety' },
  weather: { name: 'weather-agent', port: 8108, domain: 'weather' },
  logistics: { name: 'logistics-agent', port: 8109, domain: 'logistics' },
  executive: { name: 'executive-agent', port: 8110, domain: 'executive' },
} as const;
