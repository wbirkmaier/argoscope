# Contributing

## Local setup

1. Install `uv`.
2. Run `uv sync --all-extras --dev`.
3. Run `pre-commit install`.

## Validation

- `uv run ruff format --check .`
- `uv run ruff check .`
- `uv run mypy src`
- `uv run pytest`
- `uv run pytest --cov=src --cov-report=term-missing`
- `uv build`

## Scope

- Keep analysis read-only.
- Prefer official Argo CD rendering when available, with fixture adapters in tests.
- Do not claim resource deletion or production impact without direct evidence in the input.
