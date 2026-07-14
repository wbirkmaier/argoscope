# ADR 0001: Start With Rendered Fixtures

## Status

Accepted

## Context

Argo CD templating behavior is rich, and local development should not depend on a live Argo installation.

## Decision

Use rendered Application fixtures and a small renderer adapter before attempting direct CLI integration.

## Consequences

- tests stay deterministic
- official CLI support can be added later without rewriting analysis logic
