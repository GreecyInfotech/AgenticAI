import { useEffect, useRef } from 'react';
import { AlertTriangle, Sparkles } from 'lucide-react';
import type { AgentResponse } from '@/types/api';
import { Badge } from '@/components/ui/Badge';
import { Card } from '@/components/ui/Card';
import { ChatMessage } from '@/components/chat/ChatMessage';
import { ChatInput } from '@/components/chat/ChatInput';
import { LoadingSpinner } from '@/components/ui/LoadingSpinner';
import type { ChatMessage as ChatMessageType } from '@/types/api';

interface AgentTrailPanelProps {
  trail?: AgentResponse[];
  visible: boolean;
}

export function AgentTrailPanel({ trail, visible }: AgentTrailPanelProps) {
  if (!visible || !trail?.length) {
    return (
      <Card padding="md" className="h-full">
        <div className="flex h-full flex-col items-center justify-center text-center text-surface-400">
          <Sparkles className="mb-3 h-8 w-8 opacity-50" />
          <p className="text-sm">Agent orchestration trail will appear here after each response.</p>
        </div>
      </Card>
    );
  }

  return (
    <Card padding="none" className="flex h-full flex-col overflow-hidden">
      <div className="border-b border-surface-200 px-4 py-3">
        <h3 className="font-display text-sm font-semibold text-surface-900">Agent Trail</h3>
        <p className="text-xs text-surface-500">{trail.length} agent step(s)</p>
      </div>
      <div className="scrollbar-thin flex-1 space-y-3 overflow-y-auto p-4">
        {trail.map((step, index) => (
          <div
            key={`${step.agentType}-${index}`}
            className="rounded-xl border border-surface-200 bg-surface-50 p-3"
          >
            <div className="mb-2 flex items-center justify-between gap-2">
              <span className="font-medium text-surface-900">{step.agentType ?? 'UNKNOWN'}</span>
              <Badge tone={step.status === 'SUCCESS' ? 'success' : step.status === 'FAILED' ? 'danger' : 'info'}>
                {step.status ?? 'PENDING'}
              </Badge>
            </div>
            {step.message && (
              <p className="text-sm text-surface-600">{step.message}</p>
            )}
            {typeof step.confidence === 'number' && (
              <p className="mt-2 text-xs text-surface-400">
                Confidence: {(step.confidence * 100).toFixed(0)}%
              </p>
            )}
            {step.requiresEscalation && (
              <div className="mt-2 flex items-center gap-1 text-xs text-amber-700">
                <AlertTriangle className="h-3.5 w-3.5" />
                Escalation flagged
              </div>
            )}
          </div>
        ))}
      </div>
    </Card>
  );
}

interface ChatPanelProps {
  messages: ChatMessageType[];
  isLoading: boolean;
  onSend: (message: string) => void;
  placeholder?: string;
  emptyTitle?: string;
  emptyDescription?: string;
  suggestions?: string[];
  showTrail?: boolean;
  activeTrail?: AgentResponse[];
}

export function ChatPanel({
  messages,
  isLoading,
  onSend,
  placeholder,
  emptyTitle = 'How can I help you today?',
  emptyDescription = 'Ask about loans, KYC, claims, portfolio advice, and more.',
  suggestions = [],
  showTrail = true,
  activeTrail,
}: ChatPanelProps) {
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, isLoading]);

  const latestTrail = activeTrail ?? messages.filter((m) => m.role === 'assistant').at(-1)?.agentTrail;

  return (
    <div className="grid h-full gap-4 lg:grid-cols-[1fr_320px]">
      <Card padding="none" className="flex min-h-[560px] flex-col overflow-hidden">
        <div className="scrollbar-thin flex-1 space-y-4 overflow-y-auto p-4">
          {messages.length === 0 ? (
            <div className="flex h-full flex-col items-center justify-center px-6 py-12 text-center">
              <div className="mb-4 rounded-2xl bg-brand-50 p-4 text-brand-600">
                <Sparkles className="h-8 w-8" />
              </div>
              <h2 className="font-display text-xl font-semibold text-surface-900">{emptyTitle}</h2>
              <p className="mt-2 max-w-md text-sm text-surface-500">{emptyDescription}</p>
              {suggestions.length > 0 && (
                <div className="mt-6 flex flex-wrap justify-center gap-2">
                  {suggestions.map((suggestion) => (
                    <button
                      key={suggestion}
                      type="button"
                      onClick={() => onSend(suggestion)}
                      className="rounded-full border border-surface-200 bg-white px-4 py-2 text-sm text-surface-700 transition hover:border-brand-300 hover:bg-brand-50"
                    >
                      {suggestion}
                    </button>
                  ))}
                </div>
              )}
            </div>
          ) : (
            messages.map((message) => <ChatMessage key={message.id} message={message} />)
          )}
          {isLoading && (
            <div className="flex items-center gap-2 text-sm text-surface-500">
              <LoadingSpinner className="h-4 w-4" />
              Processing with agent orchestrator...
            </div>
          )}
          <div ref={bottomRef} />
        </div>
        <ChatInput onSend={onSend} isLoading={isLoading} placeholder={placeholder} />
      </Card>

      {showTrail && (
        <div className="hidden min-h-[560px] lg:block">
          <AgentTrailPanel trail={latestTrail} visible={!!latestTrail?.length} />
        </div>
      )}
    </div>
  );
}
