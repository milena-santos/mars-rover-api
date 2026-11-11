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
{"x": 5, "y": 5, "landing_x": 0, "landing_y": 0, "direction": "NORTH"}
```

`x` and `y` are the shared plateau dimensions. The first launch creates the
plateau. Later launches must reuse the same dimensions and a free landing cell.

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

| Environment | Git branch | Deploy trigger |
| --- | --- | --- |
| staging | `develop` | after CI checks pass |
| production | `main` | after CI checks pass |

### First-time setup

1. Push this repository to GitHub.
2. In Render, create a Blueprint from `render.yaml`.
3. After the first deploy, copy each service hostname and HTTPS origin.
4. Set both values per environment with the exact service identity only:
   - staging `ALLOWED_HOSTS`: `your-staging-host.onrender.com`
   - staging `CSRF_TRUSTED_ORIGINS`: `https://your-staging-host.onrender.com`
   - production `ALLOWED_HOSTS`: `your-production-host.onrender.com`
   - production `CSRF_TRUSTED_ORIGINS`: `https://your-production-host.onrender.com`
5. Do not use wildcards such as `.onrender.com` or `*`.
6. Confirm `/health/` and `/api/docs/` on staging and production.

Free Render Postgres instances are ephemeral. Upgrade the database plan if you
need durable data.

## CI and CD

GitHub Actions runs formatting, linting, type checks, and tests on pull
requests and pushes.

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
