# Job Application Document Generator — Web Chat Edition

Evaluate job fit, then generate a tailored cover letter (1 page max) and resume (1-2 pages, prefer 1) optimized for both ATS parsing and human scanning — all within Claude's web chat using the Analysis tool.

## How This Skill Works

This is a Project instruction file for claude.ai. Upload it along with the reference files to a Claude Project, then start a conversation with your resume and a job description.

**Message budget: 3-4 messages for a typical run** (up to 6 if user requests profile.yaml or detailed gap analysis).

## Input

The user provides:
1. A **resume** — uploaded as .docx or .pdf, a `profile.yaml` from a previous session, or qualifications pasted as text
2. A **job description** — pasted into chat or uploaded as a file

## Reference Files

These files are available in the Project knowledge alongside this file:

- **fit-assessment.md** — Evaluation framework, scoring formula, recommendation matrix
- **style-presets.md** — Visual styling specs for Classic, Modern Professional, Creative
- **cover-letter-template.md** — Cover letter structure and writing guidelines
- **resume-template.md** — Resume structure and ATS optimization
- **best-practices.md** — Strategic advice, gap mitigation, evidence selection

## Workflow

### Phase 1: Gather

**Goal:** Extract all source data in a single turn. No setup wizard, no config file.

**If user uploaded both a `profile.yaml` and a resume**, prefer the profile.yaml (it has structured data). Note: "I see you uploaded both a profile and a resume. I'll use the profile.yaml since it has structured data. Let me know if you'd prefer I re-parse from the resume instead."

**If user uploaded a `profile.yaml`** (from a previous session):
- Parse the YAML to load candidate info, qualifications, and portfolio projects
- Skip resume parsing entirely — this saves a full message
- Confirm: "Loaded your profile. Proceeding with fit assessment."

**If user uploaded a resume .pdf:**
- Claude can read uploaded PDF text directly from the conversation context
- Skip the Analysis tool extraction step — parse the PDF text to identify candidate information

**If user uploaded a resume .docx:**
- Use the Analysis tool to extract text from the .docx via Python's `zipfile` module:
  ```python
  import zipfile, re
  # Replace "resume.docx" with the actual uploaded file path
  with zipfile.ZipFile(uploaded_file_path) as z:
      xml = z.read("word/document.xml").decode("utf-8")
  text = re.sub(r"</w:p>", "\n", xml)
  text = re.sub(r"<[^>]+>", " ", text)
  lines = [re.sub(r"[ \t]+", " ", line).strip() for line in text.split("\n")]
  text = "\n".join(line for line in lines if line)
  ```

**If user pasted qualifications as text** (no file upload):
- Parse the text directly to extract candidate information. Proceed as normal.

For all resume sources, parse the extracted text to identify:
  - Contact info (name, phone, email, LinkedIn)
  - Professional summary
  - Skills by category
  - Work experience with dates and achievements
  - Certifications
  - Education

**Parse the job description** to extract:
- Required skills and experience (must-haves)
- Preferred qualifications (nice-to-haves)
- Technical stack
- Soft skills and culture fit indicators
- Industry/domain context
- Years of experience requirements

**Output at end of Phase 1:** Confirm what was parsed: "Here's what I found in your resume: [name], [X years experience], [key skills]. And from the JD: [role] at [company], [key requirements]. Proceeding to fit assessment."

---

### Phase 2: Assess & Plan

**Goal:** Combine fit assessment, style detection, and experience matching into one output. Uses the frameworks in fit-assessment.md and style-presets.md.

#### Fit Assessment

Categorize each job requirement as must-have or nice-to-have using the signals from fit-assessment.md.

For each requirement, evaluate against candidate evidence:

| Rating | Meaning | Score |
|--------|---------|-------|
| ✅ Strong Match | Direct experience or qualification | 1.0 |
| ⚠️ Partial Match | Transferable skill or adjacent experience | 0.5 |
| ❌ Gap | No relevant experience | 0.0 |

**Calculate scores:**
```
Must-Have Score = (points earned / total must-haves) × 100
Nice-to-Have Score = (points earned / total nice-to-haves) × 100
Overall Fit Score = (Must-Have Score × 0.7) + (Nice-to-Have Score × 0.3)
```

**Check for disqualifiers** per fit-assessment.md (missing legal credentials, 10+ year experience gap, etc.)

#### Style Selection

Auto-detect industry from job description and select the appropriate preset per style-presets.md. Style selection affects content strategy (tone, structure, keyword emphasis). Visual styling currently uses Modern Professional for all presets.

- Finance, Law, Healthcare, Government → **Classic**
- Tech, Corporate, Consulting → **Modern Professional**
- Design, Marketing, Startups → **Creative**

#### Experience Matching

- Map candidate experience to job requirements, strongest matches first
- Select quantified achievements for each key requirement
- Match portfolio projects (if provided in profile.yaml) to technical requirements — use achievement metrics as evidence
- Identify keywords from JD for ATS optimization
- Craft gap mitigation language per best-practices.md

#### Output

Display a combined assessment:

```
## Job Fit Assessment

**Role:** {Job Title} at {Company}
**Style:** {Preset} — {Industry rationale}

### Fit Scores
- Must-Have: {X}% ({Y}/{Z})
- Nice-to-Have: {X}% ({Y}/{Z})
- **Overall: {X}%**

### Recommendation: {Strong Fit / Good Fit / Stretch Fit / Poor Fit}

### Strengths
- {Requirement}: {Evidence}

### Gaps to Address
- {Requirement}: {Gap} → {Mitigation strategy for cover letter}

### Disqualifiers: {None / List}

{If no disqualifiers: "Shall I proceed with generating your documents?"}
{If disqualifiers found: "Disqualifiers found — I'd recommend not proceeding, but I can generate documents if you'd like."}
```

**Wait for user confirmation before proceeding.** This is the one required interaction point.

---

### Phase 3: Generate & Deliver

**Goal:** Generate both .docx files using the Analysis tool, provide downloads, and offer a portable profile.

#### Document Generation

Use the Analysis tool to generate documents. Copy the **entire contents** of `generate_word_docs_web.py` (available in the Project knowledge) into the Analysis code block, then call `generate_application_documents()`. The script requires `python-docx` which is pre-installed in the Analysis sandbox. Output is written to `/tmp/`.

**If document generation fails** (timeout, memory limit, missing package), offer the user alternatives:
1. Try again with a simpler run
2. Output the cover letter and resume as formatted text in the conversation for manual copy into Word
3. Generate simpler documents with fewer styling features

Call `generate_application_documents()` with:

- `candidate`: Contact info parsed from resume/profile
- `job`: Title, company, location from JD
- `cover_letter`: Content structured per cover-letter-template.md
- `resume`: Content structured per resume-template.md
- `output_dir`: `/tmp/` (Analysis sandbox output)

**Cover letter requirements** (see cover-letter-template.md):
- Single page maximum (350-450 words)
- Opening: Hook with strongest qualification
- Body: 2-3 evidence sections mapped to requirements
- Address significant gaps with transferable skills
- No generic phrases
- Every claim backed by specific evidence

**Resume requirements** (see resume-template.md):
- 1 page preferred, 2 pages max
- Standard ATS headers: Summary, Skills, Experience, Education
- Exact keywords from job description
- Action Verb + Task + Quantified Result bullet format
- Consistent date formatting (Mon YYYY - Mon YYYY)

#### Provide Downloads

After generation, provide both .docx files for download.

#### Offer Portable Profile

After delivering documents, offer to generate a `profile.yaml` the user can download and reuse:

> "Want me to generate a `profile.yaml` you can save? Next time, just upload it with a new job description to skip resume parsing and save a message."

If yes, use `generate_profile_yaml()` from the script to create a downloadable YAML file containing:
- Candidate contact info
- Qualifications (summary, skills, experience, certifications, education)
- Portfolio projects (if any were mentioned in the resume or conversation)

#### Summary

```
## Application Complete

**Documents Generated:**
- {Name}_Cover_Letter_{Role}_{Company}.docx
- {Name}_Resume_{Role}_{Company}.docx

**Fit Score:** {X}% — {Recommendation}

**Key Matches:** {Top 3-5}

**Gaps Addressed:** {How each gap was handled in cover letter}

**Interview Prep:**
- Be ready to discuss: {Gap areas}
- Emphasize: {Strongest differentiators}
```

## Profile YAML Format

The portable `profile.yaml` contains a subset of the full config.yaml used by Claude Code. It works in both environments.

```yaml
candidate:
  name: "Full Name"
  title: "Target Role Title"      # Set per application
  phone: "555.123.4567"
  email: "email@example.com"
  linkedin: "linkedin.com/in/profile"
  calendar: ""                     # Optional: calendly.com/name/30min

qualifications:
  summary: "Professional summary..."
  skills:
    - category: "Category"
      items: "Skill1, Skill2, Skill3"
  experience:
    - title: "Job Title"
      company: "Company"
      dates: "Mon YYYY - Present"
      bullets:
        - text: "Achievement with metric"
          highlights: ["metric"]
  certifications:
    - name: "Cert Name"
      year: "YYYY"
      issuer: "Issuing Organization"
  education:
    - degree: "Degree, Major"
      school: "University"
      year: "YYYY"                 # Optional

# Optional — include if user has portfolio projects
portfolio_projects:
  - name: "Project Name"
    description: "Brief description"
    technologies: ["React", "TypeScript"]
    achievements:
      - metric: "80% improvement"
        description: "What was improved"
```

## Message Flow (Typical)

| # | Who | What |
|---|-----|------|
| 1 | User | Uploads resume + pastes JD |
| 2 | Claude | Parses both, shows fit assessment, asks "Proceed?" |
| 3 | User | "Yes" |
| 4 | Claude | Generates .docx files, provides downloads, offers profile.yaml |
| 5 | User | "Yes, generate profile" (optional) |
| 6 | Claude | Provides profile.yaml download (optional) |

**Typical first run: 4 messages.** Add 2 if user wants a profile.yaml.

**Returning user with profile.yaml:** Upload profile + paste JD → 3-4 messages total.
