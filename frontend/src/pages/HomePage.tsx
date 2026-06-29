import { Link } from 'react-router-dom';
import { ArrowRight, Building2, Headphones, Shield, Sparkles } from 'lucide-react';
import { Card } from '@/components/ui/Card';

const portals = [
  {
    title: 'Customer Portal',
    description: 'Self-service banking and insurance assistant for loans, KYC, claims, and portfolio advice.',
    path: '/customer',
    icon: Building2,
    accent: 'from-brand-500 to-brand-700',
  },
  {
    title: 'Employee Portal',
    description: 'Staff operations console with AI assistance and case escalation workflows.',
    path: '/employee',
    icon: Headphones,
    accent: 'from-emerald-500 to-teal-700',
  },
  {
    title: 'Admin Portal',
    description: 'Platform operations — agent registry, health monitoring, and orchestration debug chat.',
    path: '/admin',
    icon: Shield,
    accent: 'from-violet-500 to-indigo-700',
  },
];

export function HomePage() {
  return (
    <div className="min-h-screen bg-surface-950 text-white">
      <div className="relative overflow-hidden">
        <div className="absolute inset-0 bg-[radial-gradient(circle_at_top_right,rgba(51,102,255,0.25),transparent_50%)]" />
        <div className="absolute inset-0 bg-[radial-gradient(circle_at_bottom_left,rgba(16,185,129,0.12),transparent_45%)]" />

        <div className="relative mx-auto max-w-6xl px-4 py-16 sm:px-6 sm:py-24">
          <div className="mb-12 flex items-center gap-3">
            <div className="flex h-12 w-12 items-center justify-center rounded-2xl bg-brand-500">
              <Sparkles className="h-6 w-6" />
            </div>
            <div>
              <p className="font-display text-lg font-semibold">BFSI Agentic AI Platform</p>
              <p className="text-sm text-slate-400">Banking · Financial Services · Insurance</p>
            </div>
          </div>

          <h1 className="max-w-3xl font-display text-4xl font-bold tracking-tight sm:text-5xl">
            Intelligent assistants for every banking persona
          </h1>
          <p className="mt-4 max-w-2xl text-lg text-slate-300">
            Multi-agent orchestration across KYC, AML, fraud, loans, claims, compliance, and more —
            with dedicated portals for customers, employees, and platform administrators.
          </p>

          <div className="mt-12 grid gap-6 md:grid-cols-3">
            {portals.map(({ title, description, path, icon: Icon, accent }) => (
              <Link key={path} to={path} className="group">
                <Card
                  padding="lg"
                  className="h-full border-slate-800 bg-slate-900/80 text-white transition group-hover:border-brand-500/50 group-hover:bg-slate-900"
                >
                  <div
                    className={`mb-4 inline-flex rounded-xl bg-gradient-to-br ${accent} p-3 text-white`}
                  >
                    <Icon className="h-6 w-6" />
                  </div>
                  <h2 className="font-display text-xl font-semibold">{title}</h2>
                  <p className="mt-2 text-sm leading-relaxed text-slate-400">{description}</p>
                  <span className="mt-6 inline-flex items-center gap-2 text-sm font-medium text-brand-300 group-hover:text-brand-200">
                    Open portal
                    <ArrowRight className="h-4 w-4 transition group-hover:translate-x-1" />
                  </span>
                </Card>
              </Link>
            ))}
          </div>

          <p className="mt-12 text-sm text-slate-500">
            API Gateway: <code className="text-slate-400">localhost:8000</code> · Requires backend platform running
          </p>
        </div>
      </div>
    </div>
  );
}
