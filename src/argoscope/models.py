from __future__ import annotations

from pydantic import BaseModel, Field


class RenderedSource(BaseModel):
    repo_url: str
    target_revision: str
    path: str


class RenderedDestination(BaseModel):
    server: str
    namespace: str


class RenderedSyncPolicyAutomated(BaseModel):
    prune: bool = False
    self_heal: bool = False


class RenderedSyncPolicy(BaseModel):
    automated: RenderedSyncPolicyAutomated | None = None


class RenderedApplication(BaseModel):
    name: str
    project: str
    source: RenderedSource
    destination: RenderedDestination
    sync_policy: RenderedSyncPolicy | None = None
    labels: dict[str, str] = Field(default_factory=dict)


class ApplicationFixture(BaseModel):
    applicationset: str
    applications: list[RenderedApplication]


class GeneratedApplication(BaseModel):
    name: str
    project: str
    cluster: str
    namespace: str
    repo_url: str
    target_revision: str
    path: str
    automated_prune: bool
    self_heal: bool
    production_target: bool


class PreviewReport(BaseModel):
    applicationset: str
    generated_applications: list[GeneratedApplication]
    clusters: list[str]
    namespaces: list[str]
