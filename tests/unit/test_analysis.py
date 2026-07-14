from pathlib import Path

from argoscope.adapters import ArgocdCliRendererAdapter, FixtureRendererAdapter
from argoscope.analysis import build_preview_report
from argoscope.exceptions import ArgoScopeError
from argoscope.fixtures import load_rendered_fixture


def test_build_preview_report_collects_clusters_and_namespaces() -> None:
    report = build_preview_report(
        load_rendered_fixture(Path("tests/fixtures/guestbook-appset/applicationset.yaml"))
    )

    assert report.clusters == [
        "https://kubernetes.default.svc",
        "https://prod-west.example.com",
        "https://staging-west.example.com",
    ]
    assert report.namespaces == ["guestbook", "guestbook-prod", "guestbook-staging"]


def test_build_preview_report_marks_production_targets() -> None:
    report = build_preview_report(
        load_rendered_fixture(Path("tests/fixtures/guestbook-appset/applicationset.yaml"))
    )
    production_flags = {
        application.name: application.production_target
        for application in report.generated_applications
    }

    assert production_flags["guestbook-prod-west"] is True
    assert production_flags["guestbook-staging-west"] is False


def test_fixture_renderer_adapter_loads_rendered_fixture() -> None:
    fixture = FixtureRendererAdapter().render(
        Path("tests/fixtures/guestbook-appset/applicationset.yaml")
    )

    assert fixture.applicationset == "guestbook-matrix"


def test_argocd_cli_adapter_reports_not_implemented() -> None:
    try:
        ArgocdCliRendererAdapter().render(
            Path("tests/fixtures/guestbook-appset/applicationset.yaml")
        )
    except ArgoScopeError as error:
        assert "live Argo CD rendering is not implemented" in str(error)
    else:
        raise AssertionError("expected ArgoScopeError")
