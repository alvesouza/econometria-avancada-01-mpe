---
tags: [notes, lecture-08, python, reference-implementation, self-checks, arma, unit-root, sarima, garch-mle, stochastic-volatility, metropolis]
date: 2026-10-25
status: taught
source: "Runnable script Notas/L08/L08_python_checks.py (this note shows it section by section); figures/make_figures.py (imported: AR(2) ACF and variance, psi weights, Durbin-Levinson PACF, ARFIMA ACF); companions/check_companions.py (imported: the two pages' read-out functions); data: AirPassengers from seasonal.pdf slide 17, Tsay's m-deciles08.txt and d-gmsp9908.txt in Listas/data/"
---

# Class 8 · Computation in Python — every routine, with the assert that must pass

> Every computation the unit uses, written in Python (numpy, scipy, statsmodels; no R, no `arch`,
> no PyMC), and each checked with an `assert` against the number printed in the deck, the site page or
> the book. The code below is the script **`Notas/L08/L08_python_checks.py`**, split into its sections.
> Run `python Notas/L08/L08_python_checks.py` (about one minute). It prints one `ok` line per section
> and ends with `ALL L08 CHECKS PASSED`, which is the output of the run on 2026-10-27.
> Prev: [[L08-11-pitfalls]] · Map: [[L08-00-map]] · Formulas: [[L08-10-formulas]]

**What is reused, not rewritten.**

| Already in the unit | What it computes | How this note uses it |
|---|---|---|
| `figures/make_figures.py` | `ar2_acf`, `ar2_gamma0`, `cycle_length`, `psi_weights`, `acf_linear`, `pacf_from_acf` (Durbin–Levinson), `arfima_acf`; eight figures with their own asserts | **imported** as `mf` (functions only; `build()` is not called) |
| `companions/check_companions.py` | `ar_python()` and `ga_python()`, the exact read-out strings of the AR(2) Triangle and the Volatility Dial | **imported** as `cc`; §1 and §6 check that the pages' defaults print the numbers derived here |
| statsmodels | `ArmaProcess.acf`, `arma_pacf`, `adfuller`, `SARIMAX`, `OLS` | independent path for every hand formula |

**What had to be written.** `arch` and PyMC are not installed, so the GARCH likelihoods (normal and
standardized $t$), their maximisation, the GARCH simulator, and the random-walk Metropolis sampler for
the Bayesian GARCH-$t$ are written here in NumPy/SciPy (the variance recursion is one call to
`scipy.signal.lfilter`). The SV part uses simulation and closed forms only; a full SV Gibbs sampler
(L08-08 §6) is described in the note but not coded.

**Conventions.** `near(x, printed, tol)` passes when `x` matches a printed value to `tol` (default 5e-4).
Monte Carlo checks are seeded and allow about four standard errors. Equation numbers "(k)" are those of
the section note named in each heading. Tsay's MA sign ($a_t-\theta a_{t-1}$) is used in formulas;
statsmodels and R print $+\theta$.

---

## 0 · Setup

```python
"""Class 8 (L08) reference implementation, with assert self-checks against the decks' and books' numbers.

Run:  python Notas/L08/L08_python_checks.py      (stops at the first failed assert; about 1-2 minutes)

Sections §1-§9 are the code blocks of L08-12-python.md, in the same order. The model functions
(AR(2) ACF and variance, psi weights, PACF by Durbin-Levinson, ARFIMA ACF) are imported from
figures/make_figures.py, and the two companions' read-out functions from companions/check_companions.py
(reuse, not copies). Equation numbers "(k)" refer to the section note named in each header.
Every Monte Carlo draw is seeded; MC checks use tolerances of about four standard errors.
Data: AirPassengers is printed on seasonal.pdf slide 17 (embedded below); CRSP Decile 1 and the
daily S&P 500 returns are Tsay's files in Listas/data/ (read-only).
"""
import math
import pathlib
import sys
import warnings

import numpy as np
import statsmodels.api as sm
from scipy import integrate, optimize, signal, special, stats
from statsmodels.tsa.arima_process import ArmaProcess, arma_pacf
from statsmodels.tsa.statespace.sarimax import SARIMAX
from statsmodels.tsa.stattools import adfuller

HERE = pathlib.Path(__file__).resolve().parent
DATA = HERE.parents[1] / "Listas" / "data"
sys.path.insert(0, str(HERE / "figures"))
sys.path.insert(0, str(HERE / "companions"))
import make_figures as mf  # noqa: E402  model functions only; build() is not called
import check_companions as cc  # noqa: E402  the companions' read-out functions

warnings.filterwarnings("ignore")          # statsmodels' convergence chatter on the small SARIMA grid
sys.stdout.reconfigure(encoding="utf-8")


def near(x, printed, tol=5e-4):
    """True when x agrees with a printed value to within tol (default: half a unit in the 3rd decimal)."""
    return abs(float(x) - printed) <= tol
```

---

## 1 · AR(2), AR(p), PACF, information criteria → [[L08-01-ar2-arp-cycles-identification]]

The triangle conditions L08-01 (15)–(17) are checked against the root moduli at five points (stationary
complex, stationary real, the GNP factor, a unit-root edge, an explosive complex pair). The recursion
L08-01 (6) is checked against statsmodels' exact ACF, the GNP cycle against R's printed roots (10.656) and
Tsay's rounded factor (10.62), the PACF against `arma_pacf` and against a long seeded sample, and the
companion's default read-outs against the same numbers.

```python
# === §1 AR(2), AR(p), PACF, information criteria (L08-01) ===
def ar2_roots(p1, p2):
    """Solutions x of 1 - p1 x - p2 x^2 = 0 (L08-01 (10)); stationary iff all |x| > 1."""
    return np.roots([-p2, -p1, 1.0])


def in_triangle(p1, p2):
    """Triangle conditions L08-01 (15)-(17)."""
    return p2 < 1 - p1 and p2 < 1 + p1 and p2 > -1


for (p1, p2), stat, cplx in [((1.75, -0.80), True, True), ((0.90, 0.05), True, False),
                             ((0.869, -0.274), True, True), ((0.5, 0.5), False, False), ((0.5, -1.2), False, True)]:
    x = ar2_roots(p1, p2)
    assert (np.abs(x).min() > 1) == stat == in_triangle(p1, p2), (p1, p2)      # roots <=> triangle
    assert (p1 ** 2 + 4 * p2 < 0) == cplx == bool(np.iscomplex(x).any())
r = mf.ar2_acf(1.75, -0.8, 40)
assert near(r[1], 0.9722, 5e-5) and near(r[2], 0.9014, 5e-5) and r.argmin() == 15 and near(r.min(), -0.1866, 5e-5)
assert near(math.sqrt(mf.ar2_gamma0(1.75, -0.8)), 7.12069, 5e-6) and near(abs(ar2_roots(1.75, -0.8)[0]), 1.1180, 5e-5)
assert near(math.sqrt(mf.ar2_gamma0(0.9, 0.05)), 3.1275, 5e-5) and near(ar2_roots(0.9, 0.05).real.min(), -19.05, 5e-3)
assert near(mf.cycle_length(1.75, -0.8), 30.09, 5e-3) and near(mf.cycle_length(0.6, -0.4), 5.836, 5e-4)
# The ACF recursion agrees with statsmodels' exact ACF.
assert np.allclose(ArmaProcess(ar=[1, -1.75, 0.8]).acf(41), r, atol=1e-12)
# GNP AR(3) (T eq. 2.15): R's unrounded coefficients give k = 10.656; Tsay's rounded factor gives 10.62.
roots = np.roots([0.1423, -0.1793, -0.3480, 1.0])                       # 1 - .348x - .1793x^2 + .1423x^3
z = roots[np.argmax(roots.imag)]                                          # 4-decimal coefficients: R used more digits
assert near(z.real, 1.590253, 5e-4) and near(abs(z), 1.913308, 5e-4) and near(abs(roots.real.min()), 1.920152, 5e-4)
assert near(2 * math.pi / math.acos(1.590253 / 1.913308), 10.65638, 5e-6)  # from R's printed roots (ar-ma.html)
assert near(2 * math.pi / math.acos(z.real / abs(z)), 10.656, 2e-3)
assert near(mf.cycle_length(0.869, -0.274), 10.62, 5e-3)
assert near((1 - .348 - .1793 + .1423) * 0.0077, 0.0047355, 5e-8)        # intercept from R's mean
assert np.allclose(np.polymul([1, 0.521], [1, -0.869, 0.274]), [1, -0.348, -0.178749, 0.142754])
# PACF: Durbin-Levinson on the exact ACF equals statsmodels' arma_pacf; AR(2) cuts off after lag 2.
pac = mf.pacf_from_acf(mf.ar2_acf(0.6, -0.4, 10), 10)
assert np.allclose(pac, arma_pacf([1, -0.6, 0.4], [1], lags=11)[1:], atol=1e-10)
assert near(pac[0], 0.4286, 5e-5) and near(pac[1], -0.4, 1e-10) and np.abs(pac[2:]).max() < 1e-10
# Sample PACF of a long seeded AR(2): within 4/sqrt(T) of the theory (SE 1/sqrt(T), T p. 47).
rng = np.random.default_rng(81)
T = 10000
e = rng.standard_normal(T + 500)
y = signal.lfilter([1.0], [1, -0.6, 0.4], e)[500:]
spac = sm.tsa.pacf(y, nlags=6)
assert np.all(np.abs(spac[1:3] - pac[:2]) < 4 / math.sqrt(T)) and np.all(np.abs(spac[3:]) < 4 / math.sqrt(T))
assert near(1 / math.sqrt(996), 0.0317, 5e-5) and near(2 / math.sqrt(176), 0.151, 5e-4)
# Table 2.1 (T p. 47): AIC picks p = 9, BIC picks p = 1.
aic = [-5.838, -5.837, -5.846, -5.845, -5.847, -5.847, -5.846, -5.847, -5.849, -5.847, -5.845, -5.843]
bic = [-5.833, -5.827, -5.831, -5.825, -5.822, -5.818, -5.812, -5.807, -5.805, -5.798, -5.791, -5.784]
assert int(np.argmin(aic)) + 1 == 9 and int(np.argmin(bic)) + 1 == 1
# The AR(2) companion's default read-outs (imported) print the same numbers.
o, status = cc.ar_python(1.75, -0.8, 1.0, -5.48715, -3.508837, 50)
assert status == "stationary" and (o["rho1"], o["rho2"], o["sd"], o["k"]) == ("0.972", "0.901", "7.121", "30.09")
print("§1 ok: AR(2) roots/triangle, gamma0, cycles 30.09/10.62/10.656, PACF, Table 2.1, companion")
```

---

## 2 · Forecasts, MA, ARMA → [[L08-02-forecasting-ma-arma]]

The forecast recursion, the closed forms L08-02 (7)–(10) and the ψ-weight variance (28) must agree with
the ar2-forecast page (E: −6.7954 … ; V: 1, 4.0625, …; limit sd 7.12069), and a seeded rerun of the
page's 10 000-path Monte Carlo must land within MC error of the limit. Then the MA(1) bound
$\lvert\rho_1\rvert\le\frac12$ on a fine grid, and ARMA(1,1) $(0.8,0.4)$: $\gamma_0=1.4444$, $\rho_1=0.5231$.

```python
# === §2 Forecasts, MA, ARMA (L08-02) ===
p1, p2, yn, yn1 = 1.75, -0.8, -5.487150, -3.508837
psi = mf.psi_weights([p1, p2], [], 60)
E = [p1 * yn + p2 * yn1]
E.append(p1 * E[0] + p2 * yn)
for h in range(2, 50):
    E.append(p1 * E[-1] + p2 * E[-2])
V = np.cumsum(psi[:50] ** 2)                                       # L08-02 (28)
closed = [p1 * yn + p2 * yn1, (p1 ** 2 + p2) * yn + p1 * p2 * yn1,  # L08-02 (7)-(10)
          (p1 ** 3 + 2 * p1 * p2) * yn + (p1 ** 2 * p2 + p2 ** 2) * yn1,
          (p1 ** 4 + 3 * p1 ** 2 * p2 + p2 ** 2) * yn + (p1 ** 3 * p2 + 2 * p1 * p2 ** 2) * yn1]
assert np.allclose(E[:4], closed) and np.allclose(E[:4], [-6.7954, -7.5023, -7.6927, -7.4603], atol=5e-5)
assert np.allclose(V[:4], [1, 4.0625, 9.1814, 15.7318], atol=5e-5)
assert near(V[1], 1 + p1 ** 2, 1e-12) and near(V[2], 1 + p1 ** 2 + (p1 ** 2 + p2) ** 2, 1e-12)
assert near(math.sqrt(V[-1]), 7.1206, 5e-5) and near(math.sqrt(mf.ar2_gamma0(p1, p2)), 7.12069, 5e-6)
# The page's Monte Carlo (M = 10 000 paths, 50 steps): our seeded run lands within MC error of 0 and 7.12.
rng = np.random.default_rng(1233)
M = 10000
yf = np.zeros((50, M))
yf[0] = p1 * yn + p2 * yn1 + rng.standard_normal(M)
yf[1] = p1 * yf[0] + p2 * yn + rng.standard_normal(M)
for h in range(2, 50):
    yf[h] = p1 * yf[h - 1] + p2 * yf[h - 2] + rng.standard_normal(M)
assert abs(yf[49].mean()) < 4 * 7.12 / math.sqrt(M) and abs(yf[49].std() - 7.1207) < 0.2
# MA(1) in Tsay's sign r = a - theta a_{-1}: rho1 = -theta/(1+theta^2); |rho1| <= 1/2 with the bound at theta = 1.
rho1 = lambda th: -th / (1 + th ** 2)
assert near(rho1(0.6), -0.4412, 5e-5) and rho1(0.5) == rho1(2.0) == -0.4
th = np.linspace(-5, 5, 100001)
assert near(np.abs(rho1(th)).max(), 0.5, 1e-12) and near(abs(th[np.argmax(np.abs(rho1(th)))]), 1.0, 1e-4)
assert np.allclose(ArmaProcess(ma=[1, -0.6]).acf(4), [1, rho1(0.6), 0, 0], atol=1e-12)
# ARMA(1,1), (phi, theta) = (0.8, 0.4): gamma0 = (1 - 2 phi theta + theta^2)/(1 - phi^2), rho1 (L08-02 (23)-(25)).
ph, th1 = 0.8, 0.4
g0 = (1 - 2 * ph * th1 + th1 ** 2) / (1 - ph ** 2)
r1 = (ph - th1) * (1 - ph * th1) / (1 - 2 * ph * th1 + th1 ** 2)
acf_arma = ArmaProcess(ar=[1, -ph], ma=[1, -th1]).acf(4)
assert near(g0, 1.4444, 5e-5) and near(r1, 0.5231, 5e-5) and np.allclose(acf_arma[1:3], [r1, ph * r1], atol=1e-12)
assert np.allclose(mf.psi_weights([ph], [th1], 4), [1, 0.4, 0.32, 0.256])
print("§2 ok: AR(2) forecast means/variances, 7.12 limit, MC, MA(1) bound, ARMA(1,1) 0.5231")
```

---

## 3 · Unit roots, Dickey–Fuller, spurious regression → [[L08-03-unit-roots-dickey-fuller]]

`df_tstats` is the figure's simulation with the same seed, so the quantiles printed in the figure and
here are identical; they must match Wooldridge's Table 18.2 to 0.06. `adfuller` with no lags equals the
hand $t$ ratio of the regression $\Delta y_t=c+u\,y_{t-1}+e_t$. The spurious-regression rate (66.2% at
$n=50$, Davidson–MacKinnon via W p. 579) and the telescoping identity behind the DF numerator
(L08-03 (21)) close the section.

```python
# === §3 Unit roots, Dickey-Fuller, spurious regression (L08-03) ===
def df_tstats(T=250, R=20000, seed=2026):
    """t ratio of u in Delta y = c + u y_{-1} + e under H0 (driftless RW): the figure's simulation, same seed."""
    rng = np.random.default_rng(seed)
    y = rng.standard_normal((R, T)).cumsum(axis=1)
    dy, yl = np.diff(y, axis=1), y[:, :-1]
    ylc = yl - yl.mean(axis=1, keepdims=True)
    b = (ylc * dy).sum(1) / (ylc ** 2).sum(1)
    resid = dy - dy.mean(1, keepdims=True) - b[:, None] * ylc
    se = np.sqrt((resid ** 2).sum(1) / (T - 3) / (ylc ** 2).sum(1))
    return b / se


t = df_tstats()
q = np.quantile(t, [0.01, 0.025, 0.05, 0.10])
assert np.allclose(q, [-3.43, -3.12, -2.86, -2.57], atol=0.06)        # W Table 18.2 (p. 575)
assert near((t < -1.645).mean(), 0.465, 0.01)
# One series: statsmodels' ADF agrees with the hand regression (same lag structure, constant only).
rng = np.random.default_rng(7)
rw = rng.standard_normal(500).cumsum()
stat, pval, *_ = adfuller(rw, maxlag=0, regression="c", autolag=None)
X = sm.add_constant(rw[:-1])
fit = sm.OLS(np.diff(rw), X).fit()
assert near(stat, fit.tvalues[1], 1e-8) and pval > 0.05
ar = signal.lfilter([1.0], [1, -0.5], rng.standard_normal(500))
assert adfuller(ar, maxlag=0, regression="c", autolag=None)[1] < 0.01
# Spurious regression (W p. 579): two independent RWs, n = 50, nominal 5% two-sided t test.
rng = np.random.default_rng(1974)
R, n = 10000, 50
xs = rng.standard_normal((R, n)).cumsum(1)
ys = rng.standard_normal((R, n)).cumsum(1)
xc, yc = xs - xs.mean(1, keepdims=True), ys - ys.mean(1, keepdims=True)
b1 = (xc * yc).sum(1) / (xc ** 2).sum(1)
u = yc - b1[:, None] * xc
tsp = b1 / np.sqrt((u ** 2).sum(1) / (n - 2) / (xc ** 2).sum(1))
assert near((np.abs(tsp) > stats.t.ppf(0.975, n - 2)).mean(), 0.662, 0.03)
# 3M drift (T eq. 2.37): t = 0.0103/0.002318 = 4.44; crossover (sigma/mu)^2 = 38.2 months (L08-03 (10)).
assert near(0.0103 / (0.0637 / math.sqrt(755)), 4.44, 5e-3) and near((0.0637 / 0.0103) ** 2, 38.2, 0.05)
# Telescoping (L08-03 (21)): sum p_{t-1} e_t = (p_T^2 - sum e_t^2)/2 exactly, p_0 = 0.
e = rng.standard_normal(300)
p = e.cumsum()
assert near((np.r_[0, p[:-1]] * e).sum(), (p[-1] ** 2 - (e ** 2).sum()) / 2, 1e-9)
assert near(stats.chi2.cdf(1, 1), 0.683, 5e-4)                        # P(chi2_1 < 1): DF numerator negative
print("§3 ok: DF quantiles", np.round(q, 2), "false rejection 46.5%, ADF = hand t, spurious 66%, telescoping")
```

---

## 4 · Long memory → [[L08-04-long-memory-arfima]]

The product recursion for $\rho_k$ is checked against the Gamma-function form for four values of $d$
(including a negative one, where $\Gamma(d)<0$: hence `gammasgn`), the PACF $d/(k-d)$ is recovered from
the ACF by Durbin–Levinson (T p. 102, property 4), and the asymptotic $k^{2d-1}$ law is within 1% at
$k=100$.

```python
# === §4 Long memory (L08-04) ===
for d in (0.1, 0.25, 0.4, -0.25):
    rr = mf.arfima_acf(d, 200)
    k = np.arange(1, 201)
    gam = special.gammasgn(d) * np.exp(special.gammaln(k + d) + special.gammaln(1 - d)       # Gamma ratio, log scale
                                       - special.gammaln(k - d + 1) - special.gammaln(d))
    assert np.allclose(rr[1:], gam, rtol=1e-9) and near(rr[1], d / (1 - d), 1e-12)        # L08-04 (7)-(10)
    assert np.allclose(mf.pacf_from_acf(rr, 8), d / (np.arange(1, 9) - d), atol=1e-9)    # PACF d/(k-d), T p. 102
r25, r4 = mf.arfima_acf(0.25, 100), mf.arfima_acf(0.4, 100)
assert np.allclose(r25[1:4], [1 / 3, 0.2381, 0.1948], atol=5e-5)
asym = special.gamma(1 - 0.4) / special.gamma(0.4) * 100 ** (2 * 0.4 - 1)          # (-d)!/(d-1)! k^(2d-1)
assert near(r4[100], 0.2673, 5e-5) and abs(asym / r4[100] - 1) < 0.01 and (2 / 3) ** 100 < 3e-18
coef = np.array([1, -0.25, -0.25 * 0.75 / 2, -0.25 * 0.75 * 1.75 / 6])               # (1-B)^d, L08-04 (3)
assert np.allclose(coef, [special.binom(0.25, j) * (-1) ** j for j in range(4)])
print("§4 ok: ARFIMA ACF = Gamma form, PACF d/(k-d), rho_100(0.4) = 0.267, binomial coefficients")
```

---

## 5 · Seasonal models → [[L08-05-seasonal-airline-model]]

statsmodels' `SARIMAX` reproduces the slides' and the page's airline fits on log AirPassengers for
$n=96$, 108 and 144 to the third decimal (log-likelihood 148.76, BIC −284.27 / −336.93 / −474.77), and
the BIC search over the 16 models picks $(0,1,1)(0,1,1)_{12}$. The out-of-sample RMSE comparison
(36.6 vs 63.3) is our computation, not the page's. The airline ACF L08-05 (11)–(12) is checked
against the ACF of the expanded MA polynomial, the corrected ARMA(26,13) coefficients against
`numpy.polymul`, and Tsay's January-effect regression against his own data file.

```python
# === §5 Seasonal models (L08-05) ===
AIR = np.array([112, 118, 132, 129, 121, 135, 148, 148, 136, 119, 104, 118, 115, 126, 141, 135, 125, 149, 170, 170, 158, 133, 114, 140,
                145, 150, 178, 163, 172, 178, 199, 199, 184, 162, 146, 166, 171, 180, 193, 181, 183, 218, 230, 242, 209, 191, 172, 194,
                196, 196, 236, 235, 229, 243, 264, 272, 237, 211, 180, 201, 204, 188, 235, 227, 234, 264, 302, 293, 259, 229, 203, 229,
                242, 233, 267, 269, 270, 315, 364, 347, 312, 274, 237, 278, 284, 277, 317, 313, 318, 374, 413, 405, 355, 306, 271, 306,
                315, 301, 356, 348, 355, 422, 465, 467, 404, 347, 305, 336, 340, 318, 362, 348, 363, 435, 491, 505, 404, 359, 310, 337,
                360, 342, 406, 396, 420, 472, 548, 559, 463, 407, 362, 405, 417, 391, 419, 461, 472, 535, 622, 606, 508, 461, 390, 432], float)
assert len(AIR) == 144 and AIR.sum() == 40363                        # seasonal.pdf slide 17 (Box-Jenkins Series G)
ly = np.log(AIR)


def airline(n):
    """ARIMA(0,1,1)x(0,1,1)_12 on log passengers 1949.1..(n); statsmodels prints +theta (Tsay's -theta)."""
    return SARIMAX(ly[:n], order=(0, 1, 1), seasonal_order=(0, 1, 1, 12)).fit(disp=False)


printed = {96: (-0.3941, -0.6129, -284.27), 108: (-0.3864, -0.5885, -336.93), 144: (-0.4018, -0.5569, -474.77)}
for n, (ma1, sma1, bic) in printed.items():
    m = airline(n)
    assert near(m.params[0], ma1, 2e-3) and near(m.params[1], sma1, 2e-3) and near(m.bic, bic, 0.02), (n, m.params, m.bic)
assert near(airline(96).llf, 148.76, 5e-3) and near(airline(144).aic, -483.39, 5e-3)
grid = {}
for i in (0, 1):
    for j in (0, 1):
        for k in (0, 1):
            for l in (0, 1):
                grid[(i, j, k, l)] = SARIMAX(ly[:108], order=(i, 1, j), seasonal_order=(k, 1, l, 12)).fit(disp=False).bic
assert min(grid, key=grid.get) == (0, 1, 0, 1)                         # the page: BIC picks (0,1,1)(0,1,1)_12
pred = np.exp(airline(108).get_forecast(36).predicted_mean)
tt = np.arange(144)
D = np.column_stack([np.ones(144), tt] + [(tt % 12 == mth).astype(float) for mth in range(1, 12)])
bdet = np.linalg.lstsq(D[:108], ly[:108], rcond=None)[0]
rmse_air = math.sqrt(np.mean((AIR[108:] - pred) ** 2))
rmse_det = math.sqrt(np.mean((AIR[108:] - np.exp(D[108:] @ bdet)) ** 2))
assert near(rmse_air, 36.6, 0.05) and near(rmse_det, 63.3, 0.05)
# Airline ACF (T p. 84) vs statsmodels' ACF of the expanded MA(s+1) polynomial (statsmodels sign: 1 + ...).
for th, TH, s, vals in [(0.678, 0.314, 4, (-0.4645, -0.2858, 0.1328)), (0.3864, 0.5885, 12, (-0.3362, -0.4371, 0.1470))]:
    poly = np.polymul([1, -th], np.r_[1, np.zeros(s - 1), -TH])
    acf = ArmaProcess(ma=poly).acf(s + 3)
    assert np.allclose([acf[1], acf[s], acf[s - 1], acf[s + 1]], [vals[0], vals[1], vals[2], vals[2]], atol=5e-5)
    assert near(acf[s + 1], acf[1] * acf[s], 1e-12) and np.abs(np.r_[acf[2:s - 1], acf[s + 2:]]).max() < 1e-12
# ARIMA(1,1,1)x(1,1,1)_12 = constrained ARMA(26,13) (L08-05 (16)-(18)): the corrected lag-12 and lag-13 coefficients.
phi, PHI = 0.3, 0.2
ar_full = np.polymul(np.polymul([1, -phi], np.r_[1, np.zeros(11), -PHI]), np.polymul([1, -1], np.r_[1, np.zeros(11), -1]))
assert len(ar_full) == 27                                              # degree 26
assert near(-ar_full[12], 1 + PHI, 1e-12) and near(-ar_full[13], -(1 + phi) * (1 + PHI), 1e-12)
assert near(-ar_full[1], 1 + phi, 1e-12) and near(-ar_full[2], -phi, 1e-12) and near(-ar_full[26], -phi * PHI, 1e-12)
# CRSP Decile 1, January effect (T Ex. 2.4, p. 88): R_t = 0.002864 + 0.125251 Jan_t.
dec = np.loadtxt(DATA / "m-deciles08.txt", skiprows=1)
jan = ((dec[:, 0] // 100) % 100 == 1).astype(float)
ols = sm.OLS(dec[:, 1], sm.add_constant(jan)).fit()
assert len(dec) == 468 and np.allclose(ols.params, [0.002864, 0.125251], atol=5e-7)
assert np.allclose(ols.bse, [0.003333, 0.011546], atol=5e-7) and near(ols.rsquared, 0.2016, 5e-5)
print(f"§5 ok: airline fits = slides, BIC winner, RMSE {rmse_air:.1f} vs {rmse_det:.1f}, ACF, ARMA(26,13), January 0.1253")
```

---

## 6 · ARCH and GARCH: moments, forecasts, maximum likelihood → [[L08-06-arch-garch]]

`garch_var` is the recursion (T 3.16) as one linear filter; `nll_garch` is the conditional
log-likelihood, Gaussian or standardized $t$ (L08-06 (15), (16)–(17)); `fit_garch` maximises it by
Nelder–Mead with $\sigma_1^2$ fixed at the sample variance (T p. 134). Checks: the Gaussian kurtosis
formula (25) against a seeded million-draw simulation (with a small $\alpha_1$ so that the sample kurtosis
converges), Tsay Ex. 3.3 and Table 3.1, the IGARCH line, the Petrobras numbers, recovery of the truth
on simulated data, and a fit to Tsay's daily S&P 500 (1999–2008, $T=2515$). On that file the
Gaussian MLE gives $(\hat\alpha_0,\hat\alpha_1,\hat\beta_1)=(1.01\times10^{-6},\ 0.0710,\ 0.9238)$, persistence
0.9948, and the $t$ fit has the higher log-likelihood.

```python
# === §6 ARCH and GARCH: moments, forecasts, maximum likelihood (L08-06) ===
def garch_var(a, w, al, be, s0):
    """sigma^2_t = w + al a^2_{t-1} + be sigma^2_{t-1} (T eq. 3.16) as one linear filter; sigma^2_1 = s0."""
    x = w + al * np.r_[0.0, a[:-1] ** 2]
    x[0] = s0
    return signal.lfilter([1.0], [1.0, -be], x)


def nll_garch(par, a, s0, dist="normal"):
    """Negative conditional log-likelihood, normal (L08-06 (15)) or standardized t (L08-06 (16)-(17))."""
    w, al, be = par[:3]
    if w <= 0 or al < 0 or be < 0 or al + be >= 1:
        return 1e12
    s2 = garch_var(a, w, al, be, s0)
    if dist == "normal":
        return 0.5 * np.sum(np.log(2 * np.pi * s2) + a ** 2 / s2)
    nu = par[3]
    if nu <= 2.05:
        return 1e12
    c = special.gammaln((nu + 1) / 2) - special.gammaln(nu / 2) - 0.5 * np.log((nu - 2) * np.pi)
    return -np.sum(c - 0.5 * np.log(s2) - (nu + 1) / 2 * np.log1p(a ** 2 / ((nu - 2) * s2)))


def fit_garch(a, dist="normal"):
    """Conditional MLE by Nelder-Mead; sigma^2_1 fixed at the sample variance (T p. 134)."""
    s0 = a.var()
    x0 = [0.05 * s0, 0.05, 0.90] + ([8.0] if dist == "t" else [])
    res = optimize.minimize(nll_garch, x0, args=(a, s0, dist), method="Nelder-Mead",
                            options=dict(xatol=1e-10, fatol=1e-10, maxiter=40000, maxfev=40000))
    return res.x, -res.fun


def sim_garch(n, w, al, be, rng, nu=None, burn=1000):
    """Simulate a GARCH(1,1) with N(0,1) or standardized t_nu innovations."""
    z = rng.standard_normal(n + burn) if nu is None else rng.standard_t(nu, n + burn) * math.sqrt((nu - 2) / nu)
    a, s2 = np.empty(n + burn), w / (1 - al - be)
    for t_ in range(n + burn):
        a[t_] = math.sqrt(s2) * z[t_]
        s2 = w + al * a[t_] ** 2 + be * s2
    return a[burn:]


assert np.allclose(garch_var(np.arange(5.0), 0.1, 0.2, 0.7, 1.0), [1.0, 0.8, 0.86, 1.502, 2.9514])   # recursion by hand
# ARCH(1) (L08-06 (8), (12)): Intel (3.12) uncond. sd and kurtosis.
assert near(math.sqrt(0.0111 / (1 - 0.356)), 0.1313, 5e-5) and near(3 * (1 - 0.356 ** 2) / (1 - 3 * 0.356 ** 2), 4.227, 5e-4)
assert near(math.sqrt(0.00070027 / (1 - 0.36978713)), 0.0333, 5e-5)    # Petrobras ARCH(1)
# GARCH(1,1) Gaussian kurtosis (L08-06 (25)) against a long seeded simulation (alpha small: 8th moment finite).
w, al, be = 0.1, 0.05, 0.90
kg = 6 * al ** 2 / (1 - 2 * al ** 2 - (al + be) ** 2)
sim = sim_garch(1_000_000, w, al, be, np.random.default_rng(3))
assert near(np.mean(sim ** 2), w / (1 - al - be), 0.03) and abs(stats.kurtosis(sim) - kg) < 0.05
# Tsay Ex. 3.3 (3.19): persistence, sigma_inf, half-life, kurtosis; the 0.9772 on p. 137 is 0.9727.
w, al, be = 0.000086, 0.1216, 0.8511
pers = al + be
assert near(pers, 0.9727, 1e-12) and near(w / (1 - pers), 0.003150, 5e-7) and near(math.sqrt(w / (1 - pers)), 0.0561, 5e-5)
assert near(math.log(0.5) / math.log(pers), 25.04, 5e-3) and near(3 + 6 * al ** 2 / (1 - 2 * al ** 2 - pers ** 2), 6.654, 5e-4)
s1 = 0.0536
fc = [s1 ** 2]
for _ in range(4):
    fc.append(w + pers * fc[-1])                                       # (3.17)
closed = [w / (1 - pers) + pers ** (l - 1) * (s1 ** 2 - w / (1 - pers)) for l in range(1, 6)]
assert np.allclose(fc, closed) and np.allclose(np.sqrt(fc), [0.0536, 0.0537, 0.0537, 0.0538, 0.0538], atol=1.2e-4)
assert near(0.9583 - 0.8456, 0.1127, 1e-12)                            # two-pass estimate (T p. 140)
ig = [s1 ** 2]
for _ in range(9):
    ig.append(0.000119 + 1.0 * ig[-1])
assert np.allclose(np.diff(ig), 0.000119)                              # IGARCH forecasts are a line (3.22)
# Petrobras normal GARCH (garchmodeling.html): persistence, sigma_inf, half-life, excess kurtosis, LR.
w, al, be = 2.254954e-05, 0.1031668, 0.8768059
assert near(al + be, 0.97997, 5e-6) and near(math.sqrt(w / (1 - al - be)), 0.03356, 5e-6)
assert near(math.log(0.5) / math.log(al + be), 34.26, 5e-3) and near(6 * al ** 2 / (1 - 2 * al ** 2 - (al + be) ** 2), 3.477, 5e-4)
assert near(2 * (11151.72 - 10672.32), 958.8, 1e-9)
# MLE recovers the truth on a seeded sample (normal and t), and runs on Tsay's daily S&P 500 file.
rng = np.random.default_rng(11)
a = sim_garch(4000, 2e-5, 0.08, 0.90, rng)
th_n, ll_n = fit_garch(a)
assert abs(th_n[1] - 0.08) < 0.03 and abs(th_n[2] - 0.90) < 0.04
a_t = sim_garch(4000, 0.02, 0.08, 0.90, np.random.default_rng(12), nu=7)
th_t, ll_t = fit_garch(a_t, "t")
assert abs(th_t[3] - 7) < 2.5 and abs(th_t[1] + th_t[2] - 0.98) < 0.03 and ll_t > fit_garch(a_t)[1]
gs = np.loadtxt(DATA / "d-gmsp9908.txt", skiprows=1)
sp = np.log1p(gs[:, 2])
sp = sp - sp.mean()
th_sp, ll_sp = fit_garch(sp)
th_spt, ll_spt = fit_garch(sp, "t")
assert len(sp) == 2515 and 0.98 < th_sp[1] + th_sp[2] < 1 and 0.03 < th_sp[1] < 0.15 and ll_spt > ll_sp
# The Volatility Dial's default read-outs (imported) agree.
o, regime, _ = cc.ga_python(0.86, 0.1216, 0.8511, 5.36, True, 7.04, 60)
assert regime == "stationary" and (o["pers"], o["hl"], o["sinf"], o["kg"]) == ("0.9727", "25.04", "5.61", "3.654")
print("§6 ok: ARCH/GARCH moments, Table 3.1, IGARCH line, Petrobras numbers, MLE (normal, t), S&P 500:",
      np.round(th_sp, 6), "persistence", round(th_sp[1] + th_sp[2], 4))
```

---

## 7 · Asymmetry and tails → [[L08-07-garch-family-asymmetry-tails]]

The APARCH-to-GJR mapping L08-07 (6)–(7) is checked both numerically and as an identity between the
two news-impact curves; the literal reading of the glossary's GJR formula is shown to be nonstationary.
$E\lvert\varepsilon\rvert$ for the standardized $t$ (T p. 143) is checked against quadrature (0.7595 at
$\nu=7.04$), Tiao's two forms of the kurtosis (T p. 166) against each other (12.55 for the Petrobras
GARCH-$t$), and the AIC ladder of the glossary page is recomputed.

```python
# === §7 Asymmetry and tails (L08-07) ===
ag, gg, bg = 0.09234234, 0.2083503, 0.8817760                        # fGarch leverage, delta = 2 (APARCH form)
assert near(ag * (1 - gg) ** 2, 0.05787, 5e-6) and near(ag * (1 + gg) ** 2, 0.13483, 5e-6)
assert near(4 * ag * gg, 0.07696, 5e-6) and near(ag * (1 + gg ** 2) + bg, 0.97813, 5e-6)
assert ag + gg / 2 + bg > 1                                            # the literal indicator reading is not stationary
z = np.linspace(-6, 6, 2001)
nic_aparch = ag * (np.abs(z) - gg * z) ** 2
nic_gjr = (ag * (1 - gg) ** 2 + 4 * ag * gg * (z < 0)) * z ** 2      # the same curve written as GJR
assert np.allclose(nic_aparch, nic_gjr)
at_, gt_ = 0.0964078, 0.3458799                                        # T-GARCH (delta = 1)
assert near(0.09641 * 1.34588, 0.12976, 5e-6) and near(at_ * (1 + gt_), 0.12975, 5e-6) and near(at_ * (1 - gt_), 0.06306, 5e-5)
ae, ge = -0.05549, 0.18138                                             # rugarch EGARCH: ratio exp(-2 alpha c)
assert near(math.exp(-2 * ae * 1), 1.117, 5e-4) and near(math.exp(-2 * ae * 2), 1.249, 5e-4)
assert near(ae * -1 + ge * 1, 0.23687, 5e-6) and near(ae * 1 + ge * 1, 0.12589, 5e-6)
# E|eps|: sqrt(2/pi) for N(0,1); for the standardized t (T p. 143) by formula and by quadrature.
assert near(integrate.quad(lambda x: abs(x) * stats.norm.pdf(x), -np.inf, np.inf)[0], math.sqrt(2 / math.pi), 1e-9)
nu = 7.04
sc = math.sqrt((nu - 2) / nu)
eabs_formula = 2 * math.sqrt(nu - 2) * math.exp(special.gammaln((nu + 1) / 2) - special.gammaln(nu / 2)) / ((nu - 1) * math.sqrt(math.pi))
eabs_quad = integrate.quad(lambda x: abs(x) * stats.t.pdf(x / sc, nu) / sc, -np.inf, np.inf)[0]
assert near(eabs_formula, eabs_quad, 1e-8) and near(eabs_formula, 0.7595, 5e-5)
# Tiao's kurtosis formula (T p. 166): the general and the t forms agree; Petrobras GARCH-t total 12.55.
al, be, nu = 0.07428964, 0.9094674, 7.042551
kg = 6 * al ** 2 / (1 - 2 * al ** 2 - (al + be) ** 2)
K = 6 / (nu - 4)
ka1 = (K + kg + 5 / 6 * K * kg) / (1 - K * kg / 6)
ka2 = (6 + (nu + 1) * kg) / (nu - 4 - kg)
assert near(ka1, ka2, 1e-9) and near(kg, 1.563, 5e-4) and near(ka1, 12.55, 0.01)
assert 1 - 2 * al ** 2 * (nu - 1) / (nu - 4) - (al + be) ** 2 > 0
ll = {"GARCH": (11151.72, 3), "GJR": (11174.01, 4), "EGARCH": (11173.14, 5), "GARCH-t": (11292.37, 4), "skew-t": (11297.85, 5)}
aic_ = {k: -2 * v + 2 * p for k, (v, p) in ll.items()}
assert min(aic_, key=aic_.get) == "skew-t" and near(aic_["GARCH"], -22297.44, 1e-6)
assert near(-4.3229 * 5167, -22336.4, 0.1)                             # rugarch's per-observation AIC, scaled back
print("§7 ok: APARCH -> GJR mapping, EGARCH ratios, E|eps| = 0.7595, Tiao 12.55, AIC ladder")
```

---

## 8 · Stochastic volatility → [[L08-08-stochastic-volatility]]

Closed-form moments L08-08 (5)–(9) for Tsay Ex. 12.3 and the Petrobras SV-$t$. The ACF formula is then
checked on iid draws of the pair $(h_t,h_{t-k})$ from its bivariate normal: this isolates the formula from
the very slow convergence of sample autocorrelations of $a_t^2$ when $\phi=0.984$. A simulated SV path
with Tsay's milder parameters checks kurtosis and the lag-1 correlation in the time domain. Last, the
moments of $\ln\varepsilon^2$ used by the QML linearisation and the completing-the-square identity behind
(12.23).

```python
# === §8 Stochastic volatility (L08-08) ===
def sv_moments(mu_h, s2h, phi_):
    """E(a^2), kurtosis 3 e^{s2h}, corr(a_t^2, a_{t-1}^2): L08-08 (5)-(9), Gaussian eps."""
    return math.exp(mu_h + s2h / 2), 3 * math.exp(s2h), (math.exp(s2h * phi_) - 1) / (3 * math.exp(s2h) - 1)


mu_h, s2h = 0.454 / (1 - 0.837), 0.086 / (1 - 0.837 ** 2)             # Tsay Ex. 12.3
Ea2, kurt, c1 = sv_moments(mu_h, s2h, 0.837)
assert near(mu_h, 2.785, 5e-4) and near(s2h, 0.2872, 5e-5) and near(Ea2, 18.71, 5e-3) and near(kurt, 3.998, 5e-4)
assert near(math.sqrt(Ea2), 4.33, 5e-3) and near(c1, 0.0906, 1e-4)
phi_, sig_ = 0.9842135, 0.1387539                                     # PBR SV-t posterior means (stochvol h = log variance)
s2h_p = sig_ ** 2 / (1 - phi_ ** 2)
_, kurt_p, c1_p = sv_moments(-0.4190952, s2h_p, phi_)
assert near(s2h_p, 0.6146, 5e-5) and near(kurt_p, 5.547, 5e-4) and near(c1_p, 0.1828, 5e-5)
# The ACF formula, checked on iid draws of (h_t, h_{t-k}) from their bivariate normal (no time-series convergence issue).
rng = np.random.default_rng(88)
nn = 4_000_000
for kk in (1, 20):
    cov = s2h_p * np.array([[1, phi_ ** kk], [phi_ ** kk, 1]])
    hh = rng.multivariate_normal([0, 0], cov, nn)
    a2 = np.exp(hh) * rng.standard_normal((nn, 2)) ** 2
    formula = (math.exp(s2h_p * phi_ ** kk) - 1) / (3 * math.exp(s2h_p) - 1)
    assert abs(np.corrcoef(a2[:, 0], a2[:, 1])[0, 1] - formula) < 0.02, kk
# A simulated SV path (Tsay 12.3 parameters): sample kurtosis and lag-1 corr of a^2 near the formulas.
nT = 2_000_000
hT = signal.lfilter([1.0], [1, -0.837], 0.454 + math.sqrt(0.086) * rng.standard_normal(nT + 2000))[2000:]
aT = np.exp(hT / 2) * rng.standard_normal(nT)
assert abs(np.mean(aT ** 2) / Ea2 - 1) < 0.02 and abs(stats.kurtosis(aT, fisher=False) - kurt) < 0.15
assert abs(np.corrcoef(aT[1:] ** 2, aT[:-1] ** 2)[0, 1] - c1) < 0.01
# ln(eps^2) for eps ~ N(0,1): mean -1.2704, variance pi^2/2 (L08-08 (11)).
m1 = 2 * integrate.quad(lambda x: math.log(x * x) * stats.norm.pdf(x), 0, np.inf)[0]        # symmetric: twice (0, inf)
m2 = 2 * integrate.quad(lambda x: math.log(x * x) ** 2 * stats.norm.pdf(x), 0, np.inf)[0]
assert near(m1, -1.2704, 5e-5) and near(m2 - m1 ** 2, math.pi ** 2 / 2, 1e-6)
# Completing the square (L08-08 (17)): (x-a)^2 A + (x-b)^2 C = (x-c)^2 (A+C) + (a-b)^2 AC/(A+C).
xg, A_, a_, C_, b_ = 0.7, 1.0, -0.3, 0.837 ** 2, 1.9
c_ = (A_ * a_ + C_ * b_) / (A_ + C_)
assert near((xg - a_) ** 2 * A_ + (xg - b_) ** 2 * C_, (xg - c_) ** 2 * (A_ + C_) + (a_ - b_) ** 2 * A_ * C_ / (A_ + C_), 1e-12)
print("§8 ok: SV moments (Tsay 12.3, PBR), ACF formula by MC, simulated path, E ln chi2_1, (12.23) identity")
```

---

## 9 · Bayesian GARCH → [[L08-09-bayesian-garch]]

The M0 prior and the prior weight $4/884$; the conjugate update as a weighted average on a simulated
sample. Then the GARCH(1,1)-$t$ posterior of `bayesGARCH` (L08-09 (12)–(15): $h_0=r_0=0$, $V(r\mid h)=h$,
truncated $N(0,1000)$ priors, $\nu-2\sim\text{Exp}(0.01)$, no stationarity constraint) is sampled by a
random-walk Metropolis started at the MLE, on 2000 simulated observations with truth
$(0.02, 0.08, 0.90, \nu=7)$. Run of 2026-10-27: acceptance 0.20; posterior means
$(0.020, 0.079, 0.908, 5.84)$ after 5000 burn-in; $\Pr(\alpha_1+\beta>1\mid\text{data})=0.041$. Every posterior mean
is within four posterior sds of the truth. `bayesGARCH` itself uses a better proposal (Ardia–Hoogerheide's
GLS approximation): this sampler is the simplest correct one, not a fast one.

```python
# === §9 Bayesian GARCH (L08-09) ===
m_r2, n0, n = 0.0006617694, 1506, 1760                                # bayes-garch.pdf slides 6-8
a0_, b0_ = 5.0, 4 * m_r2
assert near(b0_ / (a0_ - 1), m_r2, 1e-15) and near(math.sqrt(b0_ ** 2 / ((a0_ - 1) ** 2 * (a0_ - 2))), 0.000382, 5e-7)
w_prior = (a0_ - 1) / (a0_ - 1 + n / 2)
assert near(w_prior, 4 / 884, 1e-12) and near(w_prior, 0.0045, 5e-5)
# M0 conjugate update on a simulated sample: posterior IG(a + n/2, b + S/2) = weighted average of prior mean and S/n.
r0 = 0.033 * np.random.default_rng(5).standard_normal(n)
S = float((r0 ** 2).sum())
post_mean = (b0_ + S / 2) / (a0_ + n / 2 - 1)
assert near(post_mean, w_prior * m_r2 + (1 - w_prior) * S / n, 1e-15)
# M1 prior sd of mu: sqrt(100 V/(n0 - 1)) = 0.006627; M2 prior sds 10 s_a, 10 s_b.
assert near(math.sqrt(100 * 0.0006609406 / (n0 - 1)), 0.006627, 5e-7) and near(10 * 0.0009933758, 0.00993, 5e-6)


def logpost_bgarch(par, r):
    """log posterior of bayesGARCH's GARCH(1,1)-t: h_0 = 0, r_0 = 0, V(r|h) = h (L08-09 (12)-(15))."""
    w, al, be, nu = par
    if w <= 0 or al <= 0 or be <= 0 or nu <= 2:
        return -np.inf
    x = w + al * np.r_[0.0, r[:-1] ** 2]
    h = signal.lfilter([1.0], [1.0, -be], x)                          # h_1 = w since h_0 = r_0 = 0
    c = special.gammaln((nu + 1) / 2) - special.gammaln(nu / 2) - 0.5 * np.log((nu - 2) * np.pi)
    ll_ = np.sum(c - 0.5 * np.log(h) - (nu + 1) / 2 * np.log1p(r ** 2 / ((nu - 2) * h)))
    lp = -(w ** 2 + al ** 2 + be ** 2) / 2000 - 0.01 * (nu - 2)      # N(0, 1000) truncated; nu - 2 ~ Exp(0.01)
    return ll_ + lp


def rw_metropolis(r, start, steps, iters, seed):
    """Random-walk Metropolis on (w, alpha, beta, nu); returns draws and the acceptance rate."""
    rng_ = np.random.default_rng(seed)
    cur, lpc = np.array(start, float), logpost_bgarch(start, r)
    out, acc = np.empty((iters, 4)), 0
    for i in range(iters):
        prop = cur + steps * rng_.standard_normal(4)
        lpp = logpost_bgarch(prop, r)
        if math.log(rng_.uniform()) < lpp - lpc:
            cur, lpc, acc = prop, lpp, acc + 1
        out[i] = cur
    return out, acc / iters


true = (0.02, 0.08, 0.90, 7.0)                                        # standardized-return scale, like GARCH11-SVar1
rb = sim_garch(2000, *true[:3], np.random.default_rng(21), nu=true[3])
mle, _ = fit_garch(rb, "t")
draws, acc = rw_metropolis(rb, mle, np.array([0.004, 0.008, 0.010, 0.8]), 20000, seed=22)
post = draws[5000:]
pm, psd = post.mean(0), post.std(0)
assert 0.15 < acc < 0.6 and np.all(np.abs(pm - np.array(true)) < 4 * psd + 1e-3)
p_nonstat = float((post[:, 1] + post[:, 2] > 1).mean())
assert p_nonstat < 0.1 and abs(pm[1] + pm[2] - (mle[1] + mle[2])) < 0.02
# The page's Bayes vs ML numbers (GARCH11-SVar1.html): persistence and half-life.
pb, pm_ = 0.08502667 + 0.89402444, 0.073478 + 0.910218
assert near(pb, 0.979051, 5e-7) and near(pm_, 0.983696, 5e-7)
assert near(math.log(0.5) / math.log(pb), 32.74, 5e-3) and near(math.log(0.5) / math.log(pm_), 42.17, 5e-3)
print(f"§9 ok: IG update (prior weight 0.45%), MH acceptance {acc:.2f}, posterior means {np.round(pm, 3)},",
      f"Pr(alpha+beta>1) = {p_nonstat:.4f}, Bayes vs ML persistence")
```

---

## 10 · Run it

```python
print("ALL L08 CHECKS PASSED")
```

Output of the run on 2026-10-27 (abridged to the section lines):

```text
§1 ok: AR(2) roots/triangle, gamma0, cycles 30.09/10.62/10.656, PACF, Table 2.1, companion
§2 ok: AR(2) forecast means/variances, 7.12 limit, MC, MA(1) bound, ARMA(1,1) 0.5231
§3 ok: DF quantiles [-3.45 -3.16 -2.87 -2.58] false rejection 46.5%, ADF = hand t, spurious 66%, telescoping
§4 ok: ARFIMA ACF = Gamma form, PACF d/(k-d), rho_100(0.4) = 0.267, binomial coefficients
§5 ok: airline fits = slides, BIC winner, RMSE 36.6 vs 63.3, ACF, ARMA(26,13), January 0.1253
§6 ok: ARCH/GARCH moments, Table 3.1, IGARCH line, Petrobras numbers, MLE (normal, t), S&P 500: [1.00000e-06 7.10430e-02 9.23751e-01] persistence 0.9948
§7 ok: APARCH -> GJR mapping, EGARCH ratios, E|eps| = 0.7595, Tiao 12.55, AIC ladder
§8 ok: SV moments (Tsay 12.3, PBR), ACF formula by MC, simulated path, E ln chi2_1, (12.23) identity
§9 ok: IG update (prior weight 0.45%), MH acceptance 0.20, posterior means [0.02  0.079 0.908 5.838], Pr(alpha+beta>1) = 0.0406, Bayes vs ML persistence
ALL L08 CHECKS PASSED
```

---

## Links

- Unit: [[L08-00-map]] · [[L08-10-formulas]] · [[L08-11-pitfalls]]
- The companions' own checks: `companions/check_companions.py`; the figures' asserts: `figures/make_figures.py`
- Class 1 computations (AR(1), VAR(1)): [[../L01/L01-11-python|L01-11]]
- Rules: [[../../rules/04_arima_raiz_unitaria|rules/04]] · [[../../rules/05_espaco_estados_volatilidade|rules/05]]
