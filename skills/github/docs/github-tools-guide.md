# GitHub Tools & Authentication Guide

## 🎯 Complete Reference for GitHub Operations

This guide covers tool selection, authentication strategies, common issues, and resolutions for GitHub operations across CLI, MCP servers, and web interfaces.

---

## **📊 Tool Selection Decision Tree**

### **When to Use GitHub CLI (`gh`)**

✅ **RECOMMENDED FOR:**
- **Wiki management** - Full CRUD operations on repository wikis (SSH required)
- **Release management** - Creating releases, tags, changelog generation
- **CI/CD operations** - Workflow management, action status checks
- **Emergency fixes** - Quick hotfixes, security patches, critical updates
- **Bulk operations** - Mass issue updates, label management, automation
- **Repository administration** - Settings, collaborators, branch protection

✅ **STRENGTHS:**
- Direct command-line efficiency for power users
- Complete GitHub API coverage
- Scriptable and automatable
- Works offline after initial authentication
- Perfect for CI/CD pipelines

⚠️ **LIMITATIONS:**
- **Security alerts access restricted** - Personal access tokens have limited permissions
- Requires terminal/command-line comfort
- Less intuitive for non-technical stakeholders

**Setup Time**: 5 minutes | **Learning Curve**: Medium

### **When to Use GitHub Project Manager MCP**

✅ **RECOMMENDED FOR:**
- **Sprint planning** - Epic, story, and task creation with proper hierarchy
- **Issue management** - Creating, updating, and tracking development work
- **Project coordination** - Roadmap planning, velocity tracking, backlog management
- **PRD generation** - Product requirement document creation and management
- **Security alert management** - Enhanced permissions for vulnerability tracking
- **Cross-functional collaboration** - Stakeholder communication and alignment

✅ **STRENGTHS:**
- **Enhanced security permissions** - Access to vulnerability alerts and Dependabot data
- Natural language interface for non-technical users
- Integrated project management workflows
- Real-time collaboration capabilities
- Automated project field management

⚠️ **LIMITATIONS:**
- Requires MCP server configuration
- Learning curve for advanced features
- May have rate limiting for high-volume operations

**Setup Time**: 15 minutes | **Learning Curve**: Low

### **When to Use Official GitHub MCP**

✅ **RECOMMENDED FOR:**
- **Backup operations** - When Project Manager MCP is unavailable
- **Basic repository tasks** - File operations, commit history, branch management
- **Simple issue operations** - Basic CRUD operations without project integration
- **Repository exploration** - Code search, file browsing, history review

✅ **STRENGTHS:**
- Stable and reliable
- Lower resource requirements
- Simple operations interface

⚠️ **LIMITATIONS:**
- **Limited security features** - Same token restrictions as GitHub CLI
- Basic functionality compared to specialized MCPs
- No advanced project management features

**Setup Time**: 10 minutes | **Learning Curve**: Low

### **When to Use Web Interface**

✅ **RECOMMENDED FOR:**
- **Visual project management** - Project boards, roadmaps, complex views
- **Security settings** - Repository security configuration, access control
- **Complex form operations** - Issue templates, pull request reviews
- **Administrative tasks** - Organization settings, team management
- **Visual diff review** - Code review, merge conflict resolution

**Setup Time**: 0 minutes | **Learning Curve**: Low

---

## **🔐 Authentication Strategies**

### **Authentication Method Comparison**

| Method | Best For | Setup Complexity | Security Level | Permissions |
|--------|----------|------------------|----------------|-------------|
| **SSH Keys** | Wiki operations, daily git work | Medium | High | Full repo access |
| **Personal Access Token (Classic)** | CLI automation, scripting | Low | Medium | Configurable scopes |
| **Fine-Grained Token** | Project-specific access | Medium | High | Granular permissions |
| **GitHub App** | Organization-wide automation | High | Highest | Org-level control |
| **OAuth** | MCP servers, third-party tools | Medium | High | App-specific scopes |

### **SSH Authentication Setup**

**CRITICAL FOR**: Wiki push operations (fine-grained tokens will fail with 403)

```bash
# Generate SSH key if needed
ssh-keygen -t ed25519 -C "your_email@example.com"

# Start SSH agent
eval "$(ssh-agent -s)"

# Add SSH key to agent
ssh-add ~/.ssh/id_ed25519

# Copy public key to clipboard
cat ~/.ssh/id_ed25519.pub

# Add to GitHub: Settings → SSH and GPG keys → New SSH key

# Verify authentication
ssh -T git@github.com
```

**Expected output**: "Hi username! You've successfully authenticated..."

### **Personal Access Token (Classic) Setup**

**BEST FOR**: GitHub CLI, general automation

```bash
# Generate token: GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)

# Required scopes for full functionality:
✅ repo (Full control of private repositories)
✅ workflow (Update GitHub Action workflows)
✅ write:org (Read and write org and team membership)
✅ read:user (Read ALL user profile data)
✅ read:project (Read project data)

# ⚠️ LIMITATION: Cannot access security alerts (HTTP 403)
```

**Authenticate GitHub CLI**:
```bash
gh auth login --scopes "repo,workflow,write:org,read:user,read:project"
```

### **Fine-Grained Token Setup**

**BEST FOR**: Repository-specific operations, enhanced security

```bash
# Generate token: GitHub → Settings → Developer settings → Personal access tokens → Fine-grained tokens

# ⚠️ WIKI LIMITATION: Fine-grained tokens CANNOT push to Wiki
# Reason: Wiki uses separate repository that's not included in fine-grained permissions

# Use Cases:
✅ Repository-specific automation
✅ Temporary access grants
✅ Read-only operations
✅ API operations (non-Wiki)

❌ Wiki push operations (use SSH instead)
❌ Cross-repository bulk operations
```

### **GitHub Project Manager MCP Authentication**

**BEST FOR**: Security alert access, project management, enhanced permissions

**Configuration** (`.mcp/claude-desktop-config.json`):
```json
{
  "mcpServers": {
    "github-project-manager": {
      "command": "github-project-manager-mcp",
      "args": [
        "--project-org", "YourOrg",
        "--project-name", "YourProjectName"
      ],
      "env": {
        "GITHUB_TOKEN": "your_token_with_enhanced_permissions"
      }
    }
  }
}
```

**Required Token Permissions**:
- Repository: Full control
- **Security: Read access to vulnerability alerts** (key advantage over CLI)
- Projects: Read/write access
- Organization: Read access for team management

---

## **🔴 Common Issues & Resolutions**

### **Issue 1: Wiki Push Fails with 403 Error**

**Symptoms**:
```bash
git push origin master
# remote: Permission to user/repo.wiki.git denied to user.
# fatal: unable to access 'https://github.com/user/repo.wiki.git/': The requested URL returned error: 403
```

**Root Cause**: Using fine-grained GitHub token or HTTPS authentication for Wiki operations

**Solution**:
```bash
# Switch to SSH authentication
cd /tmp/project-wiki

# Check current remote URL
git remote get-url origin
# If HTTPS: https://github.com/org/repo.wiki.git

# Switch to SSH
git remote set-url origin git@github.com:org/repo.wiki.git

# Verify SSH authentication
ssh -T git@github.com

# Retry push
git push origin master
```

**Prevention**: Always use SSH for Wiki operations, document in runbooks

**Time Saved**: 2+ hours per incident

---

### **Issue 2: Security Alerts Return HTTP 403**

**Symptoms**:
```bash
gh api repos/org/repo/vulnerability-alerts
# HTTP 403: Not Found (insufficient permissions)
```

**Root Cause**: Personal access tokens lack enhanced security permissions

**Solution**:
```bash
# Option 1: Use GitHub Project Manager MCP (recommended)
# Configure MCP server with enhanced token permissions

# Option 2: Use Web Interface
# Navigate to: GitHub → Repository → Security → Vulnerability alerts

# Option 3: Use npm audit for dependency vulnerabilities
npm audit --json > security-audit.json
```

**When to Use Each**:
- **GitHub Project Manager MCP**: Automated security workflows, issue creation
- **Web Interface**: Manual triage, policy configuration
- **npm audit**: Local development, pre-commit checks

**Time Saved**: 1+ hour per security audit

---

### **Issue 3: MCP Server Connection Failures**

**Symptoms**:
- MCP server not responding
- Authentication failures
- Timeout errors

**Root Causes & Solutions**:

**1. Token Expiration**:
```bash
# Check token validity
gh auth status

# Refresh authentication
gh auth refresh

# Or regenerate token on GitHub
```

**2. Configuration Errors**:
```json
// Verify .mcp/claude-desktop-config.json syntax
{
  "mcpServers": {
    "github-project-manager": {
      "command": "github-project-manager-mcp",  // ✅ Correct command
      "args": ["--project-org", "OrgName"],    // ✅ Valid args format
      "env": {
        "GITHUB_TOKEN": "ghp_xxxxxxxxxxxxx"    // ✅ Valid token format
      }
    }
  }
}
```

**3. Application Restart Required**:
```bash
# Restart Claude desktop application after config changes
# macOS: Cmd+Q then relaunch
# Linux: killall claude-desktop && claude-desktop &
# Windows: Task Manager → End Claude → Restart
```

**Time Saved**: 30+ minutes per incident

---

### **Issue 4: Git Authentication Loops**

**Symptoms**:
- Repeatedly prompted for username/password
- Authentication succeeds but push fails
- Credential helper not working

**Solutions**:

**For HTTPS (not recommended for Wiki)**:
```bash
# Configure credential helper
git config --global credential.helper store

# Or use SSH instead (recommended)
git remote set-url origin git@github.com:org/repo.git
```

**For SSH**:
```bash
# Verify SSH agent is running
ssh-add -l

# If "Could not open a connection to your authentication agent"
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519

# Verify GitHub connection
ssh -T git@github.com
```

**Time Saved**: 15+ minutes per incident

---

### **Issue 5: Project Board Sync Issues**

**Symptoms**:
- GitHub Project not reflecting current repository state
- Issues missing from project board
- Custom field values not updating

**Root Causes & Solutions**:

**1. Project-Repository Link Broken**:
```bash
# Use GitHub Project Manager MCP
"Refresh project data and reconnect to repository"

# Or via Web Interface:
# Project → Settings → Manage access → Verify repository connection
```

**2. Automation Rules Disabled**:
```bash
# Check automation status
# Project → Settings → Workflows → Verify workflows are enabled

# Common workflow issues:
# - "Auto-add" workflow not configured for new issues
# - Status field not mapped to issue state
# - Custom field validation rules too restrictive
```

**3. Field Configuration Mismatch**:
```bash
# Verify field mappings
# Project → Settings → Fields → Check field types and options

# Common issues:
# - Status field missing required options
# - Sprint field not configured for project
# - Priority field values don't match issue labels
```

**Time Saved**: 20+ minutes per incident

---

## **📋 Common Task Quick Reference**

### **Security Management**

| Task | Recommended Tool | Command/Action | Time Saved |
|------|------------------|----------------|------------|
| **View vulnerability alerts** | GitHub Project Manager MCP | "Show security alerts for this repository" | 15 min |
| **Triage security issues** | GitHub Project Manager MCP | "Create issues for critical vulnerabilities" | 30 min |
| **Update dependencies** | GitHub CLI + npm audit | `npm audit fix` → `gh pr create` | 10 min |
| **Monitor Dependabot** | GitHub Project Manager MCP | "Check Dependabot status and configure batching" | 20 min |
| **Security policy setup** | Web Interface | GitHub → Settings → Security & analysis | 5 min |

### **Wiki Operations**

| Task | Recommended Tool | Command/Action | Authentication |
|------|------------------|----------------|----------------|
| **Clone Wiki** | GitHub CLI | `git clone git@github.com:org/repo.wiki.git` | SSH required |
| **Edit Wiki pages** | Text editor | Edit .md files locally | - |
| **Push Wiki changes** | Git | `git push origin master` | SSH required |
| **Create Wiki page** | GitHub CLI | `gh api repos/:owner/:repo/wiki/pages -X POST` | PAT or SSH |
| **Delete Wiki page** | Web Interface | Wiki → Edit → Delete page | Web login |

**⚠️ CRITICAL**: Always use SSH for Wiki push operations

### **Issue Management**

| Task | Recommended Tool | Command/Action | Best For |
|------|------------------|----------------|----------|
| **Create epic/story** | GitHub Project Manager MCP | "Create new epic for [feature]" | Sprint planning |
| **Bulk label updates** | GitHub CLI | `gh issue list \| xargs gh issue edit --add-label` | Maintenance |
| **Sprint planning** | GitHub Project Manager MCP | "Plan next sprint with velocity analysis" | Team coordination |
| **Project roadmap** | Web Interface | Projects → Roadmap view | Stakeholder updates |
| **Close stale issues** | GitHub CLI | `gh issue list --state open --label stale \| xargs gh issue close` | Cleanup |

### **Repository Operations**

| Task | Recommended Tool | Command/Action | Use Case |
|------|------------------|----------------|----------|
| **Release management** | GitHub CLI | `gh release create v1.0.0 --generate-notes` | Versioning |
| **Branch protection** | Web Interface | Settings → Branches → Add rule | Security |
| **Workflow management** | GitHub CLI | `gh workflow run` | CI/CD |
| **Tag creation** | GitHub CLI | `gh api repos/:owner/:repo/git/tags -X POST` | Version control |

---

## **⚡ Workflow Optimization Patterns**

### **Security-First Development Workflow**

**Daily Security Check** (5 minutes):
```bash
# 1. Check new alerts (GitHub Project Manager MCP)
"Show new security alerts since yesterday"

# 2. Run local audit
npm audit --json > daily-audit.json

# 3. Triage critical issues
"Create GitHub issues for critical npm vulnerabilities"
```

**Weekly Security Planning** (30 minutes):
```bash
# 1. Comprehensive security review
npm audit
npm outdated

# 2. Create remediation plan
"Analyze security vulnerabilities and create sprint tasks"

# 3. Schedule dependency updates
# Use GitHub Project Manager MCP for sprint planning
```

**Monthly Security Review** (60 minutes):
```bash
# 1. Trend analysis
"Generate security trends report for last 30 days"

# 2. Policy updates
# Review and update security policies via Web Interface

# 3. Team training
# Document lessons learned, update runbooks
```

### **Efficient Wiki Management Workflow**

**Pre-Flight Checklist**:
```bash
# 1. Verify SSH authentication
ssh -T git@github.com

# 2. Clone Wiki to temporary directory
cd /tmp
git clone git@github.com:org/repo.wiki.git project-wiki
cd project-wiki

# 3. Load business context (if using memory-bank)
cat /path/to/project/memory-bank/quick-reference.json

# 4. Make edits
# Edit .md files

# 5. Validate changes (use validation scripts)
../claude-github-skill/scripts/validate-wiki.sh .

# 6. Commit and push
git add .
git commit -m "docs: [description]"
git push origin master

# 7. Verify on GitHub
# Check Wiki on GitHub web interface
```

**Time**: 10-15 minutes per Wiki update

### **Sprint Planning Workflow**

**Using GitHub Project Manager MCP** (45 minutes):
```bash
# 1. Velocity analysis
"Analyze sprint velocity for last 3 sprints"

# 2. Capacity planning
"Calculate team capacity for next sprint"

# 3. Epic breakdown
"Break down epic: [feature name] into stories"

# 4. Task creation
"Create sprint tasks with proper labels and estimates"

# 5. Project board setup
"Update project board with new sprint items"
```

**Using GitHub CLI for Bulk Operations** (15 minutes):
```bash
# 1. Create milestone
gh api repos/:owner/:repo/milestones -X POST -f title="Sprint 5"

# 2. Bulk assign to milestone
gh issue list --json number --jq '.[].number' | \
  xargs -I {} gh issue edit {} --milestone "Sprint 5"

# 3. Add sprint label
gh issue list --json number --jq '.[].number' | \
  xargs -I {} gh issue edit {} --add-label "sprint-5"
```

---

## **🎯 Tool Integration Best Practices**

### **Recommended Tool Distribution**

- **80% of operations**: GitHub Project Manager MCP (natural language, enhanced permissions)
- **15% of operations**: GitHub CLI (bulk operations, scripting, emergency fixes)
- **5% of operations**: Web Interface (complex configuration, visual review)

### **Golden Rules for Tool Selection**

1. **Security Operations**: Always use GitHub Project Manager MCP for enhanced permissions
2. **Bulk Operations**: GitHub CLI for efficiency and scriptability
3. **Visual Operations**: Web Interface for complex layouts and stakeholder presentations
4. **Emergency Response**: GitHub CLI for speed, Web Interface for verification
5. **Stakeholder Communication**: GitHub Project Manager MCP for content generation
6. **Wiki Operations**: Always use SSH authentication with GitHub CLI

### **Authentication Best Practices**

1. **Use SSH for Wiki operations** - Fine-grained tokens will fail
2. **Configure GitHub Project Manager MCP for security alerts** - Enhanced permissions required
3. **Keep GitHub CLI authenticated** - For emergency operations
4. **Document authentication methods** - In project runbooks
5. **Rotate tokens regularly** - Security best practice
6. **Use minimal required permissions** - Principle of least privilege

---

## **📊 Performance & Efficiency Metrics**

### **Time Savings by Tool**

| Tool | Setup Investment | Weekly Time Saved | ROI Break-Even |
|------|------------------|-------------------|----------------|
| **GitHub Project Manager MCP** | 15 min | 2-3 hours | Day 1 |
| **GitHub CLI** | 5 min | 1-2 hours | Day 1 |
| **Validation Scripts** | 10 min | 30-60 min | Week 1 |
| **SSH Authentication** | 10 min | 2+ hours | First Wiki edit |

### **Common Issue Resolution Times**

| Issue | Without Guide | With Guide | Time Saved |
|-------|---------------|------------|------------|
| Wiki 403 Error | 2+ hours | 5 minutes | 115 minutes |
| Security Alerts Access | 1+ hour | 10 minutes | 50 minutes |
| MCP Connection Issues | 30+ minutes | 5 minutes | 25 minutes |
| Git Auth Loops | 15+ minutes | 3 minutes | 12 minutes |
| Project Sync Issues | 20+ minutes | 5 minutes | 15 minutes |

**Total Potential Time Savings**: 4+ hours per week per developer

---

## **🔧 Troubleshooting Decision Tree**

```
Issue Category?
│
├─ Authentication
│  ├─ SSH fails → Check ssh-agent, verify key added to GitHub
│  ├─ Token expired → gh auth refresh or regenerate token
│  └─ MCP connection → Restart application, verify config
│
├─ Wiki Operations
│  ├─ Push fails 403 → Switch to SSH authentication
│  ├─ Clone fails → Verify SSH key, check repository access
│  └─ Content issues → Run validation scripts
│
├─ Security Alerts
│  ├─ HTTP 403 → Use GitHub Project Manager MCP or Web Interface
│  ├─ No alerts shown → Verify security features enabled in repo settings
│  └─ False positives → Use MCP to dismiss with reason
│
├─ Project Board
│  ├─ Sync issues → Refresh project data via MCP
│  ├─ Missing issues → Check automation rules
│  └─ Field problems → Verify field configuration
│
└─ General GitHub
   ├─ Rate limiting → Use authentication, reduce request frequency
   ├─ Permission denied → Check token scopes, verify org access
   └─ API errors → Check GitHub status page, retry with backoff
```

---

## **📚 Additional Resources**

### **Documentation**
- [GitHub CLI Manual](https://cli.github.com/manual/)
- [GitHub REST API](https://docs.github.com/en/rest)
- [GitHub Projects Documentation](https://docs.github.com/en/issues/planning-and-tracking-with-projects)

### **Related Skill Files**
- `templates/wiki-editing-checklist.md` - Wiki editing pre-flight checklist
- `scripts/validate-wiki.sh` - Automated Wiki validation
- `examples/memory-bank-integration.md` - Memory-bank integration patterns

---

**Version**: 1.0.0
**Last Updated**: October 2025
**Purpose**: Comprehensive GitHub operations guide with tool selection, authentication, and troubleshooting
