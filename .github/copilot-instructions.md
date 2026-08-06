# Copilot Instructions for This Repository

## Repository State

This repository is in onboarding mode. Treat it as a planning-first project scaffold for an AI-powered fantasy football analyst.

## Working Rules

1. Do not choose a language, framework, package manager, database, hosting provider, or external API unless the user explicitly asks for that decision.
2. Prefer updating or creating specs before generating implementation code when requirements are still ambiguous.
3. Keep changes minimal and reversible.
4. Record assumptions in the relevant spec file instead of embedding them silently in code.
5. If asked to scaffold code, preserve a neutral structure unless the user requests a concrete stack.

## Folder Intent

- `specs/` contains product context, open questions, and implementation planning.
- `src/` is reserved for source code after the stack is chosen.
- `tests/` is reserved for automated validation after the stack is chosen.

## Copilot Collaboration

- Summarize tradeoffs before making irreversible decisions.
- If a request implies a stack choice, call that out explicitly.
- Prefer placeholders and templates over speculative implementations during the current repo phase.