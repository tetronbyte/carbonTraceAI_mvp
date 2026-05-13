# 05 — Full-Stack Setup: From a Clean Machine to a Live Demo

End-to-end setup for the full system: ERPNext sandbox + FastAPI server + Next.js
frontend. Five commands gets you to `http://localhost:3000` with real factory
data flowing through the calc engine into a polished UI.

> Backend-only setup (no frontend) is in [02_SETUP_AND_RUN.md](02_SETUP_AND_RUN.md).
> This doc supersedes it for the full-stack demo.

---

## 0. Prerequisites

| Tool | Version | Why | Install |
|---|---|---|---|
| Python | **3.12+** | Backend runtime | macOS `brew install python@3.12` · Linux `apt install python3.12 python3.12-venv` |
| Node | **20+** (tested on 25) | Next.js frontend | `brew install node` · or [nvm](https://github.com/nvm-sh/nvm) |
| npm | 10+ | Pkg manager | bundled with Node |
| Docker Desktop | 4.30+ | ERPNext sandbox | https://www.docker.com/products/docker-desktop |
| Tesseract | 5.x | OCR invoice extraction | `brew install tesseract` · `apt install tesseract-ocr` |
| ngrok | latest | Remote-demo HTTPS tunnel (optional) | `brew install ngrok` |

Verify:

```bash
python3 --version    # 3.12 or higher
node --version       # v20 or higher
npm --version        # 10 or higher
docker --version     # Docker version 24+
tesseract --version  # tesseract 5+
```

---

## 1. Clone + Python environment

```bash
cd /path/to/carbonTraceAI_mvp
python3 -m venv .venv
source .venv/bin/activate
pip install --prefer-binary --no-cache-dir -r requirements.txt
```

The `--prefer-binary --no-cache-dir` flags avoid the cryptography build-from-source hang on slow networks. Total install ~2–3 minutes.

Verify backend:

```bash
python -m pytest tests/ -q -W "ignore::DeprecationWarning"
# expected: 30 passed in ~1.4s
```

---

## 2. Install frontend dependencies

```bash
cd frontend
npm install --no-audit --no-fund
cd ..
```

This pulls Next.js 15, React 19, Tailwind, Recharts, TanStack Query, lucide-react — ~147 packages, ~2 minutes on a cold cache.

Verify frontend builds:

```bash
cd frontend
npx tsc --noEmit          # typecheck — should be silent
npm run build             # production build — should report 4 dynamic + 1 static route
cd ..
```

---

## 3. Boot ERPNext

```bash
docker compose -f docker-compose.erpnext.yml up -d
```

First boot pulls `frappe/erpnext:v15.74.4` (~1.5 GB) and bootstraps a new site. **Expect 3–5 minutes** before `http://localhost:8080` responds.

Watch progress:

```bash
docker compose -f docker-compose.erpnext.yml logs -f create-site
```

When you see `Installing erpnext... done` and the spinner stops, hit:

```
http://localhost:8080
Login: Administrator / admin
```

You'll land on the empty ERPNext desk.

---

## 4. Seed the factory profile

This injects ~5k records (Items, Suppliers, BOMs, Work Orders, POs, Invoices, Stock Entries, Quality Inspections, Sales Invoices) and writes API credentials to `.env.erpnext`.

```bash
source .venv/bin/activate
python -m scripts.seed_erpnext --profile mozal_aluminium
# or:   --profile ocp_fertiliser
```

**For the YC demo, use fast-mode** (~90 s instead of 10–25 min):

```bash
python -m scripts.seed_erpnext \
  --profile mozal_aluminium \
  --months 3 \
  --work-orders-per-month 12 \
  --purchase-orders-per-month 8
```

Expected console:

```
[seed:mozal_aluminium] items=10 suppliers=10 customers=5 cost_centres=5 boms=2
                       wo=72 rework=1 po=192 pinv=115 stock=72 qa=72
                       sinv=18 errors=0
```

The file `.env.erpnext` now contains the API key/secret you'll paste into the UI:

```
ERPNEXT_BASE_URL=http://localhost:8080
ERPNEXT_API_KEY=<32-char hex>
ERPNEXT_API_SECRET=<32-char hex>
```

> The frontend pre-fills the URL but **doesn't auto-fill the key/secret** — paste them in manually. Open `.env.erpnext` with your editor.

---

## 5. Start the API + frontend (one shot)

```bash
./scripts/start_demo.sh
```

What it does:

1. Activates `.venv`
2. Boots `uvicorn src.api.main:app --port 8000 --reload`
3. Boots `npm run dev` in `frontend/` → `:3000`
4. Ctrl-C kills both

You should see:

```
▶ FastAPI on :8000
INFO:     Uvicorn running on http://0.0.0.0:8000
▶ Next.js on :3000
▶ Ready in 1.2s
```

Or start them in separate terminals:

```bash
# Terminal 1
source .venv/bin/activate
uvicorn src.api.main:app --port 8000 --reload

# Terminal 2
cd frontend
npm run dev
```

---

## 6. Demo walkthrough — `http://localhost:3000`

### Step 1 — Landing page

You see two factory profile cards (Mozal · OCP) and an ERP credentials form on the right. The ERPNext reachability dot should be **emerald green** ("ERPNext reachable").

1. Click a profile card — it gets an indigo ring + check mark
2. Paste the **API key** and **API secret** from `.env.erpnext`
3. Leave "Auto-seed if empty" checked (it'll skip the seed since we already seeded)
4. Click **Launch CBAM run**

You're routed to `/runs/<run_id>/progress`.

### Step 2 — Live progress

The 6 pipeline steps light up sequentially:

```
✓ Connect to ERP            — reachable at http://localhost:8080
↷ Seed factory data         — already seeded
✓ Pull canonical streams    — 487 canonical rows
✓ Manual + supplier + OCR   — facility + sensor + supplier + OCR added
✓ CBAM calculation engine   — 27,304 tCO2e total
✓ Render reports            — 3 artefacts in data/reports/
```

The streaming log on the right shows every event timestamped. The verified-output band appears at the bottom once the run completes.

Click **Open dashboard**.

### Step 3 — Dashboard

You see:

- 4 KPI tiles (total / CBAM cost / EU export share / grid EF)
- Emission-split donut (Direct · Indirect · Precursor)
- SEE per-product bar chart with adjusted SEE overlay
- Reconciliation health card (mass-balance, energy-balance, finance cross-check)
- Products table with click-through-able CN codes
- **Emission-lines table** — every contribution with category dot, activity × EF expansion, tier pill (e.g. "IPCC default" in amber), source citation (e.g. "IPCC V3 Ch4 Eq 4.20"), and uncertainty %

### Step 4 — Audit tab

Click **Audit trail** in the run tab nav.

- "Ingestion depth" banner shows all 5 source types with their canonical row counts (ERP / MANUAL / METER / SUPPLIER / INVOICE)
- "Canonical store" grid — every one of the 20 tables with its volume, dimmed if empty
- `ingestion_events` log — one row per ingestor invocation, immutable
- Per-line provenance cards — every emission line as its own card with the activity × EF computation made explicit

### Step 5 — Reports tab

Three download cards: XML / CSV / JSON. Click any → file downloads via `/api/runs/<id>/{xml,csv,dashboard}` (CSV and JSON are streamed through FastAPI, XML is a `FileResponse`).

---

## 7. Remote-demo path (ngrok)

For pitching to a remote audience (e.g. a YC partner):

```bash
ngrok http 3000
```

You'll get an `https://*.ngrok-free.app` URL. Share it. The frontend talks to its own backend via the `/api/*` rewrite in `next.config.mjs`, which proxies through the Next dev server — no separate API tunnel needed.

For Airbyte Cloud → local ERPNext, tunnel port 8080 instead and use the resulting URL as the ERPNext base URL in the onboarding form.

---

## 8. Environment variables

Set in `.env` (auto-loaded by `python-dotenv`) or your shell:

| Var | Default | Purpose |
|---|---|---|
| `CARBONTRACE_DB_URL` | `sqlite:///data/carbontrace.db` | Canonical store URL — Postgres also works |
| `CARBONTRACE_VAULT_KEY` | auto-generated at `data/.vault.key` | Fernet key for the credential vault. **Set explicitly in prod** |
| `CARBONTRACE_DATA_DIR` | `./data` | Where raw landings + reports go |
| `CARBONTRACE_EUA_OVERRIDE` | (none) | Manual EUA spot price for live demos. Else market_feeds falls back to static `€75/tCO2e` |
| `ERPNEXT_BASE_URL` | (written by seed) | Used by `scripts/run_erpnext_pipeline.py` |
| `ERPNEXT_API_KEY` / `ERPNEXT_API_SECRET` | (written by seed) | Frappe API tokens |
| `AIRBYTE_API_URL` | `http://localhost:8000/api/v1` | Airbyte API base (for `erpnext_airbyte` connector) |

The frontend has no env vars of its own in the current build — the `/api/*` rewrite target is hardcoded to `http://localhost:8000` in `next.config.mjs`. Change there if you move the API.

---

## 9. Smoke test (no Docker, ~30 seconds)

If you don't want to wait for ERPNext, you can seed the canonical store directly from Python and exercise only the calc engine + reports. See [02_SETUP_AND_RUN.md §2](02_SETUP_AND_RUN.md) for the inline Python snippet.

The frontend will still render — the run is triggered against ERPNext, but if you've already populated `data/carbontrace.db` and `data/reports/` directly, you can navigate to a static `/runs/manual-test` URL and the dashboard endpoint will pick up the latest report.

---

## 10. Troubleshooting

### Frontend won't install

```
ERESOLVE could not resolve react@^19 vs @types/react@^18
```

Already fixed in this build — `package.json` pins React 19 stable. If you re-introduce the conflict:

```bash
cd frontend
rm -rf node_modules package-lock.json
npm install --legacy-peer-deps
```

### `Connection refused` from frontend to API

The Next.js dev server proxies `/api/*` → `http://localhost:8000` per `next.config.mjs`. Confirm:

```bash
curl http://localhost:8000/api/health
# {"status":"ok", …}
```

If FastAPI isn't running on `:8000`, start it (`uvicorn src.api.main:app --port 8000 --reload`) or fix the proxy target in `frontend/next.config.mjs`.

### Port already in use

```bash
lsof -ti:8000 | xargs kill -9     # API port
lsof -ti:3000 | xargs kill -9     # Next.js port
lsof -ti:8080 | xargs kill -9     # ERPNext port (don't kill the docker process — `docker compose down` instead)
```

### `ERPNext unreachable` error in the UI

The landing page polls `/api/health?base_url=…` every 6 s. A red dot means:

- Wrong URL in the form → fix
- ERPNext still bootstrapping → wait (3–5 min on first boot)
- Docker container died → `docker compose -f docker-compose.erpnext.yml ps` → restart if needed

### API key/secret rejected

If you re-ran `docker compose down -v`, the old keys in `.env.erpnext` are invalid. Re-run `python -m scripts.seed_erpnext --profile mozal_aluminium` to mint fresh ones.

### Pipeline run hangs at "Seed factory data"

The full seed takes 10–25 minutes on a Mac. Use fast-demo mode:

```python
# In the UI, just click "Auto-seed if empty" — it sets fast_demo=True
# Or via API:
# POST /api/runs body {fast_demo: true} (default)
```

Or pre-seed once outside the UI:

```bash
python -m scripts.seed_erpnext --profile mozal_aluminium --months 3 --work-orders-per-month 12
```

### Charts don't render / "Cannot find module 'recharts'"

```bash
cd frontend
npm install recharts
```

### `OPENSSL`/Node 25 warnings during `npm run dev`

Cosmetic only — Next.js 15 + Node 25 work fine. Ignore.

---

## 11. The 5-command cheatsheet

```bash
# 1. Python + Node deps
python3 -m venv .venv && source .venv/bin/activate
pip install --prefer-binary --no-cache-dir -r requirements.txt
cd frontend && npm install --no-audit --no-fund && cd ..

# 2. ERPNext sandbox (wait 3-5 min on first boot)
docker compose -f docker-compose.erpnext.yml up -d

# 3. Seed it (~90 s in fast mode)
python -m scripts.seed_erpnext --profile mozal_aluminium --months 3 --work-orders-per-month 12

# 4. Start API + Next.js together
./scripts/start_demo.sh

# 5. Open the UI
open http://localhost:3000
```

Paste the API key/secret from `.env.erpnext` into the form, click Launch, watch the pipeline run, click through Dashboard → Audit → Reports.

---

## 12. Sample administrator credentials

For the YC demo or any external pitch:

```
ERPNext URL : http://localhost:8080
Username    : Administrator
Password    : admin
API Key     : (see .env.erpnext after first seed)
API Secret  : (see .env.erpnext after first seed)
```

These are local-sandbox creds — never use them in production. If you publish a demo via ngrok, the `Administrator/admin` credentials still apply but **anyone with the URL can see the data**. Add HTTP basic auth (FastAPI `HTTPBasic` dep) before sharing externally, or move auth to Clerk per [03_ROADMAP.md Phase 5](03_ROADMAP.md).

---

## 13. What you should read next

→ [06_NEXT_STEPS.md](06_NEXT_STEPS.md) — what's still soft in the frontend + calc engine, what to build for a YC-ready commercial product.
