# Provenance — class-01-potential-outcomes

**Topic:** Class 1, Potential outcomes, Neyman–Rubin, selection bias (`Map/class-plan.md`).
**Thesis:** a treated-vs-untreated comparison measures the causal effect plus how differently those groups would have done untreated; random assignment sets that term to zero.

## Sources (printed pages of the 2008 MHE draft in `Livros/`; may differ from the 2009 printing)

| Beat | Claim / figure | Source |
|---|---|---|
| B01 | NHIS 2005 table: 7,774 / 90,049; 2.79 / 2.07; s.e. 0.014 / 0.003; gap 0.71, t = 58.9 | MHE §2.1, p. 10 |
| B02 | PNS 2013: 4.5 / 8.8 / 18.8 % hospitalised by self-rated health; 12,060.2 thousand hospitalised | IBGE SIDRA table 5082, variables 5446 and 5450, Brazil, total; cached in `data/sidra_t5082_pns2013.json`, retrieved 2026-10-09 from `apisidra.ibge.gov.br/values/t/5082/n1/all/v/5446,5450/p/2013/c12258/all/c1/6795` |
| B03 | The four research FAQs; t values for other sample sizes are illustrative (t ∝ √n from 58.9 at n = 97,823) | MHE Ch. 1, pp. 3–7 |
| B04 | Neyman (1923), Rubin (1974, 1977) | MHE p. 11, fn. 2 |
| B06 | Holland (1986), "fundamental problem of causal inference" | MHE p. 11, fn. 2 (Holland cited there) |
| B07 | Switching equation $y_i = y_{0i} + (y_{1i}-y_{0i})d_i$ | MHE eq. 2.1.1, p. 11 |
| B10 | Naive = ATT + selection bias | MHE p. 11 |
| B12 | Training programs, hormone therapy (WHI), class size (Angrist–Lavy) | MHE pp. 12–13, 16 |
| B13 | ATE decomposition with heterogeneity term | standard algebraic extension of MHE §2.1 (law of iterated expectations) |
| B16 | Random assignment eliminates selection bias; ATT = ATE | MHE §2.2, p. 12 |
| B16b | The ideal-experiment question | MHE Ch. 1, FAQ 2, p. 4 |
| B18 | SUTVA | Rubin; named in narration, not quoted |
| B19 | STAR: ≈ 12 million dollars, ≈ 11,600 children, class sizes 13–17 vs 22–25; Table 2.2.1 values | MHE pp. 13–14 (Krueger 1999, Table 1) |
| B20 | Table 2.2.2 columns (1)–(4), s.e., ≈ 0.2σ | MHE p. 15 (Krueger 1999, Table 5); "student controls" row = white/Asian, girl, free lunch |
| B21 | $y_i = \alpha + \rho d_i + \eta_i$; bias = $E[\eta|d=1]-E[\eta|d=0]$ | MHE eq. 2.3.1, pp. 16–17 |

## Calibrated example (invented, verified by script)

Eight people, $Y_0 = (3,2,4,3,8,9,7,8)$, $Y_1 = (5,5,6,4,8,8,8,9)$. ATE 1.125 · ATT 2 · ATU 0.25 · naive −3 · SB −5. Mirror selection: naive +5.25, ATT 0.25, SB +5. All 70 assignments of 4 treated: mean gap 1.125 exactly, range −3 to 5.25. Sampling s.d. of the difference in means under complete randomisation (Neyman variance, checked by 20,000-draw simulation): 1.608 (n = 8), 0.479 (80), 0.151 (800), 0.048 (8,000).

## Production

| Item | Value |
|---|---|
| Narration | **Windows System.Speech, voice "Microsoft Zira Desktop", rate 0**. Stand-in: Speechify returned "Insufficient Credits". Synthesised by `tts_sapi.py`. Durations measured with ffprobe |
| Total narration | 3,095.8 s (51.6 min), 26 beats |
| Manim | Community Edition 0.21.0 (per toolchain record) · `video_explainer` 0.2.0, editable install from `../Video explainer` |
| ffmpeg | 8.1.1 (gyan.dev full build) |
| Draft render | `-ql`, 854×480, 15 fps |
| Compile | `explainer-compile`, drift 0.1 ms (tolerance 40 ms) |
| Gates | `beatcheck --rendered`: 26/26 pass (387 steps, ≈ 8 s per step); `layoutcheck`: 26/26 clean after fixing B04 |
| Colour roles | ORANGE $y_0$ · BLUE $y_1$ · GREEN effects · RED selection bias · PURPLE heterogeneity bias · GREY muted/unobserved · YELLOW focus |
| External assets | none: every figure is drawn in Manim from the numbers above |

## To switch to Speechify later

`speechify-tts --script beats.json` (replaces audio and durations) → re-render all beats → `beatcheck . --rendered` → `explainer-compile .`
