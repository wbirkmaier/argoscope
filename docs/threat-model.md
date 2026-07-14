# Threat Model

## Assets

- ApplicationSet manifests
- rendered Application definitions
- repository and cluster destination metadata

## Risks

- overstating production impact from weak heuristics
- accidentally invoking live Argo CD operations
- leaking repository credentials or private URLs in logs

## Mitigations

- fixture-first rendering in tests
- read-only CLI boundaries
- explicit evidence for every policy or blast-radius claim
