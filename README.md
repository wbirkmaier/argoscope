# ArgoScope

ArgoScope estimates the deployment blast radius of an Argo CD ApplicationSet change before it reaches a cluster.

## Current focus

- offline rendering from sanitized fixture inputs
- target cluster and namespace expansion
- policy and review-oriented reporting

## Deliberate limits

- no sync, prune, or delete actions
- no attempt to reproduce every Go-template edge case in Python
- no hidden repository or cluster access

## Running modes

- Offline: fixture-backed ApplicationSet rendering and comparison
- Live: planned adapter around the official Argo CD CLI when available

## Safety

- read-only by default
- deterministic JSON output
- explicit evidence for policy violations and inferred impact

## Status

```bash
uv run argoscope preview tests/fixtures/guestbook-appset/applicationset.yaml
uv run argoscope compare tests/fixtures/compare/base.rendered.json tests/fixtures/compare/head.rendered.json
```

`preview` works offline from rendered fixture data and returns generated application targets as JSON. `compare` reports added Applications, removed Applications, and destination or production-target changes between two rendered states. Policy checks and markdown review output land in later slices.
