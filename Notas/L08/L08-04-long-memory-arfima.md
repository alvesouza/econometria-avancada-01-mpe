---
tags: [notes, lecture-08, time-series, long-memory, arfima, fractional-differencing, hurst]
date: 2026-10-25
status: taught
source: "unitroot.pdf slides 32–38 (long-memory models, history, properties 1–5, ARFIMA, Bayesian ARFIMA references); Tsay AFTS 3e §2.11 pp. 101–103 (eqs. 2.52–2.53, properties 1–5, Figure 2.22), §3.13 p. 154 (LMSV, eq. 3.41)"
---

# §2.11 · Long memory — an ACF that decays like a power of the lag, between ARMA and the unit root

> **Claim.** **The fractionally differenced process $(1-B)^dx_t=a_t$ with $-0.5<d<0.5$ is stationary, yet its autocorrelations decay hyperbolically, $\rho_k\sim c\,k^{2d-1}$, instead of geometrically like every stationary ARMA.** Its whole ACF follows from one ratio, $\rho_k/\rho_{k-1}=(k-1+d)/(k-d)$, starting at $\rho_1=d/(1-d)$. With $d=0.4$ the correlation at lag 100 is still 0.27, where an AR(1) with the same $\rho_1$ has $10^{-18}$. **Long memory sits between the two cases of [[L08-03-unit-roots-dickey-fuller]]:** shocks fade (unlike a random walk) but slowly (unlike ARMA). Absolute returns are the financial example.
> Prev: [[L08-03-unit-roots-dickey-fuller]] · Next: [[L08-05-seasonal-airline-model]] · Map: [[L08-00-map]]

**Notation.**

| Symbol | Meaning | Range |
|---|---|---|
| $x_t$ | the series | |
| $a_t$ | white noise, variance $\sigma_a^2$ | |
| $d$ | fractional differencing parameter | $-0.5<d<0.5$ |
| $B$ | back-shift operator, $Bx_t=x_{t-1}$ | |
| $\binom dk$ | generalised binomial coefficient $d(d-1)\cdots(d-k+1)/k!$ | |
| $\psi_k$, $\pi_k$ | MA($\infty$) and AR($\infty$) weights | |
| $\rho_k$, $\phi_{k,k}$ | ACF and PACF at lag $k$ | |
| $f(\omega)$ | spectral density at frequency $\omega\in[0,2\pi]$ | |
| $x!=\Gamma(x+1)$ | factorial of a non-integer, through the gamma function | |

---

## 1 · U — where long memory comes from (slides 33–34)

The idea began in hydrology: Hurst (1951) found that the rescaled range of the Nile's levels grew "anomalously fast". Mandelbrot showed that, if stationarity is kept, new mathematics is needed to explain the Hurst effect, and defined long memory (Mandelbrot and Van Ness 1968; Mandelbrot and Wallis 1968). The slides cite Palma (2007) and Beran et al. (2013) for the theory.

The empirical signature (T p. 102): a sample ACF that is **not large but decays very slowly**. In Tsay's Figure 2.22 the ACF of *absolute* daily returns of the CRSP value- and equal-weighted indexes, 1970–2008, is small yet still significant at the 5% level after 300 lags, while the returns themselves are nearly uncorrelated. Ding, Granger and Engle (1993) documented the same for $|r_t|$; it is the reason long-memory volatility models exist (§6).

---

## 2 · C — fractional differencing: the operator (slide 32; T eq. 2.52, p. 101; binomial expansion p. 102)

$$(1-B)^dx_t=a_t,\qquad -0.5<d<0.5.\tag{1}$$

For non-integer $d$ the operator is defined by the binomial series (T p. 102):

$$(1-B)^d=\sum_{k=0}^\infty\binom dk(-B)^k=\sum_{k=0}^\infty(-1)^k\frac{d(d-1)\cdots(d-k+1)}{k!}B^k.\tag{2}$$

**The first terms, one at a time.**

$k=0$: $\ 1$.

$k=1$: $\ (-1)^1\dfrac{d}{1!}B=-dB$.

$k=2$: $\ (-1)^2\dfrac{d(d-1)}{2!}B^2=\dfrac{d(d-1)}{2}B^2=-\dfrac{d(1-d)}{2}B^2$.

$k=3$: $\ (-1)^3\dfrac{d(d-1)(d-2)}{3!}B^3=-\dfrac{d(1-d)(2-d)}{6}B^3$, using $(d-1)(d-2)=(1-d)(2-d)$.

So

$$(1-B)^d=1-dB-\frac{d(1-d)}{2}B^2-\frac{d(1-d)(2-d)}{6}B^3-\cdots\tag{3}$$

For $d=1$ the series stops after two terms and (3) is the ordinary difference $1-B$; for $0<d<1$ **every** past value enters, with slowly shrinking weights. That is the source of the long memory.

---

## 3 · C — the two representations (slide 35; T properties 1–2, p. 101)

**Property 1 (MA form).** If $d<0.5$, $x_t$ is weakly stationary and

$$x_t=a_t+\sum_{k=1}^\infty\psi_ka_{t-k},\qquad \psi_k=\frac{d(1+d)\cdots(k-1+d)}{k!}=\frac{(k+d-1)!}{k!\,(d-1)!}.\tag{4}$$

These are the coefficients of $(1-B)^{-d}$, the inverse of (2): $\psi_1=d$, $\psi_2=d(1+d)/2$. For $d=0.25$: $\psi_1=0.25$, $\psi_2=0.25\times1.25/2=0.156$.

**Property 2 (AR form).** If $d>-0.5$, $x_t$ is invertible. The coefficients of (2) are, written as products,

$$\pi_k=(-1)^k\binom dk=\frac{-d(1-d)\cdots(k-1-d)}{k!}=\frac{(k-d-1)!}{k!\,(-d-1)!},\qquad \pi_0=1,\tag{5}$$

(Tsay's $\pi_k$, p. 101), so that (1) reads $\sum_{k\ge0}\pi_kx_{t-k}=a_t$, i.e.

$$x_t=a_t-\sum_{k=1}^\infty\pi_kx_{t-k}=a_t+d\,x_{t-1}+\frac{d(1-d)}{2}x_{t-2}+\cdots\tag{6}$$

using $\pi_1=-d$ and $\pi_2=-d(1-d)/2$ from (3). (Check of the factorial form at $k=1$: $(-d)!/(-d-1)!=\Gamma(1-d)/\Gamma(-d)=-d$.)

**Range of $d$.** $\sum\psi_k^2<\infty$ (finite variance) needs $d<0.5$; $\sum\pi_k^2<\infty$ needs $d>-0.5$. Both hold on $(-0.5,0.5)$, the range in (1).

---

## 4 · C — the ACF, PACF and spectrum (slides 36–37; T properties 3–5, p. 102)

**Property 3 (ACF).** For $-0.5<d<0.5$,

$$\rho_k=\frac{d(1+d)\cdots(k-1+d)}{(1-d)(2-d)\cdots(k-d)},\qquad k=1,2,\dots\tag{7}$$

(The slide prints the last denominator factor as "$(k=d)$"; it is $(k-d)$.) Two consequences, each read straight off (7):

$k=1$, one factor above and below:

$$\rho_1=\frac{d}{1-d}.\tag{8}$$

Dividing (7) at $k$ by (7) at $k-1$, all factors but the last cancel:

$$\frac{\rho_k}{\rho_{k-1}}=\frac{k-1+d}{k-d}.\tag{9}$$

**Asymptotics.** Write the products in (7) with gamma functions, $d(1+d)\cdots(k-1+d)=\Gamma(k+d)/\Gamma(d)$ and $(1-d)\cdots(k-d)=\Gamma(k+1-d)/\Gamma(1-d)$:

$$\rho_k=\frac{\Gamma(1-d)}{\Gamma(d)}\cdot\frac{\Gamma(k+d)}{\Gamma(k+1-d)}.\tag{10}$$

**G — the ratio of gamma functions.** For large $k$, $\Gamma(k+a)/\Gamma(k+b)\approx k^{a-b}$ (Stirling). With $a=d$, $b=1-d$, $a-b=2d-1$:

$$\rho_k\approx\frac{(-d)!}{(d-1)!}\,k^{2d-1}\qquad(k\to\infty),\tag{11}$$

since $\Gamma(1-d)=(-d)!$ and $\Gamma(d)=(d-1)!$. **This is the definition of long memory: polynomial decay, $\log\rho_k\approx\text{const}+(2d-1)\log k$.** For $0<d<0.5$ the exponent lies in $(-1,0)$, so $\sum_k\rho_k$ diverges even though $\rho_k\to0$.

**Property 4 (PACF):** $\phi_{k,k}=d/(k-d)$. At $k=1$ it equals (8), as any PACF must; then it decays like $1/k$: it does not cut off, so neither the ACF nor the PACF identifies an ARFIMA by a cut-off (compare [[L08-02-forecasting-ma-arma]]).

**Property 5 (spectrum, named):** $f(\omega)\sim\omega^{-2d}$ as $\omega\to0$ (T eq. 2.53). For $d>0$ the spectrum **diverges at frequency zero**, while every stationary ARMA spectrum is bounded on $[0,2\pi]$. This is what the log-periodogram estimator of $d$ exploits.

### 4.1 · Worked — the ACF from (8)–(9)

**$d=0.25$.** By (8), $\rho_1=0.25/0.75=1/3=0.3333$. By (9) with $k=2$:

$$\rho_2=\rho_1\cdot\frac{1+0.25}{2-0.25}=\frac13\cdot\frac{1.25}{1.75}=0.2381.$$

With $k=3$:

$$\rho_3=\rho_2\cdot\frac{2+0.25}{3-0.25}=0.2381\cdot\frac{2.25}{2.75}=0.1948.$$

PACF: $\phi_{2,2}=0.25/1.75=0.1429$. At $k=100$, (11) gives $\frac{\Gamma(0.75)}{\Gamma(0.25)}100^{-0.5}=\frac{1.2254}{3.6256}\times0.1=0.0338$, equal to the exact product (7) to four decimals.

**$d=0.4$.** $\rho_1=0.4/0.6=2/3$. An AR(1) with the same first autocorrelation has $\phi=2/3$ and $\rho_{100}=(2/3)^{100}=2.5\times10^{-18}$. The ARFIMA has, from (11),

$$\rho_{100}\approx\frac{\Gamma(0.6)}{\Gamma(0.4)}\,100^{-0.2}=\frac{1.4892}{2.2182}\times0.3981=0.6714\times0.3981=0.267,$$

again matching (7) (0.2673). Same lag-1 dependence; at lag 100 one is still 0.27, the other is zero for every practical purpose.

![Left: autocorrelations up to lag 60 for d = 0.1, 0.25, 0.4 (solid) and AR(1) processes with the same first autocorrelation 0.111, 0.333, 0.667 (dotted); the AR(1) curves fall to zero within a few lags while the ARFIMA curves stay visibly above zero. Right: the same on log-log axes up to lag 200, where the ARFIMA autocorrelations become straight lines with slopes -0.8, -0.5 and -0.2 and the AR(1) curves plunge](figures/L08-long-memory-acf.png)
*Figure — exact ACF (7) of ARFIMA(0,$d$,0) for $d=0.1,0.25,0.4$ against an AR(1) with the same $\rho_1=d/(1-d)$ from (8); right panel log–log, slope $2d-1$ from (11). T p. 102.*

On the linear scale the two families start at the same height, and the difference is in the tail: the dotted AR(1) curves are gone by lag 20 even for $\phi=2/3$. On the log–log scale the ARFIMA correlations are straight lines with slopes $-0.8$, $-0.5$ and $-0.2$, exactly $2d-1$, while a geometric decay $\phi^k$ is a curve that bends down ever faster. **A straight line on the log–log ACF plot is the visual test for long memory.**

---

## 5 · C — ARFIMA($p,d,q$) and the three kinds of memory (slide 38; T p. 102)

If the fractionally differenced series $(1-B)^dx_t$ follows an ARMA($p,q$), $x_t$ is **ARFIMA($p,d,q$)**: $\phi(B)(1-B)^dx_t=\theta(B)a_t$. It generalises ARIMA ([[L08-03-unit-roots-dickey-fuller]] (13)) from integer to non-integer $d$; the ARMA part shapes the short lags, $d$ the long ones.

| | $\psi_k$ (shock at $t-k$) | ACF at lag $k$ | Example |
|---|---|---|---|
| stationary ARMA ($d=0$) | geometric, $\propto|\lambda|^k$ | geometric | returns |
| long memory ($0<d<0.5$) | $\psi_k\approx k^{d-1}/(d-1)!$, hyperbolic | $\rho_k\sim ck^{2d-1}$ | $|r_t|$, volatility |
| unit root ($d=1$) | $\psi_k=1$ | sample ACF $\to1$ | log prices |

($\psi_k\approx k^{d-1}/(d-1)!$ follows from (4) by the same gamma-ratio step as (11).) Estimation of $d$ in the pure model (1): **maximum likelihood**, or a **regression on the logged periodogram at low frequencies** (T p. 102), which uses property 5. Bayesian treatments (Koop, Ley, Osiewalski and Steel 1997; Pai and Ravishanker 1998; Graves et al. 2015, …) are listed on slide 38; named only.

---

## 6 · G — long memory in volatility (T §3.13, p. 154)

The long-memory stochastic volatility model (T eq. 3.41) puts the fractional difference in the log-volatility: $a_t=\sigma_t\epsilon_t$, $\sigma_t=\sigma\exp(u_t/2)$, $(1-B)^du_t=\eta_t$, $0<d<0.5$. Then $\ln a_t^2$ is a Gaussian long-memory signal plus non-Gaussian noise. Bollerslev and Jubinski (1999) and Ray and Tsay (2000) find a median $d$ of about 0.38 for the log squared daily returns of S&P 500 companies. Named here; the short-memory SV model is [[L08-08-stochastic-volatility]].

---

## Links

- Neighbours: [[L08-03-unit-roots-dickey-fuller]] ($d=1$: the unit root) · [[L08-05-seasonal-airline-model]].
- Unit: [[L08-00-map]] · [[L08-10-formulas]] · [[L08-11-pitfalls]] · [[L08-12-python]] (the ACF recursion (9) checked against (10)) · [[L08-02-forecasting-ma-arma]] (geometric ACF and the identification table) · [[L08-06-arch-garch]] (why $|r_t|$ is autocorrelated).
- Class 1: [[../L01/L01-07-ar-var-review|L01-07]] (the linear-process ACF from $\psi$ weights, L01-07 (4)).
- Rules: [[../../rules/04_arima_raiz_unitaria|rules/04]] (long memory, ARFIMA).
- **Practice (number and printed page only):** T 2.5 (p. 105). Worked solutions: `Listas/lista-L08-book-exercises.pdf`.
