# Notes for Classes 5+6 (L05) — plan (2026-10-25)

Spec: `.claude/commands/notes.md` (binding), `.claude/commands/companion.md` Steps 2–6. Shared plan:
`.agent/plans/all-units-study-set.md`. Design copied from `Notas/L01/`, `Notas/L02/` and
`.agent/plans/notas-L01-L02.md` (conventions, `_figstyle.py`, companion check harness).

Step 0 answered by the lead: **Full depth · Equation-led · Model curves (4–8 figures, exact
expressions, comparative statics) · Companions: 1–2 new + link the 3 existing · PDF: yes.**
Status: **taught** (slides exist). Output only under `Notas/L05/` plus this plan.

## Sources (opened this session)

- Slides: `Aula/class-05-06/materials/notes-on-causal-inference.pdf` (38 pp., Lopes, Oct 2024;
  printed page = PDF page), `error-in-variables.pdf` (1 p.).
- Site pages (R, reference): `omitted-variable.html`, `example1-iv-card.html` (+ `card.csv`),
  `example2-DiD-card-krueger.html` (+ `card-krueger.txt`), `example3-RDD-age-mva-internal.html`
  (+ `age-mva-internal.txt`).
- Books, printed pages (offsets in `.agent/notes/book-offsets.md`; MHE +16, W +24, G +15 — all
  spot-checked on the page-number lines):
  - MHE Ch. 2 pp. 10–18; §3.2 pp. 38–50 (CIA 3.2.2, OVB 3.2.11 p. 45, Table 3.2.1 p. 46, bad
    control 3.2.12 pp. 47–49, proxy control 3.2.13–15 pp. 49–50); §4.1 pp. 84–102 (4.1.3 p. 86,
    2SLS pp. 89–91, Wald 4.1.12 p. 94, Table 4.1.2 p. 96); §4.4 pp. 111–118 (LATE theorem 4.4.1
    p. 114 — G only); §5.2 pp. 169–176 (5.2.1–5.2.3, Table 5.2.1 p. 171, Fig. 5.2.1 p. 172);
    §6.1–6.2 pp. 189–202 (6.1.1–6.1.7, fuzzy RD 6.2.5 p. 198 — G only).
  - W §9.4 pp. 287–292 (9.27–9.36, attenuation 9.33 p. 291); §15.1–15.5 pp. 462–484 (15.9–15.13
    pp. 465–466, 15.19–15.20 p. 469, Example 15.4 Card pp. 473–474, weak-IV rule p. 478, §15.4
    EIV by IV pp. 479–481); §13.2 pp. 407–411 (13.10, 13.11, Table 13.3).
  - G §11.2 pp. 173–174 (non-identification of $\beta_s$ without an instrument; Bayesian IV named).
- DAGs, d-separation: slides only (no book on disk).

## Shared facts (do not re-derive)

- `card-krueger.txt`: `treatment = 1` is **New Jersey** (cell means match MHE Table 5.2.1); the
  slide p. 24 phrase "NJ (0) and PA (1)" is a slip. 768 rows = 384 stores × 2.
- `age-mva-internal.txt`: 48 monthly cells, ages 19.07–22.93; `over21 = age > 21`.
- `card.csv`: 3010 rows; `.` = missing (only in variables not used here).
- Existing material to LINK, never rebuild: `Aula/class-05-06/potential-outcomes.ipynb` (MHE Ch. 2,
  selection bias, STAR, regression of experiments), companions `companion-selection-bias.html`,
  `companion-sample-size.html`, `companion-eight-person-table.html`; old draft-plan material
  `Simulados/quiz-class01-{1,2,3}-*.md`, `Listas/pratica-class-01-potential-outcomes.md`,
  `Leituras/class-01-narrated.txt`, `Videos/class-01-potential-outcomes/`,
  `NotebookLM/audio/aula-01-audio-part{1,2}.md`.

## Conventions

As L01/L02: front matter (`tags`, `date: 2026-10-25`, `status: taught`, `source`), title
`# <ids> · <what it settles>`, **Claim** block, `Prev · Next · Map`, **Notation** list, sections
`## k · U|C|G — title`, numbered equations cited by number, substitutions shown in place, worked
examples with the arithmetic in view, figure + italic caption + reading paragraph, companion
callouts, `## Links` with practice by number and printed page (no statements).

## Notes

| # | File | Covers | Settles | Figure |
|---|---|---|---|---|
| 00 | `L05-00-map.md` | — | front door | — |
| 01 | `L05-01-simpson-dags.md` | slides pp. 5–14 (§2–7) | Simpson's paradox as a weighted average (drug 78% vs 83% pooled, 93/87 and 73/69 by stratum); same numbers, opposite answers (gender = fork, BP = chain); chains, forks, colliders (Rules 1–3); paths and junctions on Harrison's DAG; d-separation and the slide's two examples checked; the marketing confounder; simulating from a DAG | `L05-simpson-weights`, `L05-collider-bias` |
| 02 | `L05-02-potential-outcomes-identification.md` | slides pp. 14–17 (§8); MHE Ch. 2 pp. 10–18, §3.2.1 pp. 38–44 | $Y(a)$, ATE/ATT/QTE/CATE/causal RR; SUTVA, consistency, ignorability, positivity; randomisation identifies; the adjustment formula; propensity-score IPW proposition **proved**; drug data: adjusted ATE +5.37 points vs naive −4.86; link to the notebook and the 3 companions for the selection-bias decomposition | — (existing companions) |
| 03 | `L05-03-omitted-variables-bad-control.md` | `omitted-variable.html`; MHE §3.2.2–3.2.3 pp. 44–50 | trivariate-Gaussian conditional mean derived; short = long + γ·(regression of omitted on included); site simulation β = 0.75, γ = 1.2 made exact: mean $\beta+\gamma\rho$, sd formulas; Table 3.2.1 read through OVB; bad control (3.2.12) and proxy control (3.2.15) | `L05-ovb-sampling` |
| 04 | `L05-04-errors-in-variables.md` | `error-in-variables.pdf`; W §9.4 pp. 287–292; MHE p. 84; W §15.4 pp. 479–481 | $\operatorname{plim}\hat\beta=\beta\sigma_x^2/(\sigma_x^2+\sigma_u^2)$; error in $y$ harmless; CEV vs Cov$(x_1,e_1)=0$; with controls (9.36); IV with a second measurement removes it | `L05-attenuation` |
| 05 | `L05-05-instrumental-variables.md` | slides pp. 17–20 (§9); MHE §4.1 pp. 84–96; W §15.1–15.3, 15.5 pp. 462–484; G §11.2 pp. 173–174; `example1-iv-card.html` | IV DAG; two-equation Gaussian system, reduced form, $\beta_1=\theta_1/\delta_1=$Cov$(z,y)/$Cov$(z,x)$; why adding $z$ to the outcome regression fails (slide §9.2 = G p. 173); Wald estimator (0.0891); 2SLS; IV variance (15.12) and weak instruments (15.19, F > 10); Card: OLS 0.0747 vs IV 0.1315, first stage 0.320 (t 3.64, F 13.26); LATE named (G) | `L05-iv-plims` |
| 06 | `L05-06-difference-in-differences.md` | slides pp. 21–25 (§10); MHE §5.2 pp. 169–176; W §13.2 pp. 407–411; `example2-DiD-card-krueger.html` | back-door paths through Time and ITG; common trends (5.2.1); four-cell table and regression (5.2.3) ↔ W Table 13.3; site numbers 23.380 / 20.431 / 21.097 / 20.898, DiD 2.750 (SE 1.731); MHE Table 5.2.1 2.76; Bayesian version named | `L05-did-card-krueger` |
| 07 | `L05-07-regression-discontinuity.md` | slides pp. 26–38 (§11); MHE §6.1 pp. 189–195, §6.2 pp. 196–198 (G); `example3-RDD-age-mva-internal.html` | sharp RD (6.1.1), continuity of $E[y_0\mid x]$, (6.1.7); linear, quadratic-with-interactions fits on MLDA (jumps in σ units as the site prints); nonlinearity mistaken for a jump; local linear and the bandwidth trade-off; fuzzy RD = IV (G) | `L05-rdd-mlda` |
| 08 | `L05-08-formulas.md` | all | exam spec mapped; every result; every number | — |
| 09 | `L05-09-pitfalls.md` | all | confusions + original 25-item V/F | — |
| 10 | `L05-10-python.md` + `L05_python_checks.py` | all | d-separation by brute force on the slide DAGs; adjustment/IPW; OVB exact vs MC; attenuation; IV/Wald/2SLS on card.csv vs linearmodels; DiD four ways; RDD fits and local linear — asserts vs the sources' numbers | — |

Figures (7): one script `figures/make_figures.py` importing `Notas/_figstyle.py`, asserts per figure.

## Companions (new; must cover what the 3 existing potential-outcome pages do not)

### L05-a `companions/companion-iv-plims.html` — "The Instrument Dial"
Model (slides p. 18, W (15.9), (15.19)): $x=\delta_1z+\varepsilon^x$, $y=\beta_1x+\varphi z+\varepsilon^y$,
Var$(z)=\sigma_z^2$, Var$(\varepsilon^x)=\sigma_x^2$, Var$(\varepsilon^y)=\sigma_y^2$, Corr$(\varepsilon^x,\varepsilon^y)=\rho$,
$z\perp(\varepsilon^x,\varepsilon^y)$. Exact plims: OLS $\beta_1+(\rho\sigma_x\sigma_y+\varphi\delta_1\sigma_z^2)/(\delta_1^2\sigma_z^2+\sigma_x^2)$;
IV $\beta_1+\varphi/\delta_1$; $y$ on $(x,z)$: coefficient on $x$ $=\beta_1+\rho\sigma_y/\sigma_x$. Asymptotic SEs
(homoskedastic, W (15.12)); first-stage $F\approx n\,R^2_{xz}/(1-R^2_{xz})$. Fixed calibration ($\sigma_z,\sigma_x,\sigma_y$) and
defaults from **card.csv sample moments without controls** (so defaults reproduce the simple OLS and the
simple Wald estimate on the Card data), stated on the page.

| Control | Symbol | What it is | Range | Step | Default | Unit | Source | What visibly moves |
|---|---|---|---|---|---|---|---|---|
| True effect | $\beta_1$ | causal return to a year of schooling | −0.10 – 0.40 | 0.001 | Card simple Wald | log points / year | card.csv | every plim line level |
| First stage | $\delta_1$ | effect of the instrument on $x$ | −1.5 – 1.5 | 0.001 | Card first stage | years | card.csv | IV bias $\varphi/\delta_1$, F, IV SE |
| Endogeneity | $\rho$ | Corr$(\varepsilon^x,\varepsilon^y)$ | −0.9 – 0.9 | 0.001 | Card implied | — | card.csv | OLS and long-regression bias |
| Exclusion violation | $\varphi$ | direct effect of $z$ on $y$ | −0.10 – 0.10 | 0.001 | 0 | log points | W (15.19) | IV bias |
| Sample size | $n$ | observations | 100 – 20000 | 10 | 3010 | — | card.csv | SE bands, F |

Panels: (1) plims vs $\rho$ (OLS, IV, $y$ on $(x,z)$) with ±1.96 SE bands at $n$; (2) |bias| of IV and OLS vs $\delta_1$
with the $F=10$ boundary. Answer read-out: **IV vs OLS bias**. Landmarks: $\rho=0$ (OLS = IV), $\varphi=0$, $\delta_1=0$ (no
instrument; IV undefined, shown as such), $F=10$.

### L05-b `companions/companion-rdd-window.html` — "The Discontinuity Window"
Model (slides pp. 29–36, MHE (6.1.2), (6.1.6)): local polynomial fit on the 48 MLDA cells within
$[a_0-b,a_0+b]$, $y_a=\alpha+\rho D_a+\sum_{k\le p}\gamma_k(a-a_0)^k+\sum_{k\le p}\delta_k(a-a_0)^kD_a$ (interactions on/off),
$D_a=1(a>a_0)$ (site convention). $\hat\rho$, classical SE, $t$, jump/$\hat\sigma$ (the site's "stdevs").

| Control | Symbol | What it is | Range | Step | Default | Unit | Source | What visibly moves |
|---|---|---|---|---|---|---|---|---|
| Outcome | — | MVA or internal-cause deaths | 2 options | — | MVA | per 100,000 | data | points, fits |
| Bandwidth | $b$ | half-width of the window | 0.30 – 2.00 | 0.01 | 2.00 (all data) | years | slide p. 36 | fit, $\hat\rho$, band panel marker |
| Polynomial order | $p$ | trend order each side | 1 – 2 | 1 | 1 | — | slides pp. 31–33 | fit curvature, $\hat\rho$ |
| Interactions | — | separate slopes each side | on/off | — | off | — | MHE (6.1.6) | fit, $\hat\rho$ |
| Cutoff | $a_0$ | where $D$ switches (placebo when ≠ 21) | 19.8 – 22.2 | 0.01 | 21.00 | years | slide p. 28 | fit, $\hat\rho$ |

Panels: (1) data with fitted pieces and the window shaded; (2) $\hat\rho\pm1.96$SE vs $b$. Answer: **$\hat\rho$ with SE**.
Landmarks: $a_0=21$; $b=2$ with $p=1$, no interactions = the site's linear fit; $p=2$ with interactions = the site's
quadratic fit.

Check: `companions/check_companions.py` (node stub-DOM harness copied from L02) at three control
vectors per page (both ends + default), sweeps, reset, no NaN.

## Verification

`python Notas/L05/figures/make_figures.py`; `python Notas/L05/L05_python_checks.py`;
`python Notas/L05/companions/check_companions.py`; `python tools/check_note_links.py Notas/L05`;
`python -I ~/.claude/commands/templates/notes_pdf.py Notas/L05` (no `Missing character`;
`pdffonts` no Type 3).
