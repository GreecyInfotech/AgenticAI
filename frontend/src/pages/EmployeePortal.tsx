import { useState } from 'react';
import { AlertTriangle, RotateCcw } from 'lucide-react';
import { createCase, sendEmployeeChat } from '@/api/employee';
import { AppShell } from '@/components/layout/AppShell';
import { ChatPanel } from '@/components/chat/ChatPanel';
import { Button } from '@/components/ui/Button';
import { Card } from '@/components/ui/Card';
import { useChat } from '@/hooks/useChat';
import { useSession } from '@/hooks/useSession';
import { ApiError } from '@/api/client';

const suggestions = [
  'Review pending KYC application',
  'Check AML alert for customer',
  'Escalate fraud case to compliance',
];

export function EmployeePortal() {
  const { sessionId, customerId, setCustomerId, resetSession } = useSession();
  const [caseNote, setCaseNote] = useState('');
  const [caseLoading, setCaseLoading] = useState(false);
  const [caseResult, setCaseResult] = useState<string | null>(null);

  const { messages, isLoading, sendMessage, clearChat } = useChat({
    send: sendEmployeeChat,
    sessionId,
    customerId,
    context: { persona: 'EMPLOYEE' },
  });

  const handleCreateCase = async () => {
    if (!caseNote.trim() || caseLoading) return;
    setCaseLoading(true);
    setCaseResult(null);
    try {
      const result = await createCase({
        sessionId,
        customerId,
        message: caseNote,
      });
      setCaseResult(result.reply);
      setCaseNote('');
    } catch (err) {
      setCaseResult(
        err instanceof ApiError ? err.message : 'Failed to create escalation case',
      );
    } finally {
      setCaseLoading(false);
    }
  };

  const sidebar = (
    <div className="space-y-4">
      <Card>
        <h3 className="mb-3 font-display text-sm font-semibold text-surface-900">Staff Session</h3>
        <label className="mb-2 block text-xs font-medium text-surface-500">Customer ID</label>
        <input
          value={customerId}
          onChange={(e) => setCustomerId(e.target.value)}
          className="mb-4 w-full rounded-lg border border-surface-200 px-3 py-2 text-sm focus:border-brand-400 focus:outline-none focus:ring-2 focus:ring-brand-100"
        />
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
        <div className="mb-3 flex items-center gap-2 text-amber-700">
          <AlertTriangle className="h-4 w-4" />
          <h3 className="font-display text-sm font-semibold">Create Escalation Case</h3>
        </div>
        <textarea
          value={caseNote}
          onChange={(e) => setCaseNote(e.target.value)}
          placeholder="Describe the case for human review..."
          rows={4}
          className="mb-3 w-full rounded-lg border border-surface-200 px-3 py-2 text-sm focus:border-brand-400 focus:outline-none focus:ring-2 focus:ring-brand-100"
        />
        <Button
          variant="danger"
          size="sm"
          onClick={handleCreateCase}
          disabled={!caseNote.trim() || caseLoading}
          className="w-full"
        >
          {caseLoading ? 'Creating...' : 'Escalate Case'}
        </Button>
        {caseResult && (
          <p className="mt-3 rounded-lg bg-surface-50 p-3 text-sm text-surface-700">{caseResult}</p>
        )}
      </Card>
    </div>
  );

  return (
    <AppShell
      title="Employee Portal"
      subtitle="Staff operations & case management"
      sidebar={sidebar}
    >
      <ChatPanel
        messages={messages}
        isLoading={isLoading}
        onSend={sendMessage}
        suggestions={suggestions}
        emptyTitle="Staff AI assistant"
        emptyDescription="Get help with customer cases, compliance reviews, and operational workflows. Use the sidebar to escalate cases to human review."
        placeholder="Ask about a customer case..."
      />
    </AppShell>
  );
}
