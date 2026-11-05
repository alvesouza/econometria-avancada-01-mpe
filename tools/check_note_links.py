"""Check that every link in the study notes resolves to a file in the repo.

Purpose: /notes Step 4 verification. Scans ``Notas/**/*.md`` (or the paths given) for
Obsidian wiki-links ``[[target|alias]]`` / ``[[target#heading]]`` and Markdown links
``[text](path)``, and reports each one whose target file does not exist.

Resolution, in order (Obsidian's behaviour): relative to the note's folder, then from the
repo root, then by basename anywhere in the repo. ``.md`` is implied for wiki-links without
an extension. ``http(s):`` and ``mailto:`` links and pure ``#anchors`` are skipped; headings
inside a target are not checked.

Usage: ``python tools/check_note_links.py [paths...]``. Exit status 1 if any link is broken.
"""
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
WIKI = re.compile(r"\[\[([^\]|#]+)(?:#[^\]|]*)?(?:\|[^\]]*)?\]\]")
MD = re.compile(r"\]\(([^)\s]+)\)")
SKIP_DIRS = {".git", "node_modules", "__pycache__", ".venv"}


def _index():
    """Map basename (with and without .md) -> paths, for Obsidian's shortest-path lookup."""
    idx = {}
    for p in ROOT.rglob("*"):
        if p.is_file() and not SKIP_DIRS.intersection(p.parts):
            idx.setdefault(p.name, []).append(p)
            if p.suffix == ".md":
                idx.setdefault(p.stem, []).append(p)
    return idx


def resolves(target, note, idx):
    """True when ``target`` (as written in ``note``) names an existing file."""
    # Inside Markdown tables the alias pipe is escaped as "\|", leaving a trailing backslash.
    target = target.strip().rstrip("\\").replace("%20", " ")
    cands = [target] if pathlib.PurePath(target).suffix else [target + ".md", target]
    for c in cands:
        if (note.parent / c).exists() or (ROOT / c).exists():
            return True
    return pathlib.PurePath(target).name in idx


def main(args):
    paths = [pathlib.Path(a).resolve() for a in args] or [ROOT / "Notas"]
    notes = [q for p in paths for q in ([p] if p.is_file() else p.rglob("*.md"))]
    idx = _index()
    broken = []
    for note in notes:
        text = note.read_text(encoding="utf-8")
        # Links inside fenced code blocks are code, not links.
        text = re.sub(r"```.*?```", "", text, flags=re.S)
        for kind, rx in (("wiki", WIKI), ("md", MD)):
            for t in rx.findall(text):
                if kind == "md" and (re.match(r"[a-z]+:", t) or t.startswith("#")):
                    continue
                t = t.split("#")[0].rstrip("\\")
                if t and not resolves(t, note, idx):
                    broken.append(f"{note.relative_to(ROOT)}: [{kind}] {t}")
    print("\n".join(broken) or f"OK: all links resolve in {len(notes)} notes")
    return 1 if broken else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
