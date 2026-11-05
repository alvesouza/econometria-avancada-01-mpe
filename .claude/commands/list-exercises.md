---
description: Extract and list exercises, problems, and quiz questions from course materials (MD, HTML, PDF, notebooks). Preserves math notation.
argument-hint: <file-or-dir>
allowed-tools: Read Grep Glob Bash PowerShell
---

Extract exercises from the file(s) or directory specified by `$ARGUMENTS`.

## Instructions

0. **Auto-discover:** If `$ARGUMENTS` is a directory, do NOT assume it's named `Listas/` or any fixed name. Scan the directory's contents to identify exercise files by their content (numbered problems, "Exercício", "Lista", etc.), not by the directory name.

1. Scan the target for exercise content. Detect format automatically:

   **Markdown / text files:**
   - Look for: numbered questions (Q1, Q2...), "Exercício", "Problema", "Questão", "Exercise", numbered lists with problem content

   **HTML files (Quarto slides):**
   - Look for exercise sections in `<section>` tags, practice blocks, problem slides

   **HTML quiz files:**
   - Parse the JavaScript `Q` array to extract questions, options, and correct answers

   **PDF files:**
   - Convert via markitdown first, then scan the resulting text

   **Jupyter notebooks (.ipynb):**
   - Look for markdown cells with exercise prompts, numbered problems

2. For each exercise found, output:
   ```
   [source-file] #N — Exercise text (first ~200 chars if long)
   ```

3. Preserve all math notation (LaTeX).
4. Match the language of the source material.
5. Group exercises by source file, with a count per file and total at the end.

## Important

- For quiz HTML files, include the topic tag and number of options per question.
- For multi-part problems, list each sub-question separately with the parent reference.
- If exercises reference specific data files or datasets, note that.
- If source files are not in MD format, convert them on the fly via markitdown (Python API, UTF-8) or suggest running `/convert` first.
- Part of the study ecosystem: extracted exercises feed `/solution` for step-by-step answers and `/study-map` for cross-references.
