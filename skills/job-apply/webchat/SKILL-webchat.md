# Job Application Document Generator — Web Chat Edition

Evaluate job fit, then generate a tailored cover letter (1 page max) and resume (1-2 pages, prefer 1) optimized for ATS parsing and human scanning — all within Claude's web chat using the Analysis tool.

**Message budget: 3-4 messages** (up to 6 if user requests profile.yaml or detailed gap analysis).

## Input

The user provides:
1. A **resume** — uploaded as .docx or .pdf, a `profile.yaml` from a previous session, or qualifications pasted as text
2. A **job description** — pasted into chat or uploaded as a file

---

## Phase 1: Gather

**Goal:** Extract all source data in a single turn.

**If user uploaded a `profile.yaml`** (from a previous session):
- Parse YAML to load candidate info, qualifications, and portfolio projects
- Skip resume parsing — this saves a message
- If they also uploaded a resume, prefer the profile.yaml

**If user uploaded a resume .pdf:**
- Read the PDF text directly from conversation context — no code execution needed

**If user uploaded a resume .docx:**
- Use the Analysis tool to extract text:
  ```python
  import zipfile, re
  with zipfile.ZipFile(uploaded_file_path) as z:
      xml = z.read("word/document.xml").decode("utf-8")
  text = re.sub(r"</w:p>", "\n", xml)
  text = re.sub(r"<[^>]+>", " ", text)
  lines = [re.sub(r"[ \t]+", " ", line).strip() for line in text.split("\n")]
  text = "\n".join(line for line in lines if line)
  ```

**If user pasted qualifications as text:** Parse directly.

From the resume, extract: contact info, summary, skills by category, experience with dates and achievements, certifications, education.

From the job description, extract: must-have vs nice-to-have requirements, technical stack, industry context, years of experience.

**Output:** Confirm what was parsed and proceed to fit assessment in the same message.

---

## Phase 2: Assess & Plan

**Goal:** Score fit, select style, match experience — all in one output.

### Fit Scoring

Rate each job requirement against candidate evidence:

| Rating | Points | Meaning |
|--------|--------|---------|
| Strong Match | 1.0 | Direct experience with specific examples |
| Partial Match | 0.5 | Transferable skill or adjacent experience |
| Gap | 0.0 | No relevant experience |

**Score formula:**
```
Must-Have Score = (points / total must-haves) x 100
Nice-to-Have Score = (points / total nice-to-haves) x 100
Overall = (Must-Have x 0.7) + (Nice-to-Have x 0.3)
```

**Requirement classification signals:**
- Must-have: "Required", "Must have", "Essential", "Minimum qualifications", first 3-5 listed, legal/regulatory items
- Nice-to-have: "Preferred", "Bonus", "Plus", "Ideal candidate would have"

### Recommendation Matrix

| Overall | Must-Have | Recommendation |
|---------|-----------|----------------|
| 80%+ | 80%+ | **Strong Fit** — apply confidently |
| 60-79% | 70%+ | **Good Fit** — apply with targeted gap mitigation |
| 50-59% | 60%+ | **Stretch Fit** — apply only with referral or unique angle |
| Below 50% | Below 60% | **Poor Fit** — invest time in better matches |

### Disqualifiers (stop if any are true)

- Missing legally required credential (license, clearance)
- Missing the ONE core skill the entire role is built around
- Experience gap is 10+ years
- Role requires relocation candidate cannot do

### Style Selection

Auto-detect industry and select content strategy:
- Finance, Law, Healthcare, Government → **Classic** (conservative tone, precision)
- Tech, Corporate, Consulting → **Modern Professional** (balanced, contemporary)
- Design, Marketing, Startups → **Creative** (personality-forward, conversational)

Visual styling uses Modern Professional for all presets (hardcoded in the generator script).

### Experience Matching

- Map candidate experience to requirements, strongest matches first
- Select quantified achievements for each key requirement
- Match portfolio projects to technical requirements using achievement metrics
- Use exact keywords from the job description for ATS optimization

### Gap Mitigation

For each significant gap, prepare mitigation language:
- **Technical skill gap:** Highlight related tech + evidence of rapid learning
- **Experience years gap:** Emphasize impact depth and accelerated trajectory over tenure
- **Industry transition:** Map transferable skills to their challenges, show domain research

### Output Format

```
## Job Fit Assessment

**Role:** {Title} at {Company}
**Style:** {Preset} — {rationale}

### Fit Scores
- Must-Have: {X}% ({Y}/{Z})
- Nice-to-Have: {X}% ({Y}/{Z})
- **Overall: {X}%**

### Recommendation: {Strong Fit / Good Fit / Stretch Fit / Poor Fit}

### Strengths
- {Requirement}: {Evidence}

### Gaps to Address
- {Requirement}: {Gap} → {Mitigation strategy}

### Disqualifiers: {None / List}

Shall I proceed with generating your documents?
```

**Wait for user confirmation before proceeding.**

---

## Phase 3: Generate & Deliver

**Goal:** Generate both .docx files, provide downloads, offer portable profile.

### Document Generation

Copy the **entire contents** of `generate_word_docs_web.py` (in the Project knowledge) into the Analysis code block, then call `generate_application_documents()`. The script requires `python-docx` which is pre-installed in the sandbox. Output goes to `/tmp/`.

Call with: `candidate`, `job`, `cover_letter`, `resume`, `output_dir="/tmp/"`.

If generation fails, offer: retry with simpler run, output as formatted text, or generate with fewer styling features.

### Cover Letter Rules

- **Single page maximum** (350-450 words)
- Opening: Hook with strongest qualification — never "I am writing to express my interest"
- Body: 2-3 evidence sections mapped to top requirements, each with specific metrics
- Include Technical Alignment section only if role has specific tech requirements
- Address significant gaps with transferable skills
- Closing: Reference specific company initiative — never "I hope to hear from you soon"
- Every claim backed by specific evidence with numbers

### Resume Rules

- **1 page preferred, 2 pages max**
- ATS section headers: Summary, Skills, Experience, Education, Certifications
- Bullet formula: **Action Verb + Task + Quantified Result**
- 3-line experience header for ATS parsing (title, company, dates on separate lines)
- Date format: Mon YYYY - Mon YYYY (consistent throughout)
- Use exact keywords from job description
- Match terminology exactly — if they say "AWS", don't write "Amazon Web Services"
- Prioritize recent over old, quantified over qualitative

### Provide Downloads

After generation, provide both .docx files for download.

### Offer Portable Profile

> "Want me to generate a `profile.yaml` you can save? Next time, just upload it with a new job description to skip resume parsing and save a message."

If yes, use `generate_profile_yaml()` from the script.

### Summary

```
## Application Complete

**Documents Generated:**
- {Name}_Cover_Letter_{Role}_{Company}.docx
- {Name}_Resume_{Role}_{Company}.docx

**Fit Score:** {X}% — {Recommendation}

**Key Matches:** {Top 3-5}

**Gaps Addressed:** {How each was handled in cover letter}

**Interview Prep:**
- Be ready to discuss: {Gap areas}
- Emphasize: {Strongest differentiators}
```

---

## Profile YAML Format

The portable `profile.yaml` works with both web chat and CLI versions.

```yaml
candidate:
  name: "Full Name"
  title: "Target Role Title"
  phone: "555.123.4567"
  email: "email@example.com"
  linkedin: "linkedin.com/in/profile"
  calendar: ""

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

# Optional
portfolio_projects:
  - name: "Project Name"
    description: "Brief description"
    technologies: ["React", "TypeScript"]
    achievements:
      - metric: "80% improvement"
        description: "What was improved"
```

## Message Flow

| # | Who | What |
|---|-----|------|
| 1 | User | Uploads resume + pastes JD |
| 2 | Claude | Parses both, shows fit assessment, asks "Proceed?" |
| 3 | User | "Yes" |
| 4 | Claude | Generates .docx files, provides downloads, offers profile.yaml |

**First run: 4 messages.** Add 2 if user wants profile.yaml. Returning user with profile.yaml: 3-4 messages.
