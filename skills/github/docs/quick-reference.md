# GitHub Operations Quick Reference Card

## ⚡ Emergency Quick Reference

**Print this and keep handy!**

---

## **🔴 Critical Rule #1: Wiki Authentication**

```bash
# ⚠️ ALWAYS use SSH for Wiki operations
# ✅ CORRECT:
git clone git@github.com:org/repo.wiki.git

# ❌ WRONG (will fail with 403):
git clone https://github.com/org/repo.wiki.git
```

**Verify SSH before Wiki operations**:
```bash
ssh -T git@github.com
# Expected: "Hi username! You've successfully authenticated"
```

---

## **🔴 Critical Rule #2: Security Alerts**

```bash
# ⚠️ Personal Access Tokens cannot access security alerts (HTTP 403)

# ✅ Use GitHub Project Manager MCP instead:
"Show security alerts for this repository"

# Or use Web Interface:
GitHub → Repository → Security → Vulnerability alerts
```

---

## **Tool Selection Cheat Sheet**

| Need to... | Use This | Time |
|------------|----------|------|
| **Edit Wiki** | SSH + Git | 10 min |
| **Security alerts** | GitHub Project Manager MCP | 5 min |
| **Create sprint** | GitHub Project Manager MCP | 15 min |
| **Bulk updates** | GitHub CLI (`gh`) | 5 min |
| **Emergency fix** | GitHub CLI (`gh`) | 2 min |
| **Visual review** | Web Interface | varies |

---

## **Authentication Quick Start**

### **SSH Setup (5 minutes)**
```bash
ssh-keygen -t ed25519 -C "your_email@example.com"
ssh-add ~/.ssh/id_ed25519
cat ~/.ssh/id_ed25519.pub  # Add to GitHub Settings → SSH keys
ssh -T git@github.com  # Verify
```

### **GitHub CLI Setup (3 minutes)**
```bash
gh auth login --scopes "repo,workflow,write:org,read:user,read:project"
gh auth status  # Verify
```

### **GitHub Project Manager MCP (10 minutes)**
Edit `.mcp/claude-desktop-config.json`:
```json
{
  "mcpServers": {
    "github-project-manager": {
      "command": "github-project-manager-mcp",
      "args": ["--project-org", "YourOrg", "--project-name", "ProjectName"],
      "env": {"GITHUB_TOKEN": "your_token"}
    }
  }
}
```
Restart Claude desktop application.

---

## **Common Commands**

### **Wiki Operations**
```bash
# Clone
cd /tmp && git clone git@github.com:org/repo.wiki.git

# Edit, then push
cd repo-wiki
git add . && git commit -m "docs: update"
git push origin master
```

### **Issue Management**
```bash
# Create issue
gh issue create --title "Title" --body "Description"

# List issues
gh issue list --label "bug" --state open

# Close issue
gh issue close 123

# Bulk label
gh issue list --json number --jq '.[].number' | \
  xargs -I {} gh issue edit {} --add-label "sprint-5"
```

### **Release Management**
```bash
# Create release
gh release create v1.0.0 --generate-notes

# List releases
gh release list

# Download asset
gh release download v1.0.0
```

### **Repository Info**
```bash
# View repository
gh repo view

# Clone repository
gh repo clone org/repo

# Repository status
gh repo view --json name,description,url
```

---

## **Troubleshooting Quick Fixes**

### **Wiki Push Fails (403)**
```bash
git remote set-url origin git@github.com:org/repo.wiki.git
ssh -T git@github.com
git push origin master
```

### **Security Alerts Fail (403)**
```bash
# Use MCP instead of CLI
"Show security alerts for this repository"
```

### **GitHub CLI Auth Expired**
```bash
gh auth refresh
# Or re-authenticate
gh auth login
```

### **MCP Server Not Responding**
```bash
# Restart Claude desktop application
# Verify config: cat .mcp/claude-desktop-config.json
# Check token: gh auth status
```

### **Git Asks for Password Repeatedly**
```bash
# Switch to SSH
git remote set-url origin git@github.com:org/repo.git

# Verify SSH agent
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519
```

---

## **Validation Scripts**

```bash
# Wiki content validation
./scripts/validate-wiki.sh /tmp/project-wiki

# Technology stack check
./scripts/check-tech-stack.sh /tmp/project-wiki

# Business model validation
./scripts/verify-business-model.sh /tmp/project-wiki
```

---

## **Time-Saving Aliases**

Add to `~/.bashrc` or `~/.zshrc`:

```bash
# GitHub CLI shortcuts
alias ghi="gh issue"
alias ghil="gh issue list"
alias ghic="gh issue create"
alias ghpr="gh pr"
alias ghprc="gh pr create"
alias ghr="gh repo"
alias ghw="gh workflow"

# Wiki operations
alias wiki-clone="cd /tmp && git clone git@github.com:\$(gh repo view --json nameWithOwner --jq .nameWithOwner).wiki.git"
alias wiki-validate="~/path/to/claude-github-skill/scripts/validate-wiki.sh"

# Common checks
alias gh-verify="ssh -T git@github.com && gh auth status"
```

---

## **Project Manager MCP Commands**

```
# Security
"Show security alerts for this repository"
"Create issues for critical vulnerabilities"
"Check Dependabot status"

# Sprint Planning
"Analyze sprint velocity for last 3 sprints"
"Create new epic for [feature description]"
"Plan next sprint with velocity analysis"

# Issue Management
"Create story: [description]"
"Update project board with current progress"
"Generate sprint status report"

# PRD Generation
"Generate PRD for [capability description]"
```

---

## **Red Flags - Stop and Fix**

⚠️ **STOP if you see**:
- `Permission denied (publickey)` → SSH key not added to GitHub
- `HTTP 403` on Wiki push → Using HTTPS instead of SSH
- `HTTP 403` on security alerts → Use GitHub Project Manager MCP
- `Could not resolve host` → Network issue, check DNS
- `Repository not found` → Check repo name, verify access permissions

---

## **Performance Metrics**

| Operation | Time Without Guide | Time With Guide | Savings |
|-----------|-------------------|-----------------|---------|
| Fix Wiki 403 | 2+ hours | 5 minutes | 115 min |
| Setup MCP | 1+ hour | 15 minutes | 45 min |
| Security Alerts | 1+ hour | 10 minutes | 50 min |
| Sprint Planning | 2+ hours | 45 minutes | 75 min |

**Total Weekly Savings**: 4+ hours per developer

---

## **Help Resources**

### **Documentation**
- GitHub Tools Guide: `docs/github-tools-guide.md`
- Wiki Editing Checklist: `templates/wiki-editing-checklist.md`
- Memory-Bank Integration: `examples/memory-bank-integration.md`

### **Online Resources**
- GitHub CLI Manual: https://cli.github.com/manual/
- GitHub REST API: https://docs.github.com/en/rest
- SSH Troubleshooting: https://docs.github.com/en/authentication/troubleshooting-ssh

### **Support**
- GitHub Status: https://www.githubstatus.com/
- GitHub Community: https://github.community/

---

**Print this page and keep it visible while working with GitHub!**

**Version**: 1.0.0 | **Last Updated**: October 2025
