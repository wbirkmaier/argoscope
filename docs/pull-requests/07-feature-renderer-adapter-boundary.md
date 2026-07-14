## Problem

ArgoScope still coupled preview behavior directly to fixture files, which would make later `argocd` CLI integration unnecessarily invasive.

## Approach

- added a small renderer adapter interface
- implemented a fixture-backed renderer adapter as the current shipped path
- added an explicit placeholder adapter for future `argocd` CLI rendering so unsupported live use fails clearly rather than implicitly

## Important decisions

- kept the adapter surface to one `render()` method returning the existing fixture model
- routed `preview` through the adapter now so later live integration can reuse the same analysis path
- made the future `argocd` adapter fail loudly with a targeted message instead of silently pretending live rendering worked

## Test evidence

- `uv run ruff check .`
- `uv run mypy src`
- `uv run pytest`
- `uv run pytest --cov=src --cov-report=term-missing`
- `uv build`
- `uv run argoscope preview tests/fixtures/guestbook-appset/applicationset.yaml --renderer fixture`

## Known limitations

- the `argocd` renderer mode is intentionally not implemented yet
- compare and check still consume persisted JSON or fixture-backed preview output rather than Git references

## Self-review

- [x] Security reviewed
- [x] No write operations introduced
- [x] Output ordering is deterministic
- [x] Impact claims are evidence-based

## Review findings

- no material findings after local self-review
