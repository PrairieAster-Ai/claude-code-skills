# Style Presets Reference

Visual styling specifications for resume and cover letter generation. All presets maintain ATS compatibility while optimizing for human reviewers.

> **Implementation note:** The document generator (`generate_word_docs.py`) currently implements the **Modern Professional** style only. Classic and Creative presets are defined here as reference specifications for future implementation. When Claude selects a style, the content strategy (tone, structure, keyword emphasis) should match the selected preset, but the visual output (colors, fonts, spacing) will use Modern Professional styling.

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
- **Name:** 22pt, bold (accent color)
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

### Header Layout
- Name: 22-24pt, accent color, bold
- Contact: pipe-separated on one line, 10pt secondary color
- Accent-colored horizontal rule below contact info

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

### Header Layout
- Name: 22-24pt, accent color, bold
- Target title: 12pt, bold, below name
- Contact: pipe-separated on one line, 10pt secondary color
- Accent-colored horizontal rule below contact info

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

**Accent colors by creative sub-industry** (use only for large text 18pt+ bold or decorative elements — many do not meet WCAG AA 4.5:1 for body text on white):
- Design/UX: Coral `#f56565` or Purple `#805ad5`
- Marketing: Orange `#dd6b20` or Magenta `#d53f8c`
- Advertising: Bold Blue `#3182ce` or Yellow `#d69e2e`
- Startups: Teal `#319795` or Green `#38a169`
- Media: Red `#c53030` or Deep Purple `#6b46c1`

Body text should always use `#2d3748` (Dark Gray, 10:1 contrast) regardless of accent choice.

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

### Header Layout
- Name: 24-32pt, accent color, bold display weight
- Target title + specialty: below name
- Contact: pipe-separated, 10pt secondary color
- Creative elements (color blocks, gradients) limited to header area only

### Skills Section (Creative)
```markdown
## Skills

**Design:** Figma | Sketch | Adobe Creative Suite | Prototyping

**Development:** HTML/CSS | JavaScript | React | Responsive Design

**Strategy:** User Research | A/B Testing | Analytics | Brand Development
```

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
| Name | 22pt | 20-24pt | 24-32pt |
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
- [ ] Output as .docx (preferred by recruiters and ATS systems)
- [ ] No headers/footers with critical information
- [ ] Font size minimum 10pt
- [ ] Margins minimum 0.5 inch
- [ ] File size under 2MB

---

## Accessibility Guidelines

All color choices should meet **WCAG AA standards** for readability:

- **Body text:** Minimum 4.5:1 contrast ratio (target 7:1+ for aging readers)
- **Large text (18pt+):** Minimum 3:1 contrast ratio
- **Test colors:** https://webaim.org/resources/contrastchecker/

**Why this matters:** Hiring managers and recruiters often review dozens of resumes. High-contrast text reduces eye strain and ensures your content is readable in various lighting conditions, on different screens, and by readers of all ages.
