---
description: Summarize documents or directories into a concise structured overview. Extracts key concepts, theorems, definitions, and formulas. Preserves LaTeX math.
argument-hint: <file-or-dir>
allowed-tools: Read Grep Glob Bash PowerShell
---

Summarize the file(s) or directory specified by `$ARGUMENTS`.

## Instructions

1. Read the target file(s). If a directory, scan its contents to identify all relevant files (MD, HTML, PDF, notebooks, tex) — do NOT assume fixed directory names; identify file types by extension and content.
2. **Write the summary in English**, per the global rule in `~/.claude/CLAUDE.md`, whatever language the source is in. Quoted passages, error messages, UI strings and book/chapter/section titles keep the original wording; the surrounding prose stays English. Another language only when the user asks for it explicitly for this summary.
3. Produce a structured summary:

### For lecture slides/notes:
- Title and topic
- Key concepts and definitions (bulleted)
- Theorems and results (with formulas in LaTeX)
- Important examples or applications
- Prerequisites and connections to other topics

### For problem sets / exercise lists:
- Topics covered
- Number and types of exercises
- Difficulty assessment
- Key techniques required

### For books / textbooks:
- Chapter-level summary with key results
- Important theorems, definitions, and proofs
- Cross-references to course topics if CLAUDE.md or rules/ exist

### For quiz files (HTML or MD):
- Number of questions and topic distribution
- Types of questions (conceptual vs. computational)
- Key concepts tested

### For directories:
- Brief per-file summary (1-2 lines each)
- Overall synthesis: what the collection covers, gaps, progression

## Important

- Preserve all math notation as LaTeX (`$...$` for inline, `$$...$$` for display).
- If CLAUDE.md or rules/ exist in the project, use them to contextualize the summary within the course.
- Keep summaries concise but complete — prioritize what a student needs to know.
- If source files are not in MD format, suggest running `/convert` first for best results.
- Part of the study ecosystem: summaries inform `/quiz-gen` topic coverage and `/study-map` cross-references. For a listening version of the full material (not a summary), use `/speechify`.
