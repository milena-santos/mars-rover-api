# Mars Rover API

REST API for launching and controlling robotic probes on a rectangular
plateau on Mars.

## Project status

The Django project foundation is in place with PostgreSQL as the only
supported database. Probe domain logic, HTTP endpoints, application image,
and deployment will be delivered in later pull requests.

## Requirements

- Python 3.13
- [uv](https://docs.astral.sh/uv/)
- [Docker](https://docs.docker.com/get-docker/) and Docker Compose

## Local setup

```bash
cp .env.example .env
docker compose up -d postgres
uv sync --group dev
uv run python src/manage.py check
uv run pytest
```

Optional quality checks:

```bash
uv run ruff format .
uv run ruff check .
uv run mypy
```

Stop the local database with:

```bash
docker compose down
```

## Settings

There is a single settings module: `config.settings`.

Runtime differences between local, CI, staging, and production come only from
environment variables. Every required variable must be set explicitly; there
are no configuration fallbacks.

Local development and CI use the PostgreSQL service defined in `compose.yaml`.

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
- GitHub Actions

## License

This project is licensed under the [MIT License](LICENSE).
