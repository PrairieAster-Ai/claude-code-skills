#!/usr/bin/env python3
"""
Resume Import Utility for Job Application Skill

This script helps users import their resume into the config.yaml format.
It can parse resume text and guide users through structuring their qualifications.

Usage:
    python3 import_resume.py                    # Interactive mode
    python3 import_resume.py resume.docx        # Import from Word document
    python3 import_resume.py resume.txt         # Import from text file
"""

import sys
import re
import zipfile
import platform
from pathlib import Path

# Check for pyyaml before importing
try:
    import yaml
except ImportError:
    print("ERROR: Missing required dependency: pyyaml")
    print()
    system = platform.system()
    if system == "Darwin":  # macOS
        print("On macOS, use a virtual environment to install dependencies:")
        print()
        print("    python3 -m venv ~/.claude-venv")
        print("    source ~/.claude-venv/bin/activate")
        print("    pip install pyyaml")
        print()
        print("Then add to your ~/.zshrc to auto-activate:")
        print("    source ~/.claude-venv/bin/activate")
    elif system == "Windows":
        print("On Windows, install with:")
        print()
        print("    pip install pyyaml")
        print()
        print("Or use a virtual environment:")
        print()
        print("    python -m venv %USERPROFILE%\\.claude-venv")
        print("    %USERPROFILE%\\.claude-venv\\Scripts\\activate.bat")
        print("    pip install pyyaml")
    else:  # Linux and others
        print("Install with:")
        print("    pip3 install pyyaml --user")
    print()
    sys.exit(1)


def extract_text_from_docx(file_path):
    """Extract text from a Word document using Python's zipfile module.

    This is cross-platform and doesn't require external tools like unzip.
    """
    try:
        with zipfile.ZipFile(file_path, 'r') as docx:
            # Read the main document XML
            xml_content = docx.read('word/document.xml').decode('utf-8')

        # Preserve paragraph breaks, then remove XML tags
        text = re.sub(r'</w:p>', '\n', xml_content)
        text = re.sub(r'<[^>]+>', ' ', text)
        # Normalize whitespace within lines
        lines = [re.sub(r'[ \t]+', ' ', line).strip() for line in text.split('\n')]
        # Remove empty lines but preserve paragraph structure
        text = '\n'.join(line for line in lines if line)
        return text
    except zipfile.BadZipFile:
        print(f"Error: {file_path} is not a valid .docx file")
        return None
    except KeyError:
        print(f"Error: {file_path} does not contain expected Word document structure")
        return None
    except Exception as e:
        print(f"Error extracting text from {file_path}: {e}")
        return None


def read_text_file(file_path):
    """Read text from a plain text file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except UnicodeDecodeError:
        # Fallback to system default encoding
        try:
            with open(file_path, 'r') as f:
                return f.read()
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
            return None
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return None


def get_config_path():
    """Get the path to the config file."""
    return Path(__file__).parent / "config.yaml"


def get_example_config_path():
    """Get the path to the example config file."""
    return Path(__file__).parent / "config.example.yaml"


def load_config():
    """Load existing config or create from example."""
    config_path = get_config_path()
    example_path = get_example_config_path()

    if config_path.exists():
        with open(config_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    elif example_path.exists():
        with open(example_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    else:
        return {
            'candidate': {},
            'paths': {},
            'preferences': {},
            'qualifications': {},
            'portfolio_projects': []
        }


def save_config(config):
    """Save config to file."""
    config_path = get_config_path()
    with open(config_path, 'w', encoding='utf-8') as f:
        yaml.dump(config, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
    print(f"\nConfiguration saved to: {config_path}")


def prompt_input(prompt, default=None):
    """Prompt user for input with optional default."""
    if default:
        result = input(f"{prompt} [{default}]: ").strip()
        return result if result else default
    else:
        return input(f"{prompt}: ").strip()


def prompt_yes_no(prompt, default=True):
    """Prompt user for yes/no input."""
    default_str = "Y/n" if default else "y/N"
    result = input(f"{prompt} [{default_str}]: ").strip().lower()
    if not result:
        return default
    return result in ('y', 'yes')


def collect_candidate_info(config):
    """Collect candidate contact information."""
    print("\n" + "=" * 60)
    print("CONTACT INFORMATION")
    print("=" * 60)

    candidate = config.get('candidate', {})

    candidate['name'] = prompt_input("Full name", candidate.get('name'))
    candidate['phone'] = prompt_input("Phone number", candidate.get('phone'))
    candidate['email'] = prompt_input("Email address", candidate.get('email'))
    candidate['linkedin'] = prompt_input("LinkedIn URL (without https://)", candidate.get('linkedin'))
    candidate['calendar'] = prompt_input("Calendar link (optional)", candidate.get('calendar', ''))

    config['candidate'] = candidate
    return config


def collect_summary(config):
    """Collect professional summary."""
    print("\n" + "=" * 60)
    print("PROFESSIONAL SUMMARY")
    print("=" * 60)
    print("Enter a 2-3 sentence summary of your professional background.")
    print("(Press Enter twice to finish)")

    if 'qualifications' not in config:
        config['qualifications'] = {}

    existing = config['qualifications'].get('summary', '')
    if existing:
        print(f"\nCurrent summary: {existing[:100]}...")
        if not prompt_yes_no("Replace existing summary?", False):
            return config

    lines = []
    print("\nEnter your summary:")
    while True:
        line = input()
        if not line and lines:
            break
        lines.append(line)

    config['qualifications']['summary'] = ' '.join(lines)
    return config


def collect_skills(config):
    """Collect skills organized by category."""
    print("\n" + "=" * 60)
    print("SKILLS")
    print("=" * 60)
    print("Enter skills organized by category.")

    if 'qualifications' not in config:
        config['qualifications'] = {}

    existing = config['qualifications'].get('skills', [])
    if existing:
        print(f"\nExisting categories: {', '.join(s['category'] for s in existing)}")
        if not prompt_yes_no("Add more skill categories?", True):
            return config

    skills = existing.copy()

    while True:
        print("\n(Leave category empty to finish)")
        category = prompt_input("Skill category (e.g., 'Programming Languages', 'Tools')")
        if not category:
            break

        items = prompt_input(f"Skills in '{category}' (comma-separated)")
        if items:
            skills.append({
                'category': category,
                'items': items
            })

    config['qualifications']['skills'] = skills
    return config


def collect_experience(config):
    """Collect work experience."""
    print("\n" + "=" * 60)
    print("WORK EXPERIENCE")
    print("=" * 60)
    print("Enter your work history, most recent first.")

    if 'qualifications' not in config:
        config['qualifications'] = {}

    existing = config['qualifications'].get('experience', [])
    if existing:
        print(f"\nExisting positions: {len(existing)}")
        for exp in existing:
            print(f"  - {exp.get('title')} at {exp.get('company')}")
        if not prompt_yes_no("Add more positions?", True):
            return config

    experience = existing.copy()

    while True:
        print("\n(Leave job title empty to finish)")
        title = prompt_input("Job title")
        if not title:
            break

        company = prompt_input("Company name")
        dates = prompt_input("Dates (e.g., 'Jan 2020 - Present')")

        print("Enter bullet points for this position (one per line, empty line to finish):")
        bullets = []
        while True:
            bullet_text = input("  • ")
            if not bullet_text:
                break

            highlights_input = input("    Phrases to highlight (comma-separated, or Enter for none): ")
            highlights = [h.strip() for h in highlights_input.split(',')] if highlights_input else []

            bullets.append({
                'text': bullet_text,
                'highlights': highlights
            })

        experience.append({
            'title': title,
            'company': company,
            'dates': dates,
            'bullets': bullets
        })

    config['qualifications']['experience'] = experience
    return config


def collect_certifications(config):
    """Collect certifications."""
    print("\n" + "=" * 60)
    print("CERTIFICATIONS")
    print("=" * 60)

    if 'qualifications' not in config:
        config['qualifications'] = {}

    existing = config['qualifications'].get('certifications', [])
    if existing:
        print(f"\nExisting certifications: {len(existing)}")
        for cert in existing:
            print(f"  - {cert.get('name')}")
        if not prompt_yes_no("Add more certifications?", True):
            return config

    certifications = existing.copy()

    while True:
        print("\n(Leave certification name empty to finish)")
        name = prompt_input("Certification name")
        if not name:
            break

        year = prompt_input("Year earned")
        issuer = prompt_input("Issuing organization (optional)")

        cert = {'name': name, 'year': year}
        if issuer:
            cert['issuer'] = issuer

        certifications.append(cert)

    config['qualifications']['certifications'] = certifications
    return config


def collect_education(config):
    """Collect education."""
    print("\n" + "=" * 60)
    print("EDUCATION")
    print("=" * 60)

    if 'qualifications' not in config:
        config['qualifications'] = {}

    existing = config['qualifications'].get('education', [])
    if existing:
        print(f"\nExisting education: {len(existing)}")
        for edu in existing:
            print(f"  - {edu.get('degree')} from {edu.get('school')}")
        if not prompt_yes_no("Add more education?", True):
            return config

    education = existing.copy()

    while True:
        print("\n(Leave degree empty to finish)")
        degree = prompt_input("Degree and major (e.g., 'Bachelor of Science, Computer Science')")
        if not degree:
            break

        school = prompt_input("School name")
        year = prompt_input("Graduation year (optional)")

        edu = {'degree': degree, 'school': school}
        if year:
            edu['year'] = year

        education.append(edu)

    config['qualifications']['education'] = education
    return config


def interactive_import():
    """Run interactive import wizard."""
    print("\n" + "=" * 60)
    print("JOB APPLICATION SKILL - RESUME IMPORT WIZARD")
    print("=" * 60)
    print("\nThis wizard will help you set up your qualifications for")
    print("generating tailored resumes and cover letters.")

    config = load_config()

    # Collect all sections
    config = collect_candidate_info(config)
    config = collect_summary(config)
    config = collect_skills(config)
    config = collect_experience(config)
    config = collect_certifications(config)
    config = collect_education(config)

    # Save
    print("\n" + "=" * 60)
    print("REVIEW")
    print("=" * 60)

    quals = config.get('qualifications', {})
    print(f"\nCandidate: {config.get('candidate', {}).get('name', 'Not set')}")
    print(f"Summary: {quals.get('summary', 'Not set')[:50]}...")
    print(f"Skills: {len(quals.get('skills', []))} categories")
    print(f"Experience: {len(quals.get('experience', []))} positions")
    print(f"Certifications: {len(quals.get('certifications', []))}")
    print(f"Education: {len(quals.get('education', []))}")

    if prompt_yes_no("\nSave configuration?", True):
        save_config(config)
        print("\nYour qualifications have been saved!")
        print("You can now use /job-apply to generate tailored documents.")
    else:
        print("\nConfiguration not saved.")


def import_from_file(file_path):
    """Import resume from a file."""
    path = Path(file_path)

    if not path.exists():
        print(f"Error: File not found: {file_path}")
        return

    print(f"\nImporting from: {path}")

    if path.suffix.lower() == '.docx':
        text = extract_text_from_docx(path)
    elif path.suffix.lower() in ('.txt', '.md'):
        text = read_text_file(path)
    else:
        print(f"Unsupported file format: {path.suffix}")
        print("Supported formats: .docx, .txt, .md")
        return

    if not text:
        print("Could not extract text from file.")
        return

    print("\n" + "=" * 60)
    print("EXTRACTED TEXT (first 500 characters)")
    print("=" * 60)
    print(text[:500] + "..." if len(text) > 500 else text)

    print("\n" + "=" * 60)
    print("NEXT STEPS")
    print("=" * 60)
    print("""
The resume text has been extracted. To complete the import:

1. Run this script in interactive mode to enter your qualifications:
   python3 import_resume.py

2. Or manually edit config.yaml with your information.

The extracted text above can help you copy/paste your details.
""")


def main():
    if len(sys.argv) > 1:
        # File import mode
        import_from_file(sys.argv[1])
    else:
        # Interactive mode
        interactive_import()


if __name__ == "__main__":
    main()
