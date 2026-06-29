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
| `schedule` (weekly) | sweep | the commits merged since the last sweep (`git diff <last-sweep-sha>...HEAD`) | GitHub issues |
| `workflow_dispatch` | on-demand / verify | as instructed | issues / none |

> **Sweep state:** the workflow tracks the last-sweep SHA on a dedicated, auto-created
> `steward-state` branch (one file, `last-sweep-sha`) — CI runners are ephemeral, so this
> branch, not agent memory, is what lets each sweep resume from the last. It never touches
> your default branch. First run falls back to `HEAD~20`.

## Prerequisites

1. **Claude Code** with the composed skills available. `code-review` and `code-quality` are
   built in; `code-readability`, `security-audit`, and `github` install from this repo (the
   workflow does this automatically in CI).
2. **A Claude subscription token** for CI auth (Max/Pro) — see install step 4. Using the
   subscription means **no separate API key / API billing**.

## Install (pull-at-runtime — recommended)

The workflow **pulls the agent definition and skills from this canonical repo at runtime**
(pinned to a reviewed commit), so the repo you're installing into commits **only the
workflow** — nothing to keep in sync, one source of truth.

**1. Copy just the workflow** into `.github/workflows/`:
```bash
mkdir -p .github/workflows
curl -fsSL https://raw.githubusercontent.com/PrairieAster-Ai/claude-code-skills/main/agents/quality-steward/quality-steward.yml \
  -o .github/workflows/quality-steward.yml
```

**2. Set your project config + stack.** In the workflow:
- edit the **`PROJECT_CONFIG`** env (in "Build the run instruction") with your metric
  command, green-gate, auto-fixable surface, and doc-publish flow — these feed the
  generic agent at runtime;
- swap the `setup-node` / `npm ci` steps for your toolchain;
- review and pin **`SKILLS_REF`** to a commit you've read (it controls both the skills and
  the agent def; bump it intentionally to take upstream updates).

**3. Authenticate CI with your subscription:**
```bash
claude setup-token        # prints a one-year OAuth token — copy it
```
Add it as an **Actions** secret named exactly **`CLAUDE_CODE_OAUTH_TOKEN`** (repo-level, or
org-level with this repo in the access list). **Do not** also add an `ANTHROPIC_API_KEY`
secret — it takes precedence and silently overrides the subscription token.

**4. (Optional) Local use.** To run the agent locally (`/agents`,
`claude --agent quality-steward`), fetch the def into `.claude/agents/` — e.g. a small
`steward:sync` script that reads `SKILLS_REF` from the workflow and curls
`agents/quality-steward/quality-steward.md` at that ref. `.claude/` can stay gitignored.

### Alternative: commit the agent def
If you'd rather vendor the agent file instead of pulling it, `curl` it into
`.claude/agents/quality-steward.md`, track that path (`.claude/*` + `!.claude/agents/` in
`.gitignore`), and delete the "agents" copy line from the workflow's install step. You then
maintain your own copy and merge upstream changes by hand.

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
| Steward run blocks on `npm`/`gh`/`git` | Swap `--permission-mode acceptEdits` for `--dangerously-skip-permissions` in `claude_args` (safe on an ephemeral runner; the agent's guardrails forbid pushing to the default branch). *(In practice `acceptEdits` ran with zero permission denials — try it first.)* |
| Run fails with `error_max_turns` | The sweep is doing too much for the turn budget. Raise `--max-turns` (template ships 80) and/or shrink the first-sweep window (the agent defaults to `HEAD~20`). PR-mode runs are far lighter than the sweep. |
| Per-PR review doesn't run on a **public** repo's outside PRs | Expected — GitHub withholds secrets from fork PRs. Keep the trigger as `pull_request`; **never** switch to `pull_request_target` (it would expose your token to untrusted fork code). |
| Duplicate PRs/issues across runs | The agent dedupes against open `steward/*` PRs and matching issues; ensure `memory: project` is set so it remembers across runs. |

## Files

| File | Purpose |
|---|---|
| `quality-steward.md` | The agent definition (the brain) — the **canonical source**; the workflow pulls it at runtime (don't copy it unless using the vendored alternative). |
| `quality-steward.yml` | The GitHub Actions workflow — the **only file you copy** into a consuming repo. |
| `README.md` | This file. |
