from __future__ import annotations

from pathlib import Path

from pydantic import ValidationError

from argoscope.exceptions import ArgoScopeError
from argoscope.models import PreviewReport


def load_preview_report(path: Path) -> PreviewReport:
    try:
        return PreviewReport.model_validate_json(path.read_text())
    except FileNotFoundError as error:
        raise ArgoScopeError(f"preview snapshot not found: {path}") from error
    except ValidationError as error:
        raise ArgoScopeError(f"invalid preview snapshot: {path}: {error}") from error
