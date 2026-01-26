# CLAUDE.md Integration Guide

## Overview

This guide shows how to configure your project's `CLAUDE.md` file to work optimally with the GitHub Operations skill.

## What is CLAUDE.md?

`CLAUDE.md` is your project's instruction manual for Claude Code. At session start, Claude reads it to understand:
- Code style and conventions
- Project-specific standards
- Common commands and workflows
- Architecture and patterns

**Location:** Project root (`./CLAUDE.md`)

---

## Recommended CLAUDE.md Section

Add this section to your project's `CLAUDE.md`:

```markdown
## GitHub Operations Standards

This project uses the `claude-github-skill` for all GitHub operations.

### Authentication Configuration

**Wiki Operations (REQUIRED):**
\`\`\`bash
# Verify SSH authentication before Wiki operations
ssh -T git@github.com
# Expected: "Hi username! You've successfully authenticated..."
\`\`\`

**API Operations:**
\`\`\`bash
# Configure GitHub CLI
gh auth login
\`\`\`

### Pre-Push Validation (REQUIRED)

Before publishing any Wiki updates, run all validation scripts:

\`\`\`bash
# Content validation
./.claude/skills/github/scripts/validate-wiki.sh /tmp/[project]-wiki

# Technology stack consistency
./.claude/skills/github/scripts/check-tech-stack.sh /tmp/[project]-wiki

# Business model alignment (investor docs only)
./.claude/skills/github/scripts/verify-business-model.sh /tmp/[project]-wiki
\`\`\`

All scripts must pass before pushing to Wiki.

### Memory-Bank Integration

**Required Files:**
- `memory-bank/quick-reference.json` → Business context, tech stack, red flags
- `memory-bank/skill-config.json` → Validation rules (optional)

**Load Context Before:**
- Documenting features or statistics
- Creating investor-facing documentation
- Making technical architecture claims
- Updating Wiki with cross-references

### Business Model Standards

**Current Focus:** [Load from memory-bank/quick-reference.json]
- Business Focus: {businessFocus}
- Tech Stack: {techStack}
- Revenue Model: {revenueModel}
- NOT Pursuing: {notPursuing[]}

**Red Flags to Avoid:** {redFlags[]}

### Common GitHub Workflows

**Update Wiki Documentation:**
\`\`\`bash
# 1. Clone Wiki via SSH
cd /tmp && git clone git@github.com:[org]/[repo].wiki.git [project]-wiki

# 2. Load memory-bank context
cat memory-bank/quick-reference.json

# 3. Make changes...

# 4. Validate before committing
./.claude/skills/github/scripts/validate-wiki.sh /tmp/[project]-wiki

# 5. Commit and push
cd /tmp/[project]-wiki
git add .
git commit -m "docs: [description]"
git push origin master
\`\`\`

**Create Sprint Issues:**
\`\`\`bash
gh issue create --title "Feature: X" \
  --body "..." \
  --label "sprint-1"
\`\`\`

### Tool Selection Rules

| Task | Tool | Command |
|------|------|---------|
| Wiki push/pull | Git + SSH | `git clone git@github.com:org/repo.wiki.git` |
| Security alerts | GitHub MCP | Via MCP interface |
| Issue/PR operations | GitHub CLI | `gh issue create` / `gh pr create` |

### Error Prevention Checklist

**Before Wiki Operations:**
- [ ] SSH authentication verified
- [ ] Memory-bank loaded
- [ ] Wiki cloned via SSH
- [ ] Cross-references checked
- [ ] Validation scripts passed

**Before Investor Documentation:**
- [ ] Business model header added
- [ ] Business focus verified
- [ ] No contradictory B2B/B2C claims
- [ ] Revenue model clearly stated
```

---

## Project-Specific Examples

### Example 1: Nearest Nice Weather

```markdown
## GitHub Operations Standards

### Business Context
- **Focus:** 100% B2C outdoor recreation discovery
- **Tech Stack:** Vercel + Neon + React
- **NOT Pursuing:** B2B features

### Red Flags
- ❌ Cities appearing instead of parks
- ❌ Hardcoded POI counts (use verification dates)
- ❌ B2B features without "far-future" context

### Validation Rules
\`\`\`json
{
  "validation": {
    "deprecatedTech": ["FastAPI", "Directus"],
    "hardcodedPatterns": ["138 POI", "169 locations"]
  }
}
\`\`\`
```

### Example 2: Portfolio Factory

```markdown
## GitHub Operations Standards

### Business Context
- **Focus:** B2C portfolio showcase
- **Tech Stack:** Vite + React + Vercel

### Red Flags
- ❌ Hardcoded project counts
- ❌ Outdated technology stack in README

### Validation Rules
\`\`\`json
{
  "validation": {
    "deprecatedTech": ["Webpack", "CRA"],
    "hardcodedPatterns": ["[0-9]+ projects"]
  }
}
\`\`\`
```

---

## Testing Your Configuration

### 1. Verify CLAUDE.md is Loaded

```
User: "What are the GitHub operation standards?"
Claude: "According to CLAUDE.md, this project uses claude-github-skill with..."
```

### 2. Test Validation Scripts

```bash
# Create test Wiki checkout
cd /tmp
git clone git@github.com:org/repo.wiki.git test-wiki

# Run validations
./.claude/skills/github/scripts/validate-wiki.sh /tmp/test-wiki
echo $?  # Should be 0 if valid
```

---

## Troubleshooting

**Issue: Claude doesn't load CLAUDE.md**
- Ensure file is named exactly `CLAUDE.md` (case-sensitive)
- Place in project root directory
- Restart Claude session

**Issue: Validation scripts not found**
```bash
# Check skill installation
ls -la .claude/skills/github/scripts/

# Make executable
chmod +x .claude/skills/github/scripts/*.sh
```

**Issue: SSH authentication fails**
```bash
# Test SSH connection
ssh -T git@github.com

# If fails, add SSH key
ssh-keygen -t ed25519
gh ssh-key add ~/.ssh/id_ed25519.pub
```

---

## Best Practices

1. **Keep CLAUDE.md Updated:** Review quarterly
2. **Version Control:** Commit CLAUDE.md and memory-bank/ to git
3. **Test After Changes:** Run validation scripts
4. **Share with Team:** Ensure consistent CLAUDE.md
5. **Integrate with CI/CD:** Run validation in GitHub Actions

---

**Version:** 2.0.0
**Last Updated:** November 2025
