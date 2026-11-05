---
description: Build a single study PDF from a remediation file. Extracts recommended reading pages and exercise pages from book PDFs using the book registry for page mapping, and merges into one file.
argument-hint: <remediation.md> [--no-exercises] [--no-dividers] [--calibrate]
allowed-tools: Read Grep Glob Bash PowerShell Write Edit AskUserQuestion
---

Build a study pack PDF from the remediation file specified in `$ARGUMENTS`.

**Flags:**
- `--no-exercises` — skip exercise pages, only extract reading sections
- `--no-dividers` — skip topic divider pages between sections
- `--calibrate` — detect offsets for unverified books and update `book-registry.json`

## Instructions

### Step 1: Parse arguments and locate files

1. Parse `$ARGUMENTS` for the remediation file path (relative to project root or absolute)
2. If no path given, glob for the most recent `Listas/remediation-*.md` or `Listas/pratica-*.md` or `Listas/lista-reforco-*.md` and use that
3. Read the remediation file and verify it contains "Leituras Consolidadas por Livro" and "Exercícios Consolidados" tables

### Step 2: Load book registry

The **book registry** (`Livros/book-registry.json`) stores pre-calibrated page mapping for each book PDF:
- `offset` — front matter shift (printed page + offset = raw index before scaling)
- `scale` — pages per PDF page (1 = normal, 2 = 2-up scan like MWG)
- `verified` — if true, the script uses these values directly (no auto-detection)

Formula: `pdf_page_index = (printed_page + offset) // scale`

1. Read `Livros/book-registry.json`
2. For each book in the consolidated tables, check if the registry has a verified entry
3. If a book is **not in the registry** or `verified: false`, warn and offer to run `--calibrate`

### Step 3: Locate book PDFs

1. Glob for `Livros/*.pdf` to find available book PDFs
2. Match each book using the registry's `file` field first (exact filename match), then fall back to pattern matching:
   - "N&S 12e" → filename containing "nicholson" or "snyder"
   - "MWG" → filename containing "mas-colell" (not "solutions")
   - "MWG Solutions" → filename containing "mas-colell" AND "solutions"
   - "J-R 3e" → filename containing "jehle" or "reny"
3. Report which books were matched and which are missing

### Step 4: Run the extraction script

```
python ~/.claude/commands/templates/study_pack.py "<remediation.md>" "Livros" "<output.pdf>" --registry="Livros/book-registry.json"
```

The script:
1. Loads the registry and reads offset/scale for each verified book
2. For unverified books, falls back to auto-detection (with a warning)
3. Parses the consolidated reading and exercise tables from the MD
4. For each book, converts printed page numbers to PDF page indices using `(printed + offset) // scale`
5. Merges overlapping ranges to avoid duplicate pages
6. Creates a topic divider page before each book section (using reportlab)
7. Extracts the pages from the book PDF (using PyMuPDF)
8. Saves the merged output

### Step 4b: Calibrate mode (if `--calibrate`)

```
python ~/.claude/commands/templates/study_pack.py --calibrate "Livros" --registry="Livros/book-registry.json"
```

This scans all book PDFs, detects offset/scale for any unverified entries, and updates the registry. After calibration, review the auto-detected values and set `verified: true` manually for each book.

### Step 5: Verify the output

1. Check the output PDF exists and has a reasonable page count
2. Open a few pages to verify content matches expectations
3. Report: number of books, total pages, topics covered

### Step 6: Handle missing dependencies

If PyMuPDF or reportlab is not installed:
```
pip install PyMuPDF reportlab
```

If reportlab is missing, the script still works but skips divider pages (uses `--no-dividers` implicitly).

### Step 7: Report

Show:
- Source: remediation file used
- Registry: path used, which books were verified vs auto-detected
- Books matched: list with offset/scale values from registry
- Output: path and total page count
- Topics covered: from the divider pages
- Warning if any books were not found or not verified

Save the output PDF to `Listas/study-pack-<remediation-slug>.pdf` (same directory as the remediation file, unless user specified a different path).

## Output structure

The merged PDF contains, in order:

```
[Divider: Book 1 Name — list of topics]
[Pages from Book 1: merged reading + exercise ranges]
[Divider: Book 2 Name — list of topics]
[Pages from Book 2: merged reading + exercise ranges]
...
```

Within each book, pages are in book order (ascending page numbers), with overlapping ranges merged to avoid duplicates.

## Examples

```
/study-pack Listas/remediation-arrow-debreu-sdf-2026-07-04.md
/study-pack Listas/pratica-arrow-debreu-radner.md --no-exercises
/study-pack --calibrate
/study-pack                                                   → uses most recent remediation file
```
