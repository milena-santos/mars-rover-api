# Mars Rover API

REST API for launching and controlling robotic probes on a rectangular
plateau on Mars.

## Project status

The Django project foundation, probe domain logic, PostgreSQL persistence,
REST endpoints, application image, and local Docker Compose stack are in
place. Managed cloud environments will be delivered in later pull requests.

## API

| Method | Path | Purpose |
| --- | --- | --- |
| `GET` | `/health/` | Process and database health check |
| `POST` | `/api/probes/` | Launch a probe and configure its plateau |
| `POST` | `/api/probes/{id}/commands/` | Execute an atomic command sequence |
| `GET` | `/api/probes/` | List all probes |

Launch body:

```json
{"x": 5, "y": 5, "direction": "NORTH"}
```

Move body:

```json
{"commands": "MRM"}
```

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
files, and then starts Gunicorn on port `8000`.

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

## Planned technology

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
