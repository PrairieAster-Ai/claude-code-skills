# Job Application Skill for Claude Code

Generate tailored cover letters and resumes optimized for ATS parsing and human scanning, with job fit assessment and style customization.

## Features

- **Job Fit Assessment**: Scores your qualifications against job requirements with detailed gap analysis
- **Portfolio Integration**: Automatically includes achievements from your coding projects
- **Style Presets**: Classic, Modern Professional, or Creative styling based on industry
- **WCAG AA Accessible**: High-contrast colors for readability
- **Word Document Output**: Professional .docx files preferred by recruiters

## Quick Start

### 1. Install Prerequisites

```bash
pip3 install python-docx pyyaml --user
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

### 3. Run the Skill

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
    - "~/Documents/resume/"
  portfolio_dir: "~/Projects/"
  output_dir: "~/Documents/Job Applications/generated/"

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

1. **Phase 0**: Check for configuration (first-time setup if needed)
2. **Phase 1**: Gather resume and portfolio materials
3. **Phase 2**: Assess job fit with scoring
4. **Phase 3**: Select style preset based on industry
5. **Phase 4**: Match experience to requirements
6. **Phase 5**: Generate Word documents
7. **Phase 6**: Output summary with interview prep notes

## Style Presets

| Preset | Best For | Accent Color |
|--------|----------|--------------|
| Classic | Finance, Law, Healthcare, Government | Navy Blue |
| Modern Professional | Tech, Corporate, Consulting | Navy Blue |
| Creative | Design, Marketing, Startups | Industry-dependent |

All presets use WCAG AA accessible colors with 7:1+ contrast ratios.

## Output Files

Documents are saved to your configured output directory:

```
{FirstName}_{LastName}_Cover_Letter_{Role}_{Company}.docx
{FirstName}_{LastName}_Resume_{Role}_{Company}.docx
```

## File Structure

```
~/.claude/skills/job-apply/
├── SKILL.md              # Main skill definition
├── README.md             # This file
├── config.yaml           # Active configuration
├── config.example.yaml   # Example configuration template
├── generate_word_docs.py # Word document generator
├── import_resume.py      # Resume import wizard
├── profiles.py           # Profile switching utility
├── profiles/             # Saved user profiles
│   └── *.yaml
├── style-presets.md      # Visual styling specifications
├── fit-assessment.md     # Job fit evaluation framework
├── cover-letter-template.md
└── resume-template.md
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

### "python-docx not found"

Install the dependency:
```bash
pip3 install python-docx --user
```

### "No config.yaml found"

Copy the example config:
```bash
cp ~/.claude/skills/job-apply/config.example.yaml ~/.claude/skills/job-apply/config.yaml
```

### Documents look different than expected

Check that you're opening .docx files in Microsoft Word or a compatible application. Some viewers may not render all formatting.

## Contributing

To share this skill with others:

1. Ensure `config.yaml` is in `.gitignore` (contains personal info)
2. Include `config.example.yaml` as a template
3. Document any additional portfolio project schemas

## License

MIT License - Feel free to adapt for your own use.
