# Wiki Editing Pre-Flight Checklist

Use this checklist before making any Wiki edits to ensure quality and consistency.

## ✅ Authentication

- [ ] SSH authentication verified: `ssh -T git@github.com`
- [ ] NOT using fine-grained GitHub token (will fail with 403)

## ✅ Context Loading

- [ ] Memory-bank business context loaded (if available)
- [ ] Quick reference reviewed for current business model
- [ ] Recent changes/lessons checked

## ✅ Data Validation (if documenting statistics)

- [ ] Production API endpoint tested
- [ ] Current counts/metrics verified
- [ ] Generic phrasing used (NOT hardcoded numbers)
- [ ] Validation date documented

Example:
```bash
curl -s "https://production-url/api/endpoint?limit=1" | jq '.count'
```

## ✅ Technology Stack (if documenting architecture)

- [ ] Current tech stack verified from codebase
- [ ] Searched Wiki for deprecated technology references
- [ ] All instances updated OR deprecation warnings added

Search commands:
```bash
cd /tmp/[project]-wiki
grep -r "FastAPI" .
grep -r "PostGIS" .
grep -r "[deprecated-tech]" .
```

## ✅ Business Model Alignment (investor-facing docs)

- [ ] Business model explicitly stated
- [ ] No contradictory claims (B2C vs B2B)
- [ ] Future possibilities clearly marked as such
- [ ] Professional tone and structure

Template:
```markdown
## Business Model

**Current Focus**: 100% B2C [description]

**NOT Pursuing**: [Alternative model] features are far-future only
```

## ✅ Cross-Reference Check

- [ ] Searched for related terms across Wiki
- [ ] Identified all pages needing updates
- [ ] Updated all occurrences OR documented exceptions

Command:
```bash
grep -r "[term-being-updated]" .
```

## ✅ Content Quality

- [ ] Professional writing (spell-check, grammar)
- [ ] Clear structure (headings, bullets, code blocks)
- [ ] Accurate technical claims
- [ ] Proper citation of sources

## ✅ Deprecation (if removing/replacing content)

- [ ] Added deprecation warning (DON'T just delete)
- [ ] Linked to replacement documentation
- [ ] Listed specific outdated claims
- [ ] Included deprecation date

## ✅ Commit Message

- [ ] Descriptive commit message
- [ ] Includes validation steps performed
- [ ] References related issues/PRs if applicable

Format:
```
docs: [one-line summary]

[Detailed description of changes]
[Validation performed: API endpoint tested, cross-references updated, etc.]
[Related issues: #123]
```

## ✅ Post-Commit

- [ ] Wiki changes visible on GitHub
- [ ] Links working correctly
- [ ] Images/assets loading properly
- [ ] No broken formatting

---

**Checklist Version**: 1.0.0
**Source**: Lessons learned from October 2025 Wiki audit
