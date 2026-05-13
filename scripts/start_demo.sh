#!/usr/bin/env bash
# One-shot dev launcher: starts FastAPI on :8000 and Next.js on :3000.
# Usage:  ./scripts/start_demo.sh
# Ctrl-C kills both processes.

set -e
cd "$(dirname "$0")/.."

trap 'echo; echo "stopping…"; kill 0' EXIT INT TERM

# 1. FastAPI
if [ ! -d ".venv" ]; then
  echo "ERROR: .venv not found. Run: python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt"
  exit 1
fi
source .venv/bin/activate
echo "▶ FastAPI on :8000"
uvicorn src.api.main:app --port 8000 --reload &

# 2. Next.js
cd frontend
if [ ! -d "node_modules" ]; then
  echo "Installing frontend deps (first run)…"
  npm install --silent
fi
echo "▶ Next.js on :3000"
npm run dev &

wait
