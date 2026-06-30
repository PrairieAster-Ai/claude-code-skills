# Changelog

All notable changes to this repository are documented here. The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and the project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html) for tagged skill releases.

## [Unreleased]

### quality-steward (agent)

- **Document the `steward-state` branch + sync the agent definition.** The shipped workflow keeps durable state on a dedicated `steward-state` branch (machine-owned, never merged): the `last-sweep-sha` that anchors each weekly diff window, and — new — the accumulated `code-health/*-history.tsv` trend, which the workflow now **restores** before a sweep and **persists** after, so the CodeHealth dashboard is a real trend line across ephemeral CI runners rather than a single-row baseline. The agent definition now documents this branch (and that the agent must not write to it), and is reconciled with improvements that had accrued in the reference vendor copy but never landed here: the `/wiki-publish` composition note, the Quality-Coverage checklist refresh step, and the CodeHealth dashboard-stamp step in the document phase.

### wiki-publish (new skill)

- **Add the `wiki-publish` skill** — the shared GitHub-Wiki publishing substrate factored out of `code-readability` and `code-health`. Owns *how* generated facts reach the wiki: generic `<!--PREFIX:NAME-->…<!--/PREFIX:NAME-->` marker stamping (`stamp.mjs <facts.json> <prefix> <pages>`, generic over prefix so `ch:` for the CodeHealth dashboard and `cr:` for the team pages share one stamper), plus the wiki git plumbing (`wiki-repo.mjs` — derive the SSH `…​.wiki.git` URL, clone, **guard** against overwriting hand-authored pages lacking the generated marker, and commit/push). `code-health`'s `stamp-codehealth.mjs` now delegates to it (with an inline fallback so code-health stays self-contained), and `code-readability`'s Phase-4 publish points at it. Producers emit pages + a facts JSON; `wiki-publish` stamps and pushes. The `quality-steward` composes it in its document step.

### code-health

- **Add `quality-checklist.mjs`** — a steward-level capability-coverage tracker that ships with code-health (reusing its config + the `/wiki-publish` stamper). Probes the repo (CI workflows, ESLint config, `package.json`, pre-commit, code-health history, installed skills, and — with `--wiki` — published wiki pages) for **every** capability the quality skills offer and classifies each ✅ enabled / ⚠️ partial / ❌ gap / ➖ n/a, rendering a grouped matrix + summary into a **Quality-Coverage** dashboard (`<!--ql:*-->` markers). Built to stop audits from forgetting things: it surfaces capabilities that are *available but never enabled* — e.g. a metric that's measured but never made a merge-blocking CI gate (circular-imports / cognitive-complexity / cyclomatic / doc-coverage). The quality-steward runs it in its weekly document step.

### code-health (new skill)

- **Add the `code-health` skill** — the structural-metrics-and-dashboard half of code quality, kept separate from `/code-quality` (coverage/lint/sprint), `/code-readability` (docs), and `/security-audit` (security). Computes a **Maintainability Index** (per-file, from the TS compiler API — Halstead Volume + cyclomatic + SLOC, banded green/yellow/red), **cyclomatic complexity** per function (TS AST), **churn × complexity hotspots** (git log × AST), **coupling/instability** (`dependency-cruiser`), **change-coupling** (files edited together; cross-layer = smell), **duplication** (`jscpd`), and **circular imports** (`madge`), then rolls them into a transparent weighted **CodeHealth** score (0–100 + letter grade) and stamps the **Code Health Dashboard** wiki page via `<!--ch:*-->` markers. Ships `maintainability/complexity/hotspot/coupling/change-coupling/duplication/security/coverage-report.mjs`, `check-circular-deps.mjs` + `check-doc-coverage.mjs` (gate-able), `codehealth-report.mjs` (roll-up), `stamp-codehealth.mjs`, and `run-all.mjs`, plus `references/methodology.md` (formulas, anchors, dashboard template). Project-agnostic: per-repo settings come from a `code-health.config.json` (`dirs`/`docDirs`/`coverageWorkspaces`/`tsconfig`/`historyDir`/`blobBase`), and GitHub file links derive from the `origin` remote, so the same skill drives any TS/React repo. The `quality-steward` agent composes it for its metric + dashboard step.

### quality-steward (new agent)

- **Add the `quality-steward` orchestration agent** (`agents/quality-steward/`) — the repo's first reusable *agent* (vs. skill): one agent that composes `/code-review`, `/code-readability`, `/security-audit`, and `/github` toward three outcomes — monitor quality metrics, suggest improvements, keep docs in sync. Autonomy contract: safe mechanical fixes go through an auto-fix PR (never a direct push to the default branch); risky findings are only suggested (inline PR comments per-PR, GitHub issues on the weekly sweep). The weekly sweep reviews the week's merged commits (`git diff <last-sweep-sha>...HEAD`, SHA tracked in agent memory) so the differential review/audit skills have a real diff. Ships the agent definition (`quality-steward.md`), a portable GitHub Actions workflow (`quality-steward.yml`) with PR + weekly + on-demand triggers, a zero-side-effect `verify` mode, subscription-token auth (`CLAUDE_CODE_OAUTH_TOKEN`, no API key), and the required `id-token: write` OIDC permission, plus an install + usage README. Project-agnostic: per-project knobs (metric command, green-gate, auto-fixable surface, doc-publish flow) are documented in the agent's "Configure for your project" section. Establishes the `agents/` layout in this repo.

### code-readability (new skill)

- **Add the `code-readability` skill** — enforces a TSDoc-native comment standard that serves four readers at once (human, IDE, doc generator, AI agent), then generates and publishes cross-linked API docs to a GitHub Wiki. Modes: `assess` (doc-coverage scorecard), `annotate` (add/upgrade TSDoc, comments-only), `generate` (hybrid tool + prose Markdown), `publish` (push to the wiki), `team` (onboarding + skill-inventory pages). Ships `extract-docs.mjs` (react-docgen-typescript), `gen-schema-page.mjs` (Drizzle schema → wiki page), `gen-team-pages.mjs` (repo-stamped onboarding + skill-inventory pages), `linkify-wiki.mjs`, and `wiki-slug.mjs`, plus `references/comment-style.md` (TSDoc house style; also HTML/CSS/Sass/vanilla-JS) and `references/doc-generation.md`. Project-agnostic: paths are parameterized via `CR_TSCONFIG` / `CR_SCHEMA` / `CR_PKG` / `CR_ENV_EXAMPLE` / `CR_REPO_ROOT` env vars + CLI args, with worked examples framed as illustrative.
- **Add the `team` mode** (Phase 5) — maintains two *human-facing* wiki pages that document the team, not code symbols: `Getting-Started.md` (fresh clone → running localhost) and `Skill-Inventory.md` (a competency matrix across technology, design patterns, database, frontend, and Agile/delivery, with Aware/Working/Fluent targets). Both are hand-authored prose with repo-stamped fact-blocks: `gen-team-pages.mjs` regenerates four `<!--cr:…-->` markers — prereqs (Node + package manager), env (parsed `.env.example`), scripts (root `npm run` targets), and stack (deps + versions across all `package.json`) — so the factual bits never drift while the prose stays curated. `team scaffold` creates the pages; `team stamp` (default) refreshes the facts, ideally wired into the same periodic job that stamps other living docs.

### Automation layer (new)

- **Add `scripts/security_audit.py`**, **`hooks/pre-push.security-audit`**, **`.github/workflows/security-audit-tools-only.yml`** — the deterministic portion of the security-audit skill extracted into a standalone CLI. Originally contributed by John Malone (@Pro777) in PR #1; landed here with the PR #2 fixes layered in (ESLint 9+ flat config, gitleaks merge-base resolution, HTML-comment marker for `--post-pr` dedup, cross-repo safety check).
- **Fix `scripts/code_quality.py` lint/typecheck error counting** — replace `extract_first_number` (which grabbed the first digit anywhere in stdout, including line numbers) with dedicated `count_eslint_errors` and `count_tsc_errors` functions that look for canonical error markers (`N errors` summary line and `error TS<code>:` patterns respectively).
- **Fix `scripts/code_quality.py` coverage default** — fall through to `npx vitest run --coverage` directly instead of `npm run test`, which rarely emits coverage by itself.
- **Fix `scripts/code_quality.py` `: any` false positives** — strip `//` and `/* */` comments before counting, switch to regex `:\s*any\b` so it doesn't match `// can be: any` or `:: anything`.

### security-audit

- **Fix:** `--post-pr` dedup now embeds an HTML-comment marker (`<!-- security-audit:sha=<full> -->`) so the dedup grep is deterministic. Previously the short-SHA header didn't match the full-SHA grep and every push re-posted.
- **Fix:** `--post-pr` mode no longer mutates the user's working tree. Uses `git worktree add --detach` rooted at the PR HEAD SHA with `trap` cleanup.
- **Fix:** ESLint pre-pass uses a scratch flat-config file instead of the removed `--no-eslintrc` flag (ESLint 9+ compatible).
- **Fix:** `--fix` worktrees symlink the original `node_modules` / `.venv` / `vendor` so the test re-run can actually load dependencies. Fixes were being silently discarded as regressions.
- **Fix:** Exclusion count consistent across SKILL.md, exclusions.md, and README (25 items, was 21/25 mismatch).
- **Fix:** gitleaks `--log-opts` resolves symbolic refs (e.g. `origin/HEAD`) to a concrete merge-base before passing the range.
- **Fix:** `--post-pr` refuses to post if cwd repo doesn't match the PR's base repo (prevents cross-repo accidents).
- **Fix:** Memory and CLAUDE.md files now loaded from the PR base ref via `git show`, not from the PR head (T8 in threat model). A contributor cannot bury a malicious memory in their own PR.
- **Docs:** `--deep` mode is now specified (full-repo complexity, full-history secret scan, full SCA).
- **Docs:** Socket auth requirements clarified (`scan create` needs `socket login`).
- **Docs:** Worked example output added to README so users see the shape of a finding before installing.
- **Docs:** ASVS chapter map extended with V4 (Access Control) and V13 (API & Web Service Security) rows.
- **Docs:** T2 threat (PR-introduced tool config) expanded to list every config file the skill cares about, with an allowlist-of-acceptable-changes mitigation.
- **Style:** Em dashes removed from prose (kept inside code blocks).
- **Chore:** Dropped unused `Bash(eslint:*)` from `allowed-tools`; all eslint invocations go through `npx`.

## [0.2.0] - 2026-05-13

### Added
- `security-audit` skill (initially named `security-review`, renamed to coexist with Anthropic's bundled `/security-review`).
- `--post-pr <N>` mode that posts findings as a GitHub PR comment matching the `/code-review` plugin's format.
- Companion-skills documentation and CLAUDE.md "Review ownership" pattern.

### Changed
- Repository license: MIT → Apache License 2.0 (adds explicit patent grant).

## [0.1.0] - 2026-02-06

Initial release of `job-apply`, `code-quality`, and `github` skills.
