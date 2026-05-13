# Claude Code Skills

A collection of reusable skills for [Claude Code](https://docs.anthropic.com/en/docs/claude-code), Anthropic's official CLI for Claude.

## Available Skills

| Skill | Description | Invoke With |
|-------|-------------|-------------|
| [**security-audit**](skills/security-audit/) | Differential security audit combining SAST/SCA/secrets scanners with LLM verification, ASVS-by-touched-chapter checklists, per-repo FP memories, and sandbox-validated fixes. Coexists with Anthropic's bundled `/security-review`. | `/security-audit [base-ref] [--fix\|--tools-only\|--post-pr N\|--deep]` |
| [**job-apply**](skills/job-apply/) | Generate tailored cover letters and resumes with job fit assessment | `/job-apply [job description]` |
| [**code-quality**](skills/code-quality/) | Code quality assessment and improvement for TypeScript/React projects | `/code-quality` |
| [**github**](skills/github/) | GitHub Wiki management, business model validation, and memory-bank integration | `/github` |

---

## Installation

### Option 1: Install Individual Skills

Copy a specific skill to your project's `.claude/skills/` directory:

```bash
# Install security-audit skill
git clone https://github.com/PrairieAster-Ai/claude-code-skills.git /tmp/claude-code-skills
cp -r /tmp/claude-code-skills/skills/security-audit ~/.claude/skills/

# Or install job-apply skill
cp -r /tmp/claude-code-skills/skills/job-apply ~/.claude/skills/

# Or install code-quality skill
cp -r /tmp/claude-code-skills/skills/code-quality ~/.claude/skills/

# Or install github skill
cp -r /tmp/claude-code-skills/skills/github ~/.claude/skills/
```

### Option 2: Install as Git Submodule (Track Updates)

```bash
# Add entire collection as submodule
git submodule add https://github.com/PrairieAster-Ai/claude-code-skills.git .claude/skills-collection

# Symlink individual skills you want to use
ln -s skills-collection/skills/job-apply .claude/skills/job-apply
ln -s skills-collection/skills/code-quality .claude/skills/code-quality
ln -s skills-collection/skills/github .claude/skills/github
```

### Option 3: Global Installation

Install skills globally for use across all projects:

```bash
git clone https://github.com/PrairieAster-Ai/claude-code-skills.git ~/.claude/skills-collection

# Symlink to global skills directory
ln -s ~/.claude/skills-collection/skills/job-apply ~/.claude/skills/job-apply
ln -s ~/.claude/skills-collection/skills/code-quality ~/.claude/skills/code-quality
ln -s ~/.claude/skills-collection/skills/github ~/.claude/skills/github
```

---

## Skills Overview

### security-audit

**Purpose:** High-signal, differential security audit of the pending changes on the current branch. Pairs deterministic SAST/SCA/secrets scanners with LLM verification so the report is actually actionable. Coexists with Anthropic's bundled `/security-review` so you can run either or both.

**Features:**
- **Differential by default** — scans base vs head, reports only NEW findings
- **Deterministic pre-pass** — `semgrep` + `gitleaks` + `osv-scanner` + language-specific tools (bandit, govulncheck, eslint-plugin-security, trivy for IaC, socket for supply chain)
- **LLM-as-verifier** — each tool alarm re-read in PR context to filter noise; confidence scored 0.0–1.0
- **Asymmetric confidence** — auto-dismisses FPs at ≥0.8, never auto-dismisses TPs (misclassifying a vuln as FP is worse than the inverse)
- **Per-repo Memories** — `.claude/security-memories.md` persists FP suppressions across runs
- **ASVS-by-touched-chapter** — loads only the OWASP ASVS 5.0 chapters the diff touches
- **OWASP / CWE / MITRE ATT&CK tagging** on every finding
- **Sandbox-validated fixes** with `--fix` — patches are applied to a scratch worktree, re-scanned, and tested before being surfaced
- **SARIF outputs** for GitHub Code Scanning (post-2025-07-21 multi-run compliant)
- **CI mode** with `--tools-only`; **PR-comment mode** with `--post-pr N` (mirrors `/code-review`'s format)

**Quick Start:**
```bash
# Install required scanners (once)
pipx install semgrep lizard
brew install gitleaks osv-scanner

# Use the skill
/security-audit                  # vs origin/HEAD
/security-audit main             # vs an explicit base
/security-audit --fix            # propose sandbox-validated patches for high-confidence findings
/security-audit --tools-only     # CI mode — writes per-tool SARIF, skips LLM phase
/security-audit --post-pr 123    # post results as a GH PR comment on PR #123
```

See [security-audit README](skills/security-audit/README.md) for the full workflow and threat model.

---

### job-apply

**Purpose:** Assess job fit and generate tailored application documents.

**Features:**
- Job fit scoring with apply/skip recommendations (80%/60%/50% thresholds)
- Cover letter generation with industry-appropriate style presets
- Resume tailoring optimized for ATS and human scanning
- Gap analysis with mitigation language templates
- WCAG AA accessible document styling
- Microsoft Word (.docx) output

**Quick Start:**
```bash
# First-time setup
cp ~/.claude/skills/job-apply/config.example.yaml ~/.claude/skills/job-apply/config.yaml
python3 ~/.claude/skills/job-apply/import_resume.py

# Use the skill
/job-apply [paste job description or path to file]
```

> **No CLI?** This skill also works in Claude's free web chat — just 2 files to upload, no install required.
> See the [web chat setup guide](skills/job-apply/webchat/README.md).

See [job-apply README](skills/job-apply/README.md) for full documentation.

---

### code-quality

**Purpose:** Systematic code quality analysis and improvement for TypeScript/React projects.

**Features:**
- Lint, type-check, coverage, duplication, and complexity analysis
- Sprint planning for quality improvements
- Metric tracking over time

**Quick Start:**
```
/code-quality
```

See [code-quality README](skills/code-quality/README.md) for full documentation.

---

### github

**Purpose:** GitHub Wiki management with business model validation and memory-bank integration.

**Features:**
- GitHub Wiki operations with SSH authentication
- Business model validation (B2C/B2B consistency)
- Memory-bank integration for context-aware operations
- Tech stack consistency checking
- Validation scripts for CI/CD integration
- Integration with obra/superpowers for parallel workflows

**Quick Start:**
```bash
# Verify SSH access
ssh -T git@github.com

# Use the skill
/github - Update Wiki with new documentation
/github - Validate business model consistency
/github - Create sprint issues from WBS
```

See [github README](skills/github/README.md) for full documentation.

---

## Skill Development Standards

All skills in this collection follow [Anthropic's Claude Code skill standards](https://docs.anthropic.com/en/docs/claude-code):

- YAML frontmatter with name, description, and scoped tool permissions
- Clear documentation in README.md
- Example configurations and templates
- Validation scripts where applicable

### Creating a New Skill

```
skills/
└── your-skill/
    ├── SKILL.md           # Main skill definition (required)
    ├── README.md          # User documentation (required)
    ├── config.example.yaml # Example configuration (if needed)
    └── ...                # Supporting files
```

---

## Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Add your skill or improvements
4. Ensure documentation is complete
5. Submit a pull request

### Guidelines

- Skills should be self-contained in their directory
- Include clear installation and usage instructions
- Provide example configurations with placeholder data (never real personal data)
- Add validation scripts for complex workflows

---

## License

Apache License 2.0. See the [LICENSE](LICENSE) file at the repo root.

Each skill inherits the repo's Apache 2.0 license unless a skill directory contains its own LICENSE file overriding it.

---

## Related Resources

- [Claude Code Documentation](https://docs.anthropic.com/en/docs/claude-code)
- [Awesome Claude Skills](https://github.com/travisvn/awesome-claude-skills)
- [obra/superpowers](https://github.com/obra/superpowers) - Complementary code development skills

---

**Maintained by:** [PrairieAster.Ai](https://github.com/PrairieAster-Ai)
