#!/usr/bin/env python3
"""PostToolUse(Edit|Write) hook: warn when a generated file was hand-edited.

CLAUDE.md, AGENTS.md, and .github/** are compiled from rules/*.md. Editing them by
hand feels like it worked and is silently reverted by the next sync — the single most
wasteful failure mode this repo has.

Exit 0 always: this is advice, not a block. The message reaches Claude via stderr.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

GENERATED = (
    "CLAUDE.md",
    "AGENTS.md",
    ".github/copilot-instructions.md",
)
GENERATED_DIRS = (".github/instructions",)

# Only writes overwrite. Warning on a Read is a false positive, and a hook that cries
# wolf on reads trains people to ignore it on the edit that actually mattered.
WRITE_TOOLS = {"Edit", "Write", "MultiEdit", "NotebookEdit"}


def is_generated(path_str: str) -> bool:
    try:
        p = Path(path_str).resolve()
        root = Path.cwd().resolve()
        rel = p.relative_to(root).as_posix()
    except (ValueError, OSError):
        return False
    if rel in GENERATED:
        return True
    return any(rel.startswith(d + "/") for d in GENERATED_DIRS)


def main() -> None:
    # Tolerate a UTF-8 BOM: Windows PowerShell prepends one when piping to a native
    # process, and json.load would otherwise raise on an otherwise-valid payload.
    raw = sys.stdin.read()
    try:
        payload = json.loads(raw.lstrip("﻿\r\n\t ")) if raw.strip() else {}
    except Exception:
        sys.exit(0)

    if payload.get("tool_name") not in WRITE_TOOLS:
        sys.exit(0)

    tool_input = payload.get("tool_input") or {}
    path = tool_input.get("file_path") or tool_input.get("path") or ""
    if path and is_generated(path):
        print(
            f"NOTE: {path} is GENERATED from rules/*.md.\n"
            "This edit will be overwritten by `python tools/sync_rules.py`.\n"
            "Edit the source rule pack instead (see rules/INDEX.md, or run /rulesmith), "
            "then re-run the sync.",
            file=sys.stderr,
        )

    sys.exit(0)


if __name__ == "__main__":
    main()
