import { RotateCcw } from 'lucide-react';
import { sendCustomerChat } from '@/api/customer';
import { AppShell } from '@/components/layout/AppShell';
import { ChatPanel } from '@/components/chat/ChatPanel';
import { Button } from '@/components/ui/Button';
import { Card } from '@/components/ui/Card';
import { useChat } from '@/hooks/useChat';
import { useSession } from '@/hooks/useSession';

const suggestions = [
  'I need a home loan',
  'Check my KYC status',
  'File an insurance claim',
  'Recommend investment products',
];

export function CustomerPortal() {
  const { sessionId, customerId, setCustomerId, resetSession } = useSession();
  const { messages, isLoading, sendMessage, clearChat } = useChat({
    send: sendCustomerChat,
    sessionId,
    customerId,
  });

  const sidebar = (
    <div className="space-y-4">
      <Card>
        <h3 className="mb-3 font-display text-sm font-semibold text-surface-900">Session</h3>
        <label className="mb-3 block text-xs font-medium text-surface-500">Customer ID</label>
        <input
          value={customerId}
          onChange={(e) => setCustomerId(e.target.value)}
          className="mb-4 w-full rounded-lg border border-surface-200 px-3 py-2 text-sm focus:border-brand-400 focus:outline-none focus:ring-2 focus:ring-brand-100"
        />
        <p className="mb-4 break-all text-xs text-surface-400">Session: {sessionId}</p>
        <div className="flex gap-2">
          <Button variant="secondary" size="sm" onClick={clearChat}>
            Clear chat
          </Button>
          <Button variant="ghost" size="sm" onClick={resetSession}>
            <RotateCcw className="h-4 w-4" />
            New session
          </Button>
        </div>
      </Card>
      <Card>
        <h3 className="mb-2 font-display text-sm font-semibold text-surface-900">Capabilities</h3>
        <ul className="space-y-1 text-sm text-surface-600">
          <li>Loan eligibility & applications</li>
          <li>KYC & identity verification</li>
          <li>Claims & underwriting</li>
          <li>Portfolio & product advice</li>
          <li>AML & fraud screening</li>
        </ul>
      </Card>
    </div>
  );

  return (
    <AppShell
      title="Customer Portal"
      subtitle="Self-service AI banking assistant"
      sidebar={sidebar}
    >
      <ChatPanel
        messages={messages}
        isLoading={isLoading}
        onSend={sendMessage}
        suggestions={suggestions}
        emptyTitle="Welcome to your banking assistant"
        emptyDescription="Ask about loans, accounts, insurance, investments, or compliance — our agents will route your request automatically."
        placeholder="Ask about loans, KYC, claims..."
      />
    </AppShell>
  );
}
