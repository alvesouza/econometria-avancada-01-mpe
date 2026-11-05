---
tags: [notes, lecture-08, time-series, ar2, arp, yule-walker, stationarity-triangle, characteristic-roots, business-cycles, pacf, aic, bic]
date: 2026-10-25
status: taught
source: "ar-ma.pdf slides 18–37 (AR(2) moments, stationarity-region code, the two φ sets, theoretical vs empirical ACF at n = 10 000, 1 000, 500, 200, US real GNP AR(3), AR(p), PACF, AIC, BIC); ar-ma.html (GNP arima output, polyroot, k = 10.656); Tsay AFTS 3e §2.4.1 pp. 40–46 (eqs. 2.12–2.15, Fig. 2.4 p. 43, Example 2.1 pp. 42–45), §2.4.2 pp. 46–53 (PACF, Table 2.1 p. 47, eq. 2.16 p. 48, selection rule p. 49, model checking pp. 50–52), §2.4.3 pp. 53–54 (R²), §2.6.3 pp. 66–68 (EACF, Table 2.4); Wooldridge 6e §11.1 pp. 345–348 (eqs. 11.2–11.4)"
---

# Tsay §2.4.1–2.4.2 · AR(2) and AR(p): moments, the stationarity triangle, cycles from complex roots, and choosing p

> **Claim.** **An AR(2) is two AR(1)'s stacked, and its behaviour is read off one quadratic**, $1-\phi_1x-\phi_2x^2=0$. **Stationary iff both solutions lie outside the unit circle, which in the $(\phi_1,\phi_2)$ plane is the triangle $\phi_2<1-\phi_1$, $\phi_2<1+\phi_1$, $\phi_2>-1$.** The ACF obeys the same second-order difference equation as the series (Yule–Walker), so **real roots give a mixture of exponential decays and complex roots give damped waves with average period $k=2\pi/\cos^{-1}[\phi_1/(2\sqrt{-\phi_2})]$**, which is how a quarterly GNP AR(3) delivers a 10.6-quarter business cycle. **The order $p$ is chosen by the PACF, which cuts off after lag $p$ with standard error $1/\sqrt T$, or by AIC/BIC, which can disagree** (AR(9) vs AR(1) on the same CRSP returns).
> Prev: [[../L01/L01-07-ar-var-review|L01-07]] · Next: [[L08-02-forecasting-ma-arma]] · Map: [[L08-00-map]]

What L01-07 already settled and this note uses without repeating: weak stationarity, the ACF and Ljung–Box (L01-07 (1)–(3)), linear series and $\psi$ weights (L01-07 (4)), the AR(1) mean, variance and ACF $\rho_\ell=\phi_1^\ell$ (L01-07 (6)–(11)), conditional least squares = conditional MLE (L01-07 (12)–(13)), and AR(p) as a regression with mean (L01-07 (20)–(21)).

**Notation.**

| Symbol | Meaning | Range |
|---|---|---|
| $r_t$ | the series (Tsay); $y_t$ on the site's pages | |
| $a_t$ | white-noise shock, variance $\sigma_a^2$ ($\sigma^2$ on ar2-forecast.html) | |
| $\phi_0,\phi_1,\dots,\phi_p$ | AR intercept and coefficients | |
| $\mu=E(r_t)$ | stationary mean | |
| $\gamma_\ell,\ \rho_\ell$ | lag-$\ell$ autocovariance and autocorrelation; $\gamma_0=V(r_t)$ | $\rho_\ell\in[-1,1]$ |
| $B$ | back-shift operator, $Br_t=r_{t-1}$, $B\gamma_\ell=\gamma_{\ell-1}$ (Tsay writes $L$ too) | |
| $x_1,x_2$ | solutions of the characteristic equation $1-\phi_1x-\phi_2x^2=0$ | complex in general |
| $\omega_i=1/x_i$ | characteristic roots (Tsay's name for the inverses) | |
| $k$ | average length of the stochastic cycle | periods |
| $\phi_{\ell,\ell}$ | lag-$\ell$ partial autocorrelation (PACF) | |
| $T$ | sample length | |
| $\tilde\sigma_\ell^2$ | MLE of $\sigma_a^2$ in an AR($\ell$) fit | |

---

## 1 · C — AR(2): mean and the centred form (slide 18; T pp. 40–41)

The model (T eq. 2.12):

$$r_t=\phi_0+\phi_1r_{t-1}+\phi_2r_{t-2}+a_t.\tag{1}$$

Take expectations of (1), with $E(a_t)=0$ and, under stationarity, $E(r_t)=E(r_{t-1})=E(r_{t-2})=\mu$:

$$\mu=\phi_0+\phi_1\mu+\phi_2\mu$$

$$\mu(1-\phi_1-\phi_2)=\phi_0$$

$$\mu=\frac{\phi_0}{1-\phi_1-\phi_2},\qquad\text{provided }\phi_1+\phi_2\ne1.\tag{2}$$

(The slide prints the proviso as "$\phi_1+\phi_2=1$": the inequality sign was lost.) Substitute $\phi_0=(1-\phi_1-\phi_2)\mu$ from (2) into (1):

$$r_t=(1-\phi_1-\phi_2)\mu+\phi_1r_{t-1}+\phi_2r_{t-2}+a_t$$

$$r_t-\mu=\phi_1(r_{t-1}-\mu)+\phi_2(r_{t-2}-\mu)+a_t.\tag{3}$$

> **The intercept is not the mean.** At $\phi_1+\phi_2\to1$ the denominator of (2) vanishes: that is the unit root of [[L08-03-unit-roots-dickey-fuller]].

---

## 2 · C — the moment equations and Yule–Walker (slides 18–19; T eq. 2.13, p. 41)

Multiply (3) by $(r_{t-\ell}-\mu)$ and take expectations. For $\ell>0$, $r_{t-\ell}$ depends only on shocks dated $t-\ell$ and earlier, so $E[(r_{t-\ell}-\mu)a_t]=0$:

$$E[(r_{t-\ell}-\mu)(r_t-\mu)]=\phi_1E[(r_{t-\ell}-\mu)(r_{t-1}-\mu)]+\phi_2E[(r_{t-\ell}-\mu)(r_{t-2}-\mu)]+0$$

$$\gamma_\ell=\phi_1\gamma_{\ell-1}+\phi_2\gamma_{\ell-2},\qquad\ell>0.\tag{4}$$

For $\ell=0$ the shock term does not vanish: $E[(r_t-\mu)a_t]=E(a_t^2)=\sigma_a^2$ (only the $a_t$ in (3) is correlated with itself), so

$$\gamma_0=\phi_1\gamma_1+\phi_2\gamma_2+\sigma_a^2.\tag{5}$$

Divide (4) by $\gamma_0$ — the **Yule–Walker** (moment) equation of the ACF, T (2.13):

$$\rho_\ell=\phi_1\rho_{\ell-1}+\phi_2\rho_{\ell-2},\qquad\ell>0.\tag{6}$$

At $\ell=1$, using $\rho_0=1$ and $\rho_{-1}=\rho_1$ (L01-07 (1)):

$$\rho_1=\phi_1\rho_0+\phi_2\rho_{-1}=\phi_1+\phi_2\rho_1$$

$$\rho_1=\frac{\phi_1}{1-\phi_2}.\tag{7}$$

At $\ell=2$, substituting (7) into (6):

$$\rho_2=\phi_1\rho_1+\phi_2=\frac{\phi_1^2}{1-\phi_2}+\phi_2.\tag{8}$$

In operator form (6) is $(1-\phi_1B-\phi_2B^2)\rho_\ell=0$: **the ACF solves the same difference equation as the series without its shock**. That single fact gives the shape of the ACF (§4) and of the forecasts ([[L08-02-forecasting-ma-arma]] §1).

---

## 3 · C — the variance, step by step (slide 19)

Write (5) with $\gamma_\ell=\rho_\ell\gamma_0$. From (7), $\gamma_1=\frac{\phi_1}{1-\phi_2}\gamma_0$; from (4) at $\ell=2$, $\gamma_2=\phi_1\gamma_1+\phi_2\gamma_0$. Substitute $\gamma_2$ into (5):

$$\gamma_0=\phi_1\gamma_1+\phi_2\big(\phi_1\gamma_1+\phi_2\gamma_0\big)+\sigma_a^2$$

$$\gamma_0=\phi_1(1+\phi_2)\gamma_1+\phi_2^2\gamma_0+\sigma_a^2.$$

Substitute $\gamma_1$ from (7):

$$\gamma_0=\phi_1(1+\phi_2)\Big(\frac{\phi_1}{1-\phi_2}\gamma_0\Big)+\phi_2^2\gamma_0+\sigma_a^2$$

$$\gamma_0\Big[1-\phi_2^2-\frac{\phi_1^2(1+\phi_2)}{1-\phi_2}\Big]=\sigma_a^2.$$

Multiply both sides by $(1-\phi_2)$ and use $1-\phi_2^2=(1-\phi_2)(1+\phi_2)$:

$$\gamma_0\big[(1-\phi_2)^2(1+\phi_2)-\phi_1^2(1+\phi_2)\big]=(1-\phi_2)\sigma_a^2$$

$$\boxed{\;\gamma_0=\frac{(1-\phi_2)\,\sigma_a^2}{(1+\phi_2)\big[(1-\phi_2)^2-\phi_1^2\big]}\;}\tag{9}$$

the slide's "$\gamma_0=\frac{1-\phi_2}{(1+\phi_2)[(1-\phi_2)^2-\phi_1^2]}\sigma_a^2$". **Erratum:** `ar2-forecast.html` §3 prints $Var(y_t)=\big(\frac{1-\phi_2}{1+\phi_2}\big)\{(1-\phi_2)^2-\phi_1^2\}\sigma^2$, with the braces multiplying; its own R line `sqrt(sig^2*(1-phi2)/((1+phi2)*((1-phi2)^2-phi1^2)))` divides, as in (9), and prints 7.12069.

**Worked — the two parameter sets of slides 20–22** ($\sigma_a=1$):

| | $(\phi_1,\phi_2)=(1.75,-0.80)$ | $(\phi_1,\phi_2)=(0.90,0.05)$ |
|---|---|---|
| $\rho_1$ by (7) | $\frac{1.75}{1-(-0.80)}=\frac{1.75}{1.80}=0.9722$ | $\frac{0.90}{1-0.05}=\frac{0.90}{0.95}=0.9474$ |
| $\rho_2$ by (8) | $1.75(0.9722)+(-0.80)=1.7014-0.80=0.9014$ | $0.90(0.9474)+0.05=0.8526+0.05=0.9026$ |
| $(1-\phi_2)^2-\phi_1^2$ | $1.80^2-1.75^2=3.2400-3.0625=0.1775$ | $0.95^2-0.90^2=0.9025-0.8100=0.0925$ |
| $\gamma_0$ by (9) | $\frac{1.80}{(0.20)(0.1775)}=\frac{1.80}{0.0355}=50.704$ | $\frac{0.95}{(1.05)(0.0925)}=\frac{0.95}{0.097125}=9.7812$ |
| sd $\sqrt{\gamma_0}$ | **7.1207** (the page's 7.12069) | 3.1275 |

The first lag correlations are almost equal (0.97 vs 0.95, 0.90 vs 0.90), yet the variances differ fivefold: the first model sits close to an edge of the triangle (§5), where (9)'s bracket $0.1775$ is small.

---

## 4 · C — the characteristic equation and its roots (T eq. 2.14, pp. 41–42)

Corresponding to (6) is the polynomial equation (T 2.14)

$$1-\phi_1x-\phi_2x^2=0,\tag{10}$$

with solutions (quadratic formula, $\phi_2\ne0$)

$$x=\frac{\phi_1\pm\sqrt{\phi_1^2+4\phi_2}}{-2\phi_2}.\tag{11}$$

Their inverses $\omega_i=1/x_i$ are the **characteristic roots**. Multiplying (10) by $\omega^2$ with $x=1/\omega$ shows they solve

$$\omega^2-\phi_1\omega-\phi_2=0,\qquad\omega_1+\omega_2=\phi_1,\quad\omega_1\omega_2=-\phi_2,\tag{12}$$

and the AR polynomial factors as $1-\phi_1B-\phi_2B^2=(1-\omega_1B)(1-\omega_2B)$: **an AR(1) operating on top of another AR(1)** (T p. 42).

- **Real roots** ($\phi_1^2+4\phi_2\ge0$): the solution of (6) is $\rho_\ell=c_1\omega_1^\ell+c_2\omega_2^\ell$, a mixture of two exponential decays.
- **Complex roots** ($\phi_1^2+4\phi_2<0$): $\omega_{1,2}=Re^{\pm i\theta}$ with, by (12), $R^2=\omega_1\omega_2=-\phi_2$ and $2R\cos\theta=\omega_1+\omega_2=\phi_1$. So

$$R=\sqrt{-\phi_2},\qquad\cos\theta=\frac{\phi_1}{2\sqrt{-\phi_2}},\tag{13}$$

and $\rho_\ell=c\,R^\ell\cos(\theta\ell+\varphi)$: **a damped cosine** with damping $R$ per period and frequency $\theta$ radians per period. One full wave takes $2\pi/\theta$ periods (T p. 42):

$$\boxed{\;k=\frac{2\pi}{\cos^{-1}\!\big[\phi_1/(2\sqrt{-\phi_2})\big]}\;}\tag{14}$$

with the inverse cosine in radians. Writing the complex **solutions** of (10) as $a\pm bi$, $|a\pm bi|=1/R$ and $\cos\theta=a/\sqrt{a^2+b^2}$, so equivalently $k=2\pi/\cos^{-1}(a/\sqrt{a^2+b^2})$ (T p. 42) — the form R's `polyroot` output feeds.

> **Complex roots are the business cycle.** Damped sine waves in the ACF, and in the forecasts, are what an economist calls a stochastic cycle (T p. 42).

---

## 5 · C — the stationarity triangle (slides 20–21; T p. 45)

**Condition** (T p. 45): both characteristic roots inside the unit circle, $|\omega_i|<1$; equivalently both solutions $x_i$ of (10) outside it. Translate to $(\phi_1,\phi_2)$ with (12).

*Real roots.* $f(\omega)=\omega^2-\phi_1\omega-\phi_2$ is an upward parabola. Both roots lie in $(-1,1)$ iff $f(1)>0$, $f(-1)>0$ and the vertex $\phi_1/2$ is in $(-1,1)$:

$$f(1)=1-\phi_1-\phi_2>0\iff\phi_2<1-\phi_1,\tag{15}$$

$$f(-1)=1+\phi_1-\phi_2>0\iff\phi_2<1+\phi_1.\tag{16}$$

The product $\omega_1\omega_2=-\phi_2$ of two numbers in $(-1,1)$ is in $(-1,1)$, so in particular $\phi_2>-1$.

*Complex roots.* $|\omega_1|=|\omega_2|=R=\sqrt{-\phi_2}$ by (13), so $|\omega_i|<1\iff-\phi_2<1$:

$$\phi_2>-1.\tag{17}$$

Together, the stationary region is the **triangle** with vertices $(-2,-1)$, $(2,-1)$, $(0,1)$:

$$\boxed{\;\phi_2<1-\phi_1,\qquad\phi_2<1+\phi_1,\qquad\phi_2>-1\;}\tag{18}$$

Adding (15) and (16) gives $\phi_2<1$, so $|\phi_2|<1$ inside it (and the vertex condition $|\phi_1|<2$ is implied). The **parabola** $\phi_2=-\phi_1^2/4$ splits it: complex roots below, real above. The slide's R code draws exactly these lines (`1+phi1`, `-1`, `1-phi1`, the gray polygon `1-abs(phi1)` and `-phi1^2/4`). Note that (18) is also what keeps (9) positive: $(1-\phi_2)^2-\phi_1^2=(1-\phi_2-\phi_1)(1-\phi_2+\phi_1)>0$ by (15)–(16), and $1+\phi_2>0$ by (17).

**Worked — the four points of the figure.**

- **$(1.75,-0.80)$, slide 20.** Discriminant $\phi_1^2+4\phi_2=3.0625-3.2000=-0.1375<0$: **complex** (the point lies just below the parabola, $-1.75^2/4=-0.7656$). By (13), $R=\sqrt{0.80}=0.8944$ (solutions of modulus $1/0.8944=1.1180$, outside the circle: stationary) and $\cos\theta=1.75/(2\times0.8944)=1.75/1.7889=0.9783$, $\theta=0.2088$ rad, so by (14) $k=2\pi/0.2088=$ **30.09** periods. The ACF is a long, slow wave: it falls from 0.97 to a trough of **−0.1866 at lag 15** — half a cycle, $30.09/2\approx15$ — then dies out (damping $0.8944^{30}=0.035$ per cycle).
- **$(0.90,0.05)$, slide 20.** Discriminant $0.81+0.20=1.01>0$: **real**. By (11) the solutions are $x=\frac{0.90\pm\sqrt{1.01}}{-0.10}$, i.e. $\frac{0.90+1.00499}{-0.10}=-19.05$ and $\frac{0.90-1.00499}{-0.10}=1.0499$. One root is **barely outside the circle** (characteristic root $1/1.0499=0.9525$): a near-unit-root process with a slowly decaying, single-signed ACF ($\phi_1+\phi_2=0.95$, close to the edge (15)).
- **GNP factor $(0.869,-0.274)$** — the worked example below; complex, $k=10.62$.
- **Tsay Fig. 2.4(b), $(0.6,-0.4)$** (T p. 42): discriminant $0.36-1.6=-1.24<0$; $\cos\theta=0.6/(2\sqrt{0.4})=0.4743$, $\theta=1.0766$, $k=5.84$.

![Left: the AR(2) stationarity triangle in the phi1-phi2 plane with vertices (-2,-1), (2,-1), (0,1), the dashed parabola phi2 = -phi1^2/4 separating real from complex roots, and four marked points: the slides' (1.75, -0.80) near the right edge with cycle length 30.1, the slides' (0.90, 0.05) near the upper-right edge with real roots, the GNP factor (0.869, -0.274) with cycle 10.62, and Tsay's (0.6, -0.4) with cycle 5.84. Right: exact ACFs of the two slide models to lag 150: the complex one falls fast, dips to about -0.19 near lag 15 and oscillates out; the real one decays smoothly and slowly from 0.95](figures/L08-ar2-triangle-acf.png)
*Figure — region (18) with the parabola $\phi_2=-\phi_1^2/4$; ACF from the recursion (6)–(7) for slides 20–22's parameter sets.*

On the left, both slide points are inside the triangle, so both processes are stationary, but each hugs a different edge: $(0.90,0.05)$ is near $\phi_2=1-\phi_1$ (a real root near 1), $(1.75,-0.80)$ is near the same edge from below the parabola (complex roots of modulus 0.89). On the right the near-real-unit-root model gives the long one-signed decay, while the complex model gives the trough at lag 15 and a small second wave near lag 30 — the cycle length (14) is visible in the ACF.

> **Interactive companion.** [The AR(2) Triangle](companions/companion-ar2-dynamics.html) — move $\phi_1$, $\phi_2$, $\sigma$, $y_n$, $y_{n-1}$ and the horizon $H$; watch the point cross the parabola and the edges of the triangle, the root moduli and cycle length update, the ACF switch between decays and waves, and the forecast fan revert (or explode).

---

## 6 · C — worked: US real GNP and the 10.6-quarter cycle (slides 26–29; T Example 2.1, pp. 42–45; ar-ma.html)

Quarterly growth of US real GNP, 1947.II–1991.I, $T=176$; `ar(gnp, method="mle")` selects order 3 by AIC. Fitted (T eq. 2.15):

$$r_t=0.0047+0.348r_{t-1}+0.179r_{t-2}-0.142r_{t-3}+a_t,\qquad\hat\sigma_a=0.0097.\tag{19}$$

**The intercept from R's output.** R's `arima` reports the *mean*, `intercept` = 0.0077, with coefficients 0.3480, 0.1793, −0.1423. By (2) generalised (L01-07 (21)):

$$\phi_0=(1-\phi_1-\phi_2-\phi_3)\mu=(1-0.348-0.1793-(-0.1423))\times0.0077=0.6150\times0.0077=0.0047355.$$

$\hat\sigma_a=\sqrt{9.427\times10^{-5}}=0.009709$.

**The characteristic polynomial factors** (T p. 43):

$$1-0.348B-0.179B^2+0.142B^3\approx(1+0.521B)(1-0.869B+0.274B^2).\tag{20}$$

Check by multiplying out: $(1+0.521B)(1-0.869B+0.274B^2)=1+(0.521-0.869)B+(0.274-0.521\times0.869)B^2+0.521\times0.274B^3=1-0.348B-0.1787B^2+0.1428B^3$ ✓ (to rounding).

- The first factor $(1+0.521B)$ is a real root $\omega=-0.521$: an alternating exponential decay.
- The second is an AR(2) with $\phi_1=0.869$, $\phi_2=-0.274$. Discriminant $0.869^2+4(-0.274)=0.755161-1.096=-0.341<0$: **complex**. By (13)–(14): $\sqrt{0.274}=0.52345$, $\cos\theta=\frac{0.869}{2\times0.52345}=\frac{0.869}{1.04690}=0.83007$, $\theta=\cos^{-1}(0.83007)=0.59156$ rad,

$$k=\frac{2\pi}{0.59156}=\frac{6.28319}{0.59156}=10.62\ \text{quarters}\approx\text{3 years}.$$

**From R's roots** (ar-ma.html): `polyroot(c(1,-0.3480,-0.1793,0.1423))` gives $1.590253\pm1.063882i$ and $-1.920152$, moduli 1.913308, 1.920152 (all $>1$: stationary). With $a=1.590253$, $\sqrt{a^2+b^2}=1.913308$: $a/\sqrt{a^2+b^2}=0.83115$, $\cos^{-1}=0.58962$ rad, $k=6.28319/0.58962=$ **10.656** — the page's `10.65638`. The difference from 10.62 is the rounding of the coefficients in (20).

> **10.62 quarters is a compromise.** A nonlinear model splitting the economy into regimes finds contractions of about 3 quarters and expansions of about 12; the linear AR(3) averages them into one damped cycle (T p. 44). The same feature appears in many OECD growth rates.

---

## 7 · C — AR(p) (slide 30; T p. 46)

$r_t=\phi_0+\phi_1r_{t-1}+\dots+\phi_pr_{t-p}+a_t$ has stationary mean $\phi_0/(1-\phi_1-\dots-\phi_p)$ (L01-07 (21)) and characteristic equation

$$1-\phi_1x-\phi_2x^2-\dots-\phi_px^p=0.\tag{21}$$

**Stationary iff all solutions of (21) exceed 1 in modulus** (all characteristic roots $<1$). Multiplying the centred model by $r_{t-\ell}-\mu$ as in §2 gives the AR(p) Yule–Walker equation

$$(1-\phi_1B-\dots-\phi_pB^p)\rho_\ell=0,\qquad\ell>0,\tag{22}$$

so the ACF is **a mixture of damped sine–cosine waves (one per complex pair) and exponential decays (one per real root)** — it never cuts off. That is why the ACF cannot identify $p$; the PACF can.

---

## 8 · C — the partial autocorrelation function (slides 31–32; T pp. 46–48)

Fit AR models of increasing order by least squares (they are regressions, L01-07 §8):

$$r_t=\phi_{0,1}+\phi_{1,1}r_{t-1}+e_{1t},$$

$$r_t=\phi_{0,2}+\phi_{1,2}r_{t-1}+\phi_{2,2}r_{t-2}+e_{2t},$$

$$r_t=\phi_{0,3}+\phi_{1,3}r_{t-1}+\phi_{2,3}r_{t-2}+\phi_{3,3}r_{t-3}+e_{3t},\ \dots\tag{23}$$

**Definition.** The last coefficient of the $j$-th regression, $\hat\phi_{j,j}$, is the **lag-$j$ sample PACF**: the added contribution of $r_{t-j}$ over an AR($j-1$) — a partial $F$ (here $t$) test logic. For a **stationary Gaussian AR(p)** (T p. 47):

1. $\hat\phi_{p,p}\to\phi_p$ as $T\to\infty$;
2. $\hat\phi_{\ell,\ell}\to0$ for all $\ell>p$;
3. $V(\hat\phi_{\ell,\ell})\approx1/T$ for $\ell>p$.

So **the PACF cuts off at lag $p$**, and $\pm2/\sqrt T$ is the approximate 95% band. Population version: $\phi_{\ell,\ell}$ is a function of $\rho_1,\dots,\rho_\ell$ (the Durbin–Levinson recursion, used in [[L08-12-python]] and the figure of [[L08-02-forecasting-ma-arma]] §8). For an AR(2), $\phi_{1,1}=\rho_1$ and $\phi_{2,2}=\phi_2$.

**Worked.**

- CRSP value-weighted monthly returns, 1926–2008, $T=996$ (T Table 2.1, p. 47): $1/\sqrt{996}=0.0317\approx0.032$, band $\pm0.063$. PACF: 0.115, −0.030, **−0.102**, 0.033, 0.062, −0.050, 0.031, 0.052, **0.063**, … Lags 1 and 3 clear 0.063, lag 9 sits on it: AR(3) or AR(9) at 5%, AR(3) at 1%.
- GNP (Fig. 2.6, p. 48): $\pm2/\sqrt{176}=\pm0.151$; the first three lags are large: AR(3), as in (19).

---

## 9 · C — information criteria (slides 33–34; T eq. 2.16, pp. 48–49)

$$\text{AIC}=\frac{-2}{T}\ln(\text{likelihood})+\frac{2}{T}\times(\text{number of parameters}),\tag{24}$$

goodness of fit plus a penalty, the likelihood at the MLE. For a Gaussian AR($\ell$), $-\frac2T\ln L=\ln\tilde\sigma_\ell^2+\text{const}$ (L01-06's Gaussian log-likelihood at $\hat\sigma^2$), so

$$\text{AIC}(\ell)=\ln\tilde\sigma_\ell^2+\frac{2\ell}{T},\qquad\text{BIC}(\ell)=\ln\tilde\sigma_\ell^2+\frac{\ell\ln T}{T}.\tag{25}$$

**Selection rule** (T p. 49): compute for $\ell=0,\dots,P$ and pick the minimum. The penalty per parameter is 2 for AIC and $\ln T$ for BIC; with $T=996$, $\ln T=6.90$, so **BIC picks smaller models whenever $T>e^2\approx7.4$**.

**Worked — Table 2.1 again.** AIC is minimal at $\ell=9$ (**−5.849**); BIC at $\ell=1$ (**−5.833**), with $\ell=3$ a close second (−5.831). Same data, three answers (PACF: 3 or 9; AIC: 9; BIC: 1). Tsay's verdict: no criterion dominates; substance and simplicity decide. For GNP, R's `ord$aic` (rescaled so the minimum is 0) is 27.847, 2.742, 1.603, **0.000**, 0.323, … for orders 0, 1, 2, **3**, 4: AR(3).

> **Penalty per parameter: 2 (AIC) vs $\ln T$ (BIC).** Same idea as the $C_p$/AIC/BIC of regression in [[../L01/L01-06-gaussian-linear-regression|L01-06]], same direction of disagreement.

---

## 10 · C — fitting and checking (T pp. 49–53)

Conditional least squares from observation $p+1$ (L01-07 §5, §8); residuals $\hat a_t$; **the Ljung–Box test on the residuals has $m-g$ degrees of freedom**, $g$ the number of AR/MA coefficients (T p. 51; R and S-Plus use $m$ by default). CRSP AR(3): $Q(12)=16.35$, $p=0.060$ on $\chi^2_9$ (R prints 0.1756 on 12 df). Dropping the insignificant lag 2 gives $r_t=0.0088+0.114r_{t-1}-0.106r_{t-3}+a_t$, $\hat\sigma_a=0.0536$, $Q(12)=16.83$, $p=0.078$ on $\chi^2_{10}$: adequate. The intercept from R's mean: $(1-0.1136+0.1063)\times0.0089=0.00884$.

**$R^2$** (T §2.4.3, pp. 53–54): $1-\sum\hat a_t^2/\sum(r_t-\bar r)^2$ measures fit only for stationary series; **for a unit-root series the $R^2$ of an AR(1) fit tends to 1 whatever the true model**, and it cannot fall when lags are added (L01-06's warning again).

---

## 11 · U — what the slides' simulation shows (slides 23–25)

Slides 23–25 simulate each model (`acf1.hedi`: burn-in of $n$ draws, keep the next $n$) and overlay the sample ACF on the theoretical one at $n=10\,000$, 1 000, 500 and 200. At $n=10\,000$ the two agree; as $n$ falls the sample ACF wanders around the theoretical curve with growing error, most visibly at the long lags of the near-unit-root $(0.90,0.05)$ model, whose slow decay needs long samples to be estimated. **Sample ACFs at high lags are noisy, and for persistent series biased toward zero**; read them with the $\pm2/\sqrt T$ band.

## 12 · G — EACF (T §2.6.3, pp. 66–68)

When the model is a mixed ARMA, neither ACF nor PACF cuts off ([[L08-02-forecasting-ma-arma]] §6). Tsay and Tiao's **extended ACF** is a two-way table whose triangle of O's has its upper-left vertex at $(p,q)$ (Table 2.4 for ARMA(1,1)); X means $|\text{EACF}|\ge2/\sqrt T$. 3M monthly log returns, $T=755$: $2/\sqrt{755}=0.073$, vertex at $(0,0)$ — white noise. Named only.

---

## Links

- Neighbours: [[../L01/L01-07-ar-var-review|L01-07]] (AR(1), equilibrium law, VAR(1)) · [[L08-02-forecasting-ma-arma]] (forecasts, MA, ARMA, identification figure).
- Unit: [[L08-00-map]] · [[L08-10-formulas]] · [[L08-11-pitfalls]] · [[L08-12-python]] · [[L08-03-unit-roots-dickey-fuller]] (the edge $\phi_1+\phi_2=1$).
- Class 1: [[../L01/L01-06-gaussian-linear-regression|L01-06]] (AIC/BIC in regression). Class 9 (plain forward link): the VAR(p) has the matrix version of (21): stationarity iff all roots of $\det(I-\Phi_1x-\dots-\Phi_px^p)=0$ lie outside the unit circle.
- Rules: [[../../rules/04_arima_raiz_unitaria|rules/04]] (ARIMA, unit roots).
- **Practice (number and printed page only; statements in Tsay):** T 2.1 (p. 104), T 2.2 (p. 104), T 2.3 (p. 104), T 2.4 (p. 105). Full solutions are being built at `Listas/lista-L08-book-exercises.pdf`.
