---
description: Install and drive the shared Manim kit in any project — Beat for pacing, Stage for layout, real tables and axes panels — so a new explainer video costs a short declarative scene file instead of a thousand lines of hand-rolled animation. Owns the reusable drawing layer only; /explainer owns the plan, the narration and the compile.
argument-hint: <target-project-or-video-dir> [--install] [--check] [--lib <dir>] [--with-narration] [--audit] [--scene <BeatId>]
allowed-tools: Read Grep Glob Bash PowerShell Write Edit AskUserQuestion
---

Install the shared Manim kit into the project or video directory given in `$ARGUMENTS`, and
write scenes against it instead of against raw Manim.

The kit is **one file on disk**, `manim_kit.py`. That is the whole economic argument: the
plumbing of a narrated explainer — timing against measured audio, keeping two labels off the
same pixels, drawing a table that is actually a table — is written once and imported. A new
video then costs a **short declarative scene file**, a few dozen lines per beat, instead of a
re-implementation. Tokens spent re-deriving animation plumbing are tokens not spent on the
economics.

This command owns the **drawing layer**. It does not plan a video, write narration, synthesise
speech or mux anything — that is `/explainer`, which imports this kit for its Step 5.

## Why the kit exists — three failures, all observed in production

Not hypothetical risks. Each was measured in the first cut of the first video in this project,
and each is now structurally prevented rather than merely discouraged.

| Failure | What was measured | What the kit does about it |
|---|---|---|
| **Glacial pacing** | The first cut averaged **15.2 seconds per animation** against an idiom of **0.5 to 3 seconds** — five to thirty times too slow. A 147.9-second beat had been spread across 7 `self.play()` calls, so every gesture crawled. | `Beat.step(anims, t=…, hold=…)` separates the two clocks. `t` is the motion's **own** duration, near one second; the narration's remaining time is absorbed as **holds**, which are still, readable frames. `t > 3.0` raises `ValueError`. Long beats get **more steps, never slower ones.** |
| **Overlapping text** | A screenshot showed *"lend, and deposits rise"* written across *"excess reserves, earning nothing"*. Two free labels placed with `.next_to` had collided; the frame was unreadable and the render had reported success. | `Stage` names six screen regions and allows **one occupant each**. `st.show("note", x)` removes whatever was in `"note"` before it draws `x`, so a collision is not something you can forget to avoid. |
| **Fake tables** | Three labels stacked inside one rounded rectangle, presented as a balance sheet. No cells, no rules, no alignment — the geometry carried no information. | `table()` and `balance_sheet()` draw a real grid: one cell per value, ruled columns, a heavier rule under the header, one row per line item. |

A fourth, quieter failure the kit also removes: **hard-coded seconds**. Durations come from
`beats.json`, which holds the **measured** length of each narration clip. A scene that contains
a literal `run_time=4.5` is already out of sync with the voice.

## What gets installed

```
<project>/
├── .claude/
│   ├── speechify_tts.py        ← only with --with-narration
│   └── explainer_compile.py    ← only with --with-narration
└── <video-dir>/
    ├── manim_kit.py            ← THE KIT: copied, never edited in place
    ├── beats.json              ← the timing contract (written by /explainer Step 4)
    ├── scenes.py               ← yours: one Scene per beat, declarative
    └── media/                  ← Manim's render tree (gitignored)
```

Two layouts, both supported:

- **Next to the scenes** (default, zero configuration). `scenes.py` and `manim_kit.py` in the
  same directory, rendered with that directory as the working directory, so
  `from video_explainer import …` resolves from anywhere, because the package is installed.
- **A shared `lib/`** for a project with several videos. One copy, and each `scenes.py` opens
  with:
  ```python
  import sys; from pathlib import Path
  sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
  ```
  Use this only from the second video onwards. One video does not need a library directory.

The kit depends on **Manim CE and numpy, nothing else**. It adds no packages.

## Verified toolchain — measured on this machine, 2026-09-12

| Component | State |
|---|---|
| Manim Community Edition | **0.21.0**, rendering |
| ffmpeg / ffprobe | 8.1.1, on PATH |
| LaTeX | MiKTeX — `latex`, `pdflatex`, `dvisvgm` present, so `MathTex` renders |
| Missing | ImageMagick and `sox` are **not** installed — never depend on them |

`MathTex` needs LaTeX and costs render time; `Text` does not. The kit's `eq()` is LaTeX; its
`title()`, `note()`, `bullets()` and every table cell are not.

## The API — complete, so a scene author never opens the source

```python
from video_explainer import (Beat, Stage, palette, title, note, eq, bullets,
                       table, balance_sheet, axes_panel, sawtooth, series,
                       scatter, ols, read_csv, load_beats,
                       FAST, NORMAL, SLOW, MAX_RUN_TIME)
```

### Timing

| Call | Contract |
|---|---|
| `Beat(scene, beat_id, beats=None)` | Reads the **measured** narration length for `beat_id`. `beats` overrides the lookup; otherwise `load_beats()` reads `beats.json` from the working directory, falling back to the kit's own directory. |
| `.step(anims, t=NORMAL, hold=1.0)` | One visual event. `anims` is a **list** of Animations, or `None` for a pure pause of length `t`. `t` is the motion's own duration. `hold` is a **relative weight**, not seconds. Returns `self`, so steps chain. |
| `.run()` | Executes every step. Motion time plus hold time equals the narration length **exactly**. |
| `.events` | Number of steps declared — what the pacing audit counts. |
| `FAST, NORMAL, SLOW` | `0.6`, `1.0`, `1.8`. `MAX_RUN_TIME` is `3.0`. |
| `load_beats(path=None)` | `{beat_id: seconds}`. |

Two errors it raises on purpose, both of which mean the beat sheet is wrong rather than the code:

- `t` above `3.0` → *"Long beats get MORE steps, not slower ones."*
- total motion above the narration length → remove steps or shorten them; the kit will not
  silently compress your animation to fit the voice.

How the arithmetic actually lands: a 148-second beat with 16 steps at `t=1.0` spends 16 seconds
in motion and distributes 132 seconds of **hold** across the steps by weight. The holds are not
dead time — they are the frames in which the viewer reads what just appeared while the narration
keeps talking. Give the long weight to the step whose sentence is long.

### Layout

| Call | Contract |
|---|---|
| `Stage(scene)` | Screen regions with one occupant each. |
| `.show(slot, mob, fit=True)` | Returns `[FadeOut(previous), FadeIn(mob)]` — a **list to hand to `.step()`**, not an action. Fits and centres `mob` in the slot. |
| `.add_to(slot, mob)` | Returns `[FadeIn(mob)]` and records `mob` alongside the slot's current contents. Only for things that **cannot** collide — a dot layer over its own axes, a brace on its own curve. |
| `.clear(*slots)` | Returns the fade-outs. No argument clears every occupied slot. |
| `.occupied(slot)` | Bool. |
| `Stage.fit(mob, slot)` | Static; scales into the slot's box and moves to its centre. |

Slots, with their regions: `"title"` (top strip), `"main"` (the full centre), `"left"` and
`"right"` (half each), `"aside"` (upper right, small), `"note"` (bottom strip). Six names, and
every piece of text in the video goes through one of them.

### Components

| Call | Draws |
|---|---|
| `title(text, colour=GREY, size=30)` | A `Text` heading for the `"title"` slot. |
| `note(text, colour=GREY, size=24)` | A `Text` line for the `"note"` slot; tightened line spacing. |
| `eq(tex, size=44, colour=WHITE)` | `MathTex`. The only LaTeX in the kit. |
| `bullets(items, size=23, …)` | A left-aligned `VGroup` of `Text`. |
| `table(columns, rows, col_widths=None, row_height=0.62, font_size=21, header_colour=WHITE, rule_colour=GREY, cell_colours=None)` | A real grid. `rows` is a list of tuples, one entry per column, `""` for an empty cell. `cell_colours` is `{(data_row, col): COLOR}` — **data rows are indexed from 0 and exclude the header**, which takes `header_colour`. |
| `balance_sheet(assets, liabilities, width=9.0, …)` | A T-account built on `table()`. Each side is a list of `(label, colour_or_None)`; the shorter side is padded with empty cells. |
| `axes_panel(x_range, y_range, x_label=None, y_label=None, width=8.6, height=4.3, colour=GREY, coords=False)` | Returns **`(ax, group)`** — the `Axes` for coordinate conversion, and the `VGroup` (axes plus labels) you put in a slot. `coords=True` adds tick numbers. |
| `sawtooth(ax, n, colour=BLUE, peak=1.0)` | The inventory path, `n` trips, in the axes' coordinates. |
| `series(ax, points, colour=BLUE, width=4, clip=None)` | A polyline through `(x, y)` pairs; `clip` caps `y` so one outlier cannot blow the frame. |
| `scatter(ax, points, colour=BLUE, radius=0.045)` | A `VGroup` of dots. |
| `ols(points)` | `(slope, intercept, correlation)` — for a line you intend to **show**, not for an inference claim. |
| `read_csv(path)` | `list[dict]`. Data comes from the project's `data/` cache via `/lab-data`; a scene file never fetches. |
| `cell(panel, label)` | The `Text` of one labelled cell inside a `table()` or `balance_sheet()`, to `Indicate` a single entry. Matches the label **as written**, spaces included. Raises with the labels that *are* present, so a typo is obvious. |
| `palette()` | The colour roles, below. |

### Colour roles, fixed for the whole video

| Key | Colour | Means |
|---|---|---|
| `demand` | `BLUE` | money demand and anything derived from it |
| `focus` | `YELLOW` | the object of attention right now |
| `broken` | `RED` | what breaks; the wrong guess |
| `survives` | `GREEN` | the result that survives |
| `muted` | `GREY` | background; closed channels; dropped observations |

One meaning per colour for a whole video. A colour that means two things means nothing.

### A beat lands on its narration, and the kit guarantees it

`Beat.run()` steers by `renderer.time`, not by the sum of the durations you declared, because
Manim floors every `play()` and `wait()` to a whole frame and ~40 such calls per beat lose
most of a second. The closing hold rounds up to a frame boundary, so a beat is never short.

**Do not "fix" a negative gap by padding `hold` weights.** Those are relative weights, not
seconds; the shortfall is quantisation, and inflating a hold moves the problem instead of
removing it. If `beatcheck --rendered` reports a negative gap, the kit's timing is what to
look at, not the scene.

### Four traps the API cannot prevent

1. **Build chart furniture *after* the panel is on stage.** `show()` scales and moves the group,
   so `ax.c2p` returns different pixels before and after. Create dots, curves and braces in a
   **later** step than the one that showed the axes, or add them to the group before showing it.
2. **`Transform`, not `ReplacementTransform`, on slot contents.** `Transform(old, new)` keeps the
   mobject the slot is tracking, so the record stays valid — and the viewer sees which term
   moved, which is the explanation. `ReplacementTransform` swaps identity: `Stage` then fades a
   mobject that is no longer on screen and orphans the one that is.
3. **Never look a cell up by `m.text`.** Manim normalises whitespace out of that attribute:
   `Text("net worth").text` is `"networth"`, while the space is still drawn. A hand-rolled
   `m.text == label` scan therefore matches every one-word label and fails on every multi-word
   one — and only when that beat renders, minutes into a batch. Use `cell(panel, label)`, which
   reads the `.cell_label` that `table()` stamps on each entry. This cost a full 20-beat render.
4. **`show()` returns animations; it does not animate.** A bare `st.show(...)` whose result is
   never passed to `.step()` changes nothing on screen and fails silently.

## Never position a label by eye. Binding.

A label goes where the thing it annotates actually is, measured at run time:

```python
blab = label_near(brace, note("1.5 points", P["focus"], 21), RIGHT)   # measures
blab = note("1.5 points", P["focus"], 21).move_to(ax.c2p(5.1, 1.25))  # guesses
```

`move_to(ax.c2p(x, y))` puts a label at a coordinate someone estimated from the plot. It
knows nothing about how wide the anchor is or how wide the label is, so it survives exactly
until a font size, a data range or a phrase changes. In beat 1 of aula-07 the brace reached
past the guessed point and covered the leading `1` of `1.5 points`: the caption on screen
read `.5 points`. **That is a wrong number, not an ugly frame** -- and nothing in the render
complained.

`label_near(anchor, mob, direction, buff=0.22)` calls `next_to`, which measures both boxes.

| Use | Not |
|---|---|
| `label_near(brace, note("1.5 points"), RIGHT)` | `note(...).move_to(ax.c2p(5.1, 1.25))` |
| `lab.next_to(ax.c2p(1, 1), RIGHT, buff=0.15)` (anchored to a data point, offset measured) | `lab.move_to(ax.c2p(1.3, 1.05))` (offset guessed) |

Anchoring to a data point with `next_to` is fine -- the offset is still measured. What is
banned is a coordinate chosen so the label "looks about right" next to something else.

## Two collision checks, and what each one sees

| | Sees | Cost |
|---|---|---|
| `Stage` | One slot's box against another's. Blind to anything inside a single slot. | free |
| `check_ink` (inside `Beat.run`) | Every piece of text and every brace on screen, pairwise, after each step. | free, but only during a render |
| `layoutcheck <project>` | The same check, over every scene, with no frames written. | ~30 s per beat |

`Stage` could never have caught the brace: the brace and its label were in the same slot, in
the same `VGroup`. Slot-level checking is necessary and nowhere near sufficient.

`check_ink` deliberately ignores axes, curves and dots -- a label may sit on a chart's
furniture, never on another glyph. If a scene genuinely needs one label over another, set
`STRICT_INK = False` and say why in a comment; nothing in this course does.

**Run `layoutcheck` before you compile.** It is the cheap version of the check that the
render performs anyway, and finding a covered caption after an hour of rendering is how an
hour gets wasted twice.

## Pacing rules, binding

- **12 to 20 `.step()` calls per beat.** A 150-second beat with 7 steps is the bug being fixed.
- **`t` between 0.6 and 2.0** for almost everything; never above 3.0 (the kit enforces the cap).
- **`hold` is a relative weight.** The long weight goes to the step whose narration is long.
- **Reveal progressively: one element per step.** A chart is axes, then curve, then label, then
  annotation — four steps, not one.
- **Animate transformation, not replacement.** `Transform` an equation into its rearrangement.
  Do not `FadeOut` then `FadeIn` two versions of the same object.
- **Mean still frame under about 10 seconds.** If the audit reports more, the beat needs steps,
  not patience. If it needs more than 20, it is two beats.

## Layout rules, binding

- **Every piece of text goes through `Stage`.** Never position free text with `.next_to` onto a
  region that already holds something.
- Anything attached to a chart — an axis label, a curve label, a brace — is fine, because it is
  part of that group and moves with it. But never let two such labels share space.
- **A second idea in the same region replaces the first** via `st.show`. It does not join it.
- `"note"` is one line, not a paragraph. If it needs two sentences, it is two steps.

## The shared layer is imported, never copied

Everything under `video_explainer` lives in **one** repository: `../Video explainer`, in
`src/video_explainer/`. A project that uses it holds **none of that code**.

```bash
python "<video-explainer>/install.py" --into "<project>"
```

That runs `pip install -e`, so the interpreter points straight at the repo. A fix made there
is live in every project immediately, with no copying step to forget.

| In a scene or a script | Not this |
|---|---|
| `from video_explainer import Beat, Stage, table, mpl_figure` | `from manim_kit import ...` beside a vendored file |
| `beatcheck Videos/<slug> --rendered` | `python tools/beatcheck.py ...` from a local copy |
| `speechify-tts --check` | `python .claude/speechify_tts.py --check` |
| `explainer-compile Videos/<slug>` | `python .claude/explainer_compile.py ...` |

**Any fix to pacing, layout, tables, narration or compilation is made in `Video explainer`
and nowhere else.** If you find yourself editing a copy inside a study project, stop: that
copy should not exist. Delete it and reinstall.

This is not housekeeping. Four copies of `manim_kit.py` once existed across two repositories,
and every fix had to be hand-propagated to all four — which is exactly how the collision guard
reached one copy and not the others. The `.md` command files are the one thing still copied,
because a project is expected to edit its own.

**One consequence to respect when changing the library:** it is installed, so it must never
resolve paths relative to its own source. The narration client originally looked for `.env`
beside its own file, which was right when it was vendored and wrong the moment it became a
package — it searched the library's repository instead of the project's. Anything
project-specific — `.env`, `beats.json`, `figures/`, `data/` — resolves from the **current
working directory**, never from `__file__`.

## Instructions

### Step 1: Resolve the target and check the toolchain — report, never install silently

1. Resolve `$ARGUMENTS` to a **video directory** (the default: the directory that holds, or will
   hold, `scenes.py`) or to a project root with `--lib`.
2. Probe, and print a table of what is present and what is missing:
   ```bash
   python -c "import manim; print('manim', manim.__version__)"
   python -c "import numpy; print('numpy', numpy.__version__)"
   ffmpeg -version  | head -1
   ffprobe -version | head -1
   latex --version  | head -1
   ```
3. **Report what is missing and stop there.** Do not `pip install`, do not invoke a package
   manager, do not fetch a LaTeX distribution. Say what is absent, what it blocks, and the one
   command the user would run — the user decides whether their machine changes.
4. Name the consequences precisely: no LaTeX means no `eq()` (everything else still renders); no
   ffmpeg means Manim cannot write a video file at all; no Manim means nothing works.

### Step 2: Install the kit

```bash
cp ~/.claude/commands/templates/manim_kit.py "<video-dir>/manim_kit.py"
```

- **Copy it; never fork it.** The point of the kit is that it is the same file everywhere. A
  local improvement belongs in `~/.claude/commands/templates/manim_kit.py` first, then gets
  copied outward — so the next project inherits it instead of re-deriving it.
- With `--with-narration`, also copy `speechify_tts.py` and `explainer_compile.py` into the
  project's `.claude/` directory, and set up `.env` / `.env.example` exactly as `/explainer`
  requires. Without narration the kit still works: the timing contract is then `beats.json` with
  word-count estimates.
- Verify the import from the directory the renders will run in, and smoke-render one throwaway
  scene:
  ```bash
  python -c "from video_explainer import Beat, Stage, table; print('kit ok')"
  cd "<video-dir>" && python -m manim render -ql --media_dir "media" kittest.py KitTest
  ```
  `kittest.py` is a four-step scene against one beat id — a balance sheet and two notes. It
  exists to prove the kit, LaTeX and ffmpeg all work **before** twenty beats depend on them.
- Add the render artefacts to `.gitignore` (`media*/` — any `--media_dir` name, `audio/`, `build/`,
  `**/*.mp4` recursively, `*.log` under the video dir). The kit, `scenes.py` and `beats.json` are versioned; renders and every
  generated `.mp4` are not.

### Step 3: Take the timing from `beats.json`, never from a guess

The kit reads `{id: seconds}`. Those seconds are **measured with `ffprobe` on real audio** by
`/explainer` Step 4, or estimated at 150 words per minute when there is no voice. A scene file
that contains a bare number of seconds has broken the contract.

```bash
python -c "import json;d=json.load(open('beats.json',encoding='utf-8'));print(len(d['beats']),'beats,',round(d['total_seconds']/60,1),'min')"
```

### Step 4: Write the scene file — declarative, one Scene per beat

This is where the tokens are saved. Each beat is a list of `.step()` calls, each call one
progressive reveal. No layout arithmetic, no `run_time` bookkeeping, no `.next_to` chains.

**The model to copy.** One complete beat, fourteen steps, every rule above obeyed:

```python
"""Scenes for <slug>. One Scene per beat; the kit owns pacing and layout.

Render:  python -m manim render -ql --media_dir "media" scenes.py BeatSeven
"""
from manim import *
from video_explainer import (Beat, Stage, palette, title, note, eq, table,
                       axes_panel, scatter, series, ols, FAST, NORMAL)

P = palette()

# From the project's data/ cache (via /lab-data), never fetched here.
PAIRS = [(3.1, 2.0), (6.4, 5.1), (9.8, 8.2), (14.2, 13.6), (21.0, 19.4), (44.5, 41.0)]


class BeatSeven(Scene):
    """The long-run relation: an identity first, then what the data does with it."""

    def construct(self):
        st, b = Stage(self), Beat(self, "BeatSeven")

        b.step(st.show("title", title("Money growth and inflation")), t=FAST, hold=1)

        # the identity, then the SAME equation rearranged in place
        idt = eq(r"\pi = \mu - \eta g")
        b.step(st.show("main", idt), t=NORMAL, hold=4)
        b.step([Transform(idt, eq(r"\mu = \pi + \eta g").move_to(idt))], t=NORMAL, hold=5)
        b.step(st.show("note", note("an identity cannot fail — it can only be read")),
               t=FAST, hold=4)

        # the panel goes on stage FIRST; everything in its coordinates comes after
        ax, panel = axes_panel([0, 50, 10], [0, 50, 10],
                               x_label="money growth, % per year",
                               y_label="inflation, % per year")
        b.step(st.clear("main", "note") + st.show("left", panel), t=NORMAL, hold=2)

        dots = scatter(ax, PAIRS, colour=P["demand"])
        b.step(st.add_to("left", dots), t=NORMAL, hold=5)

        ray = series(ax, [(0, 0), (50, 50)], colour=P["survives"])
        b.step(st.add_to("left", ray), t=FAST, hold=4)
        b.step(st.show("aside", eq(r"\pi = \mu", size=34, colour=P["survives"])),
               t=FAST, hold=5)

        # the wrong first reading, and what survives it
        b.step(st.show("note", note("so inflation is money growth, full stop?",
                                    colour=P["broken"])), t=FAST, hold=4)
        slope, intercept, r = ols(PAIRS)
        fit = series(ax, [(0, intercept), (50, intercept + 50 * slope)], colour=P["focus"])
        b.step(st.add_to("left", fit), t=NORMAL, hold=4)
        b.step(st.show("note", note(f"the fitted slope is {slope:.2f}, not 1.00")),
               t=FAST, hold=6)

        # one real table, one row per quantity
        b.step(st.show("right", table(
            ["quantity", "reading"],
            [("money growth", f"{PAIRS[-1][0]:.1f}%"),
             ("inflation", f"{PAIRS[-1][1]:.1f}%"),
             ("the wedge", "real growth, times the elasticity")],
            col_widths=[2.9, 3.0],
            cell_colours={(2, 1): P["focus"]})), t=NORMAL, hold=6)

        b.step(st.show("note", note("the wedge is the whole economics", colour=P["focus"])),
               t=FAST, hold=5)
        b.step(None, t=0.0, hold=3)          # a held closing frame: nothing moves
        b.run()
```

Read it for what is **absent**: no `run_time` fractions, no coordinate arithmetic, no
`.to_corner`, no rectangle pretending to be a table, and no way for two labels to overlap. That
absence is the token saving, beat after beat.

A beat that will not fit this shape — more than 20 steps, or three separate ideas — is two
beats. Fix the beat sheet, not the scene.

### Step 5: Render and audit the pacing

```bash
cd "<video-dir>"
python -m manim render -ql --media_dir "media" scenes.py BeatSeven   # draft: 854x480, 15 fps
```

Then audit, before rendering the rest. `--audit` runs this and nothing else:

```python
# save as audit.py next to scenes.py, then: python audit.py
import json, re
from pathlib import Path
NAMED = {"FAST": 0.6, "NORMAL": 1.0, "SLOW": 1.8}
src = Path("scenes.py").read_text(encoding="utf-8")
T = {b["id"]: b["seconds"] for b in
     json.loads(Path("beats.json").read_text(encoding="utf-8"))["beats"]}
for m in re.finditer(r"class (\w+)\(Scene\):(.*?)(?=\nclass |\Z)", src, re.S):
    name, body = m.group(1), m.group(2)
    n = body.count(".step(")
    motion = sum(NAMED.get(v) or float(v)
                 for v in re.findall(r"t=(FAST|NORMAL|SLOW|[0-9]+\.?[0-9]*)", body))
    total = T.get(name, 0.0)
    still = (total - motion) / max(n, 1)
    ok = 12 <= n <= 20 and still <= 10 and motion <= total
    print(f"{name:16} steps {n:3}  motion {motion:6.1f}s  "
          f"hold {total - motion:7.1f}s  mean still {still:5.1f}s  "
          f"{'OK' if ok else 'FIX'}")
```

Gates, all three: **12 to 20 steps**, **mean still frame at or under 10 seconds**, **motion
below the narration length**. A `FIX` row is a beat to re-cut, not a number to explain away.
Only once every row says `OK` do you render the final pass at `-qh`.

### Step 6: Port it to a project that is not this course

Run the checklist in the next section. The short version: **the palette's meanings, the
citations and the scope guard are local; the timing contract, the Stage discipline and the table
rules are not.**

### Step 7: Report

| Item | Report |
|---|---|
| Kit | where it was copied to, and its checksum, so a fork is detectable |
| Toolchain | Manim, numpy, ffmpeg, LaTeX — version or **missing**, and what each absence blocks |
| Smoke test | the scene rendered, its path, its duration |
| Audit | the per-beat table from Step 5, with every gate's verdict |
| Layout | the slots each beat uses, so a reviewer can see no region is double-booked |
| Not done | anything that could not be verified on this machine |

## Porting checklist

**Change these for the new project — every one of them is local:**

| What | How to settle it |
|---|---|
| **Colour roles** | Keep five roles and one meaning each, but re-map the meanings to that subject. `demand` is meaningless outside a money video; the role it plays ("the object the argument is about") is not. Write the mapping into the video's `plan.md` and into the scene file's docstring. |
| **Source citations** | Every claim, number and calibration names its chapter, section and **printed page** in *that* project's bibliography, using *that* project's page offsets. Never carry a Kurlat page into another course. |
| **Scope guard** | Read the target project's own `CLAUDE.md` and obey its exclusions. In this project the forbidden list is Kurlat ch. 8 and chs. 12–15, Bellman and dynamic programming, stochastic DSGE and RBC, Calvo pricing, and time-series econometrics. Another project's list is different and equally binding. A beautiful animation of an out-of-scope model is still out of scope. |
| **Data** | The cache path and the provenance registry belong to the target project (`/lab-data`). A scene file never fetches; it reads a CSV that something else vouched for. |
| **Slot geometry** | Only if the target renders at a different aspect ratio. Edit `SLOTS` in the copied kit, re-run the smoke test, and push the change back to the template if it is general. |
| **Language** | On-screen labels follow the narration language. This project narrates in English per the global rule, even though the course runs in Portuguese. |

**Never change these — they are why the kit exists:**

| What | Why it is fixed |
|---|---|
| **The timing contract** | Durations come from measured audio in `beats.json`; motion plus holds equals the narration exactly. Hard-coded seconds desynchronise silently, which is the one defect a render cannot report. |
| **`MAX_RUN_TIME = 3.0`** | The cap is the anti-glacial mechanism. Raising it re-creates the 15.2-second average it was written to kill. |
| **One occupant per slot** | The overlap failure was invisible to the renderer and obvious to the viewer. Remove the discipline and it comes straight back. |
| **Real cells for tabular data** | `table()` and `balance_sheet()` or no table. Labels in a box are a drawing of a table, and a drawing of a table explains nothing. |
| **One element per step** | Progressive reveal is the explanation. A step that adds four things is a slide. |
| **One meaning per colour, for a whole video** | Colour is the only channel carrying semantics at no narration cost. Overload it and it carries none. |
| **No network, no state, no side effects in a scene file** | Scenes are re-rendered dozens of times while pacing is tuned. Anything a scene fetches gets fetched dozens of times and can change between renders. |

## Important

- **Copy the kit, do not re-implement it.** If a scene file starts growing helper functions for
  layout or timing, they belong in the template, where the next video inherits them.
- **Report a missing dependency; never install one.** Manim, ffmpeg and LaTeX are the user's
  machine, not this command's business.
- **Never hard-code a duration in a scene file.** `beats.json` or nothing.
- **The three gates are gates**, not suggestions: 12–20 steps, mean still frame ≤ 10 s, motion
  under the narration length.
- **A beat whose render fails is a blocker.** Do not compile a partial video and report success.
- **Draft at `-ql`, finish once at `-qh`.** Rendering is the expensive half of the pipeline;
  `-qm` is 1280×720/30 and `-qk` is 4K/60 if something in between is needed.
- **MiKTeX installs missing packages on first use**, which hangs an unattended render. Run one
  `eq()` beat interactively before batching twenty.
- **Never reproduce a textbook exercise statement** on screen — cite it by number and page, the
  rule `/exercise-plan`, `/speechify` and `/explainer` all follow.
- **Render artefacts stay out of git**: `media/`, `audio/`, `build/`. The kit, `scenes.py`,
  `beats.json` and the companion are versioned.

## Ecosystem

- `/explainer` → owns the video: the plan, the beat sheet, the narration script, the measured
  `beats.json`, the render order and the frame-accurate compile. It imports this kit for its
  scene step. **This command is the drawing layer only** — running it alone gets you a kit and a
  smoke test, not a video.
- `/companion` → the interactive page for the same model, on request. It inherits this kit's
  axis ranges, calibration and colour roles, so the page is the video's figure in the viewer's
  hands.
- `/lab-data` → every real series a scene plots, with provenance and a checksum. Scenes read the
  cache; they never fetch.
- `/lab` → the simulation behind a calibrated example, verified independently before it becomes
  an animation.
- `/setup-study` → its Step 6.5 copies the video tooling into a new project; this command is the
  drawing half of that setup.

## Sources

- **Manim Community Edition** docs — <https://docs.manim.community/en/stable/>
- The kit itself, `~/.claude/commands/templates/manim_kit.py`, carries the same three-failure
  rationale in its module docstring; the file is the authority on behaviour.
- The measurements quoted here — 15.2 seconds per animation in the first cut, the overlapping
  `"note"` frame, the 147.9-second beat with 7 steps, Manim 0.21.0 and ffmpeg 8.1.1 — were taken
  on this machine on 2026-09-12 while producing `Videos/aula-07-money-and-inflation/`.
