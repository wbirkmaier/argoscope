from __future__ import annotations

from pathlib import Path
from typing import Annotated

import typer

from argoscope.analysis import build_preview_report
from argoscope.exceptions import ArgoScopeError
from argoscope.fixtures import load_rendered_fixture

app = typer.Typer(
    help="Estimate Argo CD ApplicationSet change radius without touching clusters.",
    no_args_is_help=True,
    pretty_exceptions_enable=False,
)


@app.callback()
def callback() -> None:
    """ArgoScope command group."""


@app.command("version")
def version() -> None:
    typer.echo("argoscope 0.1.0")


@app.command("preview")
def preview(
    applicationset: Annotated[Path, typer.Argument(exists=True, readable=True, dir_okay=False)],
) -> None:
    try:
        report = build_preview_report(load_rendered_fixture(applicationset))
    except ArgoScopeError as error:
        raise typer.Exit(code=error.exit_code) from error

    typer.echo(report.model_dump_json(indent=2))


def main(argv: Annotated[list[str] | None, typer.Argument(hidden=True)] = None) -> None:
    app(args=argv)
