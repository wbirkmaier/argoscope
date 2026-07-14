from pathlib import Path

from argoscope.analysis import build_preview_report
from argoscope.fixtures import load_rendered_fixture
from argoscope.policy import evaluate_policy, load_policy


def test_evaluate_policy_flags_production_prune_and_mutable_revision() -> None:
    report = build_preview_report(
        load_rendered_fixture(Path("tests/fixtures/guestbook-appset/applicationset.yaml"))
    )
    policy = load_policy(Path("tests/fixtures/policy/prod-guardrails.yaml"))

    policy_report = evaluate_policy(policy, report)

    assert [violation.rule_id for violation in policy_report.violations] == [
        "prod-no-auto-prune",
        "prod-no-mutable-revision",
    ]
