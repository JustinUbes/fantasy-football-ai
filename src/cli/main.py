"""
CLI entry point — `ffa` command.

Run with:
    uv run ffa --help
    # or
    python -m src.cli.main --help
"""

import asyncio
import logging
from typing import Any

import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from src.ai.client import AdviceType, FFAIClient
from src.storage import init_db

app = typer.Typer(
    name="ffa",
    help="Fantasy Football AI — your personal analyst.",
    add_completion=False,
)
console = Console()


def _run(coro: Any) -> Any:
    return asyncio.run(coro)


# --------------------------------------------------------------------------
# db
# --------------------------------------------------------------------------


@app.command()
def db_init() -> None:
    """Initialise the local SQLite database (create tables)."""
    _run(init_db())
    console.print("[green]Database initialised.[/green]")


# --------------------------------------------------------------------------
# data
# --------------------------------------------------------------------------


@app.command()
def fetch_stats(
    seasons: list[int] = typer.Argument(..., help="NFL seasons, e.g. 2022 2023 2024"),
) -> None:
    """Download NFL weekly stats from nflverse and print a summary."""
    from src.data.nfl.stats import fetch_weekly_stats

    console.print(f"Fetching stats for seasons: {seasons} …")
    df = fetch_weekly_stats(seasons)
    console.print(f"[green]Fetched {len(df):,} rows.[/green]")
    console.print(df.head(10).to_string())


@app.command()
def sleeper_user(username: str = typer.Argument(..., help="Sleeper username")) -> None:
    """Look up a Sleeper user and list their leagues."""

    async def _main() -> None:
        from src.data.fantasy.sleeper import SleeperClient

        async with SleeperClient() as client:
            user = await client.get_user(username)
            leagues = await client.get_leagues_for_user(user.user_id)

        console.print(Panel(f"[bold]{user.display_name}[/bold]  (ID: {user.user_id})"))

        table = Table("League", "Season", "Teams", "Format")
        for lg in leagues:
            fmt = lg.scoring_settings.get("rec", 0)
            fmt_label = "PPR" if fmt == 1.0 else ("Half PPR" if fmt == 0.5 else "Standard")
            table.add_row(lg.name, lg.season, str(lg.total_rosters), fmt_label)
        console.print(table)

    _run(_main())


# --------------------------------------------------------------------------
# AI advice
# --------------------------------------------------------------------------


@app.command()
def lineup(
    context: str = typer.Option(..., "--context", "-c", help="Paste your roster and week info"),
) -> None:
    """Get AI lineup advice for the current week."""

    async def _main() -> None:
        client = FFAIClient()
        console.print("[yellow]Thinking…[/yellow]")
        answer = await client.ask(AdviceType.LINEUP, context)
        console.print(Panel(answer, title="Lineup Advice", border_style="green"))

    _run(_main())


@app.command()
def waivers(
    context: str = typer.Option(..., "--context", "-c", help="Your roster and available players"),
) -> None:
    """Get AI waiver wire recommendations."""

    async def _main() -> None:
        client = FFAIClient()
        console.print("[yellow]Thinking…[/yellow]")
        answer = await client.ask(AdviceType.WAIVER, context)
        console.print(Panel(answer, title="Waiver Wire Advice", border_style="cyan"))

    _run(_main())


@app.command()
def draft(
    context: str = typer.Option(..., "--context", "-c", help="League settings and available players"),
) -> None:
    """Get AI draft pick recommendations."""

    async def _main() -> None:
        client = FFAIClient()
        console.print("[yellow]Thinking…[/yellow]")
        answer = await client.ask(AdviceType.DRAFT, context)
        console.print(Panel(answer, title="Draft Advice", border_style="magenta"))

    _run(_main())


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    app()
