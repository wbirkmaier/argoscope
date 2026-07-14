from __future__ import annotations

from argoscope.models import ApplicationFixture, GeneratedApplication, PreviewReport


def _is_production_destination(cluster: str, namespace: str) -> bool:
    return "prod" in cluster.lower() or namespace.lower() in {"prod", "production"}


def build_preview_report(fixture: ApplicationFixture) -> PreviewReport:
    generated_applications: list[GeneratedApplication] = []
    for application in sorted(
        fixture.applications,
        key=lambda item: (item.destination.server, item.destination.namespace, item.name),
    ):
        automated = application.sync_policy.automated if application.sync_policy else None
        generated_applications.append(
            GeneratedApplication(
                name=application.name,
                project=application.project,
                cluster=application.destination.server,
                namespace=application.destination.namespace,
                repo_url=application.source.repo_url,
                target_revision=application.source.target_revision,
                path=application.source.path,
                automated_prune=automated.prune if automated else False,
                self_heal=automated.self_heal if automated else False,
                production_target=_is_production_destination(
                    application.destination.server,
                    application.destination.namespace,
                ),
            )
        )

    return PreviewReport(
        applicationset=fixture.applicationset,
        generated_applications=generated_applications,
        clusters=sorted({application.cluster for application in generated_applications}),
        namespaces=sorted({application.namespace for application in generated_applications}),
    )
