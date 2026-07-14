## Problem

ArgoScope had JSON outputs for automation, but reviewers still needed a concise pull-request friendly rendering for compare and policy results.

## Approach

- added report loading for compare and policy JSON artifacts
- rendered both report types into deterministic Markdown
- exposed `argoscope render <report.json> --format markdown`

## Important decisions

- kept JSON as the source-of-truth artifact and layered Markdown rendering on top of it
- supported compare and policy reports in one renderer so review workflows can stay simple
- used golden-file tests to keep review output stable as the report schemas evolve

## Test evidence

- `uv run ruff check .`
- `uv run mypy src`
- `uv run pytest`
- `uv run pytest --cov=src --cov-report=term-missing`
- `uv build`
- `uv run argoscope render tests/fixtures/review/compare-report.json --format markdown`

## Known limitations

- markdown output is intentionally compact and does not yet include policy rationale blocks or risk summaries
- only markdown is supported in this slice

## Self-review

- [x] Security reviewed
- [x] No write operations introduced
- [x] Output ordering is deterministic
- [x] Impact claims are evidence-based

## Review findings

- no material findings after local self-review
