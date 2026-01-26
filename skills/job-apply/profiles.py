#!/usr/bin/env python3
"""
Profile Management for Job Application Skill

Switch between user profiles to test onboarding or maintain multiple configurations.

Usage:
    python3 profiles.py list              # List all profiles
    python3 profiles.py current           # Show current profile
    python3 profiles.py save <name>       # Save current config as named profile
    python3 profiles.py switch <name>     # Switch to a named profile
    python3 profiles.py new               # Switch to empty profile (new user experience)
    python3 profiles.py delete <name>     # Delete a named profile
"""

import sys
import shutil
from pathlib import Path
import yaml


def get_skill_dir():
    """Get the skill directory."""
    return Path(__file__).parent


def get_config_path():
    """Get the path to the active config file."""
    return get_skill_dir() / "config.yaml"


def get_example_config_path():
    """Get the path to the example config file."""
    return get_skill_dir() / "config.example.yaml"


def get_profiles_dir():
    """Get the profiles directory, creating if needed."""
    profiles_dir = get_skill_dir() / "profiles"
    profiles_dir.mkdir(exist_ok=True)
    return profiles_dir


def get_profile_path(name):
    """Get path to a named profile."""
    return get_profiles_dir() / f"{name}.yaml"


def list_profiles():
    """List all saved profiles."""
    profiles_dir = get_profiles_dir()
    profiles = sorted(p.stem for p in profiles_dir.glob("*.yaml"))

    current = get_current_profile_name()

    print("\nSaved profiles:")
    if not profiles:
        print("  (none)")
    else:
        for name in profiles:
            marker = " <- active" if name == current else ""
            print(f"  - {name}{marker}")

    # Check if there's an unsaved active config
    config_path = get_config_path()
    if config_path.exists() and not current:
        print("\n  Note: Active config is not saved as a profile")

    print()


def get_current_profile_name():
    """Get the name of the current profile, if it matches a saved one."""
    config_path = get_config_path()
    if not config_path.exists():
        return None

    with open(config_path, 'r') as f:
        current_config = f.read()

    for profile_path in get_profiles_dir().glob("*.yaml"):
        with open(profile_path, 'r') as f:
            if f.read() == current_config:
                return profile_path.stem

    return None


def show_current():
    """Show information about the current profile."""
    config_path = get_config_path()

    if not config_path.exists():
        print("\nNo active configuration (new user state)")
        print("Run /job-apply to trigger onboarding\n")
        return

    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)

    profile_name = get_current_profile_name()

    print("\nCurrent profile:", profile_name or "(unsaved)")
    print("-" * 40)

    candidate = config.get('candidate', {})
    print(f"  Name: {candidate.get('name', 'Not set')}")
    print(f"  Email: {candidate.get('email', 'Not set')}")

    quals = config.get('qualifications', {})
    if quals:
        print(f"  Experience: {len(quals.get('experience', []))} positions")
        print(f"  Skills: {len(quals.get('skills', []))} categories")
        print(f"  Certifications: {len(quals.get('certifications', []))}")
    else:
        print("  Qualifications: Not configured")

    projects = config.get('portfolio_projects', [])
    print(f"  Portfolio projects: {len(projects)}")

    print()


def save_profile(name):
    """Save current config as a named profile."""
    config_path = get_config_path()

    if not config_path.exists():
        print(f"\nError: No active configuration to save")
        print("Set up your config first, then save it as a profile\n")
        return False

    profile_path = get_profile_path(name)

    if profile_path.exists():
        response = input(f"Profile '{name}' already exists. Overwrite? [y/N]: ").strip().lower()
        if response not in ('y', 'yes'):
            print("Cancelled\n")
            return False

    shutil.copy(config_path, profile_path)
    print(f"\nProfile '{name}' saved")
    print(f"  Location: {profile_path}\n")
    return True


def switch_profile(name):
    """Switch to a named profile."""
    profile_path = get_profile_path(name)

    if not profile_path.exists():
        print(f"\nError: Profile '{name}' not found")
        print("Available profiles:")
        list_profiles()
        return False

    config_path = get_config_path()

    # Warn if current config is unsaved
    if config_path.exists():
        current_name = get_current_profile_name()
        if not current_name:
            print("\nWarning: Current configuration is not saved as a profile")
            response = input("Save current config before switching? [Y/n]: ").strip().lower()
            if response not in ('n', 'no'):
                save_name = input("Profile name to save as: ").strip()
                if save_name:
                    save_profile(save_name)

    shutil.copy(profile_path, config_path)
    print(f"\nSwitched to profile '{name}'")
    show_current()
    return True


def switch_to_new():
    """Switch to empty config for new user experience."""
    config_path = get_config_path()

    # Warn if current config is unsaved
    if config_path.exists():
        current_name = get_current_profile_name()
        if not current_name:
            print("\nWarning: Current configuration is not saved as a profile")
            response = input("Save current config before switching? [Y/n]: ").strip().lower()
            if response not in ('n', 'no'):
                save_name = input("Profile name to save as: ").strip()
                if save_name:
                    save_profile(save_name)

    # Remove current config to simulate new user
    if config_path.exists():
        config_path.unlink()

    print("\nSwitched to new user state")
    print("config.yaml has been removed")
    print("\nRun /job-apply to test the onboarding experience")
    print("Or run: python3 import_resume.py\n")
    return True


def delete_profile(name):
    """Delete a named profile."""
    profile_path = get_profile_path(name)

    if not profile_path.exists():
        print(f"\nError: Profile '{name}' not found\n")
        return False

    # Don't allow deleting the active profile
    if name == get_current_profile_name():
        print(f"\nError: Cannot delete active profile '{name}'")
        print("Switch to a different profile first\n")
        return False

    response = input(f"Delete profile '{name}'? [y/N]: ").strip().lower()
    if response not in ('y', 'yes'):
        print("Cancelled\n")
        return False

    profile_path.unlink()
    print(f"\nProfile '{name}' deleted\n")
    return True


def print_usage():
    """Print usage information."""
    print(__doc__)


def main():
    if len(sys.argv) < 2:
        print_usage()
        return

    command = sys.argv[1].lower()

    if command == 'list':
        list_profiles()

    elif command == 'current':
        show_current()

    elif command == 'save':
        if len(sys.argv) < 3:
            print("\nUsage: python3 profiles.py save <name>\n")
            return
        save_profile(sys.argv[2])

    elif command == 'switch':
        if len(sys.argv) < 3:
            print("\nUsage: python3 profiles.py switch <name>\n")
            list_profiles()
            return
        switch_profile(sys.argv[2])

    elif command == 'new':
        switch_to_new()

    elif command == 'delete':
        if len(sys.argv) < 3:
            print("\nUsage: python3 profiles.py delete <name>\n")
            return
        delete_profile(sys.argv[2])

    elif command in ('help', '-h', '--help'):
        print_usage()

    else:
        print(f"\nUnknown command: {command}")
        print_usage()


if __name__ == "__main__":
    main()
