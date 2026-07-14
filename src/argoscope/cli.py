from __future__ import annotations

from typing import Annotated

import typer

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


def main(argv: Annotated[list[str] | None, typer.Argument(hidden=True)] = None) -> None:
    app(args=argv)
