---
description: Convert PDF/EPUB books into structured multi-file LaTeX with extracted figures and TikZ stubs. Three-stage pipeline (extract → post-process → TikZ stubs) with Claude-assisted math/structure refinement.
argument-hint: <pdf-path> [--chapters=N-M] [--no-compile] [--force]
allowed-tools: Read Grep Glob Bash PowerShell Write Edit AskUserQuestion
---

Convert the file specified in `$ARGUMENTS` from PDF/EPUB to structured, multi-file LaTeX.

## Step 1 — Parse arguments

Parse `$ARGUMENTS` for:
- **Input path**: PDF or EPUB file path (relative to `Livros/` or absolute)
- **`--chapters=N-M`**: optional, restrict to a chapter range (e.g. `--chapters=1-5`, `--chapters=3`)
- **`--no-compile`**: skip pdflatex compilation
- **`--force`**: overwrite existing output directory

Detect the book by filename:
- "Mas-Colell" / "MWG" → `mwg`
- "Nicholson" / "Snyder" → `ns`
- "Jehle" / "Reny" → `jr`
- Other → `generic`

Derive `<book-name>` slug (e.g. `mwg`, `ns`, `jr`).

## Step 2 — Read context

1. Read `CLAUDE.md` for LaTeX contracts and project scope
2. Read global `~/.claude/CLAUDE.md` for the mandatory font rule (`lmodern` + `cmap`)
3. Read `Map/books-index.md` if it exists, for structure reference
4. Check if `tex conversion/<book-name>/` already exists — if so, require `--force` or ask the user

## Step 3 — Extract PDF metadata

Run a quick Python one-liner to get page count and TOC:

```python
import fitz; doc = fitz.open("<pdf-path>"); print(f"Pages: {len(doc)}"); print(doc.get_toc(simple=True)[:20]); doc.close()
```

Review the TOC to understand Part/Chapter/Section structure. For MWG, note the five parts:
- Part I: Individual Decision Making (Ch 1–6)
- Part II: Game Theory (Ch 7–9)
- Part III: Market Equilibrium and Market Failure (Ch 10–14)
- Part IV: General Equilibrium (Ch 15–19)
- Part V: Welfare Economics and Incentives (Ch 20–23)

If the book is large (>200 pages) and no `--chapters` flag, recommend processing one part at a time.

## Step 4 — Run extraction script

Execute the main extraction script:

```
python ~/.claude/commands/templates/pdf_to_tex.py "<pdf-path>" "tex conversion/<book-name>" [--chapters=N-M] [--book-id=<id>]
```

This produces:
- `main.tex` + `preamble.tex` + `partN.tex` files
- `figures/` directory with extracted PNGs
- `figures/figures-manifest.json`

Check the output for basic sanity (files exist, non-empty).

## Step 5 — Run post-processing

```
python ~/.claude/commands/templates/tex_postprocess.py "tex conversion/<book-name>"
```

Review any warnings. Fix critical issues (unmatched delimiters, unclosed environments).

## Step 6 — Generate TikZ stubs

```
python ~/.claude/commands/templates/tikz_stub_gen.py "tex conversion/<book-name>"
```

This creates `tikz/fig-*.tikz.tex` stubs for each extracted figure, classified as graph/diagram/table/photo.

## Step 7 — Claude-assisted refinement (CRITICAL)

This is the most important step. The Python scripts produce a best-effort skeleton, but PDF text extraction is inherently lossy — especially for math.

For each `partN.tex` file:

1. **Read the source PDF** (the page range for that part) using the Read tool
2. **Read the generated `.tex`** file
3. **Fix and improve:**
   - **Math**: Replace garbled Unicode math with proper LaTeX commands. Look for Greek letters that weren't converted, broken subscripts/superscripts, missing delimiters. Ensure display equations use `\[...\]` or `equation` environment.
   - **Formal elements**: Ensure Definitions, Propositions, Theorems, Proofs are wrapped in proper environments (`\begin{definition}...\end{definition}` or `\begin{mwgdef}{ID}{Title}...\end{mwgdef}` for MWG). Every formal element must have a `\label{prefix:ID}`.
   - **Cross-references**: Verify that every in-text mention of "Proposition X.Y.Z", "Definition X.Y.Z", "Example X.Y.Z" etc. is a clickable `\hyperref[label]{text}` link pointing to the corresponding `\label`. Fix any that the script missed — especially implicit references like "the proposition above" (make them explicit). Add `\label{sec:X.Y}` to `\section` headings so "Section 19.E" references also work.
   - **Section hierarchy**: Verify `\part`, `\chapter`, `\section` nesting matches the book's structure
   - **Figure references**: Verify `\figref{id}{caption}` calls have correct captions from the source
   - **Footnotes**: Place `\footnote{...}` correctly
   - **Tables**: Verify `tabular` environments have correct column counts and content
4. **Do NOT rewrite** the entire file — make surgical edits using the Edit tool

Work on **one part file at a time** to stay within context limits.

## Step 8 — Compile (unless `--no-compile`)

From the output directory, run pdflatex twice:

```
cd "tex conversion/<book-name>" && pdflatex -interaction=nonstopmode main.tex && pdflatex -interaction=nonstopmode main.tex
```

If compilation fails:
1. Read the `.log` file to identify the error
2. Fix the offending `.tex` file
3. Rerun (max 3 retry cycles)

After successful compilation, verify fonts:
```
pdffonts "tex conversion/<book-name>/main.pdf"
```

All fonts must be Type 1 (never Type 3), with `uni = yes`. If any Type 3 fonts appear, ensure `lmodern` and `cmap` are loaded in the preamble.

## Step 9 — Report

Show a summary:
- Book name and detected type
- Parts/chapters extracted
- Total pages processed
- Number of figures extracted
- Number of TikZ stubs generated
- Compilation status (success/failure/skipped)
- Output path

## Notes

### The `\figref` macro
Every figure uses `\figref{fig-id}{caption}`. At compile time this checks:
1. If `tikz/fig-id.tikz.tex` exists → inputs the TikZ code
2. Else if `figures/fig-id.png` exists → includes the PNG
3. Else → shows a placeholder box

To progressively replace PNGs with TikZ, just populate the `.tikz.tex` file — no edits to part files needed.

### Cross-references (clickable links)

The extraction script automatically creates a two-way cross-reference system:

**Labels on formal elements:** Every Definition, Proposition, Theorem, Lemma, Corollary, Example, and Exercise gets a `\label` when detected. The label scheme is:
- `\label{def:3.B.1}` for Definition 3.B.1
- `\label{prop:19.E.2}` for Proposition 19.E.2
- `\label{ex:19.E.7}` for Example 19.E.7
- `\label{thm:5.C.1}` for Theorem 5.C.1
- etc.

**Hyperlinked in-text references:** Any mention of "Proposition 19.E.2", "Definition 3.B.1", "Example 19.E.7" etc. in running text is automatically converted to a clickable `\hyperref[prop:19.E.2]{Proposition 19.E.2}` link. This works for all formal element types.

During the Claude refinement step (Step 7), also check for:
- References that the script missed (e.g., "see the definition above" → make explicit: "see Definition 3.B.1")
- Broken links (label doesn't exist because the target is in a different part file or wasn't detected)
- Section references like "Section 19.E" → `\hyperref[sec:19.E]{Section 19.E}` (add `\label{sec:X.Y}` to `\section` headings manually)

### MWG-specific
MWG uses non-numeric section IDs (3.A, 3.B, etc.) so formal elements use custom environments:
- `\begin{mwgdef}{3.B.1}{Rational Preference Relation}...\end{mwgdef}` with `\label{def:3.B.1}`
- `\begin{mwgprop}{3.D.2}{Utility Maximization}...\end{mwgprop}` with `\label{prop:3.D.2}`
- `\begin{mwgexample}{3.C.1}...\end{mwgexample}` with `\label{ex:3.C.1}`

### Output structure
```
tex conversion/
└── <book-name>/
    ├── main.tex
    ├── preamble.tex
    ├── part1.tex, part2.tex, ...
    ├── figures/
    │   ├── fig-*.png
    │   └── figures-manifest.json
    ├── tikz/
    │   └── fig-*.tikz.tex
    └── main.pdf (if compiled)
```
