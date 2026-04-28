# Reliability Analysis MVP

MVP web application for functional reliability / mission reliability analysis.

## Tech Stack
- Frontend: React + TypeScript (Vite)
- Backend: FastAPI + SQLite
- Calculation Engine: Independent Python module (`calc_engine/reliability_engine`)
- Excel Export: openpyxl
- PowerPoint Export: python-pptx

## Quick Start

### Backend
```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

### Tests
```bash
cd backend
pytest -q
```

## Scope (MVP)
- Exponential reliability with constant failure rate
- 1oo1 and 1oo2 active redundancy
- Simple RBD definition and solve (acyclic, no loops)
- Auto FTA derivation for failure to operate from RBD
- Manual simple FTA for unintended operation data structures
- Rule-based recommendations
- Excel and PowerPoint export endpoints

## Out of scope (first iteration)
- Internet search for lambda values (placeholder service only)
- Periodic testing logic
- Weibull distributions
- Repairable systems
- Standby redundancy
- Loops and common-cause failure model
