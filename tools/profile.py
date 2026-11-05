#!/usr/bin/env python3
"""Activate a subset of rule packs and skills.

    python tools/profile.py list              # profiles, and what each costs
    python tools/profile.py status            # what is active now
    python tools/profile.py apply quant       # switch
    python tools/profile.py apply quant --dry-run
    python tools/profile.py reset             # back to `full`

Packs outside the active profile stay in rules/ — they are simply not compiled into
.github/instructions/. Skills outside it move to .claude/skills.disabled/, because a
skill's description sits in context permanently whether or not it is ever used.

Profiles are defined in rules/PROFILES.md, whose `active:` frontmatter is committed so
that CI and every developer resolve the same set.

No third-party dependencies.
"""

from __future__ import annotations

import argparse
import fnmatch
import re
import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from sync_rules import (  # noqa: E402 - path set above
    ALWAYS_PACKS,
    ALWAYS_SKILLS,
    expand,
    load_profiles,
)

ROOT = Path(__file__).resolve().parent.parent
PROFILES_MD = ROOT / "rules" / "PROFILES.md"
SKILLS = ROOT / ".claude" / "skills"
SKILLS_OFF = ROOT / ".claude" / "skills.disabled"






def all_packs() -> set[str]:
    return {p.stem for p in (ROOT / "rules").glob("*.md") if not p.stem.isupper()}


def all_skills() -> set[str]:
    names = {d.name for d in SKILLS.iterdir() if d.is_dir()} if SKILLS.is_dir() else set()
    if SKILLS_OFF.is_dir():
        names |= {d.name for d in SKILLS_OFF.iterdir() if d.is_dir()}
    return names


def enabled_skills() -> set[str]:
    return {d.name for d in SKILLS.iterdir() if d.is_dir()} if SKILLS.is_dir() else set()


def unmatched(patterns: list[str], universe: set[str]) -> list[str]:
    """Patterns that resolve to nothing — almost always a typo."""
    dead = []
    for pat in patterns:
        if any(ch in pat for ch in "*?["):
            if not any(fnmatch.fnmatch(u, pat) for u in universe):
                dead.append(pat)
        elif pat not in universe:
            dead.append(pat)
    return dead


def resolve(name: str, warn: bool = True) -> tuple[set[str], set[str]]:
    _, profiles = load_profiles()
    if name not in profiles:
        raise KeyError(name)
    spec = profiles[name]
    if warn:
        for kind, universe in (("pack", all_packs()), ("skill", all_skills())):
            for pat in unmatched(spec[kind + "s"], universe):
                print(f"  ! profile '{name}': {kind} '{pat}' matches nothing",
                      file=sys.stderr)
    packs = expand(spec["packs"], all_packs(), ALWAYS_PACKS)
    skills = expand(spec["skills"], all_skills(), ALWAYS_SKILLS)
    return packs, skills


def move_skills(target: set[str], dry: bool) -> list[str]:
    """Reconcile .claude/skills/ with the target set."""
    log: list[str] = []
    have = enabled_skills()
    for name in sorted(have - target):
        log.append(f"  disable  {name}")
        if not dry:
            SKILLS_OFF.mkdir(parents=True, exist_ok=True)
            dest = SKILLS_OFF / name
            if dest.exists():
                shutil.rmtree(dest)
            shutil.move(str(SKILLS / name), str(dest))
    for name in sorted(target - have):
        src = SKILLS_OFF / name
        if not src.is_dir():
            log.append(f"  ! missing {name} (not in skills.disabled/)")
            continue
        log.append(f"  enable   {name}")
        if not dry:
            shutil.move(str(src), str(SKILLS / name))
    return log


def set_active(name: str) -> None:
    text = PROFILES_MD.read_text(encoding="utf-8")
    if re.search(r"^active:.*$", text, re.M):
        text = re.sub(r"^active:.*$", f"active: {name}", text, count=1, flags=re.M)
    else:
        text = f"---\nactive: {name}\n---\n\n" + text
    PROFILES_MD.write_text(text, encoding="utf-8", newline="\n")


def cmd_list() -> int:
    active, profiles = load_profiles()
    packs_all, skills_all = all_packs(), all_skills()
    print(f"{'profile':<16}{'packs':>8}{'skills':>8}   (active: {active})")
    print("-" * 44)
    for name in profiles:
        p = expand(profiles[name]["packs"], packs_all, ALWAYS_PACKS)
        s = expand(profiles[name]["skills"], skills_all, ALWAYS_SKILLS)
        mark = "*" if name == active else " "
        print(f"{mark}{name:<15}{len(p):>8}{len(s):>8}")
    print(f"\n{len(packs_all)} packs and {len(skills_all)} skills installed.")
    return 0


def cmd_status() -> int:
    active, profiles = load_profiles()
    print(f"active profile: {active}")
    if active not in profiles:
        print(f"  ! '{active}' is not defined in rules/PROFILES.md", file=sys.stderr)
        return 1
    packs, skills = resolve(active)
    off = all_skills() - skills
    print(f"  packs   {len(packs)}/{len(all_packs())}")
    print(f"  skills  {len(skills)}/{len(all_skills())}"
          + (f"  (disabled: {', '.join(sorted(off))})" if off else ""))
    drift = enabled_skills() ^ skills
    if drift:
        print(f"\n  ! on disk differs from the profile: {', '.join(sorted(drift))}",
              file=sys.stderr)
        print("    run: python tools/profile.py apply " + active, file=sys.stderr)
        return 1
    return 0


def cmd_apply(name: str, dry: bool) -> int:
    try:
        packs, skills = resolve(name)
    except KeyError:
        print(f"error: no profile '{name}'. Run `profile.py list`.", file=sys.stderr)
        return 1

    before = len(enabled_skills())
    log = move_skills(skills, dry)
    print("\n".join(log) or "  (skills already match)")

    if dry:
        print(f"\ndry run: would activate {len(packs)} packs and {len(skills)} skills")
        return 0

    set_active(name)
    print(f"\nactive profile: {name}")
    result = subprocess.run([sys.executable, "tools/sync_rules.py"],
                            cwd=ROOT, capture_output=True, text=True)
    print(result.stdout.strip() or result.stderr.strip())
    print(f"\nskills {before} -> {len(skills)}; run `python tools/token_report.py` "
          f"to see the tier-1 saving.")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd")
    sub.add_parser("list")
    sub.add_parser("status")
    ap_apply = sub.add_parser("apply")
    ap_apply.add_argument("name")
    ap_apply.add_argument("--dry-run", action="store_true")
    sub.add_parser("reset")
    args = ap.parse_args()

    if args.cmd == "list":
        return cmd_list()
    if args.cmd == "status" or args.cmd is None:
        return cmd_status()
    if args.cmd == "apply":
        return cmd_apply(args.name, args.dry_run)
    if args.cmd == "reset":
        return cmd_apply("full", False)
    return 1


if __name__ == "__main__":
    sys.exit(main())
