"""Figures for the Class 2 notes (Notas/L02). Run: python Notas/L02/figures/make_figures.py

build() writes nine PNGs beside this file and asserts at least one plotted number per figure.
Every curve is an exact expression. Data: only numbers printed in the sources, plus a seeded,
labelled STAND-IN for the mcycle data (not on disk) in the cross-validation figures.

Sources: Fundamentos.pdf slides 21-24 (tanh model); Wooldridge pp. 38-39, 171-172 (log forms);
motorcyle-polynomialregression.pdf / .html (CV); logisticregression-discriminantanalysis.pdf
slides 13, 15, 20 (default logit) and 45-47 (Gaussian discriminant example);
Gaussian-vs-Poisson-regression.html (28 visitor counts).
"""
import pathlib
import sys

import numpy as np
from numpy.polynomial import legendre as L

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))
from _figstyle import C, apply, save  # noqa: E402

import matplotlib.pyplot as plt  # noqa: E402
import statsmodels.api as sm  # noqa: E402
from scipy.special import expit  # noqa: E402
from scipy.stats import norm  # noqa: E402

# ---------- L02-01: the tanh model (Fundamentos.pdf slide 21) ----------
SIGMA, N_TRAIN, LO, HI = 4.0, 30, 8.0, 18.0


def psi(x):
    """Regression function of Fundamentos slide 21 (annual income, thousand R$, vs years of schooling)."""
    return 45 * np.tanh(x / 1.9 - 7) + 57


def poly_bias_variance(d, n=N_TRAIN, sigma=SIGMA, grid=np.linspace(LO, HI, 400)):
    """Exact moments of the degree-d OLS polynomial fit of psi on a fixed equispaced design of n points.

    Returns (avg bias^2, avg variance, expected training MSE), averages over a uniform grid on [8, 18].
    Conditional on the design: E f(x0) = b0'(B'B)^-1 B' psi, Var f(x0) = sigma^2 b0'(B'B)^-1 b0;
    E[training MSE] = sigma^2 (1 - (d+1)/n) + ||(I-H) psi||^2 / n.
    """
    x = np.linspace(LO, HI, n)
    B = L.legvander((x - 13) / 5, d)          # Legendre basis on [-1, 1]: same column space as 1, x, ..., x^d
    Q, R = np.linalg.qr(B)
    f = psi(x)
    b0 = L.legvander((grid - 13) / 5, d)
    A = np.linalg.solve(R.T, b0.T)            # R^-T b0 for every grid point, shape (d+1, len(grid))
    mean_fit = A.T @ (Q.T @ f)
    bias2 = np.mean((mean_fit - psi(grid)) ** 2)
    var = sigma ** 2 * np.mean(np.sum(A ** 2, axis=0))
    resid = f - Q @ (Q.T @ f)
    train = sigma ** 2 * (1 - (d + 1) / n) + resid @ resid / n
    return bias2, var, train


def fig_tanh():
    rng = np.random.default_rng(21)           # seeded draw, NOT the slide's sample
    x = np.sort(rng.uniform(LO, HI, N_TRAIN))
    y = psi(x) + rng.normal(0, SIGMA, N_TRAIN)
    g = np.linspace(LO, HI, 400)
    line = np.polyval(np.polyfit(x, y, 1), g)                     # df = 2: the OLS line (slide 23)
    p6 = L.legval((g - 13) / 5, L.legfit((x - 13) / 5, y, 6))     # df = 7: degree-6 polynomial
    interp = np.interp(g, x, y)                                   # df = n = 30: polygonal interpolant

    fig, ax = plt.subplots()
    ax.plot(g, psi(g), color=C["ink"], lw=2.4, label=r"$\psi(x)=45\tanh(x/1.9-7)+57$")
    ax.scatter(x, y, s=18, color=C["good"], zorder=3, label="30 training pairs (seeded draw)")
    ax.plot(g, line, color=C["warn"], lw=1.6, label="df = 2: OLS line")
    ax.plot(g, p6, color=C["main"], lw=1.6, label="df = 7: degree-6 polynomial")
    ax.plot(g, interp, color=C["hi"], lw=1.2, label="df = 30: interpolant")
    ax.axvline(13.3, color=C["ref"], ls=":", lw=1)
    ax.annotate(r"inflection $x=13.3$, $\psi=57$", (13.3, 57), (14.2, 30), color=C["ref"],
                arrowprops=dict(arrowstyle="->", color=C["ref"]))
    ax.set(xlabel="Years of schooling $x$", ylabel="Annual income (thousand R$)", xlim=(LO, HI))
    ax.legend(fontsize=8.5, loc="upper left")
    ax.set_title("The tanh regression function and three learners of increasing flexibility")
    save(fig, "L02-tanh-regression-function")

    assert abs(psi(13.3) - 57) < 1e-12
    assert abs(psi(8.0) - 12.3386) < 1e-4 and abs(psi(18.0) - 101.3653) < 1e-4
    assert np.allclose(np.interp(x, x, y), y)                      # interpolant: training error 0


def fig_bias_variance():
    ds = np.arange(0, 16)
    rows = np.array([poly_bias_variance(d) for d in ds])
    b2, var, train = rows.T
    test = b2 + var + SIGMA ** 2
    dstar = int(ds[np.argmin(test)])

    fig, ax = plt.subplots()
    ax.plot(ds, test, color=C["good"], marker="o", ms=3.5, label="expected test error")
    ax.plot(ds, b2, color=C["main"], marker="o", ms=3.5, label=r"avg bias$^2$")
    ax.plot(ds, var, color=C["warn"], marker="o", ms=3.5, label="avg variance")
    ax.plot(ds, train, color=C["hi"], ls="--", label="expected training MSE")
    ax.axhline(SIGMA ** 2, color=C["ref"], ls=":", label=r"irreducible $\sigma^2=16$")
    ax.axvline(dstar, color=C["good"], lw=1, ls="--")
    ax.set_yscale("symlog", linthresh=1)                            # linear below 1, log above
    ax.set(ylim=(0, 1500), xlabel="Polynomial degree $d$ (df = $d+1$)",
           ylabel="Squared error (thousand R\\$)$^2$")
    ax.legend(fontsize=8.5)
    ax.set_title(f"Exact decomposition, n = 30 equispaced, $\\sigma$ = 4: optimum at d = {dstar}")
    save(fig, "L02-bias-variance-curves")

    assert np.allclose(test, b2 + var + 16)
    assert np.all(np.diff(train) <= 1e-9)                          # training error never rises with d
    # Monte Carlo check of the exact formulas at d = 3 (seeded)
    rng = np.random.default_rng(3)
    x = np.linspace(LO, HI, N_TRAIN)
    g = np.linspace(LO, HI, 400)
    B, B0 = L.legvander((x - 13) / 5, 3), L.legvander((g - 13) / 5, 3)
    P = B0 @ np.linalg.pinv(B)
    fits = (psi(x) + rng.normal(0, SIGMA, (20000, N_TRAIN))) @ P.T
    mc_b2 = np.mean((fits.mean(0) - psi(g)) ** 2)
    mc_var = np.mean(fits.var(0))
    assert abs(mc_b2 / b2[3] - 1) < 0.02 and abs(mc_var / var[3] - 1) < 0.03
    return dict(ds=ds, b2=b2, var=var, test=test, train=train, dstar=dstar)


# ---------- L02-02: log readings (Wooldridge 6e) ----------
def fig_log_readings():
    b = np.linspace(-0.8, 0.8, 400)
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(10.5, 4.0))
    a1.plot(b, 100 * b, color=C["ref"], ls="--", label=r"approximation $100\,\beta\Delta x$")
    a1.plot(b, 100 * np.expm1(b), color=C["main"], label=r"exact $100\,(e^{\beta\Delta x}-1)$")
    pts = [(0.083, "educ, W (2.44)", (6, -12)), (0.306, "rooms +1, W (6.7)", (-118, 6)),
           (-0.306, "rooms -1", (6, -14)), (-0.26, "stratio +5", (-20, 10))]
    for z, lab, off in pts:
        a1.plot([z, z], [100 * z, 100 * np.expm1(z)], color=C["warn"], lw=1.2)
        a1.plot(z, 100 * np.expm1(z), "o", color=C["warn"], ms=4)
        a1.annotate(f"{lab}: {100 * np.expm1(z):.1f}%", (z, 100 * np.expm1(z)), fontsize=7.5,
                    xytext=off, textcoords="offset points")
    a1.set(xlabel=r"$\beta\Delta x$ (change in $\log y$)", ylabel=r"$\%\Delta y$")
    a1.set_title("Log-level: the 100β reading vs the exact change")
    a1.legend(fontsize=8, loc="upper left")

    px = np.linspace(-50, 100, 400)
    beta = 0.257                                                    # W (2.46), CEO salary on sales
    a2.plot(px, beta * px, color=C["ref"], ls="--", label=r"approximation $\beta\,\%\Delta x$")
    a2.plot(px, 100 * ((1 + px / 100) ** beta - 1), color=C["main"],
            label=r"exact $100[(1+\%\Delta x/100)^{\beta}-1]$")
    a2.plot(10, 100 * (1.1 ** beta - 1), "o", color=C["warn"], ms=4)
    a2.annotate(f"sales +10%: {100 * (1.1 ** beta - 1):.2f}% (approx. 2.57%)", (10, 100 * (1.1 ** beta - 1)),
                xytext=(6, -14), textcoords="offset points", fontsize=7.5)
    a2.set(xlabel=r"$\%\Delta$ sales", ylabel=r"$\%\Delta$ salary")
    a2.set_title(r"Log-log: elasticity $\beta=0.257$")
    a2.legend(fontsize=8, loc="upper left")
    save(fig, "L02-log-linear-readings")

    assert round(100 * np.expm1(0.306), 1) == 35.8 and round(100 * np.expm1(-0.306), 1) == -26.4
    assert round(100 * np.expm1(-0.26), 1) == -22.9 and round(100 * np.expm1(-0.052), 1) == -5.1
    assert abs(100 * (1.1 ** 0.257 - 1) - 2.479) < 1e-3


# ---------- L02-03: CV on a reproducible stand-in for mcycle ----------
N_MC, DMAX = 132, 14                                                # site: first 132 rows, orders 1..14 on the slides


def mcycle_standin():
    """STAND-IN, not the MASS data: dip-and-rebound mean with noise that is small before the impact
    and large after (the shape of the site's slide 3). Standardised as the site does."""
    rng = np.random.default_rng(1985)                               # Silverman (1985); just a seed
    x = np.sort(rng.uniform(-1.75, 2.4, N_MC))
    f = 0.5 - 2.5 * np.exp(-0.5 * ((x + 0.3) / 0.28) ** 2) + 0.9 * np.exp(-0.5 * ((x - 0.5) / 0.35) ** 2)
    y = f + rng.normal(0, np.where(x < -0.8, 0.15, 0.45))
    return (x - x.mean()) / x.std(ddof=1), (y - y.mean()) / y.std(ddof=1)


def design(x, d):
    return np.vander(x, d + 1, increasing=True)                     # raw powers, as the site's cbind(x^1..x^d)


def ols_predict(xtr, ytr, xte, d):
    beta = np.linalg.lstsq(design(xtr, d), ytr, rcond=None)[0]
    return design(xte, d) @ beta


def loocv_brute(x, y, d):
    idx = np.arange(len(x))
    return np.mean([(y[i] - ols_predict(x[idx != i], y[idx != i], x[i:i + 1], d)[0]) ** 2 for i in idx])


def loocv_shortcut(x, y, d):
    """ISLP (5.2): CV_(n) = mean(((y_i - yhat_i) / (1 - h_ii))^2), h_ii from the QR of the design."""
    Q, _ = np.linalg.qr(design(x, d))
    h = np.sum(Q ** 2, axis=1)
    e = y - Q @ (Q.T @ y)
    return np.mean((e / (1 - h)) ** 2), h


def kfold_cv(x, y, d, perm, k=10):
    """Site's fold layout: L = trunc(n/k) per fold, the last fold takes the remainder; CV = sum SSE / n."""
    n = len(x)
    Lf = n // k
    left = np.arange(0, n, Lf)[:k]
    right = np.append(left[1:], n)
    sse = 0.0
    for a, b in zip(left, right):
        te = perm[a:b]
        tr = np.setdiff1d(perm, te)
        sse += np.sum((y[te] - ols_predict(x[tr], y[tr], x[te], d)) ** 2)
    return sse / n


def fig_cv():
    x, y = mcycle_standin()
    ds = np.arange(1, DMAX + 1)
    train = np.array([np.mean((y - ols_predict(x, y, x, d)) ** 2) for d in ds])
    loo = np.array([loocv_shortcut(x, y, d)[0] for d in ds])
    rng = np.random.default_rng(56789)                              # the site's seed value, numpy generator
    ntr = int(N_MC * 0.8)                                           # R: sample(1:n, 105.6) draws 105
    hold = np.empty((100, len(ds)))
    for s in range(100):
        p = rng.permutation(N_MC)
        tr, te = p[:ntr], p[ntr:]
        hold[s] = [np.mean((y[te] - ols_predict(x[tr], y[tr], x[te], d)) ** 2) for d in ds]
    kf = np.empty((100, len(ds)))
    for s in range(100):
        p = rng.permutation(N_MC)
        kf[s] = [kfold_cv(x, y, d, p) for d in ds]
    pick_hold = np.bincount(ds[np.argmin(hold, axis=1)], minlength=DMAX + 1)[1:]
    pick_kf = np.bincount(ds[np.argmin(kf, axis=1)], minlength=DMAX + 1)[1:]
    dstar = int(ds[np.argmin(kf.mean(0))])

    # pairs bootstrap of the chosen order (ISLP section 5.2) vs the formula band (ISLP eq. 7.2)
    g = np.linspace(x.min(), x.max(), 300)
    B = 1000
    rb = np.random.default_rng(31415)
    boot = np.empty((B, len(g)))
    for b in range(B):
        i = rb.integers(0, N_MC, N_MC)
        boot[b] = ols_predict(x[i], y[i], g, dstar)
    lo_b, hi_b = np.percentile(boot, [2.5, 97.5], axis=0)
    X = design(x, dstar)
    beta, rss = np.linalg.lstsq(X, y, rcond=None)[:2]
    s2 = rss[0] / (N_MC - dstar - 1)
    Cov = s2 * np.linalg.inv(X.T @ X)
    G = design(g, dstar)
    fit = G @ beta
    se = np.sqrt(np.einsum("ij,jk,ik->i", G, Cov, G))

    fig, (a1, a2, a3) = plt.subplots(1, 3, figsize=(13.5, 4.0))
    a1.plot(ds, train, color=C["hi"], ls="--", marker="o", ms=3, label="training MSE")
    a1.plot(ds, hold.mean(0), color=C["ref"], marker="o", ms=3, label="80/20 hold-out, mean of 100")
    a1.plot(ds, loo, color=C["main"], marker="o", ms=3, label="LOOCV (shortcut 5.2)")
    a1.plot(ds, kf.mean(0), color=C["good"], marker="o", ms=3, label="10-fold, mean of 100")
    a1.axvline(dstar, color=C["good"], ls=":", lw=1)
    a1.set(xlabel="Order of polynomial $d$", ylabel="MSE (standardised units)", xticks=ds)
    a1.legend(fontsize=7.5)
    a1.set_title("Estimated test error vs order")
    w = 0.4
    a2.bar(ds - w / 2, pick_hold, w, color=C["ref"], label="80/20 hold-out")
    a2.bar(ds + w / 2, pick_kf, w, color=C["good"], label="10-fold")
    a2.set(xlabel="Order chosen", ylabel="Times chosen (of 100)", xticks=ds)
    a2.legend(fontsize=7.5)
    a2.set_title("Which order wins, over 100 random splits")
    a3.scatter(x, y, s=8, color=C["ref"], alpha=0.7)
    a3.fill_between(g, lo_b, hi_b, color=C["main"], alpha=0.25, label="pairs bootstrap 95% (B = 1000)")
    a3.plot(g, fit - 2 * se, color=C["warn"], ls="--", lw=1, label=r"$\pm 2$ SE formula (7.2)")
    a3.plot(g, fit + 2 * se, color=C["warn"], ls="--", lw=1)
    a3.plot(g, fit, color=C["main"], lw=1.8, label=f"order {dstar} fit")
    a3.set(xlabel="Time after impact (standardised)", ylabel="Acceleration (standardised)", ylim=(-3.5, 3))
    a3.legend(fontsize=7.5, loc="lower right")
    a3.set_title("Bootstrap band of the chosen order")
    fig.suptitle("Reproducible stand-in for mcycle (simulated, n = 132): NOT the site's data", fontsize=10,
                 color=C["warn"], y=1.02)
    save(fig, "L02-cv-curves")

    assert np.all(np.diff(train) <= 1e-12)                          # nested OLS: training MSE never rises
    assert pick_hold.sum() == 100 and pick_kf.sum() == 100
    assert pick_kf.max() >= pick_hold.max()                         # k-fold choice is the more stable one
    noisy = g > -0.5
    assert np.mean(hi_b[noisy] - lo_b[noisy]) > np.mean(4 * se[noisy])  # heteroskedastic region: bootstrap wider
    return dict(x=x, y=y, ds=ds, train=train, loo=loo, hold=hold.mean(0), kf=kf.mean(0),
                pick_hold=pick_hold, pick_kf=pick_kf, dstar=dstar)


def fig_loocv_shortcut(cv):
    x, y, ds = cv["x"], cv["y"], cv["ds"]
    brute = np.array([loocv_brute(x, y, d) for d in ds])
    short = cv["loo"]
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(10.5, 4.0))
    for d, col in [(3, C["main"]), (12, C["warn"])]:
        h = loocv_shortcut(x, y, d)[1]
        a1.plot(x, h, color=col, marker="o", ms=2.5, lw=0.8, label=f"d = {d}: mean $h_{{ii}}$ = {h.mean():.4f}")
        a1.axhline((d + 1) / len(x), color=col, ls=":", lw=1)
    a1.set(xlabel="$x_i$ (standardised)", ylabel="leverage $h_{ii}$", yscale="log")
    a1.legend(fontsize=8)
    a1.set_title(r"Leverages: mean $=(d+1)/n$, largest at the edges")
    a2.plot(brute, short, "o", color=C["main"])
    lim = [min(brute.min(), short.min()) * 0.95, max(brute.max(), short.max()) * 1.05]
    a2.plot(lim, lim, color=C["ref"], ls="--", lw=1)
    for d, b_, s_ in zip(ds, brute, short):
        if d in (1, 3, 5, 6, 7, 8, 12):
            a2.annotate(f"d = {d}", (b_, s_), xytext=(5, -10), textcoords="offset points", fontsize=7)
    a2.set(xlabel="LOOCV by n = 132 refits", ylabel="LOOCV by the shortcut (5.2)", xlim=lim, ylim=lim)
    a2.set_title("One fit gives the same number as n refits")
    fig.suptitle("Stand-in data (simulated), orders 1-14", fontsize=10, color=C["warn"], y=1.02)
    save(fig, "L02-loocv-shortcut")

    assert np.allclose(brute, short, rtol=1e-8)
    for d in (3, 12):
        assert abs(loocv_shortcut(x, y, d)[1].sum() - (d + 1)) < 1e-9   # trace(H) = d + 1
    return brute


# --- printed coefficients -------------------------------------------------------------
B0, B1 = -10.6513, 0.0055                  # slide 15 (balance only)
LM0, LM1 = -7.519e-2, 1.299e-4             # slide 13 (OLS on the 0/1 response)
C0, C1, C2 = -10.75, 5.738e-3, -0.7149     # slide 20 (balance + student)
M1, M2, S1, S2 = 1.0, 5.0, 6.0, 2.5        # slides 45-46
Y = np.array([95, 81, 85, 100, 111, 130, 113, 92, 65, 78, 96, 118, 120, 104, 91, 91, 79,
              106, 91, 114, 110, 98, 61, 84, 96, 126, 119, 90])  # html page, June 2018


def h_roots(k, m1=M1, m2=M2, s1=S1, s2=S2):
    """Roots of h(x) = k for two univariate Gaussians, h = log N(x;m1,s1) - log N(x;m2,s2).

    Returns the sorted pair, or None when h(x) > k everywhere (class-2 region empty).
    Requires s1 != s2 (the quadratic case).
    """
    a = -0.5 * (1 / s1**2 - 1 / s2**2)
    b = m1 / s1**2 - m2 / s2**2
    c = -0.5 * (m1**2 / s1**2 - m2**2 / s2**2) + np.log(s2 / s1) - k
    d = b * b - 4 * a * c
    if d < 0:
        return None
    return np.sort([(-b - np.sqrt(d)) / (2 * a), (-b + np.sqrt(d)) / (2 * a)])


def fig_logistic_default():
    x = np.linspace(0, 2700, 600)
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(10.5, 4.2))
    a1.plot(x, expit(B0 + B1 * x), color=C["main"], label=r"logit: $\Lambda(-10.6513+0.0055x)$")
    a1.plot(x, LM0 + LM1 * x, color=C["warn"], label=r"LM: $-0.0752+0.00013x$")
    a1.axhline(0, color=C["ref"], lw=0.8)
    a1.axhline(0.5, color=C["ref"], lw=0.8, ls="--")
    xs = -B0 / B1
    a1.axvline(xs, color=C["hi"], lw=1, ls=":")
    for xb in (1000, 2000):
        pb = expit(B0 + B1 * xb)
        a1.plot(xb, pb, "o", color=C["main"])
        a1.annotate(f"{100 * pb:.2f}%" if pb < 0.1 else f"{100 * pb:.1f}%", (xb, pb),
                    textcoords="offset points", xytext=(-38, 8))
    a1.annotate(f"50% cut-off\n{xs:.1f}", (xs, 0.5), textcoords="offset points", xytext=(-75, 25),
                color=C["hi"])
    a1.set(xlabel="balance (US$)", ylabel="P(default = yes | balance)", ylim=(-0.12, 1.02),
           title="Balance only: logit vs linear probability")
    a1.legend(loc="upper left", fontsize=9)

    x2 = np.linspace(1000, 2700, 500)
    for s, col, lab in ((0, C["warn"], "non-student"), (1, C["main"], "student")):
        a2.plot(x2, expit(C0 + C1 * x2 + C2 * s), color=col, label=lab)
        cut = -(C0 + C2 * s) / C1
        a2.axvline(cut, color=col, lw=1, ls=":")
        a2.annotate(f"{cut:.0f}", (cut, 0.03), textcoords="offset points",
                    xytext=(3 if s else -30, 0), color=col)
        p15 = expit(C0 + C1 * 1500 + C2 * s)
        a2.plot(1500, p15, "o", color=col)
        a2.annotate(f"{100 * p15:.1f}%", (1500, p15), textcoords="offset points", xytext=(-42, 4), color=col)
    a2.axhline(0.5, color=C["ref"], lw=0.8, ls="--")
    a2.set(xlabel="balance (US$)", ylabel="P(default = yes | balance, student)",
           title="Balance + student: same slope, shifted curve")
    a2.legend(loc="upper left", fontsize=9)
    save(fig, "L02-logistic-default")

    assert round(100 * expit(B0 + B1 * 1000), 2) == 0.58          # slide 15
    assert round(100 * expit(B0 + B1 * 2000), 1) == 58.6          # slide 15
    assert abs(xs - 1936.6) < 0.05                                # slide 17 (1936)
    assert round(100 * expit(C0 + C1 * 1500 + C2), 1) == 5.4      # slide 20
    assert round(100 * expit(C0 + C1 * 1500), 1) == 10.5          # slide 20
    assert round(-(C0 + C2) / C1) == 1998 and round(-C0 / C1) == 1873   # slide 22 (labels swapped there)
    assert abs(-LM0 / LM1 - 578.8) < 0.1                          # LM goes negative below 578.8


def fig_gaussian_regions():
    x = np.linspace(-20, 20, 2001)
    r = h_roots(0.0)
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(10.5, 4.2))
    a1.plot(x, 0.5 * norm.pdf(x, M1, S1), color=C["main"], label=r"$\pi_1p_1(x)$: N(1, $6^2$)")
    a1.plot(x, 0.5 * norm.pdf(x, M2, S2), color=C["warn"], label=r"$\pi_2p_2(x)$: N(5, $2.5^2$)")
    a1.axvspan(r[0], r[1], color=C["warn"], alpha=0.12, label="allocate to class 2")
    for v in r:
        a1.axvline(v, color=C["hi"], lw=1, ls=":")
        a1.annotate(f"{v:.3f}", (v, 0.072), textcoords="offset points", xytext=(3, 0), color=C["hi"])
    a1.set(xlabel="x", ylabel="prior × density", ylim=(0, 0.085),
           title=r"$\pi_1=\pi_2=1/2$: class 1 wins both tails")
    a1.legend(loc="upper left", fontsize=8.5)

    h_un = norm.logpdf(x, M1, S1) - norm.logpdf(x, M2, S2)
    h_eq = norm.logpdf(x, M1, 6) - norm.logpdf(x, M2, 6)
    a2.plot(x, h_un, color=C["main"], label=r"$\sigma_1=6,\ \sigma_2=2.5$ (quadratic)")
    a2.plot(x, h_eq, color=C["good"], label=r"$\sigma_1=\sigma_2=6$ (linear, root 3)")
    a2.axhline(0, color=C["ref"], lw=0.9, label=r"ML / equal-prior threshold 0")
    a2.axhline(np.log(1 / 2), color=C["hi"], lw=1, ls="--", label=r"cost ratio $c_{21}/c_{12}=2$: $\log\frac{1}{2}$")
    a2.set(xlabel="x", ylabel=r"$h(x)=\log p_1(x)-\log p_2(x)$", ylim=(-3, 12),
           title="Discriminant function and thresholds")
    a2.legend(loc="upper center", fontsize=8.5)
    save(fig, "L02-gaussian-discriminant-regions")

    assert abs(r[0] - 1.680) < 5e-4 and abs(r[1] - 10.001) < 5e-4     # roots of slide 45's quadratic
    assert abs(h_un[0] - 43.0) < 0.01 and abs(h_un[-1] - 12.11) < 0.01  # slide 46 right panel ends
    assert abs(h_eq[0] - 23 / 9) < 1e-9                                  # slide 47: h(-20) = 2.556
    rc = h_roots(np.log(1 / 2))
    assert abs(rc[0] - 3.228) < 5e-4 and abs(rc[1] - 8.453) < 5e-4
    assert h_roots(np.log(1 / 5)) is None                               # R2 empty once c21/c12 > 3.14


def fig_roc():
    ks = np.linspace(-60, 60, 24001)
    tpr, fpr = [], []
    for k in ks:                       # allocate to class 2 iff h(x) < k (class 2 = "positive")
        r = h_roots(k)
        if r is None:
            tpr.append(0.0), fpr.append(0.0)
            continue
        tpr.append(norm.cdf(r[1], M2, S2) - norm.cdf(r[0], M2, S2))
        fpr.append(norm.cdf(r[1], M1, S1) - norm.cdf(r[0], M1, S1))
    tpr, fpr = np.array(tpr), np.array(fpr)
    o = np.argsort(fpr)
    auc_un = np.trapezoid(tpr[o], fpr[o])
    t = np.linspace(-40, 40, 4001)     # equal variances: allocate to 2 iff x > t
    tpr_eq, fpr_eq = norm.sf(t, M2, 6), norm.sf(t, M1, 6)
    auc_eq = norm.cdf((M2 - M1) / (6 * np.sqrt(2)))

    r0 = h_roots(0.0)
    p21 = norm.cdf(r0[1], M1, S1) - norm.cdf(r0[0], M1, S1)
    p12 = 1 - (norm.cdf(r0[1], M2, S2) - norm.cdf(r0[0], M2, S2))
    fig, ax = plt.subplots(figsize=(5.4, 5.0))
    ax.plot(fpr[o], tpr[o], color=C["main"], label=fr"$\sigma_1=6,\sigma_2=2.5$: AUC {auc_un:.3f}")
    ax.plot(fpr_eq, tpr_eq, color=C["good"], label=fr"$\sigma_1=\sigma_2=6$: AUC {auc_eq:.3f}")
    ax.plot([0, 1], [0, 1], color=C["ref"], lw=0.9, ls="--", label="no information")
    ax.plot(p21, 1 - p12, "o", color=C["main"])
    ax.annotate(f"ML rule ({p21:.3f}, {1 - p12:.3f})", (p21, 1 - p12), textcoords="offset points",
                xytext=(8, -14), color=C["main"])
    pe = norm.sf(3, M1, 6)
    ax.plot(pe, 1 - pe, "o", color=C["good"])
    ax.annotate(f"ML rule ({pe:.3f}, {1 - pe:.3f})", (pe, 1 - pe), textcoords="offset points",
                xytext=(8, -14), color=C["good"])
    ax.set(xlabel=r"false positive rate $p_{21}$ = P(alloc. 2 | y = 1)",
           ylabel=r"true positive rate $1-p_{12}$ = P(alloc. 2 | y = 2)",
           xlim=(0, 1), ylim=(0, 1.01), title="Exact ROC curves, deck's Gaussian example")
    ax.legend(loc="lower right", fontsize=8.5)
    save(fig, "L02-roc")

    assert abs(auc_eq - 0.6813) < 1e-4
    assert abs(auc_un - 0.8024) < 1e-3
    assert abs(p21 - 0.3881) < 1e-4 and abs(p12 - 0.1148) < 1e-4
    assert abs(pe - 0.3694) < 1e-4


def fig_gaussian_vs_poisson():
    n = Y.size
    t = np.tile(np.arange(1, 8), 4)
    wk = (t <= 3).astype(float)        # the html codes t = 1..3 (fri, sat, sun) as weekend
    X = sm.add_constant(wk)
    pois = sm.GLM(Y, X, family=sm.families.Poisson()).fit()
    ols = sm.OLS(Y, X).fit()
    lam = pois.fittedvalues
    s = np.sqrt(ols.scale)
    day = np.arange(1, n + 1)

    fig, (a1, a2) = plt.subplots(1, 2, figsize=(10.5, 4.2), gridspec_kw={"width_ratios": [1.6, 1]})
    a1.plot(day[wk == 0], Y[wk == 0], "o", color=C["main"], label="weekday (Mon–Thu)")
    a1.plot(day[wk == 1], Y[wk == 1], "s", color=C["warn"], label="'weekend' (Fri–Sun)")
    a1.step(day, lam, where="mid", color=C["ink"], lw=1.3, label=r"fitted mean (both models): 109 / 83.3")
    a1.fill_between(day, lam - 1.96 * s, lam + 1.96 * s, step="mid", color=C["ref"], alpha=0.18,
                    label=fr"Gaussian $\pm1.96\,s$, $s$={s:.2f}")
    a1.fill_between(day, lam - 1.96 * np.sqrt(lam), lam + 1.96 * np.sqrt(lam), step="mid",
                    color=C["good"], alpha=0.18, label=r"Poisson $\pm1.96\sqrt{\lambda}$")
    a1.set(xlabel="day (1 = Fri 1 June 2018)", ylabel="visitors", title="Blog visitors, 28 days")
    a1.legend(loc="upper center", bbox_to_anchor=(0.5, -0.17), fontsize=8, ncol=3)

    means = np.array([Y[wk == 0].mean(), Y[wk == 1].mean()])
    vars_ = np.array([Y[wk == 0].var(ddof=1), Y[wk == 1].var(ddof=1)])
    phi = pois.pearson_chi2 / pois.df_resid
    mu = np.linspace(60, 130, 50)
    a2.plot(mu, mu, color=C["good"], label=r"Poisson: Var = $\lambda$")
    a2.plot(mu, phi * mu, color=C["good"], ls="--", label=fr"quasi-Poisson: Var = {phi:.3f}$\lambda$")
    a2.axhline(s**2, color=C["ref"], label=fr"Gaussian: Var = $s^2$ = {s**2:.1f}")
    a2.plot(means, vars_, "D", color=C["hi"], ms=7, label="sample (mean, variance)")
    for m, v in zip(means, vars_):
        a2.annotate(f"({m:.1f}, {v:.1f})", (m, v), textcoords="offset points", xytext=(-20, -18), color=C["hi"])
    a2.set(xlabel="group mean", ylabel="group variance", title="Mean–variance check", ylim=(50, 200))
    a2.legend(loc="upper left", fontsize=8)
    save(fig, "L02-gaussian-vs-poisson-fit")

    assert np.allclose(pois.params, [4.69135, -0.26850], atol=5e-6)   # html glm output
    assert np.allclose(pois.bse, [0.02395, 0.03967], atol=5e-6)
    assert abs(pois.deviance - 38.324) < 5e-4 and abs(pois.aic - 221.76) < 5e-3
    assert np.allclose(ols.params, [109.0, -25.667], atol=5e-4) and abs(s - 11.85) < 5e-3
    assert np.allclose(vars_, [147.733, 130.424], atol=5e-3) and abs(phi - 1.444) < 5e-4


def build():
    """Make and save the nine figures and run their checks."""
    apply()
    # notes 01-03
    fig_tanh()
    fig_bias_variance()
    fig_log_readings()
    cv = fig_cv()
    fig_loocv_shortcut(cv)
    # notes 04-06
    fig_logistic_default()
    fig_gaussian_regions()
    fig_roc()
    fig_gaussian_vs_poisson()


if __name__ == "__main__":
    build()
