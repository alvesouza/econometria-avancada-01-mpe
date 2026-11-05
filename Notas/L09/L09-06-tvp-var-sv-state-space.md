---
tags: [notes, lecture-09, var-garch, var-sv, tvp-var, primiceri, state-space, kalman-filter, discounting]
date: 2026-10-25
status: taught
source: "BVAR-part11.pdf slides 38–39 (VAR-GARCH, Pelloni and Polasek 2003), 40 (VAR-SV, Uhlig 1997), 41–44 (TVP-VAR-SV, Primiceri 2005; Nakajima, Kasuya and Watanabe 2011); BVAR-part2.pdf slide 61 (large TVP-BVAR, Koop and Korobilis 2012); Tsay AFTS 3e §11.1 (pp. 558–563: local trend model, eqs. 11.1–11.14, Example 11.1, Theorem 11.1), §11.1.7 (p. 571, eq. 11.25), §11.3.1 (pp. 577–578, CAPM with time-varying coefficients); Greenberg 1e §10.3 (pp. 161–164, time-varying parameters, eqs. 10.10–10.11, Table 10.3)"
---

# Slides 38–44 · Letting the VAR move: GARCH and SV in the errors, random-walk coefficients, and the Kalman filter that makes them estimable

> **Claim.** Three ways to relax a constant VAR, in increasing order of ambition: GARCH or SV in
> $\Sigma_t$ (Pelloni–Polasek, Uhlig), and random-walk coefficients **and** random-walk log
> volatilities in a time-varying recursive structure $\Sigma_t=A_t^{-1}D_tA_t^{-1\prime}$ (Primiceri).
> Every time-varying coefficient is a **state** in a linear state-space model, and the Kalman filter
> is its exact Gaussian posterior updater: a precision-weighted average of the prediction and the
> new observation, with gain $K_t$. In the local-level model the gain settles at
> $K^*=p^*/(p^*+1)$, $p^*=(q+\sqrt{q^2+4q})/2$, and **$1-K^*$ is the MA coefficient of the
> equivalent ARIMA(0,1,1)** — 0.858 for Tsay's Alcoa volatility, from two different routes.

Prev: [[L09-05-factor-models-favar]] · Next: [[L09-07-fsv-dcc-covariances]] · Map: [[L09-00-map]]

**Notation.**

| Symbol | Meaning | Range |
|---|---|---|
| $\Sigma_t$ | conditional covariance of $u_t$ | p.d. |
| $\mathrm{vech}(\cdot)$ | stack the lower triangle, $d=q(q+1)/2$ entries | |
| $B_t$, $\beta_t$ | time-varying VAR coefficients (matrix, stacked vector) | |
| $A_t$, $\alpha_t$ | unit-lower-triangular contemporaneous matrix, its free entries | |
| $D_t=\mathrm{diag}(\sigma_{1t}^2,\dots,\sigma_{qt}^2)$ | structural variances | $>0$ |
| $Q,S,W$ | innovation covariances of $B_t$, $\alpha_t$, $\log\sigma_t$ | p.d. |
| $\mu_t$ | state of the local-level model | |
| $\sigma_e^2,\ \sigma_\eta^2$ | measurement and state innovation variances | $>0$ |
| $q=\sigma_\eta^2/\sigma_e^2$ | signal-to-noise ratio | $\ge0$ |
| $\mu_{t\mid j},\ \Sigma_{t\mid j}$ | $E(\mu_t\mid F_j)$, $\mathrm{Var}(\mu_t\mid F_j)$ (Tsay's notation) | |
| $v_t,\ V_t,\ K_t$ | one-step forecast error, its variance, the Kalman gain | |
| $\delta$ | discount factor | $(0,1]$ |

---

## 1 · C — VAR-GARCH (slides 38–39)

Pelloni and Polasek (2003):

$$y_t=\sum_{i=1}^pB_iy_{t-i}+u_t,\qquad u_t\sim N(0,\Sigma_t),\qquad\mathrm{vech}(\Sigma_t)=\alpha_0+\sum_{i=1}^rA_i\,\mathrm{vech}(\Sigma_{t-i})+\sum_{i=1}^s\Gamma_i\,\mathrm{vech}(u_{t-i}u_{t-i}').\tag{1}$$

Each $A_i,\Gamma_i$ is $d\times d$ with $d=q(q+1)/2$: for $q=3$, $r=s=1$, the variance equation alone has
$6+36+36=78$ parameters, and positive definiteness of $\Sigma_t$ is not guaranteed. This is the full
VEC model whose restricted versions (diagonal VEC, BEKK) are Tsay §10.2; Class 9 uses (1) only to
show why factor and correlation models ([[L09-07-fsv-dcc-covariances]]) are needed. Application
(slide 39): German, US and UK quarterly employment shares, 1968–1998.

---

## 2 · C/G — VAR-SV (slide 40; Uhlig 1997)

$$y_t=\sum_{i=1}^pB_iy_{t-i}+u_t,\quad u_t\sim N(0,\Sigma_t),\quad\Sigma_t^{-1}=L_tL_t',\qquad\Sigma_{t+1}^{-1}=\frac{L_t\Theta_tL_t'}{\lambda},\quad\Theta_t\sim B_q\Big(\frac{\nu+pq}2,\frac12\Big).\tag{2}$$

The precision is multiplied each period by a random matrix-Beta shock and rescaled by $\lambda$.
**The scalar case** ($q=1$, G — derived here to read (2)). With $h_t=1/\sigma_t^2$ and $L_t=\sqrt{h_t}$,
(2) is $h_{t+1}=h_t\theta_t/\lambda$ with $\theta_t\sim\mathrm{Beta}(a,\tfrac12)$, $a=(\nu+p)/2$. Since
$E\theta_t=a/(a+\tfrac12)$:

$$E(h_{t+1}\mid h_t)=h_t\frac{a}{(a+\frac12)\lambda}=h_t\quad\iff\quad\lambda=\frac{a}{a+\frac12}=\frac{\nu+p}{\nu+p+1}.\tag{3}$$

So $\lambda$ sets the drift of the precision: at the value (3) the precision is a martingale, a
multiplicative random walk. The Beta–Wishart pair is conjugate, which is why Uhlig's model has a
closed-form filter — the multiplicative cousin of the discounting of §6.

---

## 3 · C — TVP-VAR-SV (slides 41–44; Primiceri 2005)

$$y_t=\sum_{i=1}^pB_{it}y_{t-i}+u_t,\qquad u_t\sim N(0,\Sigma_t),\qquad\Sigma_t=A_t^{-1}D_t(A_t^{-1})',\tag{4}$$

$$A_t=\begin{pmatrix}1&0&\cdots&0\\\alpha_{21,t}&1&\cdots&0\\\vdots&&\ddots&\vdots\\\alpha_{q1,t}&\cdots&\alpha_{q,q-1,t}&1\end{pmatrix},\qquad D_t=\mathrm{diag}(\sigma_{1t}^2,\dots,\sigma_{qt}^2),\tag{5}$$

with three independent random walks (slide 42):

$$B_t=B_{t-1}+\nu_t,\ \nu_t\sim N(0,Q);\qquad\alpha_t=\alpha_{t-1}+\xi_t,\ \xi_t\sim N(0,S);\qquad\log\sigma_t=\log\sigma_{t-1}+\eta_t,\ \eta_t\sim N(0,W).\tag{6}$$

**Reading (4)–(5).** Multiply $u_t$ by $A_t$: $\mathrm{Cov}(A_tu_t)=A_t\Sigma_tA_t'=D_t$, diagonal. So
$A_tu_t=D_t^{1/2}\varepsilon_t$ with $\varepsilon_t\sim N(0,I)$: **a recursive SVAR
([[L09-03-structural-var]] §4) whose contemporaneous matrix and shock variances drift over time.**
Ordering still matters, now at every $t$. The decomposition is $\Sigma_t=LGL'$ of Tsay with
$L=A_t^{-1}$, $G=D_t$.

**Why random walks in $\log\sigma$**: positivity for free, and $\log\sigma_{it}^2$ enters linearly once
the model is rewritten (the SV linearisation of Class 8). Each of (6) is a state equation, and
conditional on the other two blocks each block is a linear Gaussian state-space model (or
becomes one after the log-$\chi^2$ mixture approximation for $\log\sigma_t$) — so the Gibbs
sampler draws $B_{1:T}$, $\alpha_{1:T}$ and $\log\sigma_{1:T}$ with the Kalman filter of §4 run
forward and sampled backward.

**Counting states**: $q^2p$ in $B_t$ (plus intercepts), $q(q-1)/2$ in $\alpha_t$, $q$ in $\log\sigma_t$ —
for Primiceri's three US variables (inflation, unemployment, interest rate) with two lags, $21+3+3=27$
states per period (with intercepts). Slide 43 shows the posterior mean and 16/84% bands of the
standard deviations of the residuals of the inflation, unemployment and interest-rate equations:
large peaks in the mid-1970s and around 1980, calm in the 1990s. Slide 44: Nakajima, Kasuya and
Watanabe (2011) apply it to Japan.

---

## 4 · C — state space and the Kalman filter (Tsay §11.1, pp. 558–563)

**The local trend (local level) model** (T eqs. 11.1–11.2):

$$y_t=\mu_t+e_t,\quad e_t\sim N(0,\sigma_e^2);\qquad\mu_{t+1}=\mu_t+\eta_t,\quad\eta_t\sim N(0,\sigma_\eta^2).\tag{7}$$

(7) is the scalar skeleton of (6): an unobserved random walk seen through noise. "Equation (11.1)
provides the link between the data $y_t$ and the state $\mu_t$ and is called the observation
equation ... Equation (11.2) governs the time evolution of the state variable and is the state
equation" (T p. 558).

**Derivation of the filter** (T pp. 561–563). Suppose $\mu_t\mid F_{t-1}\sim N(\mu_{t\mid t-1},\Sigma_{t\mid t-1})$.
The one-step forecast of $y_t$ is $\mu_{t\mid t-1}$, so

$$v_t=y_t-\mu_{t\mid t-1}=(\mu_t-\mu_{t\mid t-1})+e_t,\qquad V_t=\mathrm{Var}(v_t\mid F_{t-1})=\Sigma_{t\mid t-1}+\sigma_e^2,\tag{8}$$

$$\mathrm{Cov}(\mu_t,v_t\mid F_{t-1})=E[(\mu_t-\mu_{t\mid t-1})(\mu_t-\mu_{t\mid t-1}+e_t)\mid F_{t-1}]=\Sigma_{t\mid t-1}\tag{9}$$

(T eq. 11.9; $e_t$ is independent of $\mu_t$). $(\mu_t,v_t)$ is jointly normal given $F_{t-1}$, and
$F_t=\{F_{t-1},v_t\}$. Theorem 11.1 ($E(x\mid y)=\mu_x+\Sigma_{xy}\Sigma_{yy}^{-1}(y-\mu_y)$,
$\mathrm{Var}(x\mid y)=\Sigma_{xx}-\Sigma_{xy}\Sigma_{yy}^{-1}\Sigma_{yx}$) with $x=\mu_t$, $y=v_t$:

$$\mu_{t\mid t}=\mu_{t\mid t-1}+\frac{\Sigma_{t\mid t-1}}{V_t}v_t=\mu_{t\mid t-1}+K_tv_t,\qquad K_t=\frac{\Sigma_{t\mid t-1}}{V_t},\tag{10}$$

$$\Sigma_{t\mid t}=\Sigma_{t\mid t-1}-\frac{\Sigma_{t\mid t-1}^2}{V_t}=\Sigma_{t\mid t-1}(1-K_t).\tag{11}$$

Predict with the state equation: $\mu_{t+1\mid t}=\mu_{t\mid t}$ and

$$\Sigma_{t+1\mid t}=\Sigma_{t\mid t}+\sigma_\eta^2=\Sigma_{t\mid t-1}(1-K_t)+\sigma_\eta^2\tag{12}$$

(T eqs. 11.12–11.14). **$K_t$ is the regression coefficient of the state on the surprise**: the
share of each forecast error that moves the state. The likelihood comes free: $v_t\sim N(0,V_t)$
independently, so $\ln L=-\frac T2\ln2\pi-\frac12\sum_t(\ln V_t+v_t^2/V_t)$ (T eq. 11.25), maximised over
$(\sigma_e,\sigma_\eta)$.

**Note** that (11)–(12) do not involve $y$: the variance and gain path is deterministic.

### 4.1 · The steady state

If $\Sigma_{t\mid t-1}\to P$, then (12) and $K=P/(P+\sigma_e^2)$ give the fixed point

$$P=P\Big(1-\frac{P}{P+\sigma_e^2}\Big)+\sigma_\eta^2=\frac{P\sigma_e^2}{P+\sigma_e^2}+\sigma_\eta^2.$$

Multiply by $P+\sigma_e^2$:

$$P^2+P\sigma_e^2=P\sigma_e^2+\sigma_\eta^2P+\sigma_\eta^2\sigma_e^2\quad\Longrightarrow\quad P^2-\sigma_\eta^2P-\sigma_\eta^2\sigma_e^2=0.$$

Divide by $\sigma_e^4$, write $p=P/\sigma_e^2$ and $q=\sigma_\eta^2/\sigma_e^2$: $p^2-qp-q=0$, positive root

$$p^*=\frac{q+\sqrt{q^2+4q}}2,\qquad K^*=\frac{p^*}{p^*+1}.\tag{13}$$

**Comparative statics.** $q\to0$ (a nearly constant state): $p^*\approx\sqrt q\to0$, $K^*\to0$ — the
filter averages the whole past. $q\to\infty$ (noise-free data): $p^*\approx q$, $K^*\to1$ — the state
is the last observation. $dK^*/dq>0$ throughout.

**The ARIMA link** (T pp. 558–559). In steady state, (10) with $\mu_{t+1\mid t}=\mu_{t\mid t}$ reads

$$\mu_{t+1\mid t}=\mu_{t\mid t-1}+K^*(y_t-\mu_{t\mid t-1})=(1-K^*)\mu_{t\mid t-1}+K^*y_t,\tag{14}$$

exponential smoothing with weight $K^*$, which is the forecast function of
$(1-B)y_t=(1-\theta B)a_t$ with $\theta=1-K^*$ (Tsay: (7) "is also an ARIMA(0,1,1) model ... which is the
simple exponential smoothing model of Chapter 2").

### 4.2 · Worked — Tsay Example 11.1: Alcoa realised volatility (pp. 559–560)

Log daily realised volatility, 340 days. ARIMA fit: $(1-B)y_t=(1-0.858B)a_t$, $\hat\sigma_a=0.5184$
(T eq. 11.6). Local-trend MLEs: $\hat\sigma_\eta=0.0735$, $\hat\sigma_e=0.4803$.

**Route 1 — the filter's steady state, (13):**

$$q=\Big(\frac{0.0735}{0.4803}\Big)^2=0.15303^2=0.023418,$$

$$p^*=\frac{0.023418+\sqrt{0.023418^2+4(0.023418)}}2=\frac{0.023418+\sqrt{0.000548+0.093672}}2=\frac{0.023418+0.306953}2=0.165186,$$

$$K^*=\frac{0.165186}{1.165186}=0.14177,\qquad1-K^*=0.8582.$$

**Route 2 — the ARIMA fit**: $\hat\theta=0.858$. The two agree to the third decimal. Tsay checks the
converse with T eqs. 11.4–11.5 ($\theta\sigma_a^2=\sigma_e^2$, $(1+\theta^2)\sigma_a^2=2\sigma_e^2+\sigma_\eta^2$):
$\sigma_e=\sqrt{0.858(0.5184^2)}=0.4802$ and $\sigma_\eta^2=(1+0.858^2)0.26874-2(0.23058)=0.46658-0.46116=0.00542$,
$\sigma_\eta=0.0736$ — "close to the MLE". **Measurement noise is 6.5 times the state innovation
sd, so only 14% of each day's surprise is believed.**

![Left: steady-state Kalman gain against the signal-to-noise ratio q on a log scale, rising from 0 to 1, with the Alcoa point at q = 0.0234 and gain 0.142; right: the gain path K_t over 40 periods from two initial variances, 10 and 0, both converging to 0.1418](figures/L09-kalman-gain-snr.png)
*Figure — left: $K^*$ from (13) against $q$, with T Ex. 11.1's $q=0.0234$; right: the deterministic gain path (11)–(12) for $\sigma_e=0.4803$, $\sigma_\eta=0.0735$ from $\Sigma_{1\mid0}=10$ and from $0$.*

Left: the gain is an S-curve in $\log q$, steepest around $q\approx1$; Alcoa's volatility sits in the
flat lower part, where the filter is heavily smoothing. Right: from a diffuse start the first
observation gets almost full weight ($K_1=10/10.23=0.98$), from a zero-variance start none
($K_1=0$); both paths reach $0.1418$ within about 15 days — **initialisation matters only at the
start** (T §11.1.6).

---

## 5 · C — time-varying regression coefficients

**TVP-CAPM** (T §11.3.1, pp. 577–578):

$$r_t=\alpha_t+\beta_tr_{M,t}+e_t,\qquad\alpha_{t+1}=\alpha_t+\eta_t,\qquad\beta_{t+1}=\beta_t+\epsilon_t,\tag{15}$$

state $s_t=(\alpha_t,\beta_t)'$, transition $I_2$, observation row $Z_t=(1,r_{M,t})$ — **time-varying
regressors live in the observation matrix**, and the Kalman filter of §4 runs unchanged with
vectors. A TVP-VAR is (15) for each equation with $Z_t$ the VAR's lagged $y$'s: the SUR form
$y_t=z_t\beta_t+u_t$ of [[L09-04-bvar-minnesota-ssvs]] §5 with $\beta_t$ a state.

**Bayesian TVP regression** (G §10.3, pp. 161–164): $y_t=x_t'\beta_t+u_t$, $\beta_t=\beta_{t-1}+\eta_t$,
$u_t\sim N(0,\sigma^2)$, $\eta_t\sim N_K(0,\Omega)$ (G eqs. 10.10–10.11). Iterating the state equation from a
known $\beta_0$:

$$\beta_t=\beta_0+\sum_{s=1}^t\eta_s\quad\Longrightarrow\quad\mathrm{Var}(\beta_t\mid\beta_0)=t\,\Omega,\tag{16}$$

the prior uncertainty about the coefficient **grows linearly with time** — the random-walk
signature of [[../L01/L01-07-ar-var-review|L01 §7]] in parameter space. Greenberg stacks
$\beta=(\beta_T',\dots,\beta_1')'$ and writes the transition as $H\beta=\tilde\beta_0+\eta$, which
gives a Gaussian prior $\beta\sim N(H^{-1}\tilde\beta_0,H^{-1}(I_T\otimes\Omega)H^{-1\prime})$ and a Gibbs
sampler with

$$\beta\mid y,\sigma^2,\Omega\sim N_{TK}(\bar\beta,B_1),\quad B_1=\Big[\frac{X'X}{\sigma^2}+H'(I_T\otimes\Omega^{-1})H\Big]^{-1},\quad\Omega^{-1}\mid\cdot\sim W_K\Big(\alpha_0+T,\Big[S_0^{-1}+\sum_t(\beta_t-\beta_{t-1})(\beta_t-\beta_{t-1})'\Big]^{-1}\Big),\tag{17}$$

"This algorithm must be modified for large $KT$ because $B_1$ is the inverse of a $KT\times KT$
matrix" — hence the recursive (Kalman) sampler. **Greenberg's Phillips-curve example** (Table 10.3):
the TVP model's $\log_{10}$ marginal likelihood is $-92.506$, and "the AR(1) model has a larger
marginal likelihood despite the large variation in the values of $\beta_t$": time variation is not
free — it must earn its extra states.

---

## 6 · C — large TVP-VARs without MCMC (Part 2, slide 61)

Koop and Korobilis (2012): $y_t=z_t\beta_t+u_t$, $u_t\sim N(0,\Sigma)$, $\beta_t=\beta_{t-1}+v_t$,
$v_t\sim N(0,V_t)$, and "the old discount strategy of West and Harrison (1997) to avoid MCMC
altogether". Discounting chooses $V_t$ so that the prediction step inflates the filtered variance
by a fixed factor (G — the standard West–Harrison form):

$$P_{t\mid t-1}=P_{t-1\mid t-1}+V_t\overset{!}{=}\frac{P_{t-1\mid t-1}}{\delta}\quad\Longrightarrow\quad V_t=\Big(\frac1\delta-1\Big)P_{t-1\mid t-1}.\tag{18}$$

No $Q$ to estimate: one number $\delta$ replaces a $K\times K$ matrix. Information $j$ periods old is
down-weighted by about $\delta^j$, an effective memory of $1/(1-\delta)$ observations ($\delta=0.99$:
100 periods; $\delta=1$: constant coefficients). See Ahmadi and Uhlig (2009) for a fully Bayesian
FAVAR alternative (slide 61).

---

## Links

- Neighbours: [[L09-05-factor-models-favar]] · [[L09-07-fsv-dcc-covariances]] (time-varying covariances without a VAR mean).
- Structural link: [[L09-03-structural-var]] §4 ($A_t$ is a drifting recursive $A_0$).
- Class 1: [[../L01/L01-07-ar-var-review|L01 §7]] (random walks: variance $t\sigma^2$).
- Rules: [[../../rules/05_espaco_estados_volatilidade|rules/05]] (state space, TVP).
- **Practice (number and printed page only):** G 10.4 (p. 167).
