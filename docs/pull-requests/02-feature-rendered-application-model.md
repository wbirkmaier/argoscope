## Problem

ArgoScope had a repository baseline but no working analysis path for an ApplicationSet change.

## Approach

- added typed models for rendered Applications and normalized preview output
- implemented a fixture loader that pairs an ApplicationSet manifest with a sanitized rendered fixture
- exposed `argoscope preview <applicationset.yaml>` with deterministic JSON output

## Important decisions

- kept the renderer fixture-backed instead of attempting to reproduce ApplicationSet templating behavior in Python
- marked production targets conservatively from destination evidence rather than repository naming alone
- sorted generated Applications by destination and name so preview output is stable in review tools

## Test evidence

- `uv run ruff check .`
- `uv run mypy src`
- `uv run pytest`
- `uv run pytest --cov=src --cov-report=term-missing`
- `uv build`
- `uv run argoscope preview tests/fixtures/guestbook-appset/applicationset.yaml`

## Known limitations

- this slice imports rendered fixtures rather than invoking the Argo CD CLI
- no before/after comparison or policy checks yet

## Self-review

- [x] Security reviewed
- [x] No write operations introduced
- [x] Output ordering is deterministic
- [x] Impact claims are evidence-based

## Review findings

- no material findings after local self-review
