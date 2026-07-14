from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from argoscope.exceptions import ArgoScopeError
from argoscope.fixtures import load_rendered_fixture
from argoscope.models import ApplicationFixture


class RendererAdapter:
    def render(self, applicationset_path: Path) -> ApplicationFixture:
        raise NotImplementedError


@dataclass(frozen=True)
class FixtureRendererAdapter(RendererAdapter):
    def render(self, applicationset_path: Path) -> ApplicationFixture:
        return load_rendered_fixture(applicationset_path)


@dataclass(frozen=True)
class ArgocdCliRendererAdapter(RendererAdapter):
    binary: str = "argocd"

    def render(self, applicationset_path: Path) -> ApplicationFixture:
        raise ArgoScopeError(
            f"live Argo CD rendering is not implemented for {applicationset_path}; "
            f"configure fixture-backed rendering or add an adapter for `{self.binary}`"
        )


def get_renderer_adapter(mode: str) -> RendererAdapter:
    if mode == "fixture":
        return FixtureRendererAdapter()
    if mode == "argocd":
        return ArgocdCliRendererAdapter()
    raise ArgoScopeError(f"unsupported renderer mode: {mode}")
