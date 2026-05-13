'use client';

import { useQuery } from '@tanstack/react-query';
import {
  ActivitySquare, BarChart3, Download, GitBranch, Home, Loader2,
} from 'lucide-react';
import Link from 'next/link';
import { usePathname, useParams } from 'next/navigation';
import clsx from 'clsx';

import { api } from '@/lib/api';

export default function RunLayout({ children }: { children: React.ReactNode }) {
  const { runId } = useParams<{ runId: string }>();
  const pathname = usePathname();
  const runQ = useQuery({
    queryKey: ['run', runId],
    queryFn: () => api.getRun(runId),
    refetchInterval: (q) =>
      q.state.data?.state === 'running' || q.state.data?.state === 'queued' ? 800 : false,
  });

  const tabs = [
    { href: `/runs/${runId}/progress`, label: 'Live progress', icon: GitBranch },
    { href: `/runs/${runId}`,           label: 'Dashboard',     icon: BarChart3 },
    { href: `/runs/${runId}/audit`,     label: 'Audit trail',   icon: ActivitySquare },
    { href: `/runs/${runId}/reports`,   label: 'Reports',       icon: Download },
  ];

  const state = runQ.data?.state;

  return (
    <div className="min-h-screen">
      <header className="border-b border-white/5 sticky top-0 z-10 bg-ink-900/80 backdrop-blur-xl">
        <div className="max-w-7xl mx-auto px-6 py-3 flex items-center justify-between">
          <div className="flex items-center gap-4">
            <Link href="/" className="flex items-center gap-2.5 text-ink-300 hover:text-ink-100">
              <Home className="w-4 h-4" />
              <span className="text-sm font-medium">carbonTrace<span className="text-accent-glow">AI</span></span>
            </Link>
            <span className="text-ink-500">›</span>
            <div className="text-xs font-mono text-ink-400">
              run/{runId.slice(0, 8)}
            </div>
            {state && (
              <span className={clsx(
                'pill text-[10px]',
                state === 'succeeded' && 'border-emerald-400/30 bg-emerald-400/5 text-emerald-400',
                state === 'running'   && 'border-accent/30 bg-accent/5 text-accent-glow',
                state === 'queued'    && 'border-white/10 bg-white/5 text-ink-300',
                state === 'failed'    && 'border-rose-400/30 bg-rose-400/5 text-rose-400',
              )}>
                {state === 'running' && <Loader2 className="w-2.5 h-2.5 animate-spin" />}
                {state}
              </span>
            )}
          </div>
        </div>
        <nav className="max-w-7xl mx-auto px-6 flex">
          {tabs.map((t) => {
            const active = pathname === t.href;
            const Icon = t.icon;
            return (
              <Link
                key={t.href}
                href={t.href}
                className={clsx(
                  'px-4 py-2.5 text-sm flex items-center gap-2 border-b-2 transition-colors',
                  active
                    ? 'border-accent text-ink-100'
                    : 'border-transparent text-ink-400 hover:text-ink-200 hover:border-white/10'
                )}
              >
                <Icon className="w-3.5 h-3.5" />
                {t.label}
              </Link>
            );
          })}
        </nav>
      </header>
      <div className="max-w-7xl mx-auto px-6 py-8">{children}</div>
    </div>
  );
}
