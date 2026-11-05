---
tags: [notes, lecture-05, causal-inference, formulas, exam-spec]
date: 2026-10-25
status: taught
source: "Notes L05-01 … L05-07; goals of the Classes 5+6 block of Map/class-plan.md; slides notes-on-causal-inference.pdf and error-in-variables.pdf; MHE, W, G pages as cited in each note."
---

# Classes 5+6 · Formula sheet: every definition, result and number of the unit

> **What this sheet is.** §0 maps the class's stated goals to the notes that derive them; §1 lists every definition and
> result with its source numbering and the note where it is proved; §2 lists every number worked in the unit. No
> derivations here — follow the links.
> Prev: [[L05-07-regression-discontinuity]] · Next: [[L05-09-pitfalls]] · Map: [[L05-00-map]]

---

## 0 · The exam specification, item by item

Goals of the Classes 5+6 block ([[../../Map/class-plan|Map/class-plan]]), and the final-exam line "derivations
(… bias formulas) and interpretation of output from the site's examples" (no coding):

| Goal | Where | What to be able to do |
|---|---|---|
| Simpson's paradox | [[L05-01-simpson-dags]] §1–2 | write the pooled rate as a weighted average; decompose the gap; say which table answers the causal question from the graph |
| DAGs: paths, chains, forks, colliders, d-separation | [[L05-01-simpson-dags]] §3–6 | classify junctions; list paths; decide $X\perp Y\mid S$ by the blocking rule; pick an adjustment set |
| Potential outcomes, SUTVA, ATE, CATE, QTE | [[L05-02-potential-outcomes-identification]] §2, §4 | define each estimand; state each assumption and what it buys |
| Selection bias | [[L05-02-potential-outcomes-identification]] §3; existing notebook and companions | derive naive = ATT + selection bias; show randomisation removes it |
| Identification, propensity score | [[L05-02-potential-outcomes-identification]] §5–6 | derive the adjustment formula; prove the IPW identity |
| Omitted-variable bias | [[L05-03-omitted-variables-bad-control]] §1–4 | derive short = long + γδ; sign the bias; read Table 3.2.1 |
| Bad control | [[L05-03-omitted-variables-bad-control]] §5 | derive (3.2.12)'s selection term; the proxy-control coefficient |
| Errors-in-variables (attenuation) | [[L05-04-errors-in-variables]] | derive $\beta\sigma_x^2/(\sigma_x^2+\sigma_u^2)$; CEV vs (9.29); effect of controls; IV fix |
| IV (Card) | [[L05-05-instrumental-variables]] | reduced form, $\beta_1=\theta_1/\delta_1$; why $y$ on $(x,z)$ fails; Wald; 2SLS; IV variance; weak instruments; read the Card printout |
| DiD (Card–Krueger) | [[L05-06-difference-in-differences]] | common trends ⇒ DD $=\delta$; regression ↔ cell means; read the printout; what a trend violation does |
| Sharp RDD (MLDA) | [[L05-07-regression-discontinuity]] | sharp design; continuity ⇒ jump = effect at cutoff; linear/quadratic/local linear; read the fits; placebo checks |

---

## 1 · Definitions and results

### Simpson and DAGs ([[L05-01-simpson-dags]])

| # | Statement | Source |
|---|---|---|
| (1) | $\bar r_d=(1-\pi_d)r_{d0}+\pi_dr_{d1}$ | law of total probability; slide p. 6 data |
| (2) | $\bar r_1-\bar r_0=[(1-\pi_0)(r_{10}-r_{00})+\pi_0(r_{11}-r_{01})]+(\pi_1-\pi_0)(r_{11}-r_{10})$ | add and subtract |
| Rule 1 | chain $X\to Y\to Z$: $X\perp Z\mid Y$ | slide p. 8 |
| Rule 2 | fork $Y\leftarrow X\to Z$: $Y\perp Z\mid X$ | slide p. 8 |
| Rule 3 | collider $X\to Z\leftarrow Y$: $X\perp Y$, but dependent given $Z$ or any descendant of $Z$ | slide p. 9 |
| (4) | $\operatorname{Corr}(X,Z\mid W)=-ab/\sqrt{(a^2+s^2)(b^2+s^2)}$ for $W=aX+bZ+e$ | Gaussian conditioning |
| d-sep. | path blocked by $Z$ iff a chain/fork middle is in $Z$, or a collider with neither it nor a descendant in $Z$; all paths blocked ⇒ independence given $Z$ | slide p. 11 |

### Potential outcomes ([[L05-02-potential-outcomes-identification]])

| # | Statement | Source |
|---|---|---|
| (1) | $Y_i=Y_i(0)+(Y_i(1)-Y_i(0))A_i$ | MHE 2.1.1, p. 11 |
| (2)–(6) | ATE $E\{Y(1)\}-E\{Y(0)\}$; ATT $E\{Y(1)-Y(0)\mid A=1\}$; QTE $F_1^{-1}(p)-F_0^{-1}(p)$; RR $E\{Y(1)\}/E\{Y(0)\}$; CATE $E\{Y(1)-Y(0)\mid V=v\}$ | slide p. 15 |
| (7) | $E[Y\mid A=1]-E[Y\mid A=0]=\text{ATT}+\{E[Y(0)\mid A=1]-E[Y(0)\mid A=0]\}$ | MHE p. 11 |
| (8) | SUTVA: $Y_i(\mathbf a)=Y_i(\mathbf a')$ if $a_i=a'_i$ | slide p. 16 |
| (9) | randomisation: $E\{Y(a)\}=E(Y\mid A=a)$ | slide p. 16; MHE p. 12 |
| (10) | ignorability $\{Y(0),Y(1)\}\perp A\mid L$ (MHE CIA 3.2.2) | slide p. 16; MHE p. 40 |
| (11) | positivity $P(A=a\mid L=l)>0$ | slide p. 16 |
| (12) | $E\{Y(a)\}=\sum_lP(L=l)E(Y\mid A=a,L=l)$ | derived |
| (13) | ATE $=E[AY/e(L)-(1-A)Y/(1-e(L))]=E[Y(A-e(L))/\{e(L)(1-e(L))\}]$ | slide pp. 16–17 (proved) |
| (14) | $y_i=\alpha+\rho s_i+X_i'\gamma+v_i$ | MHE 3.2.9, p. 44 |

### Omitted variables, bad control ([[L05-03-omitted-variables-bad-control]])

| # | Statement | Source |
|---|---|---|
| (3) | $\beta=(\sigma_{xy}-\rho\sigma_{yz})/(1-\rho^2)$, $\gamma=(\sigma_{yz}-\rho\sigma_{xy})/(1-\rho^2)$ | omitted-variable.html |
| (4) | $\tau^2=(1-\rho^2-\sigma_{xy}^2-\sigma_{yz}^2+2\sigma_{xy}\sigma_{yz}\rho)/(1-\rho^2)$ | idem (page's "$1-\rho$" corrected) |
| (5)/(6) | short $=\beta+\gamma\rho$; generally $\operatorname{Cov}(y,s)/V(s)=\rho+\gamma'\delta_{As}$ | MHE 3.2.11, p. 45 |
| (8)/(9) | site simulation: $E\hat\beta^s=0.75+1.2\rho$, sd $\sqrt{(1+1.44(1-\rho^2))/28}$; long sd $\sqrt{1/(27(1-\rho^2))}$ | derived |
| (11) | bad control: conditional comparison $=E[y_1-y_0\mid w_1=1]+\{E[y_0\mid w_1=1]-E[y_0\mid w_0=1]\}$ | MHE 3.2.12, p. 49 |
| (12) | proxy control: coefficient $\rho-\gamma\pi_1/\pi_2$ | MHE 3.2.15, p. 50 |

### Errors in variables ([[L05-04-errors-in-variables]])

| # | Statement | Source |
|---|---|---|
| (4) | $\operatorname{plim}\hat\beta_{\text{naive}}=\beta\sigma_x^2/(\sigma_x^2+\sigma_u^2)$ | error-in-variables.pdf; W 9.33, p. 291 |
| (5) | $y=\beta_0+\beta_1x_1+(u-\beta_1e_1)$; CEV ⇒ $\operatorname{Cov}(x_1,e_1)=\sigma_{e_1}^2$ | W 9.30–9.32 |
| (7)/(8) | with controls: $\beta_1\sigma_{r}^2/(\sigma_r^2+\sigma_{e_1}^2)$, $\sigma_r^2=(1-R^2)\sigma_x^2$ | W 9.36, p. 291 |
| (9) | second measurement as IV: $\operatorname{Cov}(w_2,y)/\operatorname{Cov}(w_2,w_1)=\beta$ | W §15.4 |

### Instrumental variables ([[L05-05-instrumental-variables]])

| # | Statement | Source |
|---|---|---|
| (3) | $\operatorname{plim}\hat\beta^{OLS}=\beta_1+\rho\sigma_x\sigma_y/(\delta_1^2\sigma_z^2+\sigma_x^2)$ | derived from slide p. 18 system |
| (4) | $\theta_0=\beta_0+\beta_1\delta_0$, $\theta_1=\beta_1\delta_1$, $\tau^2=\beta_1^2\sigma_x^2+\sigma_y^2+2\beta_1\rho\sigma_x\sigma_y$ | slide p. 18 |
| (5)/(6) | $\beta_1=\theta_1/\delta_1=\operatorname{Cov}(z,y)/\operatorname{Cov}(z,x)$ | slide p. 18; W 15.9; MHE 4.1.3 |
| (8) | $y$ on $(x,z)$: coefficient on $x$ $=\beta_1+\sigma_{xy}/\sigma_x^2$, on $z$ $=-\sigma_{xy}\delta_1/\sigma_x^2$ | slide p. 19; G p. 173 |
| (9) | Wald: $\beta_1=\dfrac{E[y\mid z=1]-E[y\mid z=0]}{E[s\mid z=1]-E[s\mid z=0]}$ | MHE 4.1.12, p. 94 |
| (10) | 2SLS: reduced-form $z$ coefficient $=\beta_1\pi_{11}$ | MHE 4.1.7 |
| (11) | $\operatorname{Avar}(\hat\beta^{IV})=\sigma^2/(n\sigma_x^2\rho_{xz}^2)$ | W 15.12, p. 466 |
| (12) | $\operatorname{plim}\hat\beta_{IV}=\beta_1+\frac{\operatorname{Corr}(z,u)}{\operatorname{Corr}(z,x)}\frac{\sigma_u}{\sigma_x}$; OLS: $\beta_1+\operatorname{Corr}(x,u)\frac{\sigma_u}{\sigma_x}$ | W 15.19–15.20, p. 469 |
| rule | first-stage $|t|>3.2$ / $F>10$ | W p. 478 |
| G | LATE theorem (A1–A4 ⇒ Wald = effect on compliers) | MHE Thm 4.4.1, p. 114 |

### DiD ([[L05-06-difference-in-differences]])

| # | Statement | Source |
|---|---|---|
| (1) | $E(y_{0ist}\mid s,t)=\gamma_s+\lambda_t$ | MHE 5.2.1, p. 170 |
| (2) | $y_{ist}=\gamma_s+\lambda_t+\delta d_{st}+\varepsilon_{ist}$ | MHE 5.2.2 |
| (5) | (NJ change) − (PA change) $=\delta$ | MHE p. 170 (order corrected) |
| (6) | $y_{ti}=\beta_0+\beta_1P_t+\beta_2T_i+\beta_3P_tT_i+x'\gamma+\varepsilon$ | slide p. 22; W 13.10; MHE 5.2.3 |
| (7) | $\hat\beta_3=(\bar y_{1,1}-\bar y_{1,0})-(\bar y_{0,1}-\bar y_{0,0})$ | W 13.11, Table 13.3 |

### RDD ([[L05-07-regression-discontinuity]])

| # | Statement | Source |
|---|---|---|
| (1) | $D_a=1(a\ge a_0)$ | slide p. 28; MHE 6.1.1 |
| (3) | $y_a=\alpha+\rho D_a+\gamma a+\varepsilon_a$ | slide p. 29; MHE 6.1.2 |
| (4) | $\lim_{\Delta\to0}\{E[y\mid a_0<a<a_0+\Delta]-E[y\mid a_0-\Delta<a<a_0]\}=E[y_1-y_0\mid a=a_0]$ | MHE 6.1.7, p. 193 |
| (5) | quadratic with interactions, centred at $a_0$ | slide p. 31; MHE 6.1.6 |
| G | fuzzy RD: jump in $y$ / jump in $P(d=1\mid x)$ | MHE 6.2.5, p. 198 |

---

## 2 · Every number in the unit

| Case | Numbers | Note |
|---|---|---|
| Drug table | 93/87% (men), 73/69% (women), 78/83% pooled; same-mix effect +5.94, composition −10.51, gap −4.57 points | 01 §2 |
| Standardised / adjusted | 0.833 vs 0.779 ⇒ ATE **+0.0537**; ATT **+0.0480**; selection bias −0.0937; $e$ = 0.2437 (men), 0.7668 (women) | 01 §2, 02 §5–6 |
| Collider, $a=b=s=1$ | $\operatorname{Corr}(X,Z\mid W)=-0.5$; given descendant with $t=1$: $-1/3$ | 01 §3.1 |
| Harrison DAG | 5 paths; 15 junctions = 7 chains, 3 forks, 5 colliders; $X\to Y$ effect 6: adjust $\{Z_1,Z_3\}$ or $\{Z_2,Z_3\}$ 6.0000, $\{Z_3\}$ 6.0051, none 5.4381 | 01 §4 |
| NHIS (MHE p. 10) | 2.79 vs 2.07, difference 0.71, $t=58.9$ | 02 §3 |
| OVB simulation | $E\hat\beta^s=0.75,1.35,1.89$ at $\rho=0,0.5,0.95$; long sd 0.1925, 0.2222, 0.6163 | 03 §3 |
| MHE Table 3.2.1 | 0.132, 0.131, 0.114, 0.087, 0.066 | 03 §4 |
| Proxy control example | $0.10-0.05(0.2)/1=0.09$ | 03 §5.1 |
| Attenuation | $\sigma_x=\sigma_u$: λ = 0.5; $\beta=1.5,\sigma_u=0.75$: λ = 0.64 → 0.96; with control λ_r = 0.390 | 04 |
| Wald, MHE Table 4.1.2 | $-0.01349/-0.1514=0.0891$ (0.0210) vs OLS 0.0703 | 05 §4 |
| Card, no controls | Wald 0.155907/0.829019 = 0.1881; OLS 0.0521 | 05 §4 |
| Card, site controls | OLS 0.0746933 (0.0034983); first stage 0.320 (0.088), $t$ 3.64, $F$ 13.256, $R^2$ 0.477; RF 0.04207; IV 0.1315038 (0.0549637); CI (0.024, 0.239); SE ratio 15.7; Wu–Hausman 1.168 ($p$ 0.28); selected IV 0.1365294 (0.0495914), $F$ 16.621 | 05 §7 |
| Card calibration (companion) | $\sigma_z=0.4026$, $\sigma_x=1.9354$, $\sigma_y=0.3873$, $\delta_1=0.3199$, $\rho=-0.2851$; $F=10$ at $\delta_1=0.276$ ($n=3010$) | 05 §6 |
| W Example 15.3 | packs on cigprice 0.0003, $R^2=0$; IV 2.99 (8.70) | 05 §6 |
| Card–Krueger (site) | PA 23.380 → 21.097 ($-2.283$); NJ 20.431 → 20.897 (+0.467); DiD **2.750** (SE 1.731, $t$ 1.59, $p$ 0.113); treatment −2.949 (1.224); residual SE 9.511; $R^2$ 0.0076; 95% CI (−0.64, 6.14); $P(\beta_4>0)$ 0.944 | 06 §4, §6 |
| MHE Table 5.2.1 | PA 23.33 → 21.17, NJ 20.44 → 21.03; DD 2.76 (1.36) | 06 §4 |
| MLDA (slide) | +100 deaths/day on 150; $\hat\rho=7.7$ (all deaths) | 07 §1, §3 |
| MLDA (site data) | MVA linear 4.534 (0.768), $\hat\sigma$ 1.3293, 3.411 sd, left/right limits 29.357/33.891; MVA quadratic 4.663 (1.155), 3.508 sd; internal 0.392 (0.596), 0.380 sd; internal quadratic 1.073, 1.026 sd | 07 §6 |
| Local linear MVA | $b=0.5$: 4.772 (1.291); $b=1$: 4.759 (1.123); $b=2$: 4.534 (0.751); placebo $a_0=20$: 0.828 (1.096), $a_0=22$: −0.103 (1.106) | 07 §7 |

## Links

- Unit: [[L05-00-map]] · [[L05-09-pitfalls]] · [[L05-10-python]] (every number above is asserted there).
- Rules packs: [[../../rules/01_endogeneidade_iv|rules/01]] · [[../../rules/02_causalidade_potential_outcomes|rules/02]] · [[../../rules/03_painel_did|rules/03]].
