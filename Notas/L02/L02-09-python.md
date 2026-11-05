---
tags: [notes, lecture-02, statistical-learning, python, reference-implementation]
date: 2026-10-19
status: taught
source: "L02_python_checks.py (this folder; the code below is extracted from it verbatim); figures/make_figures.py and companions/check_companions.py reused; numbers from L02-01 … L02-06"
---

# Class 2 · Python — the reference implementation, asserted against the sources

> Every routine the class needs, each followed by the `assert`s that tie it to a printed number.
> numpy, scipy and statsmodels only — **no scikit-learn**. The lecturer's R is the reference, never
> the code. **The file is the source of truth:** `Notas/L02/L02_python_checks.py`; the blocks below
> are copied from it verbatim, section by section.
> Prev: [[L02-08-pitfalls]] · Map: [[L02-00-map]] · Formulas: [[L02-07-formulas]]

**Run:** `python Notas/L02/L02_python_checks.py` — about ten seconds; it prints one line per section and
ends with `ALL L02 CHECKS PASSED` (§8 below shows the run). The first disagreement aborts with an
`AssertionError` naming the quantity and the printed value.

**Reused, not rewritten.**

| Existing code | What it supplies | Used in |
|---|---|---|
| `figures/make_figures.py` (imported as `mf`) | `psi`, `poly_bias_variance` (exact (28) on a QR/Legendre basis), `mcycle_standin`, `design`, `ols_predict`, `loocv_brute`, `loocv_shortcut`, `kfold_cv`, `h_roots`, the 28 visitor counts `Y` | §1, §3, §5, §6, §7 |
| `companions/check_companions.py` | the Flexibility Dial and the Two-Gaussian Classifier recomputed and compared with the pages' JavaScript under `node` at three control vectors, plus a Monte Carlo of bias² and variance | cited, not imported: it checks the **pages**; this file checks the **notes** |

What is new here, and why: the IRLS routine (no existing code fits a GLM by hand), $k$-fold for an
arbitrary fold list with both (15) and (16) (`mf.kfold_cv` implements only the site's layout and
(16)), the confusion-matrix rates, and the asserts against the section notes' tables.

---

## 0 · Set-up: the comparison helper

`check(x, printed, dec)` passes when `x` rounds to the printed value at `dec` decimals, so every
assert says *which* printed number it reproduces and to how many places.

```python
"""Class 2 (L02) reference implementation with self-checks against the sources' printed numbers.

Run: python Notas/L02/L02_python_checks.py   (numpy, scipy, statsmodels; no scikit-learn)
Every section asserts the numbers of one section note and prints a one-line summary; the first
mismatch aborts with an AssertionError naming it. Shown section by section in L02-09-python.md.

Reused, not rewritten: figures/make_figures.py (imported as mf) supplies the tanh model psi, the exact
polynomial bias-variance routine, the mcycle stand-in, the OLS helpers, the two LOOCV routines and the
Gaussian discriminant roots h_roots. Importing it does not draw any figure (build() runs only as __main__).
"""
import pathlib
import sys

import numpy as np
import statsmodels.api as sm
from scipy import integrate, stats
from scipy.special import expit, logit

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent / "figures"))
import make_figures as mf  # noqa: E402


def near(x, printed, dec):
    """True when x rounds to the printed value at `dec` decimals (half a unit in the last place)."""
    return abs(x - printed) <= 0.5 * 10.0 ** -dec + 1e-9


def check(x, printed, dec, what):
    assert near(x, printed, dec), f"{what}: computed {x!r}, source prints {printed}"
```

---

## 1 · Exact bias–variance on the tanh world → [[L02-01-prediction-error-bias-variance]]

The table of note 01 §5 row by row (avg bias², variance, test, training), the optimum $d^*=5$ with
test error 19.81, an independent hat-matrix route for $d=5$, the optimism (33) as an identity, and
the line-on-a-quadratic numbers of §4.1 by quadrature and Monte Carlo.

```python
# ============================================================================ 1 · bias-variance (L02-01)
def section1():
    psi = mf.psi
    check(psi(8.0), 12.339, 3, "psi(8)")
    check(psi(18.0), 101.365, 3, "psi(18)")
    assert abs(psi(13.3) - 57) < 1e-12                       # inflection, (26)
    check(45 / 1.9, 23.68, 2, "slope at the inflection")

    # exact (21) for the degree-d OLS polynomial on 30 equispaced points, sigma = 4 (note 01 section 5 table)
    rows = {d: mf.poly_bias_variance(d) for d in range(16)}
    test = {d: b2 + v + 16 for d, (b2, v, _) in rows.items()}
    dstar = min(test, key=test.get)
    assert dstar == 5, dstar
    table = {1: (74.80, 1.03, 91.83, 93.87), 3: (7.98, 1.97, 25.95, 22.39), 5: (0.94, 2.87, 19.81, 13.79),
             6: (0.70, 3.33, 20.03, 13.01), 7: (0.11, 3.80, 19.91, 11.85), 10: (0.007, 5.37, 21.38, 10.14),
             15: (0.000, 10.20, 26.20, 7.47)}
    for d, (b2, v, te, tr) in table.items():
        cb2, cv, ctr = rows[d]
        check(cb2, b2, 3 if d == 10 or d == 15 else 2, f"bias2 d={d}")
        check(cv, v, 2, f"variance d={d}")
        check(test[d], te, 2, f"test error d={d}")
        check(ctr, tr, 2, f"training MSE d={d}")
    assert max(test[5], test[6], test[7]) - test[5] < 0.25    # "within 0.25 of each other"

    # independent route for d = 5: raw-power design, hat matrix by pinv, direct moments of (28)
    x = np.linspace(8, 18, 30)
    g = np.linspace(8, 18, 400)
    B, B0 = np.vander((x - 13) / 5, 6), np.vander((g - 13) / 5, 6)
    P = B0 @ np.linalg.pinv(B)                               # row x0: b(x0)'(B'B)^-1 B'
    bias2 = np.mean((P @ psi(x) - psi(g)) ** 2)
    var = 16 * np.mean(np.sum(P ** 2, axis=1))
    assert abs(bias2 + var + 16 - test[5]) < 1e-8

    # optimism (33): E[in-sample test] - E[train] = 2 sigma^2 (d+1)/n, exactly, via trace(I - H) = n - d - 1
    H = B @ np.linalg.pinv(B)
    assert abs(np.trace(np.eye(30) - H) - 24) < 1e-9
    r = (np.eye(30) - H) @ psi(x)
    e_train = r @ r / 30 + 16 * (1 - 6 / 30)                 # (32)
    e_insample = r @ r / 30 + 16 * 6 / 30 + 16               # bias2 + variance + noise at the design points
    check(e_insample - e_train, 6.4, 10, "optimism 2 sigma^2 (d+1)/n at d = 5")
    check(e_train, 13.79, 2, "(32) equals the table's training column at d = 5")

    # section 4.1: straight line on psi(x) = 1 - x + 2x^2, x ~ U(0,1), sigma = 0.1 (bias-variance-R.txt)
    c = np.linalg.solve([[1, 1 / 2], [1 / 2, 1 / 3]], [1 / 3, 1 / 4])   # projection of x^2 on {1, x}
    assert np.allclose(c, [-1 / 6, 1])
    ib2 = 4 * integrate.quad(lambda t: (t * t - t + 1 / 6) ** 2, 0, 1)[0]
    assert abs(ib2 - 1 / 45) < 1e-12 and near(ib2, 0.0222, 4)
    rng = np.random.default_rng(2)
    xs = rng.uniform(0, 1, 900)
    Xl = np.column_stack([np.ones(900), xs])
    h = np.sum(Xl * np.linalg.solve(Xl.T @ Xl, Xl.T).T, axis=1)
    assert abs(h.mean() - 2 / 900) < 1e-12                  # average leverage = (p+1)/n, so (24) is exact at the design
    check(0.1 ** 2 * h.mean(), 0.0000222, 7, "(24) average variance")
    # Monte Carlo, design held fixed (the reading of (24)): redraw only the noise, R times
    R, grid = 4000, np.linspace(0, 1, 201)
    G = np.column_stack([np.ones_like(grid), grid])
    P = G @ np.linalg.solve(Xl.T @ Xl, Xl.T)                  # grid fit = P y
    Y = (1 - xs + 2 * xs ** 2) + rng.normal(0, 0.1, (R, 900))
    fits = Y @ P.T
    mc_b2 = np.mean((fits.mean(0) - (1 - grid + 2 * grid ** 2)) ** 2)
    mc_var = np.mean(fits.var(0))
    assert abs(mc_b2 / ib2 - 1) < 0.05 and abs(mc_var / 2.22e-5 - 1) < 0.1
    assert ib2 / mc_var > 500 and ib2 > 2 * 0.1 ** 2         # bias^2 ~ 1000 x variance, > 2 x noise
    # fresh x in every training set: the misspecification residual 2(x^2 - x + 1/6), variance 1/45,
    # now acts as extra noise, so the variance is ~ 2 (0.01 + 1/45) / 900 or more -- still ~ 1/250 of bias^2
    X = rng.uniform(0, 1, (R, 900))
    Y = 1 - X + 2 * X ** 2 + rng.normal(0, 0.1, (R, 900))
    xb, yb = X.mean(1), Y.mean(1)
    slope = ((X - xb[:, None]) * (Y - yb[:, None])).sum(1) / ((X - xb[:, None]) ** 2).sum(1)
    fresh_var = np.mean(((yb - slope * xb)[:, None] + slope[:, None] * grid).var(0))
    assert 2 * (0.01 + 1 / 45) / 900 < fresh_var < ib2 / 200
    print(f"1 bias-variance: d* = {dstar}, test error {test[dstar]:.2f}; optimism 6.4; "
          f"line on quadratic: bias2 {ib2:.4f} (MC {mc_b2:.4f}), var 2.22e-5 (MC fixed design {mc_var:.2e}, "
          f"fresh x {fresh_var:.2e})")
```

> **One nuance the asserts expose.** (24) — variance $\sigma^2\cdot2/n'=2.22\times10^{-5}$ — is the
> variance **with the design held fixed** (the Monte Carlo that redraws only the noise gives
> $2.24\times10^{-5}$). If every training set also draws fresh $x$'s, the misspecification residual
> $2(x^2-x+\frac16)$, of variance $1/45$, behaves like extra noise and the variance is about
> $8.6\times10^{-5}$ — four times larger, still some 260 times below the squared bias. Note 01's "1000
> times" is the fixed-design figure.

---

## 2 · Log-level readings, exact vs approximate → [[L02-02-linear-log-linear-regression]]

Wooldridge's coefficients through (11) and (12), the log-log case (15)–(16), every printout
check of note 02 (Credit, houseprice, Mroz, the quadratics), and a simulation showing that the
ratio of medians in a log-level model is $e^{\beta\Delta x}$, not $1+\beta\Delta x$.

```python
# ============================================================================ 2 · log-level readings (L02-02)
def exact_pct(z):
    """(11): exact % change in y when log y changes by z = beta * dx."""
    return 100 * np.expm1(z)


def section2():
    for z, approx, exact in [(0.083, 8.3, 8.65), (0.306, 30.6, 35.8), (-0.306, -30.6, -26.4),
                             (-0.052, -5.2, -5.1), (-0.260, -26.0, -22.9)]:
        check(100 * z, approx, 1, f"(12) at {z}")
        check(exact_pct(z), exact, 2 if z == 0.083 else 1, f"(11) at {z}")
    assert -exact_pct(-0.306) < 30.6 < exact_pct(0.306)                  # the arc reading sits between
    assert abs(exact_pct(0.3) - 30 - 100 * 0.3 ** 2 / 2) < 0.5            # error ~ 100 z^2 / 2: ~5 points at 0.3
    check(100 * (1.10 ** 0.257 - 1), 2.48, 2, "(16) log-log exact at +10%")
    check(0.257 * 10, 2.57, 2, "(14) log-log approx at +10%")
    check(18.501 * 100, 1850.1, 1, "units: roe -> roedec")
    check(429.6 / 16.61, 25.86, 2, "t Student")
    check(23.18 / 3.639, 6.37, 2, "t Cards")
    check(1 - (1 - 0.9536) * 399 / 395, 0.9531, 4, "(4) adjusted R2, Credit")
    check(0.092903 * 1.886008, 0.17522, 5, "(5) per sqft")
    check(0.092903 * 1.886008 * 1000 / 3.2, 54.75, 2, "dollars per sqft")
    b, n2, br = 1.9374668, -0.3614412, 0.2907379
    for val, want in [(b + br, 2.2282), (b + n2, 1.5760), (b + n2 + br, 1.8668)]:
        check(val, want, 4, "interaction table")
    rss = 735 * 0.4511 ** 2
    check(rss, 149.57, 2, "(19) RSS")
    check(1 - rss / 752, 0.8011, 4, "(19) R2")
    check(1 - (1 - 0.8011) * 753 / 735, 0.7962, 4, "(20) adjusted R2 no intercept")
    check(-0.711872 / 0.032891, -21.64, 2, "t MTR")
    check(np.sqrt(735 / 753), 0.98798, 5, "MLE/OLS SE ratio")
    check(0.029839 * np.sqrt(735 / 753), 0.029480, 6, "LFP MLE SE")
    check(0.298 / (2 * 0.0061), 24.4, 1, "(22) experience turning point")
    check(0.545 / 0.124, 4.4, 1, "(22) rooms turning point")
    check(-54.5 + 12.4 * 5, 7.5, 1, "(23) 5 -> 6 rooms")
    check(-54.5 + 12.4 * 6, 19.9, 1, "(23) 6 -> 7 rooms")
    check(np.log(9) - np.log(8), 0.118, 3, "log points 8 -> 9")
    check(100 * (9 - 8) / 8, 12.5, 1, "percent 8 -> 9")
    # simulation: in a log-level model the fitted ratio y1/y0 is exp(beta dx), not 1 + beta dx
    rng = np.random.default_rng(6)
    x = rng.uniform(0, 10, 400_000)
    y = np.exp(1 + 0.306 * x + rng.normal(0, 0.2, x.size))
    bhat = sm.OLS(np.log(y), sm.add_constant(x)).fit().params[1]
    med = [np.median(y[(x > a - 0.05) & (x < a + 0.05)]) for a in (4.0, 5.0)]   # medians of y at x = 4 and 5
    gap = 100 * (med[1] / med[0] - 1)
    assert abs(gap - exact_pct(bhat)) < 1.5 and abs(gap - 100 * bhat) > 3
    print(f"2 log readings: rooms +1 exact {exact_pct(0.306):.1f}% vs 30.6%; -1 exact {exact_pct(-0.306):.1f}%; "
          f"sales +10% exact {100 * (1.1 ** 0.257 - 1):.2f}% vs 2.57%")
```

---

## 3 · Validation set, LOOCV, $k$-fold and the bootstrap band → [[L02-03-cross-validation-motorcycle]]

The `mcycle` data are not in the repo, so the data-driven checks run on `make_figures`'
**stand-in** (simulated; its numbers are not the site's). The asserts cover: the site's printed
counts; LOOCV by brute force (6) = shortcut (7); the Sherman–Morrison step (12)–(13) on one point;
$k=n$ folds = LOOCV; (15) ≠ (16) with unequal folds; the whole stand-in table of note 03 §8 with the
same seeds and draw order as the figure; and the bootstrap SE (17) against the formula band (18) —
equal under homoskedasticity, wider on the heteroskedastic stand-in.

```python
# ============================================================================ 3 · validation, CV, bootstrap (L02-03)
def holdout_mse(x, y, d, train_idx, test_idx):
    """(5): validation-set estimate, fit on train_idx only."""
    return np.mean((y[test_idx] - mf.ols_predict(x[train_idx], y[train_idx], x[test_idx], d)) ** 2)


def kfold(x, y, d, folds, weighted=True):
    """k-fold CV for any list of index arrays `folds`: (16) if weighted (SSE / n), else (15) (mean of fold MSEs)."""
    mse, size = [], []
    for te in folds:
        tr = np.setdiff1d(np.arange(len(x)), te)
        mse.append(holdout_mse(x, y, d, tr, te))
        size.append(len(te))
    mse, size = np.array(mse), np.array(size)
    return float(size @ mse / size.sum()) if weighted else float(mse.mean())


def site_folds(perm, k=10):
    """The site's layout: L = trunc(n/k) shuffled positions per fold, the last fold takes the remainder."""
    n, L = len(perm), len(perm) // k
    return [perm[j * L:(j + 1) * L] if j < k - 1 else perm[j * L:] for j in range(k)]


def section3():
    wins = {6: 1, 8: 2, 9: 2, 10: 15, 11: 7, 12: 63, 13: 10}           # slide 7, 100 hold-out splits
    assert sum(wins.values()) == 100 and wins[10] + wins[11] + wins[12] + wins[13] == 95
    check(1 - 0.7798, 0.2202, 4, "(4) sigma2 at d = 12")
    check(np.sqrt(1 - 0.7798), 0.4693, 4, "(4) sigma at d = 12")
    check(13 / 132, 0.0985, 4, "mean leverage d = 12")
    check(4 / 132, 0.0303, 4, "mean leverage d = 3")
    assert [len(f) for f in site_folds(np.arange(132))] == [13] * 9 + [15]
    rng = np.random.default_rng(0)
    z = rng.normal(size=20)
    s = lambda v: (v - v.mean()) / v.std(ddof=1)
    assert np.allclose(s(3.7 * z - 2), s(z))                            # (2): affine maps are undone

    x, y = mf.mcycle_standin()
    ds = np.arange(1, 15)
    # LOOCV: brute force (6) vs the one-fit shortcut (7), both from make_figures
    brute = np.array([mf.loocv_brute(x, y, d) for d in ds])
    short = np.array([mf.loocv_shortcut(x, y, d)[0] for d in ds])
    assert np.allclose(brute, short, rtol=1e-8)
    # Sherman-Morrison step (12) on one point, with an orthonormal basis to keep it well conditioned
    Q, _ = np.linalg.qr(mf.design(x, 5))
    i = 7
    bfull = Q.T @ y
    e = y - Q @ bfull
    hii = Q[i] @ Q[i]
    keep = np.arange(132) != i
    b_loo = np.linalg.lstsq(Q[keep], y[keep], rcond=None)[0]
    assert np.allclose(b_loo, bfull - Q[i] * e[i] / (1 - hii))          # (12) with A = Q'Q = I
    assert abs((y[i] - Q[i] @ b_loo) - e[i] / (1 - hii)) < 1e-12         # (13)
    # (15) vs (16) differ when fold sizes differ; (16) reproduces make_figures' site-layout k-fold
    perm = np.random.default_rng(1).permutation(132)
    f = site_folds(perm)
    assert abs(kfold(x, y, 12, f) - mf.kfold_cv(x, y, 12, perm)) < 1e-12
    assert kfold(x, y, 12, f) != kfold(x, y, 12, f, weighted=False)
    assert abs(kfold(x, y, 3, [np.array([j]) for j in range(132)]) - brute[2]) < 1e-12   # k = n is LOOCV

    # the stand-in table of note 03 section 8, same seeds and order of draws as make_figures.fig_cv
    train = np.array([np.mean((y - mf.ols_predict(x, y, x, d)) ** 2) for d in ds])
    rng = np.random.default_rng(56789)
    hold = np.array([[holdout_mse(x, y, d, p[:105], p[105:]) for d in ds]
                     for p in (rng.permutation(132) for _ in range(100))])
    kf = np.array([[kfold(x, y, d, site_folds(p)) for d in ds] for p in (rng.permutation(132) for _ in range(100))])
    want = {1: (0.9252, 0.9550, 0.9461, 0.9481), 3: (0.7376, 0.7954, 0.7781, 0.7810),
            5: (0.5388, 0.6192, 0.5900, 0.5917), 7: (0.3219, 0.3746, 0.3567, 0.3577),
            10: (0.1847, 0.2262, 0.2174, 0.2197), 12: (0.1737, 0.2220, 0.2082, 0.2117),
            13: (0.1736, 0.2357, 0.2109, 0.2164), 14: (0.1722, 0.2501, 0.2107, 0.2179)}
    for d, row in want.items():
        for got, w, lab in zip((train[d - 1], hold.mean(0)[d - 1], short[d - 1], kf.mean(0)[d - 1]), row,
                               ("train", "hold-out", "LOOCV", "10-fold")):
            check(got, w, 4, f"stand-in {lab} d={d}")
    for est in (hold.mean(0), short, kf.mean(0)):
        assert ds[np.argmin(est)] == 12
    assert np.all(train < short) and np.all(short < kf.mean(0)) and np.all(kf.mean(0)[4:] < hold.mean(0)[4:])
    pick_h = np.bincount(ds[hold.argmin(1)], minlength=15)
    pick_k = np.bincount(ds[kf.argmin(1)], minlength=15)
    assert (pick_h[14], pick_h[12], pick_h[10], pick_h[13], 100 - pick_h[[10, 12, 13, 14]].sum()) == (31, 30, 23, 10, 6)
    assert pick_k[12] == 82

    # pairs bootstrap (17) vs the formula band (18): equal on homoskedastic data, bootstrap wider here
    def bands(xx, yy, d, B, seed):
        g = np.linspace(xx.min(), xx.max(), 200)
        rb = np.random.default_rng(seed)
        boot = np.array([mf.ols_predict(xx[k], yy[k], g, d) for k in rb.integers(0, len(xx), (B, len(xx)))])
        X = mf.design(xx, d)
        beta, rss = np.linalg.lstsq(X, yy, rcond=None)[:2]
        G = mf.design(g, d)
        Qx, Rx = np.linalg.qr(X)
        se = np.sqrt(rss[0] / (len(xx) - d - 1)) * np.linalg.norm(np.linalg.solve(Rx.T, G.T), axis=0)
        return g, boot.std(0, ddof=1), se, np.percentile(boot, [2.5, 97.5], axis=0)
    xh = np.random.default_rng(4).uniform(-1, 1, 200)
    yh = np.sin(2 * xh) + np.random.default_rng(5).normal(0, 0.3, 200)
    _, seb, sef, _ = bands(xh, yh, 3, 2000, 7)
    assert abs(np.mean(seb / sef) - 1) < 0.1                            # homoskedastic: the two agree
    g, seb, sef, (lo, hi) = bands(x, y, 12, 1000, 31415)
    noisy = g > -0.5
    assert np.mean(hi[noisy] - lo[noisy]) > np.mean(4 * sef[noisy])     # heteroskedastic stand-in: bootstrap wider
    print(f"3 CV: stand-in argmin 12 for hold-out/LOOCV/10-fold; 10-fold picks 12 {pick_k[12]}/100, "
          f"hold-out {pick_h[12]}/100; LOOCV shortcut = brute force; bootstrap SE/formula SE "
          f"(homoskedastic) = 1 +- 0.1")
```

---

## 4 · Logistic regression by IRLS, against statsmodels → [[L02-04-logistic-regression]]

`irls` is note 04 (16)–(17) as code, with frequency weights so that the four cells of the student
table stand for 10,000 rows. It reproduces the iteration table of note 04 §4.1 to five decimals,
the closed form, the slide's SEs and deviance, and `statsmodels`' GLM. The `default` and
balance + student numbers come from the **printed coefficients** (the data are not on disk); a
simulated default-like sample checks `irls` against `sm.Logit` on a continuous covariate; perfectly
separated data make it fail, as they must.

```python
# ============================================================================ 4 · logistic regression (L02-04)
def irls(X, y, link, f=None, beta0=None, tol=1e-10, maxit=100):
    """Newton-Raphson as iteratively reweighted least squares (note 04 (16)-(17); note 06 section 3).

    X: n x (p+1) design with a leading column of ones; y: responses (0/1 for "logit", counts for "log");
    link: "logit" (Bernoulli) or "log" (Poisson), both canonical; f: frequency weights (rows repeated
    f_i times; None = 1); beta0: start (default 0). Returns (beta, standard errors from (X'WX)^-1,
    history of (beta, -2 loglik up to a constant) after each iteration). Raises RuntimeError when it
    does not converge, e.g. under perfect separation (no finite logit MLE).
    """
    f = np.ones(len(y)) if f is None else np.asarray(f, float)
    mean = expit if link == "logit" else np.exp
    vfun = (lambda m: m * (1 - m)) if link == "logit" else (lambda m: m)
    m2ll = ((lambda m: -2 * np.sum(f * (y * np.log(m) + (1 - y) * np.log1p(-m)))) if link == "logit"
            else (lambda m: -2 * np.sum(f * (y * np.log(m) - m))))
    beta = np.zeros(X.shape[1]) if beta0 is None else np.asarray(beta0, float)
    hist = []
    for _ in range(maxit):
        eta = X @ beta
        mu = mean(eta)
        w = f * vfun(mu)
        z = eta + (y - mu) / vfun(mu)                                    # adjusted response (17)
        new = np.linalg.solve(X.T @ (w[:, None] * X), X.T @ (w * z))     # weighted LS (16)
        hist.append((new, m2ll(mean(X @ new))))
        done = np.max(np.abs(new - beta)) < tol
        beta = new
        if done:
            break
    else:
        raise RuntimeError("IRLS did not converge")
    mu = mean(X @ beta)
    cov = np.linalg.inv(X.T @ ((f * vfun(mu))[:, None] * X))
    return beta, np.sqrt(np.diag(cov)), hist


def confusion_metrics(tn, fp, fn, tp):
    """Rates of note 04 section 9, 'positive' = spam; 'slide_fd' is the deck's FP / (FP + all actual positives)."""
    return dict(error=(fp + fn) / (tn + fp + fn + tp), fnr=fn / (fn + tp), fpr=fp / (fp + tn),
                sens=tp / (tp + fn), spec=tn / (tn + fp), prec=tp / (tp + fp), fdr=fp / (fp + tp),
                slide_fd=fp / (fp + tp + fn))


def section4():
    # the student-only model from the 2x2 table of slide 18, as four weighted rows
    s = np.array([0, 0, 1, 1.0])
    yv = np.array([0, 1, 0, 1.0])
    cnt = np.array([6850, 206, 2817, 127])
    X = sm.add_constant(s)
    beta, se, hist = irls(X, yv, "logit", f=cnt)
    table = [(-1.88322, 0.05577, 4116.20), (-2.78054, 0.15372, 3072.81), (-3.31150, 0.29836, 2917.50),
             (-3.48780, 0.39184, 2908.74), (-3.50400, 0.40477, 2908.683), (-3.50413, 0.40489, 2908.683)]
    for k, (b0, b1, dev) in enumerate(table):
        (c0, c1), cdev = hist[k]
        check(c0, b0, 5, f"IRLS iteration {k + 1} beta0")
        check(c1, b1, 5, f"IRLS iteration {k + 1} beta1")
        check(cdev, dev, 3 if k >= 4 else 2, f"IRLS iteration {k + 1} -2loglik")
    check(beta[0], np.log(206 / 6850), 9, "closed form beta0")
    check(beta[1], np.log((127 / 2817) / (206 / 6850)), 9, "closed form beta1")
    check(beta[0], -3.50413, 5, "slide 18 beta0")
    check(beta[1], 0.40489, 5, "slide 18 beta1")
    check(se[0], 0.07071, 5, "slide 18 SE beta0")
    check(se[1], 0.11502, 5, "slide 18 SE beta1")
    assert abs(se[1] - np.sqrt(1 / 206 + 1 / 6850 + 1 / 127 + 1 / 2817)) < 1e-9
    glm = sm.GLM(yv, X, family=sm.families.Binomial(), freq_weights=cnt).fit()
    assert np.allclose(glm.params, beta, atol=1e-8) and np.allclose(glm.bse, se, atol=1e-8)
    check(glm.deviance, 2908.7, 1, "slide 18 residual deviance")
    check(glm.null_deviance, 2920.6, 1, "null deviance")
    check(-2 * (333 * np.log(0.0333) + 9667 * np.log(0.9667)), 2920.6, 1, "null deviance by hand")
    check(100 * expit(beta.sum()), 4.31, 2, "P(default | student)")       # the deck prints 0.43%
    check(100 * expit(beta[0]), 2.92, 2, "P(default | non-student)")     # the deck prints 0.29%
    check(np.exp(beta[1]), 1.499, 3, "odds ratio student")
    assert abs(np.sum(cnt * (yv - expit(X @ beta)))) < 1e-6              # score row 1: mean fitted = share of 1s

    # the balance-only model from its printed coefficients (slides 13, 15, 17)
    b0, b1 = -10.6513, 0.0055
    check(100 * expit(b0 + b1 * 1000), 0.58, 2, "P at 1000")
    check(100 * expit(b0 + b1 * 2000), 58.6, 1, "P at 2000")
    check(-b0 / b1, 1936.6, 1, "(19) 50% cut-off")
    for c, x1, x2 in [(0.1, 1537.1, 1537.4), (0.2, 1684.5, 1684.9), (0.3, 1782.5, 1782.9), (0.4, 1862.9, 1863.2),
                      (0.6, 2010.3, 2010.7), (0.7, 2090.7, 2091.0), (0.8, 2188.7, 2189.1), (0.9, 2336.1, 2336.5)]:
        check((logit(c) - b0) / 0.0055, x1, 1, f"cut-off c={c}, slope 0.0055")
        check((logit(c) - b0) / 0.005499, x2, 1, f"cut-off c={c}, slope 0.005499")
    check(0.07519 / 0.0001299, 578.8, 1, "LPM zero crossing")
    check(-0.07519 + 0.0001299 * 2000, 0.185, 3, "LPM at 2000")
    check(np.exp(0.0055 * 100), 1.733, 3, "odds ratio per USD 100")
    pe_cut, pe_1000 = 0.0055 * 0.25, 0.0055 * expit(b0 + b1 * 1000) * (1 - expit(b0 + b1 * 1000))
    check(pe_cut, 0.001375, 6, "(8) at the cut-off")
    check(pe_1000, 0.0000315, 7, "(8) at 1000")
    assert round(pe_cut / pe_1000) == 44
    check(-10.65 / 0.3612, -29.49, 2, "z intercept")
    check(0.005499 / 0.0002204, 24.95, 2, "z balance")
    for dev, k, aic in [(1596.5, 2, 1600.5), (2908.7, 2, 2912.7), (1571.7, 3, 1577.7)]:
        check(dev + 2 * k, aic, 1, "AIC = deviance + 2k")
    for lr, want in [(2920.6 - 1596.5, 1324.1), (2920.6 - 2908.7, 11.9), (1596.5 - 1571.7, 24.8)]:
        check(lr, want, 1, "LR test")
        assert lr > stats.chi2.ppf(0.95, 1)
    for dev, want in [(1596.5, 0.453), (1571.7, 0.462), (2908.7, 0.004)]:
        check(1 - dev / 2920.6, want, 3, "McFadden pseudo-R2")
    # balance + student (slide 20) and the group cut-offs (slide 22 swaps them)
    c0, c1, c2 = -10.75, 0.005738, -0.7149
    check(100 * expit(c0 + c1 * 1500 + c2), 5.4, 1, "student at 1500")
    check(100 * expit(c0 + c1 * 1500), 10.5, 1, "non-student at 1500")
    check(-(c0 + c2) / c1, 1998.1, 1, "50% cut-off, student")
    check(-c0 / c1, 1873.5, 1, "50% cut-off, non-student")
    check(np.exp(c2), 0.489, 3, "odds ratio student | balance")

    # IRLS on simulated default-like data vs statsmodels' Logit, and recovery of the true coefficients
    rng = np.random.default_rng(10)
    bal = rng.gamma(4.0, 210.0, 10_000)
    yy = rng.binomial(1, expit(b0 + b1 * bal)).astype(float)
    Xs = sm.add_constant(bal)
    bh, seh, _ = irls(Xs, yy, "logit")
    ref = sm.Logit(yy, Xs).fit(disp=0)
    assert np.allclose(bh, ref.params, rtol=1e-8) and np.allclose(seh, ref.bse, rtol=1e-6)
    assert np.all(np.abs(bh - [b0, b1]) < 3.5 * seh)
    try:                                                                # perfect separation: no finite MLE
        with np.errstate(all="ignore"):
            irls(sm.add_constant(np.arange(10.0)), (np.arange(10) > 4).astype(float), "logit", maxit=30)
        raise AssertionError("separated data should not converge")
    except (RuntimeError, np.linalg.LinAlgError):
        pass

    # the spam confusion matrices (slides 36-38)
    spam = {"glm": (1325, 80, 93, 803, 7.52, 10.38, 5.69, 9.06, 8.20),
            "ridge": (1345, 60, 128, 768, 8.17, 14.29, 4.27, 7.25, 6.28),
            "enet": (1349, 56, 94, 802, 6.52, 10.49, 3.99, 6.53, 5.88),
            "lasso": (1347, 58, 95, 801, 6.65, 10.60, 4.13, 6.75, 6.08),
            "bayes": (1326, 79, 91, 805, 7.39, 10.16, 5.62, 8.94, 8.10)}
    for name, (tn, fp, fn, tp, err, fnr, fpr, fdr, sfd) in spam.items():
        m = confusion_metrics(tn, fp, fn, tp)
        assert tn + fp + fn + tp == 2301 and fn + tp == 896
        for key, want in zip(("error", "fnr", "fpr", "fdr", "slide_fd"), (err, fnr, fpr, fdr, sfd)):
            check(100 * m[key], want, 2, f"spam {name} {key}")
    m = confusion_metrics(*spam["glm"][:4])
    check(100 * m["sens"], 89.62, 2, "sensitivity")
    check(100 * m["spec"], 94.31, 2, "specificity")
    check(100 * m["prec"], 90.94, 2, "precision")
    assert min(spam, key=lambda k: spam[k][4]) == "enet" and max(spam, key=lambda k: spam[k][5]) == "ridge"
    print(f"4 logistic: IRLS student model {beta.round(5)} (SE {se.round(5)}) = statsmodels; "
          f"P 0.58%/58.6%, cut-off {-b0 / b1:.1f}; spam FDR 9.06% (slide 8.20%)")
```

> **The student model is the one `default` fit that can be reproduced exactly**, because slide 18
> prints the whole $2\times2$ table: `irls` returns $(-3.50413,\ 0.40489)$ with SEs
> $(0.07071,\ 0.11502)$, and the fitted probabilities are 2.92% and 4.31% — not the slide's 0.29% and
> 0.43%.

---

## 5 · Discriminant analysis: Gaussian cut-offs, costs, ROC, LDA/QDA on iris → [[L02-05-discriminant-analysis]]

The Bernoulli example and its prior thresholds; the quadratic $h$ of (7) with roots 1.680 and
10.001 (and `mf.h_roots` agreeing); the misallocation probabilities 0.3881 / 0.1148 / 0.3694; a
scan showing that **no single cut-off beats the two-cut-off Bayes rule** (the content of (3)); the
cost rule; ISLP's `default` tables; both AUCs, the unequal one by direct integration (independent
of the figure's trapezoid); the LDA posterior as a logistic function; and iris LDA from the slide's
summaries, with QDA computed on the same summaries.

```python
# ============================================================================ 5 · discriminant analysis (L02-05)
def h_coef(m1, m2, s1, s2):
    """(7) as a x^2 + b x + c."""
    a = -0.5 * (1 / s1 ** 2 - 1 / s2 ** 2)
    b = m1 / s1 ** 2 - m2 / s2 ** 2
    c = -0.5 * (m1 ** 2 / s1 ** 2 - m2 ** 2 / s2 ** 2) + np.log(s2 / s1)
    return a, b, c


def misallocation(lo, hi, m1=1.0, m2=5.0, s1=6.0, s2=2.5):
    """p21, p12 when R2 = (lo, hi) and R1 is its complement (section 6)."""
    p21 = stats.norm.cdf(hi, m1, s1) - stats.norm.cdf(lo, m1, s1)
    p12 = 1 - (stats.norm.cdf(hi, m2, s2) - stats.norm.cdf(lo, m2, s2))
    return p21, p12


def section5():
    # Bernoulli example (slide 43) and the priors that move it
    p1, p2 = {0: 0.5, 1: 0.5}, {0: 0.25, 1: 0.75}
    check(np.log(p1[0] / p2[0]), 0.693, 3, "h(0)")
    check(np.log(p1[1] / p2[1]), -0.405, 3, "h(1)")
    assert 0.5 * (0.5 + 0.25) == 3 / 8
    rules = [(1, 2), (2, 2), (1, 1), (2, 1)]                              # allocation of x = 0, x = 1
    pkk = {r: (sum(p1[x] for x in (0, 1) if r[x] == 1), sum(p2[x] for x in (0, 1) if r[x] == 2)) for r in rules}
    assert pkk[(1, 2)] == (0.5, 0.75) and pkk[(2, 1)] == (0.5, 0.25)      # (2,1) dominated by ML: inadmissible
    for pi1, want in [(0.30, (2, 2)), (0.34, (1, 2)), (0.59, (1, 2)), (0.61, (1, 1))]:
        bayes = tuple(1 if pi1 * p1[x] > (1 - pi1) * p2[x] else 2 for x in (0, 1))
        assert bayes == want, (pi1, bayes)
    assert np.log(0.5 / 0.25) > 0                                         # multinomial x = (1,0): class 1, slide 44 says "< 0"

    # univariate Gaussians, mu1 = 1, mu2 = 5, sigma1 = 6, sigma2 = 2.5 (slides 45-47)
    a, b, c = h_coef(1, 5, 6, 2.5)
    for v, want in [(a, 0.066111), (b, -0.772222), (c, 1.110642)]:
        check(v, want, 6, "h coefficients")
    roots = np.sort(np.roots([a, b, c]).real)
    assert np.allclose(roots, mf.h_roots(0.0))
    check(roots[0], 1.680, 3, "x_L")
    check(roots[1], 10.001, 3, "x_U")
    hx = lambda x: a * x * x + b * x + c
    assert abs(hx(3.0) - (stats.norm.logpdf(3, 1, 6) - stats.norm.logpdf(3, 5, 2.5))) < 1e-12
    check(hx(-20), 43.0, 1, "h(-20)")
    check(hx(20), 12.1, 1, "h(20)")
    check(-b / (2 * a), 5.840, 3, "argmin h")
    check(hx(-b / (2 * a)), -1.144, 3, "min h")
    p21, p12 = misallocation(*roots)
    check(p21, 0.3881, 4, "p21")
    check(p12, 0.1148, 4, "p12")
    check(0.5 * (p21 + p12), 0.2515, 4, "total error, unequal variances")
    pe = stats.norm.sf(3, 1, 6)
    check(pe, 0.3694, 4, "p21 = p12, equal variances")
    check(-(-20 - 3) / 9, 2.556, 3, "equal-variance h(-20)")
    # Bayes optimality (3): no single cut-off (a linear rule) beats the quadratic Bayes rule
    t = np.linspace(-10, 15, 5001)
    single = 0.5 * (stats.norm.sf(t, 1, 6) + stats.norm.cdf(t, 5, 2.5))   # allocate to 1 iff x < t
    assert single.min() > 0.5 * (p21 + p12)
    # unequal costs: c21/c12 = 2 -> threshold log(1/2) (14)
    rc = mf.h_roots(np.log(0.5))
    check(rc[0], 3.228, 3, "cost-rule x_L")
    check(rc[1], 8.453, 3, "cost-rule x_U")
    q21, q12 = misallocation(*rc)
    for v, want in [(q21, 0.2481), (q12, 0.3228), (0.5 * (q21 + q12), 0.2855),
                    (0.5 * (2 * p21) + 0.5 * p12, 0.4455), (0.5 * (2 * q21) + 0.5 * q12, 0.4095)]:
        check(v, want, 4, "cost table")
    check(np.exp(-hx(-b / (2 * a))), 3.14, 2, "ratio that empties R2")
    assert mf.h_roots(-np.log(3.2)) is None and mf.h_roots(-np.log(3.1)) is not None
    # posterior threshold (15) and I's default tables
    assert abs(1 / (1 + 4) - 0.2) < 1e-15                                  # c12/(c12+c21) = 0.2 <=> c21 = 4 c12
    for miss, fa, err, rate in [(252, 23, 2.75, 75.7), (138, 235, 3.73, 41.4)]:
        check(100 * (miss + fa) / 10_000, err, 2, "I default error rate")
        check(100 * miss / 333, rate, 1, "I missed share")
    assert 4 * 252 + 23 == 1031 and 4 * 138 + 235 == 787
    # AUCs (section 11): equal variance in closed form; unequal by direct integration
    check(stats.norm.cdf(4 / np.sqrt(72)), 0.681, 3, "AUC equal variances")

    def p_h1_above(k):                                                   # P(h(X1) > k), X1 ~ N(1, 36)
        r = mf.h_roots(k)
        return 1.0 if r is None else 1 - (stats.norm.cdf(r[1], 1, 6) - stats.norm.cdf(r[0], 1, 6))
    auc = integrate.quad(lambda u: p_h1_above(hx(u)) * stats.norm.pdf(u, 5, 2.5), -15, 25, limit=200)[0]
    check(auc, 0.802, 3, "AUC unequal variances")
    # LDA posterior is a logistic function of x (7.1), here p = 1, sigma = 6, pi1 = 0.3
    xg = np.linspace(-10, 15, 7)
    post = 0.3 * stats.norm.pdf(xg, 1, 6) / (0.3 * stats.norm.pdf(xg, 1, 6) + 0.7 * stats.norm.pdf(xg, 5, 6))
    alpha = (1 - 5) / 36
    assert np.allclose(post, expit(np.log(0.3 / 0.7) - alpha * 3 + alpha * xg))

    # iris, the two sepal measurements (slide 54), LDA by Mahalanobis distance (10)
    mu = np.array([[5.006, 3.428], [5.936, 2.770], [6.588, 2.974]])
    S = np.array([[[0.122, 0.097], [0.097, 0.141]], [[0.261, 0.083], [0.083, 0.096]],
                  [[0.396, 0.092], [0.092, 0.102]]])
    Sp = S.mean(0)
    assert np.allclose(Sp, [[0.25967, 0.09067], [0.09067, 0.11300]], atol=5e-6)
    check(np.linalg.det(Sp), 0.021122, 6, "|Sigma pooled|")
    Si = np.linalg.inv(Sp)
    assert np.allclose(Si, [[5.3499, -4.2925], [-4.2925, 12.2937]], atol=5e-4)
    flowers = np.array([[5.1, 3.5], [7.0, 3.2], [6.3, 3.3]])
    D = np.array([[(f - m) @ Si @ (f - m) for m in mu] for f in flowers])
    want = [[0.053, 15.530, 21.966], [25.814, 4.402, 0.737], [10.581, 2.506, 2.556]]
    assert np.all(np.abs(D - want) <= 0.0005), D                      # every distance to 3 decimals
    assert list(D.argmin(1)) == [0, 2, 1]                              # setosa, virginica (wrong), versicolor (wrong)
    al = Si @ (mu[0] - mu[1])
    assert np.allclose(al, [-7.800, 12.081], atol=2e-3)
    check(al @ (flowers[0] - mu[:2].mean(0)), 7.738, 2, "flower 1, setosa vs versicolor")
    # QDA (12) with class covariances; with every Sigma_k set to the pooled one it must reproduce LDA
    def qda_scores(xv, covs):
        return np.array([-0.5 * np.log(np.linalg.det(Sk)) - 0.5 * (xv - m) @ np.linalg.solve(Sk, xv - m)
                         for m, Sk in zip(mu, covs)])
    assert all(qda_scores(f, [Sp] * 3).argmax() == D[i].argmin() for i, f in enumerate(flowers))
    qda = [int(qda_scores(f, S).argmax()) for f in flowers]
    for k, want in [(31 / 85, 0.3647), (26 / 85, 0.3059), (28 / 85, 0.3294)]:
        check(k, want, 4, "admission priors")
    names = ["setosa", "versicolor", "virginica"]
    print(f"5 discriminant: cut-offs {roots.round(3)}, errors {p21:.4f}/{p12:.4f} (total {0.5 * (p21 + p12):.4f}); "
          f"cost rule {rc.round(3)}; AUC {auc:.3f}; iris LDA -> {[names[k] for k in D.argmin(1)]}, "
          f"QDA (computed here, no source value) -> {[names[k] for k in qda]}")
```

> **QDA on the three printed iris flowers** (class covariances from slide 54, equal priors): setosa,
> virginica, virginica — flower 101 moves from versicolor (LDA) to its true class. **The deck prints no
> QDA allocation for these flowers, so this is a computed value with no source to check against**; the
> assert that does bind is that QDA with every $\Sigma_k$ set to the pooled matrix reproduces LDA.

---

## 6 · Poisson regression by IRLS, against statsmodels → [[L02-06-gaussian-vs-poisson-regression]]

The same `irls` with the log link; every number of note 06 — the closed form, the SEs from the group
totals, rate ratio, deviances, Pearson dispersion and the quasi-Poisson correction (also through
`statsmodels`' `scale="X2"`), and the Gaussian fit beside it.

```python
# ============================================================================ 6 · Gaussian vs Poisson (L02-06)
def section6():
    y = mf.Y.astype(float)
    w = (np.tile(np.arange(1, 8), 4) <= 3).astype(float)               # fri, sat, sun = weekend on the page
    assert (w.sum(), y[w == 0].sum(), y[w == 1].sum()) == (12, 1744, 1000)
    X = sm.add_constant(w)
    beta, se, hist = irls(X, y, "log", beta0=[np.log(y.mean()), 0.0])
    ref = sm.GLM(y, X, family=sm.families.Poisson()).fit()
    assert np.allclose(beta, ref.params, atol=1e-9) and np.allclose(se, ref.bse, atol=1e-9)
    check(beta[0], 4.69135, 5, "alpha")
    check(beta[1], -0.26850, 5, "beta")
    assert abs(beta[0] - np.log(109)) < 1e-9 and abs(beta[1] - np.log((1000 / 12) / 109)) < 1e-9
    check(se[0], 0.02395, 5, "SE alpha")
    check(se[1], 0.03967, 5, "SE beta")
    assert abs(se[0] - 1 / np.sqrt(1744)) < 1e-9 and abs(se[1] - np.sqrt(1 / 1744 + 1 / 1000)) < 1e-9
    check(beta[1] / se[1], -6.77, 2, "z")
    check(np.exp(beta[1]), 0.7645, 4, "rate ratio")
    check(100 * np.expm1(beta[1]), -23.5, 1, "exact % change")
    check(100 * beta[1], -26.85, 2, "100 beta shortcut (note 06 section 4)")
    check(100 * beta[1] - 100 * np.expm1(beta[1]), -3.30, 2, "gap (note 06 says 3.4: difference of rounded values)")
    check(ref.deviance, 38.324, 3, "residual deviance")
    check(ref.null_deviance, 85.141, 3, "null deviance")
    check(ref.null_deviance - ref.deviance, 46.82, 2, "LR weekend")
    check(ref.aic, 221.76, 2, "AIC")
    check(stats.chi2.sf(ref.deviance, 26), 0.056, 3, "P(chi2_26 > deviance)")
    lam = ref.fittedvalues
    pearson = np.sum((y - lam) ** 2 / lam)
    check(pearson, 37.546, 3, "Pearson chi2")
    s2q = pearson / 26
    check(s2q, 1.444, 3, "dispersion")
    check(np.sqrt(s2q), 1.202, 3, "sigma hat")
    check(np.sqrt(s2q) * se[1], 0.0477, 4, "quasi-Poisson SE")
    check(beta[1] / (np.sqrt(s2q) * se[1]), -5.63, 2, "quasi-Poisson z")
    check((ref.null_deviance - ref.deviance) / s2q, 32.4, 1, "LR / dispersion")
    qp = sm.GLM(y, X, family=sm.families.Poisson()).fit(scale="X2")
    assert abs(qp.bse[1] - np.sqrt(s2q) * se[1]) < 1e-12
    # the Gaussian regression on the same dummy
    ols = sm.OLS(y, X).fit()
    check(ols.params[0], 109.000, 3, "beta0 OLS")
    check(ols.params[1], -25.667, 3, "beta1 OLS")
    s = np.sqrt(ols.scale)
    check(s, 11.85, 2, "residual SE")
    check(s ** 2, 140.4, 1, "s^2")
    check(ols.bse[1], 4.525, 3, "SE beta1")
    check(ols.bse[0], 2.962, 3, "SE beta0")
    check(ols.tvalues[1], -5.67, 2, "t")
    check(ols.rsquared, 0.553, 3, "R2")
    assert abs(ols.pvalues[1] - 5.8e-6) < 0.05e-6
    for grp, mean_, sd_, var_, ratio in [(0, 109.00, 12.15, 147.73, 1.36), (1, 83.33, 11.42, 130.42, 1.57)]:
        v = y[w == grp]
        check(v.mean(), mean_, 2, "group mean")
        check(v.std(ddof=1), sd_, 2, "group sd")
        check(v.var(ddof=1), var_, 2, "group variance")
        check(v.var(ddof=1) / v.mean(), ratio, 2, "variance / mean")
    check(1.96 * np.sqrt(109), 20.5, 1, "Poisson band weekday")
    check(1.96 * np.sqrt(1000 / 12), 17.9, 1, "Poisson band weekend")
    outside = np.sum(np.abs(y - lam) > 1.96 * np.sqrt(lam))
    assert outside == 3 and abs(28 * 0.05 - 1.4) < 1e-12
    print(f"6 Poisson: IRLS {beta.round(5)} (SE {se.round(5)}) = statsmodels in {len(hist)} iterations; "
          f"rate ratio {np.exp(beta[1]):.4f}; dispersion {s2q:.3f}; quasi z {beta[1] / (np.sqrt(s2q) * se[1]):.2f}")
```

> **A rounding remark on note 06 §4.** From the printed $\hat\beta=-0.26850$, the log reading is
> $100\hat\beta=-26.85\%$ and the exact one $-23.55\%$: they differ by **3.30** points. Rounding the
> first to −26.9% before subtracting would give 3.4, the difference of two rounded figures.

---

## 7 · The counterexamples of the pitfalls note → [[L02-08-pitfalls]]

The numbers Part I and Part II use that are not already in a section note: the optimum moving from
$d^*=5$ to 7 as $n$ grows, the pure-noise $E[R^2]=k/(n-1)$, the probability after an odds ratio,
the trivial credit rule, FDR vs FPR, ML vs Bayes error, $h(12)$, and quasi-Poisson leaving
$\hat\beta$ unchanged.

```python
# ============================================================================ 7 · counterexamples of L02-08-pitfalls
def section7():
    # training error ranks the degrees backwards (pitfall 1): d = 15 beats d = 5 in training, loses in test
    tr5, tr15 = mf.poly_bias_variance(5)[2], mf.poly_bias_variance(15)[2]
    te = lambda d, n=30: sum(mf.poly_bias_variance(d, n=n)[:2]) + 16
    assert tr15 < tr5 and te(15) > te(5) and tr15 < 16                 # d = 15 even trains below sigma^2
    # more data moves the optimum right (V/F 7): d* = 5 at n = 30, 7 at n = 60 and 200
    assert [int(np.argmin([te(d, n) for d in range(16)])) for n in (30, 60, 200)] == [5, 7, 7]
    # selection optimism (pitfall 5): pure noise, k = 12 polynomial terms, n = 132 -> E[R2] = k / (n - 1)
    rng = np.random.default_rng(0)
    r2 = []
    for _ in range(4000):
        x, y = rng.normal(size=132), rng.normal(size=132)
        e = y - mf.ols_predict(x, y, x, 12)
        r2.append(1 - e @ e / np.sum((y - y.mean()) ** 2))
    check(12 / 131, 0.0916, 4, "E[R2] under pure noise")
    assert abs(np.mean(r2) - 12 / 131) < 0.003
    # odds ratio is not a probability ratio (pitfall 7): odds 1 -> 1.733 moves p from 0.5 to 0.634
    check(np.exp(0.55) / (1 + np.exp(0.55)), 0.634, 3, "p after an odds ratio of 1.733 at p = 0.5")
    check((127 / 2944) / (206 / 7056), 1.478, 3, "probability ratio, student table")
    # accuracy under imbalance (pitfall 10): the all-"no" rule vs LDA at 0.2, I's default tables
    assert 333 / 10_000 < (138 + 235) / 10_000 and 4 * 333 > 4 * 138 + 235
    # FDR > FPR iff fewer flagged than actual negatives (pitfall 11)
    tn, fp, fn, tp = 1325, 80, 93, 803
    assert (fp / (fp + tp) > fp / (fp + tn)) == (fp + tp < fp + tn)
    # ML vs Bayes rule (pitfall 13): Bernoulli example with pi1 = 0.25
    ml_err = 0.25 * 0.5 + 0.75 * 0.25                                  # ML rule (1, 2): p21 = 1/2, p12 = 1/4
    bayes_err = 0.25                                                   # pi1 < 1/3: everything to class 2
    assert (ml_err, bayes_err) == (0.3125, 0.25)
    # a far observation goes to the wide class (V/F 23): h(12) > 0 in the deck's example
    a, b, c = h_coef(1, 5, 6, 2.5)
    check(a * 144 + b * 12 + c, 1.364, 3, "h(12)")
    # overdispersion leaves the Poisson point estimates alone (pitfall 15)
    y = mf.Y.astype(float)
    X = sm.add_constant((np.tile(np.arange(1, 8), 4) <= 3).astype(float))
    p, q = sm.GLM(y, X, family=sm.families.Poisson()).fit(), sm.GLM(y, X, family=sm.families.Poisson()).fit(scale="X2")
    assert np.allclose(p.params, q.params) and np.all(q.bse > p.bse)
    print("7 pitfalls: training ranks d = 15 over d = 5; d* 5 -> 7 as n grows; pure-noise E[R2] 0.0916; "
          "OR 1.733 at p = 0.5 gives 0.634; ML 0.3125 vs Bayes 0.25 at pi1 = 0.25")


if __name__ == "__main__":
    section1()
    section2()
    section3()
    section4()
    section5()
    section6()
    section7()
    print("ALL L02 CHECKS PASSED")
```

---

## 8 · The run

```text
1 bias-variance: d* = 5, test error 19.81; optimism 6.4; line on quadratic: bias2 0.0222 (MC 0.0227), var 2.22e-5 (MC fixed design 2.24e-05, fresh x 8.56e-05)
2 log readings: rooms +1 exact 35.8% vs 30.6%; -1 exact -26.4%; sales +10% exact 2.48% vs 2.57%
3 CV: stand-in argmin 12 for hold-out/LOOCV/10-fold; 10-fold picks 12 82/100, hold-out 30/100; LOOCV shortcut = brute force; bootstrap SE/formula SE (homoskedastic) = 1 +- 0.1
4 logistic: IRLS student model [-3.50413  0.40489] (SE [0.07071 0.11502]) = statsmodels; P 0.58%/58.6%, cut-off 1936.6; spam FDR 9.06% (slide 8.20%)
5 discriminant: cut-offs [ 1.68  10.001], errors 0.3881/0.1148 (total 0.2515); cost rule [3.228 8.453]; AUC 0.802; iris LDA -> ['setosa', 'virginica', 'versicolor'], QDA (computed here, no source value) -> ['setosa', 'virginica', 'virginica']
6 Poisson: IRLS [ 4.69135 -0.2685 ] (SE [0.02395 0.03967]) = statsmodels in 5 iterations; rate ratio 0.7645; dispersion 1.444; quasi z -5.63
7 pitfalls: training ranks d = 15 over d = 5; d* 5 -> 7 as n grows; pure-noise E[R2] 0.0916; OR 1.733 at p = 0.5 gives 0.634; ML 0.3125 vs Bayes 0.25 at pi1 = 0.25
ALL L02 CHECKS PASSED
```

---

## 9 · What is deliberately absent

| Not here | Why |
|---|---|
| scikit-learn (`cross_val_score`, `LogisticRegression`, `LinearDiscriminantAnalysis`) | not installed; every routine is a few lines of numpy, which also shows the formula |
| the `mcycle`, `default`, spam, iris and admission **data** | not on disk: the checks use printed tables, printed coefficients and, for CV, a labelled stand-in |
| the smoothing spline of Fundamentos | a black box on purpose (note 01 §7); polynomials stand in |
| ridge, lasso, elastic net; every Bayesian fit (logit, Poisson grid, SIR) | Classes 3+4 |
| plotting | `figures/make_figures.py` draws the figures and asserts their plotted numbers |

---

## Links

Map: [[L02-00-map]] · Formulas: [[L02-07-formulas]] · Pitfalls: [[L02-08-pitfalls]] · Class 1 code:
[[../L01/L01-11-python|L01-11]] · Figures: `figures/make_figures.py` · Companion checks:
`companions/check_companions.py` · Rules: [[../../rules/06_classificacao_validacao|rules/06]].
