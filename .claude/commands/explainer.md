---
description: Plan, animate and compile a 3blue1brown-style explainer video about a course topic — beat sheet and narration script, Manim CE scenes timed to synthesised speech, compiled into one video file with subtitles. Asks purpose, length, whether to derive the math on screen, and examples before writing anything. Use /companion separately for an interactive page.
argument-hint: <topic-or-lecture-or-exercise> [--lang <code>] [--quality l|m|h] [--no-voice] [--plan-only]
allowed-tools: Read Grep Glob Bash PowerShell Write Edit NotebookEdit AskUserQuestion Artifact
---

Produce a narrated, animated explainer video for the topic given in `$ARGUMENTS`, in the
idiom of 3blue1brown: one visual object per beat, built on screen while a voice explains it,
compiled into a single video file.

The output is **not** a recorded slide deck. A slide deck shows a finished figure and talks
about it; this shows the figure being constructed, and the construction *is* the argument.

## What gets produced

One directory per video, `Videos/<slug>/`:

```
Videos/<slug>/
├── plan.md              ← thesis, beat sheet, scope, what is deliberately left out
├── script.md            ← the narration, beat by beat, human-readable
├── beats.json           ← the timing contract: beat id, text, audio file, measured duration
├── scenes.py            ← one Manim Scene class per beat, run_time read from beats.json
├── audio/               ← one synthesised clip per beat, plus the padded WAVs
├── media/               ← Manim's render tree (gitignored)
├── companion.html       ← only if /companion was asked for; never auto-built
├── <slug>.mp4           ← THE DELIVERABLE: one file, video + narration (gitignored)
├── <slug>.srt           ← subtitles, generated from beats.json
└── provenance.md        ← sources cited, voice used, versions, render settings, checksums
```

## Verified toolchain — measured on this machine, 2026-09-12

Do not re-derive these; do re-check them if a render fails.

| Component | State |
|---|---|
| Manim Community Edition | **0.21.0**, installed and rendering |
| ffmpeg / ffprobe | 8.1.1, on PATH |
| LaTeX | MiKTeX (`latex`, `pdflatex`, `dvisvgm` present) — `MathTex` renders correctly |
| Narration | `speechify-tts` (from `video_explainer`) — **verified live**: auth OK, 125 English voices |
| Compile | `explainer-compile` (from `video_explainer`) — **verified**: 0.0 ms drift on 20 beats |
| Scene kit | `video_explainer` — timing, screen slots, real tables, collision guard. **Imported, never vendored**; installed by `/manim-kit` |
| Speechify API | `https://api.speechify.ai`, `Authorization: Bearer $SPEECHIFY_API_KEY` from `.env` |
| Missing | ImageMagick and `sox` are **not** installed — never depend on them |

Speechify facts that constrain the script, all verified live:

- `POST /v1/audio/speech` returns **JSON with base64 `audio_data`**, not binary, and caps
  `input` at **2000 characters** (2001 → HTTP 400). The client chunks on sentence boundaries.
- `speech_marks` are **word level, in milliseconds** — so a beat can be synced to a word, not
  just to a clip. But they under-report length (1750 ms of marks vs 1800 ms of file), so clip
  duration always comes from `ffprobe`.
- Models are at `/v1/audio/models`: **`simba-3.0`** (default, multilingual, includes `pt-BR`)
  and **`simba-3.2`** (recommended, English only). Use 3.0 when `--lang pt-BR`.
- Default voice `george` (en-US, warm, e-learning + audiobook tagged). `--list-voices` shows
  the other 124 English options; every voice carries a `preview_audio` URL, so audition costs
  nothing. `loudness_normalization` is on, which keeps levels equal across separate beats.

Render command that works, with the repo path containing spaces:

```bash
cd "Videos/<slug>" && python -m manim render -ql --media_dir "media" scenes.py BeatOne
```

## The method — Sanderson's own stated criteria

Not an imitation of the channel's surface. These are the criteria **he** publishes for judging
exposition, quoted verbatim, and what each one demands of a beat sheet.

| Criterion | His words | What it obliges you to do |
|---|---|---|
| **Clarity** | *"Jargon should be explained, the goals of the lesson should be understandable with minimal background, and the submission should generally display empathy for people unfamiliar with the topic."* | Every symbol named out loud when it first appears. For a *review* video the baseline is the lecture's notation, not zero — but state which |
| **Motivation** | *"It should be clear to the reader/viewer within the first 30 seconds why they should care."* | The cold open is a **hard requirement with a deadline**, not decoration. If the plan's first beat does not answer "why care" inside 30 seconds, the plan is wrong |
| **Novelty** | *"It doesn't necessarily have to be an original idea or original topic, but it should offer someone an experience they might otherwise not have by searching around online."* | The value is the *treatment*, not the topic. A video that restates the slides adds nothing — find the angle the slides could not show |
| **Memorable** | *"Something should make the piece easy to remember even several months later. Maybe it's the beauty of the presentation, the enthusiasm of the presenter, or the mind-blowingness of an aha moment."* | This is what the **closing image** is for: one frame the viewer can redraw from memory in December |

He adds, for longer pieces: *"the substance of your work should be clearly visible with a 5-10
minute view."* A 20-minute video whose point only lands at minute 18 has failed this.

**Four structural rules**, also in his own words:

1. **"Concrete before abstract."** Examples before frameworks — and he is explicit that this is
   the reverse of how someone who already understands the topic would organise it.
2. **"Never start with definitions."** A definition is *"an ending point"*, because *"the best
   pedagogical order of ideas is often very different from the correct logical order."*
3. **"Every movement on the screen should be deliberate, with an identifiable purpose."** This
   is the line that separates animation from motion. If you cannot say what a movement is
   *for*, delete it.
4. Ask of every topic: **"what picture or visual you could use to elucidate a topic."** The
   picture is the unit of explanation, not the paragraph.

His MIT colloquium names the three pillars as *"the role of visualization, narrative, and the
interplay between concreteness and abstraction."*

**What this means for this course, concretely:**

- *Concrete before abstract* → open Lista 6 Q2 on the arithmetic (a 2% target, 3% growth, and a
  central bank that misses by 1.5 points) and arrive at $\pi=\mu-\eta g$ as the explanation of
  what went wrong. Do not open on the formula and then substitute numbers.
- *Never start with definitions* → a money video must **not** open on "money is a store of
  value, a unit of account and a medium of exchange". Open on a barter failure, or on the
  question of why anyone holds an asset that pays no interest; the three functions arrive as the
  answer.
- *Every movement deliberate* → the curve shifts because a parameter changed, and the narration
  says which. No drifting, no decorative easing, no pan that carries no information.
- *Memorable* → the closing frame of a Solow video is the consumption hump with the competitive
  steady state marked strictly left of the peak, both conditions written underneath. That single
  image is the whole lecture.

> **Where the project already encodes this.** The `NotebookLM/video/*.md` prompts were written
> against the same discipline and are the closest in-house model: one visual object per video,
> a stated thesis, an explicit scope line naming what belongs to the *other* videos, every beat
> adding one element and nothing else, and a closing image the student should be able to redraw
> from memory. Read one before planning — `aula-06-video-3-diagrama-de-fase.md` is the clearest.

## Instructions

### Step 0: Ask the user — one round, always, before writing anything

**Never start planning without asking**, even when `$ARGUMENTS` names the topic precisely.
A 12-minute video is hours of render and TTS; the wrong cut is all of it wasted. Use one
`AskUserQuestion` round (never a second), pre-filling the recommended option from
`$ARGUMENTS` and from what the project already holds, so the user can accept in one click.

Ask exactly these four:

1. **Purpose** — what is this video for?
   - *Review* — the student has seen the lecture and the lista; compress, go fast, lead with
     the result, spend the time on the step that is actually hard. Assumes notation.
   - *First exposure* — builds from zero, motivates the question before naming the model,
     introduces every symbol when it first earns its place.
   - *One stuck point* — surgical. A single confusion (why $\sigma$ flips the sign, why the
     steady state sits left of the Golden Rule) and nothing else.
   - *Lista walkthrough* — the actual exercise items, in order, animated.
2. **Length** — runtime target. Say what each buys:
   - *3–5 min*, one visual object, one mechanism. The highest-value format for review.
   - *8–12 min*, three to five beats, one model start to finish. **Recommended default.**
   - *15–25 min*, full 3blue1brown scale: motivation, construction, a wrong first attempt,
     the fix, the consequence. Expensive — be sure the topic carries it.
   - *A series of shorts* — several 3-minute videos, one mechanism each, sharing a palette.
3. **Math demonstrations** — does the video derive anything on screen, and how far? Ask it
   as its own question; never infer it from the purpose. A review video can want every step,
   and a first-exposure video can want none.
   - *None* — results only. Each equation arrives finished, is named, and is used; no
     intermediate line ever appears. Right when the derivation is the lecture's job and this
     video exists to make the result mean something.
   - *Intuition first* — the picture carries the argument; at most one equation on screen at
     a time, and every symbol named out loud when it appears.
   - *Balanced* — the derivation is shown and narrated step by step, but algebra that does
     not change the picture is skipped with "which rearranges to". **Recommended default.**
   - *Textbook derivation* — **every line written out on screen**, the way a book sets a
     result it expects you to follow with a pencil: first line stated, each manipulation
     appearing under the last, nothing skipped, no "which rearranges to". Nothing is off
     limits to this — an algebraic slog is a legitimate video if the student has to be able
     to reproduce it. Right for a lista walkthrough, a first-order condition the exam will
     ask for, or any result whose *steps* are the point rather than its picture.

   The answer binds every beat. Under *None*, a beat that needs an intermediate line is the
   wrong beat — cut it, or hand the derivation to `/companion`. Under *Textbook derivation*,
   budget **one step per line** and read *Derivations are written out, line by line* in
   Step 5 before planning the beats: a twelve-line derivation is a beat and a half on its
   own, and the 3–5 minute length will not hold one.
4. **Examples** — what anchors the abstraction? (multi-select)
   - *A calibrated numerical case* — real numbers through the model, arithmetic on screen.
   - *A Brazilian data example* — IPCA, Selic, monetary aggregates. Needs `/lab-data`; say so.
   - *The course's own exercise* — the Kurlat item or lista question, by number and page.
   - *No example* — pure mechanism. Defensible for a "one stuck point" video; rarely else.

Everything else is settled by rule, not by asking:

- **Narration language: English**, per the global rule in `~/.claude/CLAUDE.md`, even though
  the course runs in pt-BR. `--lang pt-BR` overrides for one run. On-screen labels match the
  narration language. If the output is not English, accents are mandatory — unaccented
  Portuguese breaks TTS at the level of meaning.
- **Voice**: from `SPEECHIFY_API_KEY` in `.env`. `--no-voice` renders silent with subtitles
  and leaves each beat's gap intact so the user can record over it.
- **Companion page**: built unless `--no-companion`.
- If an answer implies an uneven split (four beats across a 3-minute budget), **state the
  allocation and proceed** — do not open a second round.

### Step 1: Read the project before planning

Never plan a video about a topic you have not read in this session.

1. `CLAUDE.md` — scope, notation, the code language, and the "NÃO extrapolar" guard.
2. The topic's `rules/*.md` file — formulas, the signed comparative statics, and the
   **"Armadilhas frequentes"** list. That list is the richest source of beats there is: every
   trap is a moment where a competent viewer goes wrong, which is exactly what a video beat
   should dramatise.
3. `Map/books-index.md` — the Kurlat section and **printed page** for every claim. Kurlat's
   offset is 0, so printed page = PDF page. Benigno is paginated 503–524 (`pdf = printed − 502`).
4. `Map/topics-index.md` and any reading map for the lecture — prerequisites and what the
   topic connects to, so the video can say what it assumes and what it sets up.
5. The lecture's own material in `Aula/` and the lista in `Listas/`. Slide PDFs converted by
   markitdown scramble two-column algebra — **read the PDF for any derivation you will animate.**
6. `Resolucao/kurlat_ch*_codigo/*_figuras.py` — figures for this chapter may already exist in
   matplotlib. **Reuse their geometry, calibration and axis ranges**; do not re-derive a curve
   that was already verified. Also read `estilo_mpl.py` for why the project cares about fonts.
7. `NotebookLM/video/*.md` — the house beat discipline, already written down. Inherit it:
   > one visual object per video · every beat adds one element and nothing else · a stated
   > thesis the whole video serves · an explicit scope line naming what belongs to other
   > videos · a **closing image the student should be able to redraw from memory**

### Step 2: Plan, and show the plan before building

Write `Videos/<slug>/plan.md` and **show it to the user before rendering anything**. Text is
cheap to change; a rendered and narrated beat is not.

The plan contains:

- **Thesis** — one sentence the entire video serves. Not a topic label. "Signing the
  derivative is the whole answer, and $\sigma$ is the arbiter" is a thesis; "consumption and
  interest rates" is a label.
- **The cold open, with its clock** — what is on screen in the first 30 seconds and why the
  viewer should care, against Sanderson's **Motivation** criterion. Open on a concrete question
  or a picture that does not yet make sense — **never** on a definition or an outline ("never
  start with definitions"). Write the hook out and check it against the 30-second deadline.
- **Beat sheet** — a table: beat id, what is on screen, what moves, the narration's job, the
  seconds budgeted, and the Kurlat page it is anchored to. Budget from the length answer at
  **roughly 150 spoken words per minute**.
- **The wrong first attempt**, where the topic has one. Showing a plausible approach failing,
  then fixing it, is the channel's most characteristic move and the hardest to fake. For a
  Solow video: assume the saving rate maximises consumption, discover it does not. For money:
  treat $MV=PY$ as a theory, discover it is an identity.
- **Scope line** — what is deliberately left out and where it belongs instead.
- **Closing image** — the single frame to hold at the end, and the sentence saying why *this*
  frame is the one worth remembering months later (the **Memorable** criterion).
- **The novelty line** — one sentence on what this video gives that reading the slides does not.
  If you cannot write it, the video should not be made; say so instead of making it.

Beat-count discipline, from the length answer:

| Runtime | Beats | Seconds per beat |
|---|---|---|
| 3–5 min | 3–4 | 45–90 |
| 8–12 min | 4–6 | 90–150 |
| 15–25 min | 6–9 | 120–180 |

A derivation beat is the one exception to the sub-point cap: its lines are one argument, not
a list, so twelve of them are still one beat — budget it in lines and split only when the
runtime says so. Everywhere else, if a beat needs more than three sub-points, it is two
beats. Amplitude expels depth — the
same failure `rules/10_notebooklm_prompts.md` documents for audio prompts.

### Step 3: Write the narration script

Write `Videos/<slug>/script.md`: one block per beat, with the beat id as its heading.

- **Spoken math, never read-aloud symbols.** "m over p equals the square root of F Y over
  two i" — never "M, slash, P, equals, backslash sqrt". The rules in `/speechify` Step 3
  apply in full; this command is that command's spoken register applied to animation.
- **The voice says what the screen is doing.** At every beat, narration and image refer to the
  same object at the same instant. If the narration is ahead of the drawing, the beat is wrong.
- **Silence is a tool.** After a result lands, budget a beat of quiet while the image holds.
  Write it into the script as an explicit pause, because the TTS will not invent one.
- **Numbers are spoken only when they carry a conclusion.** "Two percent target, three percent
  growth, so money grows at three and a half" earns its place; a five-step conversion read
  aloud does not.
- **Every number traces to a source** — `rules/`, the lista, or a `/lab-data` series. Never
  round or improve a figure while re-voicing it.
- Keep each beat's text inside its budget: words ÷ 150 ≈ minutes. Check, do not estimate.

### Step 4: Synthesise the narration and measure it

The narration's **measured** duration drives the animation, not the other way round. Never
guess a duration.

```bash
speechify-tts --check                                      # key + ffprobe reachable
speechify-tts --list-voices                                # pick the narration voice
speechify-tts --script "Videos/<slug>/beats.json"
```

`beats.json` is the contract between narration and animation. One entry per beat:

```json
{
  "voice": "<voice id actually used>",
  "total_seconds": 0.0,
  "beats": [
    {"id": "BeatOne", "text": "...", "audio": "audio/BeatOne.mp3", "seconds": 0.0}
  ]
}
```

Rules:

- `seconds` is measured with `ffprobe`, never taken from the API's estimate.
- `--no-voice`: still write `beats.json`, with `seconds` estimated at 150 wpm, and mark the
  file `"voice": null` so the compile step knows to skip the audio track.
- The key is read from `.env` by the client. **Never inline the key into a scene file, a
  notebook, a command line that gets logged, or `provenance.md`.**
- TTS is billable. Do not re-synthesise a beat whose text has not changed — the client skips
  a beat when the cached audio matches the text hash.

#### Why a manifest instead of the manim-voiceover plugin

`manim-voiceover` (v0.3.7, a Manim Community project) does exist and **would** accept Speechify
as a custom service: you subclass `SpeechService`, implement

```python
def generate_from_text(self, text: str, cache_dir: str = None, path: str = None) -> dict:
```

returning at least `original_audio` (the file path) and `input_text`, optionally
`word_boundaries` — which Speechify's word-level speech marks map onto directly. A scene then
calls `self.set_speech_service(...)` and wraps animations in
`with self.voiceover(text=...) as tracker:`, timing them with `tracker.duration`.

This pipeline deliberately does **not** use it, for two reasons:

1. **Synthesis inside the render loop means re-rendering can re-bill TTS.** Separating them
   makes the audio a cached artefact with a text hash: you can re-render a beat twenty times
   while tuning the animation and pay for the narration once.
2. The manifest approach is **verified end to end on this machine**; the plugin path is not.

If you do adopt the plugin later, keep `beats.json` as the source of truth for the script so
the subtitles and the compile step keep working unchanged. Its interface is recorded above so
the decision can be revisited without re-researching it.

### Step 5: Write the Manim scenes

`Videos/<slug>/scenes.py`: one `Scene` subclass per beat, named exactly as the beat id, with
`run_time` taken from `beats.json`.

**Use the kit.** The `video_explainer` package (installed by `/manim-kit`, never vendored) exists so
that three measured failures cannot recur. Import it rather than hand-rolling plumbing:

```python
"""Scenes for <slug>. One Scene per beat; durations come from beats.json."""
from manim import *
from video_explainer import Beat, Stage, balance_sheet, note, title, axes_panel

class BeatOne(Scene):
    def construct(self):
        st, b = Stage(self), Beat(self, "BeatOne")
        ax, panel = axes_panel([0, 5, 1], [0, 3, 1], x_label="trips per year")
        curve = ax.plot(lambda x: 2 * x ** 0.5, color=BLUE)
        b.step(st.show("title", title("Why hold money at all?")), t=0.6, hold=1)
        b.step(st.show("main", panel), t=1.0, hold=2)
        b.step([Create(curve)], t=1.2, hold=4)          # motion is fast; the hold carries the voice
        b.step(st.show("note", note("more trips, smaller balances")), t=0.8, hold=3)
        b.run()                                          # ends exactly on the narration's length
```

### The pacing rule — the one that was got wrong

**Animations run at their own natural speed; the narration's slack is spent HOLDING a still
frame.** Never stretch one animation across a whole paragraph of speech.

This is not a matter of taste. The first cut of the Aula 7 video spread each beat's full
duration across seven or eight animations and averaged **15.2 seconds per animation**, against
an idiom of roughly **0.5 to 3 seconds**. Every movement crawled. The viewer's verdict was
immediate: *"video movement is too slow."*

- `t` (the motion) stays between **0.6 and 2.0 seconds**. The kit raises `ValueError` above 3.
- `hold` is a relative weight for the still frame that follows, and that is where a
  150-second narration actually goes.
- **A long beat gets MORE steps, never slower ones.** Budget **12 to 20 steps per beat**.
  Seven steps in a 150-second beat is the bug, not a style.
- Reveal progressively: axes, then curve, then label, then annotation — four steps, not one.

### The layout rule — nothing is drawn over anything

Free-floating labels placed with `next_to` collide, and the result is unreadable. A frame from
the first cut had *"lend, and deposits rise"* written straight across *"excess reserves,
earning nothing"*.

- **All text goes through `Stage`.** Slots are `title`, `main`, `left`, `right`, `aside`,
  `note`, and each holds **one occupant**: `st.show("note", x)` removes what was there.
- A second idea in the same region **replaces** the first. It does not join it.
- Labels bound to a chart are fine, because they belong to that mobject group — but two such
  labels must never share space either.

### Tables have cells

Three labels stacked inside one rectangle is not a table; it is three labels and a box, and it
reads as a mistake. Use `table()` or `balance_sheet()` from the kit: real rules, one cell per
value, one row per line item. A balance sheet with reserves, bonds and loans has **three rows**
on the asset side, each in its own cell.

### Derivations are written out, line by line

Only under the *Textbook derivation* answer from Step 0 — the other three settings forbid
this. Here the algebra **is** the visual object, and the beat is the page of a book being
written, not a picture being built.

- **One line per step.** Line appears, holds while the voice says what was done to it, next
  line appears beneath. A `Beat` of 150 seconds carries roughly twelve to eighteen lines at
  `t=0.6` with the slack in `hold` — the ordinary 12–20 steps per beat, spent on algebra.
- **Keep the derivation as one `VGroup` and grow it.** The `main` slot holds one occupant, so
  the occupant is the whole stack: append the new `eq()` below the last, and in the same step
  shift the group up when it reaches the bottom of the slot. The shift is the same object
  moving, so it is still one new element per step.
- **The live line is `focus`; every line above it goes `muted`.** The viewer must know, at a
  glance, which line the voice is on. Recolour the previous line in the step that introduces
  the next one.
- **Animate the manipulation, never the retype.** A term crossing the equals sign is a
  `Transform` of the line into its successor; it is the one moment where the animation
  outperforms the book, and re-typesetting it as a fresh line throws that away. Use a fresh
  line for a genuinely new statement (substituting a second equation, imposing a condition),
  and `Transform` for rearrangement of the line already on screen.
- **Number the lines you refer back to** — `(1)`, `(2)`, in `muted` at the right margin,
  exactly as a book does — and say the number out loud when you use it later.
- **Say what was done, not what is written.** "Divide both sides by $P$" while the division
  happens; never read the resulting line aloud symbol by symbol. The screen already has it.
- **Collapse before moving on.** When the derivation ends, clear the stack and re-show the
  result alone. Carrying fourteen `muted` lines into the next beat buries it.
- **At most one derivation of this depth per video** unless the answer to *Purpose* was
  *lista walkthrough*. Two back to back is a lecture recording with better fonts.

Other scene rules:

- **One new element per step.** If a step introduces axes, a curve, a label and a shift, it is
  four steps wearing one coat.
- **Animate the transformation, not the replacement.** `Transform` an equation into its
  rearrangement so the viewer sees which term moved; do not `FadeOut`/`FadeIn` between two
  states. Watching the term move is the explanation.
- **`MathTex` needs LaTeX** and therefore costs render time; `Text` does not. Use `MathTex`
  for mathematics and `Text` for prose labels.
- **Manim is not the only way to make a picture, and for dense data it is the wrong way.**
  Manim is excellent at *construction* — a curve being built, a term moving to the other side of
  an equation. It is poor at a scatter of a hundred and fifty points or a twenty-six-year time
  series. Use `mpl_figure()` from the kit for those: it draws with matplotlib on a transparent
  ground, caches the PNG under `figures/`, and returns an `ImageMobject` you place in a Stage
  slot like anything else. `svg_asset()` and `image_asset()` bring in vector art and stills.
- **Colour carries meaning, consistently, for the whole video.** Pick one role per colour and
  write the mapping into `plan.md` — e.g. `BLUE` the function, `YELLOW` the object of
  attention, `RED` the thing that breaks, `GREY` what is background. A colour that means two
  things means nothing. Use Manim's named constants, not raw hex, so the palette stays coherent.
- **Notation follows Kurlat.** Where the lecture slides diverge from the book, say which you
  are using in the first beat, exactly as a solution would.
- **Scope guard.** The forbidden list, from `CLAUDE.md`: no stochastic DSGE, no Bellman or
  dynamic programming, no stochastic RBC, no time-series econometrics, no canonical
  log-linearised Calvo NKPC, no Kurlat ch. 8, nothing from chs. 12–15, nothing from
  Ljungqvist & Sargent. Kurlat's Cagan money demand (exercise 11.6) **is** in scope.
- Keep a scene under ~60 lines. A beat that needs more is under-planned.

### Step 5b: Visual assets that did not come from Manim

A video made only of Manim primitives looks like a video made only of Manim primitives. Widen
the palette — within one hard constraint.

**What you may bring in**

- **matplotlib figures**, via `mpl_figure()`. The right tool for scatters, long time series,
  histograms, heatmaps, anything with many marks. The kit styles axes for a dark canvas and
  caches the PNG, so re-rendering a beat does not redraw the chart.
- **Original vector art** you draw as SVG, via `svg_asset()`. Diagrams, schematics, icons.
- **Generated images** — PIL or a procedural texture — for backgrounds and fills.
- **Public-domain and openly licensed material**: Wikimedia Commons, the Internet Archive's
  public-domain collections, NASA, and the statistical agencies and central banks whose charts
  and photographs are public records (FRED, BLS, IBGE, BCB). CC0 needs nothing; CC-BY needs the
  attribution actually written down.

**What you may not**

Do not download video or stills from YouTube, TikTok, or any other platform to cut into the
piece. That material is somebody's copyrighted work, taking it breaks those platforms' terms,
and "it is for a course" does not change either fact. The same goes for stock imagery behind a
licence the project does not hold, and for frames lifted from a film or a broadcast.

If a specific clip genuinely is the only way to make a point — a famous press conference, a
particular news segment — the honest options are to **link** to it beside the video, to
**describe** it, or to **reconstruct** the relevant object yourself: a chart of what was said,
a schematic of what happened, a quotation on screen with its source.

**Provenance is part of the deliverable.** Every asset that did not originate in this project
goes into `provenance.md` with its source URL, its licence, and the date it was retrieved —
the same discipline the data series already follow. `image_asset()` refuses to load anything
without a `credit`, deliberately.

### Step 5c: Prove the layout before spending a render

```bash
layoutcheck "Videos/<slug>"        # every scene, no frames written, ~30 s a beat
```

It runs each scene with Manim's own `skip_animations` and fails on any text drawn over other
text or over a brace. Fix every collision before rendering. A covered glyph is a **wrong
caption** -- beat 1 of aula-07 once read `.5 points` because a brace sat on the `1` -- and
neither the renderer nor a glance at the file will tell you.

**A checker that flags everything is broken, not thorough.** The first version of this probe
imitated Manim's staging instead of using it, re-added every faded-out mobject, and reported
a collision in all twenty beats. What exposed it was pulling the flagged frame out of the
rendered video with `ffmpeg -ss <t> -frames:v 1` and looking: the frame was clean. Before
reporting collisions to the user, check one flagged frame against the actual video. Before
trusting a clean result, break something on purpose and confirm the checker says so.

### Step 6: Render the beats

```bash
cd "Videos/<slug>"
for S in BeatOne BeatTwo ...; do python -m manim render -ql --media_dir "media" scenes.py $S; done
```

- **Render at `-ql` (854×480, 15 fps) first — always, for every beat.** This is not a
  throwaway: the 480p pass gets compiled into a complete, watchable video, because the only
  reliable way to judge twenty minutes of pacing and composition is to watch twenty minutes of
  it. Stills lie.
- **Then stop and ask** before rendering at `-qh`. See Step 7b.
- `-qm` is 1280×720/30 for a quick look; `-qk` is 4K/60, worth it only when the source material
  genuinely resolves beyond 1080p.
- Higher fps also means finer timing granularity, which shrinks the per-beat rounding the
  compile step has to absorb.
- Renders land in `media/videos/scenes/<resolution>/<SceneName>.mp4`.
- **MiKTeX will try to install a missing package on first use, which hangs an unattended
  render.** If a `MathTex` beat stalls, run that beat once interactively to let MiKTeX fetch
  the package, or set MiKTeX to install missing packages automatically, then re-run.
- A beat whose render fails is a blocker — never compile a partial video and report success.

### Nothing may share pixels — not text, and not a chart with a table

Two collisions were shipped before this rule existed, and they had different causes.

**Text over text.** `Stage` fixed it: six named slots, one occupant each, and showing
something new in a slot removes what was there.

**A chart under a table.** `Stage` did *not* fix that one, because the two objects were in
different slots and every check passed. Two mechanisms, both now closed:

1. **`main` geometrically intersects `left`, `right` and `aside`.** Filling one of those now
   clears the others (`CONFLICTS` in the kit), and `show()` asserts that no two visible
   occupants' bounding boxes overlap — the scene raises at render time rather than producing
   the frame.
2. **`fit=False` used to skip positioning as well as scaling**, so a matplotlib figure was
   never moved into its slot at all: it stayed centred, and the table landed on top of it.
   `fit=False` now means "do not rescale"; the move into the slot always happens.

**To place a chart and a table together, use `side_by_side(chart, table)` and put the result
in `main`.** It scales each into its own column and guarantees a gutter. Never show a chart in
`main` and a table in `right`.

And route everything through the kit: a raw `self.play(...)` bypasses both `Beat`'s timing and
`Stage`'s collision guard, so a collision placed that way is invisible to every check.
`beatcheck Videos/<slug>` fails the build on raw plays for exactly this reason.

### Step 6b: Gate the pacing mechanically, before you compile

Judging pacing by eye is how a 20-beat video shipped at **15.2 seconds per animation**. Run
the gate instead:

```bash
beatcheck "Videos/<slug>"                              # static: steps, motion share, max t
beatcheck "Videos/<slug>" --rendered                   # also ffprobe every beat
beatcheck "Videos/<slug>" --rendered --quality 1080p60
```

It fails the build when a beat has too few steps for its length, when motion exceeds 30 per
cent of the beat, when any single animation runs over 2 seconds, when a scene never touches a
`Stage` slot, or when a render's length disagrees with its narration by more than about half a
second. Exit code 2 means fix the scene, not the gate.

**A tool a step names must exist and must run.** A plan that cites a gate like `beatcheck` before
anyone has written it is not a plan, it is a wish — and the first sign of it is a bare
`ls: cannot access 'tools/'`. Before citing a command anywhere: run it, see it exit 0, and fix
it if it does not. When the gate itself was first written it had two bugs — it read a stale
render directory and had the sign of the duration comparison backwards, so it failed all
twenty beats that were in fact correct. **Verify the verifier.**

These are console scripts from the installed package, so they run from any directory.

### Step 7: Compile into one video — the exact pipeline, measured

**Use the shipped script. Do not hand-roll this in shell.**

```bash
explainer-compile "Videos/<slug>" --name "<slug>"
explainer-compile "Videos/<slug>" --no-audio                # silent + subtitles
```

It exists because three failure modes were measured on this machine, and a shell one-liner
walks into all three:

1. **Manim quantises to whole frames, and rounds per `self.play()` call.** A beat can render
   *shorter* than its narration even when the fractions sum to 1.0 — measured: a beat whose
   narration is **16.656 s** rendered as **16.600 s**. Padding the audio to the video length
   would have cut 56 ms of speech off mid-word. So each beat's slot is **`max(video, audio)`**:
   the audio is padded with silence *and* the video's last frame is frozen, whichever is short.
2. **Concatenating AAC clips accumulates per-clip padding** — 10.1 ms over two clips, which
   becomes visible lip-flap on equations over twenty. Audio is concatenated as lossless PCM
   and encoded to AAC exactly **once**, at the mux.
3. **ffmpeg cannot open Git Bash's `$PWD`.** A POSIX `/tmp/claude/...` path handed to the
   native Windows ffmpeg fails with "No such file or directory". Concat entries resolve
   relative to the list file, so the script writes **relative** paths and the problem vanishes.

The script reports a per-beat table and the measured drift, and **exits non-zero if drift
exceeds one frame** (default tolerance 40 ms). Measured on the reference two-beat project:
27.467 s out, **10.7 ms drift**, video frozen on the one beat that needed it.

Never paper over drift with `-shortest` — it hides the problem by truncating whichever stream
is longer, which is exactly the speech you wrote.

Generate `<slug>.srt` from `beats.json` by accumulating the measured durations — the
subtitles then cannot drift from the audio, because both came from the same measurements.

### Step 7b: Compile the draft, hand it over, and ask before going high

**The 480p compile is a deliverable, not a throwaway.** Run the full compile on the draft
renders and give the user the file:

```bash
explainer-compile "Videos/<slug>" --name "<slug>-480p"
```

Report its duration, size and measured drift, and say plainly what it is: the whole video at
854x480 - correct in content and timing, low in resolution.

**Then ask, and wait.** Never start the high-quality render on your own initiative:

> "Draft compiled: N min, <size>, <drift> ms drift. Render the 1080p60 master now?
> That is roughly <estimate> of render time for N minutes of animation."
> - **Yes, render 1080p60 now**
> - **Not yet - I want to watch the draft first**
> - **Fix something first** (name it; a re-render at 480p is cheap)

Why this is a rule and not a preference: a 1080p60 pass over ~40 minutes of animation runs
well over an hour, and every fault found by watching - a slow beat, a collision, a label that
reads wrong - invalidates all of it. Watching costs minutes; re-rendering costs hours. The
draft exists so that the expensive pass happens exactly once.

**On a yes**, re-render every beat at `-qh`, compile again under the final name, and re-run
the gate at the new quality:

```bash
beatcheck "Videos/<slug>" --rendered --quality 1080p60
explainer-compile "Videos/<slug>" --name "<slug>"
```

### Step 8: Offer a companion — do not build one

**An interactive companion is not part of this command's output.** Building one unasked
produces a thin page nobody requested, and the useful version needs decisions this command has
no business guessing: which variables become controls, their ranges and units, what is plotted
against what, which quantities are read out live.

So: **offer** it, in one line, and stop. If the user wants one, `/companion` builds it — it
asks in detail first, and it supports several controls rather than the single slider this
command used to emit.

### Step 9: Report

`provenance.md` records: the topic and thesis, every source cited with chapter/section/printed
page, the voice id used (never the key), Manim and ffmpeg versions, the render quality, the
per-beat and total durations, the measured drift, and the companion's URL.

Then report to the user:

| Beat | On screen | Narration (s) | Render (s) | Drift |
|---|---|---|---|---|
| BeatOne | axes + curve + label | 2.50 | 2.53 | +0.03 |
| … | | | | |
| **Total** | | **6.52** | **6.53** | **0.01** |

Plus: the final file path and its duration, resolution and size; the companion link; what was
deliberately left out and where it belongs; and anything that could not be verified.

## Important

- **Ask first, always.** Purpose, length, math demonstrations and examples change every beat. One
  round, before planning — and show `plan.md` before rendering.
- **Never compile a video whose beats did not all render.** Report the failure instead.
- **The narration is measured, never estimated.** Every duration in `beats.json` comes from
  `ffprobe` on real audio.
- **Never print or commit the API key.** It lives in the gitignored `.env`; the client reads
  it from the environment. `provenance.md` records the voice, not the credential.
- **One visual object per beat, one meaning per colour, one thesis per video.** These three
  are what separate an explainer from an animated slide deck.
- **Motion is fast and holds are long.** 12 to 20 steps a beat, each under 3 seconds. The
  measured failure was 15.2 seconds per animation; do not repeat it.
- **Nothing is ever drawn over anything.** Every piece of text goes through a `Stage` slot,
  one occupant each.
- **Tables have cells.** One row per line item, real rules. Never labels stacked in a box.
- **Compile at 480p first, then ask.** The draft is a watchable deliverable, not a
  throwaway. Never spend an hour of 1080p render on a cut nobody has watched.
- **Every borrowed asset carries its licence.** See the assets rule below; if you cannot name
  the source and the licence, it does not go in the video.
- **Do not build a companion unasked.** Offer it; `/companion` builds it.
- **Scope guard holds inside animations too.** A pretty visualisation of an out-of-scope model
  is still out of scope.
- **Do not animate exercise statements** from a textbook — reference them by number and page,
  the same rule `/exercise-plan` and `/speechify` follow.
- **Every generated `.mp4` stays out of git — the final `<slug>.mp4` included.** It is
  rebuilt from versioned sources, so `.gitignore` must carry `Videos/*/media*/` (any
  `--media_dir` variant, e.g. `media_nocache/`), `Videos/*/audio/`, `Videos/*/build/`,
  `Videos/**/*.mp4` (recursive: every mp4 at any depth) and `Videos/*/*.log`; add any that
  are missing before the first render. After compiling, run
  `git check-ignore -v "Videos/<slug>/<slug>.mp4"` and fix the ignore if it prints nothing.
  Version `plan.md`, `script.md`, `beats.json`, `scenes.py`, `<slug>.srt`, `companion.html`
  and `provenance.md` (which records the mp4's checksum).
- **TTS and rendering both cost.** Re-synthesise only changed beats; draft at `-ql` and go to
  `-qh` once.

## Ecosystem

- `/speechify` → the same spoken-math discipline, for listening to a whole chapter. This
  command is that register applied to animation: `/speechify` is hours of audio, `/explainer`
  is minutes of audio married to a picture.
- `/notebooklm` → its `NotebookLM/video/*.md` prompts are the beat discipline this command
  inherits, and are the cheap way to get a video-shaped explanation without rendering one.
  Use `/notebooklm` to explore a cut, `/explainer` to produce it.
- `/manim-kit` → the reusable drawing layer this command's scenes import, and how to install
  it in another project so a new video costs a short scene file instead of a thousand lines.
- `/companion` → the interactive page, built only when asked, with several controls.
- `/lab-data` → any real data series a beat plots, with provenance; `/lab` for the simulation
  behind a calibrated example. Never fetch data inside a scene file.
- `/intake` → the front door that decides a topic deserves a video in the first place.
- `Resolucao/kurlat_ch*_codigo/*_figuras.py` → existing verified figure geometry. Reuse it.
- `/setup-study` copies this command into new study projects.

## Sources

The quoted criteria and structural rules are Grant Sanderson's own published wording, not a
paraphrase of the channel's style:

- **The four criteria** (clarity · motivation · novelty · memorable) and the "5-10 minute view"
  remark — <https://www.3blue1brown.com/blog/some1>
- **"Concrete before abstract"**, **"never start with definitions"**, *"a definition is an
  ending point"*, *"the best pedagogical order of ideas is often very different from the correct
  logical order"*, *"every movement on the screen should be deliberate, with an identifiable
  purpose"*, and *"what picture or visual you could use to elucidate a topic"* —
  <https://www.3blue1brown.com/about>
- **The three pillars** (*"the role of visualization, narrative, and the interplay between
  concreteness and abstraction"*) — abstract of "Communicating math online", MIT Applied Math
  Colloquium, 2 December 2019, <https://math.mit.edu/amc/2020ay/sanderson.pdf>
- **Manim Community Edition** docs — <https://docs.manim.community/en/stable/>
- **manim-voiceover** `SpeechService` contract —
  <https://voiceover.manim.community/en/stable/services.html> and
  <https://voiceover.manim.community/en/stable/_modules/manim_voiceover/services/base.html>
- **Speechify API** — behaviour recorded in the "Verified toolchain" table above was established
  by probing `https://api.speechify.ai` live on 2026-09-12 with the project's own key, not from
  documentation alone.

Toolchain measurements in this file (Manim 0.21.0 frame quantisation, the AAC concat drift, the
`max(video, audio)` slot rule, the 10.7 ms end-to-end result) were measured on this machine on
2026-09-12 and are reproducible with `explainer-compile` from the `video_explainer` package.
