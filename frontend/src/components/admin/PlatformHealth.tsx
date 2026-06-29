import { useQuery } from '@tanstack/react-query';
import { Activity } from 'lucide-react';
import { getPlatformHealth } from '@/api/admin';
import { Card } from '@/components/ui/Card';
import { LoadingSpinner } from '@/components/ui/LoadingSpinner';
import { StatusIndicator } from '@/components/ui/StatusIndicator';

export function PlatformHealth() {
  const { data, isLoading, isError } = useQuery({
    queryKey: ['admin', 'platform-health'],
    queryFn: getPlatformHealth,
    refetchInterval: 15_000,
  });

  return (
    <Card>
      <div className="mb-4 flex items-center gap-2">
        <Activity className="h-5 w-5 text-brand-600" />
        <h3 className="font-display font-semibold text-surface-900">Platform Health</h3>
      </div>

      {isLoading ? (
        <div className="flex justify-center py-6">
          <LoadingSpinner />
        </div>
      ) : isError ? (
        <p className="text-sm text-red-600">Unable to reach platform health endpoint.</p>
      ) : (
        <div className="grid gap-4 sm:grid-cols-3">
          <div className="rounded-xl border border-surface-200 bg-surface-50 p-4">
            <p className="mb-2 text-xs font-medium uppercase tracking-wide text-surface-500">Orchestrator</p>
            <StatusIndicator status={data?.orchestrator ?? 'DOWN'} />
          </div>
          <div className="rounded-xl border border-surface-200 bg-surface-50 p-4">
            <p className="mb-2 text-xs font-medium uppercase tracking-wide text-surface-500">Registry</p>
            <StatusIndicator status={data?.registry ?? 'DOWN'} />
          </div>
          <div className="rounded-xl border border-surface-200 bg-surface-50 p-4">
            <p className="mb-2 text-xs font-medium uppercase tracking-wide text-surface-500">Overall</p>
            <StatusIndicator status={data?.status ?? 'DOWN'} />
          </div>
        </div>
      )}
    </Card>
  );
}
