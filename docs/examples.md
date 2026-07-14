# Examples

```bash
uv run argoscope preview tests/fixtures/guestbook-appset/applicationset.yaml
uv run argoscope compare tests/fixtures/compare/base.rendered.json tests/fixtures/compare/head.rendered.json
uv run argoscope check tests/fixtures/guestbook-appset/applicationset.yaml --policy tests/fixtures/policy/prod-guardrails.yaml
```

The shipped fixture expands one ApplicationSet into three Applications across staging and production clusters.
