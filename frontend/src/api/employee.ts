import { apiFetch } from './client';
import type { CaseResponse, ChatRequest, ChatResponse } from '@/types/api';

export function sendEmployeeChat(request: ChatRequest): Promise<ChatResponse> {
  return apiFetch<ChatResponse>('/api/employee/v1/chat', {
    method: 'POST',
    body: JSON.stringify(request),
  });
}

export function createCase(request: ChatRequest): Promise<CaseResponse> {
  return apiFetch<CaseResponse>('/api/employee/v1/cases', {
    method: 'POST',
    body: JSON.stringify(request),
  });
}

export function getEmployeeHealth(): Promise<string> {
  return apiFetch<string>('/api/employee/v1/health');
}
