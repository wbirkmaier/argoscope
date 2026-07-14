# Architecture

ArgoScope separates rendering, normalization, impact analysis, and presentation.

## Planned flow

1. Adapters render or import generated Applications.
2. Normalizers convert rendered objects into typed deployment targets.
3. Analysis compares target sets, sync behavior, and policy-sensitive fields.
4. Renderers emit JSON, terminal summaries, and pull-request friendly Markdown.
