"""
NFL data pipeline using nfl-data-py (backed by nflverse).

nfl-data-py docs: https://pypi.org/project/nfl-data-py/
nflverse data:    https://github.com/nflverse/nflverse-data

Data usage pattern: week-by-week.
- Completed weeks are fetched once and cached locally (never re-downloaded).
- The current in-progress week is fetched on demand at query time.
"""

import logging
from typing import Any

import nfl_data_py as nfl
import pandas as pd

logger = logging.getLogger(__name__)

# Columns we care about from nfl-data-py weekly stats
WEEKLY_STAT_COLS = [
    "player_id",        # gsis_id
    "player_name",
    "player_display_name",
    "position",
    "recent_team",
    "season",
    "week",
    "season_type",
    "completions",
    "attempts",
    "passing_yards",
    "passing_tds",
    "interceptions",
    "carries",
    "rushing_yards",
    "rushing_tds",
    "receptions",
    "targets",
    "receiving_yards",
    "receiving_tds",
    "fantasy_points",
    "fantasy_points_ppr",
]


def fetch_weekly_stats(seasons: list[int]) -> pd.DataFrame:
    """
    Download weekly player stats for the given seasons from nflverse.

    Completed weeks are stable — cache them locally and avoid re-fetching.
    The current in-progress week should be fetched fresh on each query.

    Args:
        seasons: List of NFL seasons (e.g. [2022, 2023, 2024]).

    Returns:
        DataFrame with columns normalised to WEEKLY_STAT_COLS (missing cols filled with NaN).
    """
    logger.info("Fetching nfl-data-py weekly stats for seasons: %s", seasons)
    df = nfl.import_weekly_data(seasons)

    available = [c for c in WEEKLY_STAT_COLS if c in df.columns]
    missing = [c for c in WEEKLY_STAT_COLS if c not in df.columns]
    if missing:
        logger.warning("Columns not available in nfl-data-py output: %s", missing)

    df = df[available].copy()
    df = df[df["position"].isin(["QB", "RB", "WR", "TE", "K"])]
    df = df.reset_index(drop=True)
    logger.info("Fetched %d weekly stat rows", len(df))
    return df


def fetch_rosters(seasons: list[int]) -> pd.DataFrame:
    """Download weekly roster snapshots (includes depth chart, injury status)."""
    logger.info("Fetching rosters for seasons: %s", seasons)
    df = nfl.import_seasonal_rosters(seasons)
    logger.info("Fetched %d roster rows", len(df))
    return df


def fetch_schedule(seasons: list[int]) -> pd.DataFrame:
    """Download game schedule with home/away, spread, over/under."""
    logger.info("Fetching schedule for seasons: %s", seasons)
    df = nfl.import_schedules(seasons)
    logger.info("Fetched %d schedule rows", len(df))
    return df


def fetch_snap_counts(seasons: list[int]) -> pd.DataFrame:
    """Download offensive and defensive snap count data."""
    logger.info("Fetching snap counts for seasons: %s", seasons)
    df = nfl.import_snap_counts(seasons)
    logger.info("Fetched %d snap count rows", len(df))
    return df


def fetch_ngs_data(stat_type: str, seasons: list[int]) -> pd.DataFrame:
    """
    Download Next Gen Stats data.

    Args:
        stat_type: One of 'passing', 'rushing', 'receiving'.
        seasons:   List of NFL seasons.
    """
    logger.info("Fetching NGS %s stats for seasons: %s", stat_type, seasons)
    df = nfl.import_ngs_data(stat_type, seasons)
    logger.info("Fetched %d NGS rows", len(df))
    return df


def weekly_stats_to_records(df: pd.DataFrame) -> list[dict[str, Any]]:
    """Convert a weekly stats DataFrame to a list of dicts ready for ORM insertion."""
    df = df.rename(
        columns={
            "player_id": "gsis_id",
            "fantasy_points": "fantasy_points_std",
        }
    )
    return df.where(pd.notna(df), None).to_dict(orient="records")


def fetch_single_week(season: int, week: int) -> pd.DataFrame:
    """
    Fetch stats for a single NFL week — used for on-demand current-week queries.

    Completed weeks should be read from the local cache instead of calling this.
    Call this for the live/current week only.

    Args:
        season: NFL season year (e.g. 2024).
        week:   NFL week number (1–18 regular season, 19–22 postseason).
    """
    logger.info("Fetching single-week stats: season=%s week=%s", season, week)
    df = nfl.import_weekly_data([season])
    df = df[df["week"] == week]
    available = [c for c in WEEKLY_STAT_COLS if c in df.columns]
    df = df[available].copy()
    df = df[df["position"].isin(["QB", "RB", "WR", "TE", "K"])]
    logger.info("Fetched %d rows for week %s", len(df), week)
    return df.reset_index(drop=True)
