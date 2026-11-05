---
description: Convert files (HTML, PDF, PPTX, DOCX, EPUB, TXT, and any text-based format) to Markdown using markitdown. Preserves LaTeX math and handles UTF-8 encoding. Part of the study ecosystem — feeds /summarize, /list-exercises, /quiz-gen, /study-map, and /speechify.
argument-hint: <file-or-glob-or-dir>
allowed-tools: Read Grep Glob Bash PowerShell Write
---

Convert the file(s) specified by `$ARGUMENTS` to Markdown using markitdown.

## Instructions

### Step 1: Discover files

- If `$ARGUMENTS` is a single file: convert that file.
- If `$ARGUMENTS` is a glob pattern: expand it.
- If `$ARGUMENTS` is a directory (or empty — default to current dir): recursively find ALL convertible files:
  - **Supported formats:** `.html`, `.pdf`, `.pptx`, `.docx`, `.epub`, `.txt`, `.rtf`, `.odt`, `.csv`, `.xlsx`, `.xls`, `.json`, `.xml`, `.ipynb`
  - **Auto-discover directories:** scan all subdirectories in the project root — do NOT assume fixed names like `Aulas/` or `Listas/`. Identify directories by their content (PDFs, slides, problem sets, textbooks, etc.) and search all of them.

### Step 2: Check for existing .md files

Scan for files that already have a `.md` counterpart (same base name, same directory).

- If **any** existing `.md` files are found, ask the user **once** (not per file):
  > "Found N files that already have .md versions: [list first 5, then '...and M more' if needed]. Overwrite all, skip all, or let me pick?"
  >
  > Options: **Overwrite all** / **Skip all** / **Let me pick** (list them)
- Apply the user's choice to all files. Do NOT ask file-by-file.

### Step 3: Convert

For each file to convert, use the markitdown Python API with explicit UTF-8:

```python
from markitdown import MarkItDown
import os

md = MarkItDown()
for filepath in files_to_convert:
    result = md.convert(filepath)
    base = os.path.splitext(filepath)[0]
    output_path = base + '.md'
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(result.text_content)
```

Output each `.md` alongside the source file, same base name.

### Step 4: Report

Show a summary table:
```
Converted:
  Aulas/aula-01-standalone.html → aula-01.md (32,634 chars)
  Livros/wooldridge.pdf → wooldridge.md (245,000 chars)
  ...

Skipped (already exist):
  Aulas/aula-00.md
  ...

Errors:
  (none)

Total: N converted, M skipped, K errors
```

### Step 5: Ecosystem integration

After conversion, suggest next steps based on what was converted (using the actual directory names found in the project, not hardcoded names):
- Lecture files → "Run `/summarize <actual-lectures-dir>/` to get structured summaries"
- Books → "Run `/study-map .` to generate Obsidian cross-references"
- Exercise lists → "Run `/list-exercises <actual-lists-dir>/` to extract all exercises"
- All of the above → "Run `/setup-study` if this is a new project, or `/study-map .` to update cross-references"

## Important

- Always use the Python API, never the CLI — this controls UTF-8 encoding on Windows.
- Preserve LaTeX math notation (`\(...\)`, `\[...\]`, `$...$`, `$$...$$`).
- For large files (books, textbooks), warn the user it may take a moment.
- This command is the entry point to the ecosystem: converted MD files are consumed by `/summarize`, `/list-exercises`, `/quiz-gen`, and `/study-map`.
