from pathlib import Path

from argoscope.analysis import build_preview_report
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
