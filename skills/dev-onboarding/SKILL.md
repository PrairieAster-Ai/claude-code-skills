---
name: dev-onboarding
description: >-
  Get a developer from a fresh clone to a running localhost — fast and
  diagnosably. Generates + runs a read-only `doctor` (detect missing
  tools/versions/secrets, print the exact fix) and an idempotent `bootstrap`
  (install → env → seed → run), designed for two paths: an internal team member
  and an external/from-scratch contributor. Use to set up, verify, or scaffold a
  local dev environment.
---

# Dev Onboarding Skill

Turns "clone → running localhost" from tribal knowledge into a **deterministic,
self-diagnosing** flow. The division of labor:

- **Scripts do the reproducible steps** (check, install, seed, run) — idempotent,
  config-driven, CI-usable, no LLM needed.
- **You (the agent) diagnose and adapt** — pick the profile, read the actual
  failure, cross-reference `CLAUDE.md`/`.env.example`, explain *why*, and fix it.

It **composes with** what a repo already has — it doesn't replace the run command
(`npm start`), the `.env.example` contract, or the `code-readability` Getting-Started
wiki page. The Getting-Started page *describes* setup for humans; this skill
*executes and verifies* it from the same source facts, so they can't disagree.

## The two paths (the core design)

Onboarding diverges almost entirely on **secrets and data**, never on tools/install:

| | **`team`** — internal access | **`contributor`** — no access (fork/OSS) |
|---|---|---|
| Tools, install | identical | identical |
| Database | the real internal connection string | their own free-tier DB + a seed command |
| API keys | team/personal keys | personal free keys, or a **clearly-labeled** mock toggle |
| Goal | running on live services, fast | running on own/seed data, modify, open a PR |

> **Honesty rule:** a contributor "mock" path must never serve silent fake data
> behind the live code path. Seed a real free-tier DB, or load a *clearly-labeled*
> fixture in an explicit local mode. (Mirrors the data-integrity rule many repos keep.)

## Modes

- **`doctor`** *(default, read-only)* — cold-start check: OS/shell, each required
  tool vs. its version range (`.nvmrc`/`engines`), `.env` presence **and the shape**
  of each secret for the active profile, optional service reachability (`--services`).
  Prints a checklist with the **exact fix** for every red line; exits non-zero on any
  blocker (CI-friendly). `node scripts/doctor.mjs --profile team|contributor`.
- **`bootstrap`** *(idempotent, mutates)* — runs the doctor, then install → create
  `.env` from the example (never clobbers) → the profile's data path (contributor:
  set mock toggles + point at the seed command) → hands off to the run command.
  Re-runnable. `node scripts/bootstrap.mjs --profile …`.
- **`scaffold`** *(one-time, for a new repo)* — infers a starter
  `dev-onboarding.config.json` from `package.json`/`.nvmrc`/`.env.example`, appends a
  "Contributor (no internal access)" block to `.env.example`, and prints the npm
  aliases + Getting-Started wiring. Review the generated config before committing.
- **`verify`** — `doctor --services` + the run command's smoke endpoints; report
  green/red. Good for the steward's freshness sweep and for CI.

## Configure for your project

Add `dev-onboarding.config.json` at the repo root (or run `scaffold` to generate it):

```jsonc
{
  "project": "my-app",
  "runCommand": "npm start",
  "runUrl": "http://localhost:3001",
  "healthEndpoints": ["http://localhost:4000/api/health"],
  "requiredTools": [
    { "name": "node", "versionFrom": ".nvmrc" },
    { "name": "npm", "range": ">=10.8.0" },
    { "name": "git" },
    { "name": "docker", "optional": true, "reason": "local Redis cache" }
  ],
  "secrets": {
    "DATABASE_URL":       { "profiles": ["team","contributor"], "shape": "^postgres(ql)?://", "help": "Neon connection string" },
    "OPENWEATHER_API_KEY":{ "profiles": ["team","contributor"], "shape": "^[a-f0-9]{16,}$", "mockToggle": "USE_MOCK_WEATHER", "help": "free OpenWeather key" }
  },
  "profiles": {
    "team":        { "desc": "internal access" },
    "contributor": { "desc": "own free-tier accounts", "seedCommand": "node scripts/seed.js", "mockEnv": ["USE_SEED_DATA=true"] }
  }
}
```

Wire `npm run doctor` / `npm run bootstrap` to the scripts (point at the skill dir,
like the other skills). The same config drives any repo.

## How it relates to the other skills

- **`code-readability team`** owns the *docs* (Getting-Started + Skill-Inventory pages);
  this skill is what those pages tell you to run. They read the same `package.json` +
  `.env.example`.
- **`quality-steward`** keeps it honest: add `doctor`/the config to the weekly sweep so
  the checks never drift from `package.json` (the exact failure mode that rots hand-
  maintained setup scripts).

## Don'ts

- Don't overwrite an existing `.env` (bootstrap copies only when missing).
- Don't bake machine-specific assumptions into the scripts — everything from config.
- Don't serve silent mock data for the contributor path (honesty rule above).
- Don't replace the project's run command — hand off to it.

## Files

- `scripts/config.mjs` — config loader + helpers
- `scripts/doctor.mjs` — read-only cold-start check (the highest-leverage piece)
- `scripts/bootstrap.mjs` — idempotent setup
- `scripts/scaffold.mjs` — generate config + contributor block for a new repo
