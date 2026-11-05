# Plan: load the official course site (hedibert.org, Advanced Econometrics 2026)

Source: https://hedibert.org/current-teaching/ → tab "Advanced Econometrics - Professional Master in Economics - 2026".

1. Parse the section into classes (1, 2, 3+4, 5+6, 7, 8, 9, final exam) with every link.
2. Download every file hosted on hedibert.org (pdf, html, txt, csv) into
   `Aula/class-NN/materials/` (combined classes → `class-03-04`, `class-05-06`).
   External links (books, JSTOR, NBER, Drive, shiny apps, other sites) are listed, not downloaded.
3. Write `Aula/COURSE.md`: official info (professor, TA, evaluation, exam rule), per-class
   topics and a link table with local path or external URL, bibliography.
4. Do not edit `Aula/class-01/*` or `Map/class-plan.md`; report the mismatch between the
   draft plan and the real schedule so the user decides on reconciliation.

Verify: every hedibert.org link has a local file of non-zero size; failures listed in COURSE.md.
