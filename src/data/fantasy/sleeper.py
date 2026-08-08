"""
Sleeper API client — read-only, no API key required.

Docs: https://docs.sleeper.com/
All methods return parsed Pydantic models or raw dicts for unmapped endpoints.
"""

from typing import Any

import httpx
from pydantic import BaseModel

SLEEPER_BASE = "https://api.sleeper.app/v1"
_DEFAULT_TIMEOUT = 10.0


class SleeperUser(BaseModel):
    user_id: str
    username: str
    display_name: str
    avatar: str | None = None


class SleeperLeague(BaseModel):
    league_id: str
    name: str
    season: str
    season_type: str
    sport: str
    total_rosters: int
    scoring_settings: dict[str, Any] = {}
    roster_positions: list[str] = []
    status: str


class SleeperRoster(BaseModel):
    roster_id: int
    owner_id: str | None
    league_id: str
    players: list[str] = []
    starters: list[str] = []
    reserve: list[str] = []


class SleeperMatchup(BaseModel):
    matchup_id: int
    roster_id: int
    points: float | None = None
    starters: list[str] = []
    players: list[str] = []


class SleeperClient:
    """
    Thin async HTTP client wrapping the Sleeper read-only API.

    Usage:
        async with SleeperClient() as client:
            user = await client.get_user("justinubele")
    """

    def __init__(self, timeout: float = _DEFAULT_TIMEOUT) -> None:
        self._http = httpx.AsyncClient(
            base_url=SLEEPER_BASE,
            timeout=timeout,
            headers={"User-Agent": "fantasy-football-ai/0.1"},
        )

    async def __aenter__(self) -> "SleeperClient":
        return self

    async def __aexit__(self, *_: Any) -> None:
        await self._http.aclose()

    async def _get(self, path: str, **params: Any) -> Any:
        response = await self._http.get(path, params=params or None)
        response.raise_for_status()
        return response.json()

    # ------------------------------------------------------------------ Users

    async def get_user(self, username_or_id: str) -> SleeperUser:
        """Fetch a Sleeper user by username or user_id."""
        data = await self._get(f"/user/{username_or_id}")
        return SleeperUser(**data)

    # ----------------------------------------------------------------- Leagues

    async def get_leagues_for_user(
        self, user_id: str, sport: str = "nfl", season: str = "2024"
    ) -> list[SleeperLeague]:
        """Return all leagues a user is in for a given sport and season."""
        data = await self._get(f"/user/{user_id}/leagues/{sport}/{season}")
        return [SleeperLeague(**league) for league in (data or [])]

    async def get_league(self, league_id: str) -> SleeperLeague:
        data = await self._get(f"/league/{league_id}")
        return SleeperLeague(**data)

    # ----------------------------------------------------------------- Rosters

    async def get_rosters(self, league_id: str) -> list[SleeperRoster]:
        data = await self._get(f"/league/{league_id}/rosters")
        return [SleeperRoster(**r) for r in (data or [])]

    # --------------------------------------------------------------- Matchups

    async def get_matchups(self, league_id: str, week: int) -> list[SleeperMatchup]:
        data = await self._get(f"/league/{league_id}/matchups/{week}")
        return [SleeperMatchup(**m) for m in (data or [])]

    # ----------------------------------------------------------------- Players

    async def get_all_players(self, sport: str = "nfl") -> dict[str, Any]:
        """
        Fetch Sleeper's full player database (~5 MB JSON).
        Cache this locally — Sleeper asks you to call it at most once per day.
        Returns raw dict keyed by sleeper player_id.
        """
        return await self._get(f"/players/{sport}")

    async def get_trending_players(
        self,
        sport: str = "nfl",
        trend_type: str = "add",
        lookback_hours: int = 24,
        limit: int = 25,
    ) -> list[dict[str, Any]]:
        """Trending adds or drops across all Sleeper leagues."""
        return await self._get(
            f"/players/{sport}/trending/{trend_type}",
            lookback_hours=lookback_hours,
            limit=limit,
        )

    # -------------------------------------------------------------- Waiver / Transactions

    async def get_transactions(
        self, league_id: str, round_or_week: int
    ) -> list[dict[str, Any]]:
        """All transactions (waivers, trades, free-agent adds) for a week."""
        return await self._get(f"/league/{league_id}/transactions/{round_or_week}")
