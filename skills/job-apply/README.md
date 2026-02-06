# Job Application Skill for Claude Code

Generate tailored cover letters and resumes optimized for ATS parsing and human scanning, with job fit assessment and style customization.

## Two Ways to Use This Skill

| | **Web Chat** (claude.ai) | **Claude Code CLI** |
|---|---|---|
| **Setup** | Create a Project, upload files | Install Python packages, configure YAML |
| **Cost** | Free tier works | Requires Claude Code subscription |
| **Invoke** | Start a conversation | `/job-apply [job description]` |
| **Output** | .docx download from chat | .docx saved to output directory |
| **Messages** | 3–4 per application | Single slash command |
| **Best for** | Quick start, occasional use | Power users, batch workflows |

---

## Web Chat Quick Start

Use this skill entirely in your browser — no install, no CLI, no Python required. Works on Claude's free tier.

### What You Need

- A [claude.ai](https://claude.ai) account (free tier is fine)
- Your resume as a .docx or .pdf file (or qualifications as text)
- A job description to paste

### Setup (One-Time)

1. Go to [claude.ai](https://claude.ai) and create a new **Project**
2. Upload these files to the Project's knowledge:

   | File | Purpose |
   |------|---------|
   | `SKILL-webchat.md` | Workflow instructions (add as Project instructions) |
   | `generate_word_docs_web.py` | Document generator for the Analysis sandbox |
   | `fit-assessment.md` | Evaluation framework |
   | `style-presets.md` | Visual styling specs |
   | `cover-letter-template.md` | Cover letter structure |
   | `resume-template.md` | Resume structure |
   | `best-practices.md` | Strategic advice |

   **Download all files at once:**

   ```bash
   mkdir -p ~/Downloads/job-apply-webchat && cd ~/Downloads/job-apply-webchat && \
   for f in SKILL-webchat.md generate_word_docs_web.py fit-assessment.md \
            style-presets.md cover-letter-template.md resume-template.md \
            best-practices.md; do
     curl -sO "https://raw.githubusercontent.com/PrairieAster-Ai/claude-code-skills/main/skills/job-apply/$f"
   done && echo "Downloaded $(ls | wc -l) files to $(pwd)"
   ```

   Or browse the files in [`skills/job-apply/`](./) and download individually.

### First Run

1. Start a new conversation in your Project
2. Upload your resume (.docx) and paste the job description
3. Claude will parse both, show a fit assessment, and ask to proceed
4. Confirm, and Claude generates .docx cover letter + resume for download

**Typical message count: 3–4 messages** (upload → assessment → confirm → delivery).

### Returning Users — Portable Profile

After your first run, Claude offers to generate a `profile.yaml` file. Download and save it. On future runs:

1. Upload `profile.yaml` + paste a new job description
2. Claude skips resume parsing (saves a message) and goes straight to fit assessment

The `profile.yaml` works with both the web chat and CLI versions of this skill.

### Tips for Free Tier

- **PDF and .docx both work** — Claude reads PDF text directly; .docx is extracted via code execution
- **Save your `profile.yaml`** after the first run to reduce message count on future applications
- **Paste the full job description** directly into chat rather than describing it
- **Say "Yes" or "Proceed"** to the fit assessment to avoid spending a message on elaboration

---

## CLI Quick Start

For full automation with Claude Code's slash command interface.

### Features

- **Guided Setup**: First-time users are walked through configuration with simple questions
- **Auto-Install Dependencies**: Detects missing packages and offers to install them
- **Job Fit Assessment**: Scores your qualifications against job requirements with detailed gap analysis
- **Portfolio Integration**: Automatically includes achievements from your coding projects
- **Style Presets**: Classic, Modern Professional, or Creative styling based on industry
- **WCAG AA Accessible**: High-contrast colors for readability
- **Word Document Output**: Professional .docx files preferred by recruiters
- **Auto-Open Output**: Opens the folder with your documents after generation
- **Application History**: Tracks what jobs you've applied to

### Requirements

- **Python 3.8+** (tested on 3.8, 3.9, 3.10, 3.11, 3.12)
- **python-docx** >= 0.8.11
- **pyyaml** >= 5.0

### 1. Install Prerequisites

**On Linux:**
```bash
pip3 install python-docx pyyaml --user
```

**On macOS (Sonoma, Ventura, or Homebrew Python):**

Due to PEP 668, macOS now protects system Python from pip modifications. Use one of these methods:

```bash
# Recommended: Use a virtual environment
python3 -m venv ~/.claude-venv
source ~/.claude-venv/bin/activate
pip install python-docx pyyaml

# Add to your shell profile (~/.zshrc or ~/.bashrc) to auto-activate:
# source ~/.claude-venv/bin/activate
```

**On Windows:**

```cmd
pip install python-docx pyyaml
```

Or use a virtual environment (recommended):

```cmd
python -m venv %USERPROFILE%\.claude-venv
%USERPROFILE%\.claude-venv\Scripts\activate.bat
pip install python-docx pyyaml
```

**Verify installation:**

Linux/macOS:
```bash
python3 -c "import docx; import yaml; print('Dependencies OK')"
```

Windows:
```cmd
python -c "import docx; import yaml; print('Dependencies OK')"
```

### 2. Set Up Your Configuration

Copy the example config:

```bash
cp ~/.claude/skills/job-apply/config.example.yaml ~/.claude/skills/job-apply/config.yaml
```

### 3. Import Your Qualifications

**Option A: Interactive Wizard (Recommended)**
```bash
python3 ~/.claude/skills/job-apply/import_resume.py
```
This walks you through entering your contact info, work history, skills, certifications, and education.

**Option B: Import from Existing Resume**
```bash
# From Word document
python3 ~/.claude/skills/job-apply/import_resume.py ~/Documents/resume.docx

# From text file
python3 ~/.claude/skills/job-apply/import_resume.py ~/Documents/resume.txt
```

**Option C: Manual Edit**

Edit `config.yaml` directly with your:
- Contact information (name, phone, email, LinkedIn)
- Professional summary
- Skills by category
- Work experience with achievements
- Certifications
- Education
- Portfolio projects

### 4. Run the Skill

In Claude Code, use the slash command with a job description:

```
/job-apply [paste job description here]
```

Or reference a file:

```
/job-apply path/to/job-description.txt
```

## Configuration

### config.yaml Structure

```yaml
candidate:
  name: "Your Full Name"
  phone: "555.123.4567"
  email: "your.email@example.com"
  linkedin: "linkedin.com/in/yourprofile"
  calendar: ""  # Optional

paths:
  resume_locations:
    - "~/Documents/Job Application Docs/resume/"
    - "~/Documents/resume/"
    - "~/Documents/"
  portfolio_dir: "~/Projects/"
  output_dir: "~/Documents/Job Application Docs/generated/"

preferences:
  default_style: "modern_professional"  # classic, modern_professional, creative

# Your work history and credentials (use import_resume.py to populate)
qualifications:
  summary: "2-3 sentence professional summary..."

  skills:
    - category: "Programming Languages"
      items: "Python, JavaScript, TypeScript"
    - category: "Tools"
      items: "JIRA, Git, Docker"

  experience:
    - title: "Senior Developer"
      company: "Company Name"
      dates: "Jan 2020 - Present"
      bullets:
        - text: "Led team of 5 engineers to deliver platform"
          highlights: ["5 engineers"]  # Phrases to bold

  certifications:
    - name: "AWS Solutions Architect"
      year: "2023"
      issuer: "Amazon"

  education:
    - degree: "BS Computer Science"
      school: "University Name"

# Code projects demonstrating skills
portfolio_projects:
  - name: "Project Name"
    url: "https://project-url.com"
    description: "Brief description"
    technologies:
      - "React"
      - "TypeScript"
    achievements:
      - metric: "80% improvement"
        description: "What you improved"
    keywords:
      - "full-stack"
      - "API integration"
```

### Adding Portfolio Projects

Portfolio projects provide evidence for technical skills. For each project, include:

- **name**: Project name
- **url**: Live URL (if deployed)
- **repo**: GitHub repository URL
- **description**: 1-2 sentence description
- **technologies**: List of technologies used
- **achievements**: Quantified results with metrics
- **keywords**: Skills and concepts demonstrated

## Workflow

1. **Phase 0**: Check dependencies (auto-install if missing) and configuration (guided setup for new users)
2. **Phase 1**: Gather resume and portfolio materials
3. **Phase 2**: Assess job fit with scoring
4. **Phase 3**: Select style preset based on industry
5. **Phase 4**: Match experience to requirements
6. **Phase 5**: Generate Word documents
7. **Phase 6**: Open output folder, log application, show summary with interview prep

### First-Time Experience

New users are guided through setup with simple questions:
1. Enter your name and contact info
2. Choose your target industry (determines document style)
3. Optionally import an existing resume

No manual YAML editing required!

## Style Presets

| Preset | Best For | Accent Color |
|--------|----------|--------------|
| Classic | Finance, Law, Healthcare, Government | Navy Blue |
| Modern Professional | Tech, Corporate, Consulting | Navy Blue |
| Creative | Design, Marketing, Startups | Industry-dependent |

All presets use WCAG AA accessible colors (4.5:1+ body text, 3:1+ large text). Default colors exceed 7:1.

## Output Files

Documents are saved to your configured output directory:

```
{FirstName}_{LastName}_Cover_Letter_{Role}_{Company}.docx
{FirstName}_{LastName}_Resume_{Role}_{Company}.docx
```

## File Structure

```
~/.claude/skills/job-apply/
├── SKILL.md                  # Skill definition (Claude Code CLI)
├── SKILL-webchat.md          # Skill definition (claude.ai web chat)
├── README.md                 # This file
├── config.yaml               # Active configuration (CLI)
├── config.example.yaml       # Example configuration template
├── generate_word_docs.py     # Word document generator (CLI)
├── generate_word_docs_web.py # Word document generator (web chat sandbox)
├── import_resume.py          # Resume import wizard
├── profiles.py               # Profile switching utility
├── profiles/                 # Saved user profiles
│   └── *.yaml
├── best-practices.md         # Strategic application advice
├── style-presets.md          # Visual styling specifications
├── fit-assessment.md         # Job fit evaluation framework
├── cover-letter-template.md  # Cover letter structure
└── resume-template.md        # Resume structure
```

## Profile Management

Switch between user profiles to test onboarding or maintain multiple configurations.

```bash
# List all saved profiles
python3 ~/.claude/skills/job-apply/profiles.py list

# Show current profile info
python3 ~/.claude/skills/job-apply/profiles.py current

# Save current config as a named profile
python3 ~/.claude/skills/job-apply/profiles.py save myprofile

# Switch to a saved profile
python3 ~/.claude/skills/job-apply/profiles.py switch myprofile

# Test new user onboarding (removes config.yaml)
python3 ~/.claude/skills/job-apply/profiles.py new

# Delete a profile
python3 ~/.claude/skills/job-apply/profiles.py delete oldprofile
```

### Testing New User Experience

```bash
# 1. Save your current config
python3 ~/.claude/skills/job-apply/profiles.py save myname

# 2. Switch to new user state
python3 ~/.claude/skills/job-apply/profiles.py new

# 3. Test /job-apply - it will trigger onboarding

# 4. Switch back to your profile
python3 ~/.claude/skills/job-apply/profiles.py switch myname
```

## Troubleshooting

### "python-docx not found" or "ModuleNotFoundError: No module named 'docx'"

**On Linux:**
```bash
pip3 install python-docx pyyaml --user
```

**On macOS - "externally-managed-environment" error:**

This error occurs on macOS Sonoma/Ventura or with Homebrew Python due to PEP 668 protection.

```bash
# Solution 1: Use a virtual environment (recommended)
python3 -m venv ~/.claude-venv
source ~/.claude-venv/bin/activate
pip install python-docx pyyaml

# Solution 2: Override protection (not recommended for system Python)
pip3 install python-docx pyyaml --break-system-packages
```

If using a virtual environment, remember to activate it before running the skill:
```bash
source ~/.claude-venv/bin/activate
```

Or add this line to your `~/.zshrc` (or `~/.bashrc`):
```bash
source ~/.claude-venv/bin/activate
```

### "No config.yaml found"

Copy the example config:
```bash
cp ~/.claude/skills/job-apply/config.example.yaml ~/.claude/skills/job-apply/config.yaml
```

### Documents look different than expected

Check that you're opening .docx files in Microsoft Word or a compatible application. Some viewers may not render all formatting.

### macOS: "python3: command not found"

Install Python 3 via Homebrew:
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
brew install python
```

Or install from [python.org](https://www.python.org/downloads/).

### macOS: Permission denied or path issues

If you see errors with paths containing spaces (like "Job Application Docs"), ensure paths are properly quoted in any manual shell commands:
```bash
# Correct:
ls ~/Documents/"Job Application Docs"/generated/

# Incorrect (will fail):
ls ~/Documents/Job Application Docs/generated/
```

### Windows: "python" or "python3" not found

On Windows, Python is typically invoked as `python` (not `python3`). If neither works:

1. Install Python from [python.org](https://www.python.org/downloads/)
2. During installation, check "Add Python to PATH"
3. Restart your terminal

You can also use the Python Launcher:
```cmd
py -3 --version
py -3 -m pip install python-docx pyyaml
```

### Windows: Path issues with `~`

The `~` shortcut for home directory works in Python but not in Windows Command Prompt. Use the full path:

```cmd
:: Instead of ~/.claude/skills/job-apply/
%USERPROFILE%\.claude\skills\job-apply\

:: Or use PowerShell which supports ~
```

### Verify your setup

**Linux/macOS:**
```bash
# Check Python
python3 --version

# Check dependencies
python3 -c "import docx; import yaml; print('Dependencies: OK')"

# Check config exists
ls ~/.claude/skills/job-apply/config.yaml && echo "Config: OK" || echo "Config: MISSING"
```

**Windows (Command Prompt):**
```cmd
:: Check Python
python --version

:: Check dependencies
python -c "import docx; import yaml; print('Dependencies: OK')"

:: Check config exists
if exist "%USERPROFILE%\.claude\skills\job-apply\config.yaml" (echo Config: OK) else (echo Config: MISSING)
```

**Windows (PowerShell):**
```powershell
# Check Python
python --version

# Check dependencies
python -c "import docx; import yaml; print('Dependencies: OK')"

# Check config exists
Test-Path ~/.claude/skills/job-apply/config.yaml
```

## Known Limitations

- **PDF resumes (CLI only)**: Not supported for automatic parsing in Claude Code CLI. Convert to .docx or .txt first. (Web chat handles PDFs natively.)
- **Clipboard input**: Not implemented. Paste job description directly or save to a file.
- **Non-Latin scripts**: Filenames support Unicode, but some special characters may be removed for cross-platform compatibility.

## Contributing

To share this skill with others:

1. Ensure `config.yaml` is in `.gitignore` (contains personal info)
2. Include `config.example.yaml` as a template
3. Document any additional portfolio project schemas

## License

MIT License - Feel free to adapt for your own use.
