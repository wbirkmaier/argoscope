from pathlib import Path

from typer.testing import CliRunner

from argoscope.cli import app


def test_render_markdown_for_compare_report() -> None:
    fixture_dir = Path("tests/fixtures/review")
    expected = (fixture_dir / "expected-compare.md").read_text().rstrip("\n")

    result = CliRunner().invoke(
        app,
        ["render", str(fixture_dir / "compare-report.json"), "--format", "markdown"],
    )

    assert result.exit_code == 0
    assert result.stdout == expected + "\n"
