#!/usr/bin/env python3
"""SessionStart hook: report context-tooling readiness in a handful of tokens.

Everything printed here is paid for on every turn of the session, so it stays to a
few lines. It answers exactly one question the agent cannot otherwise cheaply
determine: which retrieval rungs are actually available right now.
"""

from __future__ import annotations

import os
import shutil
import sys
import time
from pathlib import Path

GRAPH = Path(os.environ.get("GRAPH_PATH", "graphify-out/graph.json"))
STALE_DAYS = 7


def main() -> None:
    bits: list[str] = []

    if GRAPH.exists():
        age_days = (time.time() - GRAPH.stat().st_mtime) / 86400
        if age_days > STALE_DAYS:
            bits.append(
                f"graph: STALE ({age_days:.0f}d) — run `graphify update .`"
            )
        else:
            bits.append(f"graph: ok ({age_days:.1f}d)")
    else:
        bits.append("graph: MISSING — `pip install graphifyy && graphify update .`")

    bits.append("ast-grep: ok" if shutil.which("sg") else "ast-grep: not installed")

    plans = Path(".agent/plans")
    if plans.is_dir():
        open_plans = [
            p.name
            for p in sorted(plans.glob("*.md"))
            if "- [ ]" in p.read_text(encoding="utf-8", errors="ignore")
        ]
        if open_plans:
            bits.append(f"open plans: {', '.join(open_plans[:3])}")

    print("context tooling — " + " | ".join(bits), file=sys.stderr)
    sys.exit(0)


if __name__ == "__main__":
    main()
