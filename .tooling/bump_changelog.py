#!/usr/bin/env python3
"""Update CHANGELOG.md with new version entry."""

import re
import sys
from datetime import datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
CHANGELOG_FILE = PROJECT_ROOT / "CHANGELOG.md"


def create_changelog_entry(version, date=None):
    """Create a new changelog entry."""
    if date is None:
        date = datetime.now().strftime("%Y-%m-%d")

    entry = f"""## [{version}] — {date}

### Added
-

### Changed
-

### Fixed
-

### Removed
-

"""
    return entry


def add_to_changelog(version, entry):
    """Add entry to top of CHANGELOG.md."""
    if not CHANGELOG_FILE.exists():
        # Create new changelog
        header = """# CHANGELOG

All notable changes to AutoClaude are documented here.
Format based on [Keep a Changelog](https://keepachangelog.com).

"""
        content = header + entry
    else:
        with open(CHANGELOG_FILE, "r", encoding="utf-8") as f:
            content = f.read()

        # Find insert point (after header/intro)
        match = re.search(r"(# CHANGELOG.*?\n\n.*?\n\n)", content, re.DOTALL)
        if match:
            insert_pos = match.end()
            content = content[:insert_pos] + entry + content[insert_pos:]
        else:
            content = entry + content

    with open(CHANGELOG_FILE, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"✅ Added changelog entry for v{version}")
    print(f"📝 Edit CHANGELOG.md to fill in details (Added/Changed/Fixed/Removed)")


def get_last_version():
    """Extract last version from CHANGELOG.md."""
    if not CHANGELOG_FILE.exists():
        return None

    with open(CHANGELOG_FILE) as f:
        match = re.search(r"## \[([0-9.]+)\]", f.read())
        return match.group(1) if match else None


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage: python bump_changelog.py <version>")
        print("       python bump_changelog.py 2.5.0")
        sys.exit(1)

    version = sys.argv[1]

    # Validate version format
    if not re.match(r"^\d+\.\d+\.\d+$", version):
        print(f"❌ Invalid version format: {version}. Expected X.Y.Z")
        sys.exit(1)

    # Check if version already exists
    if CHANGELOG_FILE.exists():
        with open(CHANGELOG_FILE) as f:
            if f"## [{version}]" in f.read():
                print(f"⚠️  Version {version} already in CHANGELOG.md")
                return

    print(f"\n📝 Creating changelog entry for v{version}\n")

    entry = create_changelog_entry(version)
    add_to_changelog(version, entry)

    last_version = get_last_version()
    if last_version and last_version != version:
        print(f"ℹ️  Previous version: {last_version}")

    print(f"\n✓ Changelog ready. Edit CHANGELOG.md to add details.")


if __name__ == "__main__":
    main()
