import { apiFetch } from './client';
import type { ChatRequest, ChatResponse } from '@/types/api';

export function sendCustomerChat(request: ChatRequest): Promise<ChatResponse> {
  return apiFetch<ChatResponse>('/api/customer/v1/chat', {
    method: 'POST',
    body: JSON.stringify(request),
  });
}

export function getCustomerHealth(): Promise<string> {
  return apiFetch<string>('/api/customer/v1/health');
}
