---
tags: [notes, lecture-08, time-series, forecasting, mean-reversion, ma, invertibility, arma, psi-weights, identification, acf, pacf]
date: 2026-10-25
status: taught
source: "ar-ma.pdf slides 38–52 (forecasting, 1-, 2-, multistep forecasts, mean reversion, half-life, MA(1) as constrained AR(∞), MA(q), ACF of MA(1) and MA(2), estimation, MA forecasts, summary); ar2-forecast.html (exact h-step forecast distributions of an AR(2) and their Monte Carlo check); Tsay AFTS 3e §2.4.4 pp. 54–57 (Table 2.2), §2.5 pp. 57–64 (eqs. 2.17–2.24, Table 2.3), §2.6 pp. 64–71 (eqs. 2.25–2.34); Wooldridge 6e §11.1 pp. 345–348 (eq. 11.1)"
---

# Tsay §2.4.4–2.6 · Forecasting, MA and ARMA: conditional means, $\psi$ weights, and what the ACF and PACF identify

> **Claim.** **The MSE-optimal forecast is the conditional mean, and its error is the sum of the shocks still to come, weighted by the $\psi$ weights:** $e_h(\ell)=a_{h+\ell}+\psi_1a_{h+\ell-1}+\dots+\psi_{\ell-1}a_{h+1}$, so $V[e_h(\ell)]=\sigma_a^2\sum_{i<\ell}\psi_i^2$ rises to $\gamma_0$ while the point forecast reverts to $\mu$. **For the deck's AR(2) $(1.75,-0.80)$ the forecast sd goes 1, 2.02, 3.03, 3.97, … → 7.12.** **An MA(q) is a finite-memory model: always stationary, its ACF cuts off after lag $q$, its forecasts hit the mean after $q$ steps, and it is identified only up to invertibility ($|\rho_1|\le\frac12$ for an MA(1)).** **An ARMA(1,1) has the AR(1)'s stationarity condition and an AR(1)-like ACF that starts decaying one lag late; neither its ACF nor its PACF cuts off.**
> Prev: [[L08-01-ar2-arp-cycles-identification]] · Next: [[L08-03-unit-roots-dickey-fuller]] · Map: [[L08-00-map]]

**Notation.**

| Symbol | Meaning | Range |
|---|---|---|
| $h$, $\ell$ | forecast origin, forecast horizon | $\ell\ge1$ |
| $F_h$ | information available at $h$ (inclusive) | |
| $\hat r_h(\ell)$ | $\ell$-step-ahead forecast at origin $h$ | |
| $e_h(\ell)=r_{h+\ell}-\hat r_h(\ell)$ | forecast error | |
| $\phi_i$, $\theta_j$ | AR and MA coefficients, **Tsay's sign**: $r_t=c_0+a_t-\theta_1a_{t-1}-\dots$ | |
| $c_0$ | MA constant ($=E(r_t)$) | |
| $\psi_i$ | MA($\infty$) weights / impulse response, $\psi_0=1$ | |
| $\pi_i$ | AR($\infty$) weights | |
| $\phi(B)$, $\theta(B)$ | AR and MA polynomials $1-\sum\phi_iB^i$, $1-\sum\theta_jB^j$ | |
| $y_n, y_{n-1}$ | last two observations on ar2-forecast.html | |

**Sign convention.** Tsay writes the MA part with minus signs, $r_t=c_0+a_t-\theta_1a_{t-1}$. R's `arima`, statsmodels and Wooldridge (11.1) write plus signs, $r_t=c_0+a_t+\theta_1a_{t-1}$. A printed R/statsmodels `ma1 = -0.39` is Tsay's $\theta_1=0.39$. Every formula below uses Tsay's sign.

---

## 1 · C — the forecast is the conditional mean (slide 38; T p. 54)

The forecast minimises expected squared error given $F_h$ over functions $g$ of $F_h$:

$$E\{[r_{h+\ell}-\hat r_h(\ell)]^2\mid F_h\}\le\min_gE[(r_{h+\ell}-g)^2\mid F_h].\tag{1}$$

For any $g\in F_h$, adding and subtracting $m=E(r_{h+\ell}\mid F_h)$, the cross term has conditional mean zero:

$$E[(r_{h+\ell}-g)^2\mid F_h]=V(r_{h+\ell}\mid F_h)+(m-g)^2,$$

minimised at $g=m$. Hence

$$\hat r_h(\ell)=E(r_{h+\ell}\mid F_h).\tag{2}$$

Forecasts with *estimated* parameters are conditional forecasts: they ignore parameter uncertainty, which Bayesian forecasting by MCMC would include (T p. 55; Classes 3+4, [[L08-09-bayesian-garch]]).

---

## 2 · C — AR(p) forecasts and mean reversion (slides 39–42; T pp. 54–56)

**One step.** From $r_{h+1}=\phi_0+\sum_{i=1}^p\phi_ir_{h+1-i}+a_{h+1}$ and (2), every $r$ on the right is in $F_h$ and $E(a_{h+1}\mid F_h)=0$:

$$\hat r_h(1)=\phi_0+\sum_{i=1}^p\phi_ir_{h+1-i},\qquad e_h(1)=a_{h+1},\qquad V[e_h(1)]=\sigma_a^2.\tag{3}$$

With normal shocks the 95% interval is $\hat r_h(1)\pm1.96\sigma_a$.

**Two steps.** $r_{h+2}=\phi_0+\phi_1r_{h+1}+\phi_2r_h+\dots+a_{h+2}$; replace the unknown $r_{h+1}$ by its forecast:

$$\hat r_h(2)=\phi_0+\phi_1\hat r_h(1)+\phi_2r_h+\dots+\phi_pr_{h+2-p}.\tag{4}$$

Subtract (4) from the model:

$$e_h(2)=\phi_1\big[r_{h+1}-\hat r_h(1)\big]+a_{h+2}=a_{h+2}+\phi_1a_{h+1},\qquad V[e_h(2)]=(1+\phi_1^2)\sigma_a^2\ge V[e_h(1)].\tag{5}$$

**$\ell$ steps** (T p. 56): recursively,

$$\hat r_h(\ell)=\phi_0+\sum_{i=1}^p\phi_i\hat r_h(\ell-i),\qquad\hat r_h(i)=r_{h+i}\ \text{if } i\le0.\tag{6}$$

The point forecasts obey the deterministic part of the model — the same difference equation as the ACF ([[L08-01-ar2-arp-cycles-identification]] (6), (22)). **Mean reversion:** for a stationary AR(p), $\hat r_h(\ell)\to E(r_t)$ and $V[e_h(\ell)]\to V(r_t)$ as $\ell\to\infty$. For an AR(1), $\hat x_h(\ell)=\phi_1^\ell x_h$ for the mean-adjusted series, and the half-life is $\ell=\ln0.5/\ln|\phi_1|$ (L01-07 (17)).

**Worked — Tsay Table 2.2 (p. 57).** AR(3) for CRSP value-weighted returns re-estimated on 984 months, $r_t=0.0098+0.1024r_{t-1}-0.0201r_{t-2}-0.1090r_{t-3}+a_t$, $\hat\sigma_a=0.054$. Forecasts at origin December 2007: 0.0076, 0.0161, 0.0118, 0.0099, 0.0089, 0.0093, then 0.0095–0.0097; standard errors 0.0534, 0.0537, 0.0537, then 0.0540 from step 4. The subsample mean and sd are 0.0095 and 0.0540: weak dependence means **reversion within a few months**. Only October 2008 (−0.1847) leaves the 95% band.

---

## 3 · C — worked: exact h-step forecast distributions of an AR(2) (ar2-forecast.html §§1–4)

Model $y_t=\phi_1y_{t-1}+\phi_2y_{t-2}+\epsilon_t$, $\epsilon_t\sim N(0,\sigma^2)$, $\theta=(\phi_1,\phi_2,\sigma)=(1.75,-0.80,1)$; 300 observations simulated with `set.seed(1233)` after a 300-draw burn-in; last two values $y_n=-5.487150$, $y_{n-1}=-3.508837$.

**$h=1$.** By (3) with $\phi_0=0$:

$$E(y_{n+1}\mid y_{1:n},\theta)=\phi_1y_n+\phi_2y_{n-1},\qquad V=\sigma^2.\tag{7}$$

**$h=2$.** Substitute the model for $y_{n+1}$ into $y_{n+2}=\phi_1y_{n+1}+\phi_2y_n+\epsilon_{n+2}$:

$$y_{n+2}=\phi_1\big(\phi_1y_n+\phi_2y_{n-1}+\epsilon_{n+1}\big)+\phi_2y_n+\epsilon_{n+2}$$

$$y_{n+2}=(\phi_1^2+\phi_2)y_n+\phi_1\phi_2y_{n-1}+\phi_1\epsilon_{n+1}+\epsilon_{n+2},\tag{8}$$

so $E=(\phi_1^2+\phi_2)y_n+\phi_1\phi_2y_{n-1}$ and $V=(1+\phi_1^2)\sigma^2$.

**$h=3$.** Substitute (8) and $y_{n+1}$ into $y_{n+3}=\phi_1y_{n+2}+\phi_2y_{n+1}+\epsilon_{n+3}$ and collect:

$$E(y_{n+3}\mid\cdot)=(\phi_1^3+2\phi_1\phi_2)y_n+(\phi_1^2\phi_2+\phi_2^2)y_{n-1},\qquad V=\big[1+\phi_1^2+(\phi_1^2+\phi_2)^2\big]\sigma^2.\tag{9}$$

**$h=4$.** One more substitution:

$$E(y_{n+4}\mid\cdot)=(\phi_1^4+3\phi_1^2\phi_2+\phi_2^2)y_n+(\phi_1^3\phi_2+2\phi_1\phi_2^2)y_{n-1},\quad V=\big[1+\phi_1^2+(\phi_1^2+\phi_2)^2+(\phi_1^3+2\phi_1\phi_2)^2\big]\sigma^2.\tag{10}$$

(The page labels these $h=4$ lines "$E(y_{n+3}\ldots)$" and prints "$2\phi\phi_2^2$" for $2\phi_1\phi_2^2$; its R code is right.) The coefficients on $y_n$ are the $\psi$ weights $\psi_1=\phi_1$, $\psi_2=\phi_1^2+\phi_2$, $\psi_3=\phi_1^3+2\phi_1\phi_2$, $\psi_4=\phi_1^4+3\phi_1^2\phi_2+\phi_2^2$, generated by $\psi_j=\phi_1\psi_{j-1}+\phi_2\psi_{j-2}$; **the variances are $\sigma^2\sum_{j<h}\psi_j^2$**, which is (21) below.

**Numbers** ($\phi_1=1.75$, $\phi_2=-0.80$, $\sigma=1$):

| $h$ | $\psi$ coefficients | $E(y_{n+h}\mid y_{1:n})$ | $V$ |
|---|---|---|---|
| 1 | $1.75$; $-0.80$ | $1.75(-5.487150)+(-0.80)(-3.508837)=-9.602513+2.807070=$ **−6.7954** | 1 |
| 2 | $3.0625-0.80=2.2625$; $1.75(-0.80)=-1.40$ | $2.2625(-5.487150)+(-1.40)(-3.508837)=-12.414677+4.912372=$ **−7.5023** | $1+1.75^2=$ **4.0625** |
| 3 | $5.359375-2.80=2.559375$; $-2.45+0.64=-1.81$ | $2.559375(-5.487150)+(-1.81)(-3.508837)=-14.043677+6.350995=$ **−7.6927** | $4.0625+2.2625^2=$ **9.1814** |
| 4 | $9.378906-7.35+0.64=2.668906$; $-4.2875+2.24=-2.0475$ | $2.668906(-5.487150)+(-2.0475)(-3.508837)=-14.644688+7.184344=$ **−7.4603** | $9.1814+2.559375^2=$ **15.7318** |

The mean keeps *falling* for three steps before turning: the model's momentum ($\psi_j$ rising to 2.67) outweighs reversion at first. All four distributions are normal because each $y_{n+h}$ is a fixed number plus a linear combination of iid normal shocks.

**The limit.** The AR(2) is stationary ([[L08-01-ar2-arp-cycles-identification]] §5), so $E\to0$ and $V\to\gamma_0=50.704$ by [[L08-01-ar2-arp-cycles-identification]] (9): limiting sd **7.12069**. After 50 steps the exact sd is already 7.1206.

**Monte Carlo check (page §4).** $M=10\,000$ paths simulated 50 steps forward from $(y_{n-1},y_n)$: at $h=50$ the sample mean is **0.0297** and sd **7.1259**, against 0 and 7.1207; the MC histograms at $h=1,\dots,4$ sit on the exact normals (7)–(10). The 5%, 50%, 95% quantile lines converge to $0\pm1.645\times7.12069=\pm11.71$.

![AR(2) forecast fan for phi = (1.75, -0.80): starting from y_{n-1} = -3.51 and y_n = -5.49, the forecast mean dips to about -7.7 at h = 3, then rises past zero in a long damped wave; the 5 to 95 percent band widens quickly over the first ten steps and settles between the horizontal stationary limits plus and minus 11.71](figures/L08-ar2-forecast-fan.png)
*Figure — exact mean recursion (6) and band $E\pm1.645\sigma\big(\sum_{j<h}\psi_j^2\big)^{1/2}$ for ar2-forecast.html's model and origin; dotted lines: $\pm1.645\sqrt{\gamma_0}$.*

The mean overshoots zero and returns — the complex roots' 30-period cycle seen in the forecasts rather than in the ACF. The band reaches its stationary width within about 15 steps: by then the forecast carries no information beyond the unconditional distribution.

> **Interactive companion.** [The AR(2) Triangle](companions/companion-ar2-dynamics.html) — set $y_n$, $y_{n-1}$ and the horizon $H$, then move $\phi_1,\phi_2$ toward an edge of the triangle: the band stops converging (unit root) or the mean explodes; the read-outs reproduce the table above at the defaults.

---

## 4 · C — MA(1) as a constrained AR(∞), and MA(q) (slides 43–46; T eqs. 2.17–2.22, pp. 57–59)

An AR of infinite order, $r_t=\phi_0+\phi_1r_{t-1}+\phi_2r_{t-2}+\dots+a_t$, has too many parameters. Constrain them to one, $\phi_i=-\theta_1^i$ (T 2.17):

$$r_t=\phi_0-\theta_1r_{t-1}-\theta_1^2r_{t-2}-\theta_1^3r_{t-3}-\dots+a_t,\tag{11}$$

stationary only if $|\theta_1|<1$. Rewrite (11) and lag it one period (T 2.18–2.19):

$$r_t+\theta_1r_{t-1}+\theta_1^2r_{t-2}+\dots=\phi_0+a_t,\tag{12}$$

$$r_{t-1}+\theta_1r_{t-2}+\theta_1^2r_{t-3}+\dots=\phi_0+a_{t-1}.\tag{13}$$

Multiply (13) by $\theta_1$ and subtract it from (12): every $r_{t-j}$, $j\ge1$, cancels:

$$r_t=\phi_0(1-\theta_1)+a_t-\theta_1a_{t-1}.\tag{14}$$

That is the **MA(1)**, $r_t=c_0+(1-\theta_1B)a_t$ (T 2.20); in general (T 2.22)

$$r_t=c_0+a_t-\theta_1a_{t-1}-\dots-\theta_qa_{t-q}=c_0+(1-\theta_1B-\dots-\theta_qB^q)a_t.\tag{15}$$

**Moments.** A finite linear combination of white noise has time-invariant first two moments, so **every MA(q) is weakly stationary** (no condition on the $\theta$'s), with

$$E(r_t)=c_0,\qquad V(r_t)=(1+\theta_1^2+\dots+\theta_q^2)\sigma_a^2.\tag{16}$$

Wooldridge's example of a weakly dependent but correlated series is the MA(1) $x_t=e_t+\alpha_1e_{t-1}$ (W (11.1), §11.1b): observations two or more periods apart are independent, so the LLN and CLT apply.

---

## 5 · C — ACF of MA models, the $\frac12$ bound, invertibility (slides 47–48; T pp. 59–60)

**MA(1)**, $c_0=0$. Multiply $r_t=a_t-\theta_1a_{t-1}$ by $r_{t-\ell}$ and take expectations:

$$\gamma_1=E[(a_{t-1}-\theta_1a_{t-2})(a_t-\theta_1a_{t-1})]=-\theta_1\sigma_a^2,\qquad\gamma_\ell=0\ (\ell>1).$$

Divide by $\gamma_0=(1+\theta_1^2)\sigma_a^2$ from (16):

$$\rho_1=\frac{-\theta_1}{1+\theta_1^2},\qquad\rho_\ell=0\ \ (\ell>1).\tag{17}$$

**MA(2)**: $\gamma_1=E[(a_{t-1}-\theta_1a_{t-2}-\theta_2a_{t-3})(a_t-\theta_1a_{t-1}-\theta_2a_{t-2})]=(-\theta_1+\theta_1\theta_2)\sigma_a^2$ and $\gamma_2=-\theta_2\sigma_a^2$, so

$$\rho_1=\frac{-\theta_1+\theta_1\theta_2}{1+\theta_1^2+\theta_2^2},\qquad\rho_2=\frac{-\theta_2}{1+\theta_1^2+\theta_2^2},\qquad\rho_\ell=0\ \ (\ell>2).\tag{18}$$

> **The ACF of an MA(q) cuts off after lag $q$**: a "finite-memory" model, linearly related only to its first $q$ lags.

**The $\frac12$ bound.** Since $1+\theta_1^2\ge2|\theta_1|$, (17) gives $|\rho_1|\le\frac12$, with equality at $\theta_1=\pm1$. A sample lag-1 autocorrelation of 0.7 with nothing beyond is not an MA(1).

**Invertibility.** (17) is unchanged when $\theta_1\to1/\theta_1$: $\theta_1=0.5$ and $\theta_1=2$ both give $\rho_1=-0.5/1.25=-2/2.5=-0.4$. To pick one, write $a_t=r_t+\theta_1a_{t-1}$ and substitute repeatedly:

$$a_t=r_t+\theta_1r_{t-1}+\theta_1^2r_{t-2}+\theta_1^3r_{t-3}+\dots\tag{19}$$

The present shock depends less on remote returns only if $|\theta_1|<1$: the **invertible** MA(1) (T p. 60). $|\theta_1|=1$ is noninvertible.

**Worked.** $\theta_1=0.6$ (the figure's MA(1)): $\rho_1=-0.6/1.36=-0.4412$, all higher ACFs zero.

---

## 6 · C/G — estimation (slide 49; T pp. 61–62)

MLE, with the first shocks handled two ways. **Conditional likelihood**: set $a_t=0$ for $t\le0$, then $a_1=r_1-c_0$, $a_2=r_2-c_0+\theta_1a_1$, … recursively, and the likelihood is a product of normal densities of these $a_t$. **Exact likelihood** (G): treat the initial shocks as extra parameters (or integrate them out). Preferred near noninvertibility ($|\theta_1|\to1$), where the conditional recursion forgets its start slowly; the two coincide in large samples.

**Worked — Tsay's MA(9), CRSP equal-weighted monthly returns 1926–2008.** The sample ACF is significant at lags 1, 3, 9 (MA lags are identified from the ACF). Conditional MLE (T 2.23): $r_t=0.012+a_t+0.189a_{t-1}-0.121a_{t-3}+0.122a_{t-9}$, $\hat\sigma_a=0.0714$ (printed in the plus-sign form). Residual $Q(12)=17.5$: $p=0.041$ on $12-3=9$ df, 0.132 on 12. Exact MLE (T 2.24): $0.191$, $-0.120$, $0.123$, same $\hat\sigma_a$ — negligible difference here.

---

## 7 · C — MA forecasts (slides 50–51; T pp. 62–63)

**MA(1).** $r_{h+1}=c_0+a_{h+1}-\theta_1a_h$, and $a_h\in F_h$ (the residual, or by (19)):

$$\hat r_h(1)=c_0-\theta_1a_h,\quad e_h(1)=a_{h+1};\qquad\hat r_h(2)=c_0,\quad e_h(2)=a_{h+2}-\theta_1a_{h+1},\quad V[e_h(2)]=(1+\theta_1^2)\sigma_a^2.\tag{20}$$

So $\hat r_h(\ell)=c_0$ for all $\ell\ge2$ and the 2-step error variance is already $V(r_t)$: **mean reversion takes one period.** **MA(2):** $\hat r_h(1)=c_0-\theta_1a_h-\theta_2a_{h-1}$, $\hat r_h(2)=c_0-\theta_2a_h$, $\hat r_h(\ell)=c_0$ for $\ell>2$. In general an MA(q) forecast reaches the mean after $q$ steps.

**Worked — Tsay Table 2.3 (p. 63).** The MA(9) re-estimated on 986 months: the 10-step forecast is **0.0128**, the subsample mean; forecast standard errors 0.0712 → 0.0729 → 0.0734, approaching the subsample sd 0.0736.

---

## 8 · C — ARMA(1,1) and the identification table (T §2.6.1–2.6.2, pp. 64–66; slide 52)

$$r_t-\phi_1r_{t-1}=\phi_0+a_t-\theta_1a_{t-1},\qquad\phi_1\ne\theta_1\tag{21}$$

(T 2.25; with $\phi_1=\theta_1$ the factors cancel and $r_t$ is white noise). **Mean:** $E(r_t)=\phi_0/(1-\phi_1)$, as for the AR(1). Set $\phi_0=0$. Multiplying (21) by $a_t$ (T 2.26):

$$E(r_ta_t)=E(a_t^2)-\theta_1E(a_ta_{t-1})=\sigma_a^2.\tag{22}$$

**Variance.** Take the variance of $r_t=\phi_1r_{t-1}+a_t-\theta_1a_{t-1}$; $r_{t-1}$ is uncorrelated with $a_t$, and $\mathrm{Cov}(r_{t-1},a_{t-1})=\sigma_a^2$ by (22) at $t-1$:

$$V(r_t)=\phi_1^2V(r_{t-1})+\sigma_a^2+\theta_1^2\sigma_a^2-2\phi_1\theta_1\sigma_a^2.$$

Under stationarity $V(r_t)=V(r_{t-1})=\gamma_0$:

$$\gamma_0=\frac{(1-2\phi_1\theta_1+\theta_1^2)\,\sigma_a^2}{1-\phi_1^2},\tag{23}$$

positive only if $\phi_1^2<1$: **the AR(1) stationarity condition**, unaffected by the MA part.

**Autocovariances.** Multiply (21) by $r_{t-\ell}$ and take expectations. At $\ell=1$, $E(a_tr_{t-1})=0$ and $E(a_{t-1}r_{t-1})=\sigma_a^2$:

$$\gamma_1-\phi_1\gamma_0=-\theta_1\sigma_a^2;\qquad\gamma_\ell-\phi_1\gamma_{\ell-1}=0,\ \ \ell>1\ \ \text{(T 2.27)}.\tag{24}$$

Divide by $\gamma_0$ and substitute $\sigma_a^2/\gamma_0$ from (23):

$$\rho_1=\phi_1-\frac{\theta_1\sigma_a^2}{\gamma_0}=\phi_1-\frac{\theta_1(1-\phi_1^2)}{1-2\phi_1\theta_1+\theta_1^2},\qquad\rho_\ell=\phi_1\rho_{\ell-1}\ \ (\ell>1).\tag{25}$$

**Worked, $(\phi_1,\theta_1)=(0.8,0.4)$.** $1-2(0.8)(0.4)+0.4^2=1-0.64+0.16=0.52$; $\gamma_0=0.52/(1-0.64)=0.52/0.36=1.4444\,\sigma_a^2$; $\rho_1=0.8-\frac{0.4(0.36)}{0.52}=0.8-0.2769=$ **0.5231**; $\rho_2=0.8(0.5231)=0.4185$. Compared with an AR(1) with $\phi_1=0.8$ ($\rho_1=0.8$): lower start, same decay rate from lag 2.

**General ARMA(p, q)** (T 2.28): $\phi(B)r_t=\phi_0+\theta(B)a_t$, with no common factors; weakly stationary iff all characteristic roots of $\phi(B)$ are inside the unit circle; mean $\phi_0/(1-\phi_1-\dots-\phi_p)$. ACF and PACF are not informative about $(p,q)$; Tsay uses the EACF ([[L08-01-ar2-arp-cycles-identification]] §12) or AIC/BIC over a grid. Residual $Q(m)$ has $m-g$ df, $g$ = number of AR+MA coefficients (T p. 68).

![Two rows of four bar plots, lags 1 to 12. Top row ACF, bottom row PACF, for AR(1) with phi 0.8, AR(2) with (0.6, -0.4), MA(1) with theta 0.6, and ARMA(1,1) with (0.8, 0.4). The AR(1) ACF decays geometrically and its PACF is a single spike of 0.8; the AR(2) ACF is a damped wave and its PACF has two spikes, 0.43 and -0.40; the MA(1) ACF is a single spike of -0.44 and its PACF is all negative and shrinks geometrically; the ARMA(1,1) ACF starts at 0.52 and decays geometrically while its PACF also decays](figures/L08-identification-acf-pacf.png)
*Figure — exact ACF (from the $\psi$ weights, L01-07 (4)) and PACF (Durbin–Levinson on that ACF) for four models; Tsay's MA sign.*

Read the columns as the identification table (slide 52; T pp. 63, 66):

| Model | ACF | PACF |
|---|---|---|
| AR(p) | tails off (decays, waves if complex roots) | **cuts off after lag $p$** |
| MA(q) | **cuts off after lag $q$** | tails off |
| ARMA(p, q) | tails off from lag $q$ | tails off from lag $p$ |

The AR(2) PACF is exactly $\rho_1=0.6/1.4=0.4286$ then $\phi_2=-0.4$ then zeros; the MA(1)'s single ACF spike is −0.4412 from (17); the ARMA(1,1) shows 0.5231 and then the 0.8 decay of (25), with a PACF that never stops.

---

## 9 · C — three representations; the forecast-error variance (T §2.6.5, pp. 69–71)

By long division of the two polynomials (T 2.29–2.30):

$$\frac{\theta(B)}{\phi(B)}=1+\psi_1B+\psi_2B^2+\dots\equiv\psi(B),\qquad\frac{\phi(B)}{\theta(B)}=1-\pi_1B-\pi_2B^2-\dots\equiv\pi(B).\tag{26}$$

For ARMA(1,1): $\psi_i=\phi_1^{i-1}(\phi_1-\theta_1)$ and $\pi_i=\theta_1^{i-1}(\phi_1-\theta_1)$, $i\ge1$; with $(0.8,0.4)$, $\psi=1,0.4,0.32,0.256,\dots$

**AR representation** (T 2.31): $r_t=\frac{\phi_0}{1-\theta_1-\dots-\theta_q}+\pi_1r_{t-1}+\pi_2r_{t-2}+\dots+a_t$. **Invertible** iff $\pi_i\to0$; sufficient: all zeros of $\theta(B)$ outside the unit circle (MA(1): $|\theta_1|<1$, as in (19)).

**MA representation** (T 2.32): $r_t=\mu+a_t+\psi_1a_{t-1}+\psi_2a_{t-2}+\dots$, the $\psi_i$ being the **impulse response** of the series to a shock. At origin $h$ the shocks $a_h,a_{h-1},\dots$ are known, so (T 2.33)

$$\hat r_h(\ell)=\mu+\psi_\ell a_h+\psi_{\ell+1}a_{h-1}+\dots,\qquad e_h(\ell)=a_{h+\ell}+\psi_1a_{h+\ell-1}+\dots+\psi_{\ell-1}a_{h+1},\tag{27}$$

$$\boxed{\;V[e_h(\ell)]=\big(1+\psi_1^2+\dots+\psi_{\ell-1}^2\big)\sigma_a^2\;}\quad\text{(T 2.34)}\tag{28}$$

non-decreasing in $\ell$. **Mean reversion, proved:** stationarity means $\psi_i\to0$, so by (27) $\hat r_h(\ell)\to\mu$, and by (28) $V[e_h(\ell)]\to(1+\sum_{i\ge1}\psi_i^2)\sigma_a^2=V(r_t)$ (L01-07 (4)). The ar2-forecast variances of §3 are (28) with the AR(2) $\psi$'s; for an MA(q), $\psi_i=-\theta_i$ up to $q$ and 0 after, which is (20).

> **The $\psi$ weights do three jobs:** they give the ACF (L01-07 (4)), the impulse response, and the forecast-error variance (28). A unit root makes them stop decaying — the subject of [[L08-03-unit-roots-dickey-fuller]].

---

## 10 · U — summary of slide 52

MA: order from the ACF, always stationary. AR: order from the PACF, stationary iff all characteristic roots are inside the unit circle. Stationary series: forecasts converge to the mean, forecast-error variances to the variance. "Carefully read Section 2.6 of Tsay (2010) about ARMA models" — §§8–9 above.

---

## Links

- Neighbours: [[L08-01-ar2-arp-cycles-identification]] (Yule–Walker, triangle, PACF, AIC/BIC) · [[L08-03-unit-roots-dickey-fuller]] ($\psi_i=1$ for all $i$).
- Unit: [[L08-00-map]] · [[L08-10-formulas]] · [[L08-11-pitfalls]] · [[L08-12-python]] · [[L08-06-arch-garch]] (GARCH as an ARMA for $a_t^2$).
- Class 1: [[../L01/L01-07-ar-var-review|L01-07]] (linear series, AR(1), half-life). Class 9 (plain forward link): the VAR's MA representation and impulse responses generalise (26)–(28) to matrices.
- Rules: [[../../rules/04_arima_raiz_unitaria|rules/04]].
- **Practice (number and printed page only; statements in Tsay):** T 2.1 (p. 104), T 2.2 (p. 104), T 2.3 (p. 104), T 2.4 (p. 105). Full solutions are being built at `Listas/lista-L08-book-exercises.pdf`.
