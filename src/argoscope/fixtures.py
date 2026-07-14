from __future__ import annotations

import json
from pathlib import Path

from pydantic import ValidationError

from argoscope.exceptions import ArgoScopeError
from argoscope.models import ApplicationFixture


def load_rendered_fixture(applicationset_path: Path) -> ApplicationFixture:
    fixture_path = applicationset_path.with_suffix(".rendered.json")
    try:
        return ApplicationFixture.model_validate(json.loads(fixture_path.read_text()))
    except FileNotFoundError as error:
        raise ArgoScopeError(f"rendered fixture not found: {fixture_path}") from error
    except ValidationError as error:
        raise ArgoScopeError(f"invalid rendered fixture: {fixture_path}: {error}") from error
