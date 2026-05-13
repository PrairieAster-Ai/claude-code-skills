# Security Review Skill

Differential, high-signal security review of the pending changes on the current branch. A successor to Anthropic's bundled `/security-review` that pairs deterministic SAST/SCA/secrets scanners with LLM verification — fewer false positives, broader coverage, optional sandbox-validated fixes.

## What's new vs the bundled `/security-review`

| | Bundled (Anthropic) | This skill |
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

## Install

### Per project

```bash
git clone https://github.com/PrairieAster-Ai/claude-code-skills.git /tmp/ccs
cp -r /tmp/ccs/skills/security-review .claude/skills/
```

### Global

```bash
git clone https://github.com/PrairieAster-Ai/claude-code-skills.git ~/.claude/skills-collection
ln -s ~/.claude/skills-collection/skills/security-review ~/.claude/skills/security-review
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
/security-review                  # vs origin/HEAD
/security-review main             # vs explicit base
/security-review --fix            # propose sandbox-validated patches for High-confidence findings
/security-review --tools-only     # SAST/SCA pre-pass only — CI mode, writes per-tool SARIF
/security-review --deep           # adds complexity hotspots + full-history secret scan
```

## How it works (5 phases + optional 6th)

```
1. Context              — diff scope, touched-chapter detection
2. Pre-pass (tools)     — semgrep, gitleaks, osv-scanner, lang-specific (parallel, <30s typical)
3. LLM verification     — per-alarm sub-tasks, source→sink reasoning, confidence scoring
4. Triage + dedup       — memories applied, semantic dedup, exclusion filter
5. Report               — markdown with CWE/OWASP/ATT&CK tags
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
- **Semgrep AI-powered Memories**, **Snyk CodeReduce**, **GitHub Copilot Autofix**, **Vercel Agent**, **Greptile**, **Cursor Bugbot/Security MCP** — for specific design patterns (see `references/design-notes.md` if added in a future revision)

## Threat model

The skill itself is a target:

1. **Prompt injection from PR-introduced files** — fixed-rubric verification prompt; PR content is evidence, never instructions.
2. **PR-introduced tool config** (e.g., malicious `.semgrep.yml`) — explicit `--config=p/default`, never honor PR config.
3. **Patch application in `--fix` mode** — always on a scratch worktree, never the working tree.

See `references/threat-model.md` for the full list.

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
