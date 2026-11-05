"""Figures for the Class 1 notes (Notas/L01). Run: python Notas/L01/figures/make_figures.py

build() writes fourteen PNGs beside this file and asserts at least one plotted number per figure.
Every curve is the model's exact expression; simulations are seeded and say so in their titles.

Sources: mle_sampling_rules.pdf (slides 7-9); poisson-with-breakpoint.pdf (slides 3, 9-10, 12-14,
17-19); class1-poisson-with-exponential-prior.pdf (pp. 3-4); comparing-estimators-MSE-slides.pdf;
multiplelinearregression.pdf pp. 1-22; overfitting_a_linear_model.html; ar-ma.pdf pp. 1-17;
part1-p-hacking.pdf. Coal-mining data: .agent/notes/coal-mining-data.md (Jarrett 1979).
"""
import itertools
import math
import pathlib
import sys

import numpy as np
from scipy import stats

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))
from _figstyle import C, apply, save  # noqa: E402

import matplotlib.pyplot as plt  # noqa: E402

COAL = np.array([4,5,4,1,0,4,3,4,0,6,3,3,4,0,2,6,3,3,5,4,5,3,1,4,4,1,5,5,3,4,2,5,2,2,3,4,2,1,3,2,
                 2,1,1,1,1,3,0,0,1,0,1,1,0,0,3,1,0,3,2,2,0,1,1,1,0,1,0,1,0,0,0,2,1,0,0,0,1,1,0,2,
                 3,3,1,1,2,1,1,1,1,2,4,2,0,0,0,1,4,0,0,0,1,0,0,0,0,0,1,0,0,1,0,1])
YEARS = np.arange(1851, 1963)


def _negbin_theta_pmf(s, theta, m_max=4000):
    """Exact pmf of theta_hat = s/N, N ~ NegBin (trials to the s-th success)."""
    m = np.arange(s, m_max)
    return s / m, stats.nbinom.pmf(m - s, s, theta)


def fig_sampling_rules_pmf():
    """Exact pmf of theta_hat under Bin vs NegBin, s = 1 and s = 4 with n = 10 (slides 7-8)."""
    fig, axes = plt.subplots(1, 2, figsize=(9.6, 3.8))
    out = {}
    for ax, s in zip(axes, (1, 4)):
        n, th = 10, s / 10                      # evaluated at theta = theta_hat (slide 9)
        k = np.arange(n + 1)
        ax.vlines(k / n - 0.006, 0, stats.binom.pmf(k, n, th), color=C["main"], lw=3,
                  label=r"Binomial: $\hat\theta=S/n$")
        x, p = _negbin_theta_pmf(s, th)
        keep = p > 1e-4
        ax.vlines(x[keep] + 0.006, 0, p[keep], color=C["warn"], lw=1.6,
                  label=r"Neg. binomial: $\hat\theta=s/N$")
        mean_nb = float((x * p).sum())
        ax.axvline(th, color=C["ref"], ls="--", lw=1)
        ax.axvline(mean_nb, color=C["warn"], ls=":", lw=1.4)
        ax.annotate(f"NegBin mean {mean_nb:.3f}", (mean_nb, ax.get_ylim()[1] * 0.55),
                    xytext=(6, 0), textcoords="offset points", color=C["warn"], fontsize=9)
        ax.set(title=fr"$s={s}$, $n=10$: exact pmf at $\theta={th}$", xlabel=r"$\hat\theta$",
               ylabel="probability", xlim=(-0.03, 1.05))
        out[s] = mean_nb
    axes[1].legend(loc="upper right", fontsize=8.5)
    save(fig, "L01-sampling-rules-pmf")
    assert abs(out[1] - 0.256) < 5e-4 and abs(out[4] - 0.461) < 5e-4   # slide 9 table


def fig_poisson_pmf():
    """Poisson pmf for lambda = 1, 2, 3 (slide 3; class1-poisson.html)."""
    fig, ax = plt.subplots()
    k = np.arange(0, 11)
    for j, (lam, col) in enumerate(((1, C["ref"]), (2, C["main"]), (3, C["good"]))):
        ax.vlines(k + 0.15 * (j - 1), 0, stats.poisson.pmf(k, lam), color=col, lw=3,
                  label=fr"$\lambda={lam}$")
    p2 = stats.poisson.pmf(2, 2)
    ax.annotate(fr"$\Pr(y=2\mid\lambda=2)={p2:.3f}$", (2, p2), xytext=(3.2, 0.33),
                arrowprops=dict(arrowstyle="->", color=C["hi"]), color=C["hi"])
    ax.set(xlabel="count $k$", ylabel=r"$\Pr(y=k\mid\lambda)$", title="Poisson probabilities")
    ax.legend()
    save(fig, "L01-poisson-pmf")
    assert abs(p2 - 0.271) < 5e-4 and abs(stats.poisson.cdf(3, 2) - 0.857) < 5e-4


def fig_poisson_mle_sampling():
    """MC sampling distribution of lambda_hat (lambda = 2, N = 1000) vs N(lambda, lambda/n) (slide 9)."""
    rng = np.random.default_rng(2024)
    lam, N = 2.0, 1000
    fig, axes = plt.subplots(1, 3, figsize=(10.5, 3.4), sharex=True)
    grid = np.linspace(0.4, 3.6, 400)
    for ax, n in zip(axes, (10, 50, 200)):
        lhat = rng.poisson(lam, size=(N, n)).mean(axis=1)
        step = np.ceil(0.05 * n) / n              # a whole number of support points 1/n per bin
        ax.hist(lhat, bins=np.arange(0.4 - 0.5 / n, 3.6, step), density=True,
                color=C["ref"], alpha=0.55, edgecolor="white")
        ax.plot(grid, stats.norm.pdf(grid, lam, np.sqrt(lam / n)), color=C["warn"])
        ax.axvline(lam, color=C["ink"], ls="--", lw=1)
        ax.set(title=fr"$n={n}$", xlabel=r"$\hat\lambda_{MLE}$")
        ax.text(0.03, 0.95, f"MC var {lhat.var(ddof=1):.3f}\n" + r"$\lambda/n$" + f" = {lam / n:.3f}",
                transform=ax.transAxes, va="top", fontsize=9)
        assert abs(lhat.mean() - lam) < 4 * np.sqrt(lam / n / N)   # unbiased (slide 10)
        assert abs(lhat.var(ddof=1) / (lam / n) - 1) < 0.15        # V = lambda/n (slide 10)
    axes[0].set_ylabel("density")
    save(fig, "L01-poisson-mle-sampling")


def fig_poisson_running_mean():
    """Running mean along 2000 Poisson(2) draws with lambda +- 2 sqrt(lambda/n) (slide 12)."""
    rng = np.random.default_rng(7)
    lam, M = 2.0, 2000
    n = np.arange(1, M + 1)
    run = np.cumsum(rng.poisson(lam, M)) / n
    fig, ax = plt.subplots()
    ax.plot(n, run, color=C["main"], lw=1.4, label=r"running mean $\hat\lambda_n$")
    band = 2 * np.sqrt(lam / n)
    ax.plot(n, lam + band, color=C["ref"], ls=":", label=r"$\lambda\pm2\sqrt{\lambda/n}$")
    ax.plot(n, lam - band, color=C["ref"], ls=":")
    ax.axhline(lam, color=C["good"], lw=1)
    ax.set(xscale="log", ylim=(0, 4.2), xlabel="$n$ (log scale)", ylabel=r"$\hat\lambda_n$",
           title=r"Consistency: one long Poisson(2) sequence")
    ax.legend(loc="upper right")
    save(fig, "L01-poisson-running-mean")
    assert abs(band[-1] - 2 * np.sqrt(2 / 2000)) < 1e-12 and abs(run[-1] - lam) < 4 * np.sqrt(lam / M)


def _segment(t):
    a, b = COAL[YEARS <= t], COAL[YEARS > t]
    return a.sum(), len(a), b.sum(), len(b)


def _xlogx(s, n):
    """s log(s/n) - s, the maximised Poisson log-likelihood kernel (0 log 0 = 0)."""
    return (s * np.log(s / n) if s > 0 else 0.0) - s


def fig_coal_series():
    """Yearly counts with the three MLE lines 1.705 / 3.125 / 0.917 (slides 13-14)."""
    fig, ax = plt.subplots(figsize=(8.4, 3.8))
    ax.vlines(YEARS, 0, COAL, color=C["ref"], lw=2)
    full = COAL.mean()
    m1, m2 = COAL[YEARS <= 1890].mean(), COAL[YEARS > 1890].mean()
    ax.hlines(full, 1851, 1962, color=C["warn"], ls="--", label=fr"1851–1962: $\hat\lambda$={full:.3f}")
    ax.hlines(m1, 1851, 1890, color=C["main"], label=fr"1851–1890: $\hat\lambda_1$={m1:.3f}")
    ax.hlines(m2, 1891, 1962, color=C["good"], label=fr"1891–1962: $\hat\lambda_2$={m2:.3f}")
    ax.set(xlabel="year", ylabel="disasters", title="British coal-mining disasters, 1851–1962")
    ax.legend(loc="upper right")
    save(fig, "L01-coal-series")
    assert (round(full, 3), round(m1, 3), round(m2, 3)) == (1.705, 3.125, 0.917)


def fig_coal_profile_likelihood():
    """Profile log-likelihood of tau (all cuts) and w(tau) on 1885-1895 (slides 18-19)."""
    taus = np.arange(1851, 1962)
    lp = np.array([_xlogx(*_segment(t)[:2]) + _xlogx(*_segment(t)[2:]) for t in taus])
    l0 = _xlogx(COAL.sum(), len(COAL))
    lr = 2 * (lp.max() - l0)
    win = (taus >= 1885) & (taus <= 1895)
    w = np.exp(lp[win] - lp[win].max()); w /= w.sum()
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(10, 3.8), gridspec_kw={"width_ratios": [1.4, 1]})
    a1.plot(taus, lp - lp.max(), color=C["main"])
    a1.axhline(l0 - lp.max(), color=C["warn"], ls="--",
               label=fr"single $\lambda$: $-${lp.max() - l0:.2f} (LR = {lr:.1f})")
    a1.axvspan(1885, 1895, color=C["hi"], alpha=0.12)
    a1.set(xlabel=r"cut year $\tau$", ylabel=r"$\ell_p(\tau)-\max$",
           title="Profile log-likelihood of the cut point")
    a1.legend(loc="upper right")
    a2.bar(taus[win], w, color=np.where(taus[win] == 1891, C["good"], C["ref"]))
    a2.set(xlabel=r"cut year $\tau$", ylabel=r"$w(\tau)$", title=r"Normalised likelihood, 1885–1895")
    a2.annotate(f"{w.max():.3f}", (1891, w.max()), ha="center", va="bottom", color=C["good"])
    save(fig, "L01-coal-profile-likelihood")
    assert taus[lp.argmax()] == 1891 and round(lr, 1) == 70.0 and round(w.max(), 3) == 0.251


def fig_poisson_prior_posterior():
    """Exp(1/2) prior, normalised likelihood Gamma(s+1, n), posterior Gamma(s+1, n+a) (handwritten pp. 3-4)."""
    s, n, a = 127, 41, 0.5                       # coal 1851-1891 (class1-poisson.html)
    lam = np.linspace(0.01, 6, 1200)
    post = stats.gamma(s + 1, scale=1 / (n + a))
    fig, ax = plt.subplots()
    ax.plot(lam, a * np.exp(-a * lam), color=C["hi"], label=r"prior Exp$(a=1/2)$")
    ax.plot(lam, stats.gamma.pdf(lam, s + 1, scale=1 / n), color=C["ref"], ls="--",
            label=r"likelihood (normalised), Gamma$(s+1,n)$")
    ax.plot(lam, post.pdf(lam), color=C["main"], label=r"posterior Gamma$(s+1,a+n)$")
    ax.axvline(s / n, color=C["warn"], lw=1, label=fr"MLE {s / n:.3f}")
    ax.axvline(post.mean(), color=C["good"], lw=1, ls=":", label=fr"posterior mean {post.mean():.3f}")
    ax.set(xlabel=r"$\lambda$", ylabel="density", title="Coal mining 1851–1891: prior to posterior")
    ax.legend(loc="upper left", fontsize=8.5)
    save(fig, "L01-poisson-prior-posterior")
    assert round(post.mean(), 3) == 3.084 and round(post.std(), 3) == 0.273


def mse_four(n, theta):
    """Exact MSEs of xbar, x(n), 2 xbar, (n+1)/n x(n) for U(0, theta) samples of size n.

    comparing-estimators-MSE-slides.pdf slides 3-5; B Example 1.3.8 (p. 11).
    """
    n = np.asarray(n, dtype=float)
    return (theta**2 * (1 + 3 * n) / (12 * n),
            2 * theta**2 / ((n + 1) * (n + 2)),
            theta**2 / (3 * n),
            theta**2 / (n * (n + 2)))


def fig_mse_four():
    theta = 3.0  # deck slide 6
    n = np.arange(1, 51)
    names = [r"$\hat\theta_1=\bar x$", r"$\hat\theta_2=x_{(n)}$",
             r"$\hat\theta_3=2\bar x$", r"$\hat\theta_4=\frac{n+1}{n}x_{(n)}$"]
    cols = [C["warn"], C["main"], C["ref"], C["good"]]
    fig, ax = plt.subplots()
    curves = mse_four(n, theta)
    for m, lab, col in zip(curves, names, cols):
        ax.plot(n, m, color=col, label=lab)
    at10 = [m[9] for m in curves]
    ax.scatter([10] * 4, at10, color=C["hi"], zorder=5, s=22)
    for v in at10:
        ax.annotate(f"{v:.3f}", (10, v), xytext=(5, 3), textcoords="offset points",
                    fontsize=8.5, color=C["hi"])
    ax.axvline(10, color=C["hi"], lw=0.8, ls=":")
    ax.set_yscale("log")
    ax.set_xlabel("sample size $n$")
    ax.set_ylabel(r"MSE (log scale), $\theta=3$")
    ax.set_title("Four estimators of the U(0, θ) bound: exact MSE against n")
    ax.legend(loc="upper right", fontsize=9)
    save(fig, "L01-mse-four-estimators")
    # deck slide 12 "Theory" column: 2.325, 0.136, 0.300, 0.075
    assert np.allclose(at10, [2.325, 0.13636, 0.300, 0.075], atol=5e-5)


def fig_bootstrap_max():
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(10.5, 4.0))
    n = np.arange(1, 101)
    pn = 1 - (1 - 1 / n) ** n
    a1.plot(n, pn, color=C["main"], label=r"$1-(1-1/n)^n$")
    a1.axhline(1 - np.exp(-1), color=C["ref"], ls="--", lw=1, label=r"$1-e^{-1}=0.632$")
    obs = {10: 0.666, 50: 0.622, 100: 0.632}  # deck slide 18, B = 1000 resamples
    a1.scatter(list(obs), list(obs.values()), color=C["hi"], zorder=5,
               label="deck's bootstrap share")
    a1.set_ylim(0.6, 1.01)
    a1.set_xlabel("sample size $n$")
    a1.set_ylabel(r"$P(x^*_{(n)}=x_{(n)})$")
    a1.set_title("Bootstrap point mass at $x_{(n)}$")
    a1.legend(fontsize=8.5)

    # One seeded U(0,3) sample of n = 100 (a simulation, not the deck's sample).
    rng = np.random.default_rng(2026)
    theta, m = 3.0, 100
    x = np.sort(rng.uniform(0, theta, m))
    th4 = (m + 1) / m * x[-1]
    grid = np.linspace(2.80, 3.05, 1200)
    ecdf = np.searchsorted(x, grid, side="right") / m
    a2.step(grid, ecdf**m, where="post", color=C["warn"],
            label=r"nonparametric: $\hat F_n(t)^n$")
    a2.plot(grid, np.clip(grid / th4, 0, 1) ** m, color=C["good"],
            label=r"parametric: $(t/\hat\theta_4)^n$")
    a2.plot(grid, np.clip(grid / theta, 0, 1) ** m, color=C["ref"], ls="--",
            label=r"true: $(t/3)^n$")
    a2.axvline(x[-1], color=C["hi"], lw=0.8, ls=":")
    jump = 1 - ((m - 1) / m) ** m
    a2.annotate(f"jump {jump:.3f} at $x_{{(n)}}$", (x[-1], 0.5), xytext=(-110, 0),
                textcoords="offset points", fontsize=8.5, color=C["hi"])
    a2.set_xlabel("$t$")
    a2.set_ylabel(r"$P(x^*_{(n)}\leq t)$")
    a2.set_title("CDF of $x^*_{(n)}$, n = 100 (seeded sample)")
    a2.legend(fontsize=8, loc="upper left")
    save(fig, "L01-bootstrap-max-pointmass")
    # exact jump of the bootstrap CDF at x(n) equals the slide-18 formula at n = 100
    assert abs(jump - 0.63397) < 1e-4
    assert abs(ecdf[np.searchsorted(grid, x[-1])] ** m - 1) < 1e-12


def fig_r2_vs_criteria():
    # Reproducible simulation: n = 128 (houseprice size, deck slide 7), 7 candidates
    # (as regsubsets on slide 20), 3 with nonzero slopes. Deck formulas, slides 15-16.
    rng = np.random.default_rng(128)
    n, P = 128, 7
    X = rng.standard_normal((n, P))
    y = 1.0 + X[:, :3] @ np.array([1.0, 0.7, 0.5]) + rng.standard_normal(n)

    def rss(cols):
        Z = np.column_stack([np.ones(n), X[:, list(cols)]])
        b = np.linalg.lstsq(Z, y, rcond=None)[0]
        return float(np.sum((y - Z @ b) ** 2))

    tss = float(np.sum((y - y.mean()) ** 2))
    sig2 = rss(range(P)) / (n - P - 1)          # full-model sigma-hat^2
    best = [min(rss(c) for c in itertools.combinations(range(P), d)) for d in range(1, P + 1)]
    d = np.arange(1, P + 1)
    best = np.array(best)
    r2 = 1 - best / tss
    adj = 1 - (best / (n - d - 1)) / (tss / (n - 1))   # W (6.21), p. 181
    cp = (best + 2 * d * sig2) / n                      # deck slide 16
    bic = (best + np.log(n) * d * sig2) / n             # deck slide 16
    fig, axs = plt.subplots(1, 3, figsize=(11, 3.6))
    axs[0].plot(d, r2, "o-", color=C["warn"], label="$R^2$")
    axs[0].plot(d, adj, "o-", color=C["main"], label=r"$R^2_{adj}$")
    axs[0].legend(fontsize=9)
    axs[1].plot(d, cp, "o-", color=C["main"])
    axs[2].plot(d, bic, "o-", color=C["main"])
    for ax, v, lab, best_d in [(axs[0], adj, r"$R^2$ and $R^2_{adj}$", int(d[np.argmax(adj)])),
                               (axs[1], cp, "$C_p$", int(d[np.argmin(cp)])),
                               (axs[2], bic, "BIC", int(d[np.argmin(bic)]))]:
        ax.axvline(best_d, color=C["good"], ls=":", lw=1.2)
        ax.set_xlabel("number of predictors $d$")
        ax.set_title(lab)
    fig.suptitle("Best subset of size d, simulated data (n = 128, true d = 3; seed 128)",
                 fontsize=11)
    save(fig, "L01-r2-vs-criteria")
    assert np.all(np.diff(r2) >= -1e-12)        # R^2 never falls with d
    assert int(d[np.argmin(bic)]) == 3           # BIC recovers the true size here
    return dict(r2=r2, adj=adj, cp=cp, bic=bic)


def fig_overfitting():
    # overfitting_a_linear_model.html, table "In-sample versus out-of-sample performance"
    k = np.arange(1, 6)
    p = [14, 92, 378, 1093, 2380]
    rmse_in = [4.97, 2.52, 0.70, 0.13, 0.03]
    rmse_out = [4.48, 6.83, 25.41, 36.82, 47.13]
    r2_in = [0.7303, 0.9307, 0.9946, 0.9998, 1.0000]
    r2_out = [0.7469, 0.5854, 0.1407, 0.1381, 0.0519]
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(10.5, 3.9))
    a1.plot(k, rmse_in, "o-", color=C["main"], label="in-sample (training, 253 tracts)")
    a1.plot(k, rmse_out, "o-", color=C["warn"], label="out-of-sample (test, 253 tracts)")
    a1.set_yscale("log")
    a1.set_ylabel("RMSE (log scale)")
    a2.plot(k, r2_in, "o-", color=C["main"], label="$R^2_{in}$")
    a2.plot(k, r2_out, "o-", color=C["warn"], label="$R^2_{out}$")
    a2.axhline(1, color=C["ref"], ls="--", lw=1)
    a2.set_ylim(0, 1.05)
    for ax in (a1, a2):
        ax.set_xticks(k, [f"k={i}\np={q}" for i, q in zip(k, p)])
        ax.axvspan(2.5, 5.5, color=C["grid"], alpha=0.5, lw=0)
        ax.legend(fontsize=8.5)
    a1.set_title("Error: training keeps falling, test explodes")
    a2.set_title("$R^2$: in-sample reaches 1 where prediction collapses")
    a1.text(3.6, 1.0, "p > n", color=C["ref"], fontsize=9)
    save(fig, "L01-overfitting-train-test")
    assert rmse_out[-1] / rmse_out[0] > 10.5     # "roughly 11 times worse"
    assert p == [1 + sum(math.comb(13, j) for j in range(1, i + 1)) for i in k]  # p_k, d = 13


def fig_ar1_paths():
    # Seeded simulation: one Gaussian shock sequence, three persistence values.
    rng = np.random.default_rng(1)
    T, sig = 200, 1.0
    a = rng.standard_normal(T) * sig
    t = np.arange(1, T + 1)
    fig, axs = plt.subplots(3, 1, figsize=(7.6, 6.8), sharex=True)
    for ax, phi in zip(axs, [0.5, 0.9, 1.0]):
        y = np.zeros(T)
        prev = 0.0
        for i in range(T):
            prev = phi * prev + a[i]
            y[i] = prev
        if phi < 1:
            half = 2 * sig / np.sqrt(1 - phi**2)          # stationary sd, T (2.10)-(2.11)
            ax.axhspan(-half, half, color=C["good"], alpha=0.12, lw=0)
            lab = rf"$\phi={phi}$: band $\pm2\sigma/\sqrt{{1-\phi^2}}=\pm{half:.2f}$"
        else:
            half = 2 * sig * np.sqrt(t)                    # W (11.21): Var = t sigma^2
            ax.fill_between(t, -half, half, color=C["warn"], alpha=0.12, lw=0)
            lab = r"$\phi=1$ (random walk): band $\pm2\sigma\sqrt{t}$"
        ax.plot(t, y, color=C["warn"] if phi == 1 else C["main"], lw=1.2)
        ax.axhline(0, color=C["ref"], lw=0.8)
        ax.set_title(lab, fontsize=10, loc="left")
    axs[-1].set_xlabel("$t$")
    fig.subplots_adjust(hspace=0.35)
    fig.suptitle("AR(1) paths from the same seeded shocks ($y_0=0$, $\\sigma=1$)", fontsize=11)
    save(fig, "L01-ar1-paths")
    assert abs(2 / np.sqrt(1 - 0.9**2) - 4.588) < 1e-3


def fig_ar1_equilibrium():
    phi, sig, mu, y0 = 0.9, 1.0, 0.0, 8.0
    xs = np.linspace(-9, 11, 600)
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(10.5, 3.9))
    shades = [C["hi"], C["main"], C["ref"], C["warn"]]
    for tt, col in zip([1, 3, 10, 30], shades):
        m = mu + phi**tt * (y0 - mu)
        v = sig**2 * (1 - phi ** (2 * tt)) / (1 - phi**2)
        a1.plot(xs, stats.norm.pdf(xs, m, np.sqrt(v)), color=col, lw=1.4, label=f"$t={tt}$")
    v_inf = sig**2 / (1 - phi**2)
    a1.plot(xs, stats.norm.pdf(xs, mu, np.sqrt(v_inf)), color=C["good"], lw=2.6,
            label=r"$t\to\infty$: $N(0,\,5.26)$")
    a1.axvline(y0, color=C["ref"], ls=":", lw=1)
    a1.set_title(r"$y_t\mid y_0=8$ for $\phi=0.9$ converges to equilibrium")
    a1.set_xlabel("$y_t$")
    a1.legend(fontsize=8.5)
    t = np.arange(0, 41)
    for phi_, col in [(0.5, C["good"]), (0.9, C["main"])]:
        a2.plot(t, (1 - phi_ ** (2 * t)) / (1 - phi_**2), color=col, label=rf"$\phi={phi_}$")
        a2.axhline(1 / (1 - phi_**2), color=col, ls="--", lw=0.9)
    a2.plot(t, t * 1.0, color=C["warn"], label=r"$\phi=1$: $t\sigma^2$")
    a2.set_ylim(0, 20)
    a2.set_xlabel("horizon $t$")
    a2.set_ylabel(r"Var$(y_t\mid y_0)$ / $\sigma^2$")
    a2.set_title("Conditional variance: bounded iff |φ| < 1")
    a2.legend(fontsize=8.5)
    save(fig, "L01-ar1-equilibrium")
    assert abs(v_inf - 5.2632) < 1e-4


def fig_p_vs_bf():
    x0 = 1.8  # part1-p-hacking.pdf slides 7-9
    xs = np.linspace(-3.5, 7.5, 800)
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(10.5, 3.9))
    a1.plot(xs, stats.norm.pdf(xs, 0, 1), color=C["main"], label=r"$H_0:\theta=0$")
    a1.plot(xs, stats.norm.pdf(xs, 4, 1), color=C["warn"], label=r"$H_1:\theta=4$")
    r = xs >= x0
    a1.fill_between(xs[r], stats.norm.pdf(xs[r]), color=C["main"], alpha=0.3)
    lft = xs <= x0
    a1.fill_between(xs[lft], stats.norm.pdf(xs[lft], 4, 1), color=C["warn"], alpha=0.3)
    a1.axvline(x0, color=C["hi"], lw=1.2)
    a1.annotate(r"$\phi(1.8)/\phi(-2.2)=e^{0.8}=2.23$", (x0, 0.33), xytext=(14, 0),
                textcoords="offset points", fontsize=8.5, color=C["hi"])
    a1.text(2.35, 0.02, "0.036", color=C["main"], fontsize=8.5)
    a1.text(0.2, 0.02, "0.014", color=C["warn"], fontsize=8.5)
    a1.set_title("X = 1.8: tail areas vs density heights")
    a1.set_xlabel("$x$")
    a1.legend(fontsize=8.5, loc="upper right")
    xg = np.linspace(0, 4, 400)
    pval = stats.norm.sf(xg)
    post = 1 / (1 + np.exp(-(4 * xg - 8)))   # BF10 = exp(4x - 8), equal priors
    a2.plot(xg, pval, color=C["main"], label=r"p-value $1-\Phi(x)$")
    a2.plot(xg, post, color=C["warn"], label=r"$P(H_1\mid x)$, equal priors")
    a2.axvspan(stats.norm.isf(0.05), 2.0, color=C["hi"], alpha=0.15, lw=0,
               label="p < 0.05 yet BF favours $H_0$")
    a2.axhline(0.05, color=C["ref"], ls=":", lw=1)
    a2.scatter([x0, x0], [stats.norm.sf(x0), 1 / (1 + np.exp(-(4 * x0 - 8)))],
               color=C["hi"], zorder=5)
    a2.set_xlabel("observed $x$")
    a2.set_title("Significance and evidence part ways")
    a2.legend(fontsize=8.2, loc="center right")
    save(fig, "L01-p-vs-bayes-factor")
    assert abs(stats.norm.sf(x0) - 0.0359) < 1e-4
    assert abs(1 / (1 + np.exp(-(4 * x0 - 8))) - 0.310) < 1e-3


def build():
    apply()
    # notes 01-04
    fig_sampling_rules_pmf()
    fig_poisson_pmf()
    fig_poisson_mle_sampling()
    fig_poisson_running_mean()
    fig_coal_series()
    fig_coal_profile_likelihood()
    fig_poisson_prior_posterior()
    # notes 05-08
    fig_mse_four()
    fig_bootstrap_max()
    fig_r2_vs_criteria()
    fig_overfitting()
    fig_ar1_paths()
    fig_ar1_equilibrium()
    fig_p_vs_bf()


if __name__ == "__main__":
    build()
