from __future__ import annotations

import json
from pathlib import Path

from pydantic import BaseModel, ValidationError

from argoscope.exceptions import ArgoScopeError
from argoscope.models import GeneratedApplication, PreviewReport


class PolicyRule(BaseModel):
    id: str
    description: str
    production_only: bool = False
    forbid_automated_prune: bool = False
    forbid_mutable_revisions: bool = False


class PolicyDocument(BaseModel):
    name: str
    rules: list[PolicyRule]


class PolicyViolation(BaseModel):
    rule_id: str
    application: str
    severity: str
    message: str


class PolicyReport(BaseModel):
    policy: str
    applicationset: str
    violations: list[PolicyViolation]


def load_policy(path: Path) -> PolicyDocument:
    try:
        return PolicyDocument.model_validate(json.loads(path.read_text()))
    except FileNotFoundError as error:
        raise ArgoScopeError(f"policy file not found: {path}") from error
    except ValidationError as error:
        raise ArgoScopeError(f"invalid policy file: {path}: {error}") from error


def _is_mutable_revision(revision: str) -> bool:
    lowered = revision.lower()
    return lowered in {"head", "main", "master", "latest"} or lowered.endswith(":latest")


def evaluate_policy(policy: PolicyDocument, report: PreviewReport) -> PolicyReport:
    violations: list[PolicyViolation] = []
    for application in report.generated_applications:
        for rule in policy.rules:
            if rule.production_only and not application.production_target:
                continue
            violations.extend(_evaluate_rule(rule, application))

    return PolicyReport(
        policy=policy.name,
        applicationset=report.applicationset,
        violations=sorted(
            violations, key=lambda item: (item.rule_id, item.application, item.message)
        ),
    )


def _evaluate_rule(rule: PolicyRule, application: GeneratedApplication) -> list[PolicyViolation]:
    violations: list[PolicyViolation] = []
    if rule.forbid_automated_prune and application.automated_prune:
        violations.append(
            PolicyViolation(
                rule_id=rule.id,
                application=application.name,
                severity="high",
                message="automated prune is enabled",
            )
        )
    if rule.forbid_mutable_revisions and _is_mutable_revision(application.target_revision):
        violations.append(
            PolicyViolation(
                rule_id=rule.id,
                application=application.name,
                severity="medium",
                message=f"mutable revision detected: {application.target_revision}",
            )
        )
    return violations
