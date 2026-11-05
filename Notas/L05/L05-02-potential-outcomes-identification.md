---
tags: [notes, lecture-05, causal-inference, potential-outcomes, ate, att, qte, cate, sutva, ignorability, propensity-score]
date: 2026-10-25
status: taught
source: "notes-on-causal-inference.pdf pp. 14–17: §7.2 (Daniels, Linero & Roy 2024, §1.1: ACEIs vs ARBs), §8 potential outcomes, ATE, ATT, QTE, causal relative risk, CATE; §8.1 SUTVA, consistency, randomisation, ignorability, positivity, identifiability; §8.2 propensity score and the IPW proposition. MHE Ch. 2 pp. 10–18 (eq. 2.1.1 p. 11, selection-bias decomposition p. 11, random assignment p. 12; NHIS table p. 10); MHE §3.2.1 pp. 38–43 (CIA, eqs. 3.2.1–3.2.2 p. 40). Drug counts from slide p. 6."
---

# Slides §8 · Potential outcomes: what a causal effect is, and the four assumptions that let data estimate it

> **Claim.** Each unit has two potential outcomes, $Y(1)$ and $Y(0)$, and we see one. Causal estimands are
> contrasts of their distributions — **ATE, ATT, CATE, QTE, causal risk ratio**. A naive treated-vs-untreated
> comparison equals the **ATT plus selection bias** (MHE p. 11). **Randomisation** kills the bias; without it,
> **SUTVA + consistency + ignorability given $L$ + positivity** identify the ATE through the **adjustment
> formula**, equivalently through **inverse propensity weighting**, whose identity is proved here line by line.
> On the slides' drug table, adjusting for gender turns a naive $-4.57$-point gap into an ATE of $+5.37$ points
> (ATT $+4.80$).
> Prev: [[L05-01-simpson-dags]] · Next: [[L05-03-omitted-variables-bad-control]] · Map: [[L05-00-map]]

**Notation.** The slides use $A$ (treatment) and $Y(a)$; MHE uses $d_i$ and $y_{1i},y_{0i}$. Both appear below; they name the same objects.

- $A_i\in\{0,1\}$ (= $d_i$): treatment received; $Y_i$ (= $y_i$): observed outcome; $i=1,\dots,N$.
- $Y_i(a)$ (= $y_{ai}$): potential outcome of unit $i$ under treatment $a$; $Y_i(1)-Y_i(0)$: individual causal effect.
- $L$ (MHE: $X_i$): observed pre-treatment covariates (confounders); $V$: covariates defining a subpopulation for the CATE.
- $F_a(y)=P(Y(a)\le y)$: cdf of the potential outcome; $F_a^{-1}(p)$ its $p$-quantile, $0<p<1$.
- $e(l)=P(A=1\mid L=l)$: propensity score, $0<e(l)<1$ under positivity.

---

## 1 · U — the question the slides start from (p. 14)

Daniels, Linero and Roy (2024, §1.1, reproduced on slide p. 14) compare two classes of
antihypertensives: $A=1$ if a patient is prescribed an ACE inhibitor, $A=0$ if an angiotensin-receptor
blocker; the outcome is systolic blood pressure (SBP). Prescription is not random: doctors choose by the
patient's condition. The slides' motto (p. 15): **"Causal inference requires assumptions that cannot be
checked from the data."**

---

## 2 · C — potential outcomes and the estimands (slide p. 15)

**Observed outcome** (MHE eq. 2.1.1, p. 11):

$$Y_i=Y_i(0)+\big(Y_i(1)-Y_i(0)\big)A_i=\begin{cases}Y_i(1)&A_i=1\\Y_i(0)&A_i=0.\end{cases}\tag{1}$$

**Estimands** (slide p. 15, the slides' definitions and readings):

| Estimand | Definition | Reading on the slide |
|---|---|---|
| ATE | $E\{Y(1)\}-E\{Y(0)\}$ (2) | "how much higher would the average SBP be in the population if everyone had been treated with ACEIs compared to if everyone had been treated with ARBs?" |
| ATT | $E\{Y(1)\mid A=1\}-E\{Y(0)\mid A=1\}$ (3) | contrast within the treated; $Y(0)$ for them is "the counterfactual outcome" |
| QTE | $F_1^{-1}(p)-F_0^{-1}(p)$ (4) | "particularly useful when the outcome of interest is skewed, or when the treatment only has a large effect for a small subset" |
| Causal relative risk | $E\{Y(1)\}/E\{Y(0)\}$ (5), binary $Y$ | "how many times more likely would high BP[S] be if everyone was treated with ACEIs rather than ARBs?" |
| CATE | $E\{Y(1)-Y(0)\mid V=v\}$ (6) | the ATE in the subpopulation $V=v$ |

Note that the QTE (4) is a difference of **quantiles**, not the quantile of the individual differences
$Y(1)-Y(0)$: the joint distribution of $(Y(0),Y(1))$ is never observed, but each margin can be.

> **The fundamental problem.** $Y_i(1)$ and $Y_i(0)$ are never both observed, so no estimand above is a
> function of the data until assumptions link it to $(Y_i,A_i,L_i)$ (slide p. 16: "To link observed data (no
> potential outcomes!) to potential outcomes, we need causal assumptions").

---

## 3 · C — the naive comparison: ATT plus selection bias (MHE p. 11)

**Start from the observed difference** and use (1): within $A=1$, $Y=Y(1)$; within $A=0$, $Y=Y(0)$:

$$E[Y\mid A=1]-E[Y\mid A=0]=E[Y(1)\mid A=1]-E[Y(0)\mid A=0].$$

**Add and subtract** $E[Y(0)\mid A=1]$, the treated's unobserved untreated mean:

$$E[Y\mid A=1]-E[Y\mid A=0]=\underbrace{E[Y(1)\mid A=1]-E[Y(0)\mid A=1]}_{\text{ATT (3)}}+\underbrace{E[Y(0)\mid A=1]-E[Y(0)\mid A=0]}_{\text{selection bias}}.\tag{7}$$

**MHE's example** (p. 10, 2005 NHIS; health 1 = excellent … 5 = poor): hospitalised mean 2.79 ($n=7774$),
not hospitalised 2.07 ($n=90049$), "the difference in the means is 0.71" with $t=58.9$ — hospitals seem
to make people sicker. In (7) the selection term is large: the sick go to hospital, so $E[y_{0i}\mid d_i=1]$ is
worse than $E[y_{0i}\mid d_i=0]$, and it "may be so large … that it completely masks a positive treatment
effect" (p. 12).

> **Interactive companions (existing).** The decomposition (7) is what the three Class 5+6 pages already
> do: [Selection Bias Decomposer](../../Aula/class-05-06/companion-selection-bias.html) (choose who is treated
> and how effects vary; watch the gap split into effect + bias),
> [Bigger Sample, Same Bias](../../Aula/class-05-06/companion-sample-size.html) (500 studies: intervals shrink
> onto the truth only under random assignment), and
> [The Eight-Person Table](../../Aula/class-05-06/companion-eight-person-table.html) (both potential outcomes
> visible, every random assignment enumerated). The worked notebook is
> [[../../Aula/class-05-06/potential-outcomes.ipynb|potential-outcomes.ipynb]] (MHE Ch. 2, STAR, regression on a
> randomised dummy).

---

## 4 · C — the identifying assumptions (slide p. 16)

**SUTVA.** For assignments $\mathbf a=(a_1,\dots,a_N)$ and $\mathbf a'=(a'_1,\dots,a'_N)$ with $a_i=a'_i$:

$$Y_i(\mathbf a)=Y_i(\mathbf a'),\tag{8}$$

"the potential outcome of any subject $i$ does not depend on the treatment received by the other subjects"
(no interference; one version of each treatment). (The slide's §8 heading writes "STUVA".)

**Consistency.** $Y_i=Y_i(a)$ if $A_i=a$ — the observed outcome is the potential outcome of the treatment
actually received. This is what licenses (1).

**Randomisation.** If $A$ is randomised, $\{Y(0),Y(1)\}\perp A$, hence for $a=0,1$:

$$E\{Y_i(a)\}=E\{Y_i(a)\mid A_i=a\}=E(Y_i\mid A_i=a).\tag{9}$$

The first equality is independence, the second consistency. In (7) the selection term vanishes because
$E[Y(0)\mid A=1]=E[Y(0)]=E[Y(0)\mid A=0]$, and the ATT equals the ATE (MHE p. 12).

**Ignorability** (no unmeasured confounders, unconfoundedness, exchangeability; MHE's CIA, eq. 3.2.2, p. 40):

$$\{Y(0),Y(1)\}\perp A\mid L .\tag{10}$$

"$L$ is a set of observed covariates that influence both $Y$ and $A$ (remember when we defined a fork?)".
And the slides' warning: "The validity of ignorability cannot be assessed from the observed data, regardless
of how large the sample size is" (p. 16).

**Positivity.**

$$P(A=a\mid L=l)>0\quad\text{for all }a\text{ and }l.\tag{11}$$

Every covariate cell must contain both treated and untreated units; otherwise one of the conditional means
below is undefined.

---

## 5 · C — identification: the adjustment formula

**Iterate expectations over $L$:**

$$E\{Y(a)\}=E_L\big[E\{Y(a)\mid L\}\big].$$

**Ignorability (10)** lets us condition on $A=a$ inside, since $Y(a)\perp A\mid L$; positivity (11) makes the
conditioning event non-empty:

$$E\{Y(a)\}=E_L\big[E\{Y(a)\mid A=a,L\}\big].$$

**Consistency** replaces $Y(a)$ by $Y$ on the event $A=a$:

$$E\{Y(a)\}=E_L\big[E(Y\mid A=a,L)\big]=\sum_lP(L=l)\,E(Y\mid A=a,L=l).\tag{12}$$

**ATE** is (12) at $a=1$ minus (12) at $a=0$. This is MHE's "averaging all of the X-specific effects"
(eq. 3.2.3, p. 42), and it is exactly the standardisation of [[L05-01-simpson-dags]] §2.

### 5.1 · Worked example: the slides' drug table, gender as $L$

Gender is the fork of slide p. 6 ($D\leftarrow G\to R$), so take $L=G$. $P(G=0)=357/700=0.51$, $P(G=1)=343/700=0.49$.

| $L$ | $E(Y\mid A=1,L)$ | $E(Y\mid A=0,L)$ | difference | $P(L)$ |
|---|---|---|---|---|
| men | $81/87=0.93103$ | $234/270=0.86667$ | $0.06437$ | $0.51$ |
| women | $192/263=0.73004$ | $55/80=0.68750$ | $0.04254$ | $0.49$ |

**ATE by (12):**

$$\text{ATE}=(0.51)(0.06437)+(0.49)(0.04254)=0.03283+0.02084=0.05367 .$$

**ATT:** the same differences weighted by the **treated's** gender mix, $P(G=0\mid A=1)=87/350=0.24857$,
$P(G=1\mid A=1)=263/350=0.75143$:

$$\text{ATT}=(0.24857)(0.06437)+(0.75143)(0.04254)=0.01600+0.03196=0.04796 .$$

**Naive:** $273/350-289/350=0.78000-0.82571=-0.04571$. By (7), the selection bias against the ATT is
$-0.04571-0.04796=-0.09367$: drug takers are mostly women, whose untreated recovery is low.

> **Same data, three numbers.** Naive $-4.57$ points, ATE $+5.37$, ATT $+4.80$. Only the first is free of
> assumptions; the other two are correct **if** gender is the only confounder (ignorability) and both
> genders contain takers and non-takers (positivity: $e$ below is 0.24 and 0.77, safely inside $(0,1)$).

---

## 6 · C — the propensity score and inverse weighting (slides pp. 16–17)

**Definition.** $e(l)=P(A=1\mid L=l)$.

**Proposition** (slide p. 16). Under SUTVA, consistency, ignorability and positivity with binary $A$,

$$\text{ATE}=E\left[\frac{AY}{e(L)}-\frac{(1-A)Y}{1-e(L)}\right]=E\left[Y\,\frac{A-e(L)}{e(L)\{1-e(L)\}}\right].\tag{13}$$

**Proof of the first term.** By consistency $AY=AY(1)$ (when $A=1$, $Y=Y(1)$; when $A=0$ both sides are 0):

$$E\left[\frac{AY}{e(L)}\right]=E\left[\frac{AY(1)}{e(L)}\right].$$

Iterate on $L$:

$$E\left[\frac{AY(1)}{e(L)}\right]=E_L\left[\frac{E\{AY(1)\mid L\}}{e(L)}\right].$$

By ignorability (10), $A\perp Y(1)\mid L$, so the inner expectation factors:

$$E\{AY(1)\mid L\}=E(A\mid L)\,E\{Y(1)\mid L\}=e(L)\,E\{Y(1)\mid L\}.$$

Substitute; positivity (11) makes $e(L)>0$ so it cancels:

$$E\left[\frac{AY}{e(L)}\right]=E_L\left[\frac{e(L)\,E\{Y(1)\mid L\}}{e(L)}\right]=E_L\big[E\{Y(1)\mid L\}\big]=E\{Y(1)\}.$$

**Second term**, identically with $1-A$ and $1-e(L)$: $E[(1-A)Y/(1-e(L))]=E\{Y(0)\}$. Subtracting gives the first form of (13).

**Second form.** Put the two fractions over $e(1-e)$:

$$\frac{A}{e}-\frac{1-A}{1-e}=\frac{A(1-e)-(1-A)e}{e(1-e)}=\frac{A-Ae-e+Ae}{e(1-e)}=\frac{A-e}{e(1-e)} .\qquad\blacksquare$$

**Plug-in estimator** (slide p. 17): $\widehat{\text{ATE}}=\frac1n\sum_{i=1}^nY_i\frac{A_i-\hat e(L_i)}{\hat e(L_i)\{1-\hat e(L_i)\}}$, consistent "if we can estimate the propensity score sufficiently well".

### 6.1 · Worked example: IPW on the drug table

With $L=G$ the propensity is a cell frequency: $\hat e(\text{men})=87/357=0.24370$, $\hat e(\text{women})=263/343=0.76676$.
Each treated man counts $1/0.24370=4.103$ times, each untreated man $1/(1-0.24370)=1.322$ times, and so on.
Evaluating (13) on the 700 rebuilt observations gives **0.05367**, identical to the adjustment formula
([[L05-10-python]] §2). This is not a coincidence: with a saturated (cell-frequency) propensity, IPW **is**
standardisation — weighting each cell by $1/\hat e$ re-creates the population mix $P(L=l)$ in each arm.

> **The propensity score is a balancing score** (slide p. 17): "a useful one-dimensional summary of $L$".
> With many covariates, (12) needs a mean for every cell of $L$; (13) needs only one number per unit.

---

## 7 · C — regression as an adjustment device (MHE §3.2.1, pp. 38–44)

MHE writes the CIA (10) for schooling, $\{y_{0i},y_{1i}\}\perp c_i\mid X_i$ (eq. 3.2.2), and the constant-effect
linear causal model $f_i(s)=\alpha+\rho s+\eta_i$ (3.2.7). If $\eta_i=X_i'\gamma+v_i$ with $E[\eta_i\mid X_i]=X_i'\gamma$, then

$$y_i=\alpha+\rho s_i+X_i'\gamma+v_i\qquad\text{(MHE 3.2.9, p. 44)},\tag{14}$$

and "the key assumption here is that the observable characteristics, $X_i$, are the only reason why $\eta_i$ and
$s_i$ … are correlated" — selection on observables. Note 03 asks what happens to $\rho$ when part of $X_i$ is
missing from (14).

---

## 8 · G — beyond the slides

Matching, doubly robust estimators and the efficiency theory of (13) are not on the slides. The
Heckman–Lopes–Piatek (2014) Bayesian treatment-effects paper is listed on slide p. 20 (named only), and
Greenberg §11.1 (pp. 168–173) treats binary treatment with an instrument in a Bayesian latent-index model:
**Classes 3+4 tools**, named only.

---

## Links

- Neighbours: [[L05-01-simpson-dags]] (forks = confounders; the same 5.37 by standardisation) · [[L05-03-omitted-variables-bad-control]] (next: what (14) loses when a confounder is omitted).
- Unit: [[L05-05-instrumental-variables]] (when (10) fails for every observable $L$) · [[L05-06-difference-in-differences]] (DiD's parallel trends are an ignorability statement about changes) · [[L05-07-regression-discontinuity]] (positivity fails by design: no overlap at the cutoff) · [[L05-08-formulas]] · [[L05-09-pitfalls]] · [[L05-10-python]] §2.
- Existing material for this note (draft-plan potential-outcomes set, kept and linked): [[../../Aula/class-05-06/potential-outcomes.ipynb|notebook]] · quizzes [[../../Simulados/quiz-class01-1-potential-outcomes-2026-10-10|quiz 1]], [[../../Simulados/quiz-class01-2-random-assignment-2026-10-10|quiz 2]], [[../../Simulados/quiz-class01-3-experiments-regression-2026-10-10|quiz 3]] · practice plan [[../../Listas/pratica-class-01-potential-outcomes|pratica-class-01]] · narration [[../../Leituras/class-01-narrated.txt|class-01-narrated.txt]] · video `Videos/class-01-potential-outcomes/` · audio prompts [[../../NotebookLM/audio/aula-01-audio-part1|part 1]], [[../../NotebookLM/audio/aula-01-audio-part2|part 2]].
- Rules pack: [[../../rules/02_causalidade_potential_outcomes|rules/02]].
- **Practice** (worked examples in the book, not exercises): MHE Table 2.2.1 (p. 14) and Table 2.2.2 (p. 15), Tennessee STAR balance and experimental estimates; G 11.1–11.2 (p. 180), 11.3–11.4 (p. 181) for the Bayesian treatment model of G §11.1.
