---
name: job-apply
description: Assess job fit and generate tailored cover letter and resume for a job application based on job description, existing resume, and portfolio projects. Includes fit scoring, style presets, and gap analysis.
argument-hint: "[job-description-text or 'clipboard' or path-to-job-file]"
allowed-tools: Read, Glob, Grep, Bash, Write, Task, AskUserQuestion
---

# Job Application Document Generator

Evaluate job fit, then generate a tailored cover letter (1 page max) and resume (1-2 pages, prefer 1) optimized for both ATS parsing and human scanning, with visual styling appropriate for the target industry.

## Input

Job Description: $ARGUMENTS

## Workflow

### Phase 0: Configuration Check

**First, check for user configuration:**

1. **Look for config file** at `~/.claude/skills/job-apply/config.yaml`

2. **If config exists**, load:
   - Candidate information (name, phone, email, linkedin, calendar)
   - Path preferences (resume locations, portfolio dir, output dir)
   - Style preferences
   - Portfolio projects with achievements and technologies

3. **If config does NOT exist**, run first-time setup:
   - Inform user: "This appears to be your first time using the job-apply skill. Let me set up your profile."
   - Copy `config.example.yaml` to `config.yaml`
   - Use AskUserQuestion to gather:
     - Full name
     - Phone number
     - Email address
     - LinkedIn URL
     - Calendar link (optional)
   - Save to config.yaml
   - Ask if they want to:
     - Import qualifications from an existing resume file
     - Enter qualifications manually
     - Add portfolio projects

4. **Resume Import Options** (for new users):
   - **Interactive wizard**: `python3 ~/.claude/skills/job-apply/import_resume.py`
   - **From Word document**: `python3 ~/.claude/skills/job-apply/import_resume.py resume.docx`
   - **From text file**: `python3 ~/.claude/skills/job-apply/import_resume.py resume.txt`

---

### Phase 1: Gather Source Materials

1. **Load candidate info from config.yaml**
   - Name, phone, email, LinkedIn, calendar link

2. **Load qualifications from config.yaml** (preferred):
   - `qualifications.summary`: Professional summary
   - `qualifications.skills`: Skills by category
   - `qualifications.experience`: Work history with achievements
   - `qualifications.certifications`: Professional certifications
   - `qualifications.education`: Degrees and schools

3. **If qualifications not in config**, find and parse existing resume:
   - Search configured locations (or defaults):
     - `~/Documents/Job Application Docs/resume/`
     - `~/Documents/resume/`
     - Current project directory
   - Look for `.docx`, `.pdf`, or `.md` files with "resume" in the name
   - For `.docx` files, extract text using: `unzip -p "file.docx" word/document.xml | sed -e 's/<[^>]*>//g' | tr -s '[:space:]' '\n'`
   - **Recommend** user run import wizard to save qualifications: `python3 ~/.claude/skills/job-apply/import_resume.py`

4. **Load portfolio projects from config.yaml**:
   - Each project includes: name, url, description, technologies, achievements, keywords
   - Match project technologies and keywords against job requirements
   - Use achievement metrics as evidence for qualifications

5. **If portfolio projects not in config**, scan `~/Projects/` for evidence:
   - Search for README.md files, package.json, and source code
   - Look for qualification assessments in `~/Documents/Job Application Docs/`
   - Identify technologies, frameworks, and quantifiable achievements

6. **Parse job description** to extract:
   - Required skills and experience (must-haves)
   - Preferred qualifications (nice-to-haves)
   - Technical stack (cloud platforms, tools, languages)
   - Soft skills and culture fit indicators
   - Industry/domain context
   - Years of experience requirements

---

### Phase 2: Job Fit Assessment

See [fit-assessment.md](fit-assessment.md) for complete evaluation framework.

#### Step 1: Categorize Requirements

**Must-Have Signals:** "Required", "Must possess", "Essential", "Minimum qualifications", first 5 listed requirements

**Nice-to-Have Signals:** "Preferred", "Bonus", "Would be nice", "Ideal candidate", "Plus"

#### Step 2: Build T-Chart Evaluation

For each requirement, evaluate candidate evidence:

| Requirement | Evidence | Rating |
|-------------|----------|--------|
| {Requirement 1} | {Specific evidence from resume/portfolio} | ✅ Strong / ⚠️ Partial / ❌ Gap |
| {Requirement 2} | {Evidence or transferable skill} | Rating |
| ... | ... | ... |

**Evidence Sources:**
- Work history from resume
- Portfolio project achievements (from config.yaml)
- Certifications
- Education

**Scoring:**
- ✅ Strong match = 1.0 point
- ⚠️ Partial/transferable = 0.5 points
- ❌ Gap = 0 points

#### Step 3: Calculate Fit Scores

```
Must-Have Score = (Must-have points / Must-have count) × 100
Nice-to-Have Score = (Nice-to-have points / Nice-to-have count) × 100
Overall Score = (Must-Have Score × 0.7) + (Nice-to-Have Score × 0.3)
```

#### Step 4: Check for Disqualifiers

**Non-negotiable gaps (do not proceed):**
- Missing legally required credentials (licenses, certifications required by law)
- Missing the core technical skill the role is built around
- Experience gap > 10 years (they want 15, you have 3)
- Security clearance requirements you cannot meet

#### Step 5: Generate Recommendation

| Overall Score | Must-Have Score | Recommendation |
|---------------|-----------------|----------------|
| 80%+ | 80%+ | **Strong Fit** - Proceed with application |
| 60-79% | 70%+ | **Good Fit** - Proceed, address gaps in cover letter |
| 50-59% | 60%+ | **Stretch Fit** - Consider if you have referral or compelling narrative |
| Below 50% | Below 60% | **Poor Fit** - Recommend focusing on better-matched opportunities |

#### Step 6: Present Assessment to User

Display fit assessment summary:

```
## Job Fit Assessment

**Role:** {Job Title}
**Company:** {Company if known}

### Fit Scores
- Must-Have Requirements: {X}% ({Y}/{Z} requirements)
- Nice-to-Have Requirements: {X}% ({Y}/{Z} requirements)
- Overall Fit Score: {X}%

### Recommendation: {Strong Fit / Good Fit / Stretch Fit / Poor Fit}

### Strengths (Direct Matches)
- {Requirement}: {Your evidence}
- ...

### Portfolio Project Matches
- {Project Name}: Demonstrates {skill} with {metric}
- ...

### Gaps to Address
- {Requirement}: {Gap description} → {Mitigation strategy}
- ...

### Disqualifiers Found: {None / List any}
```

**Ask user to confirm:**
```
Based on this assessment, would you like to:
- Proceed with application (generate documents)
- See detailed gap analysis
- Skip this opportunity
```

---

### Phase 3: Determine Style Preset

See [style-presets.md](style-presets.md) for complete styling specifications.

**Check config.yaml for default_style preference first.**

**Auto-detect industry from job description, or ask user to confirm:**

| Industry Signals | Recommended Preset |
|------------------|-------------------|
| Finance, Banking, Law, Government, Healthcare, Insurance | **Classic** |
| Tech, Corporate, Consulting, Enterprise Software, B2B | **Modern Professional** |
| Design, Marketing, Advertising, Startups, Agency, Creative | **Creative** |

**If ambiguous, ask user:**
```
Which style best fits this role?
- Classic (conservative industries: finance, law, healthcare)
- Modern Professional (corporate, tech, consulting)
- Creative (design, marketing, startups)
```

---

### Phase 4: Match and Prioritize

1. **Map candidate experience to job requirements**:
   - Lead with strongest matches to must-haves
   - Identify transferable skills for partial matches
   - Prepare gap mitigation language for cover letter

2. **Select strongest evidence** for each key requirement:
   - Quantified achievements (percentages, dollar amounts, team sizes)
   - Recent and relevant project examples
   - Certifications that directly apply

3. **Match portfolio projects to requirements**:
   - For each relevant portfolio project from config.yaml:
     - Match technologies to job's technical requirements
     - Match keywords to job description language
     - Select most impressive achievement metrics
   - Prioritize projects with strongest alignment to must-have requirements
   - Include portfolio URLs in resume where appropriate

4. **Identify keywords** from job description for ATS optimization

5. **Select accent color** based on preset and industry:
   - See color recommendations in [style-presets.md](style-presets.md)

6. **Craft gap mitigation statements** for cover letter:
   - Frame gaps as growth opportunities
   - Highlight transferable skills
   - Show learning velocity with examples
   - Reference portfolio projects that demonstrate rapid skill acquisition

---

### Phase 5: Generate Documents

Create both files in configured output directory (default: `~/Documents/Job Application Docs/generated/`).

**Primary output format: Microsoft Word (.docx)** - preferred by recruiters and ATS systems.

#### Word Document Generation

Use the Python script at `~/.claude/skills/job-apply/generate_word_docs.py` to create styled Word documents.

**Prerequisites:** Ensure python-docx is installed:
```bash
pip3 install python-docx --user
```

**Script Usage:**
```python
from generate_word_docs import generate_application_documents

generate_application_documents(
    candidate={
        "name": "Full Name",
        "phone": "Phone",
        "email": "Email",
        "linkedin": "LinkedIn URL",
        "calendar": "Calendar link (optional)",
        "title": "Target Role Title"
    },
    job={
        "title": "Job Title",
        "company": "Company Name",
        "location": "Location"
    },
    cover_letter={
        "opening": "Opening paragraph text...",
        "sections": [
            {
                "title": "Section Title",
                "paragraphs": [
                    {"label": "Bold Label", "text": "Content...", "highlights": ["phrase to bold"]},
                    ["Bullet item 1", "Bullet item 2"]
                ]
            }
        ],
        "closing": "Best regards,",
        "signature_title": "Title | Specialty"
    },
    resume={
        "summary": "Summary paragraph...",
        "skills": [{"category": "Category", "items": "Skill1, Skill2, Skill3"}],
        "experience": [
            {
                "title": "Job Title",
                "company": "Company",
                "dates": "Mon YYYY - Mon YYYY",
                "bullets": [
                    {"text": "Achievement with metric", "highlights": ["metric"]}
                ]
            }
        ],
        "certifications": [{"name": "Cert Name", "detail": "Year"}],
        "education": [{"degree": "Degree, Major", "school": "University"}]
    },
    output_dir="~/Documents/Job Application Docs/generated/"
)
```

#### Cover Letter Requirements

See [cover-letter-template.md](cover-letter-template.md) for structure.
Apply styling from selected preset in [style-presets.md](style-presets.md).

**Key principles:**
- Single page maximum
- Opening paragraph: Hook with most relevant qualification
- Body: 2-3 paragraphs with specific evidence mapped to requirements
- **Address significant gaps proactively** with transferable skills or learning examples
- **Reference portfolio projects** when they demonstrate relevant skills
- Technical alignment section if role is technical
- Closing: Express genuine interest and availability
- No generic phrases ("I am writing to apply...")
- Every claim backed by specific evidence

#### Resume Requirements

See [resume-template.md](resume-template.md) for structure.
Apply styling from selected preset in [style-presets.md](style-presets.md).

**ATS Optimization:**
- Use standard section headers: Summary, Skills, Experience, Education, Certifications
- Include exact keywords from job description
- Use consistent date formatting (Mon YYYY - Mon YYYY)
- Keep creative elements in header only; main content follows standard format
- Use bullet points with action verbs

**Human Scanning Optimization:**
- Apply visual hierarchy through typography (bold, sizing)
- Use accent color strategically (headers, dividers, name)
- Quantified achievements prominently displayed
- Most relevant experience emphasized first within each role
- Single line spacing for compact documents; adequate margins (0.7-1 inch)

**Portfolio Project Integration:**
- Include relevant portfolio projects in experience or separate "Projects" section
- For each included project:
  - Project name with URL (if live)
  - Brief description aligned to job requirements
  - Key achievement metric
  - Technologies used (matching job requirements)

---

### Phase 6: Output

1. Save files with naming convention:
   - `{FirstName}_{LastName}_Cover_Letter_{Role_Keywords}_{Company}.docx`
   - `{FirstName}_{LastName}_Resume_{Role_Keywords}_{Company}.docx`
   - Also save `.md` versions for reference/editing if requested

2. Provide comprehensive summary to user:

```
## Application Summary

### Fit Assessment
- Overall Score: {X}%
- Recommendation: {Strong/Good/Stretch Fit}

### Documents Generated
- Cover Letter: {full path}.docx
- Resume: {full path}.docx

### Style Applied
- Preset: {Classic/Modern Professional/Creative}
- Accent Color: {Color name} ({hex code})
- Contrast: WCAG AA accessible (7:1+ ratio)

### Key Matches Highlighted
- {Top 3-5 strongest qualification matches}

### Portfolio Projects Referenced
- {Project name}: Used to demonstrate {skill}

### Gaps Addressed in Cover Letter
- {Gap}: {How it was addressed}

### Interview Preparation Notes
- Be ready to discuss: {Gap areas they may probe}
- Emphasize: {Your strongest differentiators}
- Portfolio demos: {Projects to show if asked}
```

3. Offer next steps:
   - Documents ready to upload to job portals
   - Interview prep suggestions based on gaps
   - Suggest portfolio pieces to reference
