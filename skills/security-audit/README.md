# Security Audit Skill

Differential, high-signal security audit of the pending changes on the current branch. A coexisting alternative to Anthropic's bundled `/security-review` that pairs deterministic SAST/SCA/secrets scanners with LLM verification — fewer false positives, broader coverage, optional sandbox-validated fixes.

## What's new vs the bundled `/security-review`

| | Bundled `/security-review` (Anthropic) | `/security-audit` (this skill) |
|---|---|---|
| Differential by default | ✓ | ✓ |
| LLM diff review | ✓ | ✓ |
| Hard exclusion list | ✓ (21 rules) | ✓ (21 rules, extended) |
| Confidence floor | 0.7 | 0.7 publish · 0.8 flag · 0.9 fix |
| Deterministic pre-pass (SAST/SCA/secrets) | ✗ | **✓ (semgrep + gitleaks + osv-scanner + lang-specific)** |
| OWASP/CWE/ATT&CK tagging | ✗ | **✓** |
| Touched-chapter ASVS checklist | ✗ | **✓ (only loads chapters the diff touches)** |
| Per-repo Memories (FP suppression) | ✗ | **✓ (`.claude/security-memories.md`)** |
| Semantic dedup across alarms | ✗ | **✓** |
| Asymmetric FP/TP handling | ✗ | **✓ (auto-dismiss FPs only)** |
| Sandbox-validated fixes | ✗ | **✓ (with `--fix`)** |
| SARIF outputs for GitHub Code Scanning | ✗ | **✓ (per-tool, post-2025-07 compliant)** |

The two skills coexist (different slugs, different commands). Run either or both — `/security-review` for a fast LLM-only check, `/security-audit` when you want the tools-augmented review.

## Install

### Per project

```bash
git clone https://github.com/PrairieAster-Ai/claude-code-skills.git /tmp/ccs
cp -r /tmp/ccs/skills/security-audit .claude/skills/
```

### Global

```bash
git clone https://github.com/PrairieAster-Ai/claude-code-skills.git ~/.claude/skills-collection
ln -s ~/.claude/skills-collection/skills/security-audit ~/.claude/skills/security-audit
```

### Required tooling (installed once)

```bash
# Always-on stack
pipx install semgrep
brew install gitleaks osv-scanner   # or: go install github.com/google/osv-scanner/v2/cmd/osv-scanner@latest
pipx install lizard

# Conditional (installed on first need)
brew install aquasecurity/trivy/trivy       # IaC + containers
pipx install bandit                          # Python SAST
pipx install pip-audit                       # Python SCA
go install golang.org/x/vuln/cmd/govulncheck@latest   # Go SCA + reachability
npm i -g socket                              # Supply-chain typosquat detection
```

All seven are OSS and don't require API keys. Socket has a free tier without account for basic scans.

## Usage

```bash
/security-audit                  # vs origin/HEAD
/security-audit main             # vs explicit base
/security-audit --fix            # propose sandbox-validated patches for High-confidence findings
/security-audit --tools-only     # SAST/SCA pre-pass only — CI mode, writes per-tool SARIF
/security-audit --post-pr 123    # run audit + post results as a PR #123 comment (mirrors /code-review's format)
/security-audit --deep           # adds complexity hotspots + full-history secret scan
```

## How it works (5 phases + optional 6th)

```
1. Context              — diff scope, touched-chapter detection
2. Pre-pass (tools)     — semgrep, gitleaks, osv-scanner, lang-specific (parallel, <30s typical)
3. LLM verification     — per-alarm sub-tasks, source→sink reasoning, confidence scoring
4. Triage + dedup       — memories applied, semantic dedup, exclusion filter
5. Report               — markdown with CWE/OWASP/ATT&CK tags
5b. --post-pr (optional)— post the report as a GH PR comment (mirrors /code-review's shape)
6. --fix (optional)     — generate patch → apply to worktree → re-run rule → run tests → discard if regression
```

## Output

Each finding includes:

- Severity (High/Medium/Low)
- Confidence (0.0–1.0)
- CWE id + OWASP Top 10:2025 tag + MITRE ATT&CK technique
- Concrete source → sink chain
- Exploit scenario with a sample request/payload
- Fix sketch referencing the repo's existing secure pattern where applicable

## Designed-in references

The skill draws on:

- **OWASP Top 10:2025** and **OWASP ASVS 5.0** — the [`owasp-security`](https://github.com/PrairieAster-Ai/claude-code-skills) skill is a complementary deep-reference companion.
- **MITRE ATT&CK** for technique tagging
- **CWE Top 25** for category mapping
- **Anthropic's published `claude-code-security-review`** prompt and findings filter (baseline)
- **Semgrep AI-powered Memories**, **Snyk CodeReduce**, **GitHub Copilot Autofix**, **Vercel Agent**, **Greptile**, **Cursor Bugbot/Security MCP** — for specific design patterns

## Threat model

The skill itself is a target:

1. **Prompt injection from PR-introduced files** — fixed-rubric verification prompt; PR content is evidence, never instructions.
2. **PR-introduced tool config** (e.g., malicious `.semgrep.yml`) — explicit `--config=p/default`, never honor PR config.
3. **Patch application in `--fix` mode** — always on a scratch worktree, never the working tree.

See `references/threat-model.md` for the full list.

## Companion skills

`/security-audit` is **deliberately scoped to security only**. Run it alongside a general code reviewer for full coverage — the boundaries are non-overlapping by design.

| Skill | Owns | Doesn't own |
|---|---|---|
| **`/security-audit`** (this skill) | Injection, authn/authz, crypto, secrets, supply chain, ASVS findings, SSRF, deserialization, XSS in unsafe escape hatches | Bugs, lint, type errors, style, test coverage, perf, docs |
| **`/security-review`** (bundled in Claude Code) | LLM-only diff review with 21-rule exclusion list and 0.7 confidence floor | No tools, no memories, no fixes |
| **`/code-review`** (marketplace plugin: `claude-plugins-official/code-review`) | Bugs, CLAUDE.md compliance, git-history context, prior-PR comments, code-comment guidance | General security issues (explicit exclusion in its prompt — defers to a dedicated security reviewer) |
| **`/review`** (bundled in Claude Code) | Quick conversational PR review — broad scope | Single-pass, no agent fleet |
| **`/code-quality`** (this collection) | Lint, type-check, coverage, duplication, complexity | Anything diff-specific |
| **`/owasp-security`** (companion) | Deep OWASP Top 10:2025 / ASVS 5.0 / Agentic AI 2026 reference for implementing controls | Diff review |

### Recommended workflow

```
1. Pre-push (local)
   └─ /security-audit              # catch vulns before they leave your laptop

2. PR opened
   ├─ /security-audit --post-pr N  # post security findings as a PR comment (CI or manual)
   └─ /code-review N               # marketplace plugin — posts bugs/CLAUDE.md as a separate PR comment

3. Merge gate (CI)
   └─ /security-audit --tools-only # per-tool SARIF → GitHub Code Scanning
```

Three independent signals on the same PR, no duplicated findings.

### CLAUDE.md "Review ownership" pattern

To make the boundary explicit per-repo, add this to your `CLAUDE.md`:

```markdown
## Review ownership
- /security-audit owns: injection, authn/authz, crypto, secrets, supply chain
- /code-review owns: bugs, CLAUDE.md compliance, historical context
- Neither owns: lint, type errors, formatting, test coverage (CI handles these)
```

Both skills read CLAUDE.md and will respect this boundary.

### Shared context files

| File | Read by | Purpose |
|---|---|---|
| `CLAUDE.md`, `AGENTS.md`, `.cursorrules` | both skills | Repo conventions |
| `.claude/security-memories.md` | `/security-audit` only | Per-repo FP suppressions for security findings |
| `.claude/security-config.yaml` | `/security-audit` only | Per-repo exclusion / enable overrides |

## Limitations

- **No whole-repo graph index.** Greptile-style graph grounding would improve reachability calls but requires infra beyond Claude Code's built-ins. The skill compensates with `Grep`/`Glob` + lang-specific tools.
- **Custom rule packs aren't shipped here** — defaults use Semgrep's `p/default`. Add `--config=p/your-custom-pack` to the skill invocation for your team's rules.
- **No persistent cross-PR findings store.** Cursor's Security MCP pattern (Lambda + classifier) would be a follow-up.

## Files

| File | Purpose |
|---|---|
| `SKILL.md` | Main skill prompt with full workflow |
| `references/tools.md` | Tool-by-tool comparison + install + scope-to-diff commands |
| `references/exclusions.md` | The 21-rule hard exclusion list with rationale |
| `references/asvs-chapter-map.md` | Touched-chapter detection patterns |
| `references/threat-model.md` | Threats against the skill |
| `references/memories-template.md` | Starter `.claude/security-memories.md` |

## License

Same as the parent repo.
