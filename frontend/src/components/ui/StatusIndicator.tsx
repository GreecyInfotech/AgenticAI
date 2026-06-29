import clsx from 'clsx';

interface StatusIndicatorProps {
  status: 'UP' | 'DOWN' | string;
  label?: string;
}

export function StatusIndicator({ status, label }: StatusIndicatorProps) {
  const isUp = status.toUpperCase() === 'UP';
  return (
    <span className="inline-flex items-center gap-2 text-sm">
      <span
        className={clsx(
          'h-2.5 w-2.5 rounded-full',
          isUp ? 'bg-emerald-500 shadow-[0_0_8px_rgba(16,185,129,0.6)]' : 'bg-red-500',
        )}
      />
      <span className="font-medium text-surface-700">{label ?? status}</span>
    </span>
  );
}
