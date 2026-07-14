import json
from pathlib import Path

from typer.testing import CliRunner

from argoscope.cli import app


def test_compare_matches_expected_output() -> None:
    fixture_dir = Path("tests/fixtures/compare")
    expected = json.loads((fixture_dir / "expected-compare.json").read_text())

    result = CliRunner().invoke(
        app,
        [
            "compare",
            str(fixture_dir / "base.rendered.json"),
            str(fixture_dir / "head.rendered.json"),
        ],
    )

    assert result.exit_code == 0
    assert json.loads(result.stdout) == expected
