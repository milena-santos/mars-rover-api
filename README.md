# Mars Rover API

REST API for launching and controlling robotic probes on a rectangular
plateau on Mars.

## Project status

The Django project foundation, probe domain logic, PostgreSQL persistence,
REST endpoints, application image, local Docker Compose stack, and Render
Blueprint for staging and production are in place. Probes share one plateau,
reject collisions atomically, and keep successful command history.

## API

| Method | Path | Purpose |
| --- | --- | --- |
| `GET` | `/health/` | Process and database health check |
| `POST` | `/api/probes/` | Launch a probe on the shared plateau |
| `GET` | `/api/probes/{id}/` | Get one probe by id |
| `GET` | `/api/probes/{id}/history/` | List successful command sequences |
| `POST` | `/api/probes/{id}/commands/` | Execute an atomic command sequence |
| `GET` | `/api/probes/` | List all probes |

Launch body:

```json
{"x": 5, "y": 5, "direction": "NORTH"}
```

`x` and `y` are the shared plateau dimensions (upper-right corner). The probe
always starts at `(0, 0)`. The first launch creates the plateau. Later launches
must reuse the same dimensions and only succeed when `(0, 0)` is free.

Move body:

```json
{"commands": "MRM"}
```

Command sequences are atomic: out-of-bounds or collision leaves probe state
unchanged and does not create history entries.

Interactive OpenAPI docs are available at `/api/docs/` when the server is running.
The raw schema is at `/api/schema/`.

## Requirements

- Python 3.13
- [uv](https://docs.astral.sh/uv/)
- [Docker](https://docs.docker.com/get-docker/) and Docker Compose

## Local setup

### Full stack with Docker Compose

```bash
cp .env.example .env
docker compose up --build
```

Then open:

- [http://127.0.0.1:8000/health/](http://127.0.0.1:8000/health/)
- [http://127.0.0.1:8000/api/docs/](http://127.0.0.1:8000/api/docs/)

The `web` service runs migrations and collects static files before starting
Gunicorn.

### App on the host, database in Docker

```bash
cp .env.example .env
docker compose up -d postgres
uv sync --group dev
uv run python src/manage.py migrate
uv run python src/manage.py check
uv run pytest
uv run python src/manage.py runserver
```

Optional quality checks:

```bash
uv run ruff format .
uv run ruff check .
uv run mypy
```

Stop the local stack with:

```bash
docker compose down
```

## Settings

There is a single settings module: `config.settings`.

Runtime differences between local, CI, staging, and production come only from
environment variables. Every required variable must be set explicitly; there
are no configuration fallbacks.

Local development and CI use the PostgreSQL service defined in `compose.yaml`.
The Compose `web` service overrides `DATABASE_URL` so the app reaches Postgres
on the internal Docker network.

## Container image

```bash
docker build -t mars-rover-api .
```

The image entrypoint waits for the database, runs migrations, collects static
files, and then starts Gunicorn. The process listens on `PORT` when that
variable is set, otherwise on `8000`.

## Render environments

`render.yaml` defines one Render project with two environments:

| Environment | Git branch | Database | Deploy trigger |
| --- | --- | --- | --- |
| staging | `develop` | Neon (`DATABASE_URL`) | after CI checks pass |
| production | `main` | Neon (`DATABASE_URL`) | after CI checks pass |

Both web services run on Render. Both databases run on Neon so staging and
production stay consistent and avoid Render's single free Postgres limit.

### Neon databases

1. Create an account at [Neon](https://console.neon.tech).
2. Create a project (example name: `mars-rover-api`) in your preferred region.
3. Create two databases in that project, for example:
   - `mars_rover_staging`
   - `mars_rover_production`
4. Open **Connect** for each database and copy the Postgres URI.
5. Prefer URIs that include SSL, for example:
   `postgresql://USER:PASSWORD@HOST/mars_rover_staging?sslmode=require`

### First-time setup

1. Push this repository to GitHub.
2. Create the Neon databases and copy each `DATABASE_URL`.
3. In Render, create a Blueprint from `render.yaml`.
4. When prompted, set exact values only:
   - staging `ALLOWED_HOSTS`: `web-staging.onrender.com`
   - staging `CSRF_TRUSTED_ORIGINS`: `https://web-staging.onrender.com`
   - staging `DATABASE_URL`: Neon staging URI
   - production `ALLOWED_HOSTS`: `web-production.onrender.com`
   - production `CSRF_TRUSTED_ORIGINS`: `https://web-production.onrender.com`
   - production `DATABASE_URL`: Neon production URI
5. If Render assigns a hostname with a suffix, use that exact host/origin instead.
6. Do not use wildcards such as `.onrender.com` or `*`.
7. Confirm `/health/` and `/api/docs/` on staging and production.

## CI and CD

GitHub Actions runs formatting, linting, type checks, and tests on pull
requests and on pushes to `develop` / `main`. Required check names are always
`Format`, `Lint`, `Types`, and `Tests`. Concurrent runs for the same commit are
cancelled so those names are not duplicated.

Workflows that open pull requests must use a personal access token stored as
the repository secret `GH_WORKFLOW_TOKEN`. The default `GITHUB_TOKEN` cannot
reliably start required checks on PRs that Actions itself opens.

Create a classic or fine-grained PAT with permission to create pull requests on
this repository, then add it at
[Settings → Secrets and variables → Actions](https://github.com/milena-santos/mars-rover-api/settings/secrets/actions)
as `GH_WORKFLOW_TOKEN`.

Continuous delivery is handled by Render:

- merge to `develop` → CI passes → staging deploy
- merge to `main` → CI passes → production deploy + GitHub Release

`develop` and `main` require the CI checks to pass before merge.

## Development workflow

- `main` represents production.
- `develop` represents staging.
- Work is performed in short-lived branches created from `develop`.
- Every change reaches a permanent branch through a pull request.
- Merged short-lived branches are deleted automatically.

Branch names follow these conventions:

```text
feature/short-description
fix/short-description
chore/short-description
docs/short-description
refactor/short-description
test/short-description
hotfix/short-description
```

See [CONTRIBUTING.md](CONTRIBUTING.md) for the complete contribution workflow.

## Technology

- Django 5.2 LTS
- Django REST Framework
- PostgreSQL
- Pytest and Coverage.py
- Ruff and Mypy
- Docker
- Gunicorn and WhiteNoise
- GitHub Actions
- Render

## License

This project is licensed under the [MIT License](LICENSE).
