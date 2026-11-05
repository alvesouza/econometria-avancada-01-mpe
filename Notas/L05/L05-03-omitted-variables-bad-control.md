---
tags: [notes, lecture-05, causal-inference, omitted-variable-bias, bad-control, proxy-control, regression]
date: 2026-10-25
status: taught
source: "omitted-variable.html (Lopes, 10/11/2025): trivariate Gaussian, conditional distribution of y | x, z, simulation beta = 0.75, gamma = 1.20, n = 30, 1000 replications, corr(x, z) = 0, 0.05, ..., 0.95. MHE §3.2.2 The Omitted Variables Bias Formula pp. 44–46 (eq. 3.2.10–3.2.11 p. 45, footnote 10 multivariate version, Table 3.2.1 p. 46); §3.2.3 Bad Control pp. 47–50 (eq. 3.2.12 p. 48, the decomposition p. 49, proxy control 3.2.13–3.2.15 pp. 49–50)."
---

# omitted-variable.html · MHE §3.2.2–3.2.3 · Short equals long plus omitted times included, and the controls you must not add

> **Claim.** Leaving a regressor $z$ out of a regression moves the coefficient on $x$ by exactly
> **(effect of $z$ on $y$) × (slope of $z$ on $x$)**: "short equals long plus the effect of omitted times the
> regression of omitted on included" (MHE p. 45). The site's simulation ($\beta=0.75$, $\gamma=1.2$) is that
> formula, $E\hat\beta_{\text{short}}=0.75+1.2\rho$, plus a variance story: the long regression is centred but
> its spread blows up as $\rho\to1$. Adding controls is not always better: a variable **caused by the
> treatment** (occupation after college; a test score after schooling) is a **bad control** that reintroduces
> selection bias — the chain of [[L05-01-simpson-dags]], now in regression form.
> Prev: [[L05-02-potential-outcomes-identification]] · Next: [[L05-04-errors-in-variables]] · Map: [[L05-00-map]]

**Notation.**

- $y,x,z$: outcome, included regressor, omitted (or added) regressor; in the site's model all have mean 0 and variance 1.
- $\sigma_{xy},\sigma_{yz}$: covariances (= correlations) of $y$ with $x$ and $z$; $\rho=\operatorname{corr}(x,z)\in(-1,1)$.
- Long regression $y=\beta x+\gamma z+\varepsilon$; short regression $y=\beta^sx+u$; $\delta_{zx}=\operatorname{Cov}(z,x)/\operatorname{Var}(x)$: slope of $z$ on $x$.
- MHE: $y_i$ log wage, $s_i$ schooling, $A_i$ ability vector, $\rho$ the schooling coefficient (MHE's letter; **not** the correlation above — context disambiguates), $\gamma$ ability effects, $\delta_{As}$ slopes of $A_i$ on $s_i$.
- $n=30$ observations per replication, $N=1000$ replications (the site's design).

---

## 1 · C — the site's model: a trivariate Gaussian

$$\begin{pmatrix}y_i\\x_i\\z_i\end{pmatrix}\sim N\left(\begin{pmatrix}0\\0\\0\end{pmatrix},\begin{pmatrix}1&\sigma_{xy}&\sigma_{yz}\\\sigma_{xy}&1&\rho\\\sigma_{yz}&\rho&1\end{pmatrix}\right).\tag{1}$$

**Conditional mean.** For a Gaussian vector, $E(y\mid x,z)=\Sigma_{y,(x,z)}\Sigma_{(x,z)}^{-1}(x,z)'$. The regressor block and its inverse:

$$\Sigma_{(x,z)}=\begin{pmatrix}1&\rho\\\rho&1\end{pmatrix},\qquad\Sigma_{(x,z)}^{-1}=\frac1{1-\rho^2}\begin{pmatrix}1&-\rho\\-\rho&1\end{pmatrix}.\tag{2}$$

Multiply $(\sigma_{xy},\sigma_{yz})$ by (2):

$$(\beta,\gamma)=\frac1{1-\rho^2}\big(\sigma_{xy}-\rho\sigma_{yz},\ \sigma_{yz}-\rho\sigma_{xy}\big).\tag{3}$$

**Conditional variance** $\tau^2=1-(\sigma_{xy},\sigma_{yz})\Sigma_{(x,z)}^{-1}(\sigma_{xy},\sigma_{yz})'$. Substituting (2):

$$\tau^2=1-\frac{\sigma_{xy}^2-2\rho\sigma_{xy}\sigma_{yz}+\sigma_{yz}^2}{1-\rho^2}=\frac{1-\rho^2-\sigma_{xy}^2-\sigma_{yz}^2+2\sigma_{xy}\sigma_{yz}\rho}{1-\rho^2}.\tag{4}$$

So $y_i\mid x_i,z_i=\beta x_i+\gamma z_i+\varepsilon_i$, $\varepsilon_i\sim N(0,\tau^2)$, as on the page. (The page prints the
numerator as $1-\rho-\dots$; it is $1-\rho^2-\dots$ — the two agree only at $\rho=0$, the page's next case.
Checked against the Schur complement in [[L05-10-python]] §3.)

**At $\rho=0$** (the page's §1.2), (3) gives $\beta=\sigma_{xy}$, $\gamma=\sigma_{yz}$ and (4) gives $\tau^2=1-(\sigma_{xy}^2+\sigma_{yz}^2)$.

---

## 2 · C — the omitted-variables bias formula

**Short slope in the Gaussian model.** Regressing $y$ on $x$ alone gives $\beta^s=\operatorname{Cov}(y,x)/\operatorname{Var}(x)=\sigma_{xy}$. Write $\sigma_{xy}$ through the long model $y=\beta x+\gamma z+\varepsilon$:

$$\sigma_{xy}=\operatorname{Cov}(\beta x+\gamma z+\varepsilon,\ x)=\beta(1)+\gamma(\rho)+0.$$

Hence

$$\beta^s=\beta+\gamma\rho .\tag{5}$$

(Check with (3): $\beta+\gamma\rho=[\sigma_{xy}-\rho\sigma_{yz}+\rho\sigma_{yz}-\rho^2\sigma_{xy}]/(1-\rho^2)=\sigma_{xy}$.)

**MHE's general version** (eq. 3.2.11, p. 45). Long regression $y_i=\alpha+\rho s_i+A_i'\gamma+\varepsilon_i$ (3.2.10) with
$\varepsilon_i$ uncorrelated with $s_i$ and $A_i$ by construction. Plug it into the short-regression formula:

$$\frac{\operatorname{Cov}(y_i,s_i)}{V(s_i)}=\frac{\operatorname{Cov}(\alpha+\rho s_i+A_i'\gamma+\varepsilon_i,\ s_i)}{V(s_i)}=\rho+\gamma'\frac{\operatorname{Cov}(A_i,s_i)}{V(s_i)}=\rho+\gamma'\delta_{As}.\tag{6}$$

> **"Short equals long plus the effect of omitted times the regression of omitted on included"** (MHE p. 45).
> The formula is mechanical — it links two regressions "whether or not the longer regression is causal"
> (p. 44). The sign of the bias is sign($\gamma$) × sign($\delta$): ability raises wages and (probably) schooling,
> so the short return is too big; if some omitted factor is negatively related to schooling it can be too small
> (p. 45). Short = long exactly when the omitted and included variables are uncorrelated.

Multivariate form (MHE footnote 10, p. 45): $\beta_1^s=\beta_1^l+E[X_{1i}X_{1i}']^{-1}E[X_{1i}X_{2i}']\beta_2^l$.

---

## 3 · C — the site's simulation, made exact

**Design** (omitted-variable.html): $(x_i,z_i)\sim N(0,[\begin{smallmatrix}1&\rho\\\rho&1\end{smallmatrix}])$, $y_i=0.75x_i+1.2z_i+e_i$, $e_i\sim N(0,1)$, $n=30$,
1000 replications per $\rho\in\{0,0.05,\dots,0.95\}$; both regressions **without intercept** (`lm(y~x-1)`, `lm(y~x+z-1)`).

**Short estimator.** Write $z_i=\rho x_i+\sqrt{1-\rho^2}\,v_i$ with $v_i\sim N(0,1)$ independent of $x_i$. Substitute into $y_i$:

$$y_i=0.75x_i+1.2\big(\rho x_i+\sqrt{1-\rho^2}\,v_i\big)+e_i=(0.75+1.2\rho)x_i+1.2\sqrt{1-\rho^2}\,v_i+e_i .$$

The no-intercept OLS slope is $\sum x_iy_i/\sum x_i^2$; substitute:

$$\hat\beta^s=(0.75+1.2\rho)+\frac{\sum x_i\big(1.2\sqrt{1-\rho^2}v_i+e_i\big)}{\sum x_i^2}.\tag{7}$$

Given $x$, the last term has mean 0 and variance $(1.44(1-\rho^2)+1)/\sum x_i^2$. With $\sum x_i^2\sim\chi^2_{30}$ and $E[1/\chi^2_n]=1/(n-2)$:

$$E\hat\beta^s=0.75+1.2\rho,\qquad\operatorname{sd}(\hat\beta^s)=\sqrt{\frac{1+1.44(1-\rho^2)}{28}}.\tag{8}$$

**Long estimator.** Unbiased; given $X$, $\operatorname{Var}=[(X'X)^{-1}]_{11}$ (error variance 1). (G) The inverse-Wishart mean
$E[(X'X)^{-1}]=\Sigma^{-1}/(n-p-1)$ with $p=2$, and $[\Sigma^{-1}]_{11}=1/(1-\rho^2)$ by (2):

$$E\hat\beta=0.75,\qquad\operatorname{sd}(\hat\beta)=\sqrt{\frac1{27(1-\rho^2)}}.\tag{9}$$

| $\rho$ | $E\hat\beta^s$ by (8) | sd short | sd long by (9) | MSE short | MSE long |
|---|---|---|---|---|---|
| 0 | $0.75+1.2(0)=0.75$ | $\sqrt{2.44/28}=0.2952$ | $\sqrt{1/27}=0.1925$ | 0.0871 | 0.0370 |
| 0.5 | $0.75+1.2(0.5)=1.35$ | $\sqrt{2.08/28}=0.2726$ | $\sqrt{1/20.25}=0.2222$ | $0.36+0.0743=0.4343$ | 0.0494 |
| 0.95 | $0.75+1.2(0.95)=1.89$ | $\sqrt{1.1404/28}=0.2018$ | $\sqrt{1/2.6325}=0.6163$ | $1.2996+0.0407=1.3403$ | 0.3799 |

![Two panels of boxplots of the OLS estimate of beta over 1000 seeded replications with n = 30 at corr(x,z) from 0 to 0.95. Left, the long regression: boxes centred on 0.75 at every correlation, widening sharply beyond 0.8, with the exact mean ± 1 sd band. Right, the short regression: boxes rising along the exact line 0.75 + 1.2 rho, from 0.75 to 1.89, with a slowly narrowing band](figures/L05-ovb-sampling.png)
*Boxes: a seeded re-run of the site's simulation in Python (not the site's draws). Lines and bands: exact (8)–(9). omitted-variable.html; MHE eq. 3.2.11.*

Reading: the right panel is (5) drawn — every box sits on $0.75+1.2\rho$, and no amount of data moves it
back to 0.75. The left panel is the price of including $z$ when it is nearly collinear with $x$: centred, but at
$\rho=0.95$ its sd is three times the short regression's. Even so the long regression wins on MSE at every
$\rho$ in the table, because the bias $1.2\rho$ grows faster than the variance it saves.

---

## 4 · C — reading MHE Table 3.2.1 through the formula (p. 46)

NLSY men, log wage on schooling, $n=2434$ (MHE p. 46):

| Controls | none | age dummies | + parents' schooling, race, region | + AFQT | + occupation |
|---|---|---|---|---|---|
| schooling coefficient | 0.132 | 0.131 | 0.114 | 0.087 | 0.066 |
| (s.e.) | (0.007) | (0.007) | (0.007) | (0.009) | (0.010) |

By (6), each drop is $\gamma'\delta$ of the variables just added: family background takes $0.132-0.114=0.018$ off
and AFQT (an ability proxy) $0.114-0.087=0.027$, "a result of the fact that the additional controls are positively
correlated with both wages and schooling" (p. 46). The last drop, $0.087-0.066=0.021$, is **not** an OVB
correction: occupation is a bad control (§5).

---

## 5 · C — bad control (MHE §3.2.3, pp. 47–49)

"Bad controls are variables that are themselves outcome variables in the notional experiment at hand"
(p. 47). College $c_i$ randomly assigned; white-collar status $w_i$ and earnings $y_i$ both respond to it:

$$y_i=c_iy_{1i}+(1-c_i)y_{0i},\qquad w_i=c_iw_{1i}+(1-c_i)w_{0i}.\tag{10}$$

**Comparison within white-collar workers** (MHE eq. 3.2.12, p. 48). On $c_i=1$ the observed $(y,w)$ are $(y_1,w_1)$, on $c_i=0$ they are $(y_0,w_0)$:

$$E[y_i\mid w_i=1,c_i=1]-E[y_i\mid w_i=1,c_i=0]=E[y_{1i}\mid w_{1i}=1,c_i=1]-E[y_{0i}\mid w_{0i}=1,c_i=0].$$

**Random assignment** of $c_i$ (independent of all four potential outcomes) drops the $c_i$ conditions:

$$=E[y_{1i}\mid w_{1i}=1]-E[y_{0i}\mid w_{0i}=1].$$

**Add and subtract** $E[y_{0i}\mid w_{1i}=1]$ (MHE p. 49):

$$=\underbrace{E[y_{1i}-y_{0i}\mid w_{1i}=1]}_{\text{causal effect on those white-collar with college}}+\underbrace{E[y_{0i}\mid w_{1i}=1]-E[y_{0i}\mid w_{0i}=1]}_{\text{selection bias}}.\tag{11}$$

> **Even with college randomly assigned, conditioning on occupation is apples to oranges.** College changes
> who is in the white-collar pool; the selection term need not be zero even if $y_{1i}=y_{0i}$ for everyone
> (p. 49). In DAG language $c\to w\to y$ is a chain and $w$ is also a collider on $c\to w\leftarrow(\text{ability})\to y$:
> conditioning on it both blocks part of the effect and opens a back door.

### 5.1 · C — proxy control (MHE pp. 49–50)

Wanted: $y_i=\alpha+\rho s_i+\gamma a_i+\varepsilon_i$ (3.2.13), with $a_i$ ability measured before schooling. Available
only: late ability $al_i=\pi_0+\pi_1s_i+\pi_2a_i$ (3.2.14), raised by schooling ($\pi_1>0$).

**Solve (3.2.14) for $a_i$:** $a_i=(al_i-\pi_0-\pi_1s_i)/\pi_2$. **Substitute into (3.2.13):**

$$y_i=\alpha+\rho s_i+\gamma\left(\frac{al_i-\pi_0-\pi_1s_i}{\pi_2}\right)+\varepsilon_i .$$

**Collect terms** (MHE eq. 3.2.15):

$$y_i=\Big(\alpha-\gamma\frac{\pi_0}{\pi_2}\Big)+\Big(\rho-\gamma\frac{\pi_1}{\pi_2}\Big)s_i+\frac{\gamma}{\pi_2}\,al_i+\varepsilon_i .\tag{12}$$

With $\rho,\gamma,\pi_1,\pi_2>0$ the schooling coefficient $\rho-\gamma\pi_1/\pi_2$ is **too small**; e.g. $\rho=0.10$,
$\gamma=0.05$, $\pi_1=0.2$, $\pi_2=1$ gives $0.10-0.05(0.2)/1=0.09$. With no control at all, (6) gives
$\rho+\gamma\delta_{as}$, too big when $\delta_{as}>0$; so "the causal effect of interest lies between these two" (p. 50).

> **Timing decides.** "Variables measured before the variable of interest was determined are generally good
> controls" (p. 50). In DAG terms: condition on forks (confounders); never on chains out of the treatment
> (mediators, outcomes) or on colliders.

---

## Links

- Neighbours: [[L05-02-potential-outcomes-identification]] · [[L05-04-errors-in-variables]] (next: a regressor that is *there* but measured with noise).
- Unit: [[L05-01-simpson-dags]] (§4: the $Z_3$ collider is a bad control of the third kind) · [[L05-05-instrumental-variables]] (IV as the cure when the omitted variable cannot be measured; slide §9.2 shows that simply adding the instrument does not work) · [[L05-08-formulas]] · [[L05-09-pitfalls]] · [[L05-10-python]] §3.
- Class 1: [[../L01/L01-06-gaussian-linear-regression|L01 §6]] (OLS as a projection; partialling out). Class 2: [[../L02/L02-02-linear-log-linear-regression|L02 §2]] (the Mroz return to education that moves with controls).
- Rules pack: [[../../rules/02_causalidade_potential_outcomes|rules/02]] (omitted variable bias formula; bad controls) · [[../../rules/01_endogeneidade_iv|rules/01]] (endogeneity sources).
- **Practice:** MHE Table 3.2.1 (p. 46), read as in §4.
