"""Class 1 (L01) reference implementation, with assert self-checks against the decks' numbers.

Run:  python Notas/L01/L01_python_checks.py      (stops at the first failed assert)

Sections §1-§9 are the code blocks of L01-11-python.md, in the same order. The coal series
and the Change-Point Dial's read-out function are imported from companions/check_companions.py
(reuse, not a copy). Equation numbers "(k)" refer to the section note named in each header.
Every Monte Carlo draw is seeded; MC checks use tolerances of about four standard errors.
"""
import pathlib
import sys
from fractions import Fraction
from math import comb

import numpy as np
import statsmodels.api as sm
from scipy import linalg, stats
from scipy.special import gammaln, xlogy
from statsmodels.tsa.api import VAR
from statsmodels.tsa.ar_model import AutoReg

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / "companions"))
import check_companions as cc  # noqa: E402  coal series (from .agent/notes) + companion read-outs


sys.stdout.reconfigure(encoding="utf-8")


def near(x, printed, tol=5e-4):
    """True when x agrees with a printed value to within tol (default: half a unit in the 3rd decimal)."""
    return abs(float(x) - printed) <= tol


# === §1 Sampling rules: binomial vs negative binomial (L01-01) ===
def negbin_theta(s, theta, m_max=5000):
    """Support s/m and exact pmf of theta_hat = s/N, N = trials to the s-th success: L01-01 (13)."""
    m = np.arange(s, m_max)
    return s / m, stats.nbinom.pmf(m - s, s, theta)   # scipy counts failures, m - s


def negbin_moments(s, theta):
    x, p = negbin_theta(s, theta)
    mean = (x * p).sum()
    return mean, np.sqrt((x**2 * p).sum() - mean**2)


# slide 9 table: exact E and sd of s/N at theta = theta_hat
for s, mean, sd in [(1, 0.256, 0.281), (4, 0.461, 0.178)]:
    m_, sd_ = negbin_moments(s, s / 10)
    assert near(m_, mean) and near(sd_, sd), (s, m_, sd_)
th = 0.1
assert abs(negbin_moments(1, th)[0] - (-th * np.log(th) / (1 - th))) < 1e-12   # closed form (20)
x, p = negbin_theta(4, 0.4)
assert abs(((3 / (4 / x - 1)) * p).sum() - 0.4) < 1e-12                          # Haldane: (s-1)/(N-1) unbiased

J = lambda s, n: n**3 / (s * (n - s))                                            # observed information (8)
assert near(J(1, 10), 111.1, 0.05) and abs(J(1, 10) - 10 / (0.1 * 0.9)) < 1e-9


def wald(th_hat, n, z=1.96):
    """Wald interval th_hat +- z sqrt(th_hat(1-th_hat)/n): same under both rules, (18)."""
    se = np.sqrt(th_hat * (1 - th_hat) / n)
    return th_hat - z * se, th_hat + z * se


assert np.allclose(wald(0.1, 10), (-0.086, 0.286), atol=5e-4)
assert np.allclose(wald(0.4, 10), (0.096, 0.704), atol=5e-4)

p_bin = lambda s, n: stats.binom.cdf(s, n, 0.5)          # P(S <= s | n), extreme = few successes
p_nb = lambda s, n: stats.nbinom.sf(n - s - 1, s, 0.5)   # P(N >= n | s), extreme = many trials
assert abs(p_bin(1, 10) - 11 / 1024) < 1e-15 and near(p_bin(1, 10), 0.0107, 5e-5)
assert abs(p_nb(1, 10) - 0.5**9) < 1e-15 and near(p_nb(1, 10), 0.0020, 5e-5)
assert abs(p_bin(4, 10) - 386 / 1024) < 1e-15 and near(p_bin(4, 10), 0.377)
assert abs(p_nb(4, 10) - 130 / 512) < 1e-15 and near(p_nb(4, 10), 0.254)

# Beta posterior is the same under all three rules: Beta(a+s, b+n-s), (21)
assert near(stats.beta(1 + 1, 1 + 9).mean(), 0.167) and near(stats.beta(1 + 4, 1 + 6).mean(), 0.417)
# the site's Bernoulli code: s = 7 of n = 10, Beta(3,3) prior
for z, lo, hi in [(1.645, 0.462, 0.938), (1.960, 0.416, 0.984), (2.576, 0.327, 1.073)]:
    assert np.allclose(wald(0.7, 10, z), (lo, hi), atol=5e-4)
post = stats.beta(3 + 7, 3 + 3)
assert near(stats.beta(3, 3).std(), 0.189) and near(post.mean(), 0.625) and near(post.std(), 0.117)
assert np.allclose(post.ppf([0.025, 0.975]), (0.384, 0.837), atol=5e-4)
assert np.ceil(1.96**2 * 0.25 / 0.05**2) == 385                                  # sample size (23)
print("§1 sampling rules: ok")


# === §2 Poisson MLE, CRLB and the efficiency of s^2 (L01-02) ===
assert near(stats.poisson.pmf(2, 2), 0.271) and near(stats.poisson.cdf(3, 2), 0.857)
assert near(stats.poisson.cdf(3, 1), 0.981) and near(stats.poisson.pmf(3, 2), 0.18045, 5e-6)

lam = 2.0
k = np.arange(0, 200)
pk = stats.poisson.pmf(k, lam)
assert abs(((k / lam - 1) ** 2 * pk).sum() - 1 / lam) < 1e-12        # Fisher info per obs, (15)-(17)
mu4 = ((k - lam) ** 4 * pk).sum()
assert abs(mu4 - (lam + 3 * lam**2)) < 1e-9                           # mu4 = lambda + 3 lambda^2


def var_s2(lam, n):
    """V(s^2) for iid Poisson, L01-02 (19)."""
    return lam / n + 2 * lam**2 / (n - 1)


def eff_s2(lam, n):
    """CRLB / V(s^2), L01-02 (20); tends to 1/(1+2 lambda), (21)."""
    return (lam / n) / var_s2(lam, n)


for n in (10, 50, 200):
    assert abs(var_s2(lam, n) - (mu4 / n - lam**2 * (n - 3) / (n * (n - 1)))) < 1e-12
assert [round(var_s2(2, n), 3) for n in (10, 50, 200)] == [1.089, 0.203, 0.050]
assert [round(eff_s2(2, n), 3) for n in (10, 50, 200)] == [0.184, 0.197, 0.199]
assert abs(1 / (1 + 2 * lam) - 0.2) < 1e-15
# the deck's MC efficiencies: CRLB over its MC variance of s^2 (slide 10)
assert [round(c / v, 3) for c, v in [(0.2, 1.245), (0.04, 0.187), (0.01, 0.051)]] == [0.161, 0.214, 0.196]

# Monte Carlo (slides 8-10 design, more replications): ybar unbiased with V = lambda/n; s^2 per (19)
rng = np.random.default_rng(10)
N = 20000
for n in (10, 50, 200):
    y = rng.poisson(lam, size=(N, n))
    ybar, s2 = y.mean(axis=1), y.var(axis=1, ddof=1)
    assert abs(ybar.mean() - lam) < 4 * np.sqrt(lam / n / N)
    assert abs(ybar.var(ddof=1) / (lam / n) - 1) < 0.05
    assert abs(s2.mean() - lam) < 4 * s2.std() / np.sqrt(N)          # s^2 also unbiased
    assert abs(s2.var(ddof=1) / var_s2(lam, n) - 1) < 0.07

# slide 12: P(|lambda_hat - 2| < 0.25), exact via s_n ~ Poisson(2n) and by the CLT (14)
for n, exact, normal in [(10, 0.424, 0.424), (50, 0.789, 0.789), (200, 0.987, 0.988)]:
    S = np.arange(0, 10 * n)
    pe = stats.poisson.pmf(S, lam * n)[np.abs(S / n - lam) < 0.25].sum()
    pn = 2 * stats.norm.cdf(0.25 / np.sqrt(lam / n)) - 1
    assert near(pe, exact) and near(pn, normal), (n, pe, pn)
print("§2 Poisson MLE: ok")


# === §3 Coal mining: dispersion test, split, profile likelihood, LR (L01-03) ===
Y, YEARS = cc.Y, cc.YEARS              # Jarrett (1979), read from .agent/notes/coal-mining-data.md
assert len(Y) == 112 and Y.sum() == 191 and Y[:40].sum() == 125 and Y[:41].sum() == 127


def dispersion(seg):
    """Index s^2/ybar and upper-tail p-value of D = (n-1)s^2/ybar ~ chi2_{n-1}, L01-03 (1)."""
    n, m, v = len(seg), seg.mean(), seg.var(ddof=1)
    D = (n - 1) * v / m
    return m, v, v / m, D, stats.chi2.sf(D, n - 1)


rows = {"1851-1962": Y, "1851-1890": Y[YEARS <= 1890], "1891-1962": Y[YEARS > 1890]}
printed = {"1851-1962": (1.705, 2.714, 1.592, 176.7), "1851-1890": (3.125, 2.574, 0.824, 32.1),
           "1891-1962": (0.917, 1.063, 1.160, 82.4)}
pvals = {}
for key, seg in rows.items():
    m, v, idx, D, pv = dispersion(seg)
    m0, v0, i0, D0 = printed[key]
    assert near(m, m0) and near(v, v0) and near(idx, i0) and near(D, D0, 0.05), key
    lo, hi = m - 1.96 * np.sqrt(m / len(seg)), m + 1.96 * np.sqrt(m / len(seg))   # Wald CI, L01-02 (14)
    pvals[key] = pv
assert pvals["1851-1962"] < 0.001 and near(pvals["1851-1890"], 0.774) and near(pvals["1891-1962"], 0.168)


def seg_kernel(seg):
    """Maximised Poisson log-likelihood kernel s log(s/n) - s of one segment (0 log 0 = 0)."""
    s = seg.sum()
    return xlogy(s, s / len(seg)) - s


def profile(y, years):
    """Profile log-likelihood l_p(tau) of L01-03 (6) for every admissible cut tau."""
    taus = years[:-1]
    return taus, np.array([seg_kernel(y[years <= t]) + seg_kernel(y[years > t]) for t in taus])


taus, lp = profile(Y, YEARS)
l0 = seg_kernel(Y)
assert taus[lp.argmax()] == 1891
assert near(lp.max(), -54.055) and near(l0, -89.049)
LR = 2 * (lp.max() - l0)                                                  # (8)
assert near(LR, 69.99, 5e-3) and round(LR, 1) == 70.0
s1, s2_ = Y[:41].sum(), Y[41:].sum()
lr_compact = 2 * (s1 * np.log((s1 / 41) / (191 / 112)) + s2_ * np.log((s2_ / 71) / (191 / 112)))
assert abs(lr_compact - LR) < 1e-9                                        # compact form (9)
LR1890 = 2 * (lp[taus == 1890][0] - l0)
assert near(LR1890, 69.47, 5e-3)
assert 7e-17 < stats.chi2.sf(LR1890, 1) < 9e-17 and 5e-16 < stats.chi2.sf(70.0, 2) < 7e-16

win = (taus >= 1885) & (taus <= 1895)
w = np.exp(lp[win] - lp[win].max())
assert near(np.exp(np.round(lp[win] - lp.max(), 2)).sum(), 3.983)   # L01-03's sum, from the rounded gaps
assert near(w.sum(), 3.985)                                             # unrounded; same weights to 3 dp
w /= w.sum()                                                              # (7)
slide18 = [0.008, 0.091, 0.105, 0.038, 0.154, 0.194, 0.251, 0.098, 0.039, 0.016, 0.007]
assert np.allclose(w, slide18, atol=5e-4)
gaps = [-3.50, -1.02, -0.87, -1.89, -0.49, -0.26, 0.00, -0.94, -1.86, -2.74, -3.59]
assert np.allclose(lp[win] - lp.max(), gaps, atol=5e-3)
assert near(w[4:8].sum(), 0.696)                                          # 1889-1892
# reuse: the Change-Point Dial's own read-out function gives the same LR, w and rates
d = cc.cp_python(1851, 1962, 1891, 5, 0.95)
assert (d["LR2"], d["w"], d["s1_lam"], d["s2_lam"], d["ratio"]) == (f"{LR:.2f}", "0.251", "3.098", "0.901", "3.436")

# why a mixture is overdispersed: law of total variance (2), and the sample's own split
pi, l1, l2 = 40 / 112, 125 / 40, 66 / 72
assert near(pi * l1 + (1 - pi) * l2 + pi * (1 - pi) * (l1 - l2) ** 2, 2.825)
a_, b_ = rows["1851-1890"], rows["1891-1962"]
within = 39 * a_.var(ddof=1) + 71 * b_.var(ddof=1)
between = 40 * (a_.mean() - Y.mean()) ** 2 + 72 * (b_.mean() - Y.mean()) ** 2
assert near(111 * Y.var(ddof=1), 301.3, 0.05) and near(within, 175.9, 0.05) and near(between, 125.4, 0.05)
assert near(np.exp(-191 / 112), 0.182) and (Y == 0).sum() == 33
assert near(stats.poisson.sf(3, 191 / 112), 0.094) and (Y >= 4).sum() == 20
lhat = 191 / 112
rel = lambda s, n, l: s * np.log(lhat / l) - n * (lhat - l)              # log L(lhat_full)/L(l_segment)
assert near(rel(125, 40, 125 / 40), -18.92, 5e-3) and near(rel(66, 72, 66 / 72), -15.81, 5e-3)

# G layer: integrated (not profiled) likelihood of tau with Exp(a) priors on both rates, (10)
a = 0.5


def log_int(seg):
    s, n = seg.sum(), len(seg)
    return np.log(a) + gammaln(s + 1) - (s + 1) * np.log(n + a)


li = np.array([log_int(Y[YEARS <= t]) + log_int(Y[YEARS > t]) for t in taus[win]])
wi = np.exp(li - li.max())
wi /= wi.sum()
assert np.allclose(wi, [0.008, 0.089, 0.104, 0.038, 0.153, 0.194, 0.251, 0.099, 0.040, 0.017, 0.007], atol=5e-4)
print("§3 coal mining: ok")


# === §4 First Bayesian example: Exp(a) prior -> Gamma(s+1, a+n) posterior (L01-04) ===
y41 = Y[:41]                                       # 1851-1891, the site's class1-poisson.html
n, s = len(y41), int(y41.sum())
assert (n, s) == (41, 127) and near(y41.mean(), 3.097561, 5e-7)
a = 0.5
prior = stats.expon(scale=1 / a)
assert prior.mean() == 2 and prior.var() == 4                                     # (3)
assert np.allclose(prior.ppf([0.025, 0.975]), (0.051, 7.38), atol=5e-3)
post = stats.gamma(s + 1, scale=1 / (a + n))                                      # (8), rate a + n
mode = s / (a + n)                                                                # (11)
assert near(post.mean(), 3.084) and near(mode, 3.060) and near(post.std(), 0.273)
assert near(s / n, 3.098)
assert np.allclose(post.ppf([0.025, 0.975]), (2.573, 3.641), atol=5e-4)
se = np.sqrt((s / n) / n)
assert near(se, 0.275) and np.allclose((s / n - 1.96 * se, s / n + 1.96 * se), (2.559, 3.636), atol=5e-4)
wp, wd = a / (n + a), n / (n + a)                                                 # shrinkage weights (13)
assert abs(wp * (1 / a) + wd * (s / n) - post.mean()) < 1e-12 and near(wp, 0.01205, 5e-6)
# a grid posterior (prior x likelihood, normalised numerically) agrees with the conjugate result
g = np.linspace(1e-6, 8, 200001)
logk = s * np.log(g) - n * g - a * g
dens = np.exp(logk - logk.max())
dens /= np.trapezoid(dens, g)
assert near(np.trapezoid(g * dens, g), post.mean(), 1e-6)
assert near((191 + 1) / (112 + a), 1.707)                                         # all 112 years
print("§4 Gamma posterior: ok")


# === §5 Four estimators of the U(0, theta) bound; Monte Carlo; bootstrap (L01-05) ===
def mse_exact(n, theta=1):
    """Exact MSEs (16)-(18) of xbar, x(n), 2 xbar, (n+1)/n x(n); Fractions when theta is."""
    return [theta**2 * Fraction(1 + 3 * n, 12 * n), theta**2 * Fraction(2, (n + 1) * (n + 2)),
            theta**2 * Fraction(1, 3 * n), theta**2 * Fraction(1, n * (n + 2))]


for n in range(1, 201):
    m1, m2, m3, m4 = mse_exact(n)
    if n == 1:
        assert m1 == m2 == m3 == m4
    elif n == 2:
        assert m4 < m2 == m3 < m1
    else:
        assert m4 < m2 < m3 < m1                                   # ranking (22), n >= 3
assert [round(float(m), 3) for m in mse_exact(10, 3)] == [2.325, 0.136, 0.300, 0.075]
sd_th = [3 / np.sqrt(120), 3 * np.sqrt(10 / (121 * 12)), 3 / np.sqrt(30), 3 / np.sqrt(120)]
assert [round(v, 3) for v in sd_th] == [0.274, 0.249, 0.548, 0.274]

# Bolfarine Table 1.1 (p. 12): MSE[x(n)] at n = 10, 20 and the ratio column
assert mse_exact(10)[1] == Fraction(1, 66) and mse_exact(20)[1] == Fraction(1, 231)
assert [mse_exact(n)[0] for n in (3, 5, 10, 20)] == [Fraction(5, 18), Fraction(4, 15), Fraction(31, 120), Fraction(61, 240)]
assert [round(float(mse_exact(n)[1] / mse_exact(n)[0]), 3) for n in (3, 5, 10, 20)] == [0.36, 0.179, 0.059, 0.017]

# G layer: best multiple c x(n), (27)-(29)
mse_c = lambda c, n: c**2 * Fraction(n, n + 2) - 2 * c * Fraction(n, n + 1) + 1     # in units of theta^2
c_star = Fraction(12, 11)
assert mse_c(c_star, 10) == Fraction(1, 121) and near(9 / 121, 0.0744, 5e-5)
assert mse_c(c_star, 10) < mse_c(Fraction(11, 10), 10) == Fraction(1, 120)

# Monte Carlo at theta = 3, n = 10 (slides 9-12), many more replications than the deck's 1000
rng = np.random.default_rng(5)
theta, n, N = 3.0, 10, 200000
xs = rng.uniform(0, theta, size=(N, n))
est = np.column_stack([xs.mean(1), xs.max(1), 2 * xs.mean(1), (n + 1) / n * xs.max(1)])
mse_mc = ((est - theta) ** 2).mean(0)                                          # (26)
assert np.allclose(mse_mc / np.array([float(m) for m in mse_exact(n, 3)]), 1, atol=0.03)
assert np.allclose(est.std(0, ddof=1) / sd_th, 1, atol=0.02)

# nonparametric bootstrap: point mass at x(n), (32)
pm = lambda n: 1 - (1 - 1 / n) ** n
assert [round(pm(n), 3) for n in (10, 50, 100)] == [0.651, 0.636, 0.634]
assert near(1 - np.exp(-1), 0.632)
assert [round((o - pm(n)) / 0.015, 1) for n, o in [(10, 0.666), (50, 0.622), (100, 0.632)]] == [1.0, -0.9, -0.1]

rng = np.random.default_rng(2026)          # the same seeded sample as figure L01-bootstrap-max-pointmass
m = 100
xb = np.sort(rng.uniform(0, 3.0, m))
th4 = (m + 1) / m * xb[-1]
assert near(xb[-1], 2.969) and near(th4, 2.999)
B = 20000
boot = rng.choice(xb, size=(B, m), replace=True)
share = (boot.max(1) == xb[-1]).mean()
assert abs(share - pm(m)) < 4 * np.sqrt(pm(m) * (1 - pm(m)) / B)              # ~63% point mass
par = rng.uniform(0, th4, size=(B, m)).max(1) * (m + 1) / m                      # parametric bootstrap of theta_4
assert abs(par.std(ddof=1) / (th4 / np.sqrt(m * (m + 2))) - 1) < 0.03            # matches the plug-in SD
assert (par == th4).mean() == 0                                                  # no point mass


def plug_in_sd(th, n):
    """SDs of the four estimators with theta replaced by theta_4 (slide 19's plug-in row)."""
    return [th / np.sqrt(12 * n), th * np.sqrt(n / ((n + 1) ** 2 * (n + 2))), 2 * th / np.sqrt(12 * n), th / np.sqrt(n * (n + 2))]


assert np.allclose(plug_in_sd(2.568, 10), [0.234, 0.213, 0.469, 0.234], atol=5e-4)
assert np.allclose(plug_in_sd(2.926, 50), [0.119, 0.056, 0.239, 0.057], atol=1e-3)   # 0.11945: on the rounding edge
assert np.allclose(plug_in_sd(3.029, 100), [0.087, 0.030, 0.175, 0.030], atol=5e-4)
assert np.allclose([3 / np.sqrt(600), 3 * np.sqrt(50 / (51**2 * 52)), 3 / np.sqrt(150), 3 / np.sqrt(2600)],
                   [0.122, 0.058, 0.245, 0.059], atol=5e-4)

# comparing-estimators.html: triangular weights, n = 21; median under t4; Beta(3,9) median
wts = np.array([i if i <= 11 else 22 - i for i in range(1, 22)], float)
assert wts.sum() == 121 and (wts**2).sum() == 891
assert near((wts**2).sum() / 121**2, 0.0609, 5e-5) and near((1 / 21) / (891 / 14641), 0.78, 5e-3)
f0 = stats.t(4).pdf(0)
assert near(f0, 0.375) and near(1 / (4 * f0**2), 1.78, 5e-3) and stats.t(4).var() == 2
assert near(stats.beta(3, 9).median(), 0.236)
# bootstrap-example.html: exact t and chi-square intervals from the page's summaries
tq = stats.t.ppf(0.975, 49)
assert near(tq, 2.00958, 5e-6)
assert np.allclose((0.10006 - tq * 0.9129307 / np.sqrt(50), 0.10006 + tq * 0.9129307 / np.sqrt(50)),
                   (-0.15939, 0.35951), atol=5e-5)
assert np.allclose((50 * 0.8334424 / stats.chi2.ppf(0.975, 49), 50 * 0.8334424 / stats.chi2.ppf(0.025, 49)),
                   (0.5934305, 1.3206221), atol=5e-6)
print("§5 four estimators and the bootstrap: ok")


# === §6 Gaussian linear regression: OLS, projection, R^2, criteria, HC1 (L01-06) ===
def ols(X, y):
    """beta_hat from the normal equations (6)-(7), residuals, RSS, unbiased sigma^2 (19)."""
    b = np.linalg.solve(X.T @ X, X.T @ y)
    e = y - X @ b
    return b, e, e @ e, e @ e / (len(y) - X.shape[1])


rng = np.random.default_rng(6)
n, q = 200, 4
X = np.column_stack([np.ones(n), rng.standard_normal((n, q - 1))])
y = X @ np.array([1.0, 2.0, -1.0, 0.5]) + 1.5 * rng.standard_normal(n)
b, e, rss, s2 = ols(X, y)
fit = sm.OLS(y, X).fit()
assert np.allclose(b, np.linalg.lstsq(X, y, rcond=None)[0]) and np.allclose(b, fit.params)

P = X @ np.linalg.solve(X.T @ X, X.T)                                       # hat matrix (9)
assert np.allclose(P, P.T) and np.allclose(P @ P, P) and np.isclose(np.trace(P), q)
assert np.allclose(X.T @ e, 0) and abs(e.sum()) < 1e-9                       # (10)
tss = ((y - y.mean()) ** 2).sum()
r2 = 1 - rss / tss                                                          # (20)
adj = 1 - (1 - r2) * (n - 1) / (n - q)                                      # (23), q = k + 1
assert np.isclose(r2, fit.rsquared) and np.isclose(adj, fit.rsquared_adj) and np.isclose(s2, fit.scale)
llf = -n / 2 * np.log(2 * np.pi * rss / n) - n / 2                          # (15) at the MLE (16)-(17)
assert np.isclose(llf, fit.llf)                                             # OLS = Gaussian MLE

# HC1 by formula (29) against statsmodels
XtXi = np.linalg.inv(X.T @ X)
yh = X @ np.array([1.0, 2.0, -1.0, 0.5]) + rng.standard_normal(n) * (0.5 + np.abs(X[:, 1]))
bh, eh, _, _ = ols(X, yh)
V_hc1 = n / (n - q) * XtXi @ (X.T * eh**2) @ X @ XtXi
assert np.allclose(np.sqrt(np.diag(V_hc1)), sm.OLS(yh, X).fit(cov_type="HC1").bse)

# E(RSS) = sigma^2 (n - q) (18); in- and out-of-sample MSE at a fixed design, (26)-(27)
rng = np.random.default_rng(26)
n, p_, R = 50, 10, 20000
Xf = rng.standard_normal((n, p_))
Pf = Xf @ np.linalg.solve(Xf.T @ Xf, Xf.T)
eps, eps_new = rng.standard_normal((R, n)), rng.standard_normal((R, n))
mse_in = (((eps - eps @ Pf) ** 2).sum(1) / n).mean()
mse_out = (((eps_new - eps @ Pf) ** 2).sum(1) / n).mean()
assert abs(mse_in - (1 - p_ / n)) < 0.01 and abs(mse_out - (1 + p_ / n)) < 0.01


def criteria(rss, d, n, sig2):
    """Deck slide 16 / L01-06 (24): Cp, AIC, BIC for a model with d predictors."""
    return (rss + 2 * d * sig2) / n, (rss + 2 * d * sig2) / (n * sig2), (rss + np.log(n) * d * sig2) / n


# best subset on the same simulated data as figure L01-r2-vs-criteria (seed 128)
from itertools import combinations  # noqa: E402

rng = np.random.default_rng(128)
n, Pc = 128, 7
Xs = rng.standard_normal((n, Pc))
ys = 1.0 + Xs[:, :3] @ np.array([1.0, 0.7, 0.5]) + rng.standard_normal(n)
rss_of = lambda cols: ols(np.column_stack([np.ones(n), Xs[:, list(cols)]]), ys)[2]
sig2 = rss_of(range(Pc)) / (n - Pc - 1)
best = np.array([min(rss_of(c) for c in combinations(range(Pc), d)) for d in range(1, Pc + 1)])
dd = np.arange(1, Pc + 1)
tss = ((ys - ys.mean()) ** 2).sum()
r2s = 1 - best / tss
adjs = 1 - (1 - r2s) * (n - 1) / (n - dd - 1)
cp, aic, bic = criteria(best, dd, n, sig2)
assert np.all(np.diff(r2s) > 0) and near(r2s[0], 0.337) and near(r2s[-1], 0.644)      # (21)
assert dd[adjs.argmax()] == 5 and near(adjs.max(), 0.627)
assert dd[cp.argmin()] == 4 and near(cp[3], 1.1356, 5e-5) and near(cp[2], 1.1361, 5e-5)
assert np.array_equal(np.argsort(cp), np.argsort(aic))                                  # AIC = Cp / sigma^2
assert dd[bic.argmin()] == 3 and near(bic.min(), 1.211)

# printed numbers of L01-06
assert near(1 - (1 - 0.30) * 50 / 40, 0.125) and near(1 - (1 - 0.10) * 50 / 40, -0.125)   # W p. 181
assert near(128 / 122, 1.049) and near(np.log(128), 4.85, 5e-3) and near(np.log(128) / 2, 2.4, 0.05)
assert [1 + sum(comb(13, j) for j in range(1, kk + 1)) for kk in range(1, 6)] == [14, 92, 378, 1093, 2380]
assert near(47.13 / 4.48, 10.5, 0.05)
assert near(-2.200 + 0.717 * 21.27 + 0.225 * 4.45 + 1.013 * 6.59, 20.728)               # plane through the means
assert near(0.684 / 0.009, 76.0, 0.05) and np.allclose((0.684 - 1.96 * 0.009, 0.684 + 1.96 * 0.009), (0.666, 0.702), atol=5e-4)
for c_, s_, t_, lo_, hi_ in [(0.069, 0.067, 1.03, -0.062, 0.200), (0.439, 0.112, 3.92, 0.219, 0.659),
                             (0.960, 0.152, 6.32, 0.662, 1.258), (1.140, 0.317, 3.60, 0.519, 1.761)]:
    assert near(c_ / s_, t_, 5e-3) and near(c_ - 1.96 * s_, lo_) and near(c_ + 1.96 * s_, hi_)
F = lambda d_r2: (d_r2 / 4) / ((1 - 0.757) / 5531)                                       # W (4.41)
assert near(F(0.002), 11.4, 0.05) and near(F(0.001), 5.7, 0.05) and near(F(0.003), 17.1, 0.05)
assert near(stats.f.ppf(0.95, 4, 5531), 2.37, 5e-3)
assert near(1 - 0.245 * 5564 / 5535, 0.754) and near(1 - 0.243 * 5564 / 5531, 0.756)
print("§6 Gaussian linear regression: ok")


# === §7 AR(1), unit root, AR(p) and VAR(1) (L01-07) ===
def ar1_moments(phi0, phi, sig2):
    """Stationary mean (6) and variance (9) of an AR(1); requires |phi| < 1."""
    assert abs(phi) < 1, "no equilibrium distribution at |phi| >= 1"
    return phi0 / (1 - phi), sig2 / (1 - phi**2)


assert near(ar1_moments(0, 0.9, 1)[1], 5.263) and near(np.sqrt(5.263), 2.294)
assert near(ar1_moments(0, 0.5, 1)[1], 1.333) and near(2 / np.sqrt(1 - 0.9**2), 4.588)
half = lambda phi: np.log(0.5) / np.log(abs(phi))                                    # (17)
assert near(half(0.9), 6.58, 5e-3) and abs(half(0.5) - 1) < 1e-12
assert near(0.9**10 * 8, 2.79, 5e-3) and near((1 - 0.9**20) / 0.19, 4.62, 5e-3)      # (15) at t = 10
assert near(0.9**5, 0.59049, 5e-6) and near(np.sqrt(1000 / 1100), 0.9535, 5e-5)      # W (11.4), p. 355
assert near(0.0091 / (1 - 0.116 + 0.019 + 0.104), 0.00904, 5e-6)                     # Tsay AR(3) mean (21)
assert near(stats.chi2.sf(38.241, 30), 0.1437, 5e-5) and stats.chi2.sf(182.12, 30) < 1e-22   # Ljung-Box (3)

# simulate a stationary AR(1); OLS on the lag = AutoReg's conditional MLE (5), (13)
rng = np.random.default_rng(7)
phi0, phi, T = 0.5, 0.9, 100000
r = np.empty(T)
r[0] = phi0 / (1 - phi)
shocks = rng.standard_normal(T)
for t in range(1, T):
    r[t] = phi0 + phi * r[t - 1] + shocks[t]
Xa = np.column_stack([np.ones(T - 1), r[:-1]])
ba = ols(Xa, r[1:])[0]
assert np.allclose(ba, AutoReg(r, lags=1).fit().params)
mu_, g0 = ar1_moments(phi0, phi, 1.0)
assert abs(r.mean() - mu_) < 0.15 and abs(r.var() / g0 - 1) < 0.06 and abs(ba[1] - phi) < 0.01
assert abs(np.corrcoef(r[5:], r[:-5])[0, 1] - phi**5) < 0.02                       # ACF (11)

# unit root: V(y_t) = t sigma^2 across many random walks (18)
rw = rng.standard_normal((20000, 100)).cumsum(1)
assert abs(rw[:, -1].var() / 100 - 1) < 0.04 and abs(rw[:, 9].var() / 10 - 1) < 0.04

# VAR(1): Tsay Example 8.3 (p. 400)
phi0v = np.array([0.2, 0.4])
Phi = np.array([[0.2, 0.3], [-0.6, 1.1]])
Sig = np.array([[2.0, 1.0], [1.0, 1.0]])
assert np.allclose(sorted(np.linalg.eigvals(Phi).real), [0.5, 0.8])                  # stationary
muv = np.linalg.solve(np.eye(2) - Phi, phi0v)                                        # (23)
assert np.allclose(muv, [1.0, 2.0])
G0 = np.linalg.solve(np.eye(4) - np.kron(Phi, Phi), Sig.flatten(order="F")).reshape(2, 2, order="F")   # (25)
assert np.allclose(G0, np.array([[25, 20], [20, 40]]) / 9)
assert np.allclose(G0, linalg.solve_discrete_lyapunov(Phi, Sig))                     # G0 = Phi G0 Phi' + Sigma (24)
assert np.allclose(Phi @ G0, np.array([[11, 16], [7, 32]]) / 9)                      # Gamma_1 (26)
assert near(G0[0, 1] / np.sqrt(G0[0, 0] * G0[1, 1]), 0.632)

# simulate it; equation-by-equation OLS = statsmodels VAR; sample moments near (23)-(25)
T = 100000
L = np.linalg.cholesky(Sig)
rv = np.empty((T, 2))
rv[0] = muv
for t in range(1, T):
    rv[t] = phi0v + Phi @ rv[t - 1] + L @ rng.standard_normal(2)
Xv = np.column_stack([np.ones(T - 1), rv[:-1]])
Bv = np.linalg.lstsq(Xv, rv[1:], rcond=None)[0]                                      # (3 x 2): const, lag1, lag2
vfit = VAR(rv).fit(1)
assert np.allclose(Bv, vfit.params)
assert np.allclose(Bv[1:].T, Phi, atol=0.02) and np.allclose(rv.mean(0), muv, atol=0.2)
assert np.allclose(np.cov(rv.T), G0, rtol=0.08)
print("§7 AR / VAR: ok")


# === §8 p-hacking: family-wise error, Bonferroni, p-value vs Bayes factor (L01-08) ===
fwer = lambda m, alpha=0.05: 1 - (1 - alpha) ** m                                    # (3), independent tests
assert near(fwer(32), 0.806) and round(fwer(32), 2) == 0.81
assert [round(fwer(m), 3) for m in (1, 5, 10, 32)] == [0.050, 0.226, 0.401, 0.806]
assert 3 * 3 * 3 * 2 * 3 == 162 and near(fwer(162), 0.9998, 5e-5)
assert 0.05 / 32 == 0.0015625

rng = np.random.default_rng(32)
pv = rng.uniform(size=(200000, 32))                                                  # null p-values are U(0,1), (1)
assert abs((pv.min(1) < 0.05).mean() - fwer(32)) < 0.005
assert (pv.min(1) < 0.05 / 32).mean() <= 0.05 + 0.002                                # Bonferroni (4)
# the same 32 tests on correlated statistics (shared data): the rate falls between 0.05 and 0.806
zc = np.sqrt(0.5) * rng.standard_normal((200000, 1)) + np.sqrt(0.5) * rng.standard_normal((200000, 32))
fw_corr = (zc.max(1) > stats.norm.isf(0.05)).mean()
assert 0.05 < fw_corr < fwer(32)
print(f"   family-wise rate: independent {(pv.min(1) < 0.05).mean():.3f}, Bonferroni {(pv.min(1) < 0.05 / 32).mean():.3f}, "
      f"correlated (rho = 0.5) {fw_corr:.3f}")

x0 = 1.8
p_val = stats.norm.sf(x0)                                                            # (5)
assert near(p_val, 0.0359, 5e-5) and near(stats.norm.cdf(x0 - 4), 0.0139, 5e-5)     # (6)
BF01 = stats.norm.pdf(x0) / stats.norm.pdf(x0 - 4)                                   # (7)
assert near(BF01, 2.2255, 5e-5) and abs(np.log(1 / BF01) - (4 * x0 - 8)) < 1e-12     # (8)
assert near(1 / BF01, 0.449)
post_h1 = lambda bf01, prior_odds_10=1.0: 1 / (1 + bf01 / prior_odds_10)             # (11)
assert near(post_h1(BF01), 0.310)                                                    # (10)
odds_needed = 9 * BF01                                                               # (12)-(13)
assert near(odds_needed, 20.03, 5e-3) and near(post_h1(BF01, odds_needed), 0.9, 1e-12)
assert near(20 / 21, 0.952) and near(1 / (9 * 2.23), 1 / 20.07, 1e-5)
assert near(stats.norm.isf(0.05), 1.645)                                             # the band (1.645, 2)
print("§8 p-hacking and evidence: ok")


# === §9 Numbers behind the pitfalls and the self-test (L01-10) ===
def max_lr(y):
    """LR of the best single cut against one rate, (8), vectorised over all cuts by cumulative sums."""
    n, s = len(y), y.sum()
    s1, n1 = np.cumsum(y)[:-1], np.arange(1, n)
    lp_all = xlogy(s1, s1 / n1) + xlogy(s - s1, (s - s1) / (n - n1)) - s
    return 2 * (lp_all.max() - (xlogy(s, s / n) - s))


assert abs(max_lr(Y) - LR) < 1e-9
rng = np.random.default_rng(1962)
null_lr = np.array([max_lr(rng.poisson(191 / 112, 112)) for _ in range(4000)])   # iid Poisson: no break
perm_lr = np.array([max_lr(rng.permutation(Y)) for _ in range(4000)])           # same counts, order destroyed
q_null, q_perm = np.quantile(null_lr, 0.95), np.quantile(perm_lr, 0.95)
assert stats.chi2.isf(0.05, 1) < q_null < q_perm < 20 and null_lr.max() < 70 and perm_lr.max() < 70
assert abs(dispersion(rng.permutation(Y))[2] - dispersion(Y)[2]) < 1e-12           # s^2/ybar ignores the order
print(f"   max-LR 95% quantiles: iid Poisson null {q_null:.1f}, permuted coal {q_perm:.1f} (chi2_1: 3.84; observed 70.0)")

# profiling vs integrating on a toy series: one high first year, then ones (uniform prior on the cut)
toy = np.array([6, 1, 1, 1, 1, 1, 1, 1])
cuts = np.arange(1, len(toy))
lp_toy = np.array([seg_kernel(toy[:c]) + seg_kernel(toy[c:]) for c in cuts])
li_toy = np.array([log_int(toy[:c]) + log_int(toy[c:]) for c in cuts])            # a = 1/2 as in §3
wp_toy, wi_toy = np.exp(lp_toy - lp_toy.max()), np.exp(li_toy - li_toy.max())
wp_toy, wi_toy = wp_toy / wp_toy.sum(), wi_toy / wi_toy.sum()
assert near(wp_toy[0], 0.783) and near(wi_toy[0], 0.653)

# expected information depends on the design, at the same theta: binomial n = 10 vs neg. binomial s = 1
assert 10 / (0.5 * 0.5) == 40 and 1 / (0.5**2 * 0.5) == 8                          # L01-01 (11), (14)
assert near(np.sqrt(1 / 40), 0.158) and near(np.sqrt(1 / 8), 0.354)
# unbiased but not consistent: 2 x_1 for U(0, theta); MSE = theta^2/3 for every n
xs1 = np.random.default_rng(11).uniform(0, 3, size=(200000, 50))
assert abs(((2 * xs1[:, 0] - 3) ** 2).mean() / 3 - 1) < 0.02                         # 9/3 = 3 at theta = 3

# self-test: two inspectors, 2 defective vials in 20 (fixed n) vs 20 vials to the 2nd defective (fixed s)
assert near(J(2, 20), 222.2, 0.05) and near(stats.beta(1 + 2, 1 + 18).mean(), 0.136)
assert near(negbin_moments(2, 0.1)[0], 0.165)                                        # E(2/N) > 0.1
assert near(stats.binom.cdf(2, 20, 0.25), 0.091) and near(stats.nbinom.sf(20 - 2 - 1, 2, 0.25), 0.031)
x_03 = stats.norm.isf(0.03)                                                          # one-sided p = 0.03
assert near(x_03, 1.881) and near(np.exp(4 * x_03 - 8), 0.621) and near(1 / (1 + np.exp(-(4 * x_03 - 8))), 0.383)
assert near(1 / (1 - 0.95**2), 10.256) and near(half(0.95), 13.5, 0.05)              # AR(1), phi = 0.95
assert np.allclose(wald(0.1, 20), (-0.031, 0.231), atol=5e-4)                        # leaves [0, 1]
assert near(1 - 2 / (50 * 0.25**2), 0.36, 1e-12)                                     # Chebyshev, item 9
print("§9 pitfall and self-test numbers: ok")

print("\nALL L01 CHECKS PASSED")
