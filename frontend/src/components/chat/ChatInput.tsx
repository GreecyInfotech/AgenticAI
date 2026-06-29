import { useState, type FormEvent, type KeyboardEvent } from 'react';
import { Send } from 'lucide-react';
import { Button } from '@/components/ui/Button';
import { LoadingSpinner } from '@/components/ui/LoadingSpinner';

interface ChatInputProps {
  onSend: (message: string) => void;
  isLoading?: boolean;
  placeholder?: string;
  disabled?: boolean;
}

export function ChatInput({
  onSend,
  isLoading = false,
  placeholder = 'Type your message...',
  disabled = false,
}: ChatInputProps) {
  const [value, setValue] = useState('');

  const submit = () => {
    if (!value.trim() || isLoading || disabled) return;
    onSend(value);
    setValue('');
  };

  const handleSubmit = (e: FormEvent) => {
    e.preventDefault();
    submit();
  };

  const handleKeyDown = (e: KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      submit();
    }
  };

  return (
    <form onSubmit={handleSubmit} className="border-t border-surface-200 bg-white p-4">
      <div className="flex items-end gap-3">
        <textarea
          value={value}
          onChange={(e) => setValue(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder={placeholder}
          disabled={disabled || isLoading}
          rows={2}
          className="min-h-[48px] flex-1 resize-none rounded-xl border border-surface-200 bg-surface-50 px-4 py-3 text-sm text-surface-900 placeholder:text-surface-400 focus:border-brand-400 focus:outline-none focus:ring-2 focus:ring-brand-100 disabled:opacity-60"
        />
        <Button type="submit" disabled={!value.trim() || isLoading || disabled}>
          {isLoading ? <LoadingSpinner className="h-4 w-4 text-white" /> : <Send className="h-4 w-4" />}
          Send
        </Button>
      </div>
      <p className="mt-2 text-xs text-surface-400">Press Enter to send, Shift+Enter for new line</p>
    </form>
  );
}
