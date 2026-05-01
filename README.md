# DocuWeave

A production-grade, open-source **document generation platform** with a canvas-based editor, spreadsheet editor, transformation engine, and backend-only data processing.

## Features

- **Dual editor modes**: free-position canvas (Word/`.docx`) and spreadsheet (Excel/`.xlsx`)
- **No SQL JOINs**: table relationships defined via JSON link configs; tables fetched in parallel, joined in-memory
- **Transformation engine**: concat, math, uppercase/lowercase, sum_by_group, count_by_group, and more — composable, nested, type-validated
- **Dual template database**: PostgreSQL/MySQL (SQLAlchemy + Alembic) or MongoDB (Beanie) — switch with `TEMPLATE_DB_TYPE`
- **Dual data database**: PostgreSQL, MySQL, or MongoDB data sources — switch with `DATA_DB_TYPE`
- **Selector system**: runtime popup for picking records; backend filters data accordingly
- **Strict TDD**: 74+ unit tests, integration test stubs, API tests

## Tech Stack

| Layer | Choice |
|---|---|
| Backend | Python 3.13, FastAPI, uv |
| Template DB (SQL) | SQLAlchemy 2.x async + Alembic |
| Template DB (NoSQL) | Beanie + Motor (MongoDB) |
| Data DB drivers | asyncpg, aiomysql, motor |
| Document output | python-docx, openpyxl |
| Frontend | Next.js 15, TypeScript, Tailwind CSS v4 |
| UI components | shadcn/ui (Radix UI) |
| Canvas editor | react-konva + TipTap + @dnd-kit |
| Spreadsheet editor | Fortune Sheet (`@fortune-sheet/react`) |
| State | Zustand + TanStack Query v5 |
| Monorepo | Turborepo + pnpm |

## Monorepo Structure

```
DocuWeave/
├── apps/
│   ├── backend/          # FastAPI + Clean Architecture
│   └── frontend/         # Next.js 15 App Router
├── packages/
│   └── shared-types/     # TypeScript interfaces shared across apps
├── samples/
│   ├── sql/seed_data.sql
│   └── link_config_example.json
├── docker-compose.yml
└── docker-compose.test.yml
```

## Quick Start

### Prerequisites

- [Docker & Docker Compose](https://docs.docker.com/get-docker/)
- [uv](https://docs.astral.sh/uv/getting-started/installation/) (Python package manager)
- [pnpm](https://pnpm.io/installation) + Node.js 20+

### 1. Start infrastructure

```bash
docker compose up -d
```

### 2. Backend

```bash
cd apps/backend
cp .env.example .env          # edit DB URLs if needed
uv sync
uv run alembic upgrade head   # run migrations
uv run uvicorn docuweave.main:app --reload
```

API at `http://localhost:8000` · Docs at `http://localhost:8000/docs`

### 3. Frontend

```bash
cd apps/frontend
pnpm install
pnpm dev
```

UI at `http://localhost:3000`

### 4. Seed sample data

```bash
psql "$DATA_DB_URL" -f samples/sql/seed_data.sql
```

## Environment Variables

| Variable | Default | Description |
|---|---|---|
| `TEMPLATE_DB_TYPE` | `postgres` | `postgres`, `mysql`, or `mongodb` |
| `TEMPLATE_DB_URL` | — | Connection URL for template DB |
| `DATA_DB_TYPE` | `postgres` | `postgres`, `mysql`, or `mongodb` |
| `DATA_DB_URL` | — | Connection URL for data DB |
| `BACKEND_HOST` | `0.0.0.0` | Uvicorn bind host |
| `BACKEND_PORT` | `8000` | Uvicorn port |

## Running Tests

### Unit + API tests (no Docker needed)

```bash
cd apps/backend
uv run pytest tests/unit/ tests/api/ -v
```

### Integration tests (requires docker-compose.test.yml)

```bash
docker compose -f docker-compose.test.yml up -d
uv run pytest tests/integration/ -v -m integration
```

### Frontend tests

```bash
cd apps/frontend
pnpm test
```

## API Overview

```
GET  /health
GET  /ready

GET|POST                   /api/v1/templates
GET|PUT|DELETE             /api/v1/templates/{id}
GET|POST                   /api/v1/templates/{id}/components
PUT|DELETE                 /api/v1/templates/{id}/components/{cid}

POST /api/v1/transformations/validate
POST /api/v1/transformations/preview

GET|POST                   /api/v1/data-sources
GET|PUT|DELETE             /api/v1/data-sources/{id}
POST                       /api/v1/data-sources/{id}/test
GET                        /api/v1/data-sources/{id}/tables
GET                        /api/v1/data-sources/{id}/tables/{table}/sample

POST /api/v1/selectors/options
POST /api/v1/selectors/evaluate

POST /api/v1/documents/generate   → FileResponse (.docx or .xlsx)
```

## Architecture

Clean Architecture with 4 layers:

```
domain/          Pure Python — entities, value objects, zero I/O
use_cases/       Application logic — transformations, parallel fetch, generation
adapters/        DB adapters, HTTP routers, Pydantic schemas
infrastructure/  SQLAlchemy engines, Beanie init, factory functions
```

No SQL JOINs. All cross-table relationships are expressed in a JSON `LinkConfig` and resolved in Python via hash-map joins after `asyncio.gather` parallel fetches.

## Example: Transformation Pipeline

```json
[
  {
    "output_field": "display_name",
    "field_type": "string",
    "pipeline": [
      {
        "op": "concat",
        "fields": [
          {"field": "first_name", "transformations": [{"op": "uppercase"}]},
          {"literal": " "},
          {"field": "last_name"}
        ]
      }
    ]
  },
  {
    "output_field": "dept_total_salary",
    "field_type": "number",
    "pipeline": [{"op": "sum_by_group", "group_field": "job_id", "value_field": "salary"}]
  }
]
```

## License

MIT
