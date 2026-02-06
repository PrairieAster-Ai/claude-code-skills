#!/usr/bin/env python3
"""
Manual test script for generate_word_docs_web.py

Run from the skill directory:
    python3 test_web_manual.py

Tests:
1. Document generation with sample data → cover letter + resume .docx
2. Profile YAML round-trip → generate then load
3. Resume .docx parsing → extract text from generated resume

All output goes to /tmp/job-apply-test/. Inspect the .docx files manually.
"""

import sys
import os
from pathlib import Path

# Import the web module from the same directory
sys.path.insert(0, str(Path(__file__).parent))
from generate_word_docs_web import (
    generate_application_documents,
    generate_profile_yaml,
    load_profile_yaml,
    parse_uploaded_resume,
)

OUTPUT_DIR = "/tmp/job-apply-test/"

# Sample data matching the schema from SKILL.md / generate_word_docs.py
SAMPLE_CANDIDATE = {
    "name": "Alex Rivera",
    "phone": "555.867.5309",
    "email": "alex.rivera@example.com",
    "linkedin": "linkedin.com/in/alexrivera",
    "calendar": "",
    "title": "Senior Software Engineer",
}

SAMPLE_JOB = {
    "title": "Staff Engineer",
    "company": "Acme Corp",
    "location": "Remote",
}

SAMPLE_COVER_LETTER = {
    "opening": (
        "With 8 years of full-stack experience and a track record of leading "
        "platform migrations serving millions of users, I'm excited to bring "
        "my expertise to the Staff Engineer role at Acme Corp."
    ),
    "sections": [
        {
            "title": "Technical Leadership",
            "paragraphs": [
                {
                    "label": "Platform Migration",
                    "text": (
                        "Led a team of 6 engineers through a 14-month migration "
                        "from monolith to microservices, reducing deployment time "
                        "from 4 hours to 12 minutes."
                    ),
                    "highlights": ["6 engineers", "4 hours to 12 minutes"],
                },
                [
                    "Designed event-driven architecture handling 50K req/sec",
                    "Mentored 3 junior engineers to mid-level promotions",
                ],
            ],
        },
        {
            "title": "Why Acme Corp",
            "paragraphs": [
                (
                    "Your commitment to developer experience aligns with my "
                    "passion for building tools that make engineering teams "
                    "more productive."
                ),
            ],
        },
    ],
    "closing": "I'd welcome the chance to discuss how I can contribute. Best regards,",
    "signature_title": "Senior Software Engineer",
}

SAMPLE_RESUME = {
    "summary": (
        "Full-stack engineer with 8 years of experience building scalable "
        "distributed systems. Led platform migration serving 2M+ users. "
        "Passionate about developer experience and engineering culture."
    ),
    "skills": [
        {"category": "Languages", "items": "Python, TypeScript, Go, Rust"},
        {"category": "Infrastructure", "items": "AWS, Kubernetes, Terraform, Docker"},
        {"category": "Databases", "items": "PostgreSQL, Redis, DynamoDB, Elasticsearch"},
    ],
    "experience": [
        {
            "title": "Senior Software Engineer",
            "company": "BigTech Inc.",
            "dates": "Mar 2021 - Present",
            "bullets": [
                {
                    "text": "Led team of 6 through monolith-to-microservices migration, reducing deploy time from 4 hours to 12 minutes",
                    "highlights": ["6", "4 hours to 12 minutes"],
                },
                {
                    "text": "Designed event-driven architecture processing 50K requests/second with 99.9% uptime",
                    "highlights": ["50K requests/second", "99.9% uptime"],
                },
                "Introduced trunk-based development, cutting release cycle from 2 weeks to daily",
            ],
        },
        {
            "title": "Software Engineer",
            "company": "StartupCo",
            "dates": "Jun 2018 - Feb 2021",
            "bullets": [
                {
                    "text": "Built real-time analytics pipeline processing 10M events/day",
                    "highlights": ["10M events/day"],
                },
                "Implemented CI/CD pipeline reducing build times by 60%",
            ],
        },
    ],
    "certifications": [
        {"name": "AWS Solutions Architect Professional", "detail": "2023"},
        {"name": "Certified Kubernetes Administrator", "detail": "2022"},
    ],
    "education": [
        {"degree": "BS Computer Science", "school": "State University"},
    ],
}

SAMPLE_QUALIFICATIONS = {
    "summary": SAMPLE_RESUME["summary"],
    "skills": SAMPLE_RESUME["skills"],
    "experience": SAMPLE_RESUME["experience"],
    "certifications": [
        {"name": "AWS Solutions Architect Professional", "year": "2023"},
        {"name": "Certified Kubernetes Administrator", "year": "2022"},
    ],
    "education": SAMPLE_RESUME["education"],
}


def test_document_generation():
    """Test 1: Generate cover letter and resume .docx files."""
    print("=" * 60)
    print("TEST 1: Document Generation")
    print("=" * 60)

    cl_path, resume_path = generate_application_documents(
        candidate=SAMPLE_CANDIDATE,
        job=SAMPLE_JOB,
        cover_letter=SAMPLE_COVER_LETTER,
        resume=SAMPLE_RESUME,
        output_dir=OUTPUT_DIR,
    )

    cl_ok = Path(cl_path).exists() and Path(cl_path).stat().st_size > 0
    resume_ok = Path(resume_path).exists() and Path(resume_path).stat().st_size > 0

    print(f"  Cover letter: {'PASS' if cl_ok else 'FAIL'} ({Path(cl_path).stat().st_size:,} bytes)")
    print(f"  Resume:       {'PASS' if resume_ok else 'FAIL'} ({Path(resume_path).stat().st_size:,} bytes)")
    print(f"  Inspect at:   {OUTPUT_DIR}")
    print()
    return cl_ok and resume_ok, resume_path


def test_profile_roundtrip():
    """Test 2: Generate profile.yaml then load it back."""
    print("=" * 60)
    print("TEST 2: Profile YAML Round-Trip")
    print("=" * 60)

    profile_path = os.path.join(OUTPUT_DIR, "profile.yaml")
    generate_profile_yaml(SAMPLE_CANDIDATE, SAMPLE_QUALIFICATIONS, output_path=profile_path)

    candidate, qualifications = load_profile_yaml(profile_path)

    name_ok = candidate and candidate.get("name") == SAMPLE_CANDIDATE["name"]
    exp_ok = qualifications and len(qualifications.get("experience", [])) == 2
    skills_ok = qualifications and len(qualifications.get("skills", [])) == 3

    print(f"  Name match:       {'PASS' if name_ok else 'FAIL'}")
    print(f"  Experience count:  {'PASS' if exp_ok else 'FAIL'}")
    print(f"  Skills count:      {'PASS' if skills_ok else 'FAIL'}")
    print(f"  Profile at:        {profile_path}")
    print()
    return name_ok and exp_ok and skills_ok


def test_resume_parsing(resume_path):
    """Test 3: Parse text from the generated resume .docx."""
    print("=" * 60)
    print("TEST 3: Resume .docx Parsing")
    print("=" * 60)

    text = parse_uploaded_resume(resume_path)

    has_text = text is not None and len(text) > 100
    has_name = text is not None and "Alex Rivera" in text
    has_skill = text is not None and "Python" in text

    print(f"  Extracted text:  {'PASS' if has_text else 'FAIL'} ({len(text) if text else 0} chars)")
    print(f"  Contains name:   {'PASS' if has_name else 'FAIL'}")
    print(f"  Contains skills: {'PASS' if has_skill else 'FAIL'}")
    if text:
        preview = text[:200].replace("\n", " | ")
        print(f"  Preview: {preview}...")
    print()
    return has_text and has_name and has_skill


def main():
    print()
    print("Job Apply Web Chat — Manual Test Suite")
    print("=" * 60)
    print(f"Output directory: {OUTPUT_DIR}")
    print()

    Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)

    results = []

    ok, resume_path = test_document_generation()
    results.append(("Document Generation", ok))

    ok = test_profile_roundtrip()
    results.append(("Profile Round-Trip", ok))

    ok = test_resume_parsing(resume_path)
    results.append(("Resume Parsing", ok))

    # Summary
    print("=" * 60)
    print("SUMMARY")
    print("=" * 60)
    all_pass = True
    for name, passed in results:
        status = "PASS" if passed else "FAIL"
        print(f"  {status}  {name}")
        if not passed:
            all_pass = False

    print()
    if all_pass:
        print("All tests passed. Open the .docx files in Word to inspect formatting.")
    else:
        print("Some tests failed. Check output above.")

    print(f"\nOutput files in: {OUTPUT_DIR}")
    print()
    return 0 if all_pass else 1


if __name__ == "__main__":
    sys.exit(main())
