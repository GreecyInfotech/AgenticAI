import { useState } from 'react';
import clsx from 'clsx';
import { Activity, MessageSquare, Server } from 'lucide-react';
import { sendAdminChat } from '@/api/admin';
import { AgentTable } from '@/components/admin/AgentTable';
import { PlatformHealth } from '@/components/admin/PlatformHealth';
import { AppShell } from '@/components/layout/AppShell';
import { ChatPanel } from '@/components/chat/ChatPanel';
import { Card } from '@/components/ui/Card';
import { useChat } from '@/hooks/useChat';
import { useSession } from '@/hooks/useSession';

type AdminTab = 'agents' | 'health' | 'chat';

const tabs: { id: AdminTab; label: string; icon: typeof Server }[] = [
  { id: 'agents', label: 'Agents', icon: Server },
  { id: 'health', label: 'Health', icon: Activity },
  { id: 'chat', label: 'Debug Chat', icon: MessageSquare },
];

export function AdminPortal() {
  const [tab, setTab] = useState<AdminTab>('agents');
  const { sessionId } = useSession();
  const { messages, isLoading, sendMessage } = useChat({
    send: sendAdminChat,
    sessionId,
    context: { persona: 'ADMIN' },
  });

  const sidebar = (
    <Card padding="sm" className="p-2">
      <nav className="space-y-1">
        {tabs.map(({ id, label, icon: Icon }) => (
          <button
            key={id}
            type="button"
            onClick={() => setTab(id)}
            className={clsx(
              'flex w-full items-center gap-2 rounded-lg px-3 py-2 text-sm font-medium transition',
              tab === id
                ? 'bg-brand-50 text-brand-700'
                : 'text-surface-600 hover:bg-surface-100',
            )}
          >
            <Icon className="h-4 w-4" />
            {label}
          </button>
        ))}
      </nav>
    </Card>
  );

  return (
    <AppShell
      title="Admin Portal"
      subtitle="Platform operations & monitoring"
      sidebar={sidebar}
    >
      {tab === 'agents' && <AgentTable />}
      {tab === 'health' && <PlatformHealth />}
      {tab === 'chat' && (
        <ChatPanel
          messages={messages}
          isLoading={isLoading}
          onSend={sendMessage}
          showTrail
          emptyTitle="Admin debug chat"
          emptyDescription="Send test messages through the orchestrator with admin context for platform debugging."
          placeholder="Test orchestration flow..."
        />
      )}
    </AppShell>
  );
}
