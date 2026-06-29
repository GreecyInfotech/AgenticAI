import { Link, useLocation } from 'react-router-dom';
import { Building2, Headphones, Shield, Sparkles } from 'lucide-react';
import clsx from 'clsx';
import type { Persona } from '@/types/api';

const navItems: { persona: Persona; label: string; path: string; icon: typeof Building2 }[] = [
  { persona: 'customer', label: 'Customer', path: '/customer', icon: Building2 },
  { persona: 'employee', label: 'Employee', path: '/employee', icon: Headphones },
  { persona: 'admin', label: 'Admin', path: '/admin', icon: Shield },
];

interface HeaderProps {
  title: string;
  subtitle?: string;
}

export function Header({ title, subtitle }: HeaderProps) {
  const location = useLocation();

  return (
    <header className="border-b border-surface-200 bg-white/80 backdrop-blur">
      <div className="mx-auto flex max-w-7xl items-center justify-between gap-4 px-4 py-4 sm:px-6">
        <Link to="/" className="flex items-center gap-3">
          <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-brand-600 text-white">
            <Sparkles className="h-5 w-5" />
          </div>
          <div>
            <p className="font-display text-sm font-semibold text-surface-900">BFSI Agentic AI</p>
            <p className="text-xs text-surface-500">Enterprise Platform</p>
          </div>
        </Link>

        <nav className="hidden items-center gap-1 md:flex">
          {navItems.map(({ label, path, icon: Icon }) => {
            const active = location.pathname.startsWith(path);
            return (
              <Link
                key={path}
                to={path}
                className={clsx(
                  'inline-flex items-center gap-2 rounded-lg px-3 py-2 text-sm font-medium transition',
                  active
                    ? 'bg-brand-50 text-brand-700'
                    : 'text-surface-600 hover:bg-surface-100 hover:text-surface-900',
                )}
              >
                <Icon className="h-4 w-4" />
                {label}
              </Link>
            );
          })}
        </nav>

        <div className="text-right">
          <h1 className="font-display text-lg font-semibold text-surface-900">{title}</h1>
          {subtitle && <p className="text-xs text-surface-500">{subtitle}</p>}
        </div>
      </div>
    </header>
  );
}

interface AppShellProps {
  title: string;
  subtitle?: string;
  children: React.ReactNode;
  sidebar?: React.ReactNode;
}

export function AppShell({ title, subtitle, children, sidebar }: AppShellProps) {
  return (
    <div className="min-h-screen bg-gradient-to-b from-surface-50 to-white">
      <Header title={title} subtitle={subtitle} />
      <div className="mx-auto flex max-w-7xl gap-6 px-4 py-6 sm:px-6">
        {sidebar && (
          <aside className="hidden w-64 shrink-0 lg:block">{sidebar}</aside>
        )}
        <main className="min-w-0 flex-1">{children}</main>
      </div>
    </div>
  );
}
