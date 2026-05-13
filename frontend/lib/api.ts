// Typed client for the FastAPI server at :8000 (proxied via next.config rewrites).

export type FactoryProfile = {
  key: string;
  facility_code: string;
  sector: 'aluminium' | 'fertiliser';
  legal_name: string;
  plant_name: string;
  country: string;
  currency: string;
  electricity_supplier: string;
  grid_ef_kgco2_per_kwh: number;
  products: { item_code: string; monthly_output_tonnes: number; eu_export_share: number }[];
};

export type StepState = 'pending' | 'running' | 'succeeded' | 'failed' | 'skipped';

export type RunStep = {
  name: string;
  state: StepState;
  detail: string;
  started_at: string | null;
  finished_at: string | null;
};

export type RunStatus = {
  run_id: string;
  profile_key: string;
  base_url: string;
  state: 'queued' | 'running' | 'succeeded' | 'failed';
  started_at: string;
  finished_at: string | null;
  error: string | null;
  facility_id: string | null;
  steps: RunStep[];
  log_tail: string[];
  seed_summary: Record<string, number> | null;
  ingestion_summary: {
    events: { source: string; stream: string; records: number; ok: number; errors: number }[];
    total_records: number;
  } | null;
  calc_summary: {
    calc_run_id: string;
    facility_id: string;
    quarter: string;
    total_emissions_tco2e: number;
    projected_cbam_cost_eur: number;
    product_cn: string;
    total_see: number;
    adjusted_see: number;
    uncertainty_pct: number;
    share_estimated: number;
  } | null;
  artefacts: Record<string, string>;
};

export type EmissionLine = {
  category: 'fuel' | 'process' | 'electricity' | 'steam' | 'precursor';
  label: string;
  activity: number;
  activityUnit: string;
  ef: number;
  efUnit: string;
  tier: string;
  source: string;
  co2e: number;
  uncertaintyPct: number;
  estimated: boolean;
};

export type DashboardProduct = {
  cn: string;
  name: string;
  outputT: number;
  euExportT: number;
  directSEE: number;
  indirectSEE: number;
  totalSEE: number;
  adjustedSEE: number;
  uncertaintyPct: number;
  shareEstimated: number;
  carbonPricePaidEUR: number;
  cbamCostEUR: number;
  allocation: { method: string; share: number };
  lines: EmissionLine[];
};

export type DashboardFacility = {
  facilityId: string;
  name: string;
  country: string;
  sector: string;
  quarter: string;
  totals: {
    directTCO2e: number;
    indirectTCO2e: number;
    precursorTCO2e: number;
    totalTCO2e: number;
    projectedCBAMCostEUR: number;
    euExportShare: number;
  };
  reconciliation: {
    massBalanceResidualPct: number | null;
    energyBalanceResidualPct: number | null;
    financeResidualPct: number | null;
  };
  estimationFlags: string[];
  products: DashboardProduct[];
};

export type DashboardPayload = {
  runId: string;
  generatedAt: string;
  facilities: DashboardFacility[];
};

export type AuditPayload = {
  run: RunStatus;
  ingestion_events: {
    source: string;
    stream: string;
    record_count: number;
    ok_count: number;
    error_count: number;
    started_at: string;
    finished_at: string;
  }[];
  table_volumes: Record<string, number>;
  dashboard: DashboardPayload | Record<string, never>;
  market_feeds: { eua_source: string; fx_source: string; fetched_age_seconds: string };
};

async function jsonFetch<T>(path: string, init?: RequestInit): Promise<T> {
  const res = await fetch(path, {
    ...init,
    headers: { 'Content-Type': 'application/json', ...(init?.headers || {}) },
  });
  if (!res.ok) {
    const detail = await res.text().catch(() => '');
    throw new Error(`${res.status} ${res.statusText}: ${detail.slice(0, 200)}`);
  }
  return res.json() as Promise<T>;
}

export const api = {
  health: (baseUrl?: string) =>
    jsonFetch<{ status: string; erpnext_reachable: boolean | null; market_feeds: any }>(
      baseUrl ? `/api/health?base_url=${encodeURIComponent(baseUrl)}` : '/api/health'
    ),
  profiles: () => jsonFetch<FactoryProfile[]>('/api/profiles'),
  startRun: (body: {
    profile_key: string;
    base_url: string;
    api_key: string;
    api_secret: string;
    seed_if_empty?: boolean;
    fast_demo?: boolean;
  }) => jsonFetch<RunStatus>('/api/runs', { method: 'POST', body: JSON.stringify(body) }),
  getRun: (runId: string) => jsonFetch<RunStatus>(`/api/runs/${runId}`),
  listRuns: () => jsonFetch<RunStatus[]>('/api/runs'),
  getDashboard: (runId: string) => jsonFetch<DashboardPayload>(`/api/runs/${runId}/dashboard`),
  getAudit: (runId: string) => jsonFetch<AuditPayload>(`/api/runs/${runId}/audit`),
  xmlUrl: (runId: string) => `/api/runs/${runId}/xml`,
  csvUrl: (runId: string) => `/api/runs/${runId}/csv`,
};
