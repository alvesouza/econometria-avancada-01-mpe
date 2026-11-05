# Plan: add the newly downloaded books to Map/

Books (in `Livros/`, downloaded 2026-10-16): ISLP (2023), ISLR 2e (2023), Izbicki & Mendonça AME (2020),
Morettin & Singer (prelim. 2021), Bolfarine & Sandoval (2010).

Decisions
- **ISLP becomes the ISL reference ("I")** in class-plan, study-guide, topics-index: the course codes in
  Python and the lecturer cites the 2023 ISL. ISLR 2e shares ISLP's chapter structure (R labs), so it is
  not indexed separately. The ISLR 1e section stays in books-index/exercises-index as legacy.
- Index only chapters the course uses (syllabus + site schedule); other chapters get a one-line entry.
- Pages: printed page numbers, verified with `pdftotext -f N -l N`; record the PDF→printed offset.

Steps
1. Convert the five PDFs to MD with markitdown (next to the PDFs, like the existing books).
2. Four subagents in parallel, one per book (ISLP; AME; Morettin & Singer; Bolfarine), each returning:
   a books-index block (sections, pages, subtopics, course links) and exercises-index rows
   (number, section, page, subtopic tagged with topics-index names, level, verified yes/no).
3. Append blocks to `Map/books-index.md` and `Map/exercises-index.md`.
4. `Map/topics-index.md`: add ISLP / AME / M&S / Bolfarine rungs; switch I-citations to ISLP.
5. `Map/class-plan.md`, `Map/study-guide.md`: switch I-citations to ISLP numbers; add AME, M&S, Bolfarine
   readings where they cover the class (Class 1 inference; Class 2 learning; 3+4 Bayes; 7 GLMs).
6. Verify: every cited exercise ID exists in exercises-index; every wiki-link resolves.
