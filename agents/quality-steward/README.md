# quality-steward

A reusable **Claude Code agent** that stands watch over a repository's **code quality**
and **documentation**. It composes existing skills toward three outcomes, on a schedule
and on every PR:

> **monitor** the health metrics → **suggest** improvements → **document** (keep the docs true)

It is an *orchestration agent*, not a skill: one agent given a goal and a toolbox
(`/code-review`, `/code-readability`, `/security-audit`, `/github`) that decides what to do
with what it finds.

## What it does

| Outcome | How |
|---|---|
| **Monitor** | Runs your project's metric command (if any) and computes deltas vs. the last reading — the regression is the headline. |
| **Suggest** | Invokes `/code-review` + `/security-audit` + `/code-readability assess` on the right diff, dedupes, ranks. |
| **Document** | Runs your doc-publish flow (e.g. `/code-readability publish` / `team`) so docs never drift from the code. |

### The autonomy contract
- **Safe, mechanical fixes are auto-applied** — but only on a `steward/auto-fix-*` branch + PR, **never a direct push to the default branch**, and only when the green-gate stays green with an empty non-comment diff (doc-comments, lint `--fix`, formatting).
- **Risky findings are only suggested** — anything touching logic, deps, or security goes to **GitHub issues** (weekly sweep) or **inline PR comments** (per-PR), never edited.

### Run modes
| Trigger | Mode | Diff window | Output |
|---|---|---|---|
| `pull_request` | per-PR | the PR diff | inline PR comments |
| `schedule` (weekly) | sweep | the week's merged commits (`git diff <last-sweep-sha>...HEAD`, SHA in agent memory) | GitHub issues |
| `workflow_dispatch` | on-demand / verify | as instructed | issues / none |

## Prerequisites

1. **Claude Code** with the composed skills available. `code-review` and `code-quality` are
   built in; `code-readability`, `security-audit`, and `github` install from this repo (the
   workflow does this automatically in CI).
2. **A Claude subscription token** for CI auth (Max/Pro) — see install step 4. Using the
   subscription means **no separate API key / API billing**.

## Install

From the repo you want the steward to watch:

**1. Copy the agent definition** into the project's agent dir:
```bash
mkdir -p .claude/agents
curl -fsSL https://raw.githubusercontent.com/PrairieAster-Ai/claude-code-skills/main/agents/quality-steward/quality-steward.md \
  -o .claude/agents/quality-steward.md
```

**2. Copy the workflow** into `.github/workflows/`:
```bash
mkdir -p .github/workflows
curl -fsSL https://raw.githubusercontent.com/PrairieAster-Ai/claude-code-skills/main/agents/quality-steward/quality-steward.yml \
  -o .github/workflows/quality-steward.yml
```

**3. Make sure the agent file is tracked.** If `.claude/` is gitignored, un-ignore the
agents dir so CI can check it out — in `.gitignore`:
```gitignore
.claude/*
!.claude/agents/
```

**4. Authenticate CI with your subscription:**
```bash
claude setup-token        # prints a one-year OAuth token — copy it
```
Add it as an **Actions** secret named exactly **`CLAUDE_CODE_OAUTH_TOKEN`**
(repo-level, or org-level with this repo in the access list).
**Do not** also add an `ANTHROPIC_API_KEY` secret — it takes precedence and silently
overrides the subscription token.

**5. Adjust the workflow for your stack.** The template assumes Node/npm; swap the
`setup-node` / `npm ci` steps for your toolchain, and set the per-project knobs in
`quality-steward.md` → *Configure for your project* (metric command, green-gate commands,
auto-fixable surface, doc-publish flow).

## Verify before you rely on it

The workflow ships a **zero-side-effect verify mode**. After adding the secret:

```bash
gh workflow run quality-steward.yml -f mode=verify
gh run watch "$(gh run list --workflow=quality-steward.yml --limit 1 --json databaseId -q '.[0].databaseId')" --exit-status
```
- ✅ green → token valid, secret scoped to this repo, action wired.
- ❌ `Could not fetch an OIDC token` → `id-token: write` permission missing (it's in the template; check you copied the whole file).
- ❌ auth error → secret missing / not granted to this repo / token expired.

Then do one full run and watch it before trusting the unattended triggers:
```bash
gh workflow run quality-steward.yml -f mode=steward
```

## Usage

- **Automatic:** opens on every PR (differential review) and runs the weekly sweep.
- **On demand:** Actions → *Quality & Docs Steward* → *Run workflow* → `mode: steward`.
- **Locally:** with the agent file in `.claude/agents/`, restart Claude Code and invoke it
  via `/agents` (or `claude --agent quality-steward`). Restart is required — the agent
  registry loads at startup.

## Troubleshooting

| Symptom | Fix |
|---|---|
| `Could not fetch an OIDC token` | The job needs `id-token: write` (workflow-level and on the verify job). It's in the template. |
| Auth fails despite the secret | Ensure no `ANTHROPIC_API_KEY` secret exists (it wins); confirm the token isn't expired (`claude setup-token` mints a fresh one yearly). |
| Steward run blocks on `npm`/`gh`/`git` | Swap `--permission-mode acceptEdits` for `--dangerously-skip-permissions` in `claude_args` (safe on an ephemeral runner; the agent's guardrails forbid pushing to the default branch). |
| Per-PR review doesn't run on a **public** repo's outside PRs | Expected — GitHub withholds secrets from fork PRs. Keep the trigger as `pull_request`; **never** switch to `pull_request_target` (it would expose your token to untrusted fork code). |
| Duplicate PRs/issues across runs | The agent dedupes against open `steward/*` PRs and matching issues; ensure `memory: project` is set so it remembers across runs. |

## Files

| File | Purpose |
|---|---|
| `quality-steward.md` | The agent definition (the brain) — copy to `.claude/agents/`. |
| `quality-steward.yml` | The GitHub Actions workflow — copy to `.github/workflows/`. |
| `README.md` | This file. |
