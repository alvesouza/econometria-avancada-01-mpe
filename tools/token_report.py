#!/usr/bin/env python3
"""Measure the token cost of every agent-facing surface.

The number that matters is not tokens-per-request. It is **standing cost x turns**:
a 3,000-token instruction file in a 50-turn session is 150,000 token-turns before a
single line of code is read.

Uses Anthropic's count_tokens endpoint when ANTHROPIC_API_KEY (or an `ant auth login`
profile) is available, and falls back to a conservative character-based estimate
otherwise. Never uses tiktoken — that is OpenAI's tokenizer and undercounts Claude by
15-20% on prose and considerably more on code.

Usage:
    python tools/token_report.py            # tier-0 standing cost
    python tools/token_report.py --all      # every pack and skill too
    python tools/token_report.py --budget   # exit 1 if tier 0 exceeds its budget
    python tools/token_report.py --turns 50 # project standing cost over N turns
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from sync_rules import parse_frontmatter  # noqa: E402 - path set above

ROOT = Path(__file__).resolve().parent.parent
MODEL = "claude-opus-5"

# Tier 0 is re-sent on every request, forever. This budget is deliberately tight.
TIER0_BUDGET = 900
# Skill frontmatter descriptions also sit in context permanently.
SKILL_DESC_BUDGET = 2000

FM_RE = re.compile(r"\A---\r?\n(.*?)\r?\n---\r?\n(.*)\Z", re.DOTALL)


# ----------------------------------------------------------------------- counting


def _fallback(text: str) -> int:
    # Deliberately conservative: code tokenizes denser than prose.
    return max(1, round(len(text) / 3.4))


class Counter:
    def __init__(self) -> None:
        self.client = None
        self.exact = False
        try:
            import anthropic  # type: ignore

            self.client = anthropic.Anthropic()
            self.client.messages.count_tokens(
                model=MODEL, messages=[{"role": "user", "content": "ping"}]
            )
            self.exact = True
        except Exception:
            self.client = None

    def count(self, text: str) -> int:
        if not text.strip():
            return 0
        if self.client is not None:
            try:
                return self.client.messages.count_tokens(
                    model=MODEL, messages=[{"role": "user", "content": text}]
                ).input_tokens
            except Exception:
                pass
        return _fallback(text)


# ------------------------------------------------------------------------ surfaces


def frontmatter_description(path: Path) -> str:
    """Skill description as the model actually receives it.

    Shares sync_rules' parser rather than reimplementing it — a second copy drifted
    once already, truncating wrapped descriptions and under-reporting tier-1 cost by
    ~5x on the affected skills.
    """
    meta, _ = parse_frontmatter(path.read_text(encoding="utf-8"))
    return str(meta.get("description", ""))


def tier0_surfaces() -> list[tuple[str, Path]]:
    return [
        (name, ROOT / name)
        for name in ("CLAUDE.md", "AGENTS.md", ".github/copilot-instructions.md")
        if (ROOT / name).exists()
    ]


def bar(n: int, budget: int, width: int = 28) -> str:
    filled = min(width, round(width * n / budget)) if budget else 0
    mark = "#" if n <= budget else "!"
    return f"[{mark * filled}{'.' * (width - filled)}]"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--all", action="store_true", help="include packs and skill bodies")
    ap.add_argument("--budget", action="store_true", help="exit 1 if over budget")
    ap.add_argument("--turns", type=int, default=40, help="turns for the projection")
    args = ap.parse_args()

    c = Counter()
    print(f"token report — {'exact (count_tokens)' if c.exact else 'ESTIMATED'}\n")

    # --- tier 0 ------------------------------------------------------------
    print("TIER 0 — re-sent on every request")
    worst = 0
    for name, path in tier0_surfaces():
        n = c.count(path.read_text(encoding="utf-8"))
        worst = max(worst, n)
        flag = "" if n <= TIER0_BUDGET else f"  OVER by {n - TIER0_BUDGET}"
        print(f"  {bar(n, TIER0_BUDGET)} {n:>6}  {name}{flag}")
    print(f"  budget {TIER0_BUDGET} per surface")
    print(f"  standing cost over {args.turns} turns: ~{worst * args.turns:,} token-turns\n")

    # --- tier 1 ------------------------------------------------------------
    skills = sorted((ROOT / ".claude" / "skills").glob("*/SKILL.md"))
    desc_total = 0
    print("TIER 1 — skill descriptions, always in context")
    for s in skills:
        n = c.count(frontmatter_description(s))
        desc_total += n
        print(f"  {n:>6}  /{s.parent.name}")
    over_desc = desc_total > SKILL_DESC_BUDGET
    print(
        f"  {desc_total:>6}  TOTAL (budget {SKILL_DESC_BUDGET})"
        f"{'  OVER' if over_desc else ''}\n"
    )

    # --- tier 2: packs and skill bodies, loaded when judged relevant --------
    if args.all:
        print("TIER 2 — a pack loads when its subject is in play")
        rows: list[tuple[int, str]] = []
        for p in sorted((ROOT / "rules").glob("*.md")):
            rows.append((c.count(p.read_text(encoding="utf-8")), f"rules/{p.name}"))
        for s in skills:
            rows.append((c.count(s.read_text(encoding="utf-8")), f"/{s.parent.name} body"))
        for n, label in sorted(rows, reverse=True):
            warn = "   <- split the detail into references/" if n > 2500 else ""
            print(f"  {n:>6}  {label}{warn}")
        pack_total = sum(n for n, _ in rows)
        print(f"  {pack_total:>6}  TOTAL\n")

        # --- tier 3: references, loaded only while implementing -------------
        ref_rows: list[tuple[int, str]] = []
        for p in sorted((ROOT / "rules" / "references").glob("*.md")):
            ref_rows.append(
                (c.count(p.read_text(encoding="utf-8")), f"rules/references/{p.name}")
            )
        if ref_rows:
            print("TIER 3 — reference appendices, loaded only to implement")
            for n, label in sorted(ref_rows, reverse=True):
                print(f"  {n:>6}  {label}")
            ref_total = sum(n for n, _ in ref_rows)
            print(f"  {ref_total:>6}  TOTAL\n")
            print(
                f"  Deferred by the split: {ref_total} tokens that no longer load with "
                f"their pack.\n"
            )

    if args.budget:
        problems = []
        if worst > TIER0_BUDGET:
            problems.append(f"tier 0 at {worst} tokens (budget {TIER0_BUDGET})")
        if over_desc:
            problems.append(
                f"skill descriptions at {desc_total} tokens (budget {SKILL_DESC_BUDGET})"
            )
        if problems:
            print("BUDGET EXCEEDED:", file=sys.stderr)
            for p in problems:
                print(f"  - {p}", file=sys.stderr)
            print(
                "\nMove content to a tier-2 rule pack or a skill body. "
                "See docs/05-authoring.md.",
                file=sys.stderr,
            )
            return 1
        print("Budgets OK.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
