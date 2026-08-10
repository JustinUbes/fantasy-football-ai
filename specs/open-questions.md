# Open Questions

## Resolved Decisions

| Decision | Choice | Notes |
|---|---|---|
| Sport focus | American football (NFL) | Explicit |
| Backend language | Python | Explicit |
| AI provider | OpenAI API | Explicit |
| Cloud provider | Microsoft Azure | Explicit |
| Domain registrar | Porkbun | Explicit |
| Phase 1 fantasy platform | Sleeper | Best free API available |
| Phase 1 NFL data | `nfl-data-py` | Free, Python-native, backed by nflverse |
| Local dev database | SQLite | Zero cost, zero setup, schema mirrors production |

---

## Open — Require User Input

### 1. Frontend Framework — **Decided: React.js**
React.js chosen to keep the mobile path (React Native) open post-MVP. Backend API is served by FastAPI; the React app is a pure SPA deployed to Azure Static Web Apps.

### 2. Hosting Shape for Python Backend
**Options:**
- **Azure Container Apps** — autoscaling, pay-per-use, managed containers; recommended for FastAPI
- **Azure App Service** — simpler, flat pricing, good for predictable traffic
- **Azure Functions** — true serverless, cheapest at low volume, but Python cold starts can be slow

**Recommendation:** Azure Container Apps for the API + Azure Container Jobs for weekly data refresh cron work.

### 3. User Authentication
**Options:**
- **Azure Entra External ID (B2C)** — free up to 50k MAU, stays entirely in Azure
- **Clerk** — fastest dev experience, generous free tier, more opinionated
- **Auth0** — mature, free to 7.5k MAU

**Recommendation:** Clerk for development speed; migrate to Azure Entra External ID at scale if you want everything on one Azure bill.

### 4. OpenAI Model Strategy
**Options:**
- `gpt-4o-mini` — very cheap (~$0.15/1M input tokens), strong reasoning for structured advice
- `gpt-4o` — best quality, ~15x more expensive
- Mixed — use mini for routine advice, gpt-4o for high-stakes moments (e.g. draft day)

**Recommendation:** Start exclusively with `gpt-4o-mini`; add `gpt-4o` as a premium mode once you have real usage data to justify cost.

### 5. ESPN Fantasy Integration
ESPN has no official public API. Options:
- Use the `espn-api` community library (cwendt94) — wraps internal endpoints, fragile to breakage
- Reverse-engineer hidden endpoints directly (see docs/data-sources.md)
- Skip ESPN Phase 1, prioritize Sleeper + Yahoo first

**Recommendation:** Deprioritize ESPN until hidden endpoints are validated. Add Yahoo (OAuth2) in Phase 2.

### 6. Analyst Ranking Data Source
- Scrape FantasyPros consensus rankings as ground truth for analyst comparisons?
- Pull individual writer predictions from blogs/social (requires LLM extraction pipeline)?

**Needs your direction** — FantasyPros has ToS restrictions on scraping. Vegas lines (The Odds API) are a cleaner, legally safer option for calibration signals.

### 7. Python Package Manager
**Options:**
- `uv` — modern, extremely fast, growing adoption
- `poetry` — mature, widely used, lockfile support
- `pip + requirements.txt` — simplest, universal

**Recommendation:** `uv` — fastest-growing standard, works seamlessly with `pyproject.toml`.

### 8. Product Tiering: Weekly vs Instant Decisions
Concept:
- **Weekly mode**: baseline assistant behavior using scheduled refreshes and cached weekly context
- **Instant mode**: premium chat experience for near-real-time decision support when users want immediate guidance

Open decisions:
- What freshness window qualifies as "instant" for paid users?
- Which capabilities are weekly-only vs instant-tier (lineup, waivers, matchup, start/sit)?
- How should usage and refresh limits be enforced per tier?

Recommendation:
- Launch with weekly mode for all users first.
- Add instant mode as a paid convenience tier after local assistant and core seasonal flows are stable.

---

## Product Scope (Confirmed)
Outputs: who to draft, who to pick up, best lineup, who to drop, waiver wire advice, matchup-specific analysis, post-week reports.
Users have accounts linked to their fantasy platforms.
Focus: fantasy American football.

## Data
See `/docs/data-sources.md` for identified sources.
- **Open**: What historical depth is required? (2 seasons? 5 seasons? All available?)
- **Decided**: Stats are consumed week-by-week. Fetch the current week on demand at query time; cache completed weeks locally so we never re-download finished data.
