# Job Application Assistant — Manual Test Script

**File under test:** `job-apply-artifact.html`
**Open:** directly in a browser (Chrome, Firefox, Safari, or Edge)

---

## Test Data

### Sample JD (Strong Match)

```
Senior Software Engineer
San Francisco, CA

About Us:
We are a fast-growing technology company building the next generation of cloud-based analytics.

Requirements:
- 5+ years of experience in software development
- Strong proficiency in Python and JavaScript
- Experience with React and Node.js
- Knowledge of AWS cloud services
- Experience with PostgreSQL or similar relational databases
- Familiarity with Docker and Kubernetes
- Strong understanding of RESTful API design
- Bachelor's degree in Computer Science or related field

Preferred:
- Experience with machine learning or data science
- Knowledge of GraphQL
- Certified Scrum Master (CSM) is a plus
- Experience with Terraform or infrastructure-as-code

Responsibilities:
- Design and implement scalable software solutions
- Mentor junior developers
- Participate in code reviews and architectural discussions
```

### Sample Resume (Strong Match)

```
Jane Smith
jane.smith@email.com | (555) 123-4567 | linkedin.com/in/janesmith

Professional Summary
Experienced software engineer with 8 years of expertise building scalable web applications using Python, JavaScript, and cloud technologies. Proven track record of leading teams and delivering high-impact products.

Professional Experience

Senior Developer
Acme Corp
Jan 2020 - Present
- Led development of microservices architecture serving 500K+ daily users
- Implemented CI/CD pipelines using Docker and Kubernetes, reducing deployment time by 60%
- Mentored team of 5 junior developers in React and Node.js best practices
- Designed and deployed AWS-based infrastructure for high-availability systems
- Built RESTful APIs handling 2M+ requests per day with 99.9% uptime

Software Engineer
Tech Inc
Jun 2016 - Dec 2019
- Built RESTful APIs using Python and PostgreSQL handling 1M+ transactions daily
- Developed React frontend components with 95% test coverage
- Migrated legacy system to AWS, reducing infrastructure costs by 40%
- Implemented automated testing reducing bug escape rate by 70%

Skills
Python, JavaScript, TypeScript, React, Node.js, PostgreSQL, AWS, Docker, Kubernetes, Git, CI/CD, REST APIs, Agile, Scrum, Terraform

Education
Bachelor of Science in Computer Science, State University, 2016

Certifications
AWS Certified Solutions Architect
```

### Sample JD (Poor Match — Nursing)

```
Registered Nurse - ICU
Memorial Hospital, Chicago, IL

Requirements:
- Active RN license in the state of Illinois
- BLS and ACLS certification required
- 3+ years of ICU or critical care experience
- Experience with electronic health records (Epic preferred)
- Bachelor of Science in Nursing (BSN)

Preferred:
- CCRN certification
- Experience with ventilator management
```

### Minimal JD (No Sections)

```
We need a Python developer with 3 years experience. Must know Django and PostgreSQL. Remote position. Startup environment, fast-paced.
```

### Minimal Resume

```
John Doe
john@example.com
555-987-6543

Python developer with 5 years experience building Django and PostgreSQL applications for startups and mid-size companies.
```

---

## Section 1: Initial Load & Branding

| #    | Action                                    | Expected Behavior                                                                                         | Pass |
| ---- | ----------------------------------------- | --------------------------------------------------------------------------------------------------------- | ---- |
| 1.1  | Open `job-apply-artifact.html` in browser | Page loads with no console errors                                                                         |      |
| 1.2  | Inspect header background                 | Purple gradient: dark purple `#5a4080` → medium purple `#7d60a6` → light blue `#7fa4cf`                   |      |
| 1.3  | Inspect header logo                       | White stylized prairie aster flower (multi-petal geometric design) visible on purple background           |      |
| 1.4  | Inspect header text                       | "PrairieAster.Ai" in serif font (Georgia), "Job Application Assistant" as smaller tagline in light purple |      |
| 1.5  | Inspect page background                   | Subtle lavender tint (`#f8f6fb`), not pure white or grey                                                  |      |
| 1.6  | Inspect card borders                      | Purple-tinted grey (`#e0dae8`)                                                                            |      |
| 1.7  | Check max-width                           | Main content area is 850px wide (matches CLAUDE.md constraint)                                            |      |
| 1.8  | Check persistence bar                     | Shows below header: "No saved data — your inputs will auto-save locally". No "Clear" button visible.      |      |
| 1.9  | Check step indicator                      | Three steps shown: "1 Input" (active/purple), "2 Assessment" (grey), "3 Documents" (grey)                 |      |
| 1.10 | Check step 1 is active                    | Input panel visible with JD textarea, Resume textarea, and Style Preset dropdown                          |      |

---

## Section 2: Data Persistence

| #   | Action                                                           | Expected Behavior                                                                                                                      | Pass |
| --- | ---------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------- | ---- |
| 2.1 | Type a few characters in the JD textarea                         | After ~1 second, persistence bar updates to "Resume data auto-saved (today's date/time)" and "Clear Saved Data" button appears         |      |
| 2.2 | Reload the page (F5)                                             | JD textarea retains the typed characters. Persistence bar shows the saved timestamp.                                                   |      |
| 2.3 | Paste the full Sample JD (Strong Match) into JD textarea         | Auto-saves after 1 second (persistence bar updates)                                                                                    |      |
| 2.4 | Paste the full Sample Resume (Strong Match) into Resume textarea | Auto-saves after 1 second                                                                                                              |      |
| 2.5 | Change style preset to "Classic"                                 | Auto-saves. Reload page — "Classic" is still selected, both textareas retain content.                                                  |      |
| 2.6 | Click "Clear Saved Data"                                         | Both textareas cleared. Dropdown resets to "Modern". Persistence bar shows "No saved data". Toast: "Saved data cleared".               |      |
| 2.7 | Reload the page                                                  | Both textareas are empty. Dropdown is "Modern Professional". Persistence bar shows "No saved data".                                    |      |
| 2.8 | Open in incognito/private window                                 | Page loads normally. Persistence bar shows "No saved data". Typing triggers auto-save (may fail silently in some browsers — no crash). |      |

---

## Section 3: Input Validation

| #   | Action                                                          | Expected Behavior                                                              | Pass |
| --- | --------------------------------------------------------------- | ------------------------------------------------------------------------------ | ---- |
| 3.1 | Click "Analyze Fit & Generate Documents" with both fields empty | Red error: "Please paste a complete job description (at least 50 characters)." |      |
| 3.2 | Type 20 characters in JD, leave Resume empty, click Analyze     | Same JD error (still under 50 chars)                                           |      |
| 3.3 | Paste a valid JD (50+ chars), leave Resume empty, click Analyze | Red error: "Please paste your resume text (at least 50 characters)."           |      |
| 3.4 | Paste valid JD and valid Resume, click Analyze                  | Error disappears. Page navigates to Step 2 (Assessment).                       |      |

---

## Section 4: Fit Assessment — Strong Match

**Setup:** Paste Sample JD (Strong Match) and Sample Resume (Strong Match), select "Modern Professional", click Analyze.

| #    | Check                     | Expected Behavior                                                                                                                                                                       | Pass |
| ---- | ------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---- |
| 4.1  | Recommendation badge      | Green badge: "Strong Fit" with advice "Apply confidently. Lead with your strengths."                                                                                                    |      |
| 4.2  | Overall Score             | 80–100%, displayed in green (`#2e7d32`)                                                                                                                                                 |      |
| 4.3  | Must-Have Score           | 80–100%, displayed in green                                                                                                                                                             |      |
| 4.4  | Nice-to-Have Score        | 25–75% (some nice-to-haves won't match), green/blue/orange depending on value                                                                                                           |      |
| 4.5  | Detected Information      | Title: "Senior Software Engineer", Location: "San Francisco, CA", Level: "senior", Industry: "technology"                                                                               |      |
| 4.6  | Must-Have table           | 7-8 rows. Most show ✅ (strong match). Skills like Python, JavaScript, React, Node.js, AWS, PostgreSQL, Docker, Kubernetes should be strong matches. Education (Bachelor's) should be ✅. |      |
| 4.7  | Nice-to-Have table        | 3-4 rows. "Machine learning" may show ❌ (gap). "GraphQL" likely ❌. "CSM" likely ❌. "Terraform" should show ✅ (it's in the resume skills).                                               |      |
| 4.8  | Evidence column           | At least some must-have rows show bullet text from resume (e.g., "Led development of microservices…" or "Built RESTful APIs…")                                                          |      |
| 4.9  | Skills Analysis — Matched | Green pills showing: JavaScript, Python, React, Node.js, AWS, Docker, Kubernetes, PostgreSQL, REST, Agile, Scrum, Terraform, Git                                                        |      |
| 4.10 | Skills Analysis — Missing | Red pills showing unmatched JD skills (e.g., GraphQL, Machine Learning, CSM)                                                                                                            |      |
| 4.11 | Disqualifiers             | "No disqualifiers detected — you can proceed with your application." in green                                                                                                           |      |
| 4.12 | Navigation buttons        | "Back to Input" and "View Documents" buttons visible                                                                                                                                    |      |

---

## Section 5: Fit Assessment — Poor Match

**Setup:** Paste Sample JD (Nursing) and Sample Resume (Strong Match — tech), click Analyze.

| #   | Check                | Expected Behavior                                                                       | Pass |
| --- | -------------------- | --------------------------------------------------------------------------------------- | ---- |
| 5.1 | Recommendation badge | Red badge: "Poor Fit"                                                                   |      |
| 5.2 | Overall Score        | Below 50%, displayed in red                                                             |      |
| 5.3 | Must-Have table      | Most items show ❌ (gap) — RN license, BLS/ACLS, ICU experience are not in a tech resume |      |
| 5.4 | Matched Skills       | 0 or very few matched skills                                                            |      |
| 5.5 | Missing Skills       | Nursing-specific terms (BLS, ACLS, ICU, etc.) shown as missing                          |      |

---

## Section 6: Fit Assessment — Minimal Input

**Setup:** Paste Minimal JD and Minimal Resume, click Analyze.

| #   | Check        | Expected Behavior                                                       | Pass |
| --- | ------------ | ----------------------------------------------------------------------- | ---- |
| 6.1 | No crash     | Assessment renders without errors                                       |      |
| 6.2 | Title        | "Professional Role" (fallback) or detects a partial title               |      |
| 6.3 | Location     | "Remote" (detected from "Remote position")                              |      |
| 6.4 | Skills       | Detects Python, Django, PostgreSQL from free text                       |      |
| 6.5 | Requirements | May be 0 (no bullet points) — assessment still works via skill matching |      |
| 6.6 | Score        | Should be high (80-100%) since skills match well                        |      |

---

## Section 7: Document Preview — Modern Preset

**Setup:** From a successful Strong Match assessment, click "View Documents".

| #   | Check                 | Expected Behavior                                                                                                                                                                                 | Pass |
| --- | --------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---- |
| 7.1 | Step indicator        | Step 3 active (purple). Steps 1 and 2 show green checkmarks.                                                                                                                                      |      |
| 7.2 | Tab bar               | "Cover Letter" tab is active (purple underline). "Resume" tab is inactive.                                                                                                                        |      |
| 7.3 | Cover Letter preview  | Navy blue headers (#1a5276). Name "Jane Smith" in large H1. Subtitle "[Title] Candidate". Contact info line. Horizontal divider. Date, "Dear Hiring Manager", "Re: Senior Software Engineer".     |      |
| 7.4 | Cover Letter content  | "Relevant Experience" section with evidence paragraphs. "Technical Alignment" section with matched skills. "Why This Role" closing. "Best regards, Jane Smith".                                   |      |
| 7.5 | Click "Resume" tab    | Resume preview appears. Cover letter hides. Resume tab has purple underline.                                                                                                                      |      |
| 7.6 | Resume preview        | Navy headers. Name, subtitle, contact info, divider. Sections: Summary, Technical Skills (grouped by category), Professional Experience (title/company/dates/bullets), Certifications, Education. |      |
| 7.7 | Resume bullets sorted | Bullets most relevant to the JD appear first within each experience entry                                                                                                                         |      |
| 7.8 | Skills grouped        | Skills appear under category headings (e.g., "Programming Languages: JavaScript, Python, TypeScript")                                                                                             |      |
| 7.9 | Action buttons        | "Download .doc" (green), "Copy to Clipboard", and "Print" buttons visible above document                                                                                                          |      |

---

## Section 8: Document Preview — Classic Preset

**Setup:** Go back to Input, change preset to "Classic", click Analyze, then View Documents.

| #   | Check        | Expected Behavior                                                                                                                                           | Pass |
| --- | ------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------- | ---- |
| 8.1 | Cover Letter | Serif font (Georgia). Dark navy (#1a365d) headers. UPPERCASE H2 headings with underline. Formal tone: "I respectfully submit…", "Respectfully, Jane Smith". |      |
| 8.2 | Resume       | UPPERCASE section headers ("SUMMARY", "PROFESSIONAL EXPERIENCE", "SKILLS", "EDUCATION"). Serif body text. Conservative layout.                              |      |

---

## Section 9: Document Preview — Creative Preset

**Setup:** Go back to Input, change preset to "Creative", click Analyze, then View Documents.

| #   | Check                     | Expected Behavior                                                                                                                                                                                                                       | Pass |
| --- | ------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---- |
| 9.1 | Cover Letter              | Purple accent color (#805ad5 for technology industry). Centered name. Contact box with colored background. Casual greeting "Hi there". Sections: "What I Bring" (bulleted), "The Fit", "Let's Connect". Signs off "Cheers, Jane Smith". |      |
| 9.2 | Resume                    | Centered name in purple. Subtitle. Colored contact box. "Profile" section. "Core Competencies" as a 3-column grid of colored badges. Experience with purple-accented titles.                                                            |      |
| 9.3 | Industry color adaptation | For a healthcare JD, creative accent should be blue (#2b6cb0). For a finance JD, should be navy (#2c5282).                                                                                                                              |      |

---

## Section 10: Copy to Clipboard

| #    | Action                                          | Expected Behavior                                                                                                                    | Pass |
| ---- | ----------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------ | ---- |
| 10.1 | View a cover letter, click "Copy to Clipboard"  | Toast: "Copied to clipboard (rich text)". Paste into Google Docs or Word — formatted text with headers, bold, and styling preserved. |      |
| 10.2 | Paste into a plain text editor (Notepad)        | Pasted as plain text (no HTML tags).                                                                                                 |      |
| 10.3 | Switch to Resume tab, click "Copy to Clipboard" | Toast shows success. Paste into Word — resume formatting preserved.                                                                  |      |

---

## Section 11: Word Document Download

| #    | Action                                       | Expected Behavior                                                                                                             | Pass |
| ---- | -------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------- | ---- |
| 11.1 | Click "Download .doc" on Cover Letter tab    | Browser downloads a `.doc` file. Toast: "Downloaded Jane_Smith_Cover_Letter_Senior_Software_Engineer.doc"                     |      |
| 11.2 | Inspect filename                             | Format: `CandidateName_Cover_Letter_JobTitle.doc` with underscores, no special chars                                          |      |
| 11.3 | Open downloaded .doc in Microsoft Word       | Opens correctly. Page size 8.5" x 11". Margins ~0.75". Font matches preset. Headers in accent color. Content matches preview. |      |
| 11.4 | Open downloaded .doc in LibreOffice Writer   | Opens correctly. Formatting generally preserved.                                                                              |      |
| 11.5 | Open downloaded .doc in Google Docs (upload) | Opens and converts. Basic formatting preserved (headings, bold, colors).                                                      |      |
| 11.6 | Click "Download .doc" on Resume tab          | Downloads `Jane_Smith_Resume_Senior_Software_Engineer.doc`. Opens in Word with correct formatting.                            |      |
| 11.7 | Test with Classic preset                     | Downloaded .doc has serif fonts (Georgia), dark navy accent, uppercase section headers                                        |      |
| 11.8 | Test with Creative preset                    | Downloaded .doc has purple accent color, centered name, competency badges as inline-block elements                            |      |

---

## Section 12: Print

| #    | Action                               | Expected Behavior                                                                                                              | Pass |
| ---- | ------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------ | ---- |
| 12.1 | On the Documents step, click "Print" | Print dialog opens. Preview shows only the document content — no header, step indicator, buttons, persistence bar, or tab bar. |      |
| 12.2 | Both tabs visible in print           | If both cover letter and resume tabs exist, both documents appear with a page break between them.                              |      |
| 12.3 | Background is white                  | No colored page background in print preview.                                                                                   |      |

---

## Section 13: Navigation & Wizard Flow

| #    | Action                                                       | Expected Behavior                                                                                  | Pass |
| ---- | ------------------------------------------------------------ | -------------------------------------------------------------------------------------------------- | ---- |
| 13.1 | Complete analysis, on Assessment step, click "Back to Input" | Returns to Step 1. JD and Resume fields still contain text. Step indicator shows step 1 active.    |      |
| 13.2 | Click Analyze again (same data)                              | Re-runs analysis. Navigates to Assessment. Same results.                                           |      |
| 13.3 | Click "View Documents"                                       | Navigates to Step 3. Step indicator: steps 1 and 2 show green checkmarks, step 3 is active purple. |      |
| 13.4 | Click "Back to Assessment"                                   | Returns to Step 2. Assessment data still displayed.                                                |      |
| 13.5 | Click "Start Over"                                           | Returns to Step 1. Both textareas are empty. Step indicator resets.                                |      |
| 13.6 | Scroll position                                              | Each step navigation scrolls to the top of the page smoothly                                       |      |

---

## Section 14: Toast Notifications

| #    | Action                         | Expected Behavior                                                                          | Pass |
| ---- | ------------------------------ | ------------------------------------------------------------------------------------------ | ---- |
| 14.1 | Trigger any toast (e.g., copy) | Toast appears in bottom-right corner. Dark background, white text. Slides up with fade-in. |      |
| 14.2 | Wait 2.5 seconds               | Toast fades out and slides down.                                                           |      |
| 14.3 | Trigger two toasts rapidly     | Second toast replaces first text. Timer resets (may overlap).                              |      |

---

## Section 15: Responsive & Edge Cases

| #    | Action                                               | Expected Behavior                                                                                                                        | Pass |
| ---- | ---------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------- | ---- |
| 15.1 | Resize browser to 600px width                        | Layout remains usable. Score cards may stack. Tables may scroll horizontally. No content overflow.                                       |      |
| 15.2 | Paste a JD with no bullet points                     | Parser falls back to any bullet-like lines. If none found, 0 requirements — assessment still works (skill matching drives score).        |      |
| 15.3 | Paste a resume with no experience section            | Experience array is empty. Summary/skills still parsed. Assessment uses keyword matching. Documents generate without experience section. |      |
| 15.4 | Paste extremely long JD (5000+ words)                | No crash. Parsing may take a moment but completes. Assessment renders.                                                                   |      |
| 15.5 | Paste text with special characters (<, >, &, quotes) | No XSS. Characters are HTML-escaped in display. Documents render correctly.                                                              |      |
| 15.6 | Check browser console for errors                     | No JavaScript errors during normal usage flow                                                                                            |      |

---

## Section 16: Scoring Accuracy Spot Checks

| #    | Scenario                                                           | Expected Score Range                                                | Pass |
| ---- | ------------------------------------------------------------------ | ------------------------------------------------------------------- | ---- |
| 16.1 | Strong Match JD + Strong Match Resume                              | Overall: 80-100%, Rec: "Strong Fit"                                 |      |
| 16.2 | Nursing JD + Tech Resume                                           | Overall: 0-35%, Rec: "Poor Fit"                                     |      |
| 16.3 | Minimal JD (Python/Django) + Minimal Resume (Python/Django)        | Overall: 80-100%, Rec: "Strong Fit"                                 |      |
| 16.4 | Strong Match JD + empty-ish resume (just name and email, 50 chars) | Overall: 0-30%, Rec: "Poor Fit"                                     |      |
| 16.5 | Must-haves all match, nice-to-haves all miss                       | Must-Have: ~100%, Nice-to-Have: ~0%, Overall: ~70%, Rec: "Good Fit" |      |

---

## Section 17: JD Parser Accuracy

| #    | Input Detail                         | Expected Detection                     | Pass |
| ---- | ------------------------------------ | -------------------------------------- | ---- |
| 17.1 | "San Francisco, CA" on its own line  | Location: "San Francisco, CA"          |      |
| 17.2 | "Remote" anywhere in JD              | Location: "Remote"                     |      |
| 17.3 | "5+ years of experience"             | Experience years: 5                    |      |
| 17.4 | "Senior" in title or body            | Experience level: "senior"             |      |
| 17.5 | "software", "tech", "cloud" keywords | Industry: "technology"                 |      |
| 17.6 | "Bachelor's degree" in requirements  | Education: BS detected                 |      |
| 17.7 | "CSM" or "Certified Scrum Master"    | Certification: CSM detected            |      |
| 17.8 | Section labeled "Preferred:"         | Items below classified as nice-to-have |      |
| 17.9 | Section labeled "Requirements:"      | Items below classified as must-have    |      |

---

## Section 18: Resume Parser Accuracy

| #     | Input Detail                               | Expected Detection                                  | Pass |
| ----- | ------------------------------------------ | --------------------------------------------------- | ---- |
| 18.1  | "jane.smith@email.com" in first 10 lines   | Email extracted                                     |      |
| 18.2  | "(555) 123-4567"                           | Phone extracted                                     |      |
| 18.3  | "linkedin.com/in/janesmith"                | LinkedIn extracted                                  |      |
| 18.4  | First non-empty short line                 | Name: "Jane Smith"                                  |      |
| 18.5  | "Professional Summary" section             | Summary text extracted                              |      |
| 18.6  | "Jan 2020 - Present" date pattern          | Experience entry with correct dates                 |      |
| 18.7  | Lines before date line                     | Title and company correctly assigned via look-back  |      |
| 18.8  | Bullet points (- prefixed)                 | Bullets captured in experience entry (min 10 chars) |      |
| 18.9  | "Skills" section with comma-separated list | Skills parsed from section + database matching      |      |
| 18.10 | "Bachelor of Science in Computer Science"  | Education entry detected                            |      |
| 18.11 | "AWS Certified Solutions Architect"        | Certification detected                              |      |
| 18.12 | "500K+", "60%", "$40%" metrics             | Metrics extracted with context                      |      |
