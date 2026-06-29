import { useCallback, useState } from 'react';
import type { ChatMessage, ChatRequest } from '@/types/api';
import { ApiError } from '@/api/client';

interface UseChatOptions {
  send: (request: ChatRequest) => Promise<{
    requestId: string;
    reply: string;
    status: string;
    requiresEscalation: boolean;
    agentTrail?: ChatMessage['agentTrail'];
  }>;
  sessionId: string;
  customerId?: string;
  context?: Record<string, unknown>;
}

export function useChat({ send, sessionId, customerId, context }: UseChatOptions) {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const sendMessage = useCallback(
    async (text: string) => {
      const trimmed = text.trim();
      if (!trimmed || isLoading) return;

      const userMessage: ChatMessage = {
        id: crypto.randomUUID(),
        role: 'user',
        content: trimmed,
        timestamp: new Date(),
      };

      setMessages((prev) => [...prev, userMessage]);
      setIsLoading(true);
      setError(null);

      try {
        const response = await send({
          sessionId,
          customerId,
          message: trimmed,
          context,
        });

        const assistantMessage: ChatMessage = {
          id: response.requestId || crypto.randomUUID(),
          role: 'assistant',
          content: response.reply,
          timestamp: new Date(),
          agentTrail: response.agentTrail,
          requiresEscalation: response.requiresEscalation,
          status: response.status,
        };

        setMessages((prev) => [...prev, assistantMessage]);
      } catch (err) {
        const message =
          err instanceof ApiError
            ? err.message
            : err instanceof Error
              ? err.message
              : 'Something went wrong';
        setError(message);
        setMessages((prev) => [
          ...prev,
          {
            id: crypto.randomUUID(),
            role: 'assistant',
            content: `Sorry, I could not process your request. ${message}`,
            timestamp: new Date(),
            status: 'FAILED',
          },
        ]);
      } finally {
        setIsLoading(false);
      }
    },
    [send, sessionId, customerId, context, isLoading],
  );

  const clearChat = useCallback(() => {
    setMessages([]);
    setError(null);
  }, []);

  return { messages, isLoading, error, sendMessage, clearChat };
}
