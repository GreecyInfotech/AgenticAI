import { useQuery } from '@tanstack/react-query';
import { RefreshCw, Server } from 'lucide-react';
import { listAgents } from '@/api/admin';
import { Badge } from '@/components/ui/Badge';
import { Button } from '@/components/ui/Button';
import { Card } from '@/components/ui/Card';
import { LoadingSpinner } from '@/components/ui/LoadingSpinner';
import type { AgentRegistration } from '@/types/api';

function AgentRow({ agent }: { agent: AgentRegistration }) {
  return (
    <tr className="border-b border-surface-100 last:border-0">
      <td className="px-4 py-3 font-medium text-surface-900">{agent.type}</td>
      <td className="px-4 py-3 text-sm text-surface-600">{agent.serviceName}</td>
      <td className="px-4 py-3 text-sm text-surface-500">
        {agent.baseUrl}:{agent.port}
      </td>
      <td className="px-4 py-3">
        <Badge tone={agent.healthy ? 'success' : 'danger'}>
          {agent.healthy ? 'Healthy' : 'Unhealthy'}
        </Badge>
      </td>
    </tr>
  );
}

export function AgentTable() {
  const { data, isLoading, isError, error, refetch, isFetching } = useQuery({
    queryKey: ['admin', 'agents'],
    queryFn: listAgents,
    refetchInterval: 30_000,
  });

  return (
    <Card padding="none" className="overflow-hidden">
      <div className="flex items-center justify-between border-b border-surface-200 px-4 py-3">
        <div className="flex items-center gap-2">
          <Server className="h-4 w-4 text-brand-600" />
          <h3 className="font-display font-semibold text-surface-900">Registered Agents</h3>
        </div>
        <Button variant="ghost" size="sm" onClick={() => refetch()} disabled={isFetching}>
          <RefreshCw className={`h-4 w-4 ${isFetching ? 'animate-spin' : ''}`} />
          Refresh
        </Button>
      </div>

      {isLoading ? (
        <div className="flex items-center justify-center py-12">
          <LoadingSpinner />
        </div>
      ) : isError ? (
        <div className="p-6 text-sm text-red-600">
          Failed to load agents: {error instanceof Error ? error.message : 'Unknown error'}
        </div>
      ) : (
        <div className="overflow-x-auto">
          <table className="w-full text-left text-sm">
            <thead className="bg-surface-50 text-xs uppercase tracking-wide text-surface-500">
              <tr>
                <th className="px-4 py-3">Type</th>
                <th className="px-4 py-3">Service</th>
                <th className="px-4 py-3">Endpoint</th>
                <th className="px-4 py-3">Status</th>
              </tr>
            </thead>
            <tbody>
              {data?.map((agent) => (
                <AgentRow key={agent.type} agent={agent} />
              ))}
            </tbody>
          </table>
          {data?.length === 0 && (
            <p className="p-6 text-center text-sm text-surface-500">No agents registered.</p>
          )}
        </div>
      )}
    </Card>
  );
}
