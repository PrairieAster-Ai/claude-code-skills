#!/usr/bin/env python3
"""
Generate styled Word documents for job applications.

This module creates ATS-friendly, professionally styled cover letters and resumes
in Microsoft Word format (.docx) with WCAG AA accessible colors.

Usage:
    from generate_word_docs import generate_application_documents

    generate_application_documents(
        candidate=candidate_data,
        job=job_data,
        cover_letter=cover_letter_content,
        resume=resume_content,
        output_dir="/path/to/output"
    )
"""

import sys
import platform

def check_dependencies():
    """Check that required dependencies are installed and provide helpful error messages."""
    missing = []

    try:
        import docx
    except ImportError:
        missing.append("python-docx")

    try:
        import yaml
    except ImportError:
        missing.append("pyyaml")

    if missing:
        print(f"ERROR: Missing required dependencies: {', '.join(missing)}")
        print()

        system = platform.system()
        packages = ' '.join(missing)

        if system == "Darwin":  # macOS
            print("On macOS, use a virtual environment to install dependencies:")
            print()
            print("    python3 -m venv ~/.claude-venv")
            print("    source ~/.claude-venv/bin/activate")
            print(f"    pip install {packages}")
            print()
            print("Then add to your ~/.zshrc to auto-activate:")
            print("    source ~/.claude-venv/bin/activate")
        elif system == "Windows":
            print("On Windows, install with:")
            print()
            print(f"    pip install {packages}")
            print()
            print("Or use a virtual environment:")
            print()
            print("    python -m venv %USERPROFILE%\\.claude-venv")
            print("    %USERPROFILE%\\.claude-venv\\Scripts\\activate.bat")
            print(f"    pip install {packages}")
        else:  # Linux and others
            print("Install with:")
            print(f"    pip3 install {packages} --user")

        print()
        sys.exit(1)

check_dependencies()

from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_LINE_SPACING
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
from datetime import datetime
from pathlib import Path
import re
import yaml


# =============================================================================
# WCAG AA Accessible Colors (7:1+ contrast ratio on white)
# =============================================================================
ACCENT_COLOR = RGBColor(0x1a, 0x52, 0x76)  # Navy Blue #1a5276 - 8:1 contrast
TEXT_PRIMARY = RGBColor(0x1a, 0x20, 0x2c)  # Near-black #1a202c - 16:1 contrast
TEXT_SECONDARY = RGBColor(0x37, 0x41, 0x51)  # Dark Gray #374151 - 10:1 contrast

# Spacing constants
SPACE_BEFORE_HEADING = Pt(14)  # Space before section headings
SPACE_AFTER_HEADING = Pt(10)   # Padding under section headings (~15px)


# =============================================================================
# Helper Functions
# =============================================================================

def set_document_single_spacing(doc):
    """Set single line spacing as default for the entire document.

    Note: Only sets line spacing rule, not paragraph spacing (space_before/space_after).
    This allows individual paragraphs to control their own spacing while maintaining
    single line spacing within paragraphs.
    """
    style = doc.styles['Normal']
    style.paragraph_format.line_spacing_rule = WD_LINE_SPACING.SINGLE
    # Don't set space_after/space_before to 0 - let individual paragraphs control their spacing

    if 'List Bullet' in doc.styles:
        list_style = doc.styles['List Bullet']
        list_style.paragraph_format.line_spacing_rule = WD_LINE_SPACING.SINGLE

    # Configure Heading 2 style at the style level for theme consistency.
    # This means changing the Word document theme will update all headings.
    if 'Heading 2' in doc.styles:
        h2_style = doc.styles['Heading 2']
        h2_style.font.bold = True
        h2_style.font.size = Pt(12)
        h2_style.font.color.rgb = ACCENT_COLOR
        h2_style.paragraph_format.line_spacing_rule = WD_LINE_SPACING.SINGLE


def add_horizontal_line(paragraph):
    """Add a colored horizontal line below a paragraph."""
    p = paragraph._p
    pPr = p.get_or_add_pPr()
    pBdr = OxmlElement('w:pBdr')
    bottom = OxmlElement('w:bottom')
    bottom.set(qn('w:val'), 'single')
    bottom.set(qn('w:sz'), '12')  # 1.5pt line
    bottom.set(qn('w:color'), '1a5276')  # Accent color
    pBdr.append(bottom)
    pPr.append(pBdr)


def add_section_heading(doc, text, is_first=False):
    """
    Add a styled section heading with proper spacing.

    Uses Heading 2 paragraph style so ATS parsers can identify section
    boundaries via document structure, not just visual formatting.

    Args:
        doc: Document object
        text: Heading text
        is_first: If True, reduces space before (for first section after header)

    Returns:
        The paragraph object
    """
    section = doc.add_heading(text, level=2)
    section.paragraph_format.space_before = Pt(6) if is_first else SPACE_BEFORE_HEADING
    section.paragraph_format.space_after = SPACE_AFTER_HEADING

    # Override default Heading 2 styling to match our design
    for run in section.runs:
        run.bold = True
        run.font.size = Pt(12)
        run.font.color.rgb = ACCENT_COLOR
        run.font.name = None  # Inherit document default, not heading font
    add_horizontal_line(section)

    return section


def _format_cert_detail(cert):
    """Build certification detail string from either schema.

    Handles both formats:
    - {name, detail} — used by document generator API
    - {name, year, issuer} — used by config.yaml and import_resume.py
    """
    if cert.get('detail'):
        return cert['detail']
    parts = []
    if cert.get('issuer'):
        parts.append(cert['issuer'])
    if cert.get('year'):
        parts.append(cert['year'])
    return ', '.join(str(p) for p in parts)


# =============================================================================
# Character Sanitizer (ATS-unsafe + AI-tell prevention)
# =============================================================================
#
# Two classes of characters get cleaned here:
#
# 1. ATS-unsafe ('<', '>'): Workday and similar ATS systems strip or mangle
#    these during text extraction. The result is a butchered keyword like
#    "Capability Epic Story Task" with the hierarchy markers gone, or worse,
#    the section silently dropped.
#
# 2. AI-tell ('—', '–'): The em-dash has become a recognized indicator of
#    AI-generated writing; recruiters increasingly flag em-dash-heavy prose
#    as likely AI-edited, which carries stigma. We replace with plain
#    hyphens so the prose reads like human keystrokes. En-dash in numeric
#    ranges ("3-4 months") gets the same treatment.
#
# Replacement table:
#
#   ' > ' (hierarchy)        -> ' to '   (ASCII; NOT a Unicode arrow)
#   ' < ' (hierarchy)        -> ' / '    (ASCII; NOT a Unicode arrow)
#   '>N'  (numeric compare)  -> 'over N'
#   '<N'  (numeric compare)  -> 'under N'
#   '—' (em-dash)            -> ' - '   (surrounding whitespace collapsed)
#   '–' (en-dash, ranges)    -> '-'     (e.g. "3–4" -> "3-4")
#
# Sanitization runs once at the top of generate_application_documents() so
# both renderers and any temp-script content benefit. Source data should also
# avoid these characters (see SKILL.md ATS Optimization and AI-Tell Characters
# sections), but this is the defense-in-depth safety net.

_NUMERIC_GT = re.compile(r">\s*(\d)")
_NUMERIC_LT = re.compile(r"<\s*(\d)")
_EMDASH_PADDED = re.compile(r"\s*\u2014\s*")
_ENDASH_NUMERIC = re.compile(r"(\d)\s*\u2013\s*(\d)")


def _sanitize_for_ats(text):
    """Replace ATS-unsafe and AI-tell characters in a single string.

    ATS-unsafe: '<' and '>' get stripped/mangled by Workday and similar.
    AI-tell:    em-dash and numeric-range en-dash read as AI-edited prose
                (recruiters increasingly flag em-dash-heavy text).

    Substitutions are pure ASCII on purpose. Replacing '>' with a Unicode
    arrow (U+2192) fixes Workday but exposes the older parsers, which are
    the ones most likely to garble non-ASCII: Oracle Taleo and iCIMS both
    mangle special characters, and Jobscan's parser testing says to avoid
    arrows outright. ASCII survives every parser in the chain.
    """
    if not isinstance(text, str) or not text:
        return text
    # ATS-unsafe: '<' and '>'
    text = _NUMERIC_GT.sub(r"over \1", text)
    text = _NUMERIC_LT.sub(r"under \1", text)
    # Whatever survives the numeric passes is almost always a hierarchy
    # separator ("Capability > Epic"). Absorb any surrounding whitespace so
    # both "A > B" and "A>B" come out correctly spaced.
    text = re.sub(r"\s*>\s*", " to ", text)
    text = re.sub(r"\s*<\s*", " / ", text)
    # AI-tell: em-dash and numeric-range en-dash
    text = _EMDASH_PADDED.sub(" - ", text)
    text = _ENDASH_NUMERIC.sub(r"\1-\2", text)
    text = text.replace("\u2013", "-")
    return text


def _sanitize_data_for_ats(obj):
    """Recursively sanitize all string values in a nested dict/list structure.

    URLs cannot legally contain '<' or '>' (RFC 3986), so this is safe to
    apply across the entire input data tree including link fields.
    """
    if isinstance(obj, str):
        return _sanitize_for_ats(obj)
    if isinstance(obj, dict):
        return {k: _sanitize_data_for_ats(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_sanitize_data_for_ats(v) for v in obj]
    return obj


def sanitize_filename(text, max_length=50):
    """Convert text to a safe filename component.

    Preserves Unicode letters/numbers (Jose, Muller, field names in other
    scripts) while removing characters that are unsafe or awkward in filenames
    across platforms, and truncating on a word boundary rather than mid-word.

    Args:
        text: Input text to sanitize
        max_length: Maximum length for the sanitized filename component
                   (helps avoid Windows 260-char path limit)
    """
    # Remove characters unsafe in filenames (/ \ : * ? " < > |) plus brackets,
    # commas, semicolons and ampersands, which several upload handlers, mail
    # gateways, URL builders and CSV-backed import tools mangle. '&' is both a
    # shell metacharacter and a URL query separator.
    safe = re.sub(r'[/\\:*?"<>|()\[\]{},;&]', '', text)
    # Replace whitespace and hyphens with underscores
    safe = re.sub(r'[-\s]+', '_', safe)
    # Remove any remaining control characters
    safe = re.sub(r'[\x00-\x1f\x7f]', '', safe)
    # Collapse runs of underscores left behind by removed characters
    safe = re.sub(r'_{2,}', '_', safe)
    safe = safe.strip('._')
    # Truncate on a word boundary so titles are not cut mid-word
    # ("Retrieval Systems" must not become "Retrieval System").
    if len(safe) > max_length:
        cut = safe[:max_length]
        boundary = cut.rfind('_')
        safe = cut[:boundary] if boundary > 0 else cut
    # Strip trailing dots so a company like "Polaris Inc." cannot produce
    # a filename ending in "Inc..docx".
    safe = safe.strip('._')
    return safe or 'unnamed'



# =============================================================================
# Cover Letter Generator
# =============================================================================

def create_cover_letter(candidate, job, content, output_path):
    """
    Create a styled cover letter document.

    Args:
        candidate: dict with keys: name, phone, email, linkedin, calendar
        job: dict with keys: title, company, location, date (optional)
        content: dict with keys: opening, sections (list of {title, paragraphs}),
                 closing, signature_title
        output_path: Full path for output file
    """
    doc = Document()
    set_document_single_spacing(doc)

    # Set margins
    for section in doc.sections:
        section.top_margin = Inches(0.75)
        section.bottom_margin = Inches(0.75)
        section.left_margin = Inches(0.75)
        section.right_margin = Inches(0.75)

    # === HEADER ===
    # Name
    name_p = doc.add_paragraph()
    name_run = name_p.add_run(candidate['name'])
    name_run.bold = True
    name_run.font.size = Pt(22)
    name_run.font.color.rgb = ACCENT_COLOR
    name_p.space_after = Pt(2)

    # Contact info
    contact_parts = [candidate.get('phone', ''), candidate.get('email', ''),
                     candidate.get('linkedin', ''), candidate.get('calendar', '')]
    contact_text = '  |  '.join(p for p in contact_parts if p)

    contact_p = doc.add_paragraph()
    contact_run = contact_p.add_run(contact_text)
    contact_run.font.size = Pt(10)
    contact_run.font.color.rgb = TEXT_SECONDARY
    add_horizontal_line(contact_p)
    contact_p.space_after = Pt(20)  # Space below contact info line

    # === DATE & RECIPIENT ===
    date_str = job.get('date', datetime.now().strftime('%B %d, %Y'))
    doc.add_paragraph(date_str).space_after = Pt(16)  # Space after date

    recipient = doc.add_paragraph()
    recipient.add_run(f"Hiring Manager\n{job['company']}\n{job.get('location', '')}".strip())
    recipient.space_after = Pt(12)

    # Subject line
    subject = doc.add_paragraph()
    subject_run = subject.add_run(f"Re: {job['title']}")
    subject_run.bold = True
    subject.space_after = Pt(16)  # Space after Re: line

    # Salutation
    doc.add_paragraph("Dear Hiring Manager,").space_after = Pt(10)

    # === OPENING PARAGRAPH ===
    opening = doc.add_paragraph()
    opening.add_run(content['opening'])
    opening.space_after = Pt(12)

    # === CONTENT SECTIONS ===
    for i, section in enumerate(content.get('sections', [])):
        if section.get('title'):
            add_section_heading(doc, section['title'], is_first=(i == 0))

        for para_content in section.get('paragraphs', []):
            if isinstance(para_content, dict):
                # Labeled paragraph: {label: "...", text: "...", highlights: [...]}
                p = doc.add_paragraph()
                if para_content.get('label'):
                    p.add_run(f"{para_content['label']}: ").bold = True

                text = para_content.get('text', '')
                highlights = para_content.get('highlights', [])
                _add_text_with_highlights(p, text, highlights)
                _append_bullet_links(p, para_content.get('links', []))
                p.space_after = Pt(8)

            elif isinstance(para_content, list):
                # Bullet list
                for bullet_item in para_content:
                    bullet = doc.add_paragraph(style='List Bullet')
                    if isinstance(bullet_item, dict):
                        if bullet_item.get('label'):
                            bullet.add_run(f"{bullet_item['label']}: ").bold = True
                        _add_text_with_highlights(
                            bullet, bullet_item.get('text', ''),
                            bullet_item.get('highlights', []))
                        _append_bullet_links(bullet, bullet_item.get('links', []))
                    else:
                        bullet.add_run(bullet_item)
                    bullet.space_after = Pt(4)

            else:
                # Plain paragraph
                p = doc.add_paragraph()
                p.add_run(str(para_content))
                p.space_after = Pt(8)

    # === CLOSING ===
    closing_text = content.get('closing', 'Best regards,')
    doc.add_paragraph(closing_text).space_after = Pt(20)

    # Signature
    sig_name = doc.add_paragraph()
    sig_name.add_run(candidate['name']).bold = True
    sig_name.space_after = Pt(2)

    if content.get('signature_title'):
        sig_title = doc.add_paragraph()
        sig_run = sig_title.add_run(content['signature_title'])
        sig_run.font.color.rgb = TEXT_SECONDARY
        sig_run.font.size = Pt(10)

    # Save
    doc.save(output_path)
    return output_path


def _strip_markdown_bold(text):
    """Remove markdown bold markers (**text**) from text, returning plain text."""
    return re.sub(r'\*\*(.+?)\*\*', r'\1', text)


def _add_hyperlink(paragraph, url, text, color="1a5276", size_half_pts="20"):
    """Append a clickable hyperlink run to a paragraph.

    Uses the document's relationship table so the link is a real Word
    hyperlink (clickable in Word, Google Docs, Pages, and online viewers)
    rather than plain text.
    """
    part = paragraph.part
    r_id = part.relate_to(
        url,
        "http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink",
        is_external=True,
    )

    hyperlink = OxmlElement('w:hyperlink')
    hyperlink.set(qn('r:id'), r_id)

    new_run = OxmlElement('w:r')
    rPr = OxmlElement('w:rPr')

    c = OxmlElement('w:color')
    c.set(qn('w:val'), color)
    rPr.append(c)

    u = OxmlElement('w:u')
    u.set(qn('w:val'), 'single')
    rPr.append(u)

    sz = OxmlElement('w:sz')
    sz.set(qn('w:val'), size_half_pts)
    rPr.append(sz)

    new_run.append(rPr)

    t = OxmlElement('w:t')
    t.text = text
    t.set(qn('xml:space'), 'preserve')
    new_run.append(t)

    hyperlink.append(new_run)
    paragraph._p.append(hyperlink)
    return hyperlink


def _append_bullet_links(paragraph, links):
    """Render a bullet's `links` list as ' (label1 | label2)' with real hyperlinks.

    Separator is an ASCII vertical bar, not U+00B7. Older parsers (Taleo,
    iCIMS) mangle non-ASCII punctuation, and the same separator renders the
    contact line, which is the block Greenhouse extracts name, email, phone
    and address from. Jobscan lists the vertical bar as a safe separator.
    """
    if not links:
        return
    paragraph.add_run(' (').bold = False
    for i, link in enumerate(links):
        if i > 0:
            paragraph.add_run(' | ').bold = False
        _add_hyperlink(paragraph, link['url'], link['label'])
    paragraph.add_run(')').bold = False


def _add_text_with_highlights(paragraph, text, highlights):
    """Add text to paragraph with certain phrases bolded.

    Finds all highlight positions, resolves overlaps (longer match wins),
    then emits runs in text order. Non-highlighted text is explicitly set
    to bold=False to prevent style inheritance issues.
    """
    # Strip any markdown bold syntax that Claude may have included
    text = _strip_markdown_bold(text)

    if not highlights:
        paragraph.add_run(text).bold = False
        return

    # Filter out empty/whitespace-only highlights (str.find('') matches everywhere)
    highlights = [h for h in highlights if h and h.strip()]
    if not highlights:
        paragraph.add_run(text).bold = False
        return

    # Find all occurrences with their positions
    spans = []
    for highlight in highlights:
        start = 0
        while True:
            idx = text.find(highlight, start)
            if idx == -1:
                break
            spans.append((idx, idx + len(highlight), highlight))
            start = idx + 1

    if not spans:
        paragraph.add_run(text).bold = False
        return

    # Sort by start position, then longest match first for overlap resolution
    spans.sort(key=lambda s: (s[0], -(s[1] - s[0])))

    # Remove overlapping spans (keep the first/longest at each position)
    merged = []
    for span in spans:
        if merged and span[0] < merged[-1][1]:
            continue
        merged.append(span)

    # Emit runs in text order
    pos = 0
    for start, end, _ in merged:
        if start > pos:
            paragraph.add_run(text[pos:start]).bold = False
        paragraph.add_run(text[start:end]).bold = True
        pos = end

    if pos < len(text):
        paragraph.add_run(text[pos:]).bold = False


# =============================================================================
# Resume Generator
# =============================================================================

def create_resume(candidate, content, output_path):
    """
    Create a styled resume document.

    Args:
        candidate: dict with keys: name, title, phone, email, linkedin, calendar
        content: dict with keys: summary, skills (list of {category, items}),
                 experience (list of jobs), certifications, education
        output_path: Full path for output file
    """
    doc = Document()
    set_document_single_spacing(doc)

    # Set margins
    for section in doc.sections:
        section.top_margin = Inches(0.6)
        section.bottom_margin = Inches(0.5)
        section.left_margin = Inches(0.7)
        section.right_margin = Inches(0.7)

    # === HEADER ===
    # Name
    name_p = doc.add_paragraph()
    name_run = name_p.add_run(candidate['name'])
    name_run.bold = True
    name_run.font.size = Pt(24)
    name_run.font.color.rgb = ACCENT_COLOR
    name_p.space_after = Pt(2)

    # Title
    if candidate.get('title'):
        title_p = doc.add_paragraph()
        title_run = title_p.add_run(candidate['title'])
        title_run.bold = True
        title_run.font.size = Pt(12)
        title_p.space_after = Pt(4)

    # Contact info
    # `location` leads the contact line: recruiters and ATS location filters look for
    # city/state first, and it settles residency questions for location-gated roles.
    contact_parts = [candidate.get('location', ''), candidate.get('phone', ''),
                     candidate.get('email', ''), candidate.get('linkedin', ''),
                     candidate.get('github', ''), candidate.get('calendar', '')]
    contact_text = '  |  '.join(p for p in contact_parts if p)

    contact_p = doc.add_paragraph()
    contact_run = contact_p.add_run(contact_text)
    contact_run.font.size = Pt(10)
    contact_run.font.color.rgb = TEXT_SECONDARY
    contact_p.space_after = Pt(8)

    # === SUMMARY ===
    if content.get('summary'):
        add_section_heading(doc, 'Summary', is_first=True)
        summary_p = doc.add_paragraph()
        summary_p.add_run(content['summary'])
        summary_p.space_after = Pt(6)

    # === SKILLS ===
    # Header must read exactly "Skills": it is one of the canonical ATS section
    # names, and skill categories routinely cover non-technical ground
    # (product management, leadership, governance) that "Technical Skills"
    # mislabels for both the parser and the human skimming the page.
    if content.get('skills'):
        add_section_heading(doc, 'Skills')
        for skill in content['skills']:
            p = doc.add_paragraph()
            p.add_run(f"{skill['category']}:").bold = True
            p.add_run(f" {skill['items']}")
            p.space_after = Pt(4)
        doc.paragraphs[-1].space_after = Pt(6)

    # === PROFESSIONAL EXPERIENCE ===
    if content.get('experience'):
        add_section_heading(doc, 'Professional Experience')

        # Fix combined company|dates format (ATS-critical: must be separate lines)
        for job in content['experience']:
            company = (job.get('company') or '').strip()
            dates = (job.get('dates') or '').strip()
            if not company and '|' in dates:
                parts = dates.split('|', 1)
                if len(parts) == 2 and re.search(r'\b\d{4}\b', parts[1]):
                    job['company'] = parts[0].strip()
                    job['dates'] = parts[1].strip()

        for idx, job in enumerate(content['experience']):
            # Job title - add space before to separate from previous job
            job_title_p = doc.add_paragraph()
            job_title_p.paragraph_format.space_before = Pt(0) if idx == 0 else Pt(12)
            job_title_run = job_title_p.add_run(job['title'])
            job_title_run.bold = True
            job_title_run.font.size = Pt(11)
            job_title_p.space_after = Pt(1)

            # Company name on its own line (ATS-optimized: separate from dates)
            company_text = job['company']
            location = (job.get('location') or '').strip()
            if location:
                company_text = f"{company_text}, {location}"
            company_p = doc.add_paragraph()
            company_run = company_p.add_run(company_text)
            company_run.bold = True
            company_run.font.size = Pt(10)
            company_p.space_after = Pt(1)

            # Dates on separate line (ATS-optimized: clear date parsing)
            dates_p = doc.add_paragraph()
            dates_run = dates_p.add_run(job['dates'])
            dates_run.font.color.rgb = TEXT_SECONDARY
            dates_run.font.size = Pt(10)
            dates_p.space_after = Pt(4)

            # Bullets - indented to group with job entry
            for bullet in job.get('bullets', []):
                bullet_p = doc.add_paragraph(style='List Bullet')
                bullet_p.paragraph_format.left_indent = Inches(0.35)

                if isinstance(bullet, dict):
                    # {text: "...", highlights: [...], links: [{label, url}, ...]}
                    _add_text_with_highlights(bullet_p, bullet['text'],
                                              bullet.get('highlights', []))
                    _append_bullet_links(bullet_p, bullet.get('links', []))
                else:
                    bullet_p.add_run(
                        _strip_markdown_bold(str(bullet))
                    ).bold = False

                bullet_p.space_after = Pt(2)

    # === CERTIFICATIONS ===
    if content.get('certifications'):
        add_section_heading(doc, 'Certifications')
        for cert in content['certifications']:
            cert_p = doc.add_paragraph(style='List Bullet')
            if isinstance(cert, dict):
                cert_p.add_run(cert['name']).bold = True
                detail = _format_cert_detail(cert)
                if detail:
                    cert_p.add_run(f" - {detail}")
            else:
                cert_p.add_run(cert)
            cert_p.space_after = Pt(2)
        doc.paragraphs[-1].space_after = Pt(6)

    # === EDUCATION ===
    if content.get('education'):
        add_section_heading(doc, 'Education')
        for edu in content['education']:
            edu_p = doc.add_paragraph()
            if isinstance(edu, dict):
                edu_p.add_run(edu['degree']).bold = True
                edu_p.add_run(f" - {edu.get('school', '')}")
            else:
                edu_p.add_run(edu)
            edu_p.space_after = Pt(4)

    # Save
    doc.save(output_path)
    return output_path


# =============================================================================
# Main Entry Point
# =============================================================================

def generate_application_documents(candidate, job, cover_letter, resume, output_dir):
    """
    Generate both cover letter and resume documents.

    Args:
        candidate: dict with candidate information
            - name: Full name
            - phone: Phone number
            - email: Email address
            - linkedin: LinkedIn URL
            - calendar: Calendar link (optional)
            - title: Target job title for resume header

        job: dict with job information
            - title: Job title
            - company: Company name
            - location: Job location
            - date: Letter date (optional, defaults to today)

        cover_letter: dict with cover letter content
            - opening: Opening paragraph text
            - sections: List of {title, paragraphs} dicts
            - closing: Closing text (optional)
            - signature_title: Title under signature

        resume: dict with resume content
            - summary: Summary paragraph
            - skills: List of {category, items} dicts
            - experience: List of job dicts with title, company, dates, bullets
            - certifications: List of cert strings or {name, detail} dicts
            - education: List of edu strings or {degree, school} dicts

        output_dir: Directory to save documents

    Returns:
        Tuple of (cover_letter_path, resume_path)
    """
    # ATS sanitization: replace '<' and '>' in all user-visible text fields.
    # Workday and similar systems mangle these characters during extraction.
    candidate = _sanitize_data_for_ats(candidate)
    job = _sanitize_data_for_ats(job)
    cover_letter = _sanitize_data_for_ats(cover_letter)
    resume = _sanitize_data_for_ats(resume)

    output_dir = Path(output_dir).expanduser()
    output_dir.mkdir(parents=True, exist_ok=True)

    # Generate filenames
    name_part = sanitize_filename(candidate['name'])
    role_part = sanitize_filename(job['title'])
    company_part = sanitize_filename(job['company'])

    cl_filename = f"{name_part}_Cover_Letter_{role_part}_{company_part}.docx"
    resume_filename = f"{name_part}_Resume_{role_part}_{company_part}.docx"

    cl_path = output_dir / cl_filename
    resume_path = output_dir / resume_filename

    # Generate documents
    create_cover_letter(candidate, job, cover_letter, str(cl_path))
    print(f"Cover letter saved: {cl_path}")

    create_resume(candidate, resume, str(resume_path))
    print(f"Resume saved: {resume_path}")

    return str(cl_path), str(resume_path)


def open_output_folder(folder_path):
    """Open the output folder in the system file manager.

    Args:
        folder_path: Path to the folder to open

    Returns:
        bool: True if command was executed, False if unsupported platform
    """
    import subprocess

    folder = Path(folder_path).expanduser()

    if not folder.exists():
        print(f"Folder does not exist: {folder}")
        return False

    system = platform.system()

    try:
        if system == "Darwin":  # macOS
            subprocess.run(["open", str(folder)], check=True)
        elif system == "Windows":
            subprocess.run(["explorer", str(folder)], check=True)
        elif system == "Linux":
            # Try common file managers in order
            for cmd in ["xdg-open", "nautilus", "dolphin", "thunar", "pcmanfm"]:
                try:
                    subprocess.run([cmd, str(folder)], check=True,
                                   stderr=subprocess.DEVNULL)
                    break
                except (subprocess.CalledProcessError, FileNotFoundError):
                    continue
        else:
            print(f"Unsupported platform: {system}")
            return False

        return True
    except Exception as e:
        print(f"Could not open folder: {e}")
        return False


def save_job_description(company, role, jd_text, when=None):
    """Archive the raw job description text and return its filename.

    Job descriptions are the only honest source for "what are employers actually
    asking for". Inferring demand from generated resumes does not work: terms
    that live in the candidate's standing config skills line appear in every
    document regardless of what the posting requested.

    Args:
        company: Company name
        role: Job title
        jd_text: Raw job description text, exactly as supplied
        when: datetime to stamp (defaults to now)

    Returns:
        str: Filename relative to job_descriptions/, or '' if jd_text was empty
    """
    from datetime import datetime

    if not jd_text or not jd_text.strip():
        return ''

    when = when or datetime.now()
    jd_dir = Path(__file__).parent / "job_descriptions"
    jd_dir.mkdir(exist_ok=True)

    name = "%s_%s_%s.txt" % (
        when.strftime('%Y-%m-%d'),
        sanitize_filename(company, max_length=40),
        sanitize_filename(role, max_length=60),
    )
    (jd_dir / name).write_text(jd_text, encoding='utf-8')
    return name


def log_application(company, role, fit_score, output_dir, jd_text=None):
    """Log an application to the applications history file.

    Args:
        company: Company name
        role: Job title
        fit_score: Fit assessment score (0-100)
        output_dir: Where documents were saved
        jd_text: Raw job description text. Archived under job_descriptions/ and
            referenced from a sixth column. Older 5-column lines still parse.
    """
    from datetime import datetime

    log_path = Path(__file__).parent / "applications.log"
    now = datetime.now()
    jd_file = save_job_description(company, role, jd_text, when=now)

    entry = f"{now.strftime('%Y-%m-%d %H:%M')}\t{company}\t{role}\t{fit_score}%\t{output_dir}"
    if jd_file:
        entry += f"\t{jd_file}"
    entry += "\n"

    with open(log_path, 'a', encoding='utf-8') as f:
        f.write(entry)


def mark_submitted(company, role, when=None):
    """Mark a logged application as actually submitted.

    The log records when documents were GENERATED, which is not the same as
    applying. The distinction matters: a recruiter may pitch a role that another
    firm has already submitted the candidate for, and duplicate submissions to
    one requisition through two vendors typically get both rejected. Knowing what is actually out is what prevents that.

    Appends a seventh column, submitted=YYYY-MM-DD. Older lines and lines
    without it still parse.

    Args:
        company: Company name, must match the logged entry
        role: Job title, must match the logged entry
        when: date to stamp (defaults to today)

    Returns:
        int: number of log entries updated
    """
    from datetime import datetime

    log_path = Path(__file__).parent / "applications.log"
    if not log_path.exists():
        return 0

    stamp = "submitted=%s" % (when or datetime.now()).strftime('%Y-%m-%d')
    lines, updated = [], 0
    for line in log_path.read_text(encoding='utf-8').splitlines():
        parts = line.split('\t')
        if (len(parts) >= 3 and parts[1] == company and parts[2] == role
                and not any(p.startswith('submitted=') for p in parts)):
            parts.append(stamp)
            updated += 1
        lines.append('\t'.join(parts))
    log_path.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    return updated


def get_application_history():
    """Get list of past applications.

    Returns:
        list: List of dicts with date, company, role, score, path
    """
    log_path = Path(__file__).parent / "applications.log"

    if not log_path.exists():
        return []

    history = []
    with open(log_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            # Support both tab-delimited (new) and pipe-delimited (legacy) formats
            sep = '\t' if '\t' in line else '|'
            parts = [p.strip() for p in line.split(sep)]
            if len(parts) >= 4:
                history.append({
                    'date': parts[0],
                    'company': parts[1],
                    'role': parts[2],
                    'score': parts[3],
                    'path': parts[4] if len(parts) > 4 else '',
                    'jd_file': parts[5] if len(parts) > 5 and not parts[5].startswith('submitted=') else '',
                    'submitted': next((p.split('=', 1)[1] for p in parts if p.startswith('submitted=')), '')
                })

    return history


DEFAULT_SKILL_LEXICON = {
    "roadmap": r"roadmap", "backlog": r"backlog", "user stories": r"user stor",
    "acceptance criteria": r"acceptance criteria", "discovery": r"discovery",
    "personas / journeys": r"persona|user journey|journey map",
    "KPIs / success metrics": r"\bkpi|success metric",
    "prioritization": r"prioriti", "stakeholder management": r"stakeholder",
    "influence without authority": r"without (direct )?authority",
    "cross-functional": r"cross.functional", "product vision": r"product vision",
    "scrum": r"\bscrum\b", "kanban": r"kanban", "SAFe": r"\bsafe\b",
    "Jira": r"\bjira\b", "Confluence": r"confluence", "Azure DevOps": r"azure devops|\bado\b",
    "Rally": r"\brally\b", "Productboard": r"productboard", "Miro": r"\bmiro\b",
    "APIs": r"\bapi", "SQL": r"\bsql\b", "Python": r"python", "Java": r"\bjava\b",
    "cloud": r"\bcloud\b|\baws\b|azure|gcp", "CI/CD": r"ci/cd",
    "data pipelines / ETL": r"\betl\b|data pipeline|data lake|warehous",
    "Databricks": r"databricks", "Snowflake": r"snowflake", "dbt": r"\bdbt\b",
    "Tableau": r"tableau", "Looker": r"looker", "Power BI": r"power ?bi",
    "microservices": r"microservice", "architecture": r"architect",
    "AI / GenAI": r"\bai\b|generative ai|genai", "LLMs": r"\bllm|large language model",
    "RAG / vector search": r"\brag\b|retrieval.augmented|vector (database|db|store)|embedding|semantic search|knowledge graph",
    "MLOps": r"mlops|mlflow|kubeflow|sagemaker", "machine learning": r"machine learning",
    "responsible AI / governance": r"responsible ai|ai governance|ethical ai",
    "EDI": r"\bedi\b|x12|edifact", "ERP": r"\berp\b|netsuite|dynamics|sap",
    "HL7 / FHIR": r"hl7|fhir", "compliance / regulated": r"complian|regulat",
    "security": r"security", "privacy": r"privacy",
    "vendor management": r"vendor", "budget / ROI": r"budget|\broi\b|business case",
    "coaching / mentoring": r"coach|mentor", "UX research / design": r"\bux\b|user research|usability",
    "financial services": r"financial servic|fintech|banking|wealth",
    "healthcare": r"healthcare|clinical|patient", "e-commerce": r"e.commerce|commerce",
    "manufacturing / supply chain": r"manufactur|supply chain",
}


def analyze_job_descriptions(lexicon=None, min_pct=0):
    """Document-frequency analysis over archived job descriptions.

    Counts how many DISTINCT postings mention each term, which is the honest
    measure of employer demand. Raw term counts would let one verbose posting
    dominate, and analysing generated resumes instead would just re-measure the
    candidate's own standing skills line.

    Args:
        lexicon: dict of {label: regex}. Defaults to DEFAULT_SKILL_LEXICON.
        min_pct: suppress terms appearing in fewer than this percent of postings.

    Returns:
        dict with 'count' (postings analysed) and 'terms' (list of
        (label, n, pct) sorted by frequency descending).
    """
    jd_dir = Path(__file__).parent / "job_descriptions"
    if not jd_dir.exists():
        return {'count': 0, 'terms': []}

    docs = []
    for f in sorted(jd_dir.glob("*.txt")):
        try:
            docs.append(f.read_text(encoding='utf-8', errors='replace').lower())
        except OSError:
            continue

    n_docs = len(docs)
    if not n_docs:
        return {'count': 0, 'terms': []}

    lex = lexicon or DEFAULT_SKILL_LEXICON
    rows = []
    for label, pattern in lex.items():
        hits = sum(1 for d in docs if re.search(pattern, d))
        pct = 100.0 * hits / n_docs
        if pct >= min_pct:
            rows.append((label, hits, pct))
    rows.sort(key=lambda r: -r[1])
    return {'count': n_docs, 'terms': rows}


# =============================================================================
# Configuration Loading
# =============================================================================

def get_config_path():
    """Get the path to the config file."""
    return Path(__file__).parent / "config.yaml"


def get_example_config_path():
    """Get the path to the example config file."""
    return Path(__file__).parent / "config.example.yaml"


def load_config():
    """
    Load user configuration from config.yaml.

    Returns:
        dict: Configuration data, or None if config doesn't exist
    """
    config_path = get_config_path()
    if not config_path.exists():
        return None

    with open(config_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def get_candidate_from_config(config=None):
    """
    Extract candidate information from config.

    Args:
        config: Config dict (will load from file if not provided)

    Returns:
        dict: Candidate information for document generation
    """
    if config is None:
        config = load_config()

    if config is None:
        return None

    candidate_config = config.get('candidate', {})
    return {
        'name': candidate_config.get('name', ''),
        'title': candidate_config.get('title', ''),
        'phone': candidate_config.get('phone', ''),
        'email': candidate_config.get('email', ''),
        'linkedin': candidate_config.get('linkedin', ''),
        'calendar': candidate_config.get('calendar', ''),
    }


def get_portfolio_projects(config=None):
    """
    Get portfolio projects from config.

    Args:
        config: Config dict (will load from file if not provided)

    Returns:
        list: Portfolio projects with achievements and technologies
    """
    if config is None:
        config = load_config()

    if config is None:
        return []

    return config.get('portfolio_projects', [])


def get_qualifications(config=None):
    """
    Get qualifications (resume data) from config.

    Args:
        config: Config dict (will load from file if not provided)

    Returns:
        dict: Qualifications including summary, skills, experience,
              certifications, and education. Returns None if not configured.
    """
    if config is None:
        config = load_config()

    if config is None:
        return None

    quals = config.get('qualifications', {})

    # Return None if qualifications section is empty or missing key data
    if not quals or not quals.get('experience'):
        return None

    return {
        'summary': quals.get('summary', ''),
        'skills': quals.get('skills', []),
        'experience': quals.get('experience', []),
        'certifications': quals.get('certifications', []),
        'education': quals.get('education', [])
    }


def get_output_dir(config=None):
    """
    Get output directory from config, with ~ expansion.

    Args:
        config: Config dict (will load from file if not provided)

    Returns:
        Path: Output directory path
    """
    if config is None:
        config = load_config()

    default_dir = "~/Documents/Job Application Docs/generated/"

    if config is None:
        return Path(default_dir).expanduser()

    output_dir = config.get('paths', {}).get('output_dir', default_dir)
    return Path(output_dir).expanduser()


# =============================================================================
# Example Usage / Test
# =============================================================================

if __name__ == "__main__":
    # Check if config exists
    config = load_config()

    if config:
        print("Configuration loaded from config.yaml")
        candidate = get_candidate_from_config(config)
        print(f"  Candidate: {candidate.get('name', 'Not set')}")
        print(f"  Output dir: {get_output_dir(config)}")

        projects = get_portfolio_projects(config)
        if projects:
            print(f"  Portfolio projects: {len(projects)}")
            for p in projects:
                print(f"    - {p.get('name')}")
    else:
        print("No config.yaml found.")
        print("Copy config.example.yaml to config.yaml and fill in your information.")
        print(f"  Example config: {get_example_config_path()}")

    print("\nImport this module to generate documents.")
    print("See generate_application_documents() for the main entry point.")
