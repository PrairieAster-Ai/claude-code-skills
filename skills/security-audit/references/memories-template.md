# `.claude/security-memories.md` template

This file lives in the **target repo** (not in this skill). Drop it at `.claude/security-memories.md` to suppress known false positives across runs of `/security-audit`.

The skill reads this file on every run and applies entries before reporting. New memories are *proposed* after human triage. Never written automatically.

## Format

Each memory is a markdown section. The header is the human-readable title; the body has structured fields the skill parses.

```markdown
## FP: <one-line title>

- **Rule:** <tool>:<rule-id>  e.g.  semgrep:javascript.lang.security.audit.xss.template-injection
- **Scope:** <path glob>  e.g.  components/Markdown.tsx  or  packages/internal-tools/**
- **Reason:** Why this is a false positive in this codebase. Required.
- **Created:** YYYY-MM-DD by <author>
- **Expires:** (optional) YYYY-MM-DD — date this memory should be re-evaluated
```

## Example

```markdown
# Security review memories

## FP: dangerouslySetInnerHTML in Markdown renderer

- **Rule:** semgrep:javascript.lang.security.audit.xss.template-injection
- **Scope:** apps/web/src/components/Markdown.tsx
- **Reason:** Input passes through DOMPurify in lib/sanitize.ts:42 before render. The pattern is enforced by the test in apps/web/src/components/Markdown.test.tsx.
- **Created:** 2026-05-13 by Robert Speer
- **Expires:** 2026-11-13

## FP: child_process.exec in release scripts

- **Rule:** eslint:security/detect-child-process
- **Scope:** scripts/**, packages/database/scripts/**
- **Reason:** scripts/* runs only at release-time with developer-controlled input via npm scripts. No network exposure, no untrusted input path.
- **Created:** 2026-05-13 by Robert Speer

## FP: hardcoded test API key

- **Rule:** gitleaks:generic-api-key
- **Scope:** apps/web/playwright/fixtures/test-stripe-key.ts
- **Reason:** Documented Stripe test-mode publishable key (pk_test_*), safe to commit per Stripe's docs.
- **Created:** 2026-05-13 by Robert Speer
```

## How the skill uses memories

1. After Phase 2 (pre-pass), every alarm is matched against memories. A memory hits when **all** of `(tool, rule, path-glob)` match.
2. Matched alarms are auto-dismissed and counted in the report's "Auto-dismissed (memories: N)" line.
3. New findings that the human user dismisses during review can be promoted to memories. The skill proposes the entry but the user copies it in by hand. The skill MUST NOT write `.claude/security-memories.md` automatically.

## What memories are NOT for

- Suppressing **real** vulnerabilities. The asymmetric rule applies: memories can only suppress findings the model would already classify as FPs at confidence ≥ 0.8. A memory cannot override a TP classification.
- Suppressing **entire categories**. That belongs in `.claude/security-config.yaml` (see `exclusions.md`).
- Sharing across repos. Memories are repo-local context. They encode that codebase's specific compensating controls.

## Commit policy

Two reasonable defaults:

1. **Commit memories.** They're project context, useful for the whole team, and a good audit trail of "we considered this and decided it was OK because X."
2. **Gitignore memories.** If you want each developer's local-only triage to not affect the team's review baseline.

Pick one and document it in the repo's README. Mixing leads to confusion.
