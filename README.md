# Mars Rover API

REST API in Python for launching and controlling probes on a rectangular
Martian plateau. Companion UI:
[`mars-rover-web`](https://github.com/milena-santos/mars-rover-web).

**Live**

| Env | URL |
| --- | --- |
| Production docs | https://web-production-gbuy.onrender.com/api/docs/ |
| Staging docs | https://web-staging-pntn.onrender.com/api/docs/ |
| Front (prod) | https://mars-rover-web-prod.vercel.app |

## Overview

Implements the RD Station Mars probe challenge endpoints, plus a few deliberate
extras: shared plateau, landing/move collisions, command history, health check,
OpenAPI/Swagger, PostgreSQL, Docker, and CI/CD to Render.

Layout follows a pragmatic hexagonal split: domain rules stay free of Django;
application services orchestrate use cases; API and infrastructure adapters
sit at the edges.

## Challenge endpoints

| Method | Path | Purpose |
| --- | --- | --- |
| `POST` | `/api/probes/` | Launch a probe and configure the plateau |
| `POST` | `/api/probes/{id}/commands/` | Execute an atomic command sequence |
| `GET` | `/api/probes/` | List all probes |

### Launch

```http
POST /api/probes/
Content-Type: application/json

{"x": 5, "y": 5, "direction": "NORTH"}
```

`x` and `y` are the upper-right corner of the shared plateau. The probe always
starts at `(0, 0)`.

Success (`201`):

```json
{"id": "…", "x": 0, "y": 0, "direction": "NORTH"}
```

### Move

```http
POST /api/probes/{id}/commands/
Content-Type: application/json

{"commands": "MRM"}
```

Commands: `M` move forward, `L` turn left, `R` turn right. Out-of-bounds
sequences are rejected atomically (probe state unchanged).

Success (`200`):

```json
{"id": "…", "x": 1, "y": 1, "direction": "EAST"}
```

### List

```http
GET /api/probes/
```

```json
{
  "probes": [
    {"id": "…", "x": 1, "y": 1, "direction": "EAST"}
  ],
  "plateau": {"max_x": 5, "max_y": 5}
}
```

Interactive docs: `/api/docs/` · raw schema: `/api/schema/`.

## Extra behaviour

| Topic | Behaviour |
| --- | --- |
| Shared plateau | First launch creates it; later launches reuse the same size while probes exist |
| Landing collision | If `(0, 0)` is occupied, both probes are destroyed (`200`, `event: "collision"`) |
| Move collision | Moving onto another probe destroys both (`200`, `event: "collision"`) |
| History | Successful command sequences are stored per probe |
| Clear mission | `DELETE /api/probes/` removes probes and resets the plateau |
| Health | `GET /health/` checks process + database |

## Requirements

- Python 3.13
- [uv](https://docs.astral.sh/uv/)
- Docker / Docker Compose

## Local setup

### Full stack with Docker Compose

```bash
cp .env.example .env
docker compose up --build
```

- Health: http://127.0.0.1:8000/health/
- Swagger: http://127.0.0.1:8000/api/docs/

### App on the host, database in Docker

```bash
cp .env.example .env
docker compose up -d postgres
uv sync --group dev
uv run python src/manage.py migrate
uv run pytest
uv run python src/manage.py runserver
```

Quality checks:

```bash
uv run ruff format .
uv run ruff check .
uv run mypy
```

```bash
docker compose down
```

## Settings

Single module: `config.settings`. Local, CI, staging, and production differ
only by environment variables — every required value is explicit (no silent
fallbacks). See `.env.example`.

Compose wires Postgres on host port `5433` locally (container port `5432`) so
it does not clash with a local Postgres install.

## Technology

- Django 5.2 LTS + Django REST Framework + drf-spectacular
- PostgreSQL (local Compose; Neon in staging/production)
- Pytest + Coverage.py (≥ 80%)
- Ruff + Mypy
- Docker, Gunicorn, WhiteNoise
- GitHub Actions → Render

## Deploy (Render)

`render.yaml` defines staging (`develop`) and production (`main`). Databases
run on Neon.

When creating the Blueprint, set at least:

| Variable | Staging example | Production example |
| --- | --- | --- |
| `ALLOWED_HOSTS` | `web-staging-pntn.onrender.com` | `web-production-gbuy.onrender.com` |
| `CSRF_TRUSTED_ORIGINS` | `https://web-staging-pntn.onrender.com` | `https://web-production-gbuy.onrender.com` |
| `CORS_ALLOWED_ORIGINS` | front staging origin(s) | `https://mars-rover-web-prod.vercel.app` |
| `DATABASE_URL` | Neon staging URI | Neon production URI |

Use the exact Render hostname (including any suffix). No wildcards.

## CI and CD

GitHub Actions runs **Format**, **Lint**, **Types**, and **Tests** on PRs and
on pushes to `develop` / `main`.

- merge to `develop` → CI → staging deploy
- merge to `main` → CI → production deploy

Branch workflow and PR automation details: [CONTRIBUTING.md](CONTRIBUTING.md).

## License

[MIT](LICENSE)
