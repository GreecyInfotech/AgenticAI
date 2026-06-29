import clsx from 'clsx';
import type { HTMLAttributes } from 'react';

interface CardProps extends HTMLAttributes<HTMLDivElement> {
  padding?: 'none' | 'sm' | 'md' | 'lg';
}

const paddingMap = {
  none: '',
  sm: 'p-4',
  md: 'p-6',
  lg: 'p-8',
};

export function Card({ padding = 'md', className, children, ...props }: CardProps) {
  return (
    <div
      className={clsx(
        'rounded-2xl border border-surface-200 bg-white shadow-panel',
        paddingMap[padding],
        className,
      )}
      {...props}
    >
      {children}
    </div>
  );
}
