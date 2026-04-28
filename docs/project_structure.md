# Proposed Project Structure

```
ReliabilityAnalysisCodex/
├── backend/
│   ├── app/
│   │   ├── api/                # FastAPI routes
│   │   ├── core/               # settings/config
│   │   ├── db/                 # SQLAlchemy session/base
│   │   ├── models/             # ORM entities
│   │   ├── schemas/            # Pydantic schemas
│   │   └── services/           # calculation/export/sample-loading services
│   ├── tests/                  # unit tests
│   ├── requirements.txt
│   └── pytest.ini
├── calc_engine/
│   └── reliability_engine/     # independent reliability and logic module
├── frontend/
│   └── src/
│       ├── api/                # API client
│       ├── pages/              # simple UI screens
│       └── types/              # shared TS models
├── sample_data/
│   └── demo_system.json
└── docs/
    └── project_structure.md
```
