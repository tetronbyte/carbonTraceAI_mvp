'use client';

import { useQuery } from '@tanstack/react-query';
import {
  Box, Database, FileSearch, Fingerprint, Loader2, ScanText, ScrollText,
  Shield, Sparkles,
} from 'lucide-react';
import { useParams } from 'next/navigation';

import { api } from '@/lib/api';
import { Card, CardHeader } from '@/components/ui/Card';
import { Badge } from '@/components/ui/Badge';
import { fmtNumber } from '@/lib/format';

const SOURCE_ICON: Record<string, any> = {
  ERP:      Database,
  MANUAL:   ScanText,
  METER:    Sparkles,
  SUPPLIER: Fingerprint,
  INVOICE:  FileSearch,
};

const SOURCE_TONE: Record<string, string> = {
  ERP:      'border-accent/30 bg-accent/5 text-accent-glow',
  MANUAL:   'border-emerald-400/30 bg-emerald-400/5 text-emerald-400',
  METER:    'border-amber-400/30 bg-amber-400/5 text-amber-400',
  SUPPLIER: 'border-sky-400/30 bg-sky-400/5 text-sky-400',
  INVOICE:  'border-rose-400/30 bg-rose-400/5 text-rose-400',
};

export default function AuditPage() {
  const { runId } = useParams<{ runId: string }>();
  const auditQ = useQuery({
    queryKey: ['audit', runId],
    queryFn: () => api.getAudit(runId),
    refetchInterval: (q) =>
      q.state.data?.run.state === 'running' ? 1500 : false,
  });

  if (auditQ.isLoading || !auditQ.data) {
    return (
      <div className="text-ink-400 flex items-center gap-2">
        <Loader2 className="w-4 h-4 animate-spin" /> loading audit…
      </div>
    );
  }

  const { ingestion_events, table_volumes, dashboard, market_feeds } = auditQ.data;

  // Bucket events by source type for the depth banner
  const eventBySource: Record<string, number> = {};
  ingestion_events.forEach((e) => {
    const src = String(e.source).replace('SourceMethod.', '');
    eventBySource[src] = (eventBySource[src] ?? 0) + e.ok_count;
  });

  // First facility + product for emission-line drill-down
  const firstFacility = (dashboard as any)?.facilities?.[0];
  const firstProduct = firstFacility?.products?.[0];

  return (
    <div className="space-y-6">
      <div className="flex items-end justify-between">
        <div>
          <h1 className="text-2xl font-semibold tracking-tight flex items-center gap-2">
            <Shield className="w-5 h-5 text-accent-glow" />
            Audit trail
          </h1>
          <p className="text-sm text-ink-400 mt-1">
            Every number on the dashboard is traceable to a source document, a JSONL line, and an ERPNext record.
          </p>
        </div>
        <Badge className="border-white/10 bg-white/5 text-ink-300">
          {market_feeds.eua_source} · FX: {market_feeds.fx_source}
        </Badge>
      </div>

      {/* The depth banner — proves the 4 ingestion sources and the table volume */}
      <Card>
        <CardHeader title="Ingestion depth" subtitle="The four CBAM data-collection methods, all wired" />
        <div className="grid grid-cols-2 md:grid-cols-5 gap-3">
          {['ERP', 'MANUAL', 'METER', 'SUPPLIER', 'INVOICE'].map((src) => {
            const Icon = SOURCE_ICON[src] ?? Database;
            const count = eventBySource[src] ?? 0;
            return (
              <div key={src} className="rounded-lg border border-white/5 bg-ink-900/40 p-4">
                <div className={`pill text-[10px] mb-2 ${SOURCE_TONE[src]}`}>
                  <Icon className="w-3 h-3" /> {src}
                </div>
                <div className="text-2xl font-semibold tracking-tight">{fmtNumber(count)}</div>
                <div className="text-[10px] text-ink-500 mt-0.5">canonical rows</div>
              </div>
            );
          })}
        </div>
      </Card>

      {/* Canonical-store volumes */}
      <Card>
        <CardHeader
          title="Canonical store — table volumes"
          subtitle="Single source of truth; downstream calc + reports + dashboards read here"
        />
        <div className="grid grid-cols-2 md:grid-cols-4 gap-2 text-sm">
          {Object.entries(table_volumes)
            .sort((a, b) => b[1] - a[1])
            .map(([table, n]) => (
              <div key={table} className={`flex items-center justify-between rounded-md px-3 py-1.5
                ${n > 0 ? 'bg-ink-900/40 border border-white/5' : 'bg-ink-900/20 border border-white/[0.03] opacity-50'}`}>
                <span className="font-mono text-xs text-ink-300">{table}</span>
                <span className={`text-xs font-medium ${n > 0 ? 'text-emerald-400' : 'text-ink-500'}`}>
                  {fmtNumber(n)}
                </span>
              </div>
            ))}
        </div>
      </Card>

      {/* Ingestion event log */}
      <Card>
        <CardHeader title="ingestion_events" subtitle="Every sync stamps a row here; the verifier replays from this log" />
        {ingestion_events.length === 0 ? (
          <div className="text-ink-500 text-sm">No ingestion events recorded yet for this run.</div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="text-[11px] text-ink-400 uppercase tracking-wide">
                  <Th>Source</Th>
                  <Th>Stream</Th>
                  <Th right>Records</Th>
                  <Th right>OK</Th>
                  <Th right>Errors</Th>
                  <Th>Started</Th>
                </tr>
              </thead>
              <tbody>
                {ingestion_events.map((e, i) => {
                  const src = String(e.source).replace('SourceMethod.', '');
                  return (
                    <tr key={i} className="border-t border-white/5 hover:bg-white/[0.02]">
                      <td className="py-2 px-2">
                        <span className={`pill text-[10px] ${SOURCE_TONE[src] ?? 'border-white/10 bg-white/5 text-ink-300'}`}>
                          {src}
                        </span>
                      </td>
                      <td className="py-2 px-2 font-mono text-xs">{e.stream}</td>
                      <td className="py-2 px-2 text-right">{fmtNumber(e.record_count)}</td>
                      <td className="py-2 px-2 text-right text-emerald-400">{fmtNumber(e.ok_count)}</td>
                      <td className={`py-2 px-2 text-right ${e.error_count > 0 ? 'text-rose-400' : 'text-ink-500'}`}>
                        {fmtNumber(e.error_count)}
                      </td>
                      <td className="py-2 px-2 font-mono text-[11px] text-ink-400">
                        {String(e.started_at).slice(0, 19)}
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        )}
      </Card>

      {/* Per-emission-line provenance — the verifier's killer feature */}
      {firstProduct && (
        <Card>
          <CardHeader
            title={`Emission-line provenance · CN ${firstProduct.cn}`}
            subtitle="EF source, tier, uncertainty — citable for an EU-accredited verifier"
            right={
              <Badge className="border-white/10 bg-white/5 text-ink-300">
                <Box className="w-3 h-3" /> {firstProduct.lines.length} lines
              </Badge>
            }
          />
          <div className="space-y-1.5">
            {[...firstProduct.lines]
              .sort((a: any, b: any) => b.co2e - a.co2e)
              .map((l: any, i: number) => (
                <div key={i} className="rounded-lg border border-white/5 bg-ink-900/40 p-3">
                  <div className="flex items-start justify-between gap-3">
                    <div className="flex-1 min-w-0">
                      <div className="font-medium text-sm">{l.label}</div>
                      <div className="text-xs text-ink-400 mt-0.5">
                        <span className="font-mono">{fmtNumber(l.activity)} {l.activityUnit}</span>
                        <span className="mx-2 text-ink-600">×</span>
                        <span className="font-mono">{l.ef.toFixed(3)} {l.efUnit}</span>
                        <span className="mx-2 text-ink-600">=</span>
                        <span className="text-ink-200 font-medium">{fmtNumber(l.co2e)} tCO₂e</span>
                      </div>
                      <div className="text-[11px] text-ink-500 mt-1.5 italic">{l.source}</div>
                    </div>
                    <div className="flex flex-col items-end gap-1 flex-shrink-0">
                      <span className={`pill text-[10px] ${tierColorAudit(l.tier)}`}>
                        {l.tier.replace(/_/g, ' ')}
                      </span>
                      <span className="text-[10px] text-ink-500">±{l.uncertaintyPct.toFixed(1)}%</span>
                    </div>
                  </div>
                </div>
              ))}
          </div>
        </Card>
      )}

      {/* The replay-safety story */}
      <Card>
        <CardHeader title="Replayability" subtitle="What the verifier inherits" />
        <ol className="space-y-2.5 text-sm text-ink-300">
          {[
            ['Raw JSONL preserved per sync',
              'data/raw/erpnext/<stream>/<ts>.jsonl — re-run history any time'],
            ['Every canonical row stamped with raw_ref',
              'back-pointer to (file, line) — drill from CO₂e number to source doc'],
            ['ERPNext records remain browsable',
              `http://localhost:8080 — Work Orders → BOMs → POs → Suppliers → Invoices`],
            ['ingestion_events as the audit ledger',
              `${ingestion_events.length} events stamped this session; immutable timestamps`],
            ['CBAM XML signed at render time',
              'data/reports/cbam_quarterly_<run>.xml — what the EU declarant uploads'],
          ].map(([head, body]) => (
            <li key={head} className="flex gap-3">
              <ScrollText className="w-4 h-4 text-accent-glow flex-shrink-0 mt-0.5" />
              <div>
                <div className="font-medium text-ink-200">{head}</div>
                <div className="text-xs text-ink-500">{body}</div>
              </div>
            </li>
          ))}
        </ol>
      </Card>
    </div>
  );
}

function Th({ children, right }: { children?: React.ReactNode; right?: boolean }) {
  return <th className={`py-2 px-2 ${right ? 'text-right' : ''}`}>{children}</th>;
}

function tierColorAudit(tier: string) {
  switch (tier) {
    case 'measured':
    case 'supplier_actual': return 'border-emerald-400/30 bg-emerald-400/5 text-emerald-400';
    case 'national':        return 'border-sky-400/30 bg-sky-400/5 text-sky-400';
    case 'cbam_default':
    case 'ipcc_default':    return 'border-amber-400/30 bg-amber-400/5 text-amber-400';
    case 'estimated':       return 'border-rose-400/30 bg-rose-400/5 text-rose-400';
    default:                return 'border-white/10 bg-white/5 text-ink-300';
  }
}
