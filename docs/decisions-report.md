# Fantasy Football AI — Decisions Report

**Date:** 2026-08-08  
**Author:** GitHub Copilot (Claude Sonnet 4.6)  
**Status:** Awaiting your input on the open items below.

---

## What Was Done

The project has been bootstrapped with a working Python foundation:

| File | Purpose |
|---|---|
| `pyproject.toml` | Python project config, dependencies, `ffa` CLI script |
| `.env.example` | Environment variable template |
| `src/storage/__init__.py` | Async SQLAlchemy engine (SQLite → PostgreSQL portable) |
| `src/storage/models.py` | ORM models: Player, WeeklyStats, Analyst, AnalystPrediction, UserLeague |
| `src/data/nfl/stats.py` | `nfl-data-py` integration — weekly stats, rosters, schedule, snap counts, NGS |
| `src/data/fantasy/sleeper.py` | Full Sleeper API async client with Pydantic models |
| `src/ai/client.py` | OpenAI async wrapper with per-advice-type system prompts + structured output |
| `src/cli/main.py` | `ffa` CLI: `db-init`, `fetch-stats`, `sleeper-user`, `lineup`, `waivers`, `draft` |
| `tests/test_sleeper_client.py` | Unit tests for Sleeper client (mocked network) |
| `specs/implementation-plan.md` | Phased roadmap (Phase 1–4) |
| `specs/open-questions.md` | Resolved decisions + remaining open questions |

---

## Decisions You Need to Make

### 1. Frontend: React.js vs Next.js

**My recommendation: Next.js**

| | React.js | Next.js |
|---|---|---|
| Server-side rendering | No | Yes (better for SEO and first load) |
| API routes | No (need separate server) | Yes (cuts Azure infra by 1 service) |
| Mobile path (React Native) | Easy (shared components) | Possible (shared logic, not routing) |
| Azure deployment | Azure Static Web Apps | Azure Static Web Apps + Functions |
| Complexity | Lower | Slightly higher |

The "easy React Native translation" is a common misconception — you can share business logic and UI component *code*, but routing, navigation, and native APIs are entirely different. Build Next.js web first; extract a React Native app when you have users who specifically want mobile.

---

### 2. Python Package Manager: `uv` vs `poetry` vs `pip`

**My recommendation: `uv`**

`uv` is 10–100x faster than pip/poetry, uses the standard `pyproject.toml`, and is now maintained by Astral (same team as Ruff). It's what I've wired the project for.

To install and set up:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
cd fantasy-football-ai
uv sync        # installs all dependencies from pyproject.toml
uv run ffa --help
```

If you prefer `pip`:
```bash
pip install -e ".[dev]"
```

---

### 3. Analyst Ranking Data Source

**The problem:** FantasyPros is the gold standard for consensus analyst rankings, but their Terms of Service prohibit scraping.

**Options ranked by legal safety:**

1. **The Odds API** (https://the-odds-api.com/) — Vegas player props, legally accessible, free tier (500 req/month). Use as a calibration signal.
2. **nflverse pbp data** — Play-by-play truth data is already in `nfl-data-py`. Build your own accuracy tracker against actual fantasy points.
3. **FantasyPros API** — They offer a paid partner API (~$50/month). Worth it once you have users.
4. **RSS / public content** — Scraping individual analyst Twitter/X or Substack is fragile; X's API now costs $100/month for basic access.

**My recommendation:** Start with nflverse as the "ground truth" for actual points. For analyst input in Phase 1, manually curate a seed list of 10–20 analysts. Automate ingestion in Phase 2 via FantasyPros partner API.

---

### 4. Historical Data Depth

`nfl-data-py` has data going back to 1999. Fantasy-relevant decisions need at minimum:

- **2 seasons** — enough for basic trend analysis and model training
- **5 seasons** — recommended; captures multiple "eras" of offensive philosophy shifts
- **All available** — useful for analyst accuracy tracking, ~450 MB of parquet data locally

**My recommendation:** Start with 2022–2024 (3 seasons) for Phase 1. Download and cache as local parquet files. Expand as needed.

---

### 5. Azure Hosting Shape (when you're ready)

**My recommendation: Azure Container Apps + Azure Container Jobs**

| Component | Service | Est. cost (light usage) |
|---|---|---|
| Python API (FastAPI) | Azure Container Apps | ~$5–20/month (scale to 0) |
| Weekly data refresh | Azure Container Jobs | ~$1–3/month |
| Database | Azure Database for PostgreSQL Flexible (Burstable B1ms) | ~$15/month |
| Frontend | Azure Static Web Apps | Free tier |
| Storage (parquet/blobs) | Azure Blob Storage | ~$1–2/month |
| **Total** | | **~$22–40/month** |

This is the cheapest Azure option that scales. Kubernetes (AKS) is overkill and ~10x more expensive.

---

### 6. OpenAI Cost Projection

With `gpt-4o-mini` at $0.15/1M input + $0.60/1M output tokens:

| Usage | Tokens/call | Calls/day | Monthly cost |
|---|---|---|---|
| 1 active user (light) | ~2,000 | 5 | ~$0.05 |
| 10 users (active season) | ~2,000 | 50 | ~$0.50 |
| 100 users | ~2,000 | 500 | ~$5 |

This is extremely affordable at `gpt-4o-mini`. You can add `gpt-4o` as a "premium" tier when you charge users without breaking the bank on the free tier.

---

## Recommended Next Steps

1. **Run `uv sync`** (or `pip install -e ".[dev]"`) and validate the environment
2. **Run `uv run ffa db-init`** to create your local SQLite database
3. **Run `uv run ffa fetch-stats 2022 2023 2024`** to pull NFL data and validate coverage
4. **Add your OPENAI_API_KEY to `.env`** (copy from `.env.example`)
5. **Test the lineup CLI:** `uv run ffa lineup --context "I have Justin Jefferson, Tyreek Hill, Josh Allen..."`
6. **Answer the 6 questions above** so I can proceed to Phase 2 (web framework, auth, cloud setup)

---

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                     fantasy-football-ai                         │
│                                                                 │
│  CLI / Web UI (Phase 3)                                         │
│         │                                                       │
│         ▼                                                       │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                  Analysis Layer (src/ai)                 │   │
│  │  Draft Advisor │ Lineup Optimizer │ Waiver │ Matchup     │   │
│  │                      ▲                                   │   │
│  │              OpenAI API (gpt-4o-mini)                    │   │
│  └─────────────────────────────────────────────────────────┘   │
│         │                                                       │
│         ▼                                                       │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                   Data Layer (src/data)                  │   │
│  │                                                          │   │
│  │  nfl-data-py   │  Sleeper API  │  ESPN (Phase 2)         │   │
│  │  (weekly stats,│  (leagues,    │  (unofficial)           │   │
│  │   rosters,     │   rosters,    │                         │   │
│  │   schedule)    │   waivers)    │                         │   │
│  └─────────────────────────────────────────────────────────┘   │
│         │                                                       │
│         ▼                                                       │
│  SQLite (dev) → Azure PostgreSQL (prod)                         │
└─────────────────────────────────────────────────────────────────┘
```
