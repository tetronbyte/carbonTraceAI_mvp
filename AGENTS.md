# AGENTS.md

**Read [PROJECT_CONTEXT.md](PROJECT_CONTEXT.md) first.** Keep it updated after each meaningful change (feature, fix, decision, dependency, structure change), and make sure it is current before ending a session that changed files. No secrets in it.

## Setup (Windows, Git Bash paths)
```bash
python -m venv .venv
.venv/Scripts/python.exe -m pip install --prefer-binary --no-cache-dir -r requirements.txt
npm --prefix frontend install --no-audit --no-fund
```

## Run
`scripts/start_demo.sh` expects a Unix venv layout (`source .venv/bin/activate`), so on Windows start each service separately:
```bash
.venv/Scripts/python.exe -m uvicorn src.api.main:app --port 8000 --reload
npm --prefix frontend run dev
docker compose -f docker-compose.erpnext.yml up -d
.venv/Scripts/python.exe -m scripts.seed_erpnext --profile mozal_aluminium --months 3 --work-orders-per-month 12
```
UI at http://localhost:3000, API at http://localhost:8000, ERPNext at http://localhost:8080. ERPNext first boot takes 3-5 minutes.

## Test and build
```bash
.venv/Scripts/python.exe -m pytest tests/ -q -W "ignore::DeprecationWarning"
cd frontend && npx tsc --noEmit && npm run build
```

## Boundaries
- Never commit `.env.erpnext`, `data/.vault.key` or other credentials.
- Keep the canonical models and the calc engine's `CalculationRun` stable; they are the contract.
- `docker compose down -v` wipes ERPNext data and invalidates API keys. Ask first.
- Commit or push only when asked.

## Gotchas
- The `/api/*` proxy target is hardcoded in `frontend/next.config.mjs`.
- `.env.example` has a macOS `TESSERACT_CMD` path; change it on Windows.
- The seeder adds transactional docs on every run, so reseeding the same sandbox double-counts. Reset with `docker compose -f docker-compose.erpnext.yml down -v` first, then seed.
- Run seeding through `scripts.seed_erpnext`. It runs the setup wizard; `ERPNextSeeder` alone needs a site where the wizard already ran.
- Runs and their dashboard links live in API memory and are lost when the API restarts.
- More detail: [docs/05_FULL_STACK_SETUP.md](docs/05_FULL_STACK_SETUP.md).
