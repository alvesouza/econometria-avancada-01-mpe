"""Figures for the Classes 3+4 notes (Notas/L03). Run: python Notas/L03/figures/make_figures.py

build() writes eight PNGs beside this file and asserts at least one plotted number per figure.
Every curve is the model's exact expression (closed form or deterministic quadrature); the
simulated parts (Pareto sample, accept-reject points, running pi, Gibbs and MH chains) are seeded
and say so in their titles. The same formulas are asserted against the decks' numbers in
Notas/L03/L03_python_checks.py (cited, not imported: importing it would rerun every sampler).

Sources: aprendizagembayesiana-bayesianingredients.pdf (slides 26-56); question0.pdf;
sequential-bayes-bernoulli-uniform-trials.html; fisicos-ABCD.html; notas-bayesianas-slides.pdf;
hierarchical-beta-binomial.html; sparse-priors.pdf; Greenberg 1e Fig. 2.2 (p. 18), Table 3.2
(p. 38), Algorithm 5.3 (p. 67), (7.3)-(7.4) (pp. 93-94), p. 94 (bivariate normal Gibbs).
Coal data: .agent/notes/coal-mining-data.md via Notas/L01/companions/check_companions.py.
"""
import pathlib
import sys

import numpy as np
from scipy import integrate, stats
from scipy.special import betaln, gammaln, logsumexp

HERE = pathlib.Path(__file__).resolve()
sys.path.insert(0, str(HERE.parents[2]))
sys.path.insert(0, str(HERE.parents[2] / "L01" / "companions"))
from _figstyle import C, apply, save  # noqa: E402
import check_companions as cc  # noqa: E402  coal series (verified note) and years

import matplotlib.pyplot as plt  # noqa: E402


# ------------------------------------------------------------------ 1 sequential learning
def fig_sequential_learning():
    """(a) three coins vs heads in a row; (b) Greenberg Fig. 2.2; (c) Pareto-Uniform quantiles vs n."""
    fig, (a1, a2, a3) = plt.subplots(1, 3, figsize=(14.0, 3.9))
    p_head, ns = np.array([0.5, 0.9, 1.0]), np.arange(0, 11)
    post = np.array([p_head**n / (p_head**n).sum() for n in ns])          # uniform prior cancels
    for j, (col, lab) in enumerate(zip((C["warn"], C["main"], C["good"]), ("coin 1: P(H)=0.5", "coin 2: P(H)=0.9",
                                                                           "coin 3: P(H)=1"))):
        a1.plot(ns, post[:, j], "o-", color=col, ms=4, label=lab)
    for j in range(3):
        a1.annotate(f"{post[3, j]:.4f}", (3, post[3, j]), xytext=(6, -3 if j else 4), textcoords="offset points",
                    fontsize=8.5, color=C["ink"])
    a1.axvline(3, color=C["ref"], ls=":", lw=1)
    a1.set(title="Three coins: P(coin | n heads)", xlabel="heads in a row, n", ylabel="posterior probability",
           ylim=(-0.02, 1.02))
    a1.legend(fontsize=8.5, loc="center right")

    th = np.linspace(0.0005, 0.9995, 2000)
    a2.plot(th, stats.beta.pdf(th, 2, 2), color=C["ref"], label="prior Beta(2,2)")
    for (n, s, col, ls) in ((10, 3, C["main"], "-"), (50, 15, C["good"], "-")):
        a2.plot(th, stats.beta.pdf(th, s + 1, n - s + 1), color=col, ls=":", lw=1.6)
        a2.plot(th, stats.beta.pdf(th, 2 + s, 2 + n - s), color=col, ls=ls,
                label=f"posterior n={n}, s={s}: mean {(2 + s) / (4 + n):.3f}")
    a2.set(title="Beta-Bernoulli, G Fig. 2.2 (dotted: likelihood)", xlabel=r"$\theta$", ylabel="density")
    a2.legend(fontsize=8.2, loc="upper right")

    rng = np.random.default_rng(165431)                                    # seeded U(0, 2) sample, n = 50
    x = rng.uniform(0, 2, 50)
    n_ax = np.arange(5, 51)
    t1 = np.maximum(1.5, np.maximum.accumulate(x))[4:]
    al1 = 0.1 + n_ax
    qs = np.array([stats.pareto.ppf([0.1, 0.5, 0.9], a, scale=t) for a, t in zip(al1, t1)])
    a3.fill_between(n_ax, qs[:, 0], qs[:, 2], color=C["main"], alpha=0.18, lw=0, label="posterior 10-90%")
    a3.plot(n_ax, qs[:, 1], color=C["main"], label="posterior median")
    a3.plot(n_ax, al1 * t1 / (al1 - 1), color=C["hi"], ls="--", lw=1.4, label="posterior mean")
    a3.plot(n_ax, np.maximum.accumulate(x)[4:], color=C["warn"], lw=1.3, label=r"MLE $x_{(n)}$")
    a3.axhline(2, color=C["good"], lw=1.2, label=r"true $\theta=2$")
    a3.set(title="Pareto-Uniform (seeded sample)", xlabel="sample size n", ylabel=r"$\theta$")
    a3.legend(fontsize=8.0, loc="upper right")
    save(fig, "L03-sequential-learning")
    assert np.allclose(post[3], [0.0674, 0.3932, 0.5394], atol=5e-5)      # question0.pdf
    assert abs((2 + 3) / 14 - 0.357) < 5e-4 and abs(17 / 54 - 0.315) < 5e-4
    assert np.all(qs[:, 1] >= t1) and np.allclose(qs[:, 1], t1 * 2 ** (1 / al1))


# ------------------------------------------------------------------ 2 normal model, four priors
SIG, X0 = 40.0, 850.0
TH = np.linspace(400, 1300, 90001)


def t_prior(th, mu=900.0, s2=240.0, nu=5):
    return stats.t.pdf((th - mu) / np.sqrt(s2), nu) / np.sqrt(s2)


PRIORS = {"A: N(900, 20²)": lambda t: stats.norm.pdf(t, 900, 20), "B: N(800, 80²)": lambda t: stats.norm.pdf(t, 800, 80),
          "C: t₅(900, 240)": t_prior,
          "D: (A+B+C)/3": lambda t: (stats.norm.pdf(t, 900, 20) + stats.norm.pdf(t, 800, 80) + t_prior(t)) / 3}


def post_density(prior, x=X0, lo=600.0, hi=1000.0):
    keep = (TH >= lo) & (TH <= hi)
    th = TH[keep]
    d = prior(th) * stats.norm.pdf(x, th, SIG)
    return th, d / integrate.trapezoid(d, th)


def fig_normal_four_priors():
    fig, (a1, a2, a3) = plt.subplots(1, 3, figsize=(13.4, 3.9))
    cols = [C["main"], C["warn"], C["good"], C["hi"]]
    th = np.linspace(500, 1100, 3000)
    a1.plot(th, stats.norm.pdf(th, X0, SIG), color=C["ink"], lw=1.4, ls="--", label="likelihood, x = 850")
    for (lab, pr), col in zip(PRIORS.items(), cols):
        a1.plot(th, pr(th), color=col, label=lab)
    a1.set(title="Priors and likelihood (fisicos-ABCD)", xlabel=r"$\theta$", ylabel="density", ylim=(0, 0.026))
    a1.legend(fontsize=7.8, loc="upper left")
    means = {}
    for (lab, pr), col in zip(PRIORS.items(), cols):
        tt, d = post_density(pr)
        means[lab[0]] = integrate.trapezoid(tt * d, tt)
        a2.plot(tt, d, color=col, label=f"posterior {lab[0]}: mean {means[lab[0]]:.1f}")
    a2.axvline(X0, color=C["ink"], ls=":", lw=1)
    a2.set(title="Posteriors on [600, 1000] (quadrature)", xlabel=r"$\theta$", xlim=(680, 960), ylabel="density")
    a2.legend(fontsize=7.8, loc="upper left")
    xs = np.linspace(700, 1150, 91)
    mA = (SIG**2 * 900 + 20**2 * xs) / (SIG**2 + 20**2)
    mC = [integrate.trapezoid(TH * t_prior(TH) * stats.norm.pdf(x, TH, SIG), TH)
          / integrate.trapezoid(t_prior(TH) * stats.norm.pdf(x, TH, SIG), TH) for x in xs]
    a3.plot(xs, xs, color=C["ref"], ls=":", lw=1, label="45° line (data only)")
    a3.plot(xs, mA, color=C["main"], label="prior A (normal): slope 0.2")
    a3.plot(xs, mC, color=C["good"], label="prior C (Student-t), same variance")
    a3.axvline(X0, color=C["ink"], ls=":", lw=0.8)
    a3.axvline(900, color=C["ref"], ls="--", lw=0.8)
    a3.set(title="Posterior mean vs the observation", xlabel="observed x", ylabel=r"$E(\theta\mid x)$")
    a3.legend(fontsize=7.8, loc="upper left")
    save(fig, "L03-normal-four-priors")
    assert abs(means["A"] - 890) < 0.05 and abs(means["B"] - 840) < 0.05          # slide 40
    assert abs(means["C"] - 891.16) < 0.3 and abs(means["D"] - 876.15) < 0.3       # fisicos-ABCD SIR table
    assert mC[-1] - mA[-1] > 100                                                   # bounded influence of the t prior


# ------------------------------------------------------------------ 3 loss functions
def fig_loss_functions():
    post = stats.beta(2, 10)                                     # uniform prior, n = 10, s = 1
    mean, med, mode = post.mean(), post.median(), 0.1
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(10.6, 3.9))
    t = np.linspace(0, 0.7, 3000)
    a1.plot(t, post.pdf(t), color=C["main"], label="posterior Beta(2, 10)")
    for v, col, lab in ((mode, C["warn"], "mode 0.100 = MLE (0-1 loss)"), (med, C["hi"], f"median {med:.3f} (absolute)"),
                        (mean, C["good"], f"mean {mean:.3f} (quadratic)")):
        a1.axvline(v, color=col, lw=1.6, label=lab)
    a1.set(title="Uniform prior, s = 1 success in n = 10", xlabel=r"$\theta$", ylabel="density")
    a1.legend(fontsize=8.2, loc="upper right")
    a = np.linspace(0.0, 0.45, 901)
    tq = np.linspace(0, 1, 20001)
    fq = post.pdf(tq)
    curves = {"quadratic $(\\theta-a)^2$": [integrate.trapezoid((x - tq) ** 2 * fq, tq) for x in a],
              "absolute $|\\theta-a|$": [integrate.trapezoid(np.abs(x - tq) * fq, tq) for x in a],
              "0-1, $\\varepsilon=0.01$": [1 - (post.cdf(x + 0.01) - post.cdf(x - 0.01)) for x in a]}
    mins = {}
    for (lab, cv), col in zip(curves.items(), (C["good"], C["hi"], C["warn"])):
        cv = np.array(cv)
        r = (cv - cv.min()) / (cv.max() - cv.min())
        a2.plot(a, r, color=col, label=lab)
        mins[lab] = a[np.argmin(cv)]
        a2.plot(mins[lab], 0, "o", color=col)
    a2.set(title="Posterior expected loss (each rescaled to [0, 1])", xlabel="estimate a", ylabel="rescaled E[L(θ, a) | x]")
    a2.legend(fontsize=8.2, loc="upper center")
    save(fig, "L03-loss-functions")
    m = list(mins.values())
    assert abs(m[0] - 1 / 6) < 1e-3 and abs(m[1] - med) < 1e-3 and abs(m[2] - 0.1) < 2e-3 and abs(med - 0.148) < 5e-4


# ------------------------------------------------------------------ 4 Bayes factors
def log10_bf(m, s1, s2, alpha=1.0):
    """log10 B12, M1: theta1 = theta2 vs M2: theta1 != theta2, Beta(alpha, alpha) priors (G pp. 37-38)."""
    lm1 = betaln(alpha + s1 + s2, alpha + 2 * m - s1 - s2) - betaln(alpha, alpha)
    lm2 = betaln(alpha + s1, alpha + m - s1) + betaln(alpha + s2, alpha + m - s2) - 2 * betaln(alpha, alpha)
    return (lm1 - lm2) / np.log(10)


def fig_bayes_factor():
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(11.0, 3.9))
    p = np.linspace(0.0, 1.0, 801)
    table = {10: (-2.506, -1.200, -0.348, 0.138, 0.297), 100: (-30.775, -15.793, -6.316, -0.975, 0.756)}
    for m, col in ((10, C["main"]), (100, C["warn"])):
        a1.plot(p, log10_bf(m, p * m, (1 - p) * m), color=col, label=f"m = {m} tosses each")
        pts = np.array([0.1, 0.2, 0.3, 0.4, 0.5])
        a1.plot(pts, table[m], "o", color=col, ms=5)
    for y0 in (0.5, 1, 1.5, 2):
        a1.axhline(y0, color=C["ref"], lw=0.6, ls=":")
        a1.axhline(-y0, color=C["ref"], lw=0.6, ls=":")
    a1.axhline(0, color=C["ink"], lw=0.8)
    a1.set(title="Table 3.2: Lila's share = 1 − Michaela's", xlabel="Michaela's proportion of heads",
           ylabel=r"$\log_{10}B_{12}$ (M1: same coin behaviour)", ylim=(-33, 3))
    a1.legend(fontsize=8.5, loc="lower center")
    ms = np.unique(np.round(np.logspace(0.5, 4, 60) / 2) * 2).astype(int)
    exact = log10_bf(ms, ms / 2, ms / 2)
    bic = 0.5 * np.log10(2 * ms)
    a2.semilogx(ms, exact, color=C["main"], label="exact, equal proportions 0.5 / 0.5")
    a2.semilogx(ms, bic, color=C["warn"], ls="--", label=r"BIC-type: $\frac{1}{2}\log_{10}(2m)$")
    a2.semilogx(100, 0.756, "o", color=C["main"])
    a2.set(title="Equal proportions: B12 grows with m", xlabel="tosses each, m (log scale)",
           ylabel=r"$\log_{10}B_{12}$")
    a2.legend(fontsize=8.5, loc="upper left")
    save(fig, "L03-bayes-factor-sample-size")
    for m, row in table.items():
        got = [log10_bf(m, round(q * m), round((1 - q) * m)) for q in (0.1, 0.2, 0.3, 0.4, 0.5)]
        assert np.allclose(got, row, atol=5e-4), (m, got)
    assert np.all(np.diff(exact) > 0) and np.all(bic - exact > 0) and abs((bic - exact)[-1] - 0.5 * np.log10(2 * np.pi)) < 0.002


# ------------------------------------------------------------------ 5 Monte Carlo
def fig_monte_carlo():
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(11.0, 3.9))
    c = stats.beta.pdf(0.5, 3, 3)
    rng = np.random.default_rng(2026)
    u1, u2 = rng.uniform(size=(2, 600))
    acc = u2 * c <= stats.beta.pdf(u1, 3, 3)
    t = np.linspace(0, 1, 500)
    a1.fill_between(t, stats.beta.pdf(t, 3, 3), c, color=C["warn"], alpha=0.08, lw=0)
    a1.plot(t, np.full_like(t, c), color=C["ref"], label=r"$c\,g(y)=1.875$ (U(0,1) proposal)")
    a1.plot(t, stats.beta.pdf(t, 3, 3), color=C["main"], label="target Beta(3,3)")
    a1.scatter(u1[acc], u2[acc] * c, s=7, color=C["good"], label=f"accepted ({acc.mean():.3f})")
    a1.scatter(u1[~acc], u2[~acc] * c, s=7, color=C["warn"], alpha=0.6, label="rejected")
    a1.set(title="Accept-reject, 600 seeded proposals; 1/c = 0.5333", xlabel="y", ylabel="height u·c·g(y)", ylim=(0, 2.25))
    a1.legend(fontsize=7.8, loc="upper right", ncol=2)
    M = np.arange(1, 10001)
    se = 4 * np.sqrt(np.pi / 4 * (1 - np.pi / 4) / M)
    a2.fill_between(M / 1000, np.pi - 2 * se, np.pi + 2 * se, color=C["main"], alpha=0.15, lw=0,
                    label=r"$\pi\pm2\cdot4\sqrt{p(1-p)/M}$, $p=\pi/4$")
    for k in range(6):
        hits = (rng.uniform(size=(10000, 2)) ** 2).sum(1) < 1
        a2.plot(M / 1000, 4 * np.cumsum(hits) / M, lw=0.9, color=[C["ref"], C["hi"], C["good"], C["warn"], C["ink"], C["main"]][k])
    a2.axhline(np.pi, color=C["ink"], lw=1)
    a2.set(title="Hit-or-miss π: six seeded running estimates", xlabel="thousands of draws, M", ylabel="π estimate",
           ylim=(2.7, 3.3))
    a2.legend(fontsize=8.2, loc="upper right")
    save(fig, "L03-monte-carlo-accept-reject")
    assert abs(c - 1.875) < 1e-12 and abs(1 / c - 0.5333) < 5e-5 and abs(se[999] - 0.0519) < 5e-5


# ------------------------------------------------------------------ 6 Gibbs switch point
def fig_gibbs_switch_point():
    Y, YEARS = cc.Y, cc.YEARS
    N, S, a0, b0 = len(Y), np.cumsum(Y), 1.0, 0.5            # L01-04 prior: lambda_j ~ G(1, 1/2)
    k = np.arange(1, N + 1)
    lpk = gammaln(a0 + S) - (a0 + S) * np.log(b0 + k) + gammaln(a0 + S[-1] - S) - (a0 + S[-1] - S) * np.log(b0 + N - k)
    pk = np.exp(lpk - logsumexp(lpk))
    rng = np.random.default_rng(31415)
    kk, draws = N // 2, []
    for g in range(11000):
        l1 = rng.gamma(a0 + S[kk - 1], 1 / (b0 + kk))
        l2 = rng.gamma(a0 + S[-1] - S[kk - 1], 1 / (b0 + N - kk))
        lp = k * (l2 - l1) + S * np.log(l1 / l2)
        kk = rng.choice(k, p=np.exp(lp - logsumexp(lp)))
        if g >= 1000:
            draws.append((l1, l2, kk))
    draws = np.array(draws)
    freq = np.bincount(draws[:, 2].astype(int), minlength=N + 1)[1:] / len(draws)
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(11.0, 3.9))
    win = (YEARS >= 1880) & (YEARS <= 1902)
    a1.bar(YEARS[win], pk[win], color=C["main"], alpha=0.75, label="exact p(k | y) (rates integrated out)")
    a1.plot(YEARS[win], freq[win], "o", color=C["warn"], ms=4, label="Gibbs, 10,000 seeded sweeps")
    a1.set(title="Switch year: last year of the high-rate regime", xlabel="year k", ylabel="posterior probability")
    a1.legend(fontsize=8.2, loc="upper right")
    lam = np.linspace(0.4, 4.4, 1200)
    for j, (col, lab) in enumerate(((C["warn"], r"$\lambda_1$ (before)"), (C["good"], r"$\lambda_2$ (after)"))):
        shape = a0 + (S if j == 0 else S[-1] - S)
        rate = b0 + (k if j == 0 else N - k)
        dens = (pk[:, None] * stats.gamma.pdf(lam[None, :], shape[:, None], scale=1 / rate[:, None])).sum(0)
        a2.hist(draws[:, j], bins=60, density=True, color=col, alpha=0.3)
        a2.plot(lam, dens, color=col, label=f"{lab}: exact mixture, mean {(pk * shape / rate).sum():.3f}")
    a2.set(title="Rates: Gibbs histograms vs exact marginals", xlabel="disasters per year", ylabel="density")
    a2.legend(fontsize=8.2, loc="upper right")
    save(fig, "L03-gibbs-switch-point")
    assert YEARS[np.argmax(pk)] == 1891 and 0.5 * np.abs(freq - pk).sum() < 0.04
    assert abs((pk * (a0 + S) / (b0 + k)).sum() - 3.106) < 5e-4


# ------------------------------------------------------------------ 7 MCMC mixing
def fig_mcmc_mixing():
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(11.0, 3.9))
    lags = np.arange(0, 31)
    rng = np.random.default_rng(5)
    for rho, col in ((0.5, C["good"]), (0.9, C["main"]), (0.999, C["warn"])):
        a1.plot(lags, rho ** (2 * lags), color=col, label=fr"$\rho={rho}$: $\rho^{{2h}}$, IF {(1 + rho**2) / (1 - rho**2):.1f}")
        x2, sd, ch = -2.0, np.sqrt(1 - rho**2), np.empty(50000)
        for g in range(50000):
            x1 = rng.normal(rho * x2, sd)
            x2 = rng.normal(rho * x1, sd)
            ch[g] = x1
        ch -= ch.mean()
        ac = [1.0] + [np.dot(ch[:-h], ch[h:]) / np.dot(ch, ch) for h in lags[1:]]
        a1.plot(lags[::3], np.array(ac)[::3], "o", color=col, ms=3.5)
    a1.axhline(0.05, color=C["ref"], ls=":", lw=1)
    a1.set(title="Gibbs on N₂(0, ρ): ACF of x₁ (dots: seeded chains)", xlabel="lag h", ylabel="autocorrelation",
           ylim=(-0.05, 1.05))
    a1.legend(fontsize=8.0, loc="center right")
    s = np.logspace(-1.3, 1.6, 300)
    acc = 2 / np.pi * np.arctan(2 / s)
    a2.semilogx(s, acc, color=C["main"], label=r"acceptance $\frac{2}{\pi}\arctan(2/s)$")
    sims = []
    for s_ in (0.1, 0.3, 1.0, 2.38, 6.0, 20.0):
        x, nacc = 0.0, 0
        for g in range(20000):
            y = x + s_ * rng.normal()
            if np.log(rng.uniform()) <= (x**2 - y**2) / 2:
                x, nacc = y, nacc + 1
        sims.append(nacc / 20000)
    a2.semilogx([0.1, 0.3, 1.0, 2.38, 6.0, 20.0], sims, "o", color=C["warn"], ms=5, label="seeded RW-MH runs")
    a2.axvline(2.38, color=C["good"], ls="--", lw=1)
    a2.annotate("s = 2.38: 0.445", (2.38, 0.445), xytext=(8, 10), textcoords="offset points", fontsize=8.5, color=C["good"])
    a2.set(title="Random-walk MH on N(0,1): proposal sd s", xlabel="proposal sd s (log scale)", ylabel="acceptance rate")
    a2.legend(fontsize=8.2, loc="upper right")
    save(fig, "L03-mcmc-mixing")
    assert abs(2 / np.pi * np.arctan(2 / 2.38) - 0.4449) < 5e-5 and abs(sims[3] - 0.4449) < 0.015
    assert 0.5**6 < 0.05 < 0.5**4                                   # G p. 103: |ACF| < 0.05 by lag 3 when rho = 0.5


# ------------------------------------------------------------------ 8 shrinkage
def fig_shrinkage():
    YH = np.array([4, 1, 18, 7, 24, 16, 6, 19, 15, 13, 25, 11, 4])
    NH = np.array([129, 35, 228, 84, 291, 270, 46, 293, 241, 105, 353, 250, 41])
    MU = np.linspace(0.0005, 0.25, 600)
    EE = np.exp(np.linspace(np.log(0.5), np.log(1e7), 900))
    MM, E2 = np.meshgrid(MU, EE, indexing="ij")
    a_, b_ = MM * E2, (1 - MM) * E2
    lp = sum(betaln(a_ + y, b_ + n - y) - betaln(a_, b_) for y, n in zip(YH, NH)) + np.log(10) - 2 * np.log(10 + E2) + np.log(E2)
    w = np.exp(lp - lp.max())
    w /= w.sum()
    Ep = np.array([(w * (a_ + y) / (E2 + n)).sum() for y, n in zip(YH, NH)])
    Emu = (w * MM).sum()
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(11.0, 4.1))
    for ph, ep, n in zip(YH / NH, Ep, NH):
        a1.plot([0, 1], [ph, ep], color=C["ref"], lw=0.9)
        a1.plot(0, ph, "o", color=C["warn"], ms=3 + n / 40)
        a1.plot(1, ep, "o", color=C["main"], ms=3 + n / 40)
    a1.axhline(Emu, color=C["good"], ls="--", lw=1, label=f"E(μ | y) = {Emu:.4f}")
    a1.set(xticks=[0, 1], xticklabels=["y/n (separate)", "E(p | y) (hierarchical)"], xlim=(-0.3, 1.3),
           ylabel="death proportion", title="13 Manhattan hospitals: borrowing strength")
    a1.legend(fontsize=8.5, loc="upper center")
    y = np.linspace(0, 8, 161)

    def hs(yv, tau):
        g = lambda kp, p: kp**p * np.exp(-kp * yv**2 / 2) / (1 - kp + tau**2 * kp)
        num = integrate.quad(lambda kp: g(kp, 1), 0, 1, weight="alg", wvar=(0, -0.5))[0]
        return yv * (1 - num / integrate.quad(lambda kp: g(kp, 0), 0, 1, weight="alg", wvar=(0, -0.5))[0])

    def lap(yv, b=1 / np.sqrt(2)):
        f = lambda t, p: t**p * stats.norm.pdf(yv - t) * np.exp(-abs(t) / b)
        return integrate.quad(f, -30, 30, args=(1,), points=[0, yv])[0] / integrate.quad(f, -30, 30, args=(0,), points=[0, yv])[0]

    a2.plot(y, y, color=C["ref"], ls=":", lw=1, label="no shrinkage (MLE)")
    a2.plot(y, y / 2, color=C["warn"], label="normal prior N(0,1) (ridge): y/2")
    a2.plot(y, [lap(v) for v in y], color=C["hi"], label="Laplace prior, variance 1 (lasso)")
    hs1 = np.array([hs(v, 1.0) for v in y])
    hs01 = np.array([hs(v, 0.1) for v in y])
    a2.plot(y, hs1, color=C["main"], label=r"horseshoe, $\tau=1$")
    a2.plot(y, hs01, color=C["good"], label=r"horseshoe, $\tau=0.1$")
    a2.set(title=r"Posterior mean $E(\theta\mid y)$, $y\mid\theta\sim N(\theta,1)$", xlabel="observation y",
           ylabel=r"$E(\theta\mid y)$")
    a2.legend(fontsize=7.9, loc="upper left")
    save(fig, "L03-shrinkage")
    assert np.all(np.abs(Ep - Emu) <= np.abs(YH / NH - Emu) + 1e-12) and abs(Emu - 0.0724) < 0.002
    assert abs(hs1[-1] - 8) < 0.35 and hs01[20] < 0.1 * y[20] and abs(lap(8.0) - (8 - np.sqrt(2))) < 0.05


def build():
    apply()
    fig_sequential_learning()
    fig_normal_four_priors()
    fig_loss_functions()
    fig_bayes_factor()
    fig_monte_carlo()
    fig_gibbs_switch_point()
    fig_mcmc_mixing()
    fig_shrinkage()


if __name__ == "__main__":
    build()
