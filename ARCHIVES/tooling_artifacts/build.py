#!/usr/bin/env python3
"""
Build script pour générer l'exe AutoClaude avec PyInstaller.
Usage: python build.py
"""

import subprocess
import sys
from pathlib import Path

def main():
    """TODO: description de main."""
    script_dir = Path(__file__).parent
    spec_file = script_dir / "AutoClaude.spec"

    if not spec_file.exists():
        print(f"[ERREUR] Spec file introuvable : {spec_file}")
        sys.exit(1)

    print("[BUILD] Construction de l'exe AutoClaude...")
    result = subprocess.run(
        [sys.executable, "-m", "PyInstaller", "-y", str(spec_file)],
        cwd=script_dir
    )

    if result.returncode == 0:
        exe_path = script_dir / "dist" / "AutoClaude.exe"
        print(f"[OK] Exe généré : {exe_path}")
        print(f"[INFO] Taille : {exe_path.stat().st_size / (1024*1024):.1f} MB")
    else:
        print("[ERREUR] Erreur lors de la génération de l'exe")
        sys.exit(1)

if __name__ == "__main__":
    main()
