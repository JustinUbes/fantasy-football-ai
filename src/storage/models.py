"""
SQLAlchemy ORM models for the local database.

All tables are designed to be portable to Azure PostgreSQL without schema changes.
"""

from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.storage import Base


class Player(Base):
    """Canonical NFL player record, keyed by nfl-data-py gsis_id."""

    __tablename__ = "players"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    gsis_id: Mapped[str] = mapped_column(String(36), unique=True, index=True)
    full_name: Mapped[str] = mapped_column(String(100))
    position: Mapped[str] = mapped_column(String(10))   # QB, RB, WR, TE, K, DEF
    team: Mapped[str] = mapped_column(String(5))
    status: Mapped[str | None] = mapped_column(String(20), nullable=True)  # Active, IR, etc.
    sleeper_id: Mapped[str | None] = mapped_column(String(20), nullable=True, index=True)

    stats: Mapped[list["WeeklyStats"]] = relationship(back_populates="player")


class WeeklyStats(Base):
    """Player fantasy-relevant stats for a given NFL week."""

    __tablename__ = "weekly_stats"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    player_id: Mapped[int] = mapped_column(ForeignKey("players.id"), index=True)
    season: Mapped[int] = mapped_column(Integer)
    week: Mapped[int] = mapped_column(Integer)
    season_type: Mapped[str] = mapped_column(String(10), default="REG")  # REG, POST

    # Core fantasy scoring stats
    passing_yards: Mapped[float | None] = mapped_column(Float, nullable=True)
    passing_tds: Mapped[float | None] = mapped_column(Float, nullable=True)
    interceptions: Mapped[float | None] = mapped_column(Float, nullable=True)
    rushing_yards: Mapped[float | None] = mapped_column(Float, nullable=True)
    rushing_tds: Mapped[float | None] = mapped_column(Float, nullable=True)
    receiving_yards: Mapped[float | None] = mapped_column(Float, nullable=True)
    receiving_tds: Mapped[float | None] = mapped_column(Float, nullable=True)
    receptions: Mapped[float | None] = mapped_column(Float, nullable=True)
    targets: Mapped[float | None] = mapped_column(Float, nullable=True)
    fantasy_points_ppr: Mapped[float | None] = mapped_column(Float, nullable=True)
    fantasy_points_std: Mapped[float | None] = mapped_column(Float, nullable=True)

    player: Mapped["Player"] = relationship(back_populates="stats")


class Analyst(Base):
    """A sports/fantasy analyst whose predictions are tracked."""

    __tablename__ = "analysts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True)
    outlet: Mapped[str | None] = mapped_column(String(100), nullable=True)
    twitter_handle: Mapped[str | None] = mapped_column(String(50), nullable=True)
    accuracy_score: Mapped[float | None] = mapped_column(Float, nullable=True)
    predictions_tracked: Mapped[int] = mapped_column(Integer, default=0)

    predictions: Mapped[list["AnalystPrediction"]] = relationship(back_populates="analyst")


class AnalystPrediction(Base):
    """A single prediction made by an analyst for a player/week."""

    __tablename__ = "analyst_predictions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    analyst_id: Mapped[int] = mapped_column(ForeignKey("analysts.id"), index=True)
    player_id: Mapped[int] = mapped_column(ForeignKey("players.id"), index=True)
    season: Mapped[int] = mapped_column(Integer)
    week: Mapped[int] = mapped_column(Integer)
    predicted_points: Mapped[float | None] = mapped_column(Float, nullable=True)
    predicted_rank: Mapped[int | None] = mapped_column(Integer, nullable=True)
    actual_points: Mapped[float | None] = mapped_column(Float, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    analyst: Mapped["Analyst"] = relationship(back_populates="predictions")


class UserLeague(Base):
    """A user-linked fantasy league (Sleeper, Yahoo, etc.)."""

    __tablename__ = "user_leagues"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[str] = mapped_column(String(100), index=True)  # auth provider sub
    platform: Mapped[str] = mapped_column(String(20))              # sleeper, yahoo, espn
    platform_league_id: Mapped[str] = mapped_column(String(100))
    platform_user_id: Mapped[str] = mapped_column(String(100))
    league_name: Mapped[str | None] = mapped_column(String(200), nullable=True)
    scoring_format: Mapped[str | None] = mapped_column(String(20), nullable=True)  # ppr, half_ppr, std
    season: Mapped[int] = mapped_column(Integer)
    raw_settings: Mapped[str | None] = mapped_column(Text, nullable=True)  # JSON blob
