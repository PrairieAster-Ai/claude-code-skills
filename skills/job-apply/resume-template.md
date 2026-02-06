# Resume Template

Structure and styling guidelines for ATS-optimized, visually appealing resumes.

## Template by Style Preset

### Classic Template

```markdown
# {Full Name}

{Phone} | {Email} | {LinkedIn URL} | {Location}

---

## SUMMARY

{2-3 sentences: years of experience, primary discipline, key differentiator, quantified impact}

---

## PROFESSIONAL EXPERIENCE

### {Job Title}
**{Company Name}**
{Mon YYYY - Mon YYYY}

- {Achievement with quantified result}
- {Achievement demonstrating key skill from job description}
- {Achievement showing scale/scope}

### {Job Title}
**{Company Name}**
{Mon YYYY - Mon YYYY}

- {Achievement bullets, 3-5 per role}

---

## SKILLS

**{Category}:** {Skill}, {Skill}, {Skill}, {Skill}

**{Category}:** {Skill}, {Skill}, {Skill}, {Skill}

---

## EDUCATION

**{Degree}, {Major}** - {University Name}, {Year}

---

## CERTIFICATIONS

- {Certification Name} - {Issuer}, {Year}
- {Certification Name} - {Issuer}, {Year}
```

---

### Modern Professional Template

> **Note:** The `<style>` block below documents the intended visual styling. Actual formatting is handled by `generate_word_docs.py` / `generate_word_docs_web.py`.

```markdown
<style>
h1 { color: #1a5276; margin-bottom: 4px; }
h2 { color: #1a5276; border-bottom: 2px solid #1a5276; padding-bottom: 4px; font-size: 14px; }
h3 { color: #1a202c; margin-bottom: 2px; }
</style>

# {Full Name}

**{Target Role Title}**

{Phone} | {Email} | {LinkedIn} | {Portfolio/Calendar Link}

---

## Summary

{2-3 sentences maximum. Lead with years + discipline. Include key differentiator matching target role. End with quantified impact statement.}

---

## Technical Skills

**{Category 1}:** {Skill}, {Skill}, {Skill}, {Skill}

**{Category 2}:** {Skill}, {Skill}, {Skill}, {Skill}

**{Category 3}:** {Skill}, {Skill}, {Skill}, {Skill}

---

## Professional Experience

### {Job Title}
**{Company Name}**
{Mon YYYY - Present}

- {**Bold the metric**} - Action verb + what you did + measurable outcome
- Managed {X}-member team achieving {result}
- Reduced/Increased {metric} from {X} to {Y} ({Z}% improvement)
- Delivered {project} resulting in {business impact}

### {Job Title}
**{Company Name}**
{Mon YYYY - Mon YYYY}

- {Most impressive achievement first}
- {3-5 bullets per recent role, 2-3 for older roles}

---

## Certifications

- **{Certification Name}** - {Issuing Organization}, {Year}
- **{Certification Name}** - {Issuing Organization}, {Year}

---

## Education

**{Degree}, {Major}** - {University Name}
```

---

### Creative Template

> **Note:** The `<style>` block below documents the intended visual styling. Actual formatting is handled by `generate_word_docs.py` / `generate_word_docs_web.py`.

```markdown
<style>
:root { --accent: #805ad5; --accent-light: #e9d8fd; }
h1 { color: var(--accent); font-size: 28px; margin-bottom: 0; }
h2 { color: var(--accent); font-size: 14px; text-transform: uppercase; letter-spacing: 1px; border-bottom: 2px solid var(--accent); }
.subtitle { color: #718096; font-size: 14px; margin-top: 4px; }
.contact { background: var(--accent-light); padding: 8px 12px; border-radius: 4px; margin: 12px 0; }
</style>

<div style="text-align: center;">

# {Full Name}

<p class="subtitle">{Target Title} | {Specialty/Tagline}</p>

<p class="contact">
{Phone} | {Email} | {Portfolio} | {LinkedIn} | {GitHub}
</p>

</div>

---

## Profile

{2-3 sentences with personality. What drives you, what you're known for, your unique approach.}

---

## Core Competencies

| | | |
|---|---|---|
| {Skill Area 1} | {Skill Area 2} | {Skill Area 3} |
| {Skill Area 4} | {Skill Area 5} | {Skill Area 6} |

---

## Experience

### {Job Title}
**{Company Name}**
{Mon YYYY - Present}

- {Achievement with quantified result}
- {Achievement demonstrating creativity/innovation}
- {Achievement showing collaboration/leadership}

### {Job Title}
**{Company Name}**
{Mon YYYY - Mon YYYY}

- {Achievements - can include brief project descriptions}

---

## Education & Certifications

**{Degree}** - {University} | **{Certification}** - {Issuer}, {Year}

---

## Projects / Portfolio

**{Project Name}** - {Brief description + key technologies + link}

**{Project Name}** - {Brief description + key technologies + link}
```

---

## Writing Guidelines

### Summary Section
- Lead with years of experience + primary role
- Include 1-2 specific skills matching job requirements
- End with impact statement or unique qualifier
- NO objectives, NO "seeking opportunities"

**Good example:**
> Senior Product Owner with 10+ years of agile product ownership and 10+ years in software development. Proven expertise delivering AI/ML solutions, financial services products, and enterprise integrations. Skilled at translating complex technical concepts for stakeholders while driving delivery in fast-changing environments.

### Experience Bullets

**Formula: Action Verb + Task/Project + Quantified Result**

- DO: "Reduced vendor migration costs from **$7M to $3.5M** through strategic planning and stakeholder alignment"
- DON'T: "Responsible for vendor migration planning"

**Strong action verbs:**
- Delivered, Architected, Implemented, Reduced, Increased, Achieved
- Led, Managed, Coordinated, Facilitated, Mentored
- Designed, Built, Developed, Created, Launched
- Optimized, Improved, Streamlined, Automated, Transformed

### Quantification Examples
- Percentages: "Improved velocity by **60%**"
- Dollar amounts: "Reduced costs from **$7M to $3.5M**"
- Scale: "Serving **717,000 clients**"
- Time: "From **2 weeks to 2 hours**"
- Team size: "Managed **15-member** team"
- Coverage: "Improved test coverage to **80%+**"

---

## Visual Hierarchy Techniques

### Bold for Emphasis
Bold the most important elements in each bullet:
- Metrics and numbers
- Key technologies matching job description
- Impressive outcomes

### Scannable Layout
- First bullet of each job = most impressive achievement
- Keep bullets to 1-2 lines maximum
- Group related skills in categories
- Use consistent formatting throughout

### White Space
- 1-inch margins (0.75 for Modern/Creative if needed)
- 1.15-1.5 line spacing
- Clear section breaks with horizontal rules
- Don't cram - one strong page beats two weak pages

---

## Length Guidelines

**Target: 1 page preferred, 2 pages maximum**

### For 1-page resume:
- Summary: 2-3 lines
- Skills: 3-4 categories
- Experience: 3-4 most relevant roles, 3-4 bullets each
- Certifications: Most relevant only
- Education: Degrees only, no details

### For 2-page resume (10+ years experience):
- All above plus:
- More complete experience history
- Additional certifications
- Project highlights section if applicable

---

## ATS Optimization Checklist

- [ ] Standard section headers (Summary, Skills, Experience, Education)
- [ ] Consistent date format throughout (Mon YYYY)
- [ ] Job title keywords in summary and experience
- [ ] Skills match job description terminology exactly
- [ ] No tables for main content (sidebar okay)
- [ ] No images or graphics in content area
- [ ] Company names clearly stated
- [ ] Dates for each position
- [ ] Output as .docx (preferred by recruiters and ATS systems)
- [ ] File under 2MB

---

## ATS-Optimized Experience Format

**Critical for "Fill from Resume" features:** Many ATS systems (Workday, Taleo, iCIMS, Greenhouse) parse job entries by looking for distinct elements on separate lines.

### Recommended Format (3-line header):
```
Job Title           (bold, 11pt - on its own line)
Company Name        (bold, 10pt - on its own line)
Mon YYYY - Mon YYYY (regular, 10pt - on its own line)
```

### Why This Works:
1. **Job Title on its own line** - ATS can clearly identify the role
2. **Company Name on its own line** - Prevents confusion with dates or location
3. **Dates on their own line** - Enables accurate tenure calculation
4. **No pipe separators** - Pipes (`|`) aren't universally recognized delimiters
5. **Bold company name** - Adds visual hierarchy for human readers too

### Avoid These Formats:
```
❌ Job Title
   Company Name | Jan 2020 - Present    (company/dates combined)

❌ Job Title | Company Name | Dates     (all on one line)

❌ Company Name (Jan 2020 - Present)    (dates in parentheses)
```

### Date Format Best Practices:
- Always include month AND year: `Jan 2020 - Present`
- Use consistent format throughout: Don't mix `01/2020` with `January 2020`
- Spell out month abbreviations: `Jan`, `Feb`, `Mar` (not `1`, `2`, `3`)
- Some ATS default missing months to January 1st, which can affect tenure calculations
