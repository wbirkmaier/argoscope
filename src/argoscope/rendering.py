from __future__ import annotations

import json
from pathlib import Path

from pydantic import ValidationError

from argoscope.exceptions import ArgoScopeError
from argoscope.models import CompareReport
from argoscope.policy import PolicyReport


def load_render_input(path: Path) -> CompareReport | PolicyReport:
    payload = json.loads(path.read_text())
    try:
        if "violations" in payload:
            return PolicyReport.model_validate(payload)
        return CompareReport.model_validate(payload)
    except ValidationError as error:
        raise ArgoScopeError(f"invalid render input: {path}: {error}") from error


def render_markdown(report: CompareReport | PolicyReport) -> str:
    if isinstance(report, CompareReport):
        return _render_compare_markdown(report)
    return _render_policy_markdown(report)


def _render_compare_markdown(report: CompareReport) -> str:
    lines = [
        (
            f"## ApplicationSet Compare: `{report.base_applicationset}` -> "
            f"`{report.head_applicationset}`"
        ),
        "",
        f"Added applications: {len(report.added_applications)}",
        f"Removed applications: {len(report.removed_applications)}",
        f"Changed destinations: {len(report.changed_applications)}",
        f"Findings: {len(report.findings)}",
        "",
    ]
    if report.added_applications:
        lines.append("### Added")
        lines.extend(
            f"- `{application.name}` -> `{application.cluster}` / `{application.namespace}`"
            for application in report.added_applications
        )
        lines.append("")
    if report.removed_applications:
        lines.append("### Removed")
        lines.extend(
            f"- `{application.name}` from `{application.cluster}` / `{application.namespace}`"
            for application in report.removed_applications
        )
        lines.append("")
    if report.changed_applications:
        lines.append("### Changed")
        lines.extend(
            (
                f"- `{application.name}` moved from `{application.before_cluster}` / "
                f"`{application.before_namespace}` to `{application.after_cluster}` / "
                f"`{application.after_namespace}`"
            )
            for application in report.changed_applications
        )
        lines.append("")
    if report.findings:
        lines.append("### Findings")
        lines.extend(
            f"- `{finding.application}`: `{finding.kind}` ({finding.severity}) - {finding.message}"
            for finding in report.findings
        )
    return "\n".join(lines).rstrip()


def _render_policy_markdown(report: PolicyReport) -> str:
    lines = [
        f"## Policy Report: `{report.policy}`",
        "",
        f"ApplicationSet: `{report.applicationset}`",
        f"Violations: {len(report.violations)}",
        "",
    ]
    if not report.violations:
        lines.append("No violations detected.")
        return "\n".join(lines)

    lines.append("### Violations")
    lines.extend(
        (
            f"- `{violation.application}`: `{violation.rule_id}` "
            f"({violation.severity}) - {violation.message}"
        )
        for violation in report.violations
    )
    return "\n".join(lines)
