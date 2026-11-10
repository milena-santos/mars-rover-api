# Mars Rover API

REST API for launching and controlling robotic probes on a rectangular
plateau on Mars.

## Project status

The project is under active development. Its implementation is being delivered
in small, reviewable pull requests.

## Planned capabilities

- Launch a probe at `(0, 0)` with a configured plateau and direction.
- Rotate a probe left or right.
- Move a probe forward without leaving the plateau.
- Execute command sequences atomically.
- List the current position and direction of every probe.

## Planned technology

- Python 3.13
- Django 5.2 LTS
- Django REST Framework
- PostgreSQL
- Pytest and Coverage.py
- Ruff and Mypy
- Docker
- GitHub Actions

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

## Documentation

Setup, architecture, API usage, testing, and deployment instructions will be
added alongside their respective implementation phases. The README does not
describe features that are not yet available.

## License

This project is licensed under the [MIT License](LICENSE).

