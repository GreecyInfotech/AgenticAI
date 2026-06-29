import { apiFetch } from './client';
import type { AgentRegistration, ChatRequest, ChatResponse, PlatformHealth } from '@/types/api';

export function listAgents(): Promise<AgentRegistration[]> {
  return apiFetch<AgentRegistration[]>('/api/admin/v1/agents');
}

export function sendAdminChat(request: ChatRequest): Promise<ChatResponse> {
  return apiFetch<ChatResponse>('/api/admin/v1/chat', {
    method: 'POST',
    body: JSON.stringify(request),
  });
}

export function getPlatformHealth(): Promise<PlatformHealth> {
  return apiFetch<PlatformHealth>('/api/admin/v1/platform/health');
}

export function getAdminHealth(): Promise<string> {
  return apiFetch<string>('/api/admin/v1/health');
}
