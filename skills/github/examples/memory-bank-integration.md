# Memory-Bank Integration Examples

This document shows how the GitHub skill integrates with project memory-bank structures.

## Example 1: Nearest Nice Weather Project

### Memory-Bank Structure

```
memory-bank/
├── quick-reference.json          # Essential business context
├── business-context/
│   ├── business-model.md
│   └── red-flags.md
├── technical-patterns/
│   ├── successful-patterns.md
│   └── anti-patterns.md
└── session-handoffs/
    └── session-handoff-template.md
```

### Quick Reference Example

```json
{
  "businessFocus": "B2C outdoor recreation",
  "techStack": "Vercel + Neon + React",
  "primaryTable": "poi_locations",
  "redFlags": [
    "Cities appearing instead of parks",
    "B2B features being developed"
  ]
}
```

### How Skill Uses This Context

When the GitHub skill is invoked:

1. **Auto-loads** `memory-bank/quick-reference.json`
2. **Applies red flags** when reviewing Wiki edits or issue creation
3. **Uses tech stack** to validate technology consistency across Wiki
4. **References business focus** when checking investor documentation

### Example: Wiki Edit with Memory-Bank Context

```bash
# User: "Update the Wiki with our POI statistics"

# Skill automatically:
# 1. Loads quick-reference.json
# 2. Sees primaryTable: "poi_locations"
# 3. Validates production data: curl https://prod/api/poi-locations?limit=1
# 4. Uses generic phrasing: "Minnesota outdoor recreation POI database"
# 5. Adds verification date
# 6. Checks for "cities" red flag
```

## Example 2: Portfolio Factory Project

### Memory-Bank Structure

```
memory-bank/
├── quick-reference.json
├── business-context/
│   ├── target-market.md
│   └── revenue-model.md
└── wiki-content/
    └── lessons-learned.md
```

### Quick Reference Example

```json
{
  "businessFocus": "B2B SaaS document automation",
  "techStack": "Next.js + Supabase + Vercel",
  "revenueModel": "subscription",
  "notPursuing": ["B2C consumer features"]
}
```

### Example: Issue Creation with Business Context

```bash
# User: "Create issue for new consumer-facing feature"

# Skill automatically:
# 1. Loads quick-reference.json
# 2. Sees notPursuing: ["B2C consumer features"]
# 3. Warns: "⚠️ This conflicts with documented business model: B2B focus only"
# 4. Asks user to confirm or clarify business model change
```

## Example 3: Using Lessons Learned

### Project Lessons in Memory-Bank

```markdown
# memory-bank/wiki-content/lessons-learned.md

## Lesson: Authentication Method

**Problem**: Fine-grained GitHub tokens failed with 403 on Wiki push
**Solution**: Use SSH authentication only for Wiki operations
**Impact**: 2 hours lost debugging
**Prevention**: Auto-check SSH auth before Wiki operations
```

### How Skill Applies This

```bash
# User: "Update the Wiki documentation"

# Skill automatically:
# 1. Checks for memory-bank/wiki-content/lessons-learned.md
# 2. Reads authentication lesson
# 3. Runs: ssh -T git@github.com BEFORE attempting Wiki clone
# 4. If SSH fails: Reports error with lesson context
# 5. If SSH succeeds: Proceeds with Wiki operation
```

## Example 4: Technology Stack Validation

### Memory-Bank Context

```json
{
  "techStack": "Vercel Functions + Neon PostgreSQL",
  "deprecatedTech": [
    "FastAPI",
    "Docker Compose",
    "Local PostgreSQL"
  ]
}
```

### Example: Cross-Reference Check

```bash
# User: "Update Architecture page with database info"

# Skill automatically:
# 1. Loads memory-bank context
# 2. Sees deprecatedTech includes "FastAPI"
# 3. Searches Wiki for FastAPI references: grep -r "FastAPI" /tmp/project-wiki
# 4. Finds 5 outdated references
# 5. Suggests: "Update all 5 FastAPI references or add deprecation warnings"
# 6. Provides file list and line numbers
```

## Example 5: Business Model Consistency

### Memory-Bank Context

```json
{
  "businessFocus": "100% B2C ad-supported platform",
  "targetMarket": "Minneapolis metro casual users",
  "notPursuing": ["B2B tourism operators", "Premium subscriptions"]
}
```

### Example: Investor Document Update

```bash
# User: "Update Executive Summary in Wiki"

# Skill automatically:
# 1. Detects "Executive Summary" is investor-facing document
# 2. Loads business model from memory-bank
# 3. Checks for business model header
# 4. If missing: Adds header using templates/business-model-header.md
# 5. Populates with memory-bank context:
#    - Current Focus: 100% B2C ad-supported platform
#    - Target Market: Minneapolis metro casual users
#    - NOT Pursuing: B2B tourism operators, premium subscriptions
```

## Integration Best Practices

### 1. Maintain Quick Reference

Always keep `memory-bank/quick-reference.json` up-to-date:

```json
{
  "businessFocus": "Current business model",
  "techStack": "Current technology stack",
  "redFlags": ["Things to watch for"],
  "notPursuing": ["Explicitly excluded features"]
}
```

### 2. Document Lessons Learned

After resolving issues, document them:

```markdown
## Lesson: [Problem Title]

**Problem**: What went wrong
**Root Cause**: Why it happened
**Solution**: How we fixed it
**Impact**: Time/cost of issue
**Prevention**: How to avoid in future
```

### 3. Use Consistent Structure

The skill looks for these files in priority order:

1. `memory-bank/quick-reference.json` - Essential context
2. `memory-bank/business-context/` - Business model details
3. `memory-bank/technical-patterns/` - Technical guidelines
4. `memory-bank/wiki-content/lessons-learned.md` - Wiki-specific lessons

### 4. Red Flag Enforcement

Define clear red flags that trigger warnings:

```json
{
  "redFlags": [
    "Cities appearing instead of parks",
    "B2B features in B2C project",
    "Mock data in production",
    "Hardcoded database counts"
  ]
}
```

The skill will automatically check for these patterns and warn before proceeding.

## Troubleshooting

### Memory-Bank Not Loading

If the skill doesn't use memory-bank context:

```bash
# Verify structure exists
ls -la memory-bank/quick-reference.json

# Verify JSON is valid
jq . memory-bank/quick-reference.json

# Check file permissions
chmod 644 memory-bank/quick-reference.json
```

### Red Flags Not Triggering

If red flags aren't being caught:

```bash
# Check red flags are defined
jq '.redFlags' memory-bank/quick-reference.json

# Verify they're specific enough
# ❌ BAD: "wrong data"
# ✅ GOOD: "cities appearing in poi_locations table"
```

### Lessons Learned Not Applied

If past lessons aren't being used:

```bash
# Verify lessons file exists
ls -la memory-bank/wiki-content/lessons-learned.md

# Check lesson structure follows pattern
grep "## Lesson:" memory-bank/wiki-content/lessons-learned.md
```

---

**Version**: 1.0.0
**Purpose**: Demonstrate memory-bank integration patterns for Claude GitHub skill
