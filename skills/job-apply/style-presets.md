# Style Presets Reference

Visual styling specifications for resume and cover letter generation. All presets maintain ATS compatibility while optimizing for human reviewers.

## The 6-Second Rule

Hiring managers spend **6-10 seconds** scanning a resume before deciding to read further. Design elements should:
- Draw attention to name and title immediately
- Make key achievements scannable
- Create clear visual hierarchy
- Not distract from content

---

## Preset 1: Classic

**Best for:** Finance, Banking, Law, Government, Healthcare, Insurance, Accounting, Traditional Corporate

**Philosophy:** Conservative industries value precision, tradition, and risk-aversion. A clean, understated design signals cultural fit and professionalism.

### Layout
- **Single column only** - no sidebars or multi-column layouts
- **Margins:** 1 inch all sides
- **Line spacing:** 1.15
- **Section spacing:** 16-20pt between sections

### Typography
- **Name:** 18-20pt, bold
- **Section headers:** 12-14pt, bold, UPPERCASE or Title Case
- **Body text:** 11pt
- **Font family:** Calibri, Arial, Garamond, or Georgia

### Color Palette (WCAG AA Accessible)
| Element | Color | Hex Code | Contrast |
|---------|-------|----------|----------|
| Primary text | Black | `#000000` | 21:1 |
| Accent (headers, lines) | Navy Blue | `#1a365d` | 12:1 |
| Secondary text | Dark Gray | `#374151` | 10:1 |

**Alternative accents by sub-industry:**
- Finance/Banking: Navy Blue `#1a365d`
- Law: Charcoal `#2d3748`
- Healthcare: Dark Teal `#234e52`
- Government: Navy or Black only

### Visual Elements
- **Dividers:** Single thin horizontal line (1pt) between sections
- **Bullets:** Standard round bullets only
- **Icons:** None
- **Graphics:** None
- **Photos:** Never (in US/UK markets)

### Markdown Template Header
```markdown
# {Name}

{Phone} | {Email} | {LinkedIn} | {Location}

---
```

---

## Preset 2: Modern Professional

**Best for:** Tech, Corporate, Consulting, Enterprise Software, B2B, Engineering, Product Management

**Philosophy:** Balance professionalism with contemporary design. Signal that you're current and efficient while remaining appropriate for corporate environments.

### Layout
- **Single column preferred**, subtle two-column acceptable for contact/skills sidebar
- **Margins:** 0.75-1 inch
- **Line spacing:** 1.0 (single) for compact documents, 1.15 if space allows
- **Section spacing:** 10-14pt between sections

### Typography
- **Name:** 20-24pt, bold
- **Section headers:** 13-14pt, bold
- **Body text:** 10-11pt
- **Font family:** Calibri, Inter, Roboto, Lato, Helvetica

### Color Palette (WCAG AA Accessible - 7:1+ contrast)
| Element | Color | Hex Code | Contrast |
|---------|-------|----------|----------|
| Primary text | Near-black | `#1a202c` | 16:1 |
| Accent primary | Navy Blue | `#1a5276` | 8:1 |
| Accent secondary | Dark Gray | `#374151` | 10:1 |
| Highlight (optional) | Light Blue background | `#ebf8ff` | N/A |

**Alternative accents by sub-industry (all WCAG AA compliant):**
- Tech/Software: Navy `#1a5276` or Dark Teal `#115e59`
- Consulting: Deep Navy `#1e3a5f`
- Product/PM: Charcoal `#374151`
- Engineering: Dark Blue `#1e40af`
- Manufacturing: Navy `#1a5276`

### Visual Elements
- **Dividers:** Horizontal lines with slight accent color
- **Bullets:** Round or square, consistent throughout
- **Icons:** Minimal - contact info only (phone, email, LinkedIn icons acceptable)
- **Graphics:** None in body; subtle header styling okay
- **Name styling:** Can include colored accent bar or underline

### Markdown Template Header
```markdown
<div style="border-left: 4px solid #2b6cb0; padding-left: 12px;">

# {Name}
**{Target Title}**

</div>

{Phone} | {Email} | {LinkedIn} | {Portfolio}

---
```

### Two-Column Variant (Contact Sidebar)
```markdown
# {Name}

**{Target Title}**

---

| | |
|---|---|
| **Contact** | **Summary** |
| {Phone} | {2-3 sentence summary} |
| {Email} | |
| {LinkedIn} | |
| {Location} | |

---
```

---

## Preset 3: Creative

**Best for:** Design, Marketing, Advertising, Startups, Agency, UX/UI, Brand, Media, Entertainment

**Philosophy:** Your resume is a work sample. Show design sensibility while maintaining readability. Personality matters, but content still rules.

### Layout
- **Two-column acceptable** - sidebar for skills/contact
- **Asymmetric layouts** permitted
- **Margins:** 0.5-0.75 inch
- **Line spacing:** 1.2-1.4
- **Section spacing:** 12-16pt between sections

### Typography
- **Name:** 24-32pt, can use display weight
- **Section headers:** 12-14pt, bold or semi-bold
- **Body text:** 10-11pt
- **Font family:** Montserrat, Poppins, Open Sans, Raleway, Nunito
- **Font pairing:** Can use two complementary fonts (one display, one body)

### Color Palette
| Element | Color | Hex Code |
|---------|-------|----------|
| Primary text | Dark Gray | `#2d3748` |
| Accent primary | (Industry dependent) | See below |
| Accent secondary | Lighter tint of primary | - |
| Background accent | Very light tint | 5-10% opacity of primary |

**Accent colors by creative sub-industry:**
- Design/UX: Coral `#f56565` or Purple `#805ad5`
- Marketing: Orange `#dd6b20` or Magenta `#d53f8c`
- Advertising: Bold Blue `#3182ce` or Yellow `#d69e2e`
- Startups: Teal `#319795` or Green `#38a169`
- Media: Red `#c53030` or Deep Purple `#6b46c1`

### Visual Elements
- **Dividers:** Can use colored blocks, geometric shapes
- **Bullets:** Custom shapes acceptable, or creative symbols
- **Icons:** Encouraged for contact, skills, section headers
- **Graphics:** Header graphics, subtle background elements okay
- **Name styling:** Creative treatments welcome (color, unique typography)
- **Skills display:** Progress bars, tag clouds, or visual ratings (with text fallback)

### Critical ATS Rule
**Keep creative elements in the header/sidebar only.** The main experience section must follow standard formatting:
- Standard section headers (Experience, Education, Skills)
- Plain text job titles, companies, dates
- Standard bullet points for achievements
- No graphics interrupting the content flow

### Markdown Template Header
```markdown
<div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 24px; margin: -20px -20px 20px -20px;">

# {Name}
### {Target Title} | {Specialty}

{Phone} | {Email} | {Portfolio} | {LinkedIn}

</div>
```

### Skills Section (Creative)
```markdown
## Skills

**Design:** Figma | Sketch | Adobe Creative Suite | Prototyping

**Development:** HTML/CSS | JavaScript | React | Responsive Design

**Strategy:** User Research | A/B Testing | Analytics | Brand Development
```

---

## Fun & Novelty Presets

These presets are available in the **Artifact Edition** (self-contained HTML tool). They produce real, functional resumes and cover letters — just with personality. Great for internal applications, creative industries, or making your friends laugh.

> **Note:** Fun presets are for the artifact only. The CLI edition generates .docx files using the three professional presets above.

### Preset 4: Rogue Buccaneer

**Archetype:** Seafaring adventurer, pirate captain

**Tone:** Nautical metaphor throughout — jobs are "voyages," skills are an "arsenal," experience entries are "exploits." Formal but swashbuckling.

| Element | Value |
|---------|-------|
| Font | Georgia, Times New Roman (serif) |
| Background | Parchment `#f4e8c1` |
| Headings | Navy `#1c2841` |
| Subheadings | Brown `#8b4513` |
| Accent/borders | Gold `#c9b037` |

**Cover letter sections:** Notable Exploits, Arsenal of Talents, Why This Voyage
**Resume sections:** Captain's Summary, Arsenal of Talents, Voyages & Exploits, Charts & Credentials, Letters of Marque

---

### Preset 5: Sorority Scholar

**Archetype:** Ambitious pink powerhouse, legally unstoppable

**Tone:** Enthusiastic, confident, exclamation marks and bold claims — but backed by real evidence. "Yes, I'm THAT Candidate."

| Element | Value |
|---------|-------|
| Font | Georgia, Playfair Display (serif) |
| Headings | Hot pink `#d63384` |
| Borders | Pink `#ff69b4` / `#ffb6c1` |
| Strong text | Pink `#d63384` |

**Cover letter sections:** What I Bring to the Table, Why Me? Why Now?
**Resume sections:** About Me, Superpowers, Experience (a.k.a. How I Conquered the World), Gold Stars & Certifications

---

### Preset 6: Classified Operative

**Archetype:** Secret agent, intelligence operative

**Tone:** Military brevity, uppercase headings, monospace font. Uses "CLASSIFIED" stamp, [REDACTED] placeholders, and mission terminology.

| Element | Value |
|---------|-------|
| Font | Courier New (monospace) |
| Background | Light gray `#fafafa` |
| Headings | Black `#000000` (uppercase, letter-spaced) |
| Subheadings | Red `#c0392b` |
| Border | Heavy `2px solid #333` |
| Special | Rotated "CLASSIFIED" stamp element |

**Cover letter sections:** MISSION RECORD, OPERATIONAL CAPABILITIES, CLOSING BRIEF
**Resume sections:** AGENT PROFILE, OPERATIONAL CAPABILITIES, MISSION HISTORY, TRAINING & CREDENTIALS, CLEARANCES & CERTIFICATIONS

---

### Preset 7: Renaissance Bard

**Archetype:** Shakespearean player, theatrical performer

**Tone:** Iambic pentameter in fixed template text. Early Modern English flavor — "forsooth," "prithee," "thy court." Decorative flourishes between sections.

| Element | Value |
|---------|-------|
| Font | Palatino Linotype, Palatino, Georgia (serif) |
| Background | Cream `#fdf6e3` |
| Headings | Purple `#4b0082` (centered) |
| Subheadings | Burgundy `#800020` (italic) |
| Accent/borders | Gold `#c9b037` |
| Special | Decorative flourish dividers |

**Cover letter sections:** Of Deeds Most Worthy, Acts of Valor True; The Player's Repertoire; The Final Soliloquy
**Resume sections:** The Prologue, Wherein Our Player Speaks; The Player's Repertoire of Worthy Arts; Of Deeds Most Worthy, Acts of Valor True; Of Scholarly Pursuits and Letters Earned

---

## Color Psychology Quick Reference

| Color | Psychology | Best For |
|-------|------------|----------|
| **Navy Blue** | Trust, reliability, stability | Finance, Law, Corporate, Tech |
| **Teal** | Innovation, clarity, calm confidence | Tech, Healthcare, Consulting |
| **Forest Green** | Growth, balance, sustainability | Environmental, Healthcare, Agriculture |
| **Burgundy** | Sophistication, experience, authority | Executive, Traditional industries |
| **Charcoal** | Modern, neutral, professional | Universal safe choice |
| **Purple** | Creativity, innovation, wisdom | Creative, Consulting, Education |
| **Orange** | Energy, enthusiasm, friendliness | Marketing, Sales, Startups |
| **Coral/Salmon** | Approachable, creative, warm | Design, Marketing, HR |

### Color Contrast Requirements
- Minimum contrast ratio: **4.5:1** for body text
- Minimum contrast ratio: **3:1** for large text (18pt+)
- Test with: https://webaim.org/resources/contrastchecker/

---

## Typography Specifications

### Recommended Font Pairings

**Classic:**
- Georgia (headers) + Arial (body)
- Garamond (headers) + Calibri (body)

**Modern Professional:**
- Roboto Bold (headers) + Roboto Regular (body)
- Lato Bold (headers) + Lato Regular (body)
- Inter Semi-Bold (headers) + Inter Regular (body)

**Creative:**
- Montserrat Bold (headers) + Open Sans (body)
- Poppins Semi-Bold (headers) + Lato (body)
- Raleway Bold (headers) + Nunito (body)

### Font Size Hierarchy

| Element | Classic | Modern | Creative |
|---------|---------|--------|----------|
| Name | 18-20pt | 20-24pt | 24-32pt |
| Title/Tagline | 12pt | 12-14pt | 14-16pt |
| Section headers | 12-14pt | 13-14pt | 12-14pt |
| Job titles | 11pt bold | 11pt bold | 11pt bold |
| Body text | 11pt | 10-11pt | 10-11pt |
| Contact info | 10pt | 10pt | 10-11pt |

---

## ATS Compatibility Checklist (All Presets)

Regardless of visual style, ensure:

- [ ] Standard section headers used (Summary, Experience, Education, Skills)
- [ ] Job titles, companies, dates in plain text
- [ ] No text embedded in images
- [ ] No tables for main content (contact sidebar tables okay)
- [ ] Single-column for main content area
- [ ] PDF exported with selectable text
- [ ] No headers/footers with critical information
- [ ] Font size minimum 10pt
- [ ] Margins minimum 0.5 inch
- [ ] File size under 2MB

---

## Rendering Notes

When generating markdown documents:

1. **For immediate use:** Standard markdown renders well in most contexts
2. **For styled PDF:** Include CSS style block at top or use pandoc with custom CSS
3. **For Word conversion:** Stick to standard markdown; avoid HTML blocks
4. **For web portfolio:** HTML/CSS blocks render correctly

### CSS Style Block (Optional)
```html
<style>
:root {
  --accent-color: #1a5276;  /* WCAG AA accessible navy blue */
  --text-primary: #1a202c;
  --text-secondary: #374151;  /* WCAG AA accessible dark gray */
}
h1 { color: var(--accent-color); }
h2 { border-bottom: 2px solid var(--accent-color); padding-bottom: 4px; }
strong { color: var(--text-primary); }
</style>
```

---

## Accessibility Guidelines

All color choices should meet **WCAG AA standards** for readability:

- **Body text:** Minimum 4.5:1 contrast ratio (target 7:1+ for aging readers)
- **Large text (18pt+):** Minimum 3:1 contrast ratio
- **Test colors:** https://webaim.org/resources/contrastchecker/

**Why this matters:** Hiring managers and recruiters often review dozens of resumes. High-contrast text reduces eye strain and ensures your content is readable in various lighting conditions, on different screens, and by readers of all ages.
