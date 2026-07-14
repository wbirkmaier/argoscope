from __future__ import annotations

from pathlib import Path
from typing import Annotated

import typer

from argoscope.analysis import build_preview_report
from argoscope.diffing import compare_preview_reports
from argoscope.exceptions import ArgoScopeError
from argoscope.fixtures import load_rendered_fixture
from argoscope.snapshot_io import load_preview_report

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


@app.command("compare")
def compare(
    base: Annotated[Path, typer.Argument(exists=True, readable=True, dir_okay=False)],
    head: Annotated[Path, typer.Argument(exists=True, readable=True, dir_okay=False)],
) -> None:
    try:
        report = compare_preview_reports(load_preview_report(base), load_preview_report(head))
    except ArgoScopeError as error:
        raise typer.Exit(code=error.exit_code) from error

    typer.echo(report.model_dump_json(indent=2))


def main(argv: Annotated[list[str] | None, typer.Argument(hidden=True)] = None) -> None:
    app(args=argv)
