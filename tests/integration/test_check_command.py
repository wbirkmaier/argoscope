import json
from pathlib import Path

from typer.testing import CliRunner

from argoscope.cli import app


def test_check_matches_expected_output() -> None:
    fixture_root = Path("tests/fixtures")
    expected = json.loads((fixture_root / "policy" / "expected-report.json").read_text())

    result = CliRunner().invoke(
        app,
        [
            "check",
            str(fixture_root / "guestbook-appset" / "applicationset.yaml"),
            "--policy",
            str(fixture_root / "policy" / "prod-guardrails.yaml"),
        ],
    )

    assert result.exit_code == 0
    assert json.loads(result.stdout) == expected
