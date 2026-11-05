"""Figures for the Classes 5+6 notes (Notas/L05). Run: python Notas/L05/figures/make_figures.py

build() writes seven PNGs beside this file and asserts at least one plotted number per figure.
Every curve is the model's exact expression; the data panels use the site's three data sets
(Aula/class-05-06/materials). Seeded simulations are labelled as such.

Sources: notes-on-causal-inference.pdf pp. 5-7 (Simpson), 8-12 (colliders, d-separation),
17-19 (IV system), 21-25 (DiD), 26-36 (RDD); error-in-variables.pdf; omitted-variable.html;
example1-iv-card.html; example2-DiD-card-krueger.html; example3-RDD-age-mva-internal.html;
W eqs. (9.33), (9.36), (15.19), (15.20); MHE (3.2.11), (5.2.1)-(5.2.3), (6.1.2), (6.1.6).
"""
import pathlib
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))
from _figstyle import C, apply, save  # noqa: E402

import matplotlib.pyplot as plt  # noqa: E402

DATA = pathlib.Path(__file__).resolve().parents[3] / "Aula" / "class-05-06" / "materials"


# ---------- L05-01: Simpson's paradox as a weighted average (slides pp. 5-7) ----------
def fig_simpson():
    # recovered / patients, slide p. 6 table
    rm_d, rw_d = 81 / 87, 192 / 263          # drug: men, women
    rm_n, rw_n = 234 / 270, 55 / 80          # no drug
    pw_d, pw_n = 263 / 350, 80 / 350         # share of women among drug / no-drug takers
    pw_pop = 343 / 700                       # share of women in the 700 patients
    pi = np.linspace(0, 1, 201)
    rate = lambda rm, rw, p: (1 - p) * rm + p * rw

    fig, (a1, a2) = plt.subplots(1, 2, figsize=(11, 4.3))
    a1.plot(pi, rate(rm_d, rw_d, pi), color=C["main"], label="drug: $(1-\\pi)\\,0.931+\\pi\\,0.730$")
    a1.plot(pi, rate(rm_n, rw_n, pi), color=C["ref"], label="no drug: $(1-\\pi)\\,0.867+\\pi\\,0.688$")
    a1.plot([pw_d], [rate(rm_d, rw_d, pw_d)], "o", color=C["warn"], ms=8)
    a1.plot([pw_n], [rate(rm_n, rw_n, pw_n)], "o", color=C["warn"], ms=8, label="observed mixes (78% vs 83%)")
    a1.annotate("drug, $\\pi=263/350$\n273/350 = 0.780", (pw_d, rate(rm_d, rw_d, pw_d)), xytext=(0.62, 0.66),
                arrowprops=dict(arrowstyle="->", color=C["warn"]), color=C["warn"], fontsize=9)
    a1.annotate("no drug, $\\pi=80/350$\n289/350 = 0.826", (pw_n, rate(rm_n, rw_n, pw_n)), xytext=(0.02, 0.70),
                arrowprops=dict(arrowstyle="->", color=C["warn"]), color=C["warn"], fontsize=9)
    for r, col in ((rate(rm_d, rw_d, pw_pop), C["good"]), (rate(rm_n, rw_n, pw_pop), C["good"])):
        a1.plot([pw_pop], [r], "s", color=col, ms=7)
    a1.axvline(pw_pop, color=C["good"], ls=":", lw=1.2)
    a1.text(pw_pop - 0.47, 0.955, "common mix $\\pi=343/700$:\ndrug 0.833 vs 0.779", color=C["good"], fontsize=9, va="top")
    a1.set(xlabel="share of women $\\pi$ in the group", ylabel="recovery rate", title="Same strata, different mixes",
           ylim=(0.62, 0.97))
    a1.legend(loc="upper right", fontsize=8, bbox_to_anchor=(1.0, 0.86))

    # (b) continuous version (slide p. 7, example 3): illustrative linear model, exact population lines.
    # Age group g in {young, middle, old}, equally likely; exercise | g ~ N(m_g, s^2);
    # chol = c_g - beta * exercise. Within-group slope -beta; pooled slope from the law of total covariance.
    m = np.array([2.0, 5.0, 8.0])            # mean weekly exercise hours by age group (illustrative)
    cg = np.array([180.0, 201.0, 222.0])     # cholesterol intercept by age group (illustrative)
    beta, s = 2.0, 1.0
    var_x = s**2 + np.var(m)                 # Var(exercise) = E Var + Var E
    cov_xy = -beta * var_x + np.mean((m - m.mean()) * (cg - cg.mean()))
    pooled = cov_xy / var_x
    xs = np.linspace(-1, 11, 50)
    labels = ["young", "middle-aged", "elderly"]
    for k in range(3):
        xk = np.linspace(m[k] - 2.2 * s, m[k] + 2.2 * s, 20)
        a2.plot(xk, cg[k] - beta * xk, color=C["main"], alpha=0.55 + 0.2 * k, label=f"within {labels[k]}: slope $-{beta:.0f}$")
    ybar = np.mean(cg - beta * m)
    a2.plot(xs, ybar + pooled * (xs - m.mean()), color=C["warn"], lw=2.5, label=f"pooled: slope $+{pooled:.2f}$")
    a2.set(xlabel="weekly exercise (hours)", ylabel="cholesterol", title="Exercise and cholesterol (illustrative model)")
    a2.legend(loc="upper left", fontsize=8)
    save(fig, "L05-simpson-weights")

    assert abs(rate(rm_d, rw_d, pw_d) - 273 / 350) < 1e-12 and abs(rate(rm_n, rw_n, pw_n) - 289 / 350) < 1e-12
    ate = rate(rm_d, rw_d, pw_pop) - rate(rm_n, rw_n, pw_pop)
    assert abs(ate - 0.05367) < 5e-5, ate                          # adjusted (standardised) effect, note 02
    assert abs(273 / 350 - 289 / 350 + 0.04571) < 5e-5             # naive gap -4.57 points
    assert abs(pooled - 4.0) < 1e-12                                # (-2*7 + 42)/7 = 4


# ---------- L05-01: collider bias, exact Gaussian algebra (slides pp. 9, 11-12) ----------
def collider_corr(a, b, s, t=0.0):
    """Corr(X, Z | U) for X, Z iid N(0,1), W = aX + bZ + e (Var e = s^2), U = W + v (Var v = t^2); t = 0 gives Corr(X, Z | W)."""
    return -a * b / np.sqrt((a**2 + s**2 + t**2) * (b**2 + s**2 + t**2))


def fig_collider():
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(11, 4.2))
    a = np.linspace(0, 3, 301)
    for s, ls in ((0.5, "-"), (1.0, "--"), (2.0, ":")):
        a1.plot(a, collider_corr(a, 1.0, s), color=C["warn"], ls=ls, label=f"given $W$, noise sd $s={s}$")
    a1.axhline(0, color=C["good"], lw=2, label="unconditional: Corr$(X,Z)=0$")
    a1.set(xlabel="coefficient $a$ in $W=aX+Z+e$", ylabel="partial correlation of $X$ and $Z$",
           title="Conditioning on a collider creates dependence", ylim=(-1, 0.1))
    a1.legend(loc="lower left", fontsize=8)

    t = np.linspace(0, 4, 301)
    a2.plot(t, collider_corr(1.0, 1.0, 1.0, t), color=C["warn"], label="given descendant $U=W+v$ ($a=b=s=1$)")
    a2.axhline(collider_corr(1.0, 1.0, 1.0), color=C["warn"], ls=":", lw=1.2, label="given $W$ itself: $-0.5$")
    a2.axhline(0, color=C["good"], lw=2, label="fork $X\\leftarrow T\\rightarrow Z$ given $T$: 0")
    a2.set(xlabel="sd $t$ of the noise in the descendant $U$", ylabel="partial correlation",
           title="A descendant of a collider also opens the path", ylim=(-0.6, 0.05))
    a2.legend(loc="lower right", fontsize=8)
    save(fig, "L05-collider-bias")

    assert abs(collider_corr(1, 1, 1) + 0.5) < 1e-12
    assert abs(collider_corr(1, 1, 1, 1) + 1 / 3) < 1e-12
    # Monte Carlo cross-check of the formula (seeded)
    rng = np.random.default_rng(5)
    X, Z = rng.normal(size=(2, 200_000))
    Wv = X + Z + rng.normal(size=X.size)
    rx = X - np.polyfit(Wv, X, 1)[0] * Wv
    rz = Z - np.polyfit(Wv, Z, 1)[0] * Wv
    assert abs(np.corrcoef(rx, rz)[0, 1] + 0.5) < 0.01


# ---------- L05-03: omitted-variable bias, the site's simulation made exact (omitted-variable.html) ----------
OVB_BETA, OVB_GAMMA, OVB_N, OVB_REPS = 0.75, 1.20, 30, 1000


def ovb_exact(rho, n=OVB_N, beta=OVB_BETA, gamma=OVB_GAMMA):
    """Exact mean and sd of the no-intercept OLS slope on x: short (y on x) and long (y on x, z).

    (x, z) ~ N(0, [[1, rho], [rho, 1]]), y = beta x + gamma z + e, e ~ N(0, 1), n draws.
    Short: beta_hat = beta + gamma rho + (gamma sqrt(1-rho^2) S_xv + S_xe)/S_xx, E[1/S_xx] = 1/(n-2).
    Long: beta_hat | X ~ N(beta, [(X'X)^-1]_11), E[(X'X)^-1] = Sigma^-1/(n-3) (inverse Wishart mean).
    """
    m_s = beta + gamma * rho
    sd_s = np.sqrt((1 + gamma**2 * (1 - rho**2)) / (n - 2))
    sd_l = np.sqrt(1 / ((n - 3) * (1 - rho**2)))
    return m_s, sd_s, beta + 0 * rho, sd_l


def ovb_mc(rhos, seed=123):
    rng = np.random.default_rng(seed)
    short, long_ = np.zeros((len(rhos), OVB_REPS)), np.zeros((len(rhos), OVB_REPS))
    for j, r in enumerate(rhos):
        L = np.linalg.cholesky(np.array([[1, r], [r, 1]]))
        for i in range(OVB_REPS):
            x, z = L @ rng.normal(size=(2, OVB_N))
            y = OVB_BETA * x + OVB_GAMMA * z + rng.normal(size=OVB_N)
            short[j, i] = (x @ y) / (x @ x)
            X = np.column_stack([x, z])
            long_[j, i] = np.linalg.solve(X.T @ X, X.T @ y)[0]
    return short, long_


def fig_ovb():
    rhos = np.round(np.arange(0, 0.951, 0.05), 2)            # the site's grid seq(0, 0.95, by = 0.05)
    short, long_ = ovb_mc(rhos)
    g = np.linspace(0, 0.95, 200)
    m_s, sd_s, m_l, sd_l = ovb_exact(g)
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(11, 4.3), sharey=True)
    for ax, mc, m, sd, col, title in ((a1, long_, m_l, sd_l, C["good"], "Long regression $y=\\beta x+\\gamma z+\\varepsilon$"),
                                      (a2, short, m_s, sd_s, C["warn"], "Short regression $y=\\beta x+\\varepsilon$")):
        ax.boxplot(mc.T, positions=rhos, widths=0.03, showfliers=False, manage_ticks=False,
                   medianprops=dict(color=C["ink"]), boxprops=dict(color=C["ref"]), whiskerprops=dict(color=C["ref"]),
                   capprops=dict(color=C["ref"]))
        ax.plot(g, m, color=col, lw=2.2, label="exact mean")
        ax.fill_between(g, m - sd, m + sd, color=col, alpha=0.15, label="exact mean $\\pm$ 1 sd")
        ax.axhline(OVB_BETA, color=C["main"], ls="--", lw=1.4, label="true $\\beta=0.75$")
        ax.set(xlabel="corr$(x,z)=\\rho$", title=title, xlim=(-0.04, 0.99))
        ax.legend(loc="upper left", fontsize=8)
    a1.set_ylabel("OLS estimate of $\\beta$ (1000 seeded draws, $n=30$)")
    a2.text(0.5, 0.5, "mean $=0.75+1.2\\rho$", color=C["warn"], fontsize=10)
    save(fig, "L05-ovb-sampling")

    ms, ss, ml, sl = ovb_exact(rhos)
    assert np.all(np.abs(short.mean(1) - ms) < 4 * ss / np.sqrt(OVB_REPS))
    assert np.all(np.abs(long_.mean(1) - ml) < 4 * sl / np.sqrt(OVB_REPS))
    assert abs(ovb_exact(0.95)[0] - 1.89) < 1e-12 and abs(ovb_exact(0.5)[0] - 1.35) < 1e-12
    assert np.all(np.abs(short.std(1) / ss - 1) < 0.12) and np.all(np.abs(long_.std(1) / sl - 1) < 0.12)


# ---------- L05-04: attenuation (error-in-variables.pdf; W (9.33), (9.36)) ----------
def fig_attenuation():
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(11, 4.2))
    k = np.linspace(0, 4, 401)                       # noise-to-signal ratio sigma_u^2 / sigma_x^2
    a1.plot(k, 1 / (1 + k), color=C["warn"], label="no controls: $\\lambda=\\sigma_x^2/(\\sigma_x^2+\\sigma_u^2)$")
    for R2, ls in ((0.5, "--"), (0.8, ":")):
        a1.plot(k, (1 - R2) / (1 - R2 + k), color=C["warn"], ls=ls,
                label=f"controls explain $R^2={R2}$ of $x^*$: $\\sigma_r^2=(1-R^2)\\sigma_x^2$")
    a1.axhline(1, color=C["good"], lw=2, label="IV with an independent 2nd measure: 1")
    a1.plot([1], [0.5], "o", color=C["hi"])
    a1.annotate("equal variances: half the slope", (1, 0.5), xytext=(1.5, 0.62), color=C["hi"],
                arrowprops=dict(arrowstyle="->", color=C["hi"]), fontsize=9)
    a1.set(xlabel="noise-to-signal ratio $\\sigma_u^2/\\sigma_x^2$", ylabel="plim $\\hat\\beta/\\beta$",
           title="Attenuation factor", ylim=(0, 1.08))
    a1.legend(loc="upper right", fontsize=8)

    rng = np.random.default_rng(9)                   # seeded illustration, beta = 1, sigma_x = sigma_u = 1
    n = 300
    x = rng.normal(size=n)
    y = 1.0 * x + rng.normal(scale=0.5, size=n)
    w = x + rng.normal(size=n)
    bx = np.polyfit(x, y, 1)[0]
    bw = np.polyfit(w, y, 1)[0]
    a2.scatter(w, y, s=9, color=C["warn"], alpha=0.45, label="observed $w=x+u$")
    a2.scatter(x, y, s=9, color=C["main"], alpha=0.45, label="true $x$")
    g = np.linspace(-4, 4, 10)
    a2.plot(g, bx * g, color=C["main"], lw=2.2, label=f"OLS on $x$: {bx:.2f}")
    a2.plot(g, bw * g, color=C["warn"], lw=2.2, label=f"OLS on $w$: {bw:.2f} (plim 0.5)")
    a2.set(xlabel="regressor", ylabel="$y$", title="One seeded sample: $\\beta=1$, $\\sigma_x=\\sigma_u=1$", xlim=(-4, 4))
    a2.legend(loc="upper left", fontsize=8)
    save(fig, "L05-attenuation")

    assert abs(1 / (1 + 1) - 0.5) < 1e-12 and abs((1 - 0.8) / (1 - 0.8 + 1) - 1 / 6) < 1e-12
    assert abs(bw - 0.5) < 0.1 and abs(bx - 1) < 0.08


# ---------- L05-05: IV vs OLS plims, calibrated to card.csv (partialled on the site's controls) ----------
# Sample moments of educ, lwage, nearc4 after partialling out the 14 controls of example1-iv-card.html
# (computed in L05_python_checks.py, check_iv_calibration): they make the defaults reproduce OLS 0.0747, IV 0.1315.
IV_SZ, IV_SX, IV_SY = 0.402558, 1.935373, 0.387296
IV_B1, IV_D1, IV_RHO = 0.131504, 0.319899, -0.285147


def iv_plims(rho, d1=IV_D1, phi=0.0, b1=IV_B1, sz=IV_SZ, sx=IV_SX, sy=IV_SY):
    """Exact plims for x = d1 z + ex, y = b1 x + phi z + ey, Corr(ex, ey) = rho, z indep of (ex, ey).

    Returns (OLS of y on x, IV with z, coefficient on x in OLS of y on (x, z)) — slides pp. 18-19, W (15.19).
    """
    var_x = d1**2 * sz**2 + sx**2
    ols = b1 + (rho * sx * sy + phi * d1 * sz**2) / var_x
    iv = b1 + phi / d1
    long_x = b1 + rho * sy / sx
    return ols, iv, long_x


def fig_iv():
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(11, 4.3))
    r = np.linspace(-0.9, 0.9, 361)
    ols, iv, lx = iv_plims(r)
    a1.plot(r, ols, color=C["warn"], label="OLS of $y$ on $x$")
    a1.plot(r, iv + 0 * r, color=C["good"], lw=2.4, label="IV with $z$ (= $\\beta_1$)")
    a1.plot(r, lx, color=C["hi"], ls="--", label="$x$-coefficient in $y$ on $(x,z)$")
    o0, i0, _ = iv_plims(IV_RHO)
    a1.plot([IV_RHO], [o0], "o", color=C["warn"], ms=7)
    a1.plot([IV_RHO], [i0], "o", color=C["good"], ms=7)
    a1.annotate(f"Card: OLS {o0:.4f}", (IV_RHO, o0), xytext=(-0.85, -0.02), color=C["warn"],
                arrowprops=dict(arrowstyle="->", color=C["warn"]), fontsize=9)
    a1.annotate(f"Card: IV {i0:.4f}", (IV_RHO, i0), xytext=(-0.85, 0.20), color=C["good"],
                arrowprops=dict(arrowstyle="->", color=C["good"]), fontsize=9)
    a1.axvline(0, color=C["ref"], lw=1, ls=":")
    a1.set(xlabel="endogeneity $\\rho=$ Corr$(\\varepsilon^x,\\varepsilon^y)$", ylabel="probability limit",
           title="Valid instrument: only IV is centred on $\\beta_1$", ylim=(-0.12, 0.4))
    a1.legend(loc="upper left", fontsize=8)
    a1.text(0.42, 0.04, "OLS and the long regression nearly coincide:\n$\\delta_1^2\\sigma_z^2=0.017 \\ll \\sigma_x^2=3.746$",
            fontsize=8, color=C["ink"], transform=a1.transAxes)

    d = np.linspace(0.02, 1.5, 400)
    phi = 0.005                                      # small direct effect of z on y (exclusion violated)
    o, i, _ = iv_plims(IV_RHO, d1=d, phi=phi)
    a2.plot(d, np.abs(i - IV_B1), color=C["good"], label=f"|IV bias| $=|\\varphi|/\\delta_1$, $\\varphi={phi}$")
    a2.plot(d, np.abs(o - IV_B1), color=C["warn"], label="|OLS bias|")
    n = 3010
    R2 = d**2 * IV_SZ**2 / (d**2 * IV_SZ**2 + IV_SX**2)
    F = n * R2 / (1 - R2)
    d10 = d[np.argmin(np.abs(F - 10))]
    a2.axvline(d10, color=C["ref"], ls=":", lw=1.4)
    a2.text(d10 + 0.03, 0.19, f"first-stage $F=10$\nat $n=3010$\n($\\delta_1={d10:.3f}$)", color=C["ref"], fontsize=9)
    a2.axvline(IV_D1, color=C["main"], ls="--", lw=1.2)
    a2.text(IV_D1 + 0.02, 0.15, "Card $\\delta_1=0.320$", color=C["main"], fontsize=9)
    a2.set(xlabel="first-stage coefficient $\\delta_1$", ylabel="|asymptotic bias|", ylim=(0, 0.25),
           title="Weak first stage magnifies a small exclusion violation")
    a2.legend(loc="upper right", fontsize=8)
    save(fig, "L05-iv-plims")

    assert abs(o0 - 0.0747) < 5e-4 and abs(i0 - 0.1315) < 5e-4
    assert abs(iv_plims(0.0)[0] - IV_B1) < 1e-4                      # rho = 0: OLS consistent up to tiny phi=0 term
    assert abs(iv_plims(IV_RHO, d1=0.05, phi=0.005)[1] - IV_B1 - 0.1) < 1e-12
    assert abs(d10 - 0.277) < 0.005, d10


# ---------- L05-06: DiD on the site's Card-Krueger file (example2-DiD-card-krueger.html) ----------
def did_cells():
    d = pd.read_csv(DATA / "card-krueger.txt", sep=r"\s+")
    m = d.groupby(["treatment", "time"]).outcome.mean()
    return d, m


def fig_did():
    d, m = did_cells()
    pa0, pa1, nj0, nj1 = m[0, 0], m[0, 1], m[1, 0], m[1, 1]
    did = (nj1 - nj0) - (pa1 - pa0)
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(11, 4.3))
    a1.plot([0, 1], [pa0, pa1], "o-", color=C["ref"], label="Pennsylvania (control), $n=75$")
    a1.plot([0, 1], [nj0, nj1], "o-", color=C["main"], label="New Jersey (treated), $n=309$")
    a1.plot([0, 1], [nj0, nj0 + (pa1 - pa0)], "o--", color=C["main"], alpha=0.5, label="NJ counterfactual (common trend)")
    a1.annotate("", xy=(1.03, nj1), xytext=(1.03, nj0 + pa1 - pa0), arrowprops=dict(arrowstyle="<->", color=C["good"], lw=2))
    a1.text(1.06, (nj1 + nj0 + pa1 - pa0) / 2, f"DiD = {did:.2f}", color=C["good"], va="center")
    for xv, yv in ((0, pa0), (1, pa1), (0, nj0), (1, nj1)):
        a1.text(xv - 0.04 if xv == 0 else xv + 0.04, yv + (-0.32 if (xv, yv) == (1, nj1) else 0.12), f"{yv:.2f}", ha="right" if xv == 0 else "left", fontsize=9)
    a1.set(xticks=[0, 1], xticklabels=["Feb 1992", "Nov 1992"], xlim=(-0.3, 1.45), ylim=(17.5, 24),
           ylabel="mean FTE employment per store", title="Card–Krueger: four cell means")
    a1.legend(loc="lower left", fontsize=8)

    se = 1.731                                        # SE of the interaction, site lm output
    delta = np.linspace(-2, 6, 200)                   # differential trend NJ minus PA had there been no policy
    est = did - delta
    a2.plot(delta, est, color=C["main"], label="effect implied by DiD $-\\Delta$")
    a2.fill_between(delta, est - 1.96 * se, est + 1.96 * se, color=C["main"], alpha=0.15, label="$\\pm1.96\\times1.731$")
    a2.axhline(0, color=C["ref"], lw=1)
    a2.axvline(0, color=C["good"], ls="--", lw=1.4, label="common trends ($\\Delta=0$): 2.75")
    a2.axvline(did, color=C["warn"], ls=":", lw=1.4, label=f"$\\Delta={did:.2f}$ wipes it out")
    a2.set(xlabel="differential trend $\\Delta$ (FTE) assumed absent by (5.2.1)", ylabel="employment effect (FTE)",
           title="What a failure of common trends does")
    a2.legend(loc="upper right", fontsize=8)
    save(fig, "L05-did-card-krueger")

    assert abs(pa0 - 23.380) < 5e-4 and abs(pa1 - 21.0967) < 5e-4
    assert abs(nj0 - 20.4306) < 5e-4 and abs(nj1 - 20.8972) < 5e-4
    assert abs(did - 2.75) < 1e-9


# ---------- L05-07: RDD on the MLDA cells (example3-RDD-age-mva-internal.html) ----------
def rdd_fit(age, y, a0=21.0, b=None, p=1, inter=False):
    """OLS of y on [1, D, (a-a0)^k, (a-a0)^k D] within |a-a0| <= b; D = 1(a > a0). Returns (jump, se, sigma, n)."""
    keep = np.ones_like(age, bool) if b is None else np.abs(age - a0) <= b
    a, yy = age[keep] - a0, y[keep]
    D = (a > 0).astype(float)
    cols = [np.ones_like(a), D] + [a**k for k in range(1, p + 1)] + ([a**k * D for k in range(1, p + 1)] if inter else [])
    X = np.column_stack(cols)
    beta, *_ = np.linalg.lstsq(X, yy, rcond=None)
    resid = yy - X @ beta
    dof = len(yy) - X.shape[1]
    s2 = resid @ resid / dof
    se = np.sqrt(s2 * np.linalg.inv(X.T @ X)[1, 1])
    return beta[1], se, np.sqrt(s2), len(yy), beta


def fig_rdd():
    d = pd.read_csv(DATA / "age-mva-internal.txt", sep=r"\s+")
    age = d.age.values
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(11, 4.4))
    over = age > 21
    for col, name, c in (("mva", "motor-vehicle accidents", C["main"]), ("internal", "internal causes", C["warn"])):
        y = d[col].values
        a1.scatter(age[~over], y[~over], s=16, color=c, marker="o")
        a1.scatter(age[over], y[over], s=16, color=c, marker="s", label=name)
        j1, *_ , b1 = rdd_fit(age, y)
        j2, *_ , b2 = rdd_fit(age, y, p=2, inter=True)
        for side in (age <= 21, age > 21):
            g = np.linspace(age[side].min(), age[side].max(), 50) - 21
            D = float(g[0] > 0)
            a1.plot(g + 21, b1[0] + b1[1] * D + b1[2] * g, color=c, lw=2)
            a1.plot(g + 21, b2[0] + b2[1] * D + b2[2] * g + b2[3] * g**2 + (b2[4] * g + b2[5] * g**2) * D,
                    color=c, lw=1.3, ls="--")
    a1.axvline(21, color=C["ref"], ls=":")
    a1.text(19.1, 38.5, "solid: linear (6.1.2)   dashed: quadratic with interactions (6.1.6)", fontsize=8, color=C["ink"])
    a1.set(xlabel="age (years)", ylabel="deaths per 100,000", ylim=(10, 40), title="MLDA: the jump at 21")
    a1.legend(loc="center left", fontsize=8)

    bws = np.round(np.arange(0.40, 2.001, 0.05), 2)
    for col, c in (("mva", C["main"]), ("internal", C["warn"])):
        y = d[col].values
        est = np.array([rdd_fit(age, y, b=b, inter=True)[:2] for b in bws])
        a2.plot(bws, est[:, 0], "o-", ms=3, color=c, label=f"{col}: local linear jump")
        a2.fill_between(bws, est[:, 0] - 1.96 * est[:, 1], est[:, 0] + 1.96 * est[:, 1], color=c, alpha=0.15)
    a2.axhline(0, color=C["ref"], lw=1)
    a2.set(xlabel="bandwidth $b$: cells with $|a-21|\\leq b$", ylabel="estimated jump $\\hat\\rho$ ($\\pm1.96$ SE)",
           title="Local linear: the bandwidth trade-off")
    a2.legend(loc="upper right", fontsize=8)
    save(fig, "L05-rdd-mlda")

    j, se, s, n, _ = rdd_fit(age, d.mva.values)
    assert abs(j - 4.534) < 5e-4 and abs(se - 0.768) < 5e-4 and abs(j / s - 3.411) < 5e-4 and n == 48
    jq, _, sq, _, _ = rdd_fit(age, d.mva.values, p=2, inter=True)
    assert abs(jq / sq - 3.508) < 5e-4
    ji, _, si, _, _ = rdd_fit(age, d.internal.values)
    assert abs(ji / si - 0.380) < 5e-4
    jqi, _, sqi, _, _ = rdd_fit(age, d.internal.values, p=2, inter=True)
    assert abs(jqi / sqi - 1.026) < 5e-4


def build():
    """Make and save the seven figures and run their checks."""
    apply()
    fig_simpson()
    fig_collider()
    fig_ovb()
    fig_attenuation()
    fig_iv()
    fig_did()
    fig_rdd()


if __name__ == "__main__":
    build()
