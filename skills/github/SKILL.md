---
name: github
description: Manage GitHub Wiki and GitHub Projects for the current repo. Knows the authentication quirks for each (SSH for Wiki push, OAuth scopes for Projects).
allowed-tools: "Bash(git:*),Bash(gh:*),Bash(ssh:*),Read,Write,Edit,Grep,Glob"
---

# GitHub Wiki & Projects Skill

Assists with GitHub Wiki editing and GitHub Project board management for the current repository.

## Authentication Reference

GitHub uses **three different auth mechanisms** depending on the operation. Getting these wrong produces confusing 403 errors.

| Operation | Auth method | Notes |
|-----------|------------|-------|
| Wiki **read** (clone) | SSH or HTTPS | Either works |
| Wiki **push** | SSH only | Fine-grained PATs get 403. Always use `git@github.com:` URL. |
| Issues, PRs, releases | `gh` CLI | Uses the OAuth token from `gh auth login` |
| GitHub Projects (boards) | `gh` CLI + `project` scope | Requires `gh auth refresh -s read:project,project` first |

### Before Wiki operations

```bash
# Verify SSH works
ssh -T git@github.com

# Derive the wiki URL from the current repo
REPO_URL=$(git remote get-url origin | sed 's/\.git$/.wiki.git/' | sed 's|https://github.com/|git@github.com:|')
git clone "$REPO_URL" /tmp/$(basename $(git rev-parse --show-toplevel))-wiki
```

### Before GitHub Projects operations

The default `gh` OAuth token lacks project scopes. If `gh project list` fails with a scopes error, tell the user:

> Your `gh` token needs the `project` scope. Run:
> ```
> gh auth refresh -s read:project,project
> ```

## Wiki Workflow

1. **Clone** the wiki into `/tmp/<project>-wiki` using SSH URL
2. **Edit** markdown files
3. **Validate** — check for broken links, TODO markers, stale content
4. **Commit and push** from the wiki checkout

```bash
cd /tmp/<project>-wiki
git add .
git commit -m "docs: <description>"
git push origin master
```

Wiki repos have a single `master` branch and no PR workflow — commits push directly.

## GitHub Projects Workflow

Detect the repo owner from `gh repo view`:

```bash
OWNER=$(gh repo view --json owner --jq '.owner.login')

# List projects
gh project list --owner "$OWNER"

# View a project
gh project view <number> --owner "$OWNER"

# Add an issue to a project
gh project item-add <project-number> --owner "$OWNER" --url <issue-url>
```

## Common Pitfalls

- **Wiki push 403**: You used HTTPS or a fine-grained token. Switch to SSH.
- **Project scope error**: Run `gh auth refresh -s read:project,project`.
- **Wiki branch confusion**: Wiki repos use `master`, not `main`.
- **Stale wiki clone**: Always `git pull` before editing if the clone already exists.
