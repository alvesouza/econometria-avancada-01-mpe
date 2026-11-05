"""Figures for the Class 7 notes (Notas/L07). Run: python Notas/L07/figures/make_figures.py

build() writes seven PNGs beside this file and asserts at least one plotted number per figure.
Every curve is an exact expression (or, for the pregnancy panel, the site's own Gibbs sampler ported
line by line and seeded). Importing this module draws nothing; L07_python_checks.py imports the
shared pieces (data, eight-schools posterior, hierarchical Gibbs, Tobit moments, efficiency ratios).

Sources: GLM3.pdf slides 7-8 (h(z, alpha) = exp(z'alpha)), 16-18 (scale mixture), 22-23 (AR(1) errors);
HLM.pdf slide 23 (eight schools); hierarchicalmodel.html (pregnant women, Souza 1999 / Gamerman & Lopes
2006 Fig. 5.5); limiteddependentvariablemodels.pdf slide 9 (truncation probability) and slides 11-12
(ordered probit); Wooldridge 6e eqs. (17.24)-(17.30) pp. 538-539; Greenberg pp. 124, 127-128 (0.4 vs 1/4).
"""
import pathlib
import sys

import numpy as np
from scipy import stats

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))
from _figstyle import C, apply, save  # noqa: E402

import matplotlib.pyplot as plt  # noqa: E402

# ---------------------------------------------------------------- data printed in the sources
# Eight schools (HLM.pdf slide 23): estimated effect y_i and its standard error sigma_i.
SCHOOLS = list("ABCDEFGH")
Y8 = np.array([28.39, 7.94, -2.75, 6.82, -0.64, 0.63, 18.01, 12.16])
S8 = np.array([14.9, 10.2, 16.3, 11.0, 9.4, 11.4, 10.4, 17.6])

# Pregnant women (hierarchicalmodel.html, section 1): weight gain y_ij at visit time x_ij (weeks),
# I = 68 women, 5 to 7 visits each, n = 427 pairs. NA = no visit. Copied from the Rmd verbatim.
PREG_Y = """
3.3 6.1 8.5 7.9 11.8 14.8 NA
2.0 4.3 8.0 11.0 12.2 15.6 NA
4.5 6.8 8.1 13.5 15.0 NA NA
5.5 5.5 8.0 13.2 13.9 15.1 NA
2.0 9.5 12.2 18.2 19.3 22.0 NA
1.8 2.0 4.5 7.1 9.5 12.6 13.5
0.2 1.4 3.6 5.8 8.3 9.0 NA
3.8 3.4 5.4 8.8 10.4 12.3 15.3
1.9 5.9 6.0 10.6 14.0 21.1 NA
0.0 1.3 3.0 6.4 8.3 10.8 11.2
1.6 1.9 3.4 7.5 8.6 10.0 11.3
1.2 3.0 4.0 8.0 9.0 12.0 14.5
5.4 6.3 10.8 11.2 13.3 15.0 NA
9.5 10.3 14.1 15.4 17.3 17.6 NA
-1.7 1.7 5.4 7.2 8.9 NA NA
2.0 2.4 4.0 4.8 9.8 12.1 NA
-2.8 -2.0 1.5 4.2 5.7 6.7 NA
-3.0 -0.5 1.7 6.0 8.5 11.0 11.0
0.9 1.2 2.3 5.0 8.0 9.3 10.9
2.0 3.2 4.4 6.5 7.5 11.5 14.6
3.6 5.8 7.3 9.0 12.5 13.4 NA
1.1 1.1 6.7 9.6 13.1 17.9 18.2
9.0 11.3 12.9 16.2 17.5 19.0 21.3
0.6 0.8 3.0 3.5 4.5 6.5 8.0
3.2 5.6 8.1 11.5 14.4 17.0 20.0
3.0 3.1 3.5 6.0 7.2 10.0 16.5
-0.2 -0.6 0.0 2.0 8.7 11.0 13.5
0.5 -1.2 1.6 3.2 3.8 6.0 8.4
0.9 3.5 7.2 9.5 11.6 14.4 NA
3.2 4.0 5.5 8.0 9.8 10.7 14.5
1.6 4.0 6.5 7.7 10.5 12.0 NA
5.2 7.0 9.7 13.8 15.4 NA NA
2.8 6.6 11.0 11.5 18.0 20.5 26.3
3.7 3.9 6.8 12.3 15.0 NA NA
-2.6 -3.5 -1.5 1.2 4.0 6.0 NA
7.0 8.1 10.5 14.5 17.4 NA NA
-1.5 0.3 4.0 8.4 10.3 14.5 NA
-0.2 0.0 4.2 5.8 7.5 9.2 NA
2.8 2.5 5.2 8.5 10.5 13.2 NA
-1.4 -0.2 0.5 2.5 4.5 6.7 11.0
1.0 1.0 0.0 4.9 9.2 11.5 NA
0.7 0.1 4.5 5.7 8.0 12.5 NA
4.0 3.9 6.0 8.7 10.0 13.0 NA
4.0 4.5 6.8 12.0 14.0 15.9 NA
2.5 5.4 10.3 13.2 17.4 19.2 24.0
1.7 2.0 1.5 3.0 4.7 6.0 11.4
1.6 2.0 4.0 6.5 6.5 8.5 9.5
0.3 6.0 10.0 13.0 18.7 20.9 NA
1.9 -0.5 1.5 3.8 3.8 7.5 NA
3.5 2.5 3.5 5.0 8.1 12.0 15.0
4.6 5.1 6.4 9.5 10.6 14.5 NA
-4.6 -4.7 -0.9 3.7 3.0 10.0 10.5
2.0 2.2 3.7 6.5 9.0 8.5 NA
-1.5 -1.4 -1.5 2.8 5.7 6.2 NA
0.2 1.2 3.0 4.5 7.0 5.7 NA
-1.0 -0.7 0.0 4.0 7.5 8.0 10.5
2.0 5.4 11.5 14.2 20.5 NA NA
3.0 3.8 6.5 8.8 11.0 NA NA
7.0 10.4 13.0 15.0 16.0 18.0 NA
3.1 4.5 7.5 8.2 9.5 11.7 NA
-1.0 0.6 2.8 5.5 7.9 9.2 NA
-2.0 -0.7 2.4 5.7 9.8 11.1 11.5
0.5 0.5 -2.9 -1.0 1.5 3.4 4.8
3.5 6.9 9.0 16.0 15.7 NA NA
0.3 1.7 3.4 3.1 4.3 3.4 NA
-5.5 -5.0 -4.8 -1.0 2.5 5.0 14.5
-3.0 2.0 2.5 8.0 9.8 12.2 NA
-2.6 -3.2 -2.0 1.0 3.0 4.4 NA
"""
PREG_X = """
8.571 13.000 17.571 20.857 24.571 35.429 40.143
14.429 18.714 23.000 27.000 31.000 37.429 37.857
13.429 18.857 23.143 34.143 37.000 38.000 39.286
12.571 17.000 21.429 32.429 34.286 38.571 40.571
13.714 23.571 27.714 32.429 35.286 39.571 41.857
11.286 14.857 21.286 25.000 30.000 34.429 39.000
13.143 17.143 23.000 28.000 31.429 36.000 38.000
10.429 14.429 17.857 21.857 25.714 30.429 36.000
8.857 14.429 17.714 23.429 28.000 37.714 38.429
12.000 15.000 19.857 24.286 26.714 31.000 37.286
11.429 15.143 19.429 23.571 27.857 32.143 34.571
9.143 14.857 19.143 26.000 28.571 34.000 39.000
10.143 15.571 26.286 29.286 33.286 37.286 37.571
9.143 15.000 21.000 23.857 28.000 31.000 35.857
12.000 22.429 26.429 32.286 35.571 38.000 41.429
6.857 11.000 15.571 19.857 24.000 28.714 36.000
11.429 15.857 20.857 25.857 30.429 34.571 39.286
8.571 14.143 18.571 23.286 29.143 33.286 37.286
11.857 16.857 20.714 24.857 28.857 33.286 37.000
13.143 17.429 21.857 26.286 30.286 35.429 39.143
14.000 18.286 22.857 27.000 31.286 36.714 41.200
13.286 17.143 21.571 26.143 30.429 35.714 39.857
11.857 16.000 23.000 27.000 29.000 33.000 40.000
13.429 18.571 22.286 26.143 33.286 35.143 39.714
15.143 20.143 25.286 29.429 33.857 37.286 39.286
8.571 13.286 16.429 20.286 24.286 29.286 42.429
9.571 14.000 18.429 22.429 34.571 37.000 39.000
11.571 16.857 20.143 24.143 28.857 33.714 38.000
14.714 19.000 23.286 29.000 33.286 39.286 39.571
14.714 19.000 23.714 28.571 31.143 35.143 37.571
10.143 17.286 20.000 24.500 30.714 35.000 39.857
11.857 19.714 23.714 28.000 33.000 35.000 40.286
10.857 15.286 21.857 24.857 31.143 34.000 40.000
11.429 15.429 20.429 31.000 36.429 38.000 40.000
11.429 16.000 19.286 24.857 29.429 34.000 40.571
14.857 19.571 24.286 31.571 42.143 43.000 44.000
14.429 20.286 25.000 30.143 33.143 37.286 40.000
8.000 15.000 22.714 24.571 30.429 34.857 39.000
13.000 17.286 21.857 25.571 32.571 35.714 39.000
8.429 13.429 17.286 23.429 27.429 31.429 39.429
6.714 12.571 16.571 21.286 26.571 34.571 38.571
11.286 16.143 22.429 27.286 30.714 37.571 39.571
11.714 15.857 20.286 25.143 28.857 37.714 39.143
8.857 11.571 16.000 23.857 28.286 35.714 39.714
13.500 19.857 25.000 29.143 33.857 36.143 42.000
8.429 11.571 16.571 20.857 25.429 29.714 39.714
8.286 13.143 18.286 22.571 27.143 31.571 41.429
15.000 20.714 25.000 29.143 36.857 41.000 42.000
9.429 15.857 20.429 25.286 29.857 35.714 41.286
7.429 11.429 16.571 20.471 27.429 35.857 39.571
12.286 16.857 22.000 27.571 32.000 37.286 41.429
12.286 16.571 21.286 25.571 30.429 34.571 36.143
11.429 17.571 22.143 27.143 32.429 37.143 41.571
12.143 16.429 20.857 25.143 29.286 33.429 39.143
14.714 19.143 23.571 27.714 32.143 38.143 40.714
8.143 12.857 16.286 21.857 25.143 30.857 40.714
8.286 15.714 26.286 30.571 37.714 39.000 40.143
13.571 18.571 23.143 31.429 34.429 37.000 39.143
14.857 18.857 23.571 30.571 32.286 37.714 38.286
12.857 17.143 21.857 26.571 31.000 35.571 38.714
6.857 13.714 19.714 23.857 30.000 34.286 41.286
10.143 15.143 19.429 24.143 29.571 33.000 39.143
8.571 13.000 18.143 23.000 28.143 35.286 40.857
12.286 16.571 21.571 30.857 33.429 35.000 37.714
7.000 9.000 13.857 16.857 25.857 30.000 37.000
8.857 11.000 15.857 20.000 26.857 32.571 41.286
10.000 12.000 14.714 21.714 26.571 29.714 40.714
9.429 13.714 17.714 22.000 26.286 30.571 36.714
"""


def pregnancy():
    """Return (ys, xs): lists of 68 arrays, the observed weight gains and visit times of each woman."""
    Y = np.array([[np.nan if v == "NA" else float(v) for v in r.split()] for r in PREG_Y.strip().splitlines()])
    X = np.array([[float(v) for v in r.split()] for r in PREG_X.strip().splitlines()])
    ok = ~np.isnan(Y)
    return [Y[i, ok[i]] for i in range(len(Y))], [X[i, ok[i]] for i in range(len(Y))]


# ---------------------------------------------------------------- L07-01: GLS vs OLS under h(z, alpha)
def design_normal(n=100):
    """Fixed design standing in for x_i ~ N(0, 1) (GLM3 slide 8): normal quantiles at (i - 1/2)/n."""
    return stats.norm.ppf((np.arange(1, n + 1) - 0.5) / n)


def gls_efficiency(alpha1, x=None):
    """Var(OLS)/Var(GLS) for intercept and slope when Var(e_i) = sigma^2 exp(alpha0 + alpha1 x_i).

    Exact given the design: Var_OLS = (X'X)^-1 X'Omega X (X'X)^-1, Var_GLS = (X'Omega^-1 X)^-1.
    alpha0 and sigma^2 cancel from the ratio. Returns an array (ratio_intercept, ratio_slope).
    """
    x = design_normal() if x is None else x
    X = np.column_stack([np.ones_like(x), x])
    h = np.exp(alpha1 * x)
    A = np.linalg.inv(X.T @ X)
    v_ols = A @ (X.T * h) @ X @ A
    v_gls = np.linalg.inv((X.T / h) @ X)
    return np.diag(v_ols) / np.diag(v_gls)


def fig_gls():
    a1 = np.linspace(0, 2.5, 101)
    r = np.array([gls_efficiency(a) for a in a1])
    fig, (ax, bx) = plt.subplots(1, 2, figsize=(10, 4))
    ax.plot(a1, r[:, 1], color=C["main"], label="slope $\\beta_1$")
    ax.plot(a1, r[:, 0], color=C["ref"], ls="--", label="intercept $\\beta_0$")
    r1 = gls_efficiency(1.0)
    ax.scatter([1.0], [r1[1]], color=C["good"], zorder=3)
    ax.annotate(f"slide 8: $\\alpha_1=1$, ratio {r1[1]:.2f}", (1.0, r1[1]), (0.15, 30),
                color=C["good"], arrowprops=dict(arrowstyle="->", color=C["good"]))
    ax.axhline(1, color=C["ref"], lw=1, ls=":")
    ax.set(xlabel="heteroskedasticity parameter $\\alpha_1$ in $h=\\exp(\\alpha_0+\\alpha_1x)$",
           ylabel="Var(OLS) / Var(GLS), log scale", title="What ignoring $\\Omega$ costs")
    ax.set_yscale("log")
    ax.legend()
    xg = np.linspace(-2.5, 2.5, 200)
    for a, col in ((0.5, C["ref"]), (1.0, C["main"]), (2.0, C["warn"])):
        bx.plot(xg, np.exp(-a * xg) / np.exp(-a * xg).max(), color=col, label=f"$\\alpha_1={a}$")
    bx.set(xlabel="$x_i$", ylabel="GLS weight $1/h_i$ (scaled to max 1)",
           title="WLS weights $1/h_i$")
    bx.legend()
    save(fig, "L07-gls-efficiency")
    assert np.allclose(gls_efficiency(0.0), 1.0)                  # homoskedastic: OLS is GLS
    assert np.all(np.diff(r[:, 1]) > 0)                          # cost rises with alpha1
    return r1


# ---------------------------------------------------------------- L07-02: Student-t as a scale mixture
def t_weight(e, nu):
    """E(1/omega_i | e_i) for e_i | omega_i ~ N(0, omega_i), omega_i ~ IG(nu/2, nu/2): (nu+1)/(nu+e^2).

    This is the mean of the Gamma full conditional of lambda_i = 1/omega_i (GLM3 slide 18; Greenberg
    p. 115 with sigma^2 = 1): the weight the observation gets in the next beta draw.
    """
    return (nu + 1) / (nu + e ** 2)


def mixture_pdf(e, nu):
    """Integrate N(e | 0, omega) against IG(omega | nu/2, nu/2) numerically (checks the t identity)."""
    from scipy import integrate
    f = lambda w: stats.norm.pdf(e, 0, np.sqrt(w)) * stats.invgamma.pdf(w, nu / 2, scale=nu / 2)
    return integrate.quad(f, 0, np.inf, limit=200)[0]


def fig_t():
    e = np.linspace(-6, 6, 601)
    fig, (ax, bx) = plt.subplots(1, 2, figsize=(10, 4))
    ax.plot(e, stats.norm.pdf(e), color=C["ink"], lw=2.4, label="$N(0,1)$ ($\\nu=\\infty$)")
    for nu, col in ((2, C["warn"]), (5, C["hi"]), (10, C["main"]), (25, C["good"])):
        ax.plot(e, stats.t.pdf(e, nu), color=col, label=f"$t_{{{nu}}}$")
    ax.set_yscale("log")
    ax.set(ylim=(1e-6, 0.6), xlabel="$\\epsilon/\\sigma$", ylabel="density (log scale)",
           title="Student-t tails: polynomial, not Gaussian")
    ax.legend(fontsize=8.5)
    for nu, col in ((2, C["warn"]), (5, C["hi"]), (10, C["main"]), (25, C["good"])):
        bx.plot(e, t_weight(e, nu), color=col, label=f"$\\nu={nu}$")
    bx.axhline(1, color=C["ink"], lw=1.5, label="Gaussian: weight 1")
    bx.set(xlabel="standardized residual $\\epsilon_i/\\sigma$", ylabel="$E(\\omega_i^{-1}\\mid\\cdot)=(\\nu+1)/(\\nu+\\epsilon_i^2/\\sigma^2)$",
           title="Gibbs weight of observation $i$ in the $\\beta$ draw")
    bx.legend(fontsize=8.5)
    save(fig, "L07-t-scale-mixture")
    for nu in (2, 5, 10):
        assert abs(mixture_pdf(1.7, nu) - stats.t.pdf(1.7, nu)) < 1e-9   # the scale-mixture identity
    assert abs(t_weight(0, 5) - 1.2) < 1e-12 and abs(t_weight(4, 5) - 6 / 21) < 1e-12


# ---------------------------------------------------------------- L07-03: AR(1) errors
def ar1_ratios(rho, phi):
    """Large-n variance ratios for the slope when u_t is AR(1)(rho) and x_t is AR(1)(phi), both stationary.

    true Var(OLS) / naive OLS formula = (1 + rho phi)/(1 - rho phi);
    Var(OLS) / Var(GLS) = (1 + rho phi)(1 + rho^2 - 2 rho phi) / ((1 - rho phi)(1 - rho^2)).
    Derived in L07-03 section 3.
    """
    rho = np.asarray(rho, float)
    naive = (1 + rho * phi) / (1 - rho * phi)
    eff = naive * (1 + rho ** 2 - 2 * rho * phi) / (1 - rho ** 2)
    return naive, eff


def fig_ar1():
    fig, (ax, bx) = plt.subplots(1, 2, figsize=(10, 4))
    k = np.arange(0, 16)
    for r, col in ((0.3, C["ref"]), (0.6, C["main"]), (0.9, C["warn"]), (-0.6, C["hi"])):
        ax.plot(k, r ** k, marker="o", ms=3, color=col, label=f"$\\rho={r}$")
    ax.axhline(0, color=C["ref"], lw=0.8)
    ax.set(xlabel="lag $k$", ylabel="Corr$(\\epsilon_t,\\epsilon_{t+k})=\\rho^k$",
           title="The one-parameter $\\Omega_\\rho$ (slides 22-23)")
    ax.legend(fontsize=8.5)
    rho = np.linspace(-0.95, 0.95, 381)
    for phi, col in ((0.0, C["ref"]), (0.5, C["main"]), (0.9, C["warn"])):
        naive, eff = ar1_ratios(rho, phi)
        bx.plot(rho, eff, color=col, label=f"Var OLS / Var GLS, $\\phi={phi}$")
        bx.plot(rho, naive, color=col, ls="--", lw=1.4, label=f"true / naive OLS var, $\\phi={phi}$")
    bx.set_yscale("log")
    bx.axhline(1, color=C["ink"], lw=0.8)
    bx.set(xlabel="error autocorrelation $\\rho$", ylabel="variance ratio (log scale)",
           title="Regressor persistence $\\phi$ decides the damage")
    bx.legend(fontsize=7.5, loc="lower center")
    save(fig, "L07-ar1-gls")
    n0, e0 = ar1_ratios(0.0, 0.9)
    assert abs(n0 - 1) < 1e-12 and abs(e0 - 1) < 1e-12
    n9, _ = ar1_ratios(0.9, 0.9)
    assert abs(n9 - 1.81 / 0.19) < 1e-12                         # 9.53: naive SE too small by a factor 3.09
    _, e_iid = ar1_ratios(0.9, 0.0)
    assert abs(e_iid - 1.81 / 0.19) < 1e-12                      # phi = 0: (1 + rho^2)/(1 - rho^2)


# ---------------------------------------------------------------- L07-04: eight schools, exact in tau
def schools_conditional(tau, y=Y8, s=S8, kappa=1.0, v0=1e6):
    """Posterior of (mu, theta) given tau for y_i ~ N(theta_i, s_i^2/kappa), theta_i ~ N(mu, tau^2), mu ~ N(0, v0).

    Returns dict with mu_hat, V_mu, B (shrinkage factors), mean (E theta_i | y, tau), sd.
    """
    d = s ** 2 / kappa
    w = 1 / (d + tau ** 2)
    v_mu = 1 / (1 / v0 + w.sum())
    mu = v_mu * np.sum(w * y)
    B = d / (d + tau ** 2)
    mean = (1 - B) * y + B * mu
    var = (1 - B) * d + B ** 2 * v_mu
    return dict(mu=mu, v_mu=v_mu, B=B, mean=mean, sd=np.sqrt(var))


def schools_tau_posterior(grid, y=Y8, s=S8, kappa=1.0, A=100.0, v0=1e6):
    """Normalized p(tau | y) on `grid` for tau ~ U(0, A): N_8(y | 0, diag(s^2/kappa + tau^2) + v0 11')."""
    lp = np.array([stats.multivariate_normal(np.zeros(len(y)), np.diag(s ** 2 / kappa + t ** 2) + v0).logpdf(y)
                   if t < A else -np.inf for t in grid])
    p = np.exp(lp - lp.max())
    return p / np.trapezoid(p, grid)


def quantile_on_grid(grid, p, q):
    cdf = np.concatenate([[0], np.cumsum((p[1:] + p[:-1]) / 2 * np.diff(grid))])
    return float(np.interp(q, cdf / cdf[-1], grid))


def fig_schools():
    taus = np.linspace(0, 30, 301)
    paths = np.array([schools_conditional(t)["mean"] for t in taus])
    grid = np.linspace(0, 100, 4001)
    p = schools_tau_posterior(grid)
    med = quantile_on_grid(grid, p, 0.5)
    fig, (ax, bx) = plt.subplots(1, 2, figsize=(10, 4.2))
    for i in range(8):
        ax.plot(taus, paths[:, i], color=C["main"] if i else C["warn"], lw=2.2 if i == 0 else 1.4)
        ax.text(30.4, paths[-1, i], SCHOOLS[i], va="center", fontsize=9)
    ax.axvline(med, color=C["good"], ls="--", lw=1.2)
    ax.text(med + 0.4, 21, f"posterior median $\\tau$ = {med:.2f}", color=C["good"], fontsize=9)
    ax.set(xlabel="between-school sd $\\tau$", ylabel="$E(\\theta_i\\mid y,\\tau)$",
           title="Shrinkage paths of the eight schools")
    bx.plot(grid[grid <= 30], p[grid <= 30], color=C["main"])
    bx.axvline(med, color=C["good"], ls="--", lw=1.2)
    bx.set(xlabel="$\\tau$", ylabel="$p(\\tau\\mid y)$, prior $U(0,100)$",
           title="Marginal posterior of $\\tau$ (exact, on a grid)")
    save(fig, "L07-eight-schools-shrinkage")
    c0 = schools_conditional(0.0)
    assert np.allclose(c0["mean"], c0["mu"]) and abs(c0["mu"] - 7.8705) < 1e-3   # complete pooling
    assert abs(med - 5.23) < 0.01
    return med


# ---------------------------------------------------------------- L07-04: pregnant women, the site's Gibbs
def ols_by_woman(ys, xs):
    coefs = np.array([np.polyfit(x, y, 1)[::-1] for y, x in zip(ys, xs)])   # (alpha_i, beta_i)
    return coefs


def gibbs_hlm(ys, xs, M0=1000, M=2000, seed=20261025):
    """Port of hierarchicalmodel.html section 4.3, same priors, initial values and update order.

    y_ij ~ N(a_i + b_i x_ij, s_y^2); (a_i, b_i) ~ N((a, b), diag(s_a^2, s_b^2)); (a, b) ~ N(0, 1000 I);
    s_y^2, s_a^2, s_b^2 ~ IG(0.001, 0.001). Returns (draws1 [M x 5]: a, b, s_y, s_a, s_b; draws2 [M x I x 2]).
    The theta_i block is vectorized over women (one 2x2 solve each), otherwise line for line.
    """
    rng = np.random.default_rng(seed)
    I = len(ys)
    n = sum(len(y) for y in ys)
    XtX = np.array([[[len(x), x.sum()], [x.sum(), x @ x]] for x in xs])
    Xty = np.array([[y.sum(), x @ y] for y, x in zip(ys, xs)])
    iA0 = np.diag([1 / 1000, 1 / 1000])
    a0 = b0 = c0 = d0 = e0 = f0 = 0.001
    thetas = ols_by_woman(ys, xs)
    s2a, s2b = thetas[:, 0].var(ddof=1), thetas[:, 1].var(ddof=1)
    iSig = np.diag([1 / s2a, 1 / s2b])
    d1 = np.zeros((M0 + M, 5))
    d2 = np.zeros((M0 + M, I, 2))
    for it in range(M0 + M):
        V = np.diag(1 / np.diag(iA0 + I * iSig))
        mean = V @ iSig @ thetas.sum(0)
        theta = np.array([rng.normal(mean[0], np.sqrt(V[0, 0])), rng.normal(mean[1], np.sqrt(V[1, 1]))])
        ssr = sum(np.sum((y - t[0] - t[1] * x) ** 2) for y, x, t in zip(ys, xs, thetas))
        s2y = 1 / rng.gamma(a0 + n / 2, 1 / (b0 + ssr / 2))
        s2a = 1 / rng.gamma(c0 + I / 2, 1 / (d0 + np.sum((thetas[:, 0] - theta[0]) ** 2) / 2))
        s2b = 1 / rng.gamma(e0 + I / 2, 1 / (f0 + np.sum((thetas[:, 1] - theta[1]) ** 2) / 2))
        iSig = np.diag([1 / s2a, 1 / s2b])
        var = np.linalg.inv(iSig + XtX / s2y)
        mean = np.einsum("ijk,ik->ij", var, iSig @ theta + Xty / s2y)
        L = np.linalg.cholesky(var)
        thetas = mean + np.einsum("ijk,ik->ij", L, rng.standard_normal((I, 2)))
        d1[it] = [theta[0], theta[1], np.sqrt(s2y), np.sqrt(s2a), np.sqrt(s2b)]
        d2[it] = thetas
    return d1[M0:], d2[M0:]


def fig_pregnancy():
    ys, xs = pregnancy()
    x1, y1 = np.concatenate(xs), np.concatenate(ys)
    pooled = np.polyfit(x1, y1, 1)[::-1]
    ind = ols_by_woman(ys, xs)
    d1, d2 = gibbs_hlm(ys, xs)
    post = d2.mean(0)
    fig, (ax, bx) = plt.subplots(1, 2, figsize=(10, 4.2))
    for (a, b), (pa, pb) in zip(ind, post):
        ax.annotate("", (pa, pb), (a, b), arrowprops=dict(arrowstyle="->", color=C["ref"], lw=0.7))
    ax.scatter(ind[:, 0], ind[:, 1], s=14, color=C["warn"], label="individual OLS $(\\hat\\alpha_i,\\hat\\beta_i)$", zorder=3)
    ax.scatter(post[:, 0], post[:, 1], s=14, color=C["main"], label="hierarchical posterior means", zorder=3)
    ax.scatter([pooled[0]], [pooled[1]], s=70, marker="*", color=C["good"], label="pooled OLS", zorder=4)
    ax.set(xlabel="intercept $\\alpha_i$", ylabel="slope $\\beta_i$ (kg per week)",
           title="68 women: individual fits pulled toward the population")
    ax.legend(fontsize=8)
    bx.scatter(x1, y1, s=6, color=C["ref"], alpha=0.6)
    xg = np.linspace(5, 45, 2)
    bx.plot(xg, pooled[0] + pooled[1] * xg, color=C["good"], lw=2.6, label="pooled line")
    for i in (0, 16, 22, 65):
        bx.plot(xs[i], ys[i], "o", ms=3.5, color=C["warn"])
        bx.plot(xg, post[i, 0] + post[i, 1] * xg, color=C["main"], lw=1.2)
    bx.plot([], [], color=C["main"], label="hierarchical lines, women 1, 17, 23, 66")
    bx.set(xlabel="visit time $x_{ij}$ (weeks)", ylabel="weight gain $y_{ij}$ (kg)", xlim=(5, 45),
           title="Pooled line vs woman-specific lines")
    bx.legend(fontsize=8)
    save(fig, "L07-pregnancy-hierarchical")
    assert abs(pooled[0] - (-4.52639)) < 5e-5 and abs(pooled[1] - 0.47633) < 5e-6   # site's lm() output
    assert len(x1) == 427
    sd_ind, sd_post = ind.std(0), post.std(0)
    assert np.all(sd_post < sd_ind)                                # shrinkage: posterior means less dispersed
    return d1, d2, ind, pooled


# ---------------------------------------------------------------- L07-05: Tobit
def tobit_moments(x, beta, sigma, b0=0.0):
    """Tobit at covariate x (W 17.21, 17.24-17.26, 17.30): returns dict of P(y>0), E(y|y>0), E(y), two slopes."""
    xb = b0 + beta * np.asarray(x, float)
    z = xb / sigma
    Phi, phi = stats.norm.cdf(z), stats.norm.pdf(z)
    lam = np.exp(stats.norm.logpdf(z) - stats.norm.logcdf(z))
    return dict(p_pos=Phi, e_pos=xb + sigma * lam, e_all=Phi * xb + sigma * phi,
                dE_all=beta * Phi, dE_pos=beta * (1 - lam * (z + lam)))


def p_zero_slide(a, beta=2.0, s2=0.25):
    """Slide 9: x ~ N(a, 1), y* | x ~ N(beta x, s2) => y* ~ N(a beta, beta^2 + s2); P(y = 0) = Phi(-a beta / sqrt(beta^2 + s2))."""
    return stats.norm.cdf(-a * beta / np.sqrt(beta ** 2 + s2))


def fig_tobit():
    beta, sigma = 2.0, 0.5
    x = np.linspace(-1.5, 1.5, 301)
    m = tobit_moments(x, beta, sigma)
    fig, (ax, bx) = plt.subplots(1, 2, figsize=(10, 4.2))
    ax.plot(x, beta * x, color=C["ref"], ls="--", label="$E(y^*\\mid x)=\\beta x$ (latent)")
    ax.plot(x, m["e_all"], color=C["main"], label="$E(y\\mid x)=\\Phi(z)\\beta x+\\sigma\\phi(z)$ (17.25)")
    ax.plot(x, m["e_pos"], color=C["warn"], label="$E(y\\mid y>0,x)=\\beta x+\\sigma\\lambda(z)$ (17.24)")
    ax.axhline(0, color=C["ink"], lw=0.8)
    ax.set(ylim=(-1.5, 3.2), xlabel="$x$", ylabel="$y$", title="Three means, $\\beta=2$, $\\sigma=0.5$ ($z=\\beta x/\\sigma$)")
    ax.legend(fontsize=8)
    a = np.linspace(-4, 4, 401)
    bx.plot(a, p_zero_slide(a), color=C["main"], label="$P(y=0)=\\Phi(-2a/2.062)$")
    bx.plot(a, 1 - p_zero_slide(a), color=C["good"], ls="--", label="OLS attenuation $\\gamma/\\beta=P(y>0)$")
    for aa in (0.0, 0.7, 1.3):
        pz = p_zero_slide(aa)
        bx.scatter([aa], [pz], color=C["warn"], zorder=3)
        bx.annotate(f"a = {aa}: {pz:.3f}", (aa, pz), (aa + 0.4, pz + 0.12), fontsize=8.5, color=C["warn"])
    bx.set(xlabel="mean of the covariate $a$", ylabel="probability", title="Slide 9: how much is censored")
    bx.legend(fontsize=8, loc="center left")
    save(fig, "L07-tobit-moments")
    assert abs(np.sqrt(4.25) - 2.062) < 5e-4
    assert abs(p_zero_slide(0.0) - 0.5) < 1e-12
    assert abs(p_zero_slide(0.7) - 0.2485) < 1e-4 and abs(p_zero_slide(1.3) - 0.1036) < 1e-4
    assert np.all(m["e_pos"] > m["e_all"]) and np.all(m["e_all"] > 0)


# ---------------------------------------------------------------- L07-06: probit vs logit, ordered probit
def ordered_probs(xb, cuts):
    """P(y = j) = Phi(gamma_j - x'b) - Phi(gamma_{j-1} - x'b), gamma_0 = -inf, gamma_J = +inf (LDV slide 11)."""
    g = np.concatenate([[-np.inf], cuts, [np.inf]])
    F = stats.norm.cdf(g[None, :] - np.asarray(xb, float)[:, None])
    return np.diff(F, axis=1)


def fig_probit():
    z = np.linspace(-5, 5, 401)
    lam = lambda u: 1 / (1 + np.exp(-u))
    fig, (ax, bx) = plt.subplots(1, 2, figsize=(10, 4.2))
    ax.plot(z, stats.norm.cdf(z), color=C["main"], label="probit $\\Phi(z)$")
    ax.plot(z, lam(1.6 * z), color=C["warn"], ls="--", label="logit $\\Lambda(1.6z)$")
    ax.plot(z, lam(z), color=C["ref"], ls=":", label="logit $\\Lambda(z)$")
    ax.plot(z, stats.norm.pdf(z), color=C["main"], lw=1.2)
    ax.plot(z, lam(z) * (1 - lam(z)), color=C["ref"], lw=1.2)
    ax.text(0.15, 0.41, "$\\phi(0)=0.399$", color=C["main"], fontsize=9)
    ax.text(0.15, 0.27, "$\\Lambda'(0)=0.25$", color=C["ref"], fontsize=9)
    ax.set(xlabel="index $z=x'\\beta$", ylabel="probability / density",
           title="Same shape, different scale: $0.399/0.25\\approx1.6$")
    ax.legend(fontsize=8.5, loc="center right")
    cuts = np.array([0.0, 1.0, 2.0])
    xb = np.linspace(-3, 5, 401)
    P = ordered_probs(xb, cuts)
    for j, col in enumerate((C["main"], C["good"], C["hi"], C["warn"])):
        bx.plot(xb, P[:, j], color=col, label=f"$P(y={j+1})$")
    for g in cuts:
        bx.axvline(g, color=C["ref"], lw=0.8, ls=":")
    bx.set(xlabel="$x'\\beta$", ylabel="category probability",
           title="Ordered probit, $J=4$, cut-points $\\gamma=(0,1,2)$")
    bx.legend(fontsize=8.5)
    save(fig, "L07-probit-logit-ordered")
    assert abs(stats.norm.pdf(0) - 0.39894) < 1e-5 and abs(stats.norm.pdf(0) / 0.25 - 1.5958) < 1e-4
    assert np.allclose(P.sum(1), 1)
    assert abs(ordered_probs([0.0], cuts)[0, 0] - 0.5) < 1e-12           # x'b = gamma_1: half below


def build():
    apply()
    r1 = fig_gls()
    fig_t()
    fig_ar1()
    med = fig_schools()
    fig_pregnancy()
    fig_tobit()
    fig_probit()
    print(f"L07 figures written: 7 PNGs; GLS/OLS slope ratio at alpha1 = 1: {r1[1]:.3f}; "
          f"eight-schools posterior median tau = {med:.3f}")


if __name__ == "__main__":
    build()
