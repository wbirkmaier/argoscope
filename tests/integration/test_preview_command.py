import json
from pathlib import Path

from typer.testing import CliRunner

from argoscope.cli import app


def test_preview_matches_expected_output() -> None:
    fixture_dir = Path("tests/fixtures/guestbook-appset")
    expected = json.loads((fixture_dir / "expected-preview.json").read_text())

    result = CliRunner().invoke(app, ["preview", str(fixture_dir / "applicationset.yaml")])

    assert result.exit_code == 0
    assert json.loads(result.stdout) == expected


def test_preview_reports_missing_rendered_fixture() -> None:
    fixture_dir = Path("tests/fixtures/missing-render")
    result = CliRunner().invoke(app, ["preview", str(fixture_dir / "applicationset.yaml")])

    assert result.exit_code == 2
