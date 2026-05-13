'use client';

import { useMutation, useQuery } from '@tanstack/react-query';
import {
  ActivitySquare, ArrowRight, Building2, CheckCircle2, FlaskConical,
  Globe2, Loader2, Sparkles, Zap,
} from 'lucide-react';
import { useRouter } from 'next/navigation';
import { useEffect, useState } from 'react';

import { api, FactoryProfile } from '@/lib/api';
import { Button } from '@/components/ui/Button';
import { Card } from '@/components/ui/Card';

export default function LandingPage() {
  const router = useRouter();
  const profilesQ = useQuery({ queryKey: ['profiles'], queryFn: api.profiles });
  const [selected, setSelected] = useState<FactoryProfile | null>(null);
  const [baseUrl, setBaseUrl] = useState('http://localhost:8080');
  const [apiKey, setApiKey] = useState('');
  const [apiSecret, setApiSecret] = useState('');
  const [seedIfEmpty, setSeedIfEmpty] = useState(true);

  // Health probe (ERPNext reachable?)
  const healthQ = useQuery({
    queryKey: ['health', baseUrl],
    queryFn: () => api.health(baseUrl),
    enabled: !!baseUrl,
    refetchInterval: 6000,
  });

  // Pre-pick the first profile once profiles load.
  useEffect(() => {
    if (profilesQ.data && profilesQ.data.length > 0 && !selected) {
      setSelected(profilesQ.data[0]);
    }
  }, [profilesQ.data, selected]);

  const startMutation = useMutation({
    mutationFn: () =>
      api.startRun({
        profile_key: selected!.key,
        base_url: baseUrl,
        api_key: apiKey,
        api_secret: apiSecret,
        seed_if_empty: seedIfEmpty,
        fast_demo: true,
      }),
    onSuccess: (run) => router.push(`/runs/${run.run_id}/progress`),
  });

  const canStart = selected && baseUrl && apiKey && apiSecret && !startMutation.isPending;

  return (
    <main className="min-h-screen flex flex-col">
      <Header />
      <section className="flex-1 max-w-7xl mx-auto px-6 py-12 w-full">
        <div className="grid grid-cols-1 lg:grid-cols-[1.1fr_1fr] gap-10 items-start">
          {/* LEFT: hero + profile cards */}
          <div>
            <div className="mb-10">
              <span className="pill border-accent/30 bg-accent/10 text-accent-glow">
                <Sparkles className="w-3 h-3" /> CBAM Definitive Period · Q2 2026
              </span>
              <h1 className="mt-5 text-4xl md:text-5xl font-semibold tracking-tight leading-[1.05]">
                Audit-grade <span className="text-accent-glow">CBAM accounting</span>
                <br /> for African manufacturers.
              </h1>
              <p className="mt-4 text-ink-300 max-w-2xl">
                ERPNext-native ingestion. IPCC-cited calc engine. Every CO₂e number
                traceable to a source document. Pick a factory profile to launch
                an end-to-end run.
              </p>
            </div>

            <h2 className="text-sm font-medium text-ink-400 uppercase tracking-wider mb-3">
              1 · Choose a factory profile
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
              {profilesQ.isLoading && (
                <div className="col-span-2 text-ink-400 text-sm">Loading profiles…</div>
              )}
              {profilesQ.data?.map((p) => (
                <ProfileCard
                  key={p.key}
                  profile={p}
                  selected={selected?.key === p.key}
                  onClick={() => setSelected(p)}
                />
              ))}
            </div>

            <div className="mt-10">
              <h2 className="text-sm font-medium text-ink-400 uppercase tracking-wider mb-3">
                Pipeline depth at a glance
              </h2>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
                {DEPTH_STATS.map((s) => (
                  <div key={s.label} className="glass rounded-lg p-4">
                    <div className="text-2xl font-semibold tracking-tight">{s.value}</div>
                    <div className="text-xs text-ink-400 mt-1">{s.label}</div>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* RIGHT: ERP creds + launch */}
          <Card className="lg:sticky lg:top-8">
            <h2 className="text-sm font-medium text-ink-400 uppercase tracking-wider mb-1">
              2 · Connect ERPNext
            </h2>
            <p className="text-xs text-ink-500 mb-5">
              Sample admin credentials are pre-filled for the local sandbox.
            </p>

            <ConnectionStatus reachable={healthQ.data?.erpnext_reachable} />

            <div className="space-y-3 mt-4">
              <Field label="ERPNext base URL">
                <input
                  className="input"
                  value={baseUrl}
                  onChange={(e) => setBaseUrl(e.target.value)}
                  placeholder="http://localhost:8080"
                />
              </Field>
              <Field label="API key">
                <input
                  className="input font-mono"
                  value={apiKey}
                  onChange={(e) => setApiKey(e.target.value)}
                  placeholder="from .env.erpnext"
                />
              </Field>
              <Field label="API secret">
                <input
                  className="input font-mono"
                  type="password"
                  value={apiSecret}
                  onChange={(e) => setApiSecret(e.target.value)}
                  placeholder="••••••••"
                />
              </Field>

              <label className="flex items-center gap-2 text-sm text-ink-300 mt-3">
                <input
                  type="checkbox"
                  checked={seedIfEmpty}
                  onChange={(e) => setSeedIfEmpty(e.target.checked)}
                  className="rounded accent-accent"
                />
                Auto-seed ERPNext if empty (fast demo mode, ~90s)
              </label>
            </div>

            <div className="mt-5 flex flex-col gap-2">
              <Button
                size="lg"
                onClick={() => startMutation.mutate()}
                disabled={!canStart}
              >
                {startMutation.isPending ? (
                  <><Loader2 className="w-4 h-4 animate-spin" /> Starting…</>
                ) : (
                  <>Launch CBAM run <ArrowRight className="w-4 h-4" /></>
                )}
              </Button>
              {startMutation.isError && (
                <p className="text-xs text-rose-400">
                  {(startMutation.error as Error).message}
                </p>
              )}
              <p className="text-xs text-ink-500">
                Runs: connect → seed (if empty) → pull → manual + OCR → calc engine → reports.
              </p>
            </div>

            <div className="mt-6 pt-5 border-t border-white/5">
              <p className="text-xs text-ink-400 mb-2 font-medium">Sample administrator creds</p>
              <div className="font-mono text-[11px] text-ink-300 space-y-0.5">
                <div>URL  http://localhost:8080</div>
                <div>User Administrator / admin</div>
                <div className="text-ink-500">
                  API key/secret are auto-written to <code>.env.erpnext</code> after first seed.
                </div>
              </div>
            </div>
          </Card>
        </div>
      </section>

      <style jsx>{`
        .input {
          width: 100%;
          background: rgba(13, 16, 24, 0.7);
          border: 1px solid rgba(255, 255, 255, 0.08);
          border-radius: 0.5rem;
          padding: 0.5rem 0.75rem;
          font-size: 0.875rem;
          color: white;
          transition: border-color 0.15s, box-shadow 0.15s;
        }
        .input:focus {
          outline: none;
          border-color: rgba(99, 102, 241, 0.5);
          box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.15);
        }
      `}</style>
    </main>
  );
}

const DEPTH_STATS = [
  { label: '4 ingestion sources', value: 'ERP · OCR · Manual · Supplier' },
  { label: 'ERP modules consumed', value: '14' },
  { label: 'Canonical tables', value: '20' },
  { label: 'CBAM formulas wired', value: '4' },
];

function Header() {
  return (
    <header className="border-b border-white/5">
      <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
        <div className="flex items-center gap-2.5">
          <div className="w-7 h-7 rounded-md bg-gradient-to-br from-accent to-emerald-500 flex items-center justify-center">
            <ActivitySquare className="w-4 h-4 text-white" />
          </div>
          <span className="font-semibold tracking-tight">carbonTrace<span className="text-accent-glow">AI</span></span>
          <span className="pill border-white/10 bg-white/5 text-ink-400 ml-2 text-[10px]">
            v0.1 · CBAM definitive
          </span>
        </div>
        <nav className="flex gap-1">
          <a href="https://github.com/tetronbyte/carbonTraceAI_mvp" target="_blank" rel="noreferrer"
             className="text-xs text-ink-400 hover:text-ink-100 px-3 py-1.5 rounded-md hover:bg-white/5 transition-colors">
            GitHub
          </a>
        </nav>
      </div>
    </header>
  );
}

function ProfileCard({
  profile, selected, onClick,
}: { profile: FactoryProfile; selected: boolean; onClick: () => void }) {
  const totalCapacity = profile.products.reduce(
    (s, p) => s + p.monthly_output_tonnes * 12, 0
  );
  const productSummary = profile.products.map((p) => p.item_code.split('-')[0]).slice(0, 3).join(' · ');
  const Icon = profile.sector === 'aluminium' ? Zap : FlaskConical;

  return (
    <button
      type="button"
      onClick={onClick}
      className={`text-left glass rounded-xl p-5 transition-all glass-hover relative overflow-hidden
        ${selected
          ? 'border-accent/60 shadow-glow-accent bg-accent/5'
          : 'hover:border-white/15'}`}
    >
      <div className="flex items-start justify-between mb-3">
        <div className={`w-9 h-9 rounded-lg flex items-center justify-center
          ${profile.sector === 'aluminium' ? 'bg-amber-500/15 text-amber-400' : 'bg-emerald-500/15 text-emerald-400'}`}>
          <Icon className="w-4 h-4" />
        </div>
        {selected && <CheckCircle2 className="w-5 h-5 text-accent-glow" />}
      </div>
      <h3 className="font-semibold text-base">{profile.legal_name}</h3>
      <p className="text-xs text-ink-400 mt-0.5">{profile.plant_name}</p>

      <div className="mt-3 grid grid-cols-3 gap-1 text-[11px]">
        <Tag label="Country" value={profile.country} icon={<Globe2 className="w-3 h-3" />} />
        <Tag label="Capacity" value={`${(totalCapacity / 1e6).toFixed(1)}M t/y`} />
        <Tag label="Grid EF" value={`${profile.grid_ef_kgco2_per_kwh.toFixed(2)} kg/kWh`} />
      </div>
      <p className="text-[11px] text-ink-500 mt-3 font-mono">{productSummary}</p>
    </button>
  );
}

function Tag({ label, value, icon }: { label: string; value: string; icon?: React.ReactNode }) {
  return (
    <div>
      <div className="text-ink-500 flex items-center gap-1">{icon}{label}</div>
      <div className="text-ink-100 font-medium">{value}</div>
    </div>
  );
}

function Field({ label, children }: { label: string; children: React.ReactNode }) {
  return (
    <label className="block">
      <span className="text-xs text-ink-400 mb-1.5 block">{label}</span>
      {children}
    </label>
  );
}

function ConnectionStatus({ reachable }: { reachable: boolean | null | undefined }) {
  if (reachable === undefined || reachable === null) {
    return (
      <div className="flex items-center gap-2 text-xs text-ink-400">
        <div className="w-1.5 h-1.5 rounded-full bg-ink-500 animate-pulse-soft" />
        Probing ERPNext…
      </div>
    );
  }
  return reachable ? (
    <div className="flex items-center gap-2 text-xs text-emerald-400">
      <div className="w-1.5 h-1.5 rounded-full bg-emerald-400 shadow-[0_0_8px_rgba(16,185,129,0.6)]" />
      ERPNext reachable · Building2 ready
    </div>
  ) : (
    <div className="flex items-center gap-2 text-xs text-rose-400">
      <div className="w-1.5 h-1.5 rounded-full bg-rose-400" />
      ERPNext not reachable at this URL
    </div>
  );
}
