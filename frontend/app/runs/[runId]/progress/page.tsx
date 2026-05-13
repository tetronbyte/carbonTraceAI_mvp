'use client';

import { useQuery } from '@tanstack/react-query';
import {
  ArrowRight, Check, ChevronRight, CircleAlert, CircleDot, Database,
  FileSpreadsheet, FlaskConical, Network, ScanLine, Sparkles, Terminal,
} from 'lucide-react';
import Link from 'next/link';
import { useParams } from 'next/navigation';
import clsx from 'clsx';
import { useEffect, useRef } from 'react';

import { api, RunStep } from '@/lib/api';
import { Card } from '@/components/ui/Card';
import { Button } from '@/components/ui/Button';
import { fmtEur, fmtNumber, fmtPct, fmtTonnes, stepLabel } from '@/lib/format';

const STEP_ICONS: Record<string, any> = {
  connect_erp:       Network,
  seed_erp:          Database,
  pull_erp:          FileSpreadsheet,
  manual_supplement: ScanLine,
  calculate:         FlaskConical,
  render_reports:    Sparkles,
};

export default function ProgressPage() {
  const { runId } = useParams<{ runId: string }>();
  const runQ = useQuery({
    queryKey: ['run', runId],
    queryFn: () => api.getRun(runId),
    refetchInterval: (q) =>
      q.state.data?.state === 'running' || q.state.data?.state === 'queued' ? 800 : false,
  });

  // Auto-scroll log to bottom
  const logRef = useRef<HTMLDivElement>(null);
  useEffect(() => {
    if (logRef.current) logRef.current.scrollTop = logRef.current.scrollHeight;
  }, [runQ.data?.log_tail.length]);

  const run = runQ.data;
  if (!run) return <Loading />;

  return (
    <div className="grid grid-cols-1 lg:grid-cols-[1.3fr_1fr] gap-6">
      <div className="space-y-6">
        {/* Pipeline steps */}
        <Card>
          <div className="flex items-center justify-between mb-5">
            <div>
              <h2 className="text-lg font-semibold">Pipeline</h2>
              <p className="text-sm text-ink-400">
                {run.profile_key === 'mozal_aluminium' ? 'Mozal Aluminium · MZ' : 'OCP Fertiliser · MA'} ·{' '}
                <span className="font-mono text-xs">{run.base_url}</span>
              </p>
            </div>
            {run.state === 'succeeded' && (
              <Link href={`/runs/${runId}`}>
                <Button>
                  Open dashboard <ArrowRight className="w-4 h-4" />
                </Button>
              </Link>
            )}
          </div>
          <div className="space-y-3">
            {run.steps.map((step) => (
              <StepRow key={step.name} step={step} />
            ))}
          </div>
        </Card>

        {/* Final metrics card (only when succeeded) */}
        {run.calc_summary && (
          <Card>
            <h3 className="text-sm font-medium text-ink-400 uppercase tracking-wider mb-4">
              Verified output
            </h3>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
              <Metric
                label="Total emissions"
                value={fmtTonnes(run.calc_summary.total_emissions_tco2e)}
                sub="tCO₂e"
              />
              <Metric
                label="Projected CBAM cost"
                value={fmtEur(run.calc_summary.projected_cbam_cost_eur)}
                sub="EUA × export"
              />
              <Metric
                label="Total SEE"
                value={`${run.calc_summary.total_see.toFixed(3)}`}
                sub={`adj ${run.calc_summary.adjusted_see.toFixed(3)}`}
              />
              <Metric
                label="Data quality"
                value={`±${run.calc_summary.uncertainty_pct.toFixed(1)}%`}
                sub={`${fmtPct(run.calc_summary.share_estimated, 1)} estimated`}
                tone={run.calc_summary.share_estimated > 0.2 ? 'warn' : 'ok'}
              />
            </div>
          </Card>
        )}
      </div>

      <div className="space-y-6">
        {/* Live log */}
        <Card className="overflow-hidden">
          <div className="flex items-center gap-2 mb-3">
            <Terminal className="w-4 h-4 text-ink-400" />
            <h3 className="text-sm font-medium text-ink-300">Live log</h3>
            {run.state === 'running' && (
              <span className="ml-auto flex items-center gap-1.5 text-xs text-accent-glow">
                <CircleDot className="w-3 h-3 animate-pulse" />
                streaming
              </span>
            )}
          </div>
          <div
            ref={logRef}
            className="font-mono text-[11px] text-ink-300 bg-ink-900/80 rounded-lg p-3 h-80 overflow-y-auto scrollbar-thin space-y-0.5"
          >
            {run.log_tail.length === 0 ? (
              <span className="text-ink-500">Waiting for output…</span>
            ) : (
              run.log_tail.map((line, i) => (
                <div key={i} className="whitespace-pre-wrap">
                  <span className="text-ink-600">{line.slice(0, 19)}</span>
                  <span className="ml-2">{line.slice(19)}</span>
                </div>
              ))
            )}
          </div>
        </Card>

        {/* Source-by-source ingestion counts */}
        {run.ingestion_summary && (
          <Card>
            <h3 className="text-sm font-medium text-ink-300 mb-3">
              Ingestion · {fmtNumber(run.ingestion_summary.total_records)} rows
            </h3>
            <div className="space-y-1.5">
              {run.ingestion_summary.events.map((e, i) => (
                <div key={i} className="flex items-center justify-between text-xs py-1.5 border-b border-white/5 last:border-b-0">
                  <div className="flex items-center gap-2">
                    <span className="pill border-white/10 bg-white/5 text-ink-300 text-[10px]">
                      {e.source.replace('SourceMethod.', '')}
                    </span>
                    <span className="font-mono text-ink-200">{e.stream}</span>
                  </div>
                  <div className="text-ink-400">
                    {e.ok}<span className="text-ink-600"> / </span>
                    <span className={e.errors > 0 ? 'text-rose-400' : 'text-ink-600'}>
                      {e.records}
                    </span>
                  </div>
                </div>
              ))}
            </div>
          </Card>
        )}

        {run.error && (
          <Card className="border-rose-400/30 bg-rose-500/5">
            <div className="flex items-start gap-3">
              <CircleAlert className="w-5 h-5 text-rose-400 flex-shrink-0" />
              <div>
                <h3 className="text-sm font-medium text-rose-400">Pipeline error</h3>
                <p className="text-xs text-ink-300 mt-1 font-mono">{run.error}</p>
              </div>
            </div>
          </Card>
        )}
      </div>
    </div>
  );
}

function StepRow({ step }: { step: RunStep }) {
  const Icon = STEP_ICONS[step.name] ?? CircleDot;
  return (
    <div className={clsx(
      'flex items-center gap-4 rounded-lg px-4 py-3 transition-colors',
      step.state === 'running'   && 'bg-accent/5 border border-accent/30',
      step.state === 'succeeded' && 'bg-emerald-400/5 border border-emerald-400/20',
      step.state === 'failed'    && 'bg-rose-500/5 border border-rose-400/30',
      step.state === 'pending'   && 'border border-white/5',
      step.state === 'skipped'   && 'border border-white/5 opacity-60',
    )}>
      <div className={clsx(
        'w-9 h-9 rounded-lg flex items-center justify-center flex-shrink-0',
        step.state === 'running'   && 'bg-accent/15 text-accent-glow',
        step.state === 'succeeded' && 'bg-emerald-400/15 text-emerald-400',
        step.state === 'failed'    && 'bg-rose-500/15 text-rose-400',
        step.state === 'pending'   && 'bg-white/5 text-ink-500',
        step.state === 'skipped'   && 'bg-white/5 text-ink-500',
      )}>
        {step.state === 'succeeded' ? <Check className="w-4 h-4" /> :
         step.state === 'running'   ? <Icon className="w-4 h-4 animate-pulse" /> :
         step.state === 'failed'    ? <CircleAlert className="w-4 h-4" /> :
         <Icon className="w-4 h-4" />}
      </div>
      <div className="flex-1 min-w-0">
        <div className="font-medium text-sm">{stepLabel(step.name)}</div>
        {step.detail && (
          <div className="text-xs text-ink-400 mt-0.5 truncate">{step.detail}</div>
        )}
      </div>
      <div className="text-xs text-ink-500 font-mono">
        {step.state === 'running' ? 'in progress' :
         step.state === 'pending' ? 'queued' :
         step.state === 'skipped' ? 'skipped'    :
         step.finished_at?.slice(11, 19)}
      </div>
    </div>
  );
}

function Metric({
  label, value, sub, tone = 'default',
}: { label: string; value: string; sub: string; tone?: 'default' | 'ok' | 'warn' }) {
  return (
    <div className="rounded-lg bg-ink-900/40 border border-white/5 p-3">
      <div className="text-[11px] text-ink-400 uppercase tracking-wide">{label}</div>
      <div className={clsx(
        'text-2xl font-semibold tracking-tight mt-1',
        tone === 'warn' && 'text-amber-400',
        tone === 'ok'   && 'text-emerald-400',
      )}>{value}</div>
      <div className="text-[10px] text-ink-500 mt-0.5">{sub}</div>
    </div>
  );
}

function Loading() {
  return (
    <div className="text-ink-400 text-sm flex items-center gap-2">
      <CircleDot className="w-4 h-4 animate-pulse" /> loading run…
    </div>
  );
}
