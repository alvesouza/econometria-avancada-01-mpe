# Plan: rebuild class plan and maps around the official schedule

Source of truth: `Aula/COURSE.md` (hedibert.org, 9 classes + final exam). Note: `.agent/notes/course-site.md`.

1. `Map/class-plan.md`: rewrite. Overview table (real class → topics → rule files), then one
   section per class: goals (from the site's class description), the professor's materials
   (local files), book reading (pages from `Map/books-index.md`), practice (IDs present in
   `Map/exercises-index.md` only), R. Add "syllabus items not on the site schedule" and
   "site topics beyond the syllabus table" sections. Status: official.
2. `Map/study-guide.md`: reorder blocks to the real class sequence; keep the Before/After/
   Connections format; add the professor's material per block.
3. `Map/topics-index.md`: replace the "no lectures yet" line; add a **Lecture** line per topic
   pointing to the real classes.
4. `rules/01`–`08` header "Lecture" line → real classes; `rules/09` header line → official
   schedule + a short class → topic table.
5. Leave `Map/books-index.md`, `Map/exercises-index.md` and `Aula/class-01/*` unchanged; report
   that the existing `Aula/class-01` notebook/companions are class 5–6 content.

Verify: every exercise ID cited exists in `Map/exercises-index.md`; every local file link exists.
