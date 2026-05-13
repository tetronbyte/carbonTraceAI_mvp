export const fmtTonnes = (n: number) =>
  n >= 1_000_000 ? `${(n / 1_000_000).toFixed(2)}M t`
  : n >= 1_000 ? `${(n / 1_000).toFixed(1)}k t`
  : `${n.toFixed(0)} t`;

export const fmtEur = (n: number) =>
  n >= 1_000_000 ? `€${(n / 1_000_000).toFixed(2)}M`
  : n >= 1_000 ? `€${(n / 1_000).toFixed(0)}k`
  : `€${n.toFixed(0)}`;

export const fmtPct = (n: number, digits: number = 1) =>
  `${(n * (n < 1 && n > 0 ? 100 : 1)).toFixed(digits)}%`;

export const fmtNumber = (n: number) =>
  new Intl.NumberFormat('en-US', { maximumFractionDigits: 2 }).format(n);

export const fmtSEE = (n: number) => `${n.toFixed(3)}`;

export const tierColor = (tier: string) => {
  switch (tier) {
    case 'measured':         return 'text-emerald-400 border-emerald-400/30 bg-emerald-400/5';
    case 'supplier_actual':  return 'text-emerald-400 border-emerald-400/30 bg-emerald-400/5';
    case 'national':         return 'text-sky-400   border-sky-400/30   bg-sky-400/5';
    case 'cbam_default':     return 'text-amber-400 border-amber-400/30 bg-amber-400/5';
    case 'ipcc_default':     return 'text-amber-400 border-amber-400/30 bg-amber-400/5';
    case 'estimated':        return 'text-rose-400  border-rose-400/30  bg-rose-400/5';
    default:                 return 'text-ink-300   border-white/10     bg-white/5';
  }
};

export const tierLabel = (tier: string) => {
  switch (tier) {
    case 'measured':        return 'Measured';
    case 'supplier_actual': return 'Supplier verified';
    case 'national':        return 'National default';
    case 'cbam_default':    return 'CBAM Annex';
    case 'ipcc_default':    return 'IPCC default';
    case 'estimated':       return 'Estimated';
    default:                return tier;
  }
};

export const categoryColor = (cat: string) => {
  switch (cat) {
    case 'fuel':        return '#fb923c';   // orange
    case 'process':     return '#ef4444';   // red
    case 'electricity': return '#facc15';   // yellow
    case 'steam':       return '#f97316';   // dark orange
    case 'precursor':   return '#6366f1';   // indigo
    default:            return '#94a3b8';   // slate
  }
};

export const stepLabel = (name: string) => {
  switch (name) {
    case 'connect_erp':       return 'Connect to ERP';
    case 'seed_erp':          return 'Seed factory data';
    case 'pull_erp':          return 'Pull canonical streams';
    case 'manual_supplement': return 'Manual + supplier + OCR';
    case 'calculate':         return 'CBAM calculation engine';
    case 'render_reports':    return 'Render reports';
    default:                  return name.replace(/_/g, ' ');
  }
};
