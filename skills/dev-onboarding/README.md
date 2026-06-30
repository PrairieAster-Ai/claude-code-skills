# dev-onboarding

Get a developer from a fresh `git clone` to a running localhost — **fast** and
**self-diagnosing** — for two paths: an internal **team member** and an external
**contributor** (forking to customize/contribute, no internal access).

## Why

Most repos have *docs* and *running-service health checks*, but nothing that checks a
**cold machine** — missing tools, wrong Node version, absent/placeholder secrets — and
tells you the exact fix. And the one script that claims that role tends to rot ("works
on my machine"). This skill fills that gap with a read-only **doctor** + an idempotent
**bootstrap**, both driven by one `dev-onboarding.config.json`, so they can't drift.

## Quick start (in a configured repo)

```bash
npm run doctor                       # read-only: what's missing + how to fix it
npm run doctor -- --profile contributor
npm run bootstrap                    # idempotent: install → .env → seed → run
```

## Set it up in a new repo

```bash
node ~/.claude/skills/dev-onboarding/scripts/scaffold.mjs   # infers a starter config
# review dev-onboarding.config.json, add the npm aliases it prints, commit
```

## Scripts

| Script | Role |
|---|---|
| `scripts/doctor.mjs` | **read-only** cold-start check (tools/versions/env shape/services) with exact fixes; exits non-zero on blockers |
| `scripts/bootstrap.mjs` | **idempotent** setup → hands off to the run command |
| `scripts/scaffold.mjs` | generate config + `.env.example` contributor block for a new repo |
| `scripts/config.mjs` | shared config loader |

## The two profiles

`--profile team` (internal access to real services) vs. `--profile contributor` (own
free-tier accounts / seed data). They differ only on **secrets and data** — never tools
or install. The contributor path must use real free-tier services or a *clearly-labeled*
fixture, never silent mock data.

Composes with the `code-readability` Getting-Started page (the docs) and `quality-steward`
(weekly freshness). See `SKILL.md` for modes, config schema, and design rationale.
