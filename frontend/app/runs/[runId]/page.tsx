'use client';

import { useQuery } from '@tanstack/react-query';
import {
  AlertTriangle, ArrowRight, CheckCircle2, Factory, Flag, Globe2,
  Leaf, Loader2, ScanLine, TrendingUp, Zap,
} from 'lucide-react';
import Link from 'next/link';
import { useParams } from 'next/navigation';
import clsx from 'clsx';
import {
  Bar, BarChart, Cell, Pie, PieChart, ResponsiveContainer, Tooltip,
  XAxis, YAxis,
} from 'recharts';

import { api, DashboardFacility } from '@/lib/api';
import { Card, CardHeader } from '@/components/ui/Card';
import { Badge } from '@/components/ui/Badge';
import {
  categoryColor, fmtEur, fmtNumber, fmtPct, fmtSEE, fmtTonnes, tierColor, tierLabel,
} from '@/lib/format';

export default function DashboardPage() {
  const { runId } = useParams<{ runId: string }>();
  const dashQ = useQuery({
    queryKey: ['dashboard', runId],
    queryFn: () => api.getDashboard(runId),
    refetchOnMount: 'always',
    retry: 2,
  });

  if (dashQ.isLoading) {
    return (
      <div className="text-ink-400 flex items-center gap-2">
        <Loader2 className="w-4 h-4 animate-spin" />
        Waiting for the calc engine…
      </div>
    );
  }

  if (dashQ.isError || !dashQ.data || dashQ.data.facilities.length === 0) {
    return (
      <Card>
        <h3 className="text-lg font-medium">No dashboard yet</h3>
        <p className="text-sm text-ink-400 mt-2">
          The dashboard JSON only appears once the calc engine has run.
        </p>
        <Link href={`/runs/${runId}/progress`} className="text-accent-glow text-sm mt-3 inline-flex items-center gap-1">
          Watch progress <ArrowRight className="w-3.5 h-3.5" />
        </Link>
      </Card>
    );
  }

  // For the MVP demo we render the first facility. Production would have a
  // facility switcher in the layout chrome.
  const facility = dashQ.data.facilities[0];
  return <FacilityDashboard facility={facility} />;
}

function FacilityDashboard({ facility }: { facility: DashboardFacility }) {
  const t = facility.totals;
  const recon = facility.reconciliation;

  return (
    <div className="space-y-6">
      {/* Header band */}
      <div className="flex items-end justify-between flex-wrap gap-3">
        <div>
          <div className="flex items-center gap-2 text-xs text-ink-400 mb-1">
            <Factory className="w-3.5 h-3.5" />
            <span className="font-mono">{facility.facilityId}</span>
            <span className="text-ink-600">•</span>
            <Globe2 className="w-3.5 h-3.5" />
            {facility.country}
            <span className="text-ink-600">•</span>
            <span className="capitalize">{facility.sector}</span>
          </div>
          <h1 className="text-2xl font-semibold tracking-tight">{facility.name}</h1>
        </div>
        <div className="flex items-center gap-2">
          <Badge className="border-accent/30 bg-accent/5 text-accent-glow">
            Quarter {facility.quarter}
          </Badge>
          {facility.estimationFlags.length > 0 ? (
            <Badge className="border-amber-400/30 bg-amber-400/5 text-amber-400">
              <AlertTriangle className="w-3 h-3" />
              {facility.estimationFlags.length} product{facility.estimationFlags.length > 1 ? 's' : ''} flagged
            </Badge>
          ) : (
            <Badge className="border-emerald-400/30 bg-emerald-400/5 text-emerald-400">
              <CheckCircle2 className="w-3 h-3" /> All within 20% est-share
            </Badge>
          )}
        </div>
      </div>

      {/* KPI tiles */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
        <Kpi label="Total emissions"
             value={fmtTonnes(t.totalTCO2e)}
             accent="text-ink-100"
             sub={`${fmtNumber(t.totalTCO2e)} tCO₂e`}
             icon={<Leaf className="w-3.5 h-3.5" />} />
        <Kpi label="Projected CBAM cost"
             value={fmtEur(t.projectedCBAMCostEUR)}
             accent="text-amber-400"
             sub={`@ €75 EUA × EU exports`}
             icon={<TrendingUp className="w-3.5 h-3.5" />} />
        <Kpi label="EU export share"
             value={`${(t.euExportShare * 100).toFixed(1)}%`}
             accent="text-accent-glow"
             sub="of total output"
             icon={<Globe2 className="w-3.5 h-3.5" />} />
        <Kpi label="Energy grid"
             value={`${facility.sector === 'aluminium' && facility.country === 'MZ' ? '0.04' : '0.62'} kg/kWh`}
             accent={facility.country === 'MZ' ? 'text-emerald-400' : 'text-ink-200'}
             sub={facility.country === 'MZ' ? 'Hydro advantage' : 'Grid-EF baseline'}
             icon={<Zap className="w-3.5 h-3.5" />} />
      </div>

      {/* Charts row */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <Card className="lg:col-span-1">
          <CardHeader title="Emission split" subtitle="Scope 1 · Scope 2 · Precursors" />
          <ResponsiveContainer width="100%" height={220}>
            <PieChart>
              <Pie
                dataKey="value"
                data={[
                  { name: 'Direct',    value: t.directTCO2e,    color: '#ef4444' },
                  { name: 'Indirect',  value: t.indirectTCO2e,  color: '#facc15' },
                  { name: 'Precursor', value: t.precursorTCO2e, color: '#6366f1' },
                ]}
                innerRadius={55}
                outerRadius={90}
                paddingAngle={3}
                stroke="none"
              >
                {[ '#ef4444', '#facc15', '#6366f1' ].map((c) => <Cell key={c} fill={c} />)}
              </Pie>
              <Tooltip
                contentStyle={{
                  background: '#0d1018', border: '1px solid rgba(255,255,255,0.1)',
                  borderRadius: 8, fontSize: 12,
                }}
                formatter={(v: number) => `${fmtNumber(v)} tCO₂e`}
              />
            </PieChart>
          </ResponsiveContainer>
          <div className="space-y-1.5 mt-2">
            <Legend color="#ef4444" label="Direct (fuel + process)"  v={t.directTCO2e} />
            <Legend color="#facc15" label="Indirect (electricity)"    v={t.indirectTCO2e} />
            <Legend color="#6366f1" label="Precursor (embedded)"      v={t.precursorTCO2e} />
          </div>
        </Card>

        <Card className="lg:col-span-2">
          <CardHeader
            title="Specific embedded emissions"
            subtitle="tCO₂e per tonne of product · adjusted = after Block-G deduction"
          />
          <ResponsiveContainer width="100%" height={220}>
            <BarChart data={facility.products.map(p => ({
              name: p.cn,
              total:    Number(p.totalSEE.toFixed(3)),
              adjusted: Number(p.adjustedSEE.toFixed(3)),
            }))} barCategoryGap="35%">
              <XAxis dataKey="name" stroke="#6c7689" fontSize={11} tickLine={false} axisLine={false} />
              <YAxis stroke="#6c7689" fontSize={11} tickLine={false} axisLine={false}
                     tickFormatter={(v) => v.toFixed(1)} />
              <Tooltip
                contentStyle={{
                  background: '#0d1018', border: '1px solid rgba(255,255,255,0.1)',
                  borderRadius: 8, fontSize: 12,
                }}
                formatter={(v: number) => v.toFixed(3)}
              />
              <Bar dataKey="total"    fill="#6366f1" radius={[4,4,0,0]} />
              <Bar dataKey="adjusted" fill="#34d399" radius={[4,4,0,0]} />
            </BarChart>
          </ResponsiveContainer>
          <div className="flex gap-4 text-xs text-ink-400 mt-2">
            <span className="flex items-center gap-1.5">
              <span className="w-2 h-2 rounded-sm bg-accent" /> Total SEE
            </span>
            <span className="flex items-center gap-1.5">
              <span className="w-2 h-2 rounded-sm bg-emerald-400" /> Adjusted (carbon-tax credited)
            </span>
          </div>
        </Card>
      </div>

      {/* Reconciliation + Per-product table */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <Card>
          <CardHeader title="Reconciliation health"
                      subtitle="Verifier checks · pass tolerances configurable" />
          <ReconciliationRow label="Mass balance"  pct={recon.massBalanceResidualPct}  tolerance={5}  />
          <ReconciliationRow label="Energy balance" pct={recon.energyBalanceResidualPct} tolerance={10} />
          <ReconciliationRow label="Finance cross-check" pct={recon.financeResidualPct} tolerance={2}  />
        </Card>

        <Card className="lg:col-span-2">
          <CardHeader title="Products"
                      subtitle={`${facility.products.length} CN code${facility.products.length === 1 ? '' : 's'} in this quarter`} />
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="text-[11px] text-ink-400 uppercase tracking-wide">
                  <Th>CN</Th>
                  <Th>Name</Th>
                  <Th right>Output</Th>
                  <Th right>EU exports</Th>
                  <Th right>Total SEE</Th>
                  <Th right>Adj SEE</Th>
                  <Th right>±%</Th>
                  <Th right>CBAM €</Th>
                  <Th right>Est %</Th>
                </tr>
              </thead>
              <tbody>
                {facility.products.map((p) => (
                  <tr key={p.cn} className="border-t border-white/5 hover:bg-white/[0.02]">
                    <Td><span className="font-mono">{p.cn}</span></Td>
                    <Td>{p.name}</Td>
                    <Td right>{fmtTonnes(p.outputT)}</Td>
                    <Td right>{fmtTonnes(p.euExportT)}</Td>
                    <Td right>{fmtSEE(p.totalSEE)}</Td>
                    <Td right><span className="text-emerald-400">{fmtSEE(p.adjustedSEE)}</span></Td>
                    <Td right>±{p.uncertaintyPct.toFixed(1)}%</Td>
                    <Td right>{fmtEur(p.cbamCostEUR)}</Td>
                    <Td right>
                      <span className={p.shareEstimated > 0.2 ? 'text-amber-400' : 'text-ink-300'}>
                        {(p.shareEstimated * 100).toFixed(0)}%
                      </span>
                    </Td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </Card>
      </div>

      {/* Emission lines (the depth view — sortable by category) */}
      {facility.products.map((p) => (
        <Card key={p.cn}>
          <CardHeader
            title={`Emission lines · CN ${p.cn}`}
            subtitle={`${p.lines.length} contributions · every value has tier + source citation`}
            right={
              <div className="flex items-center gap-2">
                <Badge className="border-white/10 bg-white/5 text-ink-300">
                  <Flag className="w-3 h-3" /> {p.allocation.method}
                </Badge>
              </div>
            }
          />
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="text-[11px] text-ink-400 uppercase tracking-wide">
                  <Th></Th>
                  <Th>Label</Th>
                  <Th right>Activity</Th>
                  <Th right>EF</Th>
                  <Th>Tier</Th>
                  <Th>Source</Th>
                  <Th right>CO₂e</Th>
                  <Th right>±%</Th>
                </tr>
              </thead>
              <tbody>
                {[...p.lines]
                  .sort((a, b) => b.co2e - a.co2e)
                  .map((l, i) => (
                  <tr key={i} className="border-t border-white/5">
                    <Td>
                      <span
                        className="inline-block w-2 h-2 rounded-sm"
                        style={{ background: categoryColor(l.category) }}
                      />
                    </Td>
                    <Td>{l.label}</Td>
                    <Td right>
                      <span className="font-mono text-xs">
                        {fmtNumber(l.activity)} {l.activityUnit}
                      </span>
                    </Td>
                    <Td right>
                      <span className="font-mono text-xs">
                        {l.ef.toFixed(3)} {l.efUnit}
                      </span>
                    </Td>
                    <Td>
                      <span className={clsx('pill text-[10px]', tierColor(l.tier))}>
                        {tierLabel(l.tier)}
                      </span>
                    </Td>
                    <Td>
                      <span className="text-[11px] text-ink-400">{l.source}</span>
                    </Td>
                    <Td right>
                      <span className="font-medium">{fmtNumber(l.co2e)} t</span>
                    </Td>
                    <Td right>±{l.uncertaintyPct.toFixed(1)}%</Td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </Card>
      ))}
    </div>
  );
}

function Kpi({
  label, value, accent, sub, icon,
}: { label: string; value: string; accent: string; sub: string; icon?: React.ReactNode }) {
  return (
    <Card>
      <div className="flex items-center gap-1.5 text-[11px] text-ink-400 uppercase tracking-wider mb-2">
        {icon}{label}
      </div>
      <div className={`text-3xl font-semibold tracking-tight ${accent}`}>{value}</div>
      <div className="text-xs text-ink-500 mt-1">{sub}</div>
    </Card>
  );
}

function Legend({ color, label, v }: { color: string; label: string; v: number }) {
  return (
    <div className="flex items-center justify-between text-xs">
      <div className="flex items-center gap-2 text-ink-300">
        <span className="w-2 h-2 rounded-sm" style={{ background: color }} />
        {label}
      </div>
      <span className="text-ink-200 font-medium">{fmtTonnes(v)}</span>
    </div>
  );
}

function ReconciliationRow({
  label, pct, tolerance,
}: { label: string; pct: number | null; tolerance: number }) {
  if (pct === null || pct === undefined) {
    return (
      <div className="flex items-center justify-between py-2.5 border-t border-white/5 first:border-t-0">
        <div className="text-sm text-ink-300">{label}</div>
        <span className="pill text-[10px] border-white/10 bg-white/5 text-ink-400">
          <ScanLine className="w-2.5 h-2.5" /> n/a
        </span>
      </div>
    );
  }
  const passing = pct <= tolerance;
  return (
    <div className="flex items-center justify-between py-2.5 border-t border-white/5 first:border-t-0">
      <div className="text-sm text-ink-300">{label}</div>
      <div className="flex items-center gap-2 text-xs">
        <span className="text-ink-400">residual {pct.toFixed(1)}%</span>
        <span className={clsx(
          'pill text-[10px]',
          passing
            ? 'border-emerald-400/30 bg-emerald-400/5 text-emerald-400'
            : 'border-amber-400/30 bg-amber-400/5 text-amber-400'
        )}>
          {passing
            ? <><CheckCircle2 className="w-2.5 h-2.5" /> within ±{tolerance}%</>
            : <><AlertTriangle className="w-2.5 h-2.5" /> exceeds ±{tolerance}%</>
          }
        </span>
      </div>
    </div>
  );
}

function Th({ children, right }: { children?: React.ReactNode; right?: boolean }) {
  return <th className={clsx('py-2 px-2', right && 'text-right')}>{children}</th>;
}

function Td({ children, right }: { children: React.ReactNode; right?: boolean }) {
  return <td className={clsx('py-2 px-2', right && 'text-right')}>{children}</td>;
}
