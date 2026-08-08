"""
Tests for the Sleeper API client.
Uses httpx mock to avoid real network calls.
"""

import pytest
import httpx

from src.data.fantasy.sleeper import SleeperClient, SleeperUser, SleeperLeague


MOCK_USER = {
    "user_id": "123456789",
    "username": "testuser",
    "display_name": "Test User",
    "avatar": None,
}

MOCK_LEAGUES = [
    {
        "league_id": "abc123",
        "name": "The Best League",
        "season": "2024",
        "season_type": "regular",
        "sport": "nfl",
        "total_rosters": 12,
        "scoring_settings": {"rec": 1.0},
        "roster_positions": ["QB", "RB", "RB", "WR", "WR", "TE", "FLEX", "BN"],
        "status": "in_season",
    }
]


@pytest.mark.asyncio
async def test_get_user_parses_response(respx_mock):
    respx_mock.get("https://api.sleeper.app/v1/user/testuser").mock(
        return_value=httpx.Response(200, json=MOCK_USER)
    )

    async with SleeperClient() as client:
        user = await client.get_user("testuser")

    assert isinstance(user, SleeperUser)
    assert user.user_id == "123456789"
    assert user.display_name == "Test User"


@pytest.mark.asyncio
async def test_get_leagues_for_user(respx_mock):
    respx_mock.get(
        "https://api.sleeper.app/v1/user/123456789/leagues/nfl/2024"
    ).mock(return_value=httpx.Response(200, json=MOCK_LEAGUES))

    async with SleeperClient() as client:
        leagues = await client.get_leagues_for_user("123456789")

    assert len(leagues) == 1
    league = leagues[0]
    assert isinstance(league, SleeperLeague)
    assert league.name == "The Best League"
    assert league.total_rosters == 12


@pytest.mark.asyncio
async def test_http_error_raises(respx_mock):
    respx_mock.get("https://api.sleeper.app/v1/user/unknown").mock(
        return_value=httpx.Response(404)
    )

    with pytest.raises(httpx.HTTPStatusError):
        async with SleeperClient() as client:
            await client.get_user("unknown")
