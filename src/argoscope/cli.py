from __future__ import annotations

from pathlib import Path
from typing import Annotated

import typer

from argoscope.adapters import get_renderer_adapter
from argoscope.analysis import build_preview_report
from argoscope.diffing import compare_preview_reports
from argoscope.exceptions import ArgoScopeError
from argoscope.policy import evaluate_policy, load_policy
from argoscope.rendering import load_render_input, render_markdown
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
    renderer: Annotated[
        str,
        typer.Option("--renderer", help="Render source: 'fixture' or 'argocd'."),
    ] = "fixture",
) -> None:
    try:
        report = build_preview_report(get_renderer_adapter(renderer).render(applicationset))
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


@app.command("check")
def check(
    applicationset: Annotated[Path, typer.Argument(exists=True, readable=True, dir_okay=False)],
    policy: Annotated[
        Path,
        typer.Option("--policy", exists=True, readable=True, dir_okay=False),
    ],
) -> None:
    try:
        preview_report = build_preview_report(
            get_renderer_adapter("fixture").render(applicationset)
        )
        policy_report = evaluate_policy(load_policy(policy), preview_report)
    except ArgoScopeError as error:
        raise typer.Exit(code=error.exit_code) from error

    typer.echo(policy_report.model_dump_json(indent=2))


@app.command("render")
def render(
    report: Annotated[Path, typer.Argument(exists=True, readable=True, dir_okay=False)],
    output_format: Annotated[
        str, typer.Option("--format", help="Only 'markdown' is currently supported.")
    ] = "markdown",
) -> None:
    if output_format != "markdown":
        raise typer.Exit(code=2)

    try:
        typer.echo(render_markdown(load_render_input(report)))
    except ArgoScopeError as error:
        raise typer.Exit(code=error.exit_code) from error


def main(argv: Annotated[list[str] | None, typer.Argument(hidden=True)] = None) -> None:
    app(args=argv)
