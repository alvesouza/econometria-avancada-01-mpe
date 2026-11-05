---
tags: [notes, lecture-07, python, reference-implementation, gibbs, metropolis-hastings]
date: 2026-10-25
status: taught
source: "L07_python_checks.py (this folder; the code below is extracted from it verbatim); figures/make_figures.py (data, eight-schools posterior, hierarchical Gibbs, Tobit moments, efficiency ratios) reused by import; numbers from L07-01 … L07-06 and W Tables 8.1, 12.1, 17.1, 17.3"
---

# Class 7 · Python — every sampler of the class, asserted against the sources

> Every routine the class needs, each followed by the `assert`s that tie it to a printed number.
> numpy, scipy, statsmodels and the `wooldridge` data only — **no PyMC, no scikit-learn**: every Gibbs and
> Metropolis–Hastings step is written out, as the slides write it. The lecturer's R is the reference, never
> the code. **The file is the source of truth:** `Notas/L07/L07_python_checks.py`; the blocks below are
> copied from it verbatim, section by section.
> Prev: [[L07-08-pitfalls]] · Map: [[L07-00-map]] · Formulas: [[L07-07-formulas]]

**Run:** `python Notas/L07/L07_python_checks.py` — about two minutes (the samplers); it prints one line per
section and ends with `ALL L07 CHECKS PASSED` (§8). The first disagreement aborts with an `AssertionError`
naming the quantity and the printed value. Data: `pip install wooldridge` (allowed by the project plan).

**Reused, not rewritten.**

| Existing code | What it supplies | Used in |
|---|---|---|
| `figures/make_figures.py` (imported as `mf`) | eight-schools data, `schools_conditional`, `schools_tau_posterior`; pregnancy data and `gibbs_hlm` (the site's sampler, ported); `gls_efficiency`; `ar1_ratios`; `tobit_moments`, `p_zero_slide`; `t_weight`, `mixture_pdf` | §1, §2, §4, §5, §7 |
| `companions/check_companions.py` | the two pages recomputed and compared with their JavaScript under `node` | cited, not imported: it checks the **pages** |
| `statsmodels` `OLS`, `WLS`, `Probit`, `Logit` | the frequentist fits of W's tables | §1, §3, §5, §6 |

What is new here, and why: no existing project code samples these models. `statsmodels` has no Bayesian
samplers and no Tobit; its `GLSAR` iterates Cochrane–Orcutt, not Prais–Winsten, so PW is three lines here.

---

```python
"""Class 7 (L07) reference implementation with self-checks against the sources' printed numbers.

Run: python Notas/L07/L07_python_checks.py   (numpy, scipy, statsmodels, wooldridge; no scikit-learn, no PyMC)
Every section asserts the numbers of one section note and prints a one-line summary; the first
mismatch aborts with an AssertionError naming it. Shown section by section in L07-09-python.md.

Reused, not rewritten: figures/make_figures.py (imported as mf) supplies the eight-schools data and
exact posterior in tau, the pregnant-women data and the port of the site's hierarchical Gibbs sampler,
the GLS/OLS efficiency ratio, the AR(1) variance ratios, the Tobit moments and the ordered-probit
probabilities. Importing it draws nothing (build() runs only as __main__).
Data for the Wooldridge tables come from the `wooldridge` package (pip install wooldridge).
"""
import pathlib
import sys

import numpy as np
import statsmodels.api as sm
import wooldridge
from scipy import integrate, optimize, stats
from scipy.special import gammaln

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent / "figures"))
import make_figures as mf  # noqa: E402


def near(x, printed, dec):
    """True when x rounds to the printed value at `dec` decimals (half a unit in the last place)."""
    return abs(x - printed) <= 0.5 * 10.0 ** -dec + 1e-9


def check(x, printed, dec, what):
    assert near(x, printed, dec), f"{what}: computed {x!r}, source prints {printed}"
```

## 0 · Set-up, and the two samplers every note reuses

`check(x, printed, dec)` passes when `x` rounds to the printed value at `dec` decimals. `rtruncnorm` is slide 26's inverse-CDF draw (note 03 (15)), with the upper-tail reflection; `draw_beta` is the general-Ω conditional (note 01 (8)) — the boxed result of the map.


```python
# ============================================================================ shared samplers
def rtruncnorm(rng, mu, sd, a, b):
    """Draw N(mu, sd^2) truncated to [a, b] by the inverse CDF (GLM3 slide 26).

    y = mu + sd * Phi^-1( u Phi((b-mu)/sd) + (1-u) Phi((a-mu)/sd) ), u ~ U(0, 1).
    Vectorized over mu, a, b. Works on the upper tail by symmetry so Phi^-1 is never asked for 1 - 1e-17.
    """
    mu, a, b = np.broadcast_arrays(np.asarray(mu, float), np.asarray(a, float), np.asarray(b, float))
    u = rng.uniform(size=mu.shape)
    al, be = (a - mu) / sd, (b - mu) / sd
    flip = al > 0                                   # whole interval in the upper tail: reflect
    lo = np.where(flip, -be, al)
    hi = np.where(flip, -al, be)
    z = stats.norm.ppf(u * stats.norm.cdf(hi) + (1 - u) * stats.norm.cdf(lo))
    return mu + sd * np.where(flip, -z, z)


def draw_beta(rng, X, y, prec_w, sigma2, b0, V0inv):
    """beta | . ~ N(b1, V1), V1^-1 = V0^-1 + X' W X / sigma2, V1^-1 b1 = V0^-1 b0 + X' W y / sigma2.

    prec_w: vector of weights (diagonal of Omega^-1) or a full matrix Omega^-1. GLM3 slide 5.
    """
    XtW = X.T * prec_w if np.ndim(prec_w) == 1 else X.T @ prec_w
    P = V0inv + XtW @ X / sigma2
    V1 = np.linalg.inv(P)
    b1 = V1 @ (V0inv @ b0 + XtW @ y / sigma2)
    return rng.multivariate_normal(b1, V1), b1, V1
```

## 1 · GLS, WLS and Case I → [[L07-01-general-covariance-gls]]

OLS on $(Py,PX)$ = GLS; W Table 8.1 from the `401KSUBS` data; FGLS; a Gibbs sampler with a random-walk MH step for α on the slide-8 design.


```python
# ============================================================================ 1 · general covariance, GLS, WLS (L07-01)
def section1():
    rng = np.random.default_rng(1)
    n = 40
    X = np.column_stack([np.ones(n), rng.normal(size=n)])
    A = rng.normal(size=(n, n))
    Omega = A @ A.T / n + np.eye(n)                       # an arbitrary known covariance
    y = X @ np.array([1.0, 2.0]) + np.linalg.cholesky(Omega) @ rng.normal(size=n)
    L = np.linalg.cholesky(Omega)
    P = np.linalg.inv(L)                                  # P Omega P' = I (slide 4)
    assert np.allclose(P @ Omega @ P.T, np.eye(n))
    b_star = np.linalg.lstsq(P @ X, P @ y, rcond=None)[0]   # OLS on (Py, PX)
    Oi = np.linalg.inv(Omega)
    b_gls = np.linalg.solve(X.T @ Oi @ X, X.T @ Oi @ y)     # (X'O^-1X)^-1 X'O^-1 y
    assert np.allclose(b_star, b_gls)
    # full conditional with a vague prior collapses to GLS (slide 5 with V0^-1 -> 0)
    _, b1, V1 = draw_beta(rng, X, y, Oi, 2.0, np.zeros(2), np.zeros((2, 2)))
    assert np.allclose(b1, b_gls) and np.allclose(V1, 2.0 * np.linalg.inv(X.T @ Oi @ X))

    # Wooldridge Example 8.6 (Table 8.1, p. 257): nettfa on inc, single people (fsize = 1), WLS weights 1/inc
    d = wooldridge.data("401ksubs")
    d = d[d.fsize == 1]
    Xd = sm.add_constant(d[["inc"]])
    ols = sm.OLS(d.nettfa, Xd).fit(cov_type="HC0")
    wls = sm.WLS(d.nettfa, Xd, weights=1 / d.inc).fit()
    check(len(d), 2017, 0, "Table 8.1 n")
    check(ols.params["inc"], 0.821, 3, "OLS inc")
    check(ols.bse["inc"], 0.104, 3, "OLS inc robust SE")
    check(ols.params["const"], -10.57, 2, "OLS intercept")
    check(wls.params["inc"], 0.787, 3, "WLS inc")
    check(wls.bse["inc"], 0.063, 3, "WLS inc SE")
    check(wls.params["const"], -9.58, 2, "WLS intercept")
    check(wls.bse["const"], 1.65, 2, "WLS intercept SE")
    check(ols.rsquared, 0.0827, 4, "OLS R2")
    check(wls.rsquared, 0.0709, 4, "WLS R2")
    # WLS is OLS on the transformed variables (8.25)-(8.26): divide every column, the constant too, by sqrt(h)
    sh = np.sqrt(d.inc.values)
    b_tr = np.linalg.lstsq(Xd.values / sh[:, None], d.nettfa.values / sh, rcond=None)[0]
    assert np.allclose(b_tr, wls.params.values)

    # Case I, h(x, alpha) = exp(alpha0 + alpha1 x), slide-8 design: n = 100, alpha = (1, 1), sigma^2 = 1
    n = 100
    x = rng.normal(size=n)
    Xh = np.column_stack([np.ones(n), x])
    beta_true, alpha_true = np.array([2.0, 4.0]), np.array([1.0, 1.0])
    yh = Xh @ beta_true + np.sqrt(np.exp(Xh @ alpha_true)) * rng.normal(size=n)
    # FGLS (W 8.30-8.33) = the slide's initial value for alpha: regress log(e_ols^2) on x
    b_ols = np.linalg.lstsq(Xh, yh, rcond=None)[0]
    g = np.linalg.lstsq(Xh, np.log((yh - Xh @ b_ols) ** 2), rcond=None)[0]
    b_fgls = sm.WLS(yh, Xh, weights=np.exp(-Xh @ g)).fit().params
    # slope of the log-variance regression is consistent for alpha1; the intercept is off by E log chi2_1 = -1.27
    check(stats.chi2(1).expect(np.log), -1.27, 2, "E log chi2_1")
    # Gibbs for beta + random-walk MH for alpha (slide 7: alpha needs MH), priors as slide 8
    V0inv, Vainv = np.eye(2) / 100, np.eye(2) / 100

    def loglik_alpha(a, b):
        e = yh - Xh @ b
        lh = Xh @ a
        return -0.5 * np.sum(lh) - 0.5 * np.sum(e ** 2 * np.exp(-lh))

    a, b = g.copy(), b_ols.copy()
    keep, acc = [], 0
    for it in range(12000):
        b, _, _ = draw_beta(rng, Xh, yh, np.exp(-Xh @ a), 1.0, np.zeros(2), V0inv)
        prop = a + 0.15 * rng.normal(size=2)
        lr = loglik_alpha(prop, b) - loglik_alpha(a, b) - 0.5 * (prop @ Vainv @ prop - a @ Vainv @ a)
        if np.log(rng.uniform()) < lr:
            a, acc = prop, acc + 1
        if it >= 2000:
            keep.append(np.r_[b, a])
    keep = np.array(keep)
    pm = keep.mean(0)
    assert 0.15 < acc / 12000 < 0.7, acc / 12000
    assert np.all(np.abs(pm[2:] - alpha_true) < 0.4) and np.all(np.abs(pm[:2] - beta_true) < 0.4), pm
    # efficiency ratio used in the figure (exact, fixed normal-quantile design)
    r = mf.gls_efficiency(1.0)
    check(r[1], 4.38, 2, "Var OLS / Var GLS slope at alpha1 = 1")
    print(f"1 GLS: OLS on (Py, PX) = GLS; W Table 8.1 OLS .821 (.104) / WLS .787 (.063) reproduced; "
          f"Case I MH acceptance {acc/12000:.2f}, posterior means beta {pm[0]:.2f}, {pm[1]:.2f}, alpha {pm[2]:.2f}, {pm[3]:.2f}; "
          f"FGLS slope {b_fgls[1]:.2f}; OLS/GLS slope variance at alpha1 = 1: {r[1]:.2f}")
    return dict(acc=acc / 12000, pm=pm, b_ols=b_ols, g=g, b_fgls=b_fgls)
```

## 2 · Student-t errors → [[L07-02-student-t-errors]]

The scale-mixture identity by quadrature, the ν prior probabilities, and the Gibbs + MH sampler of slides 16–19 with one planted outlier.


```python
# ============================================================================ 2 · Student-t errors (L07-02)
def gibbs_t(rng, X, y, b0, V0inv, nu0_s, s0sq, nu_prior_mean, M0, M, nu_init=10.0, step=0.25):
    """Gibbs + MH sampler of GLM3 slides 16-19 for y = X beta + e, e_i | w_i ~ N(0, sigma2 w_i), w_i ~ IG(nu/2, nu/2).

    Full conditionals: w_i ~ IG((nu+1)/2, (nu + e_i^2/sigma2)/2); beta ~ N with weights 1/w_i;
    sigma2 ~ IG((nu0+n)/2, (nu0 s0^2 + sum e_i^2/w_i)/2); nu by random-walk MH on
    log p(nu|w) = n[(nu/2)log(nu/2) - lgamma(nu/2)] - [1/nu^0 + 0.5 sum(log w_i + 1/w_i)] nu, nu > 0 (slide 18).
    Returns draws (M x (k+2)): beta, sigma2, nu; plus the MH acceptance rate and the mean weights 1/w_i.
    """
    n, k = X.shape
    beta = np.linalg.lstsq(X, y, rcond=None)[0]
    sigma2 = np.sum((y - X @ beta) ** 2) / (n - k)
    nu, w = nu_init, np.ones(n)
    out, acc, wbar = np.zeros((M, k + 2)), 0, np.zeros(n)

    def lp_nu(v, w):
        if v <= 0:
            return -np.inf
        return n * (0.5 * v * np.log(0.5 * v) - gammaln(0.5 * v)) - (1 / nu_prior_mean + 0.5 * np.sum(np.log(w) + 1 / w)) * v

    for it in range(M0 + M):
        e = y - X @ beta
        w = 1 / rng.gamma((nu + 1) / 2, 2 / (nu + e ** 2 / sigma2))       # 1/w ~ G((nu+1)/2, rate (nu+e^2/s2)/2)
        beta, _, _ = draw_beta(rng, X, y, 1 / w, sigma2, b0, V0inv)
        e = y - X @ beta
        sigma2 = 1 / rng.gamma((nu0_s + n) / 2, 2 / (nu0_s * s0sq + np.sum(e ** 2 / w)))
        prop = nu + step * rng.normal()
        if np.log(rng.uniform()) < lp_nu(prop, w) - lp_nu(nu, w):
            nu, acc = prop, acc + 1
        if it >= M0:
            out[it - M0] = np.r_[beta, sigma2, nu]
            wbar += 1 / w / M
    return out, acc / (M0 + M), wbar


def section2():
    # the scale-mixture identity, numerically (G p. 52)
    for nu in (1, 3, 5, 10, 30):
        for e in (0.0, 0.8, 2.5, 6.0):
            assert abs(mf.mixture_pdf(e, nu) - stats.t.pdf(e, nu)) < 1e-8, (nu, e)
    # prior of nu ~ Exp(mean 25) (slide 17): mass on nu <= 10 and nu >= 40
    p10, p40 = 1 - np.exp(-10 / 25), np.exp(-40 / 25)
    check(p10, 0.3297, 4, "P(nu <= 10)")
    check(p40, 0.2019, 4, "P(nu >= 40)")
    # Var of t_nu is nu/(nu-2) sigma^2: the scale sigma^2 is not the variance (pitfall)
    check(stats.t(5).var(), 5 / 3, 6, "Var t_5")
    # slide-19 simulation: n = 100, nu = 10, sigma^2 = 1, beta = (0.5, 1, 2); priors beta0 = 0, V0 = 10 I3, nu0 = 5, s0^2 = 1, nu^0 = 25
    rng = np.random.default_rng(19)
    n = 100
    X = np.column_stack([np.ones(n), rng.normal(size=(n, 2))])
    beta_true = np.array([0.5, 1.0, 2.0])
    y = X @ beta_true + stats.t(10).rvs(size=n, random_state=rng)
    y[7] += 15.0                                                     # one gross outlier
    draws, acc, wbar = gibbs_t(rng, X, y, np.zeros(3), np.eye(3) / 10, 5.0, 1.0, 25.0, M0=3000, M=20000)
    pm = draws.mean(0)
    ols = np.linalg.lstsq(X, y, rcond=None)[0]
    assert np.all(np.abs(pm[:3] - beta_true) < 0.3), pm
    assert wbar[7] < 0.2 * np.median(wbar), (wbar[7], np.median(wbar))   # the outlier is downweighted
    keep = np.arange(n) != 7
    ols_clean = np.linalg.lstsq(X[keep], y[keep], rcond=None)[0]
    shift_ols, shift_t = abs(ols[0] - ols_clean[0]), abs(pm[0] - ols_clean[0])
    assert shift_t < 0.5 * shift_ols, (shift_t, shift_ols)               # the outlier moves OLS, barely the t fit
    print(f"2 t errors: mixture identity holds; P(nu<=10) = {p10:.4f}, P(nu>=40) = {p40:.4f}; "
          f"Gibbs-MH (one outlier +15): beta {pm[0]:.2f}, {pm[1]:.2f}, {pm[2]:.2f} vs OLS {ols[0]:.2f}, {ols[1]:.2f}, {ols[2]:.2f}; "
          f"posterior mean nu {pm[4]:.1f}; MH acceptance {acc:.2f}; outlier weight {wbar[7]:.3f} vs median {np.median(wbar):.3f}")
    return dict(pm=pm, ols=ols, acc=acc, w_out=wbar[7], w_med=np.median(wbar))
```

## 3 · AR(1) errors → [[L07-03-ar1-errors]]

$\Omega_\rho^{-1}$ tridiagonal and $P'P=\Omega_\rho^{-1}$; iterated Prais–Winsten reproducing W Table 12.1; Cochrane–Orcutt; the truncated-normal draw against `truncnorm`; the slide-27 sampler with the small-sin ρ step.


```python
# ============================================================================ 3 · AR(1) errors (L07-03)
def omega_rho(n, rho):
    """Omega_rho of GLM3 slide 23: entries rho^|i-j| / (1 - rho^2)."""
    i = np.arange(n)
    return rho ** np.abs(i[:, None] - i[None, :]) / (1 - rho ** 2)


def omega_rho_inv(n, rho):
    """Omega_rho^-1 in closed form: tridiagonal, diagonal (1, 1+rho^2, ..., 1+rho^2, 1), off-diagonal -rho."""
    return np.diag(np.r_[1, np.full(n - 2, 1 + rho ** 2), 1]) - rho * (np.eye(n, k=1) + np.eye(n, k=-1))


def prais_winsten(y, X, rho):
    """Quasi-differenced data of W (12.31)-(12.32): first row scaled by sqrt(1 - rho^2), then y_t - rho y_{t-1}."""
    ys = np.r_[np.sqrt(1 - rho ** 2) * y[0], y[1:] - rho * y[:-1]]
    Xs = np.vstack([np.sqrt(1 - rho ** 2) * X[0], X[1:] - rho * X[:-1]])
    return ys, Xs


def section3():
    n, rho = 6, 0.7
    Om = omega_rho(n, rho)
    Oi = np.linalg.inv(Om)
    tri = omega_rho_inv(n, rho)
    assert np.allclose(Oi, tri)                                       # tridiagonal inverse
    Pm = np.vstack([np.r_[np.sqrt(1 - rho ** 2), np.zeros(n - 1)],
                    np.eye(n)[1:] - rho * np.eye(n, k=-1)[1:]])
    assert np.allclose(Pm.T @ Pm, Oi) and np.allclose(Pm @ Om @ Pm.T, np.eye(n))   # PW is the P of slide 4

    # Wooldridge Example 12.4 (Table 12.1, p. 384): iterated Prais-Winsten on BARIUM
    b = wooldridge.data("barium")
    y = b.lchnimp.values
    X = sm.add_constant(b[["lchempi", "lgas", "lrtwex", "befile6", "affile6", "afdec6"]]).values
    ols = sm.OLS(y, X).fit()
    check(ols.params[1], 3.12, 2, "OLS log(chempi)")
    check(ols.bse[1], 0.48, 2, "OLS SE log(chempi)")
    check(ols.params[0], -17.80, 2, "OLS intercept")
    r, n_pw = 0.0, 0
    while True:
        fit = sm.OLS(*prais_winsten(y, X, r)).fit()
        u = y - X @ fit.params
        r_new = np.sum(u[1:] * u[:-1]) / np.sum(u[:-1] ** 2)         # W (12.14): regress u_t on u_{t-1}
        n_pw += 1
        if abs(r_new - r) < 1e-10:
            break
        r = r_new
    check(r, 0.293, 3, "PW rho-hat")
    check(fit.params[1], 2.94, 2, "PW log(chempi)")
    check(fit.bse[1], 0.63, 2, "PW SE log(chempi)")
    check(fit.params[0], -37.08, 2, "PW intercept")
    check(fit.params[6], -0.577, 3, "PW afdec6")
    check(fit.params[6] / fit.bse[6], -1.69, 2, "PW t afdec6")
    # Cochrane-Orcutt drops the first row: same rho iteration, different numbers in a sample of 131
    r_co = 0.0
    for _ in range(200):
        ys, Xs = prais_winsten(y, X, r_co)
        f_co = sm.OLS(ys[1:], Xs[1:]).fit()
        u = y - X @ f_co.params
        r_co = np.sum(u[1:] * u[:-1]) / np.sum(u[:-1] ** 2)

    # truncated-normal inverse-CDF draw (slide 26) equals truncnorm's quantile function, exactly
    uu = np.linspace(0.001, 0.999, 999)
    mu, sd, lo, hi = 0.9, 0.05, -1.0, 1.0
    yq = mu + sd * stats.norm.ppf(uu * stats.norm.cdf((hi - mu) / sd) + (1 - uu) * stats.norm.cdf((lo - mu) / sd))
    assert np.allclose(yq, stats.truncnorm((lo - mu) / sd, (hi - mu) / sd, loc=mu, scale=sd).ppf(uu), atol=1e-10)
    rng = np.random.default_rng(26)
    tail = rtruncnorm(rng, np.zeros(20000), 1.0, 8.0, np.inf)            # deep upper tail: no Phi^-1(1) blow-up
    assert np.all(tail >= 8.0) and abs(tail.mean() - stats.truncnorm(8, np.inf).mean()) < 0.01

    # slide-27 simulation: n = 200, rho = 0.9, sigma^2 = 1, beta = (2, 4); priors beta0 = 0, V0 = 100 I2,
    # nu0 = 5, s0^2 = 1, rho0 = 0.9, V_rho = 100; rho by the "small sin" truncated-normal conditional (slide 25)
    n = 200
    Xs = rng.normal(size=(n, 2))
    e = np.zeros(n)
    e[0] = rng.normal() / np.sqrt(1 - 0.81)
    for t in range(1, n):
        e[t] = 0.9 * e[t - 1] + rng.normal()
    ys = Xs @ np.array([2.0, 4.0]) + e
    beta, s2, rh = np.linalg.lstsq(Xs, ys, rcond=None)[0], 1.0, 0.5
    keep = []
    for it in range(6000):
        Oi = omega_rho_inv(n, rh)                                   # closed form, no 200 x 200 inversion
        beta, _, _ = draw_beta(rng, Xs, ys, Oi, s2, np.zeros(2), np.eye(2) / 100)
        res = ys - Xs @ beta
        s2 = 1 / rng.gamma((5 + n) / 2, 2 / (5 * 1.0 + res @ Oi @ res))
        et, el = res[1:], res[:-1]
        Vr = 1 / (1 / 100 + el @ el / s2)
        r1 = Vr * (0.9 / 100 + el @ et / s2)
        rh = float(rtruncnorm(rng, r1, np.sqrt(Vr), -1.0, 1.0))
        if it >= 1000:
            keep.append([beta[0], beta[1], s2, rh])
    pm = np.array(keep).mean(0)
    assert abs(pm[0] - 2) < 0.2 and abs(pm[1] - 4) < 0.2 and abs(pm[3] - 0.9) < 0.07, pm
    print(f"3 AR(1): Omega_rho^-1 tridiagonal, PW matrix P'P = Omega^-1; W Table 12.1 reproduced (PW 2.94 (0.63), "
          f"rho-hat {r:.3f}, t_afdec6 {fit.params[6]/fit.bse[6]:.2f}; {n_pw} iterations); Cochrane-Orcutt rho {r_co:.3f}, "
          f"log(chempi) {f_co.params[1]:.2f}; Gibbs (slide 27 design) beta {pm[0]:.2f}, {pm[1]:.2f}, sigma2 {pm[2]:.2f}, rho {pm[3]:.3f}")
    return dict(rho=r, pw=fit, co=f_co, r_co=r_co, pm=pm)
```

## 4 · Hierarchical models → [[L07-04-hierarchical-linear-models]]

Eight schools exactly; the site's pooled and individual regressions to every printed digit; the site's Gibbs sampler (ported in `figures/make_figures.py`, `gibbs_hlm`) and the weights $w$ and θ.


```python
# ============================================================================ 4 · hierarchical models (L07-04)
def section4():
    # eight schools: exact p(tau | y) under tau ~ U(0, 100), mu ~ N(0, 1e6) (HLM slide 23)
    grid = np.linspace(0, 100, 4001)
    p = mf.schools_tau_posterior(grid)
    med = mf.quantile_on_grid(grid, p, 0.5)
    mean_tau = np.trapezoid(grid * p, grid)
    q025, q975 = mf.quantile_on_grid(grid, p, 0.025), mf.quantile_on_grid(grid, p, 0.975)
    w = 1 / mf.S8 ** 2
    pooled, pooled_sd = np.sum(w * mf.Y8) / w.sum(), 1 / np.sqrt(w.sum())
    check(pooled, 7.87, 2, "complete-pooling mean")
    check(pooled_sd, 4.17, 2, "complete-pooling sd")
    check(med, 5.23, 2, "posterior median tau")
    # fully Bayes E(theta_i | y): integrate E(theta_i | y, tau) against p(tau | y)
    cond = np.array([mf.schools_conditional(t)["mean"] for t in grid])
    eb = np.trapezoid(cond * p[:, None], grid, axis=0)
    cA = mf.schools_conditional(med)
    assert np.all(np.diff(np.sort(eb)) >= 0) and eb.max() < mf.Y8.max() and eb.min() > mf.Y8.min()
    # school A at the posterior median of tau, by hand: B_A = 14.9^2/(14.9^2 + tau^2)
    BA = 14.9 ** 2 / (14.9 ** 2 + med ** 2)
    check(cA["B"][0], BA, 10, "B_A")
    check(cA["mean"][0], (1 - BA) * 28.39 + BA * cA["mu"], 10, "E(theta_A | y, tau)")

    # pregnant women (hierarchicalmodel.html): pooled, individual and hierarchical regressions
    ys, xs = mf.pregnancy()
    x1, y1 = np.concatenate(xs), np.concatenate(ys)
    fit = sm.OLS(y1, sm.add_constant(x1)).fit()
    check(len(y1), 427, 0, "n")
    check(fit.params[0], -4.52639, 5, "pooled intercept")
    check(fit.params[1], 0.47633, 5, "pooled slope")
    check(fit.bse[0], 0.48680, 5, "pooled SE intercept")
    check(fit.bse[1], 0.01897, 5, "pooled SE slope")
    check(np.sqrt(fit.scale), 3.612, 3, "residual standard error")
    check(fit.rsquared, 0.5974, 4, "R2")
    ind = mf.ols_by_woman(ys, xs)
    sig = np.array([np.sqrt(np.sum((y - c[0] - c[1] * x) ** 2) / (len(y) - 2)) for y, x, c in zip(ys, xs, ind)])
    for col, (mn, q1, md, mean, q3, mx) in zip(ind.T, ((-14.432, -6.744, -4.260, -4.412, -2.330, 5.157),
                                                        (0.126, 0.395, 0.450, 0.470, 0.525, 0.801))):
        got = (col.min(), np.quantile(col, 0.25), np.median(col), col.mean(), np.quantile(col, 0.75), col.max())
        for g_, pr in zip(got, (mn, q1, md, mean, q3, mx)):
            check(g_, pr, 3, "individual-regression summary")
    check(sig.mean(), 1.0133, 4, "mean individual sigma")
    check(sig.min(), 0.3484, 4, "min individual sigma")
    d1, d2 = mf.gibbs_hlm(ys, xs)
    post = d2.mean(0)
    pm1 = d1.mean(0)
    # partial pooling: posterior means less dispersed than individual OLS, centred near the population means
    assert np.all(post.std(0) < ind.std(0))
    assert abs(pm1[0] - ind[:, 0].mean()) < 1.0 and abs(pm1[1] - ind[:, 1].mean()) < 0.05
    # the conditional shrinkage weight of a woman's intercept (alpha_i given everything else), HLM slide 12 form:
    # precision 1/s_a^2 + T/s_y^2  =>  weight on her own data  w = T s_a^2 / (T s_a^2 + s_y^2)
    sy, sa = pm1[2], pm1[3]
    w6 = 6 * sa ** 2 / (6 * sa ** 2 + sy ** 2)
    # random-effects quasi-demeaning, W (14.10) p. 442: theta = 1 - sqrt(s_u^2 / (s_u^2 + T s_a^2))
    theta_re = 1 - np.sqrt(sy ** 2 / (sy ** 2 + 6 * sa ** 2))
    assert 0 < theta_re < w6 < 1
    # predictive for woman 1 at her 7th (unobserved) visit, x = 40.143 (site section 4.4.3)
    pred1 = d2[:, 0, 0] + d2[:, 0, 1] * 40.143
    q1 = np.quantile(pred1, [0.025, 0.5, 0.975])
    print(f"4 hierarchical: eight schools pooled {pooled:.2f} (sd {pooled_sd:.2f}), tau median {med:.2f}, mean {mean_tau:.2f}, "
          f"95% [{q025:.2f}, {q975:.2f}]; E(theta_A|y) = {eb[0]:.2f}; pregnancy pooled -4.52639 + 0.47633 x reproduced; "
          f"Gibbs means alpha {pm1[0]:.3f}, beta {pm1[1]:.4f}, s_y {pm1[2]:.3f}, s_a {pm1[3]:.3f}, s_b {pm1[4]:.4f}; "
          f"weight on own data (T=6) {w6:.3f}, RE theta {theta_re:.3f}; woman 1 at x=40.143: median {q1[1]:.2f} [{q1[0]:.2f}, {q1[2]:.2f}]")
    return dict(med=med, mean_tau=mean_tau, q=(q025, q975), eb=eb, pooled=pooled, pooled_sd=pooled_sd, cA=cA,
                pm1=pm1, post=post, ind=ind, w6=w6, theta_re=theta_re, q1=q1)
```

## 5 · Tobit → [[L07-05-tobit]]

Slide 9's probabilities; the Stein attenuation by Monte Carlo; (17.24)–(17.30) against simulation and numerical derivatives; W Table 17.3 by MLE; Chib's data augmentation.


```python
# ============================================================================ 5 · Tobit (L07-05)
def tobit_mle(X, h):
    def nll(th):
        b, s = th[:-1], np.exp(th[-1])
        xb = X @ b
        return -np.sum(np.where(h > 0, stats.norm.logpdf((h - xb) / s) - np.log(s), stats.norm.logcdf(-xb / s)))
    ols = sm.OLS(h, X).fit()
    th = np.r_[ols.params, np.log(np.sqrt(ols.scale))]
    for meth in ("BFGS", "Nelder-Mead", "BFGS"):
        th = optimize.minimize(nll, th, method=meth, options=dict(maxiter=200000, maxfev=200000, xatol=1e-10,
                                                                     fatol=1e-10) if meth == "Nelder-Mead" else dict(gtol=1e-9)).x
    return th[:-1], np.exp(th[-1]), -nll(th)


def gibbs_tobit(rng, X, h, M0=1000, M=5000):
    """Chib (1992) data augmentation, LDV slides 7-8 / G Algorithm 8.2, flat prior (V0^-1 = 0, nu0 = 0).

    y*_i = y_i if y_i > 0, else y*_i ~ N(x_i b, s2) truncated to (-inf, 0]; b | y* ~ N((X'X)^-1 X'y*, s2 (X'X)^-1);
    s2 | b, y* ~ IG(n/2, (y* - Xb)'(y* - Xb)/2).
    """
    n = len(h)
    cen = h <= 0
    XtXi = np.linalg.inv(X.T @ X)
    Lc = np.linalg.cholesky(XtXi)
    b = XtXi @ X.T @ h
    s2 = np.var(h)
    ystar = h.astype(float).copy()
    out = np.zeros((M, X.shape[1] + 1))
    for it in range(M0 + M):
        ystar[cen] = rtruncnorm(rng, X[cen] @ b, np.sqrt(s2), -np.inf, 0.0)
        bhat = XtXi @ X.T @ ystar
        b = bhat + np.sqrt(s2) * Lc @ rng.normal(size=len(bhat))
        r = ystar - X @ b
        s2 = 1 / rng.gamma(n / 2, 2 / (r @ r))
        if it >= M0:
            out[it - M0] = np.r_[b, np.sqrt(s2)]
    return out


def section5():
    # slide 9: y* ~ N(a beta, beta^2 + sigma^2) with beta = 2, sigma^2 = 0.25
    check(np.sqrt(4.25), 2.062, 3, "sd of y*")
    for a, pr in ((0.0, 0.5), (0.7, 0.25), (1.3, 0.1)):
        check(mf.p_zero_slide(a), pr, 2, f"Prob. trunc. at a = {a}")
    # OLS on censored data with normal x: slope = beta P(y > 0) (Stein's lemma), Monte Carlo check
    rng = np.random.default_rng(5)
    xs = rng.normal(0.7, 1, 1_000_000)
    yc = np.maximum(0, 2 * xs + 0.5 * rng.normal(size=xs.size))
    slope = np.polyfit(xs, yc, 1)[0]
    assert abs(slope - 2 * (1 - mf.p_zero_slide(0.7))) < 0.005, slope
    # pointwise Tobit moments (W 17.24, 17.25, 17.30) against Monte Carlo at x0 = 0.3
    m = mf.tobit_moments(0.3, 2.0, 0.5)
    ysim = np.maximum(0, 0.6 + 0.5 * rng.normal(size=2_000_000))
    assert abs(ysim.mean() - m["e_all"]) < 2e-3 and abs(ysim[ysim > 0].mean() - m["e_pos"]) < 2e-3
    eps = 1e-5
    num = (mf.tobit_moments(0.3 + eps, 2.0, 0.5)["e_all"] - mf.tobit_moments(0.3 - eps, 2.0, 0.5)["e_all"]) / (2 * eps)
    assert abs(num - m["dE_all"]) < 1e-6                                # (17.30) is the derivative of (17.25)
    num2 = (mf.tobit_moments(0.3 + eps, 2.0, 0.5)["e_pos"] - mf.tobit_moments(0.3 - eps, 2.0, 0.5)["e_pos"]) / (2 * eps)
    assert abs(num2 - m["dE_pos"]) < 1e-6                               # (17.26)

    # Wooldridge Example 17.2 (Table 17.3, p. 541): hours of 753 married women, 325 zeros
    d = wooldridge.data("mroz")
    cols = ["nwifeinc", "educ", "exper", "expersq", "age", "kidslt6", "kidsge6"]
    X = sm.add_constant(d[cols]).values
    h = d.hours.values.astype(float)
    check(int((h == 0).sum()), 325, 0, "zeros")
    ols = sm.OLS(h, X).fit()
    for j, pr in zip(range(8), (1330.48, -3.45, 28.76, 65.67, -0.700, -30.51, -442.09, -32.78)):
        check(ols.params[j], pr, 2 if abs(pr) > 1 else 3, f"OLS col {j}")
    check(np.sqrt(ols.scale), 750.18, 2, "OLS sigma")
    b, s, ll = tobit_mle(X, h)
    for j, pr in zip(range(8), (965.31, -8.81, 80.65, 131.56, -1.86, -54.41, -894.02, -16.22)):
        check(b[j], pr, 2, f"Tobit col {j}")
    check(s, 1122.02, 2, "Tobit sigma")
    check(ll, -3819.09, 2, "Tobit log-likelihood")
    ape = stats.norm.cdf(X @ b / s).mean()
    xm = X.mean(0)
    xm[4] = xm[3] ** 2                                                  # (average exper)^2, as W says
    pea = stats.norm.cdf(xm @ b / s)
    check(ape, 0.589, 3, "APE scale")
    check(pea, 0.645, 3, "PEA scale")
    check(ape * b[2], 47.50, 1, "APE educ")
    # Chib data augmentation reproduces the MLE (flat prior: posterior means ~ MLE)
    dr = gibbs_tobit(np.random.default_rng(17), X, h)
    pm, psd = dr.mean(0), dr.std(0)
    se = np.array([21.58, 111.88])
    assert abs(pm[2] - b[2]) < 0.25 * se[0] and abs(pm[6] - b[6]) < 0.25 * se[1], (pm[2], pm[6])
    assert abs(psd[2] / se[0] - 1) < 0.15 and abs(psd[6] / se[1] - 1) < 0.15
    print(f"5 Tobit: slide 9 P(y=0) 0.500/0.249/0.104; OLS-on-censored slope {slope:.4f} = beta P(y>0) "
          f"{2*(1-mf.p_zero_slide(0.7)):.4f}; W Table 17.3 Tobit reproduced (educ {b[2]:.2f}, kidslt6 {b[6]:.2f}, sigma {s:.2f}, "
          f"loglik {ll:.2f}); APE {ape:.3f}, PEA {pea:.3f}; Gibbs posterior means educ {pm[2]:.2f} (sd {psd[2]:.2f}), "
          f"kidslt6 {pm[6]:.2f} (sd {psd[6]:.2f}), sigma {pm[-1]:.1f}")
    return dict(b=b, s=s, ll=ll, ape=ape, pea=pea, pm=pm, psd=psd, slope=slope)
```

## 6 · Probit, ordered and multinomial probit → [[L07-06-probit-ordered-multinomial]]

W Table 17.1 (probit and logit), the scale factors, Albert–Chib, Greenberg's prior arithmetic, the ordered-probit sampler with uniform cut-points, and a multinomial probit sampler with Ω known.


```python
# ============================================================================ 6 · probit, ordered, multinomial (L07-06)
def gibbs_probit(rng, X, y, M0=1000, M=5000):
    """Albert & Chib (1993), G Algorithm 8.3 with a flat prior: z_i ~ TN(x_i b, 1) on (0, inf) if y_i = 1 else (-inf, 0];
    b | z ~ N((X'X)^-1 X'z, (X'X)^-1). B1 does not change across iterations because sigma^2 = 1."""
    XtXi = np.linalg.inv(X.T @ X)
    Lc = np.linalg.cholesky(XtXi)
    b = np.zeros(X.shape[1])
    lo = np.where(y == 1, 0.0, -np.inf)
    hi = np.where(y == 1, np.inf, 0.0)
    out = np.zeros((M, X.shape[1]))
    for it in range(M0 + M):
        z = rtruncnorm(rng, X @ b, 1.0, lo, hi)
        b = XtXi @ X.T @ z + Lc @ rng.normal(size=len(b))
        if it >= M0:
            out[it - M0] = b
    return out


def gibbs_ordered(rng, X, y, J, M0=2000, M=8000):
    """Ordered probit (LDV slide 12): gamma_1 = 0 fixed, flat priors.
    z_i ~ TN(x_i b, 1) on (gamma_{y_i - 1}, gamma_{y_i}]; b | z as in the probit;
    gamma_j ~ U(max{max z_i: y_i = j, gamma_{j-1}}, min{min z_i: y_i = j+1, gamma_{j+1}}), j = 2..J-1."""
    XtXi = np.linalg.inv(X.T @ X)
    Lc = np.linalg.cholesky(XtXi)
    b = np.zeros(X.shape[1])
    gam = np.r_[-np.inf, 0.0, np.arange(1, J - 1, dtype=float), np.inf]   # gamma_0 .. gamma_J
    out = np.zeros((M, X.shape[1] + J - 2))
    for it in range(M0 + M):
        z = rtruncnorm(rng, X @ b, 1.0, gam[y - 1], gam[y])
        b = XtXi @ X.T @ z + Lc @ rng.normal(size=len(b))
        for j in range(2, J):
            lo = max(z[y == j].max(), gam[j - 1])
            hi = min(z[y == j + 1].min(), gam[j + 1])
            gam[j] = rng.uniform(lo, hi)
        if it >= M0:
            out[it - M0] = np.r_[b, gam[2:J]]
    return out


def gibbs_mnp(rng, Xlist, y, Sigma, M0=1000, M=4000):
    """Multinomial probit as a SUR in utility differences (LDV slides 13-15), Sigma known (identified: Sigma_11 = 1).

    w_i = X_i beta + e_i, e_i ~ N(0, Sigma), J differences; y_i = 0 if max(w_i) < 0, else y_i = argmax w_i + 1.
    w_ij | w_i,-j is univariate normal (A.9-type conditional) truncated by the choice; beta | w is the SUR draw
    V1^-1 = sum X_i' Sigma^-1 X_i, V1^-1 b1 = sum X_i' Sigma^-1 w_i (flat prior).
    ponytail: Sigma fixed at its true value; the McCulloch-Rossi inverse-Wishart step is the upgrade path.
    """
    n, J, k = Xlist.shape
    Si = np.linalg.inv(Sigma)
    P = np.einsum("ijk,jl,ilm->km", Xlist, Si, Xlist)
    V1 = np.linalg.inv(P)
    Lc = np.linalg.cholesky(V1)
    b = np.zeros(k)
    w = np.where(np.arange(J)[None, :] == (y - 1)[:, None], 0.5, -0.5)
    out = np.zeros((M, k))
    for it in range(M0 + M):
        mu = np.einsum("ijk,k->ij", Xlist, b)
        for j in range(J):
            o = [q for q in range(J) if q != j]
            # conditional of component j given the others: mean mu_j + S_jo S_oo^-1 (w_o - mu_o), var S_jj - S_jo S_oo^-1 S_oj
            Soo_i = np.linalg.inv(Sigma[np.ix_(o, o)])
            cm = mu[:, j] + (w[:, o] - mu[:, o]) @ Soo_i @ Sigma[o, j]
            cs = np.sqrt(Sigma[j, j] - Sigma[j, o] @ Soo_i @ Sigma[o, j])
            mo = w[:, o].max(1)
            lo = np.where(y == j + 1, np.maximum(0, mo), -np.inf)
            # chosen j: above 0 and all others; base chosen: below 0; another k chosen: below w_ik
            hi = np.where(y == 0, 0.0, np.where(y == j + 1, np.inf, w[np.arange(n), np.clip(y - 1, 0, J - 1)]))
            w[:, j] = rtruncnorm(rng, cm, cs, lo, hi)
        rhs = np.einsum("ijk,jl,il->k", Xlist, Si, w)
        b = V1 @ rhs + Lc @ rng.normal(size=k)
        if it >= M0:
            out[it - M0] = b
    return out


def section6():
    # Wooldridge Example 17.1 (Table 17.1, p. 533): labor force participation, MROZ
    d = wooldridge.data("mroz")
    cols = ["nwifeinc", "educ", "exper", "expersq", "age", "kidslt6", "kidsge6"]
    X = sm.add_constant(d[cols]).values
    y = d.inlf.values.astype(int)
    pr = sm.Probit(y, X).fit(disp=0)
    lg = sm.Logit(y, X).fit(disp=0)
    for j, pv in zip(range(8), (0.270, -0.012, 0.131, 0.123, -0.0019, -0.053, -0.868, 0.036)):
        check(pr.params[j], pv, 4 if abs(pv) < 0.01 else 3, f"probit col {j}")
    for j, pv in zip(range(8), (0.425, -0.021, 0.221, 0.206, -0.0032, -0.088, -1.443, 0.060)):
        check(lg.params[j], pv, 4 if abs(pv) < 0.01 else 3, f"logit col {j}")
    check(pr.llf, -401.30, 2, "probit loglik")
    check(lg.llf, -401.77, 2, "logit loglik")
    check(pr.prsquared, 0.221, 3, "probit pseudo R2")
    check(100 * np.mean((pr.predict(X) > 0.5) == y), 73.4, 1, "percent correctly predicted")
    xm = X.mean(0)
    s_pr, s_lg = stats.norm.pdf(xm @ pr.params), (lambda e: e / (1 + e) ** 2)(np.exp(xm @ lg.params))
    check(s_pr, 0.391, 3, "probit PEA scale")
    check(s_lg, 0.243, 3, "logit PEA scale")
    check(s_pr / s_lg, 1.61, 2, "ratio of scale factors")
    check(stats.norm.pdf(X @ pr.params).mean(), 0.301, 3, "probit APE scale")
    # Albert-Chib Gibbs reproduces the probit MLE
    dr = gibbs_probit(np.random.default_rng(23), X, y)
    pm, psd = dr.mean(0), dr.std(0)
    assert np.all(np.abs(pm - pr.params) < 0.3 * pr.bse), (pm, pr.params)
    assert np.all(np.abs(psd / pr.bse - 1) < 0.2)
    # Greenberg's prior elicitation (pp. 125-126 probit, p. 128 logit)
    check(stats.norm.ppf(0.10), -1.2816, 4, "beta01 probit")
    check(((stats.norm.ppf(0.3) - stats.norm.ppf(0.1)) / 1.96) ** 2, 0.1492, 4, "B0,11 probit")
    check((stats.norm.ppf(0.8) + 1.2816) / 2, 1.0616, 4, "beta02 probit")
    check((stats.norm.ppf(0.6) + 1.2816) / 2, 0.767, 3, "lower beta2 probit (G prints 0.7674, truncated)")
    check(((1.0616 - 0.7674) / 1.96) ** 2, 0.0225, 4, "B0,22 probit")
    check(stats.norm.ppf(0.4) + 1.2816, 1.0283, 4, "beta03 probit")
    check(np.log(1 / 9), -2.1972, 4, "beta01 logit")
    check((np.log(3 / 7) - np.log(1 / 9)) / 1.96, 0.6887, 4, "prior sd beta1 logit")
    check((np.log(4) + 2.1972) / 2, 1.7917, 4, "beta02 logit")
    check(stats.norm.pdf(0), 0.3989, 4, "phi(0)")

    # ordered probit (slides 11-12) on a simulated sample: x'b = 0.5 + 1.0 x, gamma = (0, 1, 2), J = 4
    rng = np.random.default_rng(14)
    n = 500
    Xo = np.column_stack([np.ones(n), rng.normal(size=n)])
    zs = Xo @ np.array([0.5, 1.0]) + rng.normal(size=n)
    yo = 1 + np.searchsorted(np.array([0.0, 1.0, 2.0]), zs)
    dro = gibbs_ordered(rng, Xo, yo, 4)
    pmo = dro.mean(0)
    assert abs(pmo[1] - 1.0) < 0.2 and abs(pmo[2] - 1.0) < 0.25 and abs(pmo[3] - 2.0) < 0.3, pmo
    lag1 = np.corrcoef(dro[1:, 2], dro[:-1, 2])[0, 1]                  # cut-point chain: slow mixing (Cowles 1996)

    # multinomial probit: 3 alternatives (0 = base), 2 utility differences, alternative-specific (intercept, x)
    n = 800
    x = rng.normal(size=n)
    Xl = np.zeros((n, 2, 4))
    Xl[:, 0, 0], Xl[:, 0, 1], Xl[:, 1, 2], Xl[:, 1, 3] = 1, x, 1, x
    Sig = np.array([[1.0, 0.5], [0.5, 1.5]])
    btrue = np.array([0.3, 1.0, -0.2, -0.8])
    wtrue = np.einsum("ijk,k->ij", Xl, btrue) + rng.multivariate_normal(np.zeros(2), Sig, size=n)
    ym = np.where(wtrue.max(1) < 0, 0, wtrue.argmax(1) + 1)
    drm = gibbs_mnp(rng, Xl, ym, Sig)
    pmm = drm.mean(0)
    assert np.all(np.abs(pmm - btrue) < 0.25), pmm
    print(f"6 probit: W Table 17.1 probit/logit reproduced (educ .131/.221, loglik -401.30/-401.77); scale factors "
          f"{s_pr:.3f}/{s_lg:.3f} = {s_pr/s_lg:.2f}; Albert-Chib means educ {pm[2]:.3f} (MLE {pr.params[2]:.3f}); "
          f"ordered probit Gibbs b {pmo[0]:.2f}, {pmo[1]:.2f}, gamma2 {pmo[2]:.2f}, gamma3 {pmo[3]:.2f} (lag-1 corr of gamma2 {lag1:.2f}); "
          f"MNP Gibbs {np.round(pmm, 2)} vs true {btrue}")
    return dict(pr=pr, lg=lg, s_pr=s_pr, s_lg=s_lg, pm=pm, pmo=pmo, lag1=lag1, pmm=pmm)
```

## 7 · The counterexamples of the pitfalls note → [[L07-08-pitfalls]]


```python
# ============================================================================ 7 · counterexamples of the pitfalls note (L07-08)
def section7():
    # (a) random-coefficient shrinkage is not "toward zero": with tau = 5.23 school C (y = -2.75) moves UP
    c = mf.schools_conditional(5.23)
    assert c["mean"][2] > mf.Y8[2] and c["mean"][0] < mf.Y8[0]
    # (b) robust SEs fix inference, not efficiency: GLS variance beats OLS's true variance at alpha1 = 1
    assert mf.gls_efficiency(1.0)[1] > 4
    # (c) Tobit coefficient is not the effect on E(y|x): at z = 0 the slope is beta/2
    check(mf.tobit_moments(0.0, 2.0, 0.5)["dE_all"], 1.0, 10, "dE/dx at z = 0")
    # (d) probit sigma is not identified: scaling (beta, sigma) by c leaves P(y = 1) unchanged
    xb = np.linspace(-2, 2, 9)
    assert np.allclose(stats.norm.cdf(xb / 1.0), stats.norm.cdf((3 * xb) / 3.0))
    # (e) t scale vs variance: sigma^2 = 1, nu = 5 gives Var = 5/3
    check(stats.t(5, scale=1).var(), 1.6667, 4, "Var t5")
    # (f) every Gibbs weight equals 1 at |e/sigma| = 1, whatever nu
    assert all(abs(mf.t_weight(1.0, nu) - 1) < 1e-12 for nu in (1, 2, 5, 30))
    # (g) censoring vs truncation: OLS on the positive subsample is also biased (slope flatter than beta)
    rng = np.random.default_rng(7)
    xs = rng.normal(0.7, 1, 400_000)
    ystar = 2 * xs + 0.5 * rng.normal(size=xs.size)
    pos = ystar > 0
    s_trunc = np.polyfit(xs[pos], ystar[pos], 1)[0]
    assert s_trunc < 2.0
    # (h) AR errors with an iid regressor: OLS keeps the right naive SE (ratio 1), GLS still gains
    n0, e0 = mf.ar1_ratios(0.9, 0.0)
    assert abs(n0 - 1) < 1e-12 and e0 > 9
    print(f"7 pitfalls: school C shrinks up to {c['mean'][2]:.2f}; truncated-sample OLS slope {s_trunc:.3f} < 2; "
          f"AR(0.9) errors + iid x: naive OLS var right, GLS gain x{e0:.2f}")
    return dict(s_trunc=s_trunc, cC=c["mean"][2])


if __name__ == "__main__":
    section1()
    section2()
    section3()
    section4()
    section5()
    section6()
    section7()
    print("ALL L07 CHECKS PASSED")
```

## 8 · The run

```python
if __name__ == "__main__":
    section1()
    section2()
    section3()
    section4()
    section5()
    section6()
    section7()
    print("ALL L07 CHECKS PASSED")
```

Output of the last run (verbatim):

```text
1 GLS: OLS on (Py, PX) = GLS; W Table 8.1 OLS .821 (.104) / WLS .787 (.063) reproduced; Case I MH acceptance 0.55, posterior means beta 2.20, 3.97, alpha 0.93, 1.12; FGLS slope 3.97; OLS/GLS slope variance at alpha1 = 1: 4.38
2 t errors: mixture identity holds; P(nu<=10) = 0.3297, P(nu>=40) = 0.2019; Gibbs-MH (one outlier +15): beta 0.43, 0.87, 1.93 vs OLS 0.54, 1.07, 2.03; posterior mean nu 3.8; MH acceptance 0.83; outlier weight 0.018 vs median 1.063
3 AR(1): Omega_rho^-1 tridiagonal, PW matrix P'P = Omega^-1; W Table 12.1 reproduced (PW 2.94 (0.63), rho-hat 0.293, t_afdec6 -1.69; 11 iterations); Cochrane-Orcutt rho 0.293, log(chempi) 2.95; Gibbs (slide 27 design) beta 1.97, 4.06, sigma2 1.03, rho 0.871
4 hierarchical: eight schools pooled 7.87 (sd 4.17), tau median 5.23, mean 6.59, 95% [0.24, 20.87]; E(theta_A|y) = 11.64; pregnancy pooled -4.52639 + 0.47633 x reproduced; Gibbs means alpha -4.363, beta 0.4687, s_y 1.119, s_a 3.210, s_b 0.1253; weight on own data (T=6) 0.980, RE theta 0.859; woman 1 at x=40.143: median 17.68 [15.68, 19.86]
5 Tobit: slide 9 P(y=0) 0.500/0.249/0.104; OLS-on-censored slope 1.5033 = beta P(y>0) 1.5029; W Table 17.3 Tobit reproduced (educ 80.65, kidslt6 -894.02, sigma 1122.02, loglik -3819.09); APE 0.589, PEA 0.645; Gibbs posterior means educ 81.84 (sd 21.76), kidslt6 -902.63 (sd 112.86), sigma 1138.8
6 probit: W Table 17.1 probit/logit reproduced (educ .131/.221, loglik -401.30/-401.77); scale factors 0.391/0.243 = 1.61; Albert-Chib means educ 0.132 (MLE 0.131); ordered probit Gibbs b 0.50, 0.89, gamma2 1.10, gamma3 2.08 (lag-1 corr of gamma2 0.99); MNP Gibbs [ 0.45  1.1  -0.11 -0.71] vs true [ 0.3  1.  -0.2 -0.8]
7 pitfalls: school C shrinks up to 7.02; truncated-sample OLS slope 1.902 < 2; AR(0.9) errors + iid x: naive OLS var right, GLS gain x9.53
ALL L07 CHECKS PASSED
```


## 9 · What is deliberately absent

- **PyMC** (not installed; the class plan lists it as optional): every sampler is hand-written, which is what
  the exam asks you to be able to write down.
- **The multinomial-probit Ω step** (inverse Wishart with a scale normalization, McCulloch–Rossi): Ω is held at
  its true value, marked `ponytail:` in `gibbs_mnp` with the upgrade path.
- **The airline data** (Greene) are not on disk: the airline posteriors of GLM3 slide 14 and HLM slides 20–21
  are read, not reproduced.
- **Convergence diagnostics** beyond what the notes use (one lag-1 autocorrelation for the cut-points): the
  samplers are long enough for the asserted tolerances, which are a fraction of a posterior sd.

## Links

- Unit: [[L07-00-map]] · [[L07-07-formulas]] · [[L07-08-pitfalls]] · figures script `figures/make_figures.py` · companion checks `companions/check_companions.py`.
- Class 2: [[../L02/L02-09-python|L02 Python]] (IRLS logit and Poisson — the frequentist fits behind §6's logit).
