# Changelog

All notable changes to this repository are documented here. The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and the project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html) for tagged skill releases.

## [Unreleased]

### code-readability (new skill)

- **Add the `code-readability` skill** — enforces a TSDoc-native comment standard that serves four readers at once (human, IDE, doc generator, AI agent), then generates and publishes cross-linked API docs to a GitHub Wiki. Modes: `assess` (doc-coverage scorecard), `annotate` (add/upgrade TSDoc, comments-only), `generate` (hybrid tool + prose Markdown), `publish` (push to the wiki). Ships `extract-docs.mjs` (react-docgen-typescript), `gen-schema-page.mjs` (Drizzle schema → wiki page), `linkify-wiki.mjs`, and `wiki-slug.mjs`, plus `references/comment-style.md` (TSDoc house style; also HTML/CSS/Sass/vanilla-JS) and `references/doc-generation.md`. Project-agnostic: paths are parameterized via `CR_TSCONFIG` / `CR_SCHEMA` env vars + CLI args, with worked examples framed as illustrative.

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
