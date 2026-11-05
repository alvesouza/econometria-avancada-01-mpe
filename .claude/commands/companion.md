---
description: Build an interactive HTML companion for one specific model or relation — several named controls, the model's exact expression, live read-outs and marked landmark cases. Only ever runs when asked for, and asks in detail what the page must do before writing a line of it.
argument-hint: <model-or-relation-or-lecture-or-video-slug> [--from <video-dir>] [--panels 1|2] [--local] [--publish]
allowed-tools: Read Grep Glob Bash PowerShell Write Edit AskUserQuestion Artifact Skill
---

Build an interactive page for the model or relation named in `$ARGUMENTS`: **several** named
controls, the model's **exact** expression, and read-outs that answer a question while the
controls move.

A companion is not a figure with a slider bolted on. It is the one artefact in the project where
the student **changes a parameter and watches the economics respond** — which is precisely what a
rendered video, a PDF and a narration cannot do. Everything else the project produces is
read-only.

## Three things that changed, and this file is where they are binding

| Was | Now | Why |
|---|---|---|
| **One slider.** `/explainer` Step 8 said "one parameter, the one the video argued about". | **Multi-variable**: several controls, typically **three to six**. | One parameter cannot express a model with several margins. The elasticity, the growth rate and the target are three different questions, and a page that exposes one of them answers a third of the model. The discipline moves from *how many* to *what each one earns its place doing*. |
| **Built automatically** as part of making a video. | **On request only.** | A page built as a by-product gets the parameter the video happened to narrate, not the one the student is stuck on. It is a deliverable in its own right or it is nothing. |
| **Asked nothing**, or folded into the video's one question round. | **A mandatory `AskUserQuestion` round, and a second round is allowed here** when the model is not yet pinned down. | The ranges, the defaults, the read-outs and the panel count are the page. Guessing them produces something plausible and useless. This is the one command in the project permitted a second round. |

Discipline did not loosen, it moved: **every control must change something visible, must be named
in the model, and must say on the page what it does.** A control that fails any of those three is
deleted, not hidden.

## When this runs

- The user asks for a companion, an interactive page, a "thing I can play with" for **specific
  content** — a model, a relation, a lecture's mechanism, a lista question's comparative static.
- `/explainer` **delegates** here when the user asks for the video's companion. It no longer
  builds its own; `--no-companion` is the standing default.
- It never runs as a side effect of anything else, and never "while I'm at it".

## What gets produced

One self-contained HTML file, living **next to the content it serves**:

```
Videos/<slug>/companion.html        ← a companion for that video's model
<wherever the content lives>/companion-<model>.html
```

For content with no video — a lecture mechanism, a lista's comparative static — put it beside the
material it serves and name it for the model, not for the lecture number.

**The companion is versioned; render artefacts are not.** `.gitignore` already excludes
`Videos/*/media*/`, `Videos/*/audio/`, `Videos/*/build/` and `Videos/**/*.mp4`. The `.html` is a
source file: it is committed, diffable, and the thing a future run edits instead of re-deriving.
Verify with `git check-ignore -v <path>` rather than assuming.

## Instructions

### Step 0: Ask in detail — mandatory, before reading anything into a design

**Never write a page without this round**, even when `$ARGUMENTS` names the model precisely and
even when a video about it already exists. Pre-fill every recommended option from `$ARGUMENTS`,
from the video's `plan.md` if there is one, and from the topic's `rules/` file, so the user can
accept in one click.

Ask, at minimum:

1. **Which model or relation — and its source.** The chapter, section and **printed page** the
   page is built from. Offer the candidates you actually found (the `rules/` entry, the Kurlat
   section, the Benigno section, the lista item) rather than an open question. A page whose model
   cannot be cited does not get built.
2. **Which variables become controls.** Offer the model's own parameters by symbol and name, as a
   multi-select, and for each confirm **range, default, step and unit**. Say which are structural
   (preferences, technology), which are policy, and which are exogenous conditions — the grouping
   becomes the page's layout.
3. **What is plotted against what** — the axes, their ranges and units — and **whether more than
   one panel** is wanted. Two panels sharing the controls (a level panel and a slope or gap
   panel) is the common case when the point is a trade-off.
4. **Which quantities are read out live.** Levels, the **derivative and its sign**, a gap against
   a target, a ratio, a count. Multi-select, and ask which single read-out is the page's answer —
   that one gets typographic priority.
5. **Landmark cases on the chart** — the 45-degree line, unit elasticity, the Golden Rule peak,
   the target, the steady state, the case where a term vanishes. Which to mark, and whether the
   page should say where the current state sits relative to each.
6. **Where it lives** — published as an Artifact (a private link the user can share) or kept as a
   local file only.

**The second round**, permitted only when the first leaves the model genuinely unpinned. Use it
when, and only when:

- the chosen model has several distinct versions in the source and the answer did not say which;
- a requested read-out needs a parameter nobody has calibrated;
- the requested ranges make a landmark unreachable, or make the curve degenerate over part of the
  range, and the fix is a modelling choice rather than a number to pick;
- the panel count and the control set are inconsistent (four controls, one panel, nothing visibly
  distinguishing two of them).

Ask **only** the unresolved items, say in one line why the first round did not settle them, and
do not re-ask what was already answered. **Never a third round**: if the model is still ambiguous
after two, report exactly what is missing and stop. An unspecified page is not built on a guess.

### Step 1: Read the model at its source

Never build a page for a model you have not read in this session.

1. The topic's `rules/*.md` — the formulas, the **signed** comparative statics and the
   "Armadilhas frequentes" list. The signs there are what the page's read-outs must agree with;
   a page that shows the opposite sign is a bug in the page, not a discovery.
2. `Map/books-index.md` for the chapter, section and **printed page**. Kurlat's offset is 0
   (printed = PDF); Benigno is printed 503–524 (`pdf = printed − 502`). Read the PDF for any
   expression you will implement — converted slide MD scrambles two-column algebra.
3. Any existing figure code for this model: `Resolucao/kurlat_ch*_codigo/*_figuras.py` and, when
   the page serves a video, that video's `scenes.py` and `plan.md`. **Reuse the axis ranges, the
   calibration and the colour roles.** The companion should be recognisably the same figure the
   student already watched, now in their hands — not a second, differently-scaled drawing of the
   same economics.
4. `CLAUDE.md` for notation and the scope guard.

### Step 2: Pin the control contract, and write it down

Before any HTML, write the contract out and keep it in the page's footer as well as in the report:

| Control | Symbol | What it is | Range | Step | Default | Unit | Source | What visibly moves |
|---|---|---|---|---|---|---|---|---|
| Elasticity | $\eta$ | income elasticity of money demand | 0 – 1.5 | 0.01 | 1.00 | — | Kurlat ch. 11, p. NNN | the wedge between $\mu$ and $\pi$ |
| Real growth | $g$ | trend real growth | 0 – 6 | 0.1 | 3.0 | % / year | lista calibration | the whole curve's level |
| Target | $\pi^*$ | inflation target | 0 – 10 | 0.25 | 3.0 | % / year | policy, stated | the target line and the gap read-out |

Rules, each of which has killed a page:

- **Three to six controls.** Two is usually a model with a margin missing; more than six is a
  dashboard nobody reads. If the model genuinely has more, group them and collapse the secondary
  group, or build two pages.
- **Every control appears in the model's written expression**, or is a calibration the page
  declares explicitly. No control for a quantity the model does not contain.
- **Every control must visibly change the picture or the answer.** Sweep each one end to end: if
  the chart and the read-outs are identical, the control is decorative — delete it, or the panel
  is plotting the wrong thing.
- **Ranges must be economically sensible and must make every landmark exactly reachable** at the
  chosen step. A step of 0.03 that reaches 0.99 and 1.02 but never $\eta = 1$ hides the one case
  the page exists to show.
- **Defaults are the course's own calibration**, cited. Not round numbers chosen for looks.
- **One line per control on the page**, in the model's own terms, saying what it does — not
  "adjust eta" but "how much money demand rises with income".
- **A reset to defaults**, always. A page the user cannot get back to the baseline from stops
  being usable after a minute.

### Step 3: Pin the read-outs and the landmarks

- **Levels** with units, **the derivative with its sign stated in words** ("inflation falls"),
  **gaps against a target**, and where relevant a **count** (periods to converge, trips to the
  bank). The sign is usually the whole answer — show it as a word, not only as a number whose
  minus sign the eye skips.
- **One read-out is the page's answer.** Give it size and weight; the rest are supporting.
- **Landmarks are marked on the chart and named**, with a read-out saying which side the current
  state is on: left of the Golden Rule peak, above or below the 45-degree line, at or off target.
  A landmark the user cannot land on exactly is a broken landmark (see the step rule above).
- **Every figure on the page carries its unit**, and every parameter carries **its source** —
  chapter, section, printed page — in a provenance line the page shows, not just in the report.
  A number with no traceable source does not go on the page.

### Step 4: Implement the model, not a drawing of it

- **The curve is the model's exact expression**, evaluated on a grid fine enough that the kink,
  the peak and the asymptote are real features rather than sampling artefacts (a few hundred
  points across the axis, not a spline through three). **Never a fitted polynomial, never a
  hand-tuned bezier, never a curve drawn to look right.** If the page shows a shape the algebra
  does not produce, the page is teaching a falsehood.
- **No closed form? Solve it in the page** — bisection or Newton on the model's own condition —
  and say in the provenance line that the root is numerical. Do not substitute an approximation
  that happens to look similar.
- **Handle the degenerate cases explicitly**: a zero denominator, a unit elasticity, a log-utility
  limit, a negative quantity the model forbids. Show the limiting case and label it; never render
  `NaN`, never silently clamp a value into the visible range, and never let a control reach a
  state the page cannot describe.
- **Real data, if any, is embedded as literal values** with its provenance from `/lab-data`. The
  page never fetches anything.

### Step 5: Build the page

**Load the `artifact-design` skill before writing the file** — and `artifact-diagramming` too if
the page needs a mechanism diagram beside the plot. Then:

- **Theme-aware with a full token set.** The complete light palette on bare `:root`; the dark
  overrides under `@media (prefers-color-scheme: dark)` guarded as `:root:not([data-theme="light"])`;
  the same overrides again under `:root[data-theme="dark"]` so an explicit choice wins both ways.
  `body` gets an explicit token background — never a transparent one.
- **Responsive to about 400 px.** A side gutter of at least 16 px set once; controls stack; the
  plot scales via `viewBox` plus `max-width: 100%`; no horizontal scroll on the body.
- **Self-contained.** No build step, no data fetches, no chart library pulled from a CDN to draw
  one curve. Fonts from Google Fonts are allowed, with a real fallback stack behind every face.
- **Inline SVG for the plot**, with paths computed in JS from the model function. Axes labelled
  with units; ticks where they are read, not everywhere.
- **Tabular numerals** (`font-variant-numeric: tabular-nums`) on every read-out, so figures stop
  jittering sideways as digits change — the single cheapest thing that makes a live page feel
  built rather than assembled.
- **A visible focus state** on every control (`:focus-visible`, a 2 px outline with an offset),
  and native `input type="range"` / `number` so keyboard and screen readers work for free.
- **Colour follows the video's roles** where there is a video — the object of attention, the thing
  that breaks, the result that survives — so the page and the animation speak the same visual
  language.
- **The `<title>` names the page**: "The Elasticity Dial", not "Interactive tool for the money
  growth and inflation relation". Two to four words, specific to this model, stable across
  republishes.
- **One line, visible, saying what this page belongs to** and which printed page the model is from.

### Step 6: Verify before reporting — run every check

1. **Numbers.** Pick **three control vectors** (both ends and the default), compute every read-out
   independently in Python from the same expression, and confirm the page agrees to the displayed
   precision. Put the three triples in the report. A page nobody checked arithmetically is a
   plausible-looking wrong answer.
2. **Every control sweeps.** Both endpoints of each, one at a time: the chart changes, the
   read-outs change, nothing overlaps, nothing leaves the frame.
3. **Landmarks are reachable exactly** at the chosen step, and the "which side" read-out flips at
   the right place.
4. **Reset** restores every default.
5. **Keyboard**: tab reaches every control, arrow keys move it, the focus ring is visible in both
   themes.
6. **400 px**: no horizontal scroll, no clipped labels, controls stacked and still usable.
7. **Both themes**, and the explicit `data-theme` override in both directions.
8. **No `NaN`, no `undefined`, no empty read-out** anywhere in the control space you sampled,
   including the degenerate cases from Step 4.
9. **Signs agree with `rules/`.** If they do not, stop and resolve it before publishing — one of
   the two is wrong and the page must not ship on the assumption it is the rules file.

### Step 7: Publish or keep local, as answered

- **Artifact** → publish with the `Artifact` tool, a one-sentence `description`, an emoji
  `favicon`, and hand back the link. Note that the page is private until the user shares it.
  Re-publishing later uses the same file path (or the artifact's `url`) so the link is stable.
- **Local** → report the file path and confirm it opens by double-click with no server.
- Either way the file stays beside the content it serves, as **What gets produced** sets out, and
  gets committed.

### Step 8: Report

| Item | Report |
|---|---|
| Page | file path, and the Artifact URL if published |
| Model | the expression implemented, with chapter, section, printed page |
| Controls | the full contract table from Step 2 |
| Read-outs | each one, its unit, and which is the page's answer |
| Landmarks | what is marked, and that each is exactly reachable |
| Verification | the three control vectors, the Python values, the page values |
| Left out | which parameters were deliberately **not** exposed, and why |

## Important

- **On request only.** Never build a companion as a side effect of a video, a lecture summary or
  an intake run. If it seems useful, offer it in one line and wait.
- **Ask first, in detail.** One round minimum, a second when the model is not pinned down, never a
  third. An under-specified page is reported as under-specified, not guessed at.
- **The curve is the model's exact expression.** No fitted approximation, no decorative shape, no
  "close enough for the intuition". The whole value of the page is that moving a control produces
  the model's own answer.
- **Every parameter carries its source**, on the page. Every figure carries its unit.
- **A control that changes nothing visible is deleted**, not hidden and not left in "for
  completeness".
- **Self-contained, no network.** No CDN data, no build step, no external state. Fonts are the
  only external resource, and they have fallbacks.
- **The signed comparative statics in `rules/` are the authority.** The page must agree with them;
  a disagreement is a blocker, not a finding.
- **Scope guard.** Kurlat chs. 1–7, 9–11 and Benigno. Nothing from ch. 8 or chs. 12–15, no
  Bellman, no stochastic DSGE, no Calvo pricing, no time-series econometrics. An interactive
  out-of-scope model is still out of scope.
- **Never reproduce a textbook exercise statement** on the page — cite it by number and page.
- **English**, per the global rule, even though the course runs in Portuguese; notation follows
  Kurlat, and any divergence from the lecture's notation is stated on the page.
- **The `.html` is versioned.** It is the source a future run edits; render artefacts are not.

## Ecosystem

- `/explainer` → owns the video. Its companion step **delegates here** and only when the user asks
  for it; the page inherits the video's axis ranges, calibration and colour roles so it is the
  same figure made movable.
- `/manim-kit` → the drawing layer for the animated version of the same model, and the source of
  the five colour roles this page reuses.
- `/lab-data` → any real series the page shows, as embedded literals with provenance. The page
  never fetches.
- `/lab` → where computation that does not fit in a page belongs: a calibration, a simulation, a
  verification path for Step 6's numbers.
- `rules/*.md` → the formulas and the signed comparative statics the read-outs must agree with.
- `/quiz-analyze` → a remediation that keeps naming the same confusion is the strongest possible
  case for a companion about exactly that margin.
- `/setup-study` copies this command into new study projects.
