import { Bot, User } from 'lucide-react';
import clsx from 'clsx';
import type { ChatMessage as ChatMessageType } from '@/types/api';
import { Badge } from '@/components/ui/Badge';

interface ChatMessageProps {
  message: ChatMessageType;
}

export function ChatMessage({ message }: ChatMessageProps) {
  const isUser = message.role === 'user';

  return (
    <div
      className={clsx('flex gap-3', isUser ? 'flex-row-reverse' : 'flex-row')}
    >
      <div
        className={clsx(
          'flex h-9 w-9 shrink-0 items-center justify-center rounded-xl',
          isUser ? 'bg-brand-100 text-brand-700' : 'bg-surface-100 text-surface-600',
        )}
      >
        {isUser ? <User className="h-4 w-4" /> : <Bot className="h-4 w-4" />}
      </div>

      <div className={clsx('max-w-[85%] space-y-2', isUser && 'text-right')}>
        <div
          className={clsx(
            'rounded-2xl px-4 py-3 text-sm leading-relaxed',
            isUser
              ? 'rounded-tr-md bg-brand-600 text-white'
              : 'rounded-tl-md border border-surface-200 bg-white text-surface-800',
          )}
        >
          <p className="whitespace-pre-wrap">{message.content}</p>
        </div>

        {!isUser && (
          <div className="flex flex-wrap items-center gap-2">
            {message.status && (
              <Badge tone={message.status === 'SUCCESS' ? 'success' : 'default'}>
                {message.status}
              </Badge>
            )}
            {message.requiresEscalation && (
              <Badge tone="warning">Escalation required</Badge>
            )}
            <span className="text-xs text-surface-400">
              {message.timestamp.toLocaleTimeString()}
            </span>
          </div>
        )}
      </div>
    </div>
  );
}
