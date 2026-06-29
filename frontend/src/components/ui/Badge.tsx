import clsx from 'clsx';

type Tone = 'default' | 'success' | 'warning' | 'danger' | 'info';

interface BadgeProps {
  children: React.ReactNode;
  tone?: Tone;
  className?: string;
}

const tones: Record<Tone, string> = {
  default: 'bg-surface-100 text-surface-700',
  success: 'bg-emerald-50 text-emerald-700 ring-1 ring-emerald-200',
  warning: 'bg-amber-50 text-amber-800 ring-1 ring-amber-200',
  danger: 'bg-red-50 text-red-700 ring-1 ring-red-200',
  info: 'bg-brand-50 text-brand-700 ring-1 ring-brand-200',
};

export function Badge({ children, tone = 'default', className }: BadgeProps) {
  return (
    <span
      className={clsx(
        'inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium',
        tones[tone],
        className,
      )}
    >
      {children}
    </span>
  );
}
