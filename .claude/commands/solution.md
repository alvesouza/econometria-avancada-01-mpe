---
description: Generate step-by-step solutions for exercises. Uses LaTeX math, includes code (R/Python) when computational. Reads project rules for conventions.
argument-hint: <file-or-exercise-text>
allowed-tools: Read Grep Glob Bash PowerShell
---

Solve the exercise(s) specified by `$ARGUMENTS`. This can be a file path (solve all exercises in it) or inline problem text.

## Instructions

1. **Read project context first** (if available):
   - `CLAUDE.md` — for scope, restrictions, language, bibliography
   - `rules/` directory — for formulas, code patterns, resolution templates
   - These define conventions to follow (e.g., which language for code, notation style, reference format)

2. **For each exercise, follow this pattern:**

   **a) State the problem** — rewrite it clearly, identifying given information and what's asked.

   **b) Identify the method** — name the technique, theorem, or approach. Reference the textbook section if identifiable (e.g., "Wooldridge, Sec. 3-2", "ZaE §4.2").

   **c) Step-by-step derivation** — show every non-trivial step. Use:
   - LaTeX for all math: `$...$` inline, `$$...$$` display
   - Numbered steps for long derivations
   - Intermediate results clearly labeled
   - Number every equation a later step uses and cite it at each step ("using (2) and (4)",
     "substituting (7) into (5)"); keep the statement's own equation numbers
   - Open with a **Notation** list (every variable and parameter, its meaning and range); define
     each new symbol where it first appears
   - One operation per displayed line; display equations instead of long inline chains, with a
     short sentence between displays
   - Show every substitution as its own line: the receiving equation with the substituted expression in place, in parentheses, before simplifying (with (1) $A=B+C$ and (2) $B=2A$: first $A=(2A)+C$, then $C=-A$); numbers plugged in are shown in place before the result, with enough decimals that the displayed arithmetic reproduces the printed value

   **d) Code** (when the problem is computational):
   - Check `CLAUDE.md` for the project's code language — use that (do NOT default to R if the project specifies Python)
   - Follow the matrix-step pattern from rules if available:
     ```r
     # 1) Setup
     # 2) Intermediate calculation
     # 3) Final result
     # 4) Verification with built-in function
     ```

   **e) Interpret the result** — what does the answer mean economically/statistically? Connect back to theory.

   **f) Verification** — cross-check the result (alternative method, numerical check, or limit cases).

3. **Match the language** of the problem statement.

## Scope & Existing Solutions

- **Textbook exercises are OFF by default** — do NOT solve exercises that come directly from the course's book PDFs unless the user explicitly asks for them.
- **Non-textbook exercises are always in scope** — exercises from lists, exams, tutorials, external problem sets, or inline text should be solved normally following all the steps above.
- **If a solution already exists** (e.g., in the solutions directory, tutorial materials, or provided alongside the exercise), do NOT simply reproduce it. Instead:
  1. Read the existing solution carefully.
  2. **Extend and detail it**: fill in skipped algebraic steps, add intermediate explanations, expand economic/statistical interpretation, and include code verification if missing.
  3. If the existing solution contains errors or shortcuts, correct them and note what was changed.
  4. The output should be a strictly more complete version of the original — never shorter.

## Output Format

- **Math-heavy solutions**: write in LaTeX (`.tex` file) and compile to PDF using `pdflatex` or `latexmk`. Place both the `.tex` source and the compiled `.pdf` in the solutions directory.
- **Code-related exercises**: write code in the programming language used by the book. If the book is language-agnostic, default to **Python**. Exception: if the book is focused on computer architecture or performance, use **C/C++**.

## Important

- Write and edit `.tex` with the file Write/Edit tools, not shell heredocs or `sed`: the shell here collapses `\\` to `\` and turns `\b`, `\n` into control characters.
- Never skip algebraic steps that a student might find non-obvious.
- For proofs: state what you're proving, then proceed formally.
- If the exercise has multiple parts (a, b, c...), solve each with clear separation.
- Reference specific textbook pages/sections whenever possible.
