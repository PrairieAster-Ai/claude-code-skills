#!/usr/bin/env python3
"""
MCP Server for the Job Application Skill.

Exposes the job-apply skill's document generation, profile management,
and reference materials to Claude Desktop via the Model Context Protocol.

Usage:
    python3 mcp_server.py          # stdio transport (Claude Desktop)
    mcp dev mcp_server.py          # MCP Inspector for testing
"""

import io
import json
import logging
import shutil
import sys
from contextlib import redirect_stdout
from pathlib import Path

# Logging to stderr only — stdout is reserved for JSON-RPC
logging.basicConfig(
    level=logging.INFO,
    stream=sys.stderr,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("job-apply-mcp")

SKILL_DIR = Path(__file__).parent
sys.path.insert(0, str(SKILL_DIR))

# Import generate_word_docs with stdout protection.
# check_dependencies() at module level prints to stdout and calls sys.exit(1)
# if python-docx or pyyaml are missing — both would corrupt JSON-RPC.
DEPS_OK = False
_import_error = None

_captured = io.StringIO()
with redirect_stdout(_captured):
    try:
        from generate_word_docs import (
            generate_application_documents,
            get_candidate_from_config,
            get_config_path,
            get_output_dir,
            get_portfolio_projects,
            get_qualifications,
            load_config,
            log_application,
            open_output_folder,
        )

        DEPS_OK = True
    except SystemExit:
        _import_error = (
            "python-docx or pyyaml is not installed. "
            "Run: pip install python-docx pyyaml"
        )
    except ImportError as exc:
        _import_error = f"Import error: {exc}"

# profiles.py also calls sys.exit(1) if pyyaml is missing
_profiles_ok = False
_profiles_error = None

_captured2 = io.StringIO()
with redirect_stdout(_captured2):
    try:
        from profiles import (
            _set_active_profile,
            get_current_profile_name,
            get_profile_path,
            get_profiles_dir,
        )

        _profiles_ok = True
    except SystemExit:
        _profiles_error = "pyyaml is not installed. Run: pip install pyyaml"
    except ImportError as exc:
        _profiles_error = f"Import error: {exc}"

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("job-apply")

# =============================================================================
# Resources — static reference markdown files
# =============================================================================

RESOURCES = {
    "fit-assessment": ("fit-assessment.md", "Job fit evaluation framework"),
    "style-presets": ("style-presets.md", "Visual styling specifications"),
    "cover-letter-template": (
        "cover-letter-template.md",
        "Cover letter structure guide",
    ),
    "resume-template": ("resume-template.md", "Resume structure guide"),
    "best-practices": ("best-practices.md", "Strategic application advice"),
}


for _key, (_filename, _desc) in RESOURCES.items():
    # Capture loop variables in default arguments
    def _make_reader(filename=_filename, desc=_desc):
        @mcp.resource(
            f"job-apply://reference/{_key}",
            name=_key,
            description=desc,
        )
        def _read() -> str:
            path = SKILL_DIR / filename
            if not path.exists():
                return f"Error: {filename} not found in {SKILL_DIR}"
            return path.read_text(encoding="utf-8")

        return _read

    _make_reader(_filename, _desc)


# =============================================================================
# Tools
# =============================================================================


@mcp.tool()
def load_profile() -> str:
    """Load the active candidate profile from config.yaml.

    Returns candidate contact info, qualifications, portfolio projects,
    output directory, and active profile name as JSON.
    """
    if not DEPS_OK:
        return json.dumps({"error": _import_error})

    config = load_config()
    if config is None:
        return json.dumps(
            {
                "error": (
                    "No config.yaml found. "
                    "Set up your profile by copying config.example.yaml "
                    "to config.yaml and filling in your information."
                ),
                "config_example": str(SKILL_DIR / "config.example.yaml"),
            }
        )

    candidate = get_candidate_from_config(config)
    qualifications = get_qualifications(config)
    portfolio_projects = get_portfolio_projects(config)
    output_dir = str(get_output_dir(config))
    profile_name = get_current_profile_name() if _profiles_ok else None

    return json.dumps(
        {
            "candidate": candidate,
            "qualifications": qualifications,
            "portfolio_projects": portfolio_projects,
            "output_dir": output_dir,
            "profile_name": profile_name,
        },
        indent=2,
    )


@mcp.tool()
def generate_documents(
    job_title: str,
    company: str,
    location: str,
    cover_letter_opening: str,
    cover_letter_sections: str,
    cover_letter_closing: str,
    signature_title: str,
    resume_summary: str,
    resume_skills: str,
    resume_experience: str,
    resume_certifications: str,
    resume_education: str,
    fit_score: int,
) -> str:
    """Generate cover letter and resume Word documents for a job application.

    All JSON parameters should be JSON-encoded strings.

    Args:
        job_title: The job title being applied for.
        company: The company name.
        location: The job location.
        cover_letter_opening: Opening paragraph text.
        cover_letter_sections: JSON array of {title, paragraphs} objects.
            Each paragraphs entry can be a string, a {label, text, highlights} object,
            or a list of bullet strings.
        cover_letter_closing: Closing paragraph text (e.g. "Best regards,").
        signature_title: Title line under signature (e.g. "Senior Developer | Python").
        resume_summary: Professional summary paragraph.
        resume_skills: JSON array of {category, items} objects.
        resume_experience: JSON array of job objects with title, company, dates, bullets.
            Each bullet can be a string or {text, highlights} object.
        resume_certifications: JSON array of certification objects with name, year, issuer.
        resume_education: JSON array of education objects with degree, school.
        fit_score: Overall fit score (0-100) for application logging.
    """
    if not DEPS_OK:
        return json.dumps({"error": _import_error})

    config = load_config()
    if config is None:
        return json.dumps({"error": "No config.yaml found. Run load_profile first."})

    candidate = get_candidate_from_config(config)
    output_dir = str(get_output_dir(config))

    job = {"title": job_title, "company": company, "location": location}

    # Parse JSON string parameters
    try:
        sections = json.loads(cover_letter_sections)
    except (json.JSONDecodeError, TypeError):
        sections = []

    cover_letter = {
        "opening": cover_letter_opening,
        "sections": sections,
        "closing": cover_letter_closing,
        "signature_title": signature_title,
    }

    try:
        skills = json.loads(resume_skills)
    except (json.JSONDecodeError, TypeError):
        skills = []

    try:
        experience = json.loads(resume_experience)
    except (json.JSONDecodeError, TypeError):
        experience = []

    try:
        certifications = json.loads(resume_certifications)
    except (json.JSONDecodeError, TypeError):
        certifications = []

    try:
        education = json.loads(resume_education)
    except (json.JSONDecodeError, TypeError):
        education = []

    resume = {
        "summary": resume_summary,
        "skills": skills,
        "experience": experience,
        "certifications": certifications,
        "education": education,
    }

    # Capture stdout from generate_application_documents (it prints file paths)
    captured = io.StringIO()
    with redirect_stdout(captured):
        cl_path, resume_path = generate_application_documents(
            candidate, job, cover_letter, resume, output_dir
        )
        log_application(company, job_title, fit_score, output_dir)
        open_output_folder(output_dir)

    return json.dumps(
        {
            "cover_letter_path": cl_path,
            "resume_path": resume_path,
            "output_dir": output_dir,
            "message": f"Documents generated for {job_title} at {company}.",
        },
        indent=2,
    )


@mcp.tool()
def list_profiles() -> str:
    """List all saved candidate profiles and which one is active."""
    if not _profiles_ok:
        return json.dumps({"error": _profiles_error})

    profiles_dir = get_profiles_dir()
    profile_names = sorted(p.stem for p in profiles_dir.glob("*.yaml"))
    current = get_current_profile_name()

    profiles = []
    for name in profile_names:
        profiles.append({"name": name, "active": name == current})

    return json.dumps(
        {"profiles": profiles, "active_profile": current},
        indent=2,
    )


@mcp.tool()
def switch_profile(name: str) -> str:
    """Switch to a saved candidate profile.

    Args:
        name: The profile name to switch to.
    """
    if not _profiles_ok:
        return json.dumps({"error": _profiles_error})

    profile_path = get_profile_path(name)
    if not profile_path.exists():
        profiles_dir = get_profiles_dir()
        available = sorted(p.stem for p in profiles_dir.glob("*.yaml"))
        return json.dumps(
            {
                "error": f"Profile '{name}' not found.",
                "available_profiles": available,
            }
        )

    config_path = get_config_path()
    shutil.copy(profile_path, config_path)
    _set_active_profile(name)

    return json.dumps({"message": f"Switched to profile '{name}'."})


@mcp.tool()
def save_profile(name: str) -> str:
    """Save the current config.yaml as a named profile.

    Args:
        name: The name to save the profile as. Overwrites if it already exists.
    """
    if not _profiles_ok:
        return json.dumps({"error": _profiles_error})

    config_path = get_config_path()
    if not config_path.exists():
        return json.dumps(
            {"error": "No active config.yaml to save. Set up your profile first."}
        )

    profile_path = get_profile_path(name)
    shutil.copy(config_path, profile_path)
    _set_active_profile(name)

    return json.dumps(
        {
            "message": f"Profile '{name}' saved.",
            "path": str(profile_path),
        }
    )


# =============================================================================
# Prompt — full application workflow
# =============================================================================


@mcp.prompt()
def apply_to_job(job_description: str) -> str:
    """Full job application workflow: assess fit, compose content, generate documents.

    Args:
        job_description: The full text of the job posting to apply to.
    """
    return f"""I want to apply for a job. Here is the job description:

---
{job_description}
---

Please follow this workflow:

1. **Load my profile** — Call the `load_profile` tool to get my candidate info, qualifications, and portfolio projects. If it returns an error, help me set up config.yaml first.

2. **Assess job fit** — Read the `job-apply://reference/fit-assessment` and `job-apply://reference/best-practices` resources. Then evaluate my qualifications against the job requirements:
   - Categorize each requirement as Must-Have or Nice-to-Have
   - Rate each: Strong Match (1.0), Partial Match (0.5), or Gap (0.0)
   - Calculate: Overall Score = (Must-Have Score × 0.70) + (Nice-to-Have Score × 0.30)
   - Check for disqualifiers
   - Present the assessment with scores, strengths, gaps, and recommendation

3. **Wait for my confirmation** before proceeding. If I want to skip, stop here.

4. **Compose application content** — Read the `job-apply://reference/cover-letter-template` and `job-apply://reference/resume-template` resources. Also read `job-apply://reference/style-presets` to determine the right content tone. Then compose:
   - Cover letter: opening, 2-3 evidence sections, closing (1 page max, no generic phrases)
   - Resume: tailored summary, skills, experience with quantified achievements, certs, education
   - Address gaps with transferable skills; reference portfolio projects where relevant

5. **Generate documents** — Call `generate_documents` with all composed content and the fit score.

6. **Present summary** — Show file paths, fit score, key matches, gaps addressed, and interview prep tips for gap areas."""


# =============================================================================
# Entry point
# =============================================================================

if __name__ == "__main__":
    mcp.run(transport="stdio")
