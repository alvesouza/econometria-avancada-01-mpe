---
tags: [notes, lecture-05, causal-inference, simpson-paradox, dag, d-separation, confounding, collider]
date: 2026-10-25
status: taught
source: "notes-on-causal-inference.pdf (Lopes, Oct 2024) pp. 5–14: §2 Simpson's paradox (Examples 1–3, after Pearl, Glymour & Jewell ch. 1), §3 back to the examples with their DAGs, §4 chains/forks/colliders (Rules 1–3), §5 Harrison's DAG, paths, junctions, simulating from a DAG, §6 d-separation and its two examples, §7.1 the marketing-campaign example. DAGs are in no book on disk: the slides are the source."
---

# Slides §2–7 · Simpson's paradox, and the graph that decides which table to read

> **Claim.** The same four recovery rates favour the drug inside each stratum (93% vs 87%, 73% vs
> 69%) and oppose it in the pooled table (78% vs 83%), because a pooled rate is a **weighted average
> of the stratum rates with group-specific weights**. Arithmetic cannot say which table answers the
> causal question; the **causal graph** can. If the stratifying variable is a common cause (a **fork**,
> gender) read the stratified table; if it is a consequence of the treatment (a **chain**, blood pressure
> after treatment) read the pooled one. Three junctions and one blocking rule, **d-separation**, turn
> that judgement into a mechanical test of which variables to condition on, including the trap of
> conditioning on a **collider**.
> Prev: [[L05-00-map]] · Next: [[L05-02-potential-outcomes-identification]] · Map: [[L05-00-map]]

**Notation.**

- $D\in\{0,1\}$: drug taken; $R\in\{0,1\}$: recovered; $G$: gender ($G=1$ woman); $\pi$: share of women in a group.
- $r_{dg}=P(R=1\mid D=d,G=g)$: stratum recovery rate; $\bar r_d$: pooled rate of group $D=d$.
- $\pi_d=P(G=1\mid D=d)$: share of women among those with $D=d$; $\pi^\ast=P(G=1)$: share in all 700 patients.
- In a DAG, $A\to B$: $A$ is a direct cause of $B$. $A\perp B\mid S$: $A$ and $B$ independent given the set $S$.
- $X,Z,W,U,T,Y$: the generic nodes of the slides' examples; $a,b,s,t$: coefficients and noise sds of the Gaussian illustrations (§6).

---

## 1 · U — three paradoxes from one book (slides pp. 5–7)

The slides open with three examples quoted from Pearl, Glymour and Jewell, *Causal Inference in
Statistics*, ch. 1. The paradox, in the slides' words: "a statistical association that holds for an
entire population is re[v]ersed in every subpopulation" (p. 5).

**Example 1–2, the drug table** (700 patients, 350 chose the drug; p. 6):

| | Drug | No drug |
|---|---|---|
| Men (or: low BP) | 81 of 87 = **93%** | 234 of 270 = **87%** |
| Women (or: high BP) | 192 of 263 = **73%** | 55 of 80 = **69%** |
| Combined | 273 of 350 = **78%** | 289 of 350 = **83%** |

The drug wins in both rows and loses in the total. The slides then put **the same numbers** under
two stories:

- **Gender** (p. 6): estrogen lowers recovery whatever the treatment, and women are much more likely
  to take the drug. Gender causes both: $D\leftarrow G\rightarrow R$, plus $D\rightarrow R$.
- **Blood pressure measured after treatment** (p. 7): the drug works *by* lowering BP but is also toxic.
  BP is caused by the drug: $D\rightarrow BP\rightarrow R$, plus $D\rightarrow R$.

> **"Remarkably, though the numbers are the same in the gender and blood pressure examples, the correct
> result lies in the segregated data for the former and the aggregated data for the latter"** (slide p. 7).
> Nothing in the table distinguishes the two cases; only the arrow between the third variable and the
> drug does.

**Example 3** (p. 7): within each age group, more exercise goes with lower cholesterol; pooled over ages
the slope turns positive, because older people exercise more and have higher cholesterol regardless.
Age is "a common cause of both treatment (exercise) and outcome (cholesterol)": $\text{exer}\leftarrow\text{age}\rightarrow\text{chol}$.
(The slide says "if we don't segregate by gender" here; the variable is **age**.)

---

## 2 · C — why the reversal happens: a pooled rate is a mix

**Pooled rate as a weighted average.** By the law of total probability, for group $D=d$:

$$\bar r_d=P(R=1\mid D=d)=\sum_gP(G=g\mid D=d)\,r_{dg}=(1-\pi_d)\,r_{d0}+\pi_d\,r_{d1}.\tag{1}$$

**Plug in the drug group** ($\pi_1=263/350=0.75143$, $r_{10}=81/87=0.93103$, $r_{11}=192/263=0.73004$):

$$\bar r_1=(1-0.75143)(0.93103)+(0.75143)(0.73004)=0.23143+0.54857=0.78000 .$$

**Plug in the no-drug group** ($\pi_0=80/350=0.22857$, $r_{00}=234/270=0.86667$, $r_{01}=55/80=0.68750$):

$$\bar r_0=(1-0.22857)(0.86667)+(0.22857)(0.68750)=0.66857+0.15714=0.82571 .$$

**Decompose the pooled gap.** Add and subtract $(1-\pi_0)r_{10}+\pi_0r_{11}$, the drug's rate at the no-drug group's gender mix:

$$\bar r_1-\bar r_0=\underbrace{\big[(1-\pi_0)(r_{10}-r_{00})+\pi_0(r_{11}-r_{01})\big]}_{\text{drug vs no drug, same mix }\pi_0}+\underbrace{(\pi_1-\pi_0)(r_{11}-r_{10})}_{\text{composition}}.\tag{2}$$

Numbers in (2):

$$\text{same mix: }(0.77143)(0.93103-0.86667)+(0.22857)(0.73004-0.68750)=0.04965+0.00972=0.05938,$$

$$\text{composition: }(0.75143-0.22857)(0.73004-0.93103)=(0.52286)(-0.20099)=-0.10509,$$

$$\bar r_1-\bar r_0=0.05938+(-0.10509)=-0.04571 .$$

> **The pooled table compares a mostly-female drug group with a mostly-male control group.** The
> composition term ($-10.5$ points) swamps the within-gender benefit ($+5.9$ points). Equation (2) is the
> categorical twin of the selection-bias decomposition of [[L05-02-potential-outcomes-identification]]
> (naive gap = effect + bias).

**Standardise instead.** Evaluate (1) for both groups at the **same** mix, the population share
$\pi^\ast=343/700=0.49$:

$$\bar r_1(\pi^\ast)=(0.51)(0.93103)+(0.49)(0.73004)=0.47483+0.35772=0.83255,$$

$$\bar r_0(\pi^\ast)=(0.51)(0.86667)+(0.49)(0.68750)=0.44200+0.33688=0.77888,$$

$$\bar r_1(\pi^\ast)-\bar r_0(\pi^\ast)=0.05367 .$$

This is the **adjustment formula** of note 02 (eq. (12) there): when gender is the only confounder, the
drug raises recovery by 5.4 points on average.

![Left: recovery rate against the share of women in a group, one straight line for the drug and one for no drug, the drug line above at every share; the observed groups sit at shares 0.75 (drug, 78%) and 0.23 (no drug, 83%), and the standardised rates at the common share 0.49 are 0.833 and 0.779. Right: three age groups each with a downward exercise–cholesterol line of slope −2 and a pooled line of slope +4](figures/L05-simpson-weights.png)
*Left: eq. (1) for each group as a function of the mix $\pi$; slide p. 6 counts. Right: an illustrative linear model of slide p. 7's Example 3 (group means of exercise 2, 5, 8 hours; intercepts 180, 201, 222; within slope $-2$), exact population lines.*

On the left the drug line lies above the no-drug line at **every** mix; the reversal comes only from
reading the two lines at different points (orange dots). At a common mix (green squares) the drug wins.
On the right the pooled slope is $\operatorname{Cov}(x,y)/\operatorname{Var}(x)$ with
$\operatorname{Var}(x)=s^2+\operatorname{Var}(m_g)=1+6=7$ and
$\operatorname{Cov}(x,y)=-2(7)+\operatorname{Cov}(m_g,c_g)=-14+42=28$, so the pooled slope is $28/7=+4$
while every within-age slope is $-2$.

---

## 3 · C — the three junctions (slides pp. 8–9)

A **DAG** (directed acyclic graph) draws each variable as a node and each direct cause as an arrow;
"acyclic" means no node causes itself through a loop. Every path between two nodes is a sequence of
**junctions** of three nodes, and there are only three kinds.

| Junction | Shape | Unconditionally | Given the middle node | Slides' rule |
|---|---|---|---|---|
| **Chain** | $X\to Y\to Z$ | dependent | **independent** | Rule 1 (p. 8) |
| **Fork** | $Y\leftarrow X\rightarrow Z$ | dependent | **independent** | Rule 2 (p. 8) |
| **Collider** | $X\to Z\leftarrow Y$ | **independent** | dependent (also given any descendant of $Z$) | Rule 3 (p. 9) |

The rules, as stated on the slides:

- **Rule 1** (chains): "$X$ and $Z$ are conditionally independent given $Y$, if there is only one unidirectional path between $X$ and $Z$ and $Y$ is any set of variables that intercepts that path."
- **Rule 2** (forks): "If $X$ is a common cause of $Y$ and $Z$, and there is only one path between $Y$ and $Z$, then $Y$ and $Z$ are independent conditional on $X$."
- **Rule 3** (colliders): "If $Z$ is a collision between $X$ and $Y$ and there is only one path between $X$ and $Y$, then $X$ and $Y$ are unconditionally independent but are conditionally dependent given $Z$ and any descendants of $Z$."

(The collider picture on p. 9 labels both parents "Y"; Rule 3 beneath it names them $X$ and $Y$.)

**Back to the paradox.** Gender is the middle of a **fork** $D\leftarrow G\rightarrow R$: conditioning on it
blocks the non-causal path, so the stratified table is the causal one. Post-treatment BP is the middle of
a **chain** $D\to BP\to R$: conditioning on it blocks part of the causal effect itself, so the pooled table
is the causal one. Age in Example 3 and firm size in the marketing example (§7) are forks.

### 3.1 · C — Gaussian algebra for the collider (why conditioning *creates* dependence)

Take $X,Z$ independent $N(0,1)$ and the collider $W=aX+bZ+e$, $e\sim N(0,s^2)$ independent.

**Moments.** From the definition of $W$:

$$\operatorname{Var}(W)=a^2+b^2+s^2,\qquad\operatorname{Cov}(X,W)=a,\qquad\operatorname{Cov}(Z,W)=b,\qquad\operatorname{Cov}(X,Z)=0.\tag{3}$$

**Partial covariance and variances** (normal conditioning, $\operatorname{Cov}(A,B\mid W)=\operatorname{Cov}(A,B)-\operatorname{Cov}(A,W)\operatorname{Cov}(B,W)/\operatorname{Var}(W)$). Substituting (3):

$$\operatorname{Cov}(X,Z\mid W)=0-\frac{(a)(b)}{a^2+b^2+s^2},\qquad\operatorname{Var}(X\mid W)=1-\frac{a^2}{a^2+b^2+s^2}=\frac{b^2+s^2}{a^2+b^2+s^2},$$

$$\operatorname{Var}(Z\mid W)=\frac{a^2+s^2}{a^2+b^2+s^2}.$$

**Partial correlation.** Divide; the common denominator cancels:

$$\operatorname{Corr}(X,Z\mid W)=\frac{-ab}{\sqrt{(a^2+s^2)(b^2+s^2)}}.\tag{4}$$

With $a=b=s=1$: $-1/\sqrt{(2)(2)}=-0.5$. **A descendant** $U=W+v$, $v\sim N(0,t^2)$, replaces $s^2$ by $s^2+t^2$ in (4): with $t=1$, $-1/\sqrt{(3)(3)}=-1/3$. The dependence is weaker but not zero, which is why Rule 3 says "and any descendants".

![Left: partial correlation of X and Z given the collider W against the coefficient a, for noise sd 0.5, 1 and 2, all negative and growing in magnitude with a, against the flat zero of the unconditional correlation. Right: partial correlation given a descendant U of W against the descendant's noise sd t, rising from −0.5 at t = 0 towards zero, with the fork-given-its-middle line at zero](figures/L05-collider-bias.png)
*Eq. (4) and its descendant version; slide p. 9 (Rule 3) and p. 11 (conditioning on $U$).*

Reading: the green line is the truth before conditioning, zero. Every orange curve is a dependence the
analyst **manufactures** by conditioning on $W$: the more both causes matter relative to the noise, the
stronger it is. On the right, a noisy descendant of the collider still opens the path, fading only as the
descendant stops carrying information about $W$. A fork conditioned on its middle node, by contrast,
gives exactly zero.

---

## 4 · C — paths and junctions on a larger DAG (slides pp. 9–10)

Harrison's DAG (slide p. 9): $Z_1\to X$, $Z_1\to Z_3$, $Z_2\to Z_3$, $Z_2\to Y$, $Z_3\to X$, $Z_3\to Y$, $X\to W\to Y$.
"Paths always start at the treatment ($X$), always end at the outcome ($Y$) and are acyclic" (p. 9). The five paths:

| # | Path | Junctions | Open with no conditioning? |
|---|---|---|---|
| 1 | $X\to W\to Y$ | chain at $W$ | yes: **the causal path** |
| 2 | $X\leftarrow Z_1\to Z_3\to Y$ | fork at $Z_1$, chain at $Z_3$ | yes: back door |
| 3 | $X\leftarrow Z_1\to Z_3\leftarrow Z_2\to Y$ | fork, **collider at $Z_3$**, fork | **no**: blocked by the collider |
| 4 | $X\leftarrow Z_3\to Y$ | fork at $Z_3$ | yes: back door |
| 5 | $X\leftarrow Z_3\leftarrow Z_2\to Y$ | chain at $Z_3$, fork at $Z_2$ | yes: back door |

The slide lists all 15 junctions of the graph: 7 chains (junctions 1–7), 3 forks (8–10), 5 colliders
(11–15) — counts confirmed by brute force in [[L05-10-python]] §1.

**The adjustment puzzle this graph sets.** To estimate $X\to Y$ you must block paths 2, 4 and 5 without
blocking 1 or opening 3. $Z_3$ sits on paths 2, 4, 5 (a chain or fork node: conditioning blocks) **and** is the
collider of path 3 (conditioning opens). So $\{Z_3\}$ alone blocks three back doors and opens a fourth;
$\{Z_1,Z_3\}$ or $\{Z_2,Z_3\}$ block everything. In the slide's SEM (§5) the population regression of $Y$ on
$X$ gives **5.4381** with no controls, **6.0051** with $Z_3$ alone and exactly **6** (the causal $3\times2$) with
$\{Z_1,Z_3\}$ or $\{Z_2,Z_3\}$ ([[L05-10-python]] §1). The $Z_3$-only bias is small here, but it is not zero, and
in other graphs it is large.

---

## 5 · C — simulating data from a DAG (slide p. 10)

The slide writes the graph as a linear structural model:

$$Z_1\sim N(4.75,1.72^2),\quad Z_2\sim N(3.29,1.89^2),\tag{5}$$
$$Z_3=3Z_1-1.5Z_2+\varepsilon_{z3},\qquad X=2Z_1+2.5Z_3+\varepsilon_x,\qquad W=3X+\varepsilon_w,\qquad Y=2W+2Z_2-3Z_3+\varepsilon_y .\tag{6}$$

**Total effect of $X$ on $Y$.** Substitute $W$ from (6) into the $Y$ equation:

$$Y=2(3X+\varepsilon_w)+2Z_2-3Z_3+\varepsilon_y=6X+2Z_2-3Z_3+2\varepsilon_w+\varepsilon_y,$$

so the causal effect is $6$, and a regression recovers it only if the remaining terms $2Z_2-3Z_3$ are
uncorrelated with $X$ given the controls — exactly the back-door condition of §4.

(G) **A slip in the slide's R code.** The code first computes every node noise-free
(`z3 = 3*z1 - 1.5*z2`, `x = 2*z1 + 2.5*z3`, …) and only afterwards adds noise to each one, so the noise
of $Z_3$ never reaches $X$, $W$ or $Y$. The data it prints do not follow (6). [[L05-10-python]] §1 uses the
equations as written, with each noise variance equal to the variance of its node's systematic part (the
code's `sig.*` rule).

**Causal discovery vs validation** (p. 10, quoted): discovery generates a DAG from data; validation tests a
proposed DAG; "it is typically possible for more than one DAG to satisfy the causal validation tests". Named
only.

---

## 6 · C — d-separation (slide p. 11)

**Definition** (slide p. 11, verbatim in substance). A path $p$ is **blocked** by a set of nodes $Z$ if and only if

1. $p$ contains a chain $A\to B\to C$ or a fork $A\leftarrow B\to C$ whose middle node $B$ is in $Z$, or
2. $p$ contains a collider $A\to B\leftarrow C$ such that $B$ is **not** in $Z$ and **no descendant** of $B$ is in $Z$.

"If $Z$ blocks every path between $X$ and $Y$, then $X$ and $Y$ are d-separated, conditional on $Z$, and thus are independent conditional on $Z$." Two consequences on the slide: "d-connected" = some path is open; and "if we are not conditioning on any variable, then only colliders can block a path".

### 6.1 · Worked example 1 (slide pp. 11–12): $Z\to W\leftarrow X\to Y$, $W\to U$

The only path from $Z$ to $Y$ is $Z\to W\leftarrow X\to Y$: a collider at $W$, then a fork at $X$.

| Conditioning set | Collider $W$ | Fork $X$ | Path | Verdict (slide) |
|---|---|---|---|---|
| $\varnothing$ | blocks | open | blocked | $Z\perp Y$ |
| $\{W\}$ | **opened** | open | open | dependent |
| $\{U\}$ ($U$ descends from $W$) | **opened** | open | open | dependent |
| $\{W,X\}$ | opened | **blocks** | blocked | $Z\perp Y\mid W,X$ |

### 6.2 · Worked example 2 (slide p. 12): add $T\to Z$ and $T\to Y$

Now two paths: (a) $Z\leftarrow T\to Y$ (fork at $T$), (b) $Z\to W\leftarrow X\to Y$ (as above). $Z\perp Y\mid S$
needs **both** blocked: (a) needs $T\in S$; (b) needs $W,U\notin S$ or $X\in S$.

| $S$ | path (a) | path (b) | Verdict |
|---|---|---|---|
| $\varnothing$ | open | blocked | dependent: "$Z\not\perp Y$, since path between $Z$ and $Y$ with no colliders" |
| $\{T\}$ | blocked | blocked | $Z\perp Y\mid T$ |
| $\{T,W\}$ | blocked | open ($X\notin S$) | dependent |
| $\{T,W,X\}$ | blocked | blocked | $Z\perp Y\mid T,W,X$ |

The slide's two full lists — d-connected given $W$, $U$, $\{W,U\}$, $\{W,T\}$, $\{U,T\}$, $\{W,U,T\}$, $\{W,X\}$, $\{U,X\}$,
$\{W,U,X\}$; d-separated given $T$, $\{X,T\}$, $\{W,X,T\}$, $\{U,X,T\}$, $\{W,U,X,T\}$ — follow from the two
conditions, and the five separating sets are **all** the separating subsets of $\{T,W,U,X\}$ (checked
exhaustively in [[L05-10-python]] §1).

> **The test is mechanical.** List every path, mark each junction, apply the two blocking conditions. The
> only judgement is the graph itself — and that, as the slides say of ignorability, "cannot be assessed
> from the observed data" (p. 16).

---

## 7 · C — the marketing campaign (slides pp. 12–13)

A seller of computer equipment offered discounts to some business customers; larger firms were more
likely to get them, and larger firms buy more (Kögel's example). Graph: $\text{disc}\leftarrow\text{size}\rightarrow\text{sales}$,
$\text{disc}\to\text{sales}$. Firm size is the middle of a **fork** on the back-door path, so "to isolate the causal
effect, we need to control for or hold constant the confounding variables" (p. 13): compare discounted and
non-discounted firms **of the same size**, exactly as in the gender table. The naive comparison mixes the
discount effect with the size effect, upwards.

---

## 8 · G — what the slides do not ask

The back-door criterion in general, do-calculus and causal discovery algorithms are named in the
slides' sources (Pearl et al.; Neal 2020; *The Mixtape*, linked from [[../../Aula/COURSE|Aula/COURSE]]) but not
developed. Not examinable beyond the junction rules and d-separation above.

---

## Links

- Neighbours: [[L05-00-map]] · [[L05-02-potential-outcomes-identification]] (next: the same confounding in potential-outcome language; adjustment formula = §2's standardisation).
- Unit: [[L05-03-omitted-variables-bad-control]] (a confounder left out = OVB; a mediator put in = bad control, the BP chain) · [[L05-05-instrumental-variables]] (the IV DAG) · [[L05-06-difference-in-differences]] (back doors through Time and group) · [[L05-08-formulas]] · [[L05-09-pitfalls]] · [[L05-10-python]] (d-separation by brute force).
- Class 2: [[../L02/L02-04-logistic-regression|L02 §4]] — the `default` student coefficient that flips sign once balance is controlled is a Simpson reversal through a fork.
- Rules pack: [[../../rules/02_causalidade_potential_outcomes|rules/02]] (bad controls, confounding).
- Existing material: [[../../Aula/class-05-06/potential-outcomes.ipynb|potential-outcomes notebook]].
- **Practice:** no book on disk has DAG exercises; the slides' two d-separation examples (pp. 11–12) and Harrison's path list (pp. 9–10) are the drill. Redo §6.2 for $Z$ and $U$.
