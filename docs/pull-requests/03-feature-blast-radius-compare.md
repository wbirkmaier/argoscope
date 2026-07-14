## Problem

Previewing one rendered state is useful, but reviewers also need a direct before/after view of target changes between two ApplicationSet outputs.

## Approach

- added typed compare output for added, removed, and changed Applications
- implemented a snapshot loader for persisted preview JSON
- exposed `argoscope compare <base.json> <head.json>` for deterministic offline comparison

## Important decisions

- compared normalized preview reports rather than raw Application manifests so the diff focuses on rollout-relevant fields
- scoped the first compare pass to cluster, namespace, and production-target movement instead of overloading it with policy logic
- kept the command file-based for this slice; Git ref adapters can layer on later without changing the core diffing model

## Test evidence

- `uv run ruff check .`
- `uv run mypy src`
- `uv run pytest`
- `uv run pytest --cov=src --cov-report=term-missing`
- `uv build`
- `uv run argoscope compare tests/fixtures/compare/base.rendered.json tests/fixtures/compare/head.rendered.json`

## Known limitations

- compare does not yet classify mutable tag changes or cluster-scoped resource risk
- Git reference expansion is still pending

## Self-review

- [x] Security reviewed
- [x] No write operations introduced
- [x] Output ordering is deterministic
- [x] Impact claims are evidence-based

## Review findings

- no material findings after local self-review
