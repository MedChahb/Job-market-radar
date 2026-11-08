"""Command-line entry point: `radar <command>`."""

import typer

from radar import __version__
from radar.doctor import check_database, check_ollama
from radar.settings import get_settings

app = typer.Typer(
    help="Job Market Radar: collect, classify, extract and publish job offers.",
    no_args_is_help=True,
)


@app.command()
def version() -> None:
    """Print the installed version."""
    typer.echo(__version__)


@app.command()
def doctor() -> None:
    """Check that the database and Ollama are reachable."""
    settings = get_settings()
    checks = [check_database(settings.database_url), check_ollama(settings.ollama_url)]
    for check in checks:
        mark = "ok  " if check.ok else "FAIL"
        typer.echo(f"[{mark}] {check.name}: {check.detail}")
    if not all(check.ok for check in checks):
        raise typer.Exit(code=1)
