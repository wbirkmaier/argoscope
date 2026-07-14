from pathlib import Path

from argoscope.rendering import load_render_input, render_markdown


def test_render_markdown_for_compare_report_matches_golden_file() -> None:
    report = load_render_input(Path("tests/fixtures/review/compare-report.json"))

    rendered = render_markdown(report)

    assert rendered == Path("tests/fixtures/review/expected-compare.md").read_text().rstrip("\n")


def test_render_markdown_for_policy_report_matches_golden_file() -> None:
    report = load_render_input(Path("tests/fixtures/review/policy-report.json"))

    rendered = render_markdown(report)

    assert rendered == Path("tests/fixtures/review/expected-policy.md").read_text().rstrip("\n")
