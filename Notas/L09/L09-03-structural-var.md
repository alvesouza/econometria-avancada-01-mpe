---
tags: [notes, lecture-09, svar, identification, cholesky, recursive, order-condition]
date: 2026-10-25
status: taught
source: "BVAR-part11.pdf slides 31 (Rubio-Ramírez, Waggoner and Zha 2010 quote), 32 (trivariate SVAR(1) with commodity prices, output, interest rate), 33 (SVAR(p) set-up), 34 (exact identification), 35–36 (Illustrations 1–2: zero patterns of A0), 37 (monetary policy shock, figure); Tsay AFTS 3e §8.2.1 (pp. 399–401, eqs. 8.9–8.10, Example 8.3) and p. 413 (ordering dependence)"
---

# Slides 31–37 · Structural VARs: the reduced form cannot tell orthogonal rotations apart, so $q(q-1)/2$ restrictions must come from economics

> **Claim.** A structural VAR $A_0y_t=A_1y_{t-1}+\dots+u_t$ with orthogonal unit-variance shocks
> maps to the reduced form by $B_i=A_0^{-1}A_i$, $\Sigma=(A_0'A_0)^{-1}$. Any orthogonal $Q$ turns
> $(A_0,A)$ into $(QA_0,QA)$ **with exactly the same $(B,\Sigma)$**, so the data identify $\Sigma$'s
> $q(q+1)/2$ numbers and nothing more; $A_0$ has $q^2$. The gap, $q(q-1)/2$, must be filled by
> restrictions. **The Cholesky ordering of [[L09-02-vma-irf-fevd]] is one such set — a recursive
> SVAR —** and Tsay's Example 8.3 shows two orderings giving two different, equally valid
> "structural" equations from one reduced form.

Prev: [[L09-02-vma-irf-fevd]] · Next: [[L09-04-bvar-minnesota-ssvs]] · Map: [[L09-00-map]]

**Notation.**

| Symbol | Meaning |
|---|---|
| $A_0$ | $q\times q$ contemporaneous structural matrix, invertible |
| $A_i$, $A=(A_1,\dots,A_p)$ | structural lag matrices |
| $u_t$ | structural shocks, $N(0,I_q)$ (slide 33) |
| $B_i,\ \Sigma$ | reduced-form coefficients and innovation covariance |
| $e_t=A_0^{-1}u_t$ | reduced-form innovation (called $u_t$ in [[L09-01-var-p-estimation-forecasting]]) |
| $Q$ | $q\times q$ orthogonal matrix, $Q'Q=I$ |
| $L,G$ | Tsay's unit-lower-triangular $L$ and diagonal $G$, $\Sigma=LGL'$ |

---

## 1 · U — the question

Slide 31 quotes Rubio-Ramírez, Waggoner and Zha (2010): "Since the seminal work by Sims (1980),
identification of structural vector autoregressions (SVARs) has been an unresolved theoretical
issue. Filling this theoretical gap is of vital importance because impulse responses based on
SVARs have been widely used for policy analysis and to provide stylized facts for dynamic
stochastic general equilibrium (DSGE) models." A reduced-form VAR forecasts; a **policy question**
("what does a monetary shock do to output?") needs a shock with an economic name, and naming it
is identification.

---

## 2 · C — from structure to reduced form (slide 33)

$$A_0y_t=A_1y_{t-1}+\dots+A_py_{t-p}+u_t,\qquad u_t\overset{iid}{\sim}N(0,I_q).\tag{1}$$

Premultiply (1) by $A_0^{-1}$:

$$y_t=A_0^{-1}A_1y_{t-1}+\dots+A_0^{-1}A_py_{t-p}+A_0^{-1}u_t.\tag{2}$$

Matching (2) with the reduced form $y_t=B_1y_{t-1}+\dots+B_py_{t-p}+e_t$:

$$B_i=A_0^{-1}A_i,\qquad B=A_0^{-1}A,\qquad e_t=A_0^{-1}u_t.\tag{3}$$

The innovation covariance, using $\mathrm{Cov}(u_t)=I$ and $(MN)^{-1}=N^{-1}M^{-1}$:

$$\Sigma=\mathrm{Cov}(e_t)=A_0^{-1}I(A_0^{-1})'=A_0^{-1}(A_0')^{-1}=(A_0'A_0)^{-1}.\tag{4}$$

These are slide 33's "$B_i=A_0^{-1}A_i$, $B=A_0^{-1}A$, $\Sigma=(A_0'A_0)^{-1}$". The structural
impulse response follows from [[L09-02-vma-irf-fevd]] (1) with $e_t=A_0^{-1}u_t$:

$$y_t=\sum_s\Psi_sA_0^{-1}u_{t-s},\qquad\frac{\partial y_{t+s}}{\partial u_t'}=\Psi_sA_0^{-1}.\tag{5}$$

---

## 3 · C — why the reduced form cannot identify $A_0$

Slide 34 defines $g(A_0,A)=(A_0^{-1}A,\ (A_0'A_0)^{-1})$. Take any orthogonal $Q$ and set
$\tilde A_0=QA_0$, $\tilde A=QA$. Then

$$\tilde A_0^{-1}\tilde A=(QA_0)^{-1}QA=A_0^{-1}Q^{-1}QA=A_0^{-1}A=B,\tag{6}$$

$$(\tilde A_0'\tilde A_0)^{-1}=(A_0'Q'QA_0)^{-1}=(A_0'A_0)^{-1}=\Sigma.\tag{7}$$

So $g(QA_0,QA)=g(A_0,A)$: **the likelihood is flat along the orbit $\{QA_0\}$**. Since $B$ is
pinned once $A_0$ is (by (3), $A=A_0B$), everything reduces to recovering $A_0$ from $\Sigma$.

**Order condition (counting).** $\Sigma$ is symmetric: $q(q+1)/2$ free numbers. $A_0$ has $q^2$.
The shortfall is

$$q^2-\frac{q(q+1)}2=\frac{q(q-1)}2\tag{8}$$

— the dimension of the orthogonal group. With $q=2$: one restriction; $q=3$: three; $q=5$: ten;
$q=6$: fifteen. Restrictions are typically zeros in $A_0$ (a variable does not enter an
equation contemporaneously).

**Definition** (slide 34, verbatim): "The SVAR is exactly identified if and only if, for almost
any reduced-form parameter point $(B,\Sigma)$, there exists a unique structural parameter point
$(A_0,A)\in R$ such that $g(A_0,A)=(B,\Sigma)$." Counting is necessary, not sufficient: the zeros
must also be placed so that no rotation other than $Q=I$ (up to sign) preserves them — the rank
condition that Rubio-Ramírez, Waggoner and Zha make operational. "Much of the SVAR literature
involves exactly identified models" (slide 33). Waggoner and Zha (2003) give an MCMC algorithm for
a restricted $A_0$ (slide 34).

---

## 4 · C — recursive identification is the Cholesky factor

Restrict $A_0$ to be **lower triangular** with positive diagonal: $q(q-1)/2$ zeros above the
diagonal, exactly (8). Then $A_0^{-1}$ is lower triangular with positive diagonal and, by (4),
$A_0^{-1}(A_0^{-1})'=\Sigma$. The Cholesky factor is unique, so

$$A_0^{-1}=P\quad(\text{the lower Cholesky factor of }\Sigma),\qquad\Psi_sA_0^{-1}=\Psi_sP=\Theta_s.\tag{9}$$

**The orthogonalised IRF of [[L09-02-vma-irf-fevd]] (6) is the structural IRF of a recursive SVAR.**
The economic content of the ordering: variable 1's equation contains no other current variable
(it reacts to nothing within the period); variable $q$'s contains them all.

### 4.1 · Worked — Tsay Example 8.3 (pp. 400–401), both orderings

Reduced form: $\phi_0=(0.2,\ 0.4)'$, $\Phi=\begin{pmatrix}0.2&0.3\\-0.6&1.1\end{pmatrix}$,
$\Sigma=\begin{pmatrix}2&1\\1&1\end{pmatrix}$ (the VAR(1) of [[../L01/L01-07-ar-var-review|L01 §9.1]]).

**Ordering $(r_1,r_2)$.** Factor $\Sigma=LGL'$ with $L=\begin{pmatrix}1&0\\l&1\end{pmatrix}$,
$G=\mathrm{diag}(g_1,g_2)$:

$$LGL'=\begin{pmatrix}g_1&lg_1\\lg_1&l^2g_1+g_2\end{pmatrix}=\begin{pmatrix}2&1\\1&1\end{pmatrix}\Rightarrow g_1=2,\quad l=\tfrac12,\quad g_2=1-\tfrac14(2)=0.5.$$

$L^{-1}=\begin{pmatrix}1&0\\-0.5&1\end{pmatrix}$ (T: "$L^{-1}=\begin{pmatrix}1.0&0.0\\-0.5&1.0\end{pmatrix}$").
Premultiply the reduced form by $L^{-1}$ (T eq. 8.9):

$$L^{-1}\phi_0=\begin{pmatrix}0.2\\-0.5(0.2)+0.4\end{pmatrix}=\begin{pmatrix}0.2\\0.3\end{pmatrix},\qquad L^{-1}\Phi=\begin{pmatrix}0.2&0.3\\-0.5(0.2)-0.6&-0.5(0.3)+1.1\end{pmatrix}=\begin{pmatrix}0.2&0.3\\-0.7&0.95\end{pmatrix}.$$

Row 2 of $L^{-1}r_t$ is $r_{2t}-0.5r_{1t}$; moving $-0.5r_{1t}$ to the right gives Tsay's structural
equation (T eq. 8.10):

$$r_{2t}=0.3+0.5r_{1t}-0.7r_{1,t-1}+0.95r_{2,t-1}+b_{2t},\qquad\mathrm{Var}(b_{2t})=0.5.\tag{10}$$

**Ordering $(r_2,r_1)$.** Now $\Sigma^*=\begin{pmatrix}1&1\\1&2\end{pmatrix}$: $g_1=1$, $l=1$,
$g_2=2-1=1$, $L^{-1}=\begin{pmatrix}1&0\\-1&1\end{pmatrix}$, and (T p. 401)

$$r_{1t}=-0.2+1.0\,r_{2t}-0.8r_{2,t-1}+0.8r_{1,t-1}+c_{2t},\qquad\mathrm{Var}(c_{2t})=1.\tag{11}$$

(Check the intercept: $-1(0.4)+0.2=-0.2$; the lag terms: $-1(1.1)+0.3=-0.8$ on $r_{2,t-1}$ and
$-1(-0.6)+0.2=0.8$ on $r_{1,t-1}$.)

> **(10) says $r_1$ drives $r_2$ within the period; (11) says $r_2$ drives $r_1$. Both are exact
> rewritings of the same reduced form.** The data are silent between them: the choice is an
> assumption about timing.

In SVAR form (1), $A_0=G^{-1/2}L^{-1}$ (rows rescaled to unit-variance shocks). Impact responses
$A_0^{-1}=LG^{1/2}=P$:

| impact on → / of shock | ordering $(r_1,r_2)$: shock 1 | shock 2 | ordering $(r_2,r_1)$: $r_1$ shock | $r_2$ shock |
|---|---|---|---|---|
| $r_1$ | $\sqrt2=1.414$ | 0 | 1 | 1 |
| $r_2$ | $0.5\sqrt2=0.707$ | $\sqrt{0.5}=0.707$ | 0 | 1 |

In general, with $\sigma_1,\sigma_2,\rho$: ordering $(r_1,r_2)$ gives $r_1$ an own impact $\sigma_1$
and a cross impact 0; ordering $(r_2,r_1)$ gives $\sigma_1\sqrt{1-\rho^2}$ and $\rho\sigma_1$. With
$\sigma_1=\sqrt2$ and $\rho=1/\sqrt2$: $\sqrt2\sqrt{1/2}=1$ and $(1/\sqrt2)\sqrt2=1$ — the table.

**What it does to the variance decomposition.** With Example 8.3's numbers, the share of $r_1$'s 10-step forecast-error variance attributed to the $r_2$ shock is **13.6%** under ordering $(r_1,r_2)$ and **48.5%** under $(r_2,r_1)$ (the defaults of the Ordering Dial, verified in `companions/check_companions.py`): the same data, a story that changes by 35 percentage points.

![Three panels for Tsay Example 8.3: the response of r1 to its own shock starts at 1.414 under ordering (r1, r2) and at 1 under (r2, r1); the response of r1 to the r2 shock starts at 0 under one ordering and at 1 under the other; the third panel plots the own and cross impacts against rho, coinciding only at rho = 0](figures/L09-cholesky-ordering.png)
*Figure — orthogonalised responses $\Phi^hA_0^{-1}$ of T Ex. 8.3 under the two recursive orderings, and the impact on $r_1$ against $\rho$ with $\sigma_1^2=2$ (T p. 400; (9)).*

The middle panel is the whole problem: "the effect of an $r_2$ shock on $r_1$" is zero on impact
and humped, or one on impact and monotone, depending only on the ordering. The right panel
shows when it does not matter: the curves meet at $\rho=0$, and the gap grows with $|\rho|$ — at
Example 8.3's $\rho=0.707$ the own impact falls from 1.414 to 1.

---

## 5 · C — non-recursive identification on the slides

**Slide 32** (commodity prices $P_{c,t}$, output $Y_t$, interest rate $R_t$, SVAR(1)): equation 1
is "monetary policy" with a $0.0$ coefficient on $\log Y_t$ (the central bank does not see current
output); equation 2 "characterizes behaviour of finished-goods producers" with $0.0$ on $R_t$;
equation 3, commodity prices "set in active competitive markets", is unrestricted. That is two
zeros; (8) asks for three with $q=3$, so the zeros shown are not enough by themselves — a third
restriction (another zero, or a sign restriction) is needed to pin down $A_0$.

**Illustrations 1–2** (slides 35–36), counted:

| | $q$ | needed, (8) | zeros in $A_0$ | order condition |
|---|---|---|---|---|
| Illustration 1: $\log Y,\log P,R,\log M,\log P_c$ × PS, PS, MP, MD, Inf | 5 | 10 | 1+2+2+2+4 = 11 | met, 1 overidentifying |
| Illustration 2: PCOM, M2, R, Y, CPI, U × Inform, MP, MD, Prod, Prod, Prod | 6 | 15 | 0+4+2+5+4+3 = 18 | met, 3 overidentifying |

(Row counts for Illustration 1 as printed, rows = variables: $\log Y$ 1 zero, $\log P$ 2, $R$ 2,
$\log M$ 2, $\log P_c$ 4; the slide reuses the labels $a_{14}$, $a_{15}$ in several rows — read
them as distinct free entries.) Illustration 2's monetary-policy row has free entries only on
M2 and R: the Fed reacts within the month to money and the funds rate, not to output, prices or
unemployment, which arrive with a lag. **Overidentified** models restrict $\Sigma$ and can be
tested; exactly identified ones fit $\Sigma$ perfectly whatever the zeros mean. Slide 37 shows
the resulting monetary-policy-shock responses (figure only).

---

## 6 · U — Python

`statsmodels.tsa.vector_ar.svar_model.SVAR(y, svar_type="A", A=mask)` estimates $A_0$ with
`"E"` marking free entries; the recursive case needs no SVAR call at all — `VARResults.irf(h).orth_irfs`
is (9). Both are used in [[L09-10-python]] §3.

---

## Links

- Neighbours: [[L09-02-vma-irf-fevd]] (the $\Theta_s$ that (9) reinterprets) · [[L09-04-bvar-minnesota-ssvs]].
- Later in the unit: [[L09-06-tvp-var-sv-state-space]] (Primiceri's $A_t$ is a time-varying recursive $A_0$).
- Class 1: [[../L01/L01-07-ar-var-review|L01 §9.1]] (Example 8.3's mean, $\Gamma_0$, stationarity).
- Rules: [[../../rules/05_espaco_estados_volatilidade|rules/05]].
- **Interactive companion.** [The Ordering Dial](companions/companion-var-irf-ordering.html) — set $\rho=0$ and the two orderings coincide; push $|\rho|$ up and watch the impact matrix and the FEVD split.
- **Practice (number and printed page only):** T 8.1 (p. 462) and T 8.7(b) (p. 463) involve orthogonalised IRFs whose ordering must be stated.
