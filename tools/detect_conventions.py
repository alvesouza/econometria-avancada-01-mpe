#!/usr/bin/env python3
"""Infer a codebase's conventions and write them to .agent/conventions.md.

    python tools/detect_conventions.py            # write .agent/conventions.md
    python tools/detect_conventions.py --print    # inspect without writing
    python tools/detect_conventions.py --path ../other-repo

Rules in this repo state what is *correct*. This states what is *local* — indentation,
naming, doc-comment style, comment density, test layout, error-handling idiom — so an
agent can match the surrounding code instead of importing habits from elsewhere.

Every finding carries a confidence share. Low confidence means the codebase is
inconsistent, and the file being edited wins over the aggregate.

No third-party dependencies.
"""

from __future__ import annotations

import argparse
import math
import re
import sys
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path

SKIP_DIRS = {
    ".git", "node_modules", "dist", "build", "target", "out", "bin", "obj",
    ".venv", "venv", "__pycache__", ".mypy_cache", ".pytest_cache", ".ruff_cache",
    "vendor", "third_party", "Pods", ".dart_tool", ".next", ".nuxt", "coverage",
    "graphify-out", ".idea", ".vs",
}

# Generated code lies about conventions.
SKIP_FILE_PAT = re.compile(
    r"(\.g\.dart|\.freezed\.dart|_pb2\.py|\.pb\.go|\.designer\.cs|\.min\.js|"
    r"\.generated\.[a-z]+|\.d\.ts)$"
)

LANGS = {
    ".py": "Python", ".cs": "C#", ".rs": "Rust", ".ts": "TypeScript",
    ".tsx": "TypeScript", ".js": "JavaScript", ".jsx": "JavaScript",
    ".go": "Go", ".java": "Java", ".kt": "Kotlin", ".dart": "Dart",
    ".c": "C", ".h": "C/C++ header", ".cpp": "C++", ".hpp": "C++",
    ".cc": "C++", ".rb": "Ruby", ".php": "PHP", ".swift": "Swift",
    ".scala": "Scala", ".r": "R", ".R": "R", ".sql": "SQL",
}

LINE_COMMENT = {
    "Python": "#", "Ruby": "#", "R": "#",
    "C#": "//", "Rust": "//", "TypeScript": "//", "JavaScript": "//",
    "Go": "//", "Java": "//", "Kotlin": "//", "Dart": "//", "C": "//",
    "C++": "//", "C/C++ header": "//", "Swift": "//", "Scala": "//",
    "PHP": "//", "SQL": "--",
}

# Doc-comment openers, most specific first so `///` is not eaten by `//`.
DOC_STYLES = [
    ("///", re.compile(r"^\s*///[^/]")),          # rustdoc, XML docs, Dart
    ("/** */", re.compile(r"^\s*/\*\*")),          # JSDoc, Javadoc
    ('"""', re.compile(r'^\s*(?:[rubf]*)"""')),    # Python
    ("#'", re.compile(r"^\s*#'")),                  # roxygen (R)
]

CONFIG_FILES = {
    ".editorconfig": "EditorConfig",
    ".prettierrc": "Prettier", ".prettierrc.json": "Prettier",
    ".prettierrc.yaml": "Prettier", ".prettierrc.yml": "Prettier",
    "prettier.config.js": "Prettier",
    ".clang-format": "clang-format",
    "rustfmt.toml": "rustfmt", ".rustfmt.toml": "rustfmt",
    ".eslintrc": "ESLint", ".eslintrc.json": "ESLint", ".eslintrc.js": "ESLint",
    "eslint.config.js": "ESLint", "eslint.config.mjs": "ESLint",
    "biome.json": "Biome",
    "pyproject.toml": "Python project (check [tool.ruff]/[tool.black])",
    "setup.cfg": "Python config", "tox.ini": "tox",
    ".flake8": "flake8", "ruff.toml": "Ruff",
    ".csharpierrc": "CSharpier", ".editorconfig.cs": "C# EditorConfig",
    "Directory.Build.props": "MSBuild shared props",
    "analysis_options.yaml": "Dart analyzer",
    ".golangci.yml": "golangci-lint", ".golangci.yaml": "golangci-lint",
    ".rubocop.yml": "RuboCop",
    "checkstyle.xml": "Checkstyle", ".scalafmt.conf": "scalafmt",
    ".pre-commit-config.yaml": "pre-commit",
}

TEST_MARKERS = {
    "pytest": re.compile(r"^\s*(?:import pytest|from pytest)", re.M),
    "unittest": re.compile(r"unittest\.TestCase"),
    "xUnit": re.compile(r"\[Fact\]|\[Theory\]"),
    "NUnit": re.compile(r"\[Test\]|\[TestFixture\]"),
    "MSTest": re.compile(r"\[TestMethod\]"),
    "Jest/Vitest": re.compile(r"^\s*(?:describe|it|test)\s*\(", re.M),
    "Go testing": re.compile(r"func Test\w+\(t \*testing\.T\)"),
    "JUnit": re.compile(r"@Test\b"),
    "Rust builtin": re.compile(r"#\[cfg\(test\)\]|#\[test\]"),
    "Dart test": re.compile(r"^\s*(?:test|testWidgets)\s*\(", re.M),
    "Catch2/gtest": re.compile(r"TEST_CASE\s*\(|TEST(_F)?\s*\("),
}

# Deliberately narrow. `None` and `??` appear constantly in Python and TypeScript and
# say nothing about how failures are handled, so matching them reports noise as signal.
ERROR_IDIOMS = {
    "exceptions": re.compile(r"^\s*(?:throw|raise)\s", re.M),
    "Result/Either": re.compile(r"\bResult<|\bEither<|\breturn\s+(?:Ok|Err)\("),
    "error returns": re.compile(r"^\s*if err != nil", re.M),
    "Option/Maybe": re.compile(r"\bOption<|\bMaybe<"),
}

MAX_FILES_PER_LANG = 60
MAX_BYTES = 400_000


@dataclass
class LangStats:
    files: int = 0
    lines: int = 0
    comment_lines: int = 0
    indent: Counter = field(default_factory=Counter)
    line_len: list[int] = field(default_factory=list)
    doc_style: Counter = field(default_factory=Counter)
    func_naming: Counter = field(default_factory=Counter)
    type_naming: Counter = field(default_factory=Counter)
    errors: Counter = field(default_factory=Counter)


def naming_of(name: str) -> str | None:
    """Classify an identifier's casing.

    A single lowercase word (`main`, `render`) is snake_case with one segment — treating
    it as its own category splits the count and reports false disagreement.
    """
    if not name or not name[0].isalpha():
        return None
    if name.isupper():
        return "UPPER_SNAKE"
    if name.islower():
        return "snake_case"          # includes single-word lowercase
    if name[0].isupper():
        return "PascalCase"
    return "camelCase"


FUNC_PAT = {
    "Python": re.compile(r"^\s*def\s+(\w+)", re.M),
    "Rust": re.compile(r"^\s*(?:pub(?:\([^)]*\))?\s+)?(?:async\s+)?fn\s+(\w+)", re.M),
    "Go": re.compile(r"^\s*func\s+(?:\([^)]*\)\s*)?(\w+)", re.M),
    "C#": re.compile(r"^\s*(?:public|private|protected|internal)[\w\s<>\[\],]*?\s(\w+)\s*\(", re.M),
    "TypeScript": re.compile(r"^\s*(?:export\s+)?(?:async\s+)?function\s+(\w+)|^\s*(\w+)\s*\([^)]*\)\s*[:{]", re.M),
    "JavaScript": re.compile(r"^\s*(?:export\s+)?(?:async\s+)?function\s+(\w+)", re.M),
    "Dart": re.compile(r"^\s*(?:[\w<>,\s\[\]]+\s+)?(\w+)\s*\([^)]*\)\s*(?:async\s*)?\{", re.M),
    "Java": re.compile(r"^\s*(?:public|private|protected)[\w\s<>\[\],]*?\s(\w+)\s*\(", re.M),
}

TYPE_PAT = {
    "Python": re.compile(r"^\s*class\s+(\w+)", re.M),
    "Rust": re.compile(r"^\s*(?:pub\s+)?(?:struct|enum|trait)\s+(\w+)", re.M),
    "C#": re.compile(r"^\s*(?:public|internal)?\s*(?:sealed\s+|abstract\s+|static\s+)*(?:class|record|struct|interface|enum)\s+(\w+)", re.M),
    "TypeScript": re.compile(r"^\s*(?:export\s+)?(?:class|interface|type|enum)\s+(\w+)", re.M),
    "Go": re.compile(r"^\s*type\s+(\w+)\s+(?:struct|interface)", re.M),
    "Dart": re.compile(r"^\s*(?:abstract\s+)?class\s+(\w+)", re.M),
    "Java": re.compile(r"^\s*(?:public\s+)?(?:final\s+|abstract\s+)*(?:class|interface|enum|record)\s+(\w+)", re.M),
}


def iter_files(root: Path):
    for p in root.rglob("*"):
        if not p.is_file():
            continue
        if any(part in SKIP_DIRS for part in p.parts):
            continue
        if SKIP_FILE_PAT.search(p.name):
            continue
        yield p


def analyse(root: Path) -> tuple[dict[str, LangStats], Counter, list[str], Counter, Counter]:
    stats: dict[str, LangStats] = {}
    ext_counts: Counter = Counter()
    configs: list[str] = []
    frameworks: Counter = Counter()
    test_layout: Counter = Counter()
    seen_config = set()

    for path in iter_files(root):
        if path.name in CONFIG_FILES and path.name not in seen_config:
            seen_config.add(path.name)
            configs.append(f"{path.name} ({CONFIG_FILES[path.name]})")

        lang = LANGS.get(path.suffix)
        if lang is None:
            continue
        ext_counts[lang] += 1

        st = stats.setdefault(lang, LangStats())
        if st.files >= MAX_FILES_PER_LANG:
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")[:MAX_BYTES]
        except OSError:
            continue
        st.files += 1

        lower = str(path).lower()
        is_test = any(m in lower for m in ("test", "spec", "__tests__"))
        if is_test:
            if "tests/" in lower or "test/" in lower or "__tests__" in lower:
                test_layout["separate test directory"] += 1
            else:
                test_layout["tests beside source"] += 1
            for name, pat in TEST_MARKERS.items():
                if pat.search(text):
                    frameworks[name] += 1

        lc = LINE_COMMENT.get(lang, "//")
        for line in text.splitlines():
            st.lines += 1
            stripped = line.strip()
            if stripped.startswith(lc) or stripped.startswith("*") or stripped.startswith("/*"):
                st.comment_lines += 1
            if line and not line[0].isspace():
                st.line_len.append(len(line.rstrip()))
            m = re.match(r"^([ \t]+)", line)
            if m and stripped:
                ws = m.group(1)
                st.indent["tab" if "\t" in ws else f"{len(ws)}-space-unit"] += 1

        for style, pat in DOC_STYLES:
            hits = len(pat.findall(text))
            if hits:
                st.doc_style[style] += hits
                break

        if (pat := FUNC_PAT.get(lang)) is not None:
            for m in pat.finditer(text):
                name = next((g for g in m.groups() if g), None)
                if name and (n := naming_of(name)):
                    st.func_naming[n] += 1
        if (pat := TYPE_PAT.get(lang)) is not None:
            for m in pat.finditer(text):
                if (n := naming_of(m.group(1))):
                    st.type_naming[n] += 1

        for idiom, pat in ERROR_IDIOMS.items():
            if (hits := len(pat.findall(text))):
                st.errors[idiom] += hits

    return stats, ext_counts, configs, frameworks, test_layout


def top(counter: Counter, min_share: float = 0.0) -> tuple[str, float] | None:
    """Most common entry and its share of the total."""
    if not counter:
        return None
    total = sum(counter.values())
    name, n = counter.most_common(1)[0]
    share = n / total
    return (name, share) if share >= min_share else (name, share)


def confidence(share: float) -> str:
    return "high" if share >= 0.8 else "medium" if share >= 0.6 else "**low**"


def indent_unit(counter: Counter) -> tuple[str, float] | None:
    """Collapse observed leading-whitespace widths into a likely indent unit.

    Counting "widths divisible by N" is wrong: 4-space indentation is divisible by 2, so
    2 always wins. The first indent level is the unit, so take the most common raw width
    and sanity-check it against the gcd of the common widths.
    """
    if not counter:
        return None
    total = sum(counter.values())
    if counter.get("tab", 0) > total / 2:
        return ("tab", counter["tab"] / total)

    widths = Counter()
    for key, n in counter.items():
        if key == "tab":
            continue
        w = int(key.split("-")[0])
        if 0 < w <= 64:
            widths[w] += n
    if not widths:
        return None

    common = [w for w, n in widths.most_common(6) if n >= widths.most_common(1)[0][1] * 0.1]
    step = common[0]
    for w in common[1:]:
        step = math.gcd(step, w)
    if step not in (1, 2, 3, 4, 8):
        step = widths.most_common(1)[0][0]

    # Share = lines whose indent is a multiple of the inferred unit.
    agree = sum(n for w, n in widths.items() if w % step == 0)
    return (f"{step} spaces", agree / total)


def render(root: Path, stats, ext_counts, configs, frameworks, test_layout) -> str:
    out: list[str] = [
        "<!-- Generated by tools/detect_conventions.py. Regenerate after large merges. -->",
        "",
        "# Codebase conventions",
        "",
        f"Detected in `{root.name}`. **Descriptive, not prescriptive** — this records what "
        "the codebase already does so changes match it.",
        "",
        "Precedence: correctness and security rules outrank this file; this file outranks "
        "the stylistic preferences in `rules/`. Where confidence is **low** the codebase is "
        "inconsistent — follow the file you are editing and say so.",
        "",
    ]

    if ext_counts:
        out += ["## Languages", ""]
        total = sum(ext_counts.values())
        for lang, n in ext_counts.most_common(8):
            out.append(f"- {lang} — {n} files ({n / total:.0%})")
        out.append("")

    if configs:
        out += [
            "## Tooling", "",
            "These are authoritative — they are enforced, and they outrank anything inferred below.",
            "",
        ]
        out += [f"- `{c}`" for c in sorted(configs)]
        out.append("")

    out += ["## Per language", ""]
    for lang, st in sorted(stats.items(), key=lambda kv: -ext_counts[kv[0]]):
        if st.files == 0:
            continue
        out.append(f"### {lang}")
        out.append("")
        rows = []

        if (iu := indent_unit(st.indent)):
            rows.append(("Indent", iu[0], iu[1]))
        if st.line_len:
            st.line_len.sort()
            p90 = st.line_len[int(len(st.line_len) * 0.9) - 1]
            cap = next((c for c in (80, 88, 100, 120, 140) if p90 <= c), ">140")
            rows.append(("Line length", f"p90 {p90}, likely cap {cap}", 1.0))
        if (fn := top(st.func_naming)):
            rows.append(("Functions", fn[0], fn[1]))
        if (ty := top(st.type_naming)):
            rows.append(("Types", ty[0], ty[1]))
        if (ds := top(st.doc_style)):
            rows.append(("Doc comments", ds[0], ds[1]))
        if st.lines:
            density = st.comment_lines / st.lines
            label = "sparse" if density < 0.05 else "moderate" if density < 0.15 else "heavy"
            rows.append(("Comment density", f"{density:.0%} — {label}", 1.0))
        if (er := top(st.errors)):
            rows.append(("Error handling", er[0], er[1]))

        if rows:
            out += ["| Aspect | Observed | Confidence |", "|---|---|---|"]
            for aspect, value, share in rows:
                conf = "—" if share == 1.0 else confidence(share)
                out.append(f"| {aspect} | {value} | {conf} |")
        out += ["", f"_Sampled {st.files} files, {st.lines:,} lines._", ""]

    if frameworks or test_layout:
        out += ["## Tests", ""]
        if (fw := top(frameworks)):
            others = [f for f, _ in frameworks.most_common()[1:3]]
            extra = f" (also: {', '.join(others)})" if others else ""
            out.append(f"- Framework: **{fw[0]}**{extra}")
        if (tl := top(test_layout)):
            out.append(f"- Layout: {tl[0]} ({confidence(tl[1])} confidence)")
        out.append("")

    out += [
        "## How to use this",
        "",
        "1. Match these conventions in new code, without commenting on it.",
        "2. Where confidence is **low**, match the file you are editing instead.",
        "3. Never let a convention override a correctness, safety, or security rule.",
        "4. When you deliberately diverge, say so and give the reason.",
        "",
        "See `rules/codebase-work.md` for the full precedence order.",
        "",
    ]
    return "\n".join(out)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--path", type=Path, default=Path.cwd(), help="repo to analyse")
    ap.add_argument("--print", dest="to_stdout", action="store_true", help="print instead of writing")
    args = ap.parse_args()

    root = args.path.resolve()
    if not root.is_dir():
        print(f"error: {root} is not a directory", file=sys.stderr)
        return 1

    stats, ext_counts, configs, frameworks, test_layout = analyse(root)
    if not ext_counts:
        print("No recognised source files found.", file=sys.stderr)
        return 1

    doc = render(root, stats, ext_counts, configs, frameworks, test_layout)

    if args.to_stdout:
        print(doc)
        return 0

    dest = root / ".agent" / "conventions.md"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(doc, encoding="utf-8", newline="\n")
    langs = ", ".join(f"{lang}" for lang, _ in ext_counts.most_common(3))
    print(f"wrote {dest.relative_to(root)} — {sum(ext_counts.values())} files, {langs}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
