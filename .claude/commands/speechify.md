---
description: Turn study material (a reading, a chapter, a summary, a rules file) into a narrated plain-text script for Speechify or any TTS app — math spoken in words, no tables, no code, no markdown. Part of the study ecosystem — consumes /convert and /summarize output, complements /notebooklm audio prompts.
argument-hint: <file-or-dir-or-topic> [--lang <code>] [--split] [--short]
allowed-tools: Read Grep Glob Bash PowerShell Write Edit AskUserQuestion
---

Produce a **listening version** of the material specified by `$ARGUMENTS`.

The output is a plain `.txt` file a text-to-speech app (Speechify, Voice Dream, Edge Read
Aloud, Apple/Android TTS) can read end to end **without ever pronouncing a symbol, a table
cell, or a line of code**. It is not a summary: it carries the same content as the source,
re-voiced so it survives being heard instead of seen.

## Instructions

### Step 1: Resolve the source

- **A file** → narrate that file.
- **A directory** → list the candidates and ask which to narrate (do not silently batch:
  each narration is long).
- **A topic, session, or chapter number** (e.g. "session 6", "chapter 4") → look, in this
  order, for: an existing reading/study document in the project (`Leituras/`, `Map/`,
  `Resolucao/`, or whatever the project calls it), the topic file in `rules/`, the lecture
  slides, and the textbook chapter. Prefer a document that is already structured; narrate
  the book chapter directly only when nothing else covers it.
- If the best source is a PDF with no `.md` counterpart, run `/convert` on it first.

**Never narrate a source you have not read in full.** Pull the section/page anchors while
reading — the narration must be able to say "printed page 199" out loud.

### Step 2: Fix the language, and be strict about accents

- **Default: English**, per the global rule in `~/.claude/CLAUDE.md` — including when the
  source material, the course, and the file names are in another language.
- Another language **only** when the user asks (`--lang pt-BR`, "narrate in Portuguese").
- ⚠️ **If the output is not English, accents are mandatory and non-negotiable.** Unaccented
  Portuguese or Spanish breaks TTS at the level of meaning: the engine reads *e* (and) where
  the text needed *é* (is), *nao* instead of *não*, and stresses the wrong syllable in every
  proparoxytone. Write `é`, `não`, `são`, `você`, `análise`, `variância`. Check before
  delivering (Step 6).
- Technical vocabulary keeps the form the course uses. Terms like *stochastic discount
  factor*, *portfolio sort*, *spanning regression*, *look-ahead bias* stay in English inside
  a Portuguese narration — but say them as words, never as an acronym the listener cannot
  unpack the first time. Expand an acronym on first use, then use it freely.

### Step 3: Convert what the eye reads into what the ear can follow

This is the whole skill. Apply every rule.

**Math → spoken words.** Never emit `$`, `\`, `^`, `_`, `{`, `}`. Say the formula the way
you would dictate it to someone writing on a board, then say what it means:

| Written | Spoken |
|---|---|
| $m_{t+1} = a - b'f_{t+1}$ | "m in date t plus one is equal to a minus b transposed times the vector of factors" |
| $\lambda = R_f \Sigma_F b$ | "lambda is equal to the gross risk-free rate times sigma of the factors times b" |
| $\hat\alpha'\hat\Sigma_\varepsilon^{-1}\hat\alpha$ | "the vector of alphas transposed, times the inverse of the residual covariance matrix, times the vector of alphas" |
| $F(N, T-N-K)$ | "an F distribution with N and T minus N minus K degrees of freedom" |
| $\sum_i w_i^2 \to 0$ | "the sum of the squared weights tends to zero" |
| $t = 2.1$ | "a t statistic of two point one" (pt-BR: "t de dois vírgula um") |

Greek letters are said by name: alpha, beta, lambda, sigma, epsilon, theta.

**Numbers.** In English, keep numerals — TTS reads `4.6%` and `755` correctly; write the
unit as a word when the symbol is ambiguous (`per cent` / `per year`). In Portuguese and
Spanish, **spell decimals out** ("quatro vírgula seis por cento ao ano") — a bare `4,6%`
is read inconsistently. Years and long figures are safer spelled out in any language when
they carry the point of a sentence.

**Tables → spoken enumerations.** A table is invisible to a listener. Turn each table into
a sentence that names the dimension and then walks the rows: *"Compare the two in five
dimensions. First, where the premium comes from: on the covariance view… on the
characteristic view… Second, what the investor should buy…"*. Never leave pipe characters.

**Code → the order of operations.** Do not read code aloud. Replace each code block with a
paragraph naming the routine, its inputs, the sequence of steps, and the one trap that
breaks it: *"Routine five, the joint test. Run one regression per test asset, keep the
intercepts and the residuals, build the residual covariance matrix with the right degrees
of freedom, and check that the number of assets is comfortably below the number of periods."*

**Strip every visual marker.** No `#`, `*`, `_`, backticks, `|`, `>`, links, footnotes,
emoji, `§`, `⚠️`, `→`, `⇒`, `×`, `%` (as a symbol in prose), or bracketed citations. A
cross-reference becomes speech: "section six point three, printed page 199".

**Headings → spoken announcements.** Every part opens by saying what it is, which section
of the source it covers, and the page range. Sub-sections are announced as "six point two",
"six point three" — never as a bare numeral hanging in the air.

**Add what a listener needs and a reader does not.** Signposting ("three things follow, and
the third is the one that matters"), a restatement of the claim before a long derivation,
and a spoken recap at the end of each part. Short paragraphs — one idea each — because
paragraph breaks are the only navigation the app exposes.

### Step 4: Structure the script

Open with a short **"how to listen"**: what this is, how many parts, that math is spoken,
and any scope rule the course imposes (e.g. a methods ceiling — say out loud, each time it
comes up, that a named technique is out of scope and why).

Then the body, one part per section of the source, each ending with a **spoken checklist**
("you should be able to derive… you should be able to state…").

Then the support parts, which are where audio beats reading:

1. **Pitfalls** — each said as "the error is… the correction is…".
2. **Spoken formula sheet** — every numbered equation dictated in order, framed for active
   recall: *"pause after the equation number, say the formula, then hear the answer."*
3. **Implementation** — the routines from Step 3, described, never read as code.
4. **Reading route and exercises** — addresses only (source, chapter, printed page); never
   read exercise statements aloud.
5. **Self-test** — numbered questions with an explicit pause cue between them.
6. **Glossary** — one sentence per term.
7. **The whole topic in five lines** — the last thing heard, and the piece worth replaying.

### Step 5: Write the file

- Format: **plain `.txt`, UTF-8**. Not `.md` — Speechify imports both, but markdown leaves
  syntax the voice may read.
- Location: the project's readings directory if one exists (`Leituras/`, `Readings/`,
  `Map/`); otherwise alongside the source.
- Name: `<source-base>-narrated.txt`, or `<topic>-narrated-<lang>.txt` when a language other
  than English was requested.
- `--split` → also write one numbered file per part (`…-01-intro.txt`, `…-02-…`), for
  listening in an app that treats each file as a track.
- `--short` → produce only the support parts (pitfalls, formula sheet, self-test, five
  lines): a 30-40 minute revision pass instead of the full narration.

### Step 6: Verify before reporting (mandatory)

Run this check and fix anything it flags:

```python
import unicodedata
s = open(path, encoding='utf-8').read()
bad = set(chr(36) + chr(167) + '#*_`|~^{}[]<>' + chr(92))
print("hostile symbols:", sorted({c for c in s if c in bad}) or "none")
print("odd non-ASCII:", sorted({c for c in s if ord(c) > 127
      and not unicodedata.category(c).startswith('L')
      and c not in 'çÇ—–…"' + chr(8220)+chr(8221)+chr(8216)+chr(8217)}) or "none")
print("accented chars:", sum(1 for c in s if c in 'áéíóúâêôãõçàÁÉÍÓÚÂÊÔÃÕÇ'))
w = len(s.split()); print("words:", w, "| ~minutes at 150 wpm:", round(w/150))
print("paragraphs:", len([p for p in s.split('\n\n') if p.strip()]))
```

Gates: **no** hostile symbols; **no** stray non-ASCII beyond letters and normal punctuation;
for a non-English script, the accented count must be in the thousands for a long text — a
near-zero count means the accents were dropped and the file must be rewritten, not patched.

### Step 7: Report

Give the file path, word count, **estimated listening time at 150 words per minute and at
1.5×**, the part list, and the import line: *"Speechify → Add file → pick the `.txt`;
paragraphs become navigation points."* Offer `--split` if the file is over ~90 minutes.

## Important

- **Narration is not summarization.** Keep every derivation, every number, every example. If
  the source proves something in four steps, the narration says all four. `/summarize` is
  the command for compression; this one is for conversion.
- **Every number must trace back to the source.** Do not round, re-derive, or "improve" a
  figure while re-voicing it.
- **Respect the project's scope rules.** If `CLAUDE.md` sets a methods ceiling or marks
  material as non-examinable, the narration says so out loud where it applies, in the same
  terms the written material uses.
- **Do not narrate exercise statements** from a textbook — reference them by number and page,
  the same rule `/exercise-plan` follows.
- **Long is expected.** A chapter-length reading lands at 20,000–30,000 words and two to
  three hours of audio; that is the point. Do not silently compress to save effort.

## Ecosystem

- `/convert` → PDF/HTML/PPTX to markdown; run it first when the source is a PDF.
- `/summarize` → the compressed read; `/speechify` is the full listen. They are different
  deliverables from the same source.
- `/notebooklm` → generates prompts for NotebookLM to produce an **AI-hosted discussion**
  about the material. `/speechify` produces **your own text, read aloud**: faithful, complete,
  and reproducible. Use NotebookLM for a second voice on the topic; use this for the material
  itself.
- `/study-map`, `/exercise-plan` → the narration's "reading route" and "exercises" parts
  should quote their addresses (chapter, section, printed page) rather than invent them.
- `/setup-study` copies this command into new study projects.
