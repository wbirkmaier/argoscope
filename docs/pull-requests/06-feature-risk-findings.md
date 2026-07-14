## Problem

Compare output showed destination deltas, but it still lacked a higher-level risk signal that reviewers could scan quickly.

## Approach

- added blast-radius findings to compare reports
- flagged production expansion and direct introduction of new production Applications
- surfaced the same findings in Markdown review output

## Important decisions

- kept findings derived from before/after evidence rather than inventing heuristic severity scores disconnected from actual changes
- treated production expansion as high severity because it changes environment exposure even when the Application name stays the same
- only emit an automated-prune-enabled finding on a false-to-true transition, not merely because prune exists in the head state

## Test evidence

- `uv run ruff check .`
- `uv run mypy src`
- `uv run pytest`
- `uv run pytest --cov=src --cov-report=term-missing`
- `uv build`
- `uv run argoscope compare tests/fixtures/compare/base.rendered.json tests/fixtures/compare/head.rendered.json`

## Known limitations

- findings are still based on rendered Application metadata and do not inspect manifest-level resource scope yet
- deletion risk is implied through compare output, not summarized as a separate finding yet

## Self-review

- [x] Security reviewed
- [x] No write operations introduced
- [x] Output ordering is deterministic
- [x] Impact claims are evidence-based

## Review findings

- no material findings after local self-review
