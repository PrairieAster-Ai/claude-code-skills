# Job Application Best Practices

## Fit Assessment: Apply or Move On?

### The Key Numbers

| Match Level | Action |
|-------------|--------|
| **80%+ overall, 80%+ must-haves** | Strong candidate - apply confidently |
| **60-79% overall, 70%+ must-haves** | Good candidate - apply with gap mitigation |
| **50-59% overall, 60%+ must-haves** | Stretch - apply only with referral or unique angle |
| **Below 50%** | Move on - invest time elsewhere |

### Quick Disqualifier Check

**Do NOT apply if missing:**
- Legally required credentials (licenses, clearances)
- The ONE core skill the role is built around
- 10+ years of the required experience
- Non-negotiable location/travel requirements

**These are NOT disqualifiers:**
- 1-3 years less than "required" experience
- One unfamiliar tool in their tech stack
- "Preferred" certifications you don't have
- Adjacent industry experience

### The 62% Statistic

Research shows 62% of candidates who applied for jobs they were "underqualified" for still received offers. Job descriptions are wish lists, not hard requirements.

---

## Lessons Learned

### Source Material Discovery

1. **Resume files may have inconsistent naming**
   - Search for variations: "resume", "Resume", "CV", "cv"
   - Check common date formats in filenames
   - The most recent file by modification date is usually current

2. **DOCX extraction technique**
   ```bash
   unzip -p "file.docx" word/document.xml | sed -e 's/<[^>]*>//g' | tr -s '[:space:]' '\n'
   ```
   - This extracts readable text from Word documents
   - Formatting is lost but content is preserved
   - Use `head` and `tail` for long documents

3. **Portfolio project evidence**
   - README.md files often contain project summaries
   - package.json shows technology stack
   - Git commit history shows development practices
   - Look for `/docs`, `/documentation`, or wiki folders

### Job Description Analysis

1. **Classify requirements as must-have vs nice-to-have**
   - **Must-have signals:** "Required", "Must possess", "Essential", first 5 listed
   - **Nice-to-have signals:** "Preferred", "Bonus", "Plus", "Ideal candidate"
   - Requirements listed first are usually most important
   - Repeated skills/technologies indicate high priority

2. **Decode recruiter language**
   - "Fast-paced environment" = high workload, changing priorities
   - "Ambiguous environments" = undefined scope, figure it out
   - "Strong communicator" = client-facing or cross-functional
   - "Technical acumen" = can talk to engineers, not necessarily code
   - "Self-starter" = minimal management/onboarding

3. **Match terminology exactly**
   - If they say "AWS", use "AWS" not "Amazon Web Services"
   - If they say "Agile", don't substitute "Scrum" exclusively
   - Mirror their capitalization and abbreviations

### Evidence Selection

1. **Prioritize recent over old**
   - Last 5 years most relevant for senior roles
   - Older experience can be summarized briefly

2. **Prioritize quantified over qualitative**
   - Numbers always beat adjectives
   - "Improved performance" < "Reduced load time by 40%"

3. **Match industry when possible**
   - Financial services role? Lead with financial services experience
   - Healthcare? Emphasize HIPAA, regulatory experience
   - Startup? Highlight scrappiness, wearing many hats

---

## Gap Mitigation Strategies

### Missing Specific Technology

**In documents:**
> "While my hands-on experience is with [Related Tech], I've built [Similar System] using comparable patterns. My track record of rapidly mastering new platforms—learning [Tech] in [Timeframe]—positions me to quickly become productive."

**Key elements:**
- Acknowledge the gap honestly
- Show related/transferable experience
- Demonstrate learning velocity with specific example

### Less Experience Than Required

**In documents:**
> "My [X] years have been marked by accelerated impact, including [Achievement]. I've consistently delivered results expected of more senior professionals, as evidenced by [Recognition/Outcome]."

**Key elements:**
- Focus on impact depth, not tenure
- Highlight scope and scale achieved
- Show trajectory of increasing responsibility

### Industry Transition

**In documents:**
> "Transitioning from [Previous Industry], I bring transferable expertise in [Skill]. My research into [Target Industry] reveals parallels around [Challenge], where my [Solution] experience directly applies."

**Key elements:**
- Map your skills to their challenges
- Show you've researched the new domain
- Demonstrate genuine interest

### Experience Equivalencies

| If Missing | Often Substitutes |
|------------|-------------------|
| Bachelor's degree | 4+ years relevant experience |
| 2 years experience | Relevant degree + strong projects |
| Specific technology | Similar tech + learning evidence |
| Industry experience | Transferable skills + domain study |

---

## ATS Success Factors

1. **File format**
   - Markdown converts cleanly to PDF
   - Avoid complex formatting that breaks parsing
   - Test by copying text to notepad - should be readable

2. **Keyword density**
   - Natural integration, not keyword stuffing
   - Use exact phrases from job description
   - Include both acronyms and full forms when space permits

3. **Section structure**
   - Use standard headers ATS systems recognize
   - Maintain consistent formatting throughout
   - Ensure dates are parseable (Mon YYYY format works well)

---

## Human Reader Optimization

### The 6-Second Rule

Hiring managers spend 6-10 seconds on initial scan. Optimize for:

1. **First 10 seconds matter most**
   - Name and title clearly visible
   - Summary captures key value proposition
   - Most impressive achievement within first scroll

2. **Scannable format**
   - Short bullet points (1-2 lines max)
   - Bold for emphasis on key metrics
   - White space between sections

3. **Tell a coherent story**
   - Career progression should be evident
   - Each role should build on previous
   - No unexplained gaps (address in cover letter if needed)

---

## Role-Specific Considerations

### Product Owner / Product Manager
- Emphasize stakeholder management
- Show business impact (revenue, cost savings)
- Highlight cross-functional collaboration
- Mention specific methodologies (Scrum, SAFe, Kanban)

### Technical Roles
- Lead with technical skills section
- Include links to GitHub/portfolio
- Quantify technical achievements (performance improvements, scale)
- Show progression from junior to senior work

### AI/ML Roles
- Demonstrate understanding of AI concepts
- Show practical implementation experience
- Mention specific models, frameworks, platforms
- Highlight responsible AI considerations if relevant

### Financial Services
- Mention regulatory knowledge (SOX, GDPR, etc.)
- Show experience with financial data scale
- Emphasize security consciousness
- Reference relevant certifications

---

## When to Apply Anyway (Low Score)

Apply with 50-60% match if you have:

1. **Strong internal referral**
2. **Newly created role** (requirements may flex)
3. **Unique perspective** they didn't know they need
4. **Killer portfolio piece** demonstrating exact skills
5. **Role posted 60+ days** (they may be struggling)

## When to Walk Away (High Score)

Don't apply even with good match if:

1. **Red flags in job description** (unrealistic scope)
2. **Poor company reviews** on Glassdoor
3. **Compensation significantly below market**
4. **Role scope = 2-3 jobs in one**
5. **You're not genuinely interested**

---

## Output Quality Checklist

### Before Fit Assessment
- [ ] Extracted all requirements from job description
- [ ] Classified must-have vs nice-to-have
- [ ] Checked for disqualifiers
- [ ] Calculated fit score accurately

### Before Delivering Documents
- [ ] Fit assessment presented to user
- [ ] User confirmed proceed with application
- [ ] Cover letter is under 1 page when rendered
- [ ] Resume is 1-2 pages when rendered
- [ ] All claims have specific evidence
- [ ] Numbers are accurate and verifiable
- [ ] Job title keywords appear in both documents
- [ ] Contact information is complete and current
- [ ] No spelling or grammar errors
- [ ] Company name from job description appears (if known)
- [ ] Tone matches company culture indicators
- [ ] Style preset matches industry
- [ ] Gaps addressed in cover letter
- [ ] Files saved with clear naming convention

### Interview Prep Notes Included
- [ ] Gap areas they may probe identified
- [ ] Strongest differentiators highlighted
- [ ] Portfolio pieces to reference suggested
