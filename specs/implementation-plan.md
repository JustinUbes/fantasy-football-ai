# Implementation Plan

## Decided Stack

| Layer | Choice | Rationale |
|---|---|---|
| Language | Python | Best-in-class AI/ML ecosystem, OpenAI SDK first-class support |
| AI | OpenAI API | Explicit user decision |
| Infrastructure | Microsoft Azure | Explicit user decision |
| Domain registrar | Porkbun | Explicit user decision |
| NFL stats (free) | `nfl-data-py` + ESPN hidden endpoints | Zero cost; week-by-week granularity for in-season decisions |
| Fantasy platform (Phase 1) | Sleeper | Full free read-only API, no OAuth needed |

---

## Phase 1 — Data Foundation (No Cost / Minimal Cost)

**Goal**: Validate data quality and establish the data pipeline before any UI or cloud work.

### 1.1 NFL Statistics Pipeline
- Integrate `nfl-data-py` (free PyPI package backed by nflverse) for historical player and game stats
- Validate coverage: rosters, seasonal stats, weekly stats, snap counts, injury reports
- Store locally in SQLite for development

### 1.2 Sleeper Fantasy API Client
- Build a read-only HTTP client wrapping the Sleeper API (no API key required)
- Fetch: leagues, rosters, players, matchups, transactions, waiver orders
- Map Sleeper player IDs to NFL player identities

### 1.3 ESPN Endpoint Exploration
- Enumerate and test the hidden ESPN fantasy endpoints (see docs/data-sources.md gist)
- Identify which endpoints cover: rosters, scoring, projections, news
- Document what is available vs. what requires authentication

### 1.4 Expert Analyst Tracking System (Design)
- Define schema for analyst predictions and outcomes
- Design accuracy-scoring logic (prediction vs. actual result)
- Sources: FantasyPros consensus data, individual beat writers, Vegas lines

### 1.5 Local Storage Schema
- SQLite schema: players, nfl_stats, analysts, analyst_predictions, users (stub), leagues
- Write migration scripts so schema can be replicated to Azure PostgreSQL later

---

## Phase 2 — AI Analysis Core (Low Cost)

**Goal**: Wire OpenAI into the data pipeline and produce useful advice output via CLI.

### 2.1 OpenAI Client Wrapper
- Thin wrapper around `openai` Python SDK
- Prompt template system for: draft advice, lineup advice, waiver wire, matchup preview
- Cost guard: token estimation before each call, model selection (gpt-4o-mini vs gpt-4o)

### 2.2 Draft Advisor
- Input: user's league settings, available players, draft position, already-drafted rosters
- Output: ranked pick recommendations with rationale

### 2.3 Lineup Optimizer
- Input: user's roster, week number, matchup data, injury reports
- Output: recommended starting lineup with reasoning

### 2.4 Waiver Wire Advisor
- Input: available free agents, user's roster weaknesses, upcoming schedule
- Output: prioritized pickup list

### 2.5 CLI Interface
- Interactive CLI for testing all advice modules before building any web UI
- Commands: `draft`, `lineup`, `waivers`, `matchup`, `report`

---

## Phase 3 — Frontend & User Accounts (Moderate Cost)

**Goal**: Web application with user auth, linked fantasy leagues, and a polished UI.

### 3.1 Web Framework — React.js
- React.js chosen for the React Native mobile path post-MVP
- API served by FastAPI backend; React app is a pure SPA (no SSR needed)

### 3.2 User Authentication
- Azure Entra ID (formerly Azure AD B2C) or Clerk for managed auth
- Users link their Sleeper/ESPN/Yahoo/Fleaflicker accounts

### 3.3 API Layer
- FastAPI (Python) serving REST endpoints consumed by the frontend
- Hosted on Azure Container Apps (recommended) or Azure Functions

### 3.4 Database Migration
- SQLite → Azure Database for PostgreSQL (Flexible Server)
- Introduce pgvector extension for analyst embedding search (optional)

---

## Phase 4 — Production & Scale

**Goal**: Reliable, deployed product with real users.

- Azure Static Web Apps (frontend) + Azure Container Apps (backend)
- Azure Blob Storage for bulk nfl-data-py snapshots and analyst article archives
- Scheduled jobs (Azure Container Jobs) for weekly data refresh
- Monitoring: Azure Monitor + Application Insights

---

## Current Focus

**Phase 1.1–1.3** — Data pipeline and Sleeper client, local SQLite storage, no cloud spend.

## Deferred Decisions

- Frontend: React.js vs Next.js (see open-questions.md)
- Azure hosting shape: Container Apps vs. App Service vs. Functions
- Whether to add embeddings (pgvector) for analyst semantic search
- Mobile app via React Native (post-MVP)