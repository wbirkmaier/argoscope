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

Repository scaffolding and CLI baseline are in place. Rendering and blast-radius analysis land in later slices.
