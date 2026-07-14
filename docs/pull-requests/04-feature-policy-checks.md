## Problem

ArgoScope could preview and compare generated Applications, but it still could not enforce rollout guardrails before review or merge.

## Approach

- added a small policy model for rendered ApplicationSet output
- evaluated production-only rules against normalized generated Applications
- exposed `argoscope check <applicationset.yaml> --policy <policy.yaml>` with JSON violations

## Important decisions

- kept the first policy set focused on production prune and mutable revisions because both are common blast-radius concerns in Argo CD reviews
- evaluated policies against normalized preview output rather than raw manifests so the rules stay stable across renderer inputs
- corrected the shipped production fixture to use a truly mutable revision (`main`) so the rule is exercised honestly

## Test evidence

- `uv run ruff check .`
- `uv run mypy src`
- `uv run pytest`
- `uv run pytest --cov=src --cov-report=term-missing`
- `uv build`
- `uv run argoscope check tests/fixtures/guestbook-appset/applicationset.yaml --policy tests/fixtures/policy/prod-guardrails.yaml`

## Known limitations

- policy files are JSON-shaped fixtures in this slice, not full Kubernetes-style policy CRDs
- cluster-scoped resource and deletion-risk checks are still pending

## Self-review

- [x] Security reviewed
- [x] No write operations introduced
- [x] Output ordering is deterministic
- [x] Impact claims are evidence-based

## Review findings

- no material findings after local self-review
