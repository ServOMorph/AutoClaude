#!/usr/bin/env python3
"""Bump version across multiple files."""

import json
import re
import sys
from pathlib import Path

TOOLING_DIR = Path(__file__).parent
PROJECT_ROOT = TOOLING_DIR.parent
CONFIG_FILE = TOOLING_DIR / "bump_version_files.json"


def load_config():
    """Load bump version configuration."""
    with open(CONFIG_FILE) as f:
        return json.load(f)


def parse_version(version_str):
    """Parse X.Y.Z version string."""
    parts = version_str.split('.')
    if len(parts) != 3:
        raise ValueError(f"Invalid version: {version_str}. Expected X.Y.Z")
    return tuple(int(p) for p in parts)


def get_current_version():
    """Get current version from constants.py."""
    constants_file = PROJECT_ROOT / "src" / "config" / "constants.py"
    with open(constants_file) as f:
        for line in f:
            if line.startswith("VERSION = "):
                match = re.search(r'"([0-9.]+)"', line)
                if match:
                    return match.group(1)
    raise ValueError("Could not find VERSION in constants.py")


def analyze_files():
    """Analyze all files for potential version references."""
    print("\n🔍 Analysing project for version references...\n")

    version_pattern = re.compile(r'\d+\.\d+\.\d+')
    found_files = {}

    for file_path in PROJECT_ROOT.rglob("*"):
        if file_path.is_file() and file_path.suffix in {".py", ".toml", ".md", ".txt", ".json"}:
            if any(x in str(file_path) for x in {".git", "__pycache__", ".pytest_cache", "dist", "build/build"}):
                continue

            try:
                with open(file_path, encoding="utf-8") as f:
                    for line_num, line in enumerate(f, 1):
                        if version_pattern.search(line):
                            rel_path = file_path.relative_to(PROJECT_ROOT)
                            if str(rel_path) not in found_files:
                                found_files[str(rel_path)] = []
                            found_files[str(rel_path)].append(line_num)
            except (UnicodeDecodeError, IsADirectoryError):
                pass

    config = load_config()
    required_files = {f["path"] for f in config["files"]}

    print("📄 Files with version references:")
    for file_path in sorted(found_files.keys()):
        is_required = file_path in required_files
        status = "✅ LISTED" if is_required else "⚠️  NEW?"
        print(f"  {status} {file_path} (lines: {found_files[file_path][:3]}...)")

    print(f"\n✓ Found {len(found_files)} files with version references")
    print(f"✓ {len(required_files)} files in config")

    new_files = set(found_files.keys()) - required_files
    if new_files:
        print(f"\n⚠️  New potential files to add to config:")
        for file_path in sorted(new_files):
            print(f"  • {file_path}")


def bump_files(old_version, new_version):
    """Update version in all configured files."""
    print(f"\n📝 Bumping version {old_version} → {new_version}\n")

    config = load_config()
    updated = 0

    for file_config in config["files"]:
        file_path = PROJECT_ROOT / file_config["path"]

        # Handle version number in path (e.g., AutoClaude_vX.Y.Z.spec)
        if "X.Y.Z" in file_config["path"]:
            new_path = PROJECT_ROOT / file_config["path"].replace("X.Y.Z", new_version)
            if file_path.exists():
                file_path.unlink()
            file_path = new_path

        if not file_path.exists():
            if file_config.get("required"):
                print(f"  ❌ {file_config['path']} (MISSING - required)")
            continue

        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        new_content = content.replace(old_version, new_version)

        if new_content != content:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(new_content)
            print(f"  ✅ {file_config['path']}")
            updated += 1
        else:
            print(f"  ⚠️  {file_config['path']} (no changes)")

    print(f"\n✓ Updated {updated} files")
    return updated


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage: python bump_version.py <new_version> [--analyze]")
        print("       python bump_version.py 2.5.0")
        print("       python bump_version.py --analyze")
        sys.exit(1)

    if sys.argv[1] == "--analyze":
        analyze_files()
        return

    new_version = sys.argv[1]

    try:
        old_version = get_current_version()
        parse_version(new_version)
    except ValueError as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

    print(f"\n{'='*60}")
    print(f"Version Bump: {old_version} → {new_version}")
    print(f"{'='*60}")

    if "--analyze" in sys.argv:
        analyze_files()

    bump_files(old_version, new_version)
    print("\n✓ Version bump complete!")


if __name__ == "__main__":
    main()
