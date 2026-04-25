"""Recherche rapide dans ARCHIVES/meta.json par tag, version ou mot-clé."""

import json
import sys
from pathlib import Path


META_PATH = Path(__file__).parent.parent / "ARCHIVES" / "meta.json"


def load_meta() -> dict:
    return json.loads(META_PATH.read_text(encoding="utf-8"))


def search(query: str) -> list[tuple[str, str, dict]]:
    meta = load_meta()
    results = []
    q = query.lower()
    for cat_name, cat in meta.get("categories", {}).items():
        for fname, fmeta in cat.get("files", {}).items():
            haystack = " ".join([
                fname.lower(),
                fmeta.get("reason", "").lower(),
                fmeta.get("recall_when", "").lower(),
                " ".join(fmeta.get("tags", [])).lower(),
            ])
            if q in haystack:
                results.append((cat_name, fname, fmeta))
    return results


def list_all() -> None:
    meta = load_meta()
    for cat_name, cat in meta.get("categories", {}).items():
        files = cat.get("files", {})
        if not files:
            continue
        print(f"\n## {cat_name} ({len(files)} fichiers)")
        for fname, fmeta in files.items():
            print(f"  • {fname}")
            print(f"    tags    : {', '.join(fmeta.get('tags', []))}")
            print(f"    rappel  : {fmeta.get('recall_when', '—')}")


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python archive_search.py <query>     # Recherche par mot-clé/tag")
        print("  python archive_search.py --list      # Liste tous les fichiers")
        sys.exit(1)

    arg = sys.argv[1]
    if arg == "--list":
        list_all()
        return

    results = search(arg)
    if not results:
        print(f"Aucun résultat pour '{arg}'")
        return

    print(f"\n{len(results)} résultat(s) pour '{arg}':\n")
    for cat, fname, fmeta in results:
        print(f"[FILE] ARCHIVES/{cat}/{fname}")
        print(f"   reason  : {fmeta.get('reason', '—')}")
        print(f"   tags    : {', '.join(fmeta.get('tags', []))}")
        print(f"   rappel  : {fmeta.get('recall_when', '—')}")
        print()


if __name__ == "__main__":
    main()
