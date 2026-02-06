# Claude Code Skills

A collection of reusable skills for [Claude Code](https://docs.anthropic.com/en/docs/claude-code), Anthropic's official CLI for Claude.

## Available Skills

| Skill | Description | Invoke With |
|-------|-------------|-------------|
| [**job-apply**](skills/job-apply/) | Generate tailored cover letters and resumes with job fit assessment | `/job-apply [job description]` |
| [**code-quality**](skills/code-quality/) | Code quality assessment and improvement for TypeScript/React projects | `/code-quality` |
| [**github**](skills/github/) | GitHub Wiki management, business model validation, and memory-bank integration | `/github` |

---

## Installation

### Option 1: Install Individual Skills

Copy a specific skill to your project's `.claude/skills/` directory:

```bash
# Install job-apply skill
git clone https://github.com/PrairieAster-Ai/claude-code-skills.git /tmp/claude-code-skills
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

MIT License - See individual skill directories for specific licenses.

---

## Related Resources

- [Claude Code Documentation](https://docs.anthropic.com/en/docs/claude-code)
- [Awesome Claude Skills](https://github.com/travisvn/awesome-claude-skills)
- [obra/superpowers](https://github.com/obra/superpowers) - Complementary code development skills

---

**Maintained by:** [PrairieAster.Ai](https://github.com/PrairieAster-Ai)
