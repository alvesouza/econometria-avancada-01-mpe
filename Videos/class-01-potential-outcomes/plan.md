# Plan: Class 1, Potential outcomes, Neyman–Rubin, selection bias

**Settings (from the brief):** first exposure · ~50 min (a full class) · textbook derivation · calibrated numerical case + book examples (MHE) + Brazilian data (PNS 2013) · narration in English.
**Anchors:** MHE Ch. 1–2 (pp. 3–18, 2008 draft pagination); rules: `rules/02_causalidade_potential_outcomes.md`; class plan: `Map/class-plan.md` Class 1.

## Thesis

A comparison of treated and untreated people measures the causal effect **plus** the difference those people would have shown with no treatment at all. Random assignment is the one device that sets that second term to zero.

## Cold open (first 30 s)

On screen: MHE's NHIS table, built row by row. Hospitalised people: 2.79. Not hospitalised: 2.07 (1 = excellent, 5 = poor health). The gap is 0.71 with t = 58.9.
Voice: "Ninety-eight thousand Americans, and the verdict is overwhelming: people who went to the hospital are in worse health than people who didn't. So, do hospitals make people sick?" The question is on screen by about 0:20. The 30-second deadline is met by a picture that looks wrong, not by a definition.

## Length and allocation

50 min ≈ 7,500 spoken words at 150 wpm. That is twice the longest format the workflow plans for, so the time is split into **6 acts and 22 beats** (≈ 140 s per beat). The result an exam asks for (naive gap = ATT + selection bias) is fully on screen by **minute ~22**. The 3blue1brown "5–10 minute view" rule is met by Acts I–II plus the decomposition. Everything after that deepens the result rather than delaying it.

| Act | Minutes | Beats | Job |
|---|---|---|---|
| I. The puzzle | 0–5 | B01–B03 | The data say hospitals hurt; a bigger sample cannot fix it |
| II. Two worlds | 5–17 | B04–B08 | Potential outcomes on a table we can see completely |
| III. The decomposition | 17–32 | B09–B14 | Naive gap = ATT + selection bias (and the ATE version) |
| IV. Random assignment | 32–42 | B15–B18 | Independence makes the bias vanish, on average |
| V. Experiments in practice | 42–50 | B19–B21 | STAR: balance, effect, the regression form |
| VI. Closing | 50–52 | B22 | The image to remember |

## The calibrated table (verified by script; all numbers exact)

Health index 0–10, higher = healthier (the opposite direction of the NHIS scale; this is said out loud in B05).

| Person | $Y_0$ | $Y_1$ | $D$ | $Y_1-Y_0$ |
|---|---|---|---|---|
| Ana | 3 | 5 | 1 | 2 |
| Bruno | 2 | 5 | 1 | 3 |
| Carla | 4 | 6 | 1 | 2 |
| Davi | 3 | 4 | 1 | 1 |
| Elisa | 8 | 8 | 0 | 0 |
| Fábio | 9 | 8 | 0 | −1 |
| Gabi | 7 | 8 | 0 | 1 |
| Hugo | 8 | 9 | 0 | 1 |

- ATE = 1.125 · ATT = 2 · ATU = 0.25
- Naive gap = 5 − 8 = **−3** · selection bias = 3 − 8 = **−5**
- −3 = 2 + (−5) = 1.125 − 5 + 0.5 × (2 − 0.25)
- Random assignment, all $\binom{8}{4}=70$ ways to treat four people: mean naive gap **= 1.125 exactly**, range −3 to 5.25. One draw (Ana, Elisa, Fábio, Hugo treated) gives 3.5.

## Brazilian data (fetched, cached in `data/`)

IBGE SIDRA table 5082, PNS 2013, Brazil, total. Hospitalised ≥ 24 h in the previous 12 months, by self-rated health:

| Self-rated health | Hospitalised (thousand) | % hospitalised |
|---|---|---|
| Very good / good | 6,643.0 | 4.5 |
| Regular | 3,791.3 | 8.8 |
| Bad / very bad | 1,626.0 | 18.8 |
| Total | 12,060.2 | 6.0 |

Only these published figures are spoken. No derived means (the percentages are rounded to one decimal, so derived means would carry false precision).

## Beat sheet

| Beat | On screen | Narration's job | s | Anchor |
|---|---|---|---|---|
| B01 ColdOpen | NHIS table built row by row; "t = 58.9" | The paradox in 30 s | 60 | MHE p. 10 |
| B02 BrazilToo | PNS bar chart: 4.5 / 8.8 / 18.8 % | Same pattern in Brazil; the arrow runs health → hospital | 120 | SIDRA 5082 |
| B03 WrongFirstAttempt | t-stat grows as n grows; the gap does not move | **Wrong first attempt:** "more data will settle it". Precision ≠ identification. The ideal-experiment FAQ | 120 | MHE pp. 3–7 |
| B04 TwoWorlds | One person, a fork: hospital / home, two health values | Potential outcomes, concrete first; we only ever see one branch | 150 | MHE p. 10–11 |
| B05 TheTable | The 8-person table, columns $Y_0$, $Y_1$ | Name $Y_{0i}$, $Y_{1i}$, $D_i$; the "god's-eye view" no dataset gives | 150 | — |
| B06 FundamentalProblem | Unobserved cells greyed, one by one | Holland's fundamental problem of causal inference | 120 | MHE p. 11 fn. 2 |
| B07 SwitchingEquation | Derivation, 5 lines → $y_i=y_{0i}+(y_{1i}-y_{0i})d_i$ | Textbook derivation from the piecewise definition | 150 | MHE eq. 2.1.1 |
| B08 Estimands | Effect column; ATE, ATT, ATU computed then named | Definitions arrive as the names of numbers already computed | 180 | MHE p. 11 |
| B09 NaiveOnTable | Observed cells only → 5 vs 8 → −3 | The table "says" hospitals hurt, though they help every treated person | 120 | — |
| B10 DerivationATT | Derivation, add and subtract $E[Y_0\mid D=1]$, numbered lines | **The core derivation:** naive = ATT + selection bias | 210 | MHE p. 11 |
| B11 PlugNumbers | Bar: −3 = 2 + (−5) | The bias swallows the effect | 120 | — |
| B12 SignOfBias | Three cards: training programs, hormone therapy, class size | Sign of the bias depends on who selects in | 150 | MHE pp. 12–16 |
| B13 DerivationATE | Derivation to naive = ATE + SB + $(1-\pi)$(ATT − ATU) | Heterogeneity adds a second bias | 210 | standard extension of MHE §2.1 |
| B14 PlugATE | −3 = 1.125 − 5 + 0.875 | Every term on the table | 90 | — |
| B15 Independence | $(Y_0,Y_1)\perp D$; table rows shuffled by coin flips | What independence means on the table | 150 | MHE p. 12 |
| B16 DerivationRandom | Derivation: SB = 0, ATT = ATE | Random assignment solves the selection problem | 180 | MHE p. 12 |
| B17 CoinFlips | Histogram of all 70 assignments; one draw at 3.5; mean line at 1.125 | Unbiased ≠ right every time; why sample size matters *after* randomisation | 150 | — |
| B18 SUTVA | Two patients in one ward; arrows between rows | The Neyman–Rubin model's assumptions: no interference, one version of treatment | 120 | Rubin (1974/1977) via MHE fn. 2 |
| B19 STARBalance | MHE Table 2.2.1, rows built | Check balance first: free lunch .47/.48/.50 … | 150 | MHE p. 14 |
| B20 STAREffect | MHE Table 2.2.2 cols (1)–(3) | ≈ 5-point effect; controls shrink the SE (2.19 → 1.21), not the estimate | 150 | MHE pp. 15, 17–18 |
| B21 RegressionForm | Derivation $y_i=\alpha+\rho d_i+\eta_i$ → bias = $E[\eta\mid d=1]-E[\eta\mid d=0]$ | Selection bias is a correlation between regressor and error | 180 | MHE eq. 2.3.1, p. 17 |
| B22 Closing | The closing image | What to remember | 90 | — |
| **Total** | | | **≈ 3,120 s ≈ 52 min** | |

**Derivations:** four (B07, B10, B13, B16) plus the short regression one in B21. The workflow's rule allows at most one deep derivation per video, but you asked for textbook derivation over a 50-minute class, so this video breaks that rule on purpose. Each derivation still ends by clearing the stack and showing its result alone.

## Colour roles (fixed for the whole video)

`ORANGE` = $Y_0$, the untreated world · `BLUE` = $Y_1$, the treated world · `GREEN` = causal effects · `RED` = selection bias · `GREY` = unobserved / muted lines · `YELLOW` = the live line or the object of attention.

## Scope line: deliberately left out

- Conditioning on covariates, CIA, OVB, bad controls → **Class 2** (MHE Ch. 3).
- IV, LATE, compliers → **Classes 3–4**.
- Angrist–Lavy's regression-discontinuity design is named only as an example of a sign of bias; RDD itself is outside the syllabus.
- Greenberg §11.1 (the Bayesian treatment model) → **Classes 14–16**, once the Bayesian tools exist.
- Inference / standard errors beyond reading them off STAR's table.

## Closing image

The 8-row table with half its cells greyed. Beneath it, one line: **observed gap = ATT + selection bias**. A coin sits on the selection-bias term, striking it out.
Why this frame: it holds the whole class. The cells you can never see, the comparison you can compute, the term that lies to you, and the one device that removes it.

## Novelty

The slides state the decomposition. This video shows a dataset where **both** worlds are visible, so you watch the naive comparison lie by exactly the selection bias. Then you watch coin flips average that bias away across all 70 possible experiments.
