from pathlib import Path

from argoscope.diffing import compare_preview_reports
from argoscope.snapshot_io import load_preview_report


def test_compare_preview_reports_detects_added_removed_and_changed_applications() -> None:
    base = load_preview_report(Path("tests/fixtures/compare/base.rendered.json"))
    head = load_preview_report(Path("tests/fixtures/compare/head.rendered.json"))

    report = compare_preview_reports(base, head)

    assert [item.name for item in report.added_applications] == ["guestbook-prod-canary"]
    assert [item.name for item in report.removed_applications] == ["guestbook-in-cluster"]
    assert report.changed_applications[0].name == "guestbook-staging-west"
    assert report.changed_applications[0].after_production_target is True
    assert [item.id for item in report.findings] == [
        "new-production-application:guestbook-prod-canary",
        "production-expansion:guestbook-staging-west",
    ]
