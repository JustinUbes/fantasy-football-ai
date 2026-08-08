# Copilot Instructions for This Repository

## Repository State

This repository is in **active development** — Phase 1 (data foundation) is underway.

## Stack (decided)

| Layer | Choice |
|---|---|
| Language | Python 3.11+ |
| Package manager | `uv` (preferred) or `pip -e ".[dev]"` |
| AI | OpenAI API (`gpt-4o-mini` default, `gpt-4o` premium) |
| NFL data | `nfl-data-py` (nflverse) |
| Fantasy platform (Phase 1) | Sleeper read-only API |
| Local DB | SQLite via SQLAlchemy async + aiosqlite |
| Production DB | Azure Database for PostgreSQL (Flexible Server) |
| Cloud | Microsoft Azure |
| Frontend | React.js (React Native path for future mobile) |

## Project Layout

```
src/
  ai/          - OpenAI client wrapper and prompt templates
  cli/         - `ffa` CLI (typer + rich)
  data/
    nfl/       - nfl-data-py integration (weekly stats, rosters, schedule)
    fantasy/   - Fantasy platform clients (Sleeper, ESPN Phase 2, Yahoo Phase 2)
  storage/     - SQLAlchemy models and async session factory
tests/         - pytest tests (asyncio_mode = auto)
specs/         - Product brief, implementation plan, open questions
docs/          - Data sources, API references, decisions report
```

## Working Rules

1. Do not add features or refactor code beyond what is directly requested.
2. Keep the data layer, AI layer, and CLI as separate concerns — do not mix them.
3. All database operations use async SQLAlchemy (`AsyncSession`). Never use sync sessions.
4. Always load `.env` via `python-dotenv` — never hardcode API keys.
5. New fantasy platform integrations go in `src/data/fantasy/`.
6. New analysis modules (draft, lineup, etc.) go in `src/analysis/` (Phase 2).
7. Record assumptions in `specs/open-questions.md` rather than silently in code.
8. When adding a new CLI command, register it in `src/cli/main.py` using the `app` typer instance.

## Running the Project

```bash
# Install (uv preferred)
uv sync

# Or with pip
pip install -e ".[dev]"

# Setup
cp .env.example .env        # fill in OPENAI_API_KEY
uv run ffa db-init          # create local SQLite DB
uv run ffa fetch-stats 2022 2023 2024   # download NFL stats
uv run ffa --help           # see all commands

# Tests
uv run pytest
```

## Open Decisions (need user input)

- Frontend: React.js (decided)
- Azure hosting shape: Container Apps (recommended) vs App Service vs Functions
- Auth: Clerk vs Azure Entra External ID
- Analyst data source: manual seed → FantasyPros partner API (Phase 2)
- Historical data depth: currently targeting 2022–2024

See `docs/decisions-report.md` and `specs/open-questions.md` for full details.

## Copilot Collaboration

- Summarize tradeoffs before making irreversible decisions.
- Prefer placeholders and interfaces over speculative implementations.
- If a request implies a new stack choice (e.g. adding a web framework), call it out explicitly.
- Cost matters — this is a solo developer project. Prefer free/cheap solutions at this stage.