"""
OpenAI client wrapper with prompt templates for fantasy football advice.

Centralises model selection, token estimation, and structured output parsing.
"""

import os
from enum import StrEnum
from typing import Any

from dotenv import load_dotenv
from openai import AsyncOpenAI
from pydantic import BaseModel

load_dotenv()

_DEFAULT_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")


class AdviceType(StrEnum):
    DRAFT = "draft"
    LINEUP = "lineup"
    WAIVER = "waiver"
    MATCHUP = "matchup"
    WEEKLY_REPORT = "weekly_report"


# ---------------------------------------------------------------------------
# System prompts
# ---------------------------------------------------------------------------

_SYSTEM_BASE = (
    "You are an expert fantasy football analyst with deep knowledge of NFL statistics, "
    "player trends, injury impacts, and fantasy scoring formats. "
    "Provide concise, actionable advice backed by specific stats and reasoning. "
    "Always acknowledge uncertainty where data is limited."
)

_SYSTEM_PROMPTS: dict[AdviceType, str] = {
    AdviceType.DRAFT: (
        f"{_SYSTEM_BASE} "
        "You are helping a user make draft picks. Consider ADP, positional scarcity, "
        "team offensive context, and the user's roster construction needs."
    ),
    AdviceType.LINEUP: (
        f"{_SYSTEM_BASE} "
        "You are setting a weekly lineup. Consider matchups, injury reports, "
        "weather, and recent usage trends."
    ),
    AdviceType.WAIVER: (
        f"{_SYSTEM_BASE} "
        "You are advising on waiver wire pickups. Consider opportunity share, "
        "target share, upcoming schedule, and roster needs."
    ),
    AdviceType.MATCHUP: (
        f"{_SYSTEM_BASE} "
        "You are providing matchup preview analysis for an upcoming fantasy week. "
        "Focus on start/sit decisions, sleepers, and bust risks."
    ),
    AdviceType.WEEKLY_REPORT: (
        f"{_SYSTEM_BASE} "
        "You are writing a post-week report. Summarise what happened, grade the "
        "lineup decisions, and set priorities for the next week."
    ),
}

# ---------------------------------------------------------------------------
# Response models
# ---------------------------------------------------------------------------


class PlayerRecommendation(BaseModel):
    player_name: str
    action: str          # e.g. "START", "SIT", "ADD", "DROP", "DRAFT"
    confidence: str      # "HIGH", "MEDIUM", "LOW"
    rationale: str
    caveats: str | None = None


class AdviceResponse(BaseModel):
    summary: str
    recommendations: list[PlayerRecommendation]
    raw_text: str


# ---------------------------------------------------------------------------
# Client
# ---------------------------------------------------------------------------


class FFAIClient:
    """
    Async wrapper around the OpenAI API for fantasy football advice.

    Usage:
        client = FFAIClient()
        response = await client.ask(AdviceType.LINEUP, context="...")
    """

    def __init__(self, model: str = _DEFAULT_MODEL) -> None:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise EnvironmentError("OPENAI_API_KEY is not set in environment or .env")
        self._client = AsyncOpenAI(api_key=api_key)
        self.model = model

    async def ask(
        self,
        advice_type: AdviceType,
        context: str,
        extra_instructions: str | None = None,
    ) -> str:
        """
        Send a prompt to OpenAI and return the raw text response.

        Args:
            advice_type:        Category of advice (drives system prompt selection).
            context:            User-specific context (roster, settings, stats).
            extra_instructions: Optional additional instructions appended to system prompt.
        """
        system = _SYSTEM_PROMPTS[advice_type]
        if extra_instructions:
            system = f"{system}\n\n{extra_instructions}"

        response = await self._client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": context},
            ],
            temperature=0.3,   # lower = more deterministic, better for structured advice
        )
        return response.choices[0].message.content or ""

    async def ask_structured(
        self,
        advice_type: AdviceType,
        context: str,
        response_model: type[BaseModel] = AdviceResponse,
    ) -> Any:
        """
        Request JSON-structured output parsed into a Pydantic model.
        Uses OpenAI's structured outputs (response_format).
        """
        system = _SYSTEM_PROMPTS[advice_type]
        system += (
            "\n\nRespond ONLY with a valid JSON object matching this schema:\n"
            f"{response_model.model_json_schema()}"
        )

        response = await self._client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": context},
            ],
            response_format={"type": "json_object"},
            temperature=0.2,
        )
        raw = response.choices[0].message.content or "{}"
        return response_model.model_validate_json(raw)

    def estimate_tokens(self, text: str) -> int:
        """Rough token estimate: ~4 chars per token for English text."""
        return len(text) // 4
