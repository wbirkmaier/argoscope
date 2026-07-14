from __future__ import annotations

from argoscope.models import ApplicationChange, BlastRadiusFinding, CompareReport, PreviewReport


def compare_preview_reports(base: PreviewReport, head: PreviewReport) -> CompareReport:
    base_map = {application.name: application for application in base.generated_applications}
    head_map = {application.name: application for application in head.generated_applications}

    changed_applications: list[ApplicationChange] = []
    findings: list[BlastRadiusFinding] = []
    for name in sorted(set(base_map) & set(head_map)):
        base_application = base_map[name]
        head_application = head_map[name]
        if (
            base_application.cluster != head_application.cluster
            or base_application.namespace != head_application.namespace
            or base_application.production_target != head_application.production_target
        ):
            changed_applications.append(
                ApplicationChange(
                    name=name,
                    before_cluster=base_application.cluster,
                    after_cluster=head_application.cluster,
                    before_namespace=base_application.namespace,
                    after_namespace=head_application.namespace,
                    before_production_target=base_application.production_target,
                    after_production_target=head_application.production_target,
                )
            )
        if not base_application.production_target and head_application.production_target:
            findings.append(
                BlastRadiusFinding(
                    id=f"production-expansion:{name}",
                    kind="production_expansion",
                    severity="high",
                    application=name,
                    message="application now targets a production destination",
                )
            )
        if not base_application.automated_prune and head_application.automated_prune:
            findings.append(
                BlastRadiusFinding(
                    id=f"automated-prune-enabled:{name}",
                    kind="automated_prune_enabled",
                    severity="medium",
                    application=name,
                    message="automated prune is enabled in the head state",
                )
            )

    for name in sorted(set(head_map) - set(base_map)):
        application = head_map[name]
        if application.production_target:
            findings.append(
                BlastRadiusFinding(
                    id=f"new-production-application:{name}",
                    kind="new_production_application",
                    severity="high",
                    application=name,
                    message="new application is introduced directly into a production destination",
                )
            )

    return CompareReport(
        base_applicationset=base.applicationset,
        head_applicationset=head.applicationset,
        added_applications=[head_map[name] for name in sorted(set(head_map) - set(base_map))],
        removed_applications=[base_map[name] for name in sorted(set(base_map) - set(head_map))],
        changed_applications=changed_applications,
        findings=sorted(findings, key=lambda item: item.id),
    )
