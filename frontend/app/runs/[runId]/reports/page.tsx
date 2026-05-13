'use client';

import { useQuery } from '@tanstack/react-query';
import {
  ArrowDownToLine, CheckCircle2, FileCode, FileSpreadsheet, FileText, Loader2,
  Lock, Send, Upload,
} from 'lucide-react';
import Link from 'next/link';
import { useParams } from 'next/navigation';

import { api } from '@/lib/api';
import { Card, CardHeader } from '@/components/ui/Card';
import { Badge } from '@/components/ui/Badge';
import { Button } from '@/components/ui/Button';
import { fmtEur, fmtNumber } from '@/lib/format';

export default function ReportsPage() {
  const { runId } = useParams<{ runId: string }>();
  const runQ = useQuery({ queryKey: ['run', runId], queryFn: () => api.getRun(runId) });
  const dashQ = useQuery({
    queryKey: ['dashboard', runId],
    queryFn: () => api.getDashboard(runId),
    retry: 1,
  });

  if (runQ.isLoading) {
    return (
      <div className="text-ink-400 flex items-center gap-2">
        <Loader2 className="w-4 h-4 animate-spin" /> loading…
      </div>
    );
  }

  const run = runQ.data;
  if (!run || run.state !== 'succeeded') {
    return (
      <Card>
        <h2 className="text-lg font-medium">Reports unavailable</h2>
        <p className="text-sm text-ink-400 mt-2">
          Reports are generated after the calc engine completes.
        </p>
        <Link href={`/runs/${runId}/progress`} className="text-accent-glow text-sm mt-3 inline-flex items-center gap-1">
          Watch progress →
        </Link>
      </Card>
    );
  }

  const facility = dashQ.data?.facilities[0];
  const products = facility?.products ?? [];

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-semibold tracking-tight flex items-center gap-2">
          <FileText className="w-5 h-5 text-accent-glow" />
          Quarterly reports
        </h1>
        <p className="text-sm text-ink-400 mt-1">
          {facility ? <>Generated for <span className="text-ink-200 font-medium">{facility.name}</span> · quarter {facility.quarter}</> : null}
        </p>
      </div>

      {/* The three artefacts */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <DownloadCard
          icon={<FileCode className="w-5 h-5 text-accent-glow" />}
          title="CBAM Quarterly XML"
          subtitle="EU CBAM IT-Tools schema · what the declarant uploads to the EU portal"
          features={[
            'Section 1-3 installation identity (EORI, UN-LOCODE, CBAM ID)',
            'Per-good EmbeddedEmissions block',
            'Emission lines with EF source citation',
            'Reconciliation residuals + estimation flags',
          ]}
          href={api.xmlUrl(runId)}
          filename={`cbam_quarterly_${runId.slice(0, 8)}.xml`}
        />
        <DownloadCard
          icon={<FileSpreadsheet className="w-5 h-5 text-amber-400" />}
          title="Dashboard CSV"
          subtitle="One row per facility × product × quarter — pivot-ready for BI tools"
          features={[
            '24 columns: output, EU export, direct/indirect/precursor split',
            'Total SEE + adjusted SEE',
            'Uncertainty + share-estimated',
            'Carbon price paid + CBAM cost',
          ]}
          href={api.csvUrl(runId)}
          filename={`cbam_quarterly_${runId.slice(0, 8)}.csv`}
        />
        <DownloadCard
          icon={<FileText className="w-5 h-5 text-emerald-400" />}
          title="Dashboard JSON"
          subtitle="Pre-aggregated for dashboards — the same shape this UI reads"
          features={[
            'Per-facility totals + reconciliation',
            'Per-product breakdown with allocation',
            'Per-emission-line provenance for drill-down',
            'Estimation-flag list for data-quality panel',
          ]}
          href={`/api/runs/${runId}/dashboard`}
          filename={`dashboard_${runId.slice(0, 8)}.json`}
        />
      </div>

      {/* Headline numbers block — easy print/PDF */}
      {facility && (
        <Card>
          <CardHeader
            title="Headline numbers"
            subtitle="What you'll see in the auditor's executive summary"
            right={<Badge className="border-emerald-400/30 bg-emerald-400/5 text-emerald-400">
              <CheckCircle2 className="w-3 h-3" /> Calc complete
            </Badge>}
          />
          <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
            <Stat label="Total emissions"   value={fmtNumber(facility.totals.totalTCO2e)}    unit="tCO₂e" />
            <Stat label="Direct (Scope 1)"  value={fmtNumber(facility.totals.directTCO2e)}   unit="tCO₂e" />
            <Stat label="Indirect (Scope 2)" value={fmtNumber(facility.totals.indirectTCO2e)} unit="tCO₂e" />
            <Stat label="Precursors"        value={fmtNumber(facility.totals.precursorTCO2e)} unit="tCO₂e" />
            <Stat label="Projected CBAM"    value={fmtEur(facility.totals.projectedCBAMCostEUR)}  unit="@ €75 EUA" />
            <Stat label="EU export share"   value={`${(facility.totals.euExportShare * 100).toFixed(1)}%`} unit="of output" />
            <Stat label="Products"          value={`${products.length}`} unit="CN codes" />
            <Stat label="Estimation flags"  value={`${facility.estimationFlags.length}`}
                  unit={facility.estimationFlags.length > 0 ? '> 20% est-share' : 'all within'} />
          </div>
        </Card>
      )}

      {/* Send to declarant */}
      <Card>
        <CardHeader title="Next step" subtitle="Forward the XML to your EU declarant" />
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="flex items-start gap-3">
            <div className="w-9 h-9 rounded-lg bg-accent/15 text-accent-glow flex items-center justify-center flex-shrink-0">
              <Upload className="w-4 h-4" />
            </div>
            <div>
              <div className="font-medium text-sm">EU CBAM portal upload</div>
              <p className="text-xs text-ink-400 mt-1">
                Your EU importer uploads the XML to the Commission's transitional CBAM Registry.
                Schema slots into the IT-Tools format 1:1.
              </p>
            </div>
          </div>
          <div className="flex items-start gap-3">
            <div className="w-9 h-9 rounded-lg bg-emerald-400/15 text-emerald-400 flex items-center justify-center flex-shrink-0">
              <Send className="w-4 h-4" />
            </div>
            <div>
              <div className="font-medium text-sm">Verifier sign-off</div>
              <p className="text-xs text-ink-400 mt-1">
                Share the audit page (read-only) with your EU-accredited verifier (DNV / TÜV / BV).
                Every CO₂e number is traceable to its raw_ref.
              </p>
            </div>
          </div>
        </div>
      </Card>

      <p className="text-xs text-ink-500 flex items-center gap-1.5">
        <Lock className="w-3 h-3" /> All artefacts are stored locally at <code className="font-mono">data/reports/</code> and never leave your machine.
      </p>
    </div>
  );
}

function DownloadCard({
  icon, title, subtitle, features, href, filename,
}: {
  icon: React.ReactNode; title: string; subtitle: string;
  features: string[]; href: string; filename: string;
}) {
  return (
    <Card className="flex flex-col h-full">
      <div className="flex items-start gap-3 mb-3">
        <div className="w-10 h-10 rounded-lg bg-white/5 flex items-center justify-center">{icon}</div>
        <div className="flex-1">
          <h3 className="font-semibold">{title}</h3>
          <p className="text-xs text-ink-400 mt-0.5">{subtitle}</p>
        </div>
      </div>
      <ul className="text-xs text-ink-300 space-y-1.5 mb-4 flex-1">
        {features.map((f) => (
          <li key={f} className="flex items-start gap-2">
            <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400 flex-shrink-0 mt-0.5" />
            {f}
          </li>
        ))}
      </ul>
      <a href={href} download={filename} className="mt-auto">
        <Button className="w-full" variant="secondary">
          <ArrowDownToLine className="w-4 h-4" /> Download {filename.split('.').pop()?.toUpperCase()}
        </Button>
      </a>
    </Card>
  );
}

function Stat({ label, value, unit }: { label: string; value: string; unit: string }) {
  return (
    <div className="rounded-lg bg-ink-900/40 border border-white/5 p-3">
      <div className="text-[10px] text-ink-400 uppercase tracking-wider">{label}</div>
      <div className="text-xl font-semibold tracking-tight mt-1">{value}</div>
      <div className="text-[10px] text-ink-500 mt-0.5">{unit}</div>
    </div>
  );
}
