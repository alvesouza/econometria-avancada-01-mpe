# Class 1 materials: verified facts (2026-10-09)

- Moved 2026-10-16 to `Aula/class-05-06/` (official schedule puts potential outcomes in Classes 5+6); notebook renamed `potential-outcomes.ipynb`. Published Artifacts still show the old "Class 1" labels until republished by URL.
- Deliverables: `Aula/class-05-06/potential-outcomes.ipynb` (notes, Python kernel) + three companions in the same folder, published as private Artifacts:
  A `companion-selection-bias.html` https://claude.ai/artifact/NQH4xcffymY5roEKXjkpWv ·
  B `companion-sample-size.html` https://claude.ai/artifact/9wN4ftRgB32YbgFeYa1jG9 ·
  C `companion-eight-person-table.html` https://claude.ai/artifact/KTnW6qcwYkexQ1sz9PYzzo
- Notebook builder lives only in the session scratchpad; edit the .ipynb directly from now on.
- Environment: **R is not installed**; Python startup is slow (imports can take > 60 s); node v24 is available for checking companion JS (stub-DOM harness).
- Illustrative DGP (A, B) closed forms match a 4M-draw Monte Carlo at (τ,λ,π,γ,σ) = (1,−.6,.5,−.5,2) → ATT 1.479, ATU 0.521, SB −1.915, naive −0.436; (−3,−1,.05,−1,.5) → naive −3.054; (3,1,.95,1,3) → naive 9.840.
- 8-person table (same as the video): ATE 1.125, self-selection ATT 2, ATU 0.25, SB −5, naive −3; over all 70 four-of-eight assignments the mean gap = 1.125, range −3 to 5.25, 17 with gap ≤ 0.
- Companion B at N = 10, λ = 0 covers ~89% (z critical value with ~5 per group), so the page says so instead of claiming 95%.
- MHE page refs are printed pages (PDF = printed + 16): NHIS table p. 10, decomposition p. 11, random assignment p. 12, STAR Tables 2.2.1/2.2.2 pp. 14–15, eq. 2.3.1–2.3.2 pp. 17–18.
