#!/usr/bin/env python3
"""PreToolUse(Bash) hook: block repo-wide searches that burn context.

Rules are suggestions a model can rationalize past. A hook cannot be. This is the
mechanism half of `rules/context.md` — it stops unscoped recursive search and points
at the cheap alternative.

Contract: read the hook payload as JSON on stdin. Exit 0 to allow. Exit 2 to block,
with the reason on stderr (Claude reads stderr and adjusts).
"""

from __future__ import annotations

import json
import os
import re
import sys

GRAPH = os.environ.get("GRAPH_PATH", "graphify-out/graph.json")

# Unscoped recursive search from the repo root. Scoped searches are fine.
#
# A depth bound is what makes a walk cheap, so anything carrying one is exempt:
# `find . -maxdepth 2 -name '*.csproj'` is a targeted lookup, not a repo-wide sweep.
DEPTH_BOUNDED = re.compile(r"-maxdepth\s+[1-9]\b")

# Commands are only recognised in command position — start of line, or after a shell
# operator. Without this, ordinary prose ("STRIDE will not find these") matches, and
# a guard that blocks writing about searching is worse than no guard.
CMD = r"(?:^|[|;&\n])\s*"

WIDE_SEARCH = [
    # Recursive grep *targeting the repo root*. `grep -rn pat src/ tests/` is scoped
    # and allowed — otherwise the guard would reject the very fix its message asks for.
    re.compile(CMD + r"grep\b[^|;]*\s-[a-zA-Z]*r[a-zA-Z]*\b[^|;]*\s\.\.?/?\s*($|[|;])"),
    re.compile(CMD + r"rg\b(?![^|;]*(--glob|-g\s|--iglob))[^|;]*\s(\.|\./|\*)\s*$"),
    re.compile(CMD + r"find\s+\S*\s"),
    re.compile(CMD + r"ls\s+-R\b"),
]

# Heredoc bodies are data, not commands. Authoring a document that mentions `find` or
# a vendored path must not trip a guard about how the agent searches.
HEREDOC_RE = re.compile(r"<<-?\s*'?\"?(\w+)'?\"?\r?\n.*?\r?\n\1\b", re.DOTALL)

# Cheap to say, expensive to run, and never what the agent actually wanted.
BULK_READ = [
    (re.compile(r"\bcat\s+[^|;]*\*"), "cat with a glob"),
    (re.compile(r"\bhead\s+-n\s*\d{4,}"), "head of thousands of lines"),
    (re.compile(r"\bfind\b[^|;]*-exec\s+cat\b"), "find -exec cat"),
]

# Directories that must never be walked.
#
# The lookbehind anchors the name to a path boundary rather than requiring a leading
# slash, so a bare `dist/` at the start of an argument is caught too, while
# `redistribute/` and `mybuild/` are not.
POISON = re.compile(
    r"(node_modules|site-packages|\.venv|(?<![\w.-])(dist|build|target|out|bin|obj)/)"
)


def block(message: str) -> None:
    print(message, file=sys.stderr)
    sys.exit(2)


def read_payload() -> dict:
    """Parse the hook payload, tolerating a UTF-8 BOM.

    Windows PowerShell prepends a BOM when piping to a native process, which makes
    json.load raise. Swallowing that silently would make this guard fail *open* — it
    would appear installed and enforce nothing — so a parse failure is reported on
    stderr even though we still allow the call through.
    """
    raw = sys.stdin.read()
    if not raw.strip():
        return {}
    try:
        return json.loads(raw.lstrip("﻿\r\n\t "))
    except Exception as exc:  # noqa: BLE001 - diagnostic only
        print(f"guard_context: unparseable hook payload ({exc}) — allowing", file=sys.stderr)
        return {}


def main() -> None:
    payload = read_payload()

    if payload.get("tool_name") != "Bash":
        sys.exit(0)

    cmd = (payload.get("tool_input") or {}).get("command", "")
    if not cmd:
        sys.exit(0)

    # Inspect only the command, not the document it may be writing.
    cmd = HEREDOC_RE.sub("<<HEREDOC", cmd)

    graph_hint = (
        f'  graphify query "<question>" --graph {GRAPH} --budget 1500\n'
        if os.path.exists(GRAPH)
        else "  (no graph yet — build one with: graphify update .)\n"
    )

    if POISON.search(cmd):
        block(
            "Blocked: this command walks a vendored or generated directory "
            "(node_modules / dist / build / target / .venv).\n"
            "Those trees are excluded from context by policy — their contents are "
            "noise you pay for on every subsequent turn.\n"
            "Scope the search to source directories instead."
        )

    for pattern in WIDE_SEARCH:
        if pattern.search(cmd) and not DEPTH_BOUNDED.search(cmd):
            block(
                "Blocked: unscoped repo-wide search.\n"
                "Escalation ladder (rules/context.md#1) — stop at the first rung that "
                "answers the question:\n"
                + graph_hint
                + "  sg -p '<pattern>' -l <lang>            # structural, if you want a code shape\n"
                "  rg -n --glob '!{node_modules,dist,build,target,.venv}' '<pat>' <dir>\n"
                "\nRe-run scoped to a directory, or query the graph."
            )

    for pattern, label in BULK_READ:
        if pattern.search(cmd):
            block(
                f"Blocked: bulk read ({label}).\n"
                "Read only what you need: `Read` with offset/limit, or find_symbol via "
                "Serena. If you genuinely need whole-repo content, use "
                "`npx repomix --compress` deliberately."
            )

    sys.exit(0)


if __name__ == "__main__":
    main()
