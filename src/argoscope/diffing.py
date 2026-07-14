from __future__ import annotations

from argoscope.models import ApplicationChange, CompareReport, PreviewReport


def compare_preview_reports(base: PreviewReport, head: PreviewReport) -> CompareReport:
    base_map = {application.name: application for application in base.generated_applications}
    head_map = {application.name: application for application in head.generated_applications}

    changed_applications: list[ApplicationChange] = []
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

    return CompareReport(
        base_applicationset=base.applicationset,
        head_applicationset=head.applicationset,
        added_applications=[head_map[name] for name in sorted(set(head_map) - set(base_map))],
        removed_applications=[base_map[name] for name in sorted(set(base_map) - set(head_map))],
        changed_applications=changed_applications,
    )
