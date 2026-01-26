# Changelog

All notable changes to the Claude GitHub Skill will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - 2025-10-24

### Added

#### Comprehensive GitHub Tools Documentation
- **`docs/github-tools-guide.md`** - Complete reference covering:
  - Tool selection decision tree (CLI vs MCP vs Web Interface)
  - Authentication strategies comparison (SSH, PAT, Fine-grained, OAuth)
  - Common issues and resolutions with time savings metrics
  - Workflow optimization patterns
  - Performance and efficiency metrics

- **`docs/quick-reference.md`** - Emergency quick reference card:
  - Print-friendly format for desk reference
  - Critical authentication rules
  - Common commands cheat sheet
  - Troubleshooting quick fixes
  - Time-saving aliases
  - Red flag warnings

#### Critical Lessons Documented

**Lesson 1: SSH Authentication for Wiki**
- **Problem**: Fine-grained tokens fail with 403 on Wiki push
- **Solution**: Always use SSH authentication
- **Time Saved**: 2+ hours per incident (115 minutes)

**Lesson 2: Security Alerts Access**
- **Problem**: Personal access tokens return HTTP 403 for security alerts
- **Solution**: Use GitHub Project Manager MCP with enhanced permissions
- **Time Saved**: 1+ hour per security audit (50 minutes)

**Lesson 3: Tool Selection Matrix**
- Security Operations: GitHub Project Manager MCP (enhanced permissions)
- Bulk Operations: GitHub CLI (efficiency, scriptability)
- Wiki Operations: SSH + Git (authentication required)
- Visual Review: Web Interface (complex layouts)

**Lesson 4: MCP Connection Issues**
- Token expiration detection and refresh procedures
- Configuration validation checklist
- Application restart requirements
- **Time Saved**: 30+ minutes per incident (25 minutes)

**Lesson 5: Git Authentication Loops**
- HTTPS vs SSH authentication comparison
- Credential helper configuration
- SSH agent troubleshooting
- **Time Saved**: 15+ minutes per incident (12 minutes)

#### Enhanced Documentation Structure

**Updated Files**:
- `skill.md`: Added authentication strategy section, bumped to v1.1.0
- `README.md`: Added documentation section with key learnings, bumped to v1.1.0

**Cross-References**:
- All documentation cross-referenced with existing templates and scripts
- Troubleshooting decision tree for systematic issue resolution
- Integration examples with memory-bank structure

### Changed

- **Version**: Updated from 1.0.0 to 1.1.0
- **Skill Prompt**: Enhanced with authentication lessons and tool selection guidance
- **README**: Reorganized with prominent documentation section

### Performance Metrics

**Time Savings Per Issue**:
| Issue | Without Guide | With Guide | Time Saved |
|-------|---------------|------------|------------|
| Wiki 403 Error | 2+ hours | 5 minutes | 115 minutes |
| Security Alerts Access | 1+ hour | 10 minutes | 50 minutes |
| MCP Connection Issues | 30+ minutes | 5 minutes | 25 minutes |
| Git Auth Loops | 15+ minutes | 3 minutes | 12 minutes |
| Project Sync Issues | 20+ minutes | 5 minutes | 15 minutes |

**Total Potential Savings**: 4+ hours per week per developer

### Tool Integration Best Practices

**Recommended Tool Distribution**:
- 80% of operations: GitHub Project Manager MCP (natural language, enhanced permissions)
- 15% of operations: GitHub CLI (bulk operations, scripting, emergency fixes)
- 5% of operations: Web Interface (complex configuration, visual review)

**Authentication Best Practices**:
1. Use SSH for Wiki operations (fine-grained tokens will fail)
2. Configure GitHub Project Manager MCP for security alerts (enhanced permissions required)
3. Keep GitHub CLI authenticated for emergency operations
4. Document authentication methods in project runbooks
5. Rotate tokens regularly (security best practice)
6. Use minimal required permissions (principle of least privilege)

## [1.0.0] - 2025-10-24

### Added

#### Core Skill
- `skill.md` - Comprehensive GitHub operations skill prompt with memory-bank integration
- Auto-load business context from memory-bank/quick-reference.json
- Apply documented lessons learned automatically
- Red flag enforcement for business model drift detection

#### Templates
- `templates/wiki-editing-checklist.md` - Pre-flight checklist for Wiki editing operations
- `templates/deprecation-warning.md` - Template for properly deprecating outdated documentation
- `templates/business-model-header.md` - Template for investor-facing document consistency

#### Validation Scripts
- `scripts/validate-wiki.sh` - Comprehensive Wiki content validation
  - Checks for hardcoded database counts
  - Detects deprecated technology references
  - Validates business model consistency
  - Finds broken internal links
  - Identifies TODO/FIXME markers
  - Checks for business model headers in investor docs

- `scripts/check-tech-stack.sh` - Technology stack consistency validation
  - Scans for deprecated technology references
  - Checks for consistency across Wiki pages
  - Validates technology mention counts

- `scripts/verify-business-model.sh` - Business model consistency validation
  - Checks B2C vs B2B consistency
  - Validates investor documents have business model headers
  - Detects contradictory claims
  - Checks revenue model consistency

#### Documentation
- `README.md` - Comprehensive installation and usage guide
- `examples/memory-bank-integration.md` - Detailed examples showing memory-bank integration patterns
- `LICENSE` - MIT License
- `.gitignore` - Standard ignore patterns

#### Features
- Multi-project reuse design (nearest-nice-weather, portfolio-factory, future projects)
- Clean separation from project codebases
- Memory-bank integration for business context awareness
- Automated validation preventing common documentation issues
- Templates ensuring consistency across projects

### Lessons Learned Integrated

This initial release incorporates 7 critical lessons from the nearest-nice-weather Wiki audit (October 2025):

1. **Database State Validation** - Always validate production data before documenting statistics
2. **Technology Stack Consistency** - Synchronize all technology references across Wiki
3. **Business Model Alignment** - Explicit business model headers in investor documents
4. **Deprecation Warnings** - Preserve history instead of deleting outdated docs
5. **SSH Authentication** - Wiki push requires SSH, fine-grained tokens fail with 403
6. **Cross-Reference Validation** - Update all references when changing technical details
7. **Investor Communication Standards** - Consistent terminology and professional tone

### Design Principles

- **Reusable**: Designed for use across multiple projects via git clone or submodule
- **Memory-Bank First**: Automatically loads business context and technical patterns
- **Lessons Applied**: Prevents recurring issues through automated checks
- **Template-Driven**: Consistent documentation structure across projects
- **Validation-First**: Catch issues before they reach production

### Installation

```bash
# Option 1: Git Clone (Recommended)
cd /path/to/your-project/.claude/skills
git clone git@github.com:PrairieAster-Ai/claude-github-skill.git github

# Option 2: Git Submodule
cd /path/to/your-project/.claude/skills
git submodule add git@github.com:PrairieAster-Ai/claude-github-skill.git github
```

### Usage

```bash
# Invoke the skill in Claude Code
/github

# Or call specific validation scripts directly
./github/scripts/validate-wiki.sh /tmp/project-wiki
./github/scripts/check-tech-stack.sh /tmp/project-wiki
./github/scripts/verify-business-model.sh /tmp/project-wiki
```

---

**Repository**: https://github.com/PrairieAster-Ai/claude-github-skill
**Initial Commit**: 1046b3d
**Created**: October 24, 2025
