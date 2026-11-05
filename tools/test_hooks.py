#!/usr/bin/env python3
"""Tests for the .claude/hooks/ scripts.

Run: python tools/test_hooks.py     (exit 1 on any failure — wire into CI)

The cases live in this file rather than on a command line on purpose: the guard
inspects the whole command string, so a shell harness that merely *mentions*
`node_modules` gets blocked by its own subject.

No third-party dependencies, so this runs anywhere the repo is checked out.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HOOK = ROOT / ".claude" / "hooks" / "guard_context.py"
GENERATED_HOOK = ROOT / ".claude" / "hooks" / "check_generated.py"
SESSION_HOOK = ROOT / ".claude" / "hooks" / "session_start.py"

BLOCK, ALLOW = "BLOCK", "allow"

CASES: list[tuple[str, str, str]] = [
    # --- unscoped search: the thing the escalation ladder exists to prevent ---
    ("grep -r TODO .", BLOCK, "recursive grep from root"),
    ("grep -rn pattern .", BLOCK, "recursive grep, combined flags"),
    ("grep -rnE 'pat' ./", BLOCK, "recursive grep, ./ form"),
    ("find . -name '*.py'", BLOCK, "unbounded find"),
    ("ls -R", BLOCK, "recursive listing"),
    # Scoping to real directories is the remediation the guard prints; it must pass.
    ("grep -rnE 'pat' rules/ .claude/skills/", ALLOW, "recursive grep, scoped to dirs"),
    ("grep -rn TODO src/", ALLOW, "recursive grep, single scoped dir"),
    # --- a depth bound is what makes a walk cheap, so it is exempt ---
    ("find . -maxdepth 3 -iname '*kafka*'", ALLOW, "depth-bounded find"),
    ("find /d/Livros -maxdepth 2 -type d", ALLOW, "depth-bounded find, absolute path"),
    # --- vendored and generated trees are never worth their tokens ---
    ("cat node_" + "modules/pkg/index.js", BLOCK, "read inside vendored tree"),
    ("rg pattern " + "dist/", BLOCK, "search inside build output"),
    ("wc -l .ve" + "nv/lib/x.py", BLOCK, "read inside virtualenv"),
    # --- bulk reads ---
    ("cat src/*.ts", BLOCK, "cat with a glob"),
    ("head -n 5000 big.log", BLOCK, "head of thousands of lines"),
    ("find src -exec cat {} \\;", BLOCK, "find -exec cat"),
    # --- the cheap paths stay open ---
    ("rg -n handler src/api", ALLOW, "scoped ripgrep"),
    ("rg -n --glob '!vendor' foo .", ALLOW, "ripgrep with an exclusion glob"),
    ("graphify query 'what calls X' --budget 1500", ALLOW, "graph query"),
    ("sg -p 'await $C.query($$$)' -l ts", ALLOW, "structural search"),
    ("python -m pytest tests/", ALLOW, "running tests"),
    ("git diff --stat", ALLOW, "ordinary git"),
    ("cat README.md", ALLOW, "single file read"),
    # Prose is not a command. The guard must not fire on words in a document it writes.
    ("echo 'STRIDE will not find these threats'", ALLOW, "prose containing 'find X'"),
    (
        "cat >> notes.md << 'EOF'\nSTRIDE will not find these.\nSee node_"
        "modules/ and dist/ exclusions.\nEOF",
        ALLOW,
        "heredoc body mentioning find and vendored paths",
    ),
    ("git commit -m 'find and fix the leak'", ALLOW, "commit message containing 'find'"),
    # Still caught in real command position, including after an operator.
    ("cd src && find . -name '*.ts'", BLOCK, "unbounded find after &&"),
    ("echo hi; grep -rn TODO .", BLOCK, "recursive grep after ;"),
]

# Payloads that must never crash the hook or block the session.
MALFORMED: list[tuple[str, str]] = [
    ("", "empty stdin"),
    ("not json at all", "unparseable body"),
    ("﻿" + json.dumps({"tool_name": "Bash", "tool_input": {"command": "ls"}}),
     "UTF-8 BOM prefix (PowerShell pipes one)"),
    (json.dumps({"tool_name": "Read", "tool_input": {"file_path": "x"}}),
     "non-Bash tool"),
    (json.dumps({"tool_name": "Bash"}), "missing tool_input"),
    (json.dumps({}), "empty object"),
]


def run(stdin_text: str, hook: Path = HOOK) -> int:
    return _run(stdin_text, hook).returncode


def _run(stdin_text: str, hook: Path) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(hook)],
        input=stdin_text.encode("utf-8"),
        capture_output=True,
    )


def edit(path: str) -> str:
    return json.dumps({"tool_name": "Edit", "tool_input": {"file_path": path}})


# check_generated.py must warn on compiled surfaces and stay silent on sources.
# A false warning on a rule pack would train people to ignore the real one.
GENERATED_CASES: list[tuple[str, bool, str]] = [
    (edit("CLAUDE.md"), True, "tier-0 surface is generated"),
    (edit("AGENTS.md"), True, "tool-neutral surface is generated"),
    (edit(".github/copilot-instructions.md"), True, "copilot surface is generated"),
    (edit(".github/instructions/lang-rust.instructions.md"), True, "instruction file"),
    (edit("rules/lang-rust.md"), False, "rule pack is the source — silent"),
    (edit("rules/references/lang-rust.md"), False, "reference file is a source"),
    (edit("README.md"), False, "hand-written — silent"),
    (edit(".claude/skills/ctx/SKILL.md"), False, "skill is hand-written"),
    (json.dumps({"tool_name": "Read", "tool_input": {"file_path": "CLAUDE.md"}}),
     False, "read of a generated file is fine"),
]


def main() -> int:
    failures: list[str] = []

    for cmd, expected, label in CASES:
        payload = json.dumps({"tool_name": "Bash", "tool_input": {"command": cmd}})
        got = BLOCK if run(payload) == 2 else ALLOW
        ok = got == expected
        print(f"{'PASS' if ok else 'FAIL'}  {got:<5}  {label}")
        if not ok:
            failures.append(f"{label}: expected {expected}, got {got} — {cmd!r}")

    print()
    for payload, label in MALFORMED:
        code = run(payload)
        ok = code == 0
        print(f"{'PASS' if ok else 'FAIL'}  exit={code}  {label}")
        if not ok:
            failures.append(f"{label}: malformed payload must exit 0, got {code}")

    print()
    for payload, want_warn, label in GENERATED_CASES:
        proc = _run(payload, GENERATED_HOOK)
        warned = b"GENERATED" in proc.stdout or b"GENERATED" in proc.stderr
        ok = warned == want_warn and proc.returncode == 0
        print(f"{'PASS' if ok else 'FAIL'}  {'warn ' if warned else 'quiet'}  {label}")
        if not ok:
            failures.append(f"check_generated {label}: warned={warned} "
                            f"want={want_warn} exit={proc.returncode}")

    print()
    for payload, label in (("", "empty stdin"), ("{}", "empty object"),
                           ('{"tool_name":"Edit"}', "missing tool_input")):
        for hook, name in ((GENERATED_HOOK, "check_generated"),
                           (SESSION_HOOK, "session_start")):
            code = run(payload, hook)
            ok = code == 0
            print(f"{'PASS' if ok else 'FAIL'}  exit={code}  {name}: {label}")
            if not ok:
                failures.append(f"{name} {label}: must exit 0, got {code}")

    print()
    if failures:
        print(f"{len(failures)} failure(s):", file=sys.stderr)
        for f in failures:
            print(f"  - {f}", file=sys.stderr)
        return 1
    total = len(CASES) + len(MALFORMED) + len(GENERATED_CASES) + 6
    print(f"All {total} hook cases passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
