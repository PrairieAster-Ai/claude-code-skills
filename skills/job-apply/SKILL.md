---
name: job-apply
description: Assess job fit and generate tailored cover letter and resume for a job application based on job description, existing resume, and portfolio projects. Includes fit scoring, style presets, and gap analysis.
argument-hint: "[job-description-text or path-to-job-file]"
allowed-tools: "Bash,Read,Write,Edit,Glob,Grep,Task,AskUserQuestion"
---

# Job Application Document Generator

Evaluate job fit, then generate a tailored cover letter (1 page max) and resume (1-2 pages, prefer 1) optimized for both ATS parsing and human scanning, with visual styling appropriate for the target industry.

## Input

Job Description: $ARGUMENTS

## Workflow

### Phase 0: Configuration and Dependency Check

#### Step 0.1: Check and Auto-Install Dependencies

Run this check:
```bash
python3 -c "import docx; import yaml; print('OK')" 2>&1 || echo "MISSING"
```

**If dependencies are missing**, offer to install them automatically:

Use AskUserQuestion:
```
I need to install python-docx and pyyaml to generate Word documents.

Options:
- "Install now" - I'll run the install command for you
- "Show me the command" - I'll show you what to run manually
- "Skip" - Continue without installing (will fail at document generation)
```

**If user chooses "Install now"**, run the appropriate command:

On Linux:
```bash
pip3 install python-docx pyyaml --user
```

On macOS (try standard install first, fall back to break-system-packages):
```bash
pip3 install python-docx pyyaml --user 2>&1 || pip3 install python-docx pyyaml --break-system-packages
```

On Windows:
```cmd
pip install python-docx pyyaml
```

Verify installation succeeded, then continue.

#### Step 0.2: Check for User Configuration

**Look for config file** at `~/.claude/skills/job-apply/config.yaml`

**If config exists**, load and continue to Phase 1.

**If config does NOT exist**, run the guided first-time setup (Step 0.3).

#### Step 0.3: Guided First-Time Setup (New Users Only)

Welcome the user:
> "Welcome to the Job Application skill! Let's set up your profile. This takes about 2 minutes and you only need to do it once."

**Gather contact information using AskUserQuestion:**

Question 1 - Name:
```
What is your full name (as it should appear on your resume)?
```
(Free text input)

Question 2 - Contact Method:
```
How should employers contact you?
Options:
- "Phone and Email" - Provide both
- "Email only" - Just email address
- "Email + LinkedIn" - Email and LinkedIn profile
```

Question 3 - Based on previous answer, gather:
- Phone number (if selected)
- Email address
- LinkedIn URL (if selected)

Question 4 - Style preference:
```
What industry are you targeting?
Options:
- "Tech/Corporate" - Modern Professional style (recommended for most roles)
- "Finance/Law/Healthcare" - Classic conservative style
- "Design/Marketing/Startups" - Creative style with more personality
```

**Create config.yaml with the gathered information:**

Use Write tool to create `~/.claude/skills/job-apply/config.yaml` with:
```yaml
candidate:
  name: "{gathered_name}"
  phone: "{gathered_phone}"
  email: "{gathered_email}"
  linkedin: "{gathered_linkedin}"
  calendar: ""

paths:
  output_dir: "~/Documents/Job Applications/"

preferences:
  default_style: "{selected_style}"

qualifications:
  summary: ""
  skills: []
  experience: []
  certifications: []
  education: []

portfolio_projects: []
```

**Ask about existing resume:**

Use AskUserQuestion:
```
Do you have an existing resume to import?
Options:
- "Yes, import from file" - I'll help you import your work history
- "No, I'll add details later" - Start with basic profile, add experience manually
- "Yes, let me paste it" - Paste your resume text and I'll parse it
```

**If importing from file:**
- Ask for the file path
- Use the import_resume.py logic to parse and populate qualifications
- Confirm what was imported

**Confirm setup complete:**
> "Profile created! Your documents will be saved to ~/Documents/Job Applications/. You can edit your full work history anytime by running `/job-apply-setup`."

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
   - Look for `.docx` or `.md` files with "resume" in the name
   - For `.docx` files, use Python's zipfile to extract text (cross-platform, no external dependencies)
   - Note: PDF files are not currently supported for automatic parsing
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

Dependencies (`python-docx`, `pyyaml`) should already be installed from Phase 0. If not, re-run the Phase 0 dependency check.

**Script Usage:** Read `~/.claude/skills/job-apply/generate_word_docs.py` for the `generate_application_documents()` function signature and parameter format. The function accepts `candidate`, `job`, `cover_letter`, `resume`, and `output_dir` arguments.

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

#### Step 6.1: Save Documents

Save files with naming convention:
- `{FirstName}_{LastName}_Cover_Letter_{Role_Keywords}_{Company}.docx`
- `{FirstName}_{LastName}_Resume_{Role_Keywords}_{Company}.docx`

#### Step 6.2: Log Application (for tracking)

Append to `~/.claude/skills/job-apply/applications.log`:
```
{date} | {company} | {role} | {fit_score}% | {output_dir}
```

#### Step 6.3: Open Output Folder

Automatically open the folder containing the generated documents so the user can immediately access them:

**On macOS:**
```bash
open "{output_dir}"
```

**On Linux:**
```bash
xdg-open "{output_dir}" 2>/dev/null || nautilus "{output_dir}" 2>/dev/null || dolphin "{output_dir}" 2>/dev/null
```

**On Windows:**
```cmd
explorer "{output_dir}"
```

#### Step 6.4: Provide Summary

Display comprehensive summary:

```
## Application Complete! 🎉

### Documents Generated
📄 Cover Letter: {filename}.docx
📄 Resume: {filename}.docx
📂 Location: {output_dir} (folder opened)

### Fit Assessment
- Overall Score: {X}%
- Recommendation: {Strong/Good/Stretch Fit}

### Key Matches Highlighted
- {Top 3-5 strongest qualification matches}

### Gaps Addressed in Cover Letter
- {Gap}: {How it was addressed}

### Next Steps
1. Review the documents in the opened folder
2. Upload to the job portal
3. Prepare for interview questions about: {gap areas}

### Interview Prep Tips
- Be ready to discuss: {Gap areas they may probe}
- Emphasize: {Your strongest differentiators}
- Portfolio demos: {Projects to show if asked}
```

#### Step 6.5: Ask About Next Action

Use AskUserQuestion:
```
What would you like to do next?
Options:
- "Apply to another job" - Start a new application
- "Edit these documents" - Open in editor for manual tweaks
- "Done for now" - Exit
```
