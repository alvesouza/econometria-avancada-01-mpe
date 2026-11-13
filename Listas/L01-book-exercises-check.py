"""Reproduce and assert every number printed in Listas/lista-L01-book-exercises.tex.

Run from anywhere: ``python Listas/L01-book-exercises-check.py``. Each ``ok(value, "printed")``
asserts that ``value`` rounds to the printed string (tolerance = half a unit of the last printed
decimal), so a change in data, seed or library that moves a printed digit aborts the script.

Data: Wooldridge PHILLIPS via the ``wooldridge`` package (pip install wooldridge);
ISLP Boston from Listas/data/Boston.csv (provenance in Listas/data/README.md); coal-mining
disasters 1851-1962 typed below (Jarrett 1979, verified in .agent/notes/coal-mining-data.md).
Q19-Q21, Q23-Q24 simulate their own data; Q23 also checks Listas/data/L01-I68-lasso-cv.dat, the
cross-validation curve the list plots. Lasso fits use an exact LARS-lasso path in NumPy (scikit-learn
is not installed).
Stochastic results (Gibbs sampler, bootstraps, simulations) use fixed NumPy seeds and are asserted at
the printed precision; another NumPy version may change the random stream and fail those lines.
"""
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.api as sm
import wooldridge
from scipy import integrate, special, stats
from statsmodels.stats.multitest import multipletests

HERE = Path(__file__).resolve().parent
N_OK = 0


def ok(value, printed):
    """Assert ``value`` matches the printed decimal string ``printed`` to its last digit."""
    global N_OK
    dec = len(printed.split(".")[1]) if "." in printed else 0
    tol = 0.5 * 10 ** (-dec) + 1e-12
    assert abs(float(value) - float(printed)) <= tol, f"{value!r} does not print as {printed}"
    N_OK += 1


# ---------------------------------------------------------------- Q1  Tsay 2.2 (AR(2), phi1 = 0)
phi0, phi2, s2a, r100, r99 = 0.01, 0.2, 0.02, -0.01, 0.02
ok(phi0 / (1 - phi2), "0.0125")                      # mean
ok(s2a / (1 - phi2**2), "0.020833")                  # variance
ok(1 - phi2**2, "0.96")
ok(phi2, "0.2")                                      # rho_2 (rho_1 = 0)
ok(phi0 + phi2 * r99, "0.014")                       # 1-step forecast
ok(phi0 + phi2 * r100, "0.008")                      # 2-step forecast
ok(np.sqrt(s2a), "0.1414")                           # sd of both forecast errors
ok(np.sqrt(s2a / (1 - phi2**2)), "0.1443")           # unconditional sd of r_t
ok(np.sqrt(1 / phi2), "2.2361")                      # |roots| of 1 - 0.2 x^2 = 0

# ---------------------------------------------------------------- Q2  Wooldridge 11.C8 (PHILLIPS)
ph = wooldridge.data("phillips").sort_values("year").reset_index(drop=True)
ph["unem_1"] = ph["unem"].shift(1)
ph["inf_1"] = ph["inf"].shift(1)
est = ph.dropna(subset=["unem_1", "inf_1"])
assert (ph["year"].min(), ph["year"].max(), len(est)) == (1948, 2003, 55)
u03, i03 = ph.loc[ph.year == 2003, ["unem", "inf"]].iloc[0]
ok(u03, "6.0"); ok(i03, "2.3")
ACTUAL_2004 = 5.5   # BLS annual average 2004 (Economic Report of the President); FRED UNRATE 2004 mean 5.54
fred_2004 = [5.7, 5.6, 5.8, 5.6, 5.6, 5.6, 5.5, 5.4, 5.4, 5.5, 5.4, 5.4]
ok(np.mean(fred_2004), "5.54")

m1 = sm.OLS(est["unem"], sm.add_constant(est[["unem_1"]])).fit()
ok(m1.params["const"], "1.489685"); ok(m1.params["unem_1"], "0.742382")
ok(m1.bse["const"], "0.5202"); ok(m1.bse["unem_1"], "0.0893")
ok(m1.rsquared, "0.5660"); ok(np.sqrt(m1.scale), "0.9986")
ok(round(m1.params["unem_1"], 6) * u03, "4.454292")   # product of the printed coefficient
f1 = m1.params["const"] + m1.params["unem_1"] * u03
ok(f1, "5.9440"); ok(f1 - ACTUAL_2004, "0.4440")

m2 = sm.OLS(est["unem"], sm.add_constant(est[["unem_1", "inf_1"]])).fit()
ok(m2.params["const"], "1.296416"); ok(m2.params["unem_1"], "0.649479"); ok(m2.params["inf_1"], "0.183009")
ok(m2.bse["const"], "0.4413"); ok(m2.bse["unem_1"], "0.0779"); ok(m2.bse["inf_1"], "0.0388")
ok(m2.params["inf_1"] / m2.bse["inf_1"], "4.72"); ok(m2.pvalues["inf_1"], "0.00002")
ok(m2.rsquared, "0.6963"); ok(m2.df_resid, "52")
ok(stats.t.ppf(0.975, 52), "2.0066")
ok(round(m2.params["unem_1"], 6) * u03, "3.896874"); ok(round(m2.params["inf_1"], 6) * i03, "0.420921")
f2 = m2.params["const"] + m2.params["unem_1"] * u03 + m2.params["inf_1"] * i03
ok(f2, "5.6142"); ok(f2 - ACTUAL_2004, "0.1142")

# Section 6-4: regress on regressors centred at the 2003 values; intercept = forecast, its se = se(y0hat)
Xc = np.column_stack([np.ones(len(est)), est["unem_1"] - u03, est["inf_1"] - i03])
m3 = sm.OLS(est["unem"].to_numpy(), Xc).fit()
ok(m3.params[0], "5.6142")
se_y0, sig = m3.bse[0], np.sqrt(m3.scale)
ok(se_y0, "0.136381"); ok(sig, "0.8434")
ok(se_y0**2, "0.018600"); ok(sig**2, "0.711321")
se_e0 = np.sqrt(se_y0**2 + sig**2)
ok(round(se_y0**2, 6) + round(sig**2, 6), "0.729921")   # sum of the printed squares; ok(se_e0, "0.8544")
half = stats.t.ppf(0.975, m3.df_resid) * se_e0
ok(half, "1.7144")
ok(f2 - half, "3.8998"); ok(f2 + half, "7.3286")

# ---------------------------------------------------------------- Q3  Wooldridge 12.1 (AR(1) x and u, large n)
for rho, lam, ratio, sd_ratio in [(0.5, 0.5, "1.6667", "1.2910"), (-0.5, 0.5, "0.6000", "0.7746")]:
    r = (1 + rho * lam) / (1 - rho * lam)
    ok(r, ratio); ok(np.sqrt(r), sd_ratio)

# ---------------------------------------------------------------- Q4  Greenberg 2.2 (illustration, coal 1851-1891)
y41 = np.array([4, 5, 4, 1, 0, 4, 3, 4, 0, 6, 3, 3, 4, 0, 2, 6, 3, 3, 5, 4, 5, 3, 1, 4, 4, 1, 5, 5, 3, 4,
                2, 5, 2, 2, 3, 4, 2, 1, 3, 2, 2])
n41, s41 = len(y41), y41.sum()
assert (n41, s41) == (41, 127)
w = 1.0 / (1.0 + n41)
ok(y41.mean(), "3.097561"); ok(w, "0.023810"); ok(1 - w, "0.976190")
ok(w * 0.5, "0.011905"); ok((1 - w) * y41.mean(), "3.023810")
ok((0.5 + s41) / (1.0 + n41), "3.035714")

# ---------------------------------------------------------------- Q5  Greenberg 7.3 (coal mining)
y = np.array([4, 5, 4, 1, 0, 4, 3, 4, 0, 6, 3, 3, 4, 0, 2, 6, 3, 3, 5, 4, 5, 3, 1, 4, 4, 1, 5, 5, 3, 4,
              2, 5, 2, 2, 3, 4, 2, 1, 3, 2, 2, 1, 1, 1, 1, 3, 0, 0, 1, 0, 1, 1, 0, 0, 3, 1, 0, 3, 2, 2,
              0, 1, 1, 1, 0, 1, 0, 1, 0, 0, 0, 2, 1, 0, 0, 0, 1, 1, 0, 2, 3, 3, 1, 1, 2, 1, 1, 1, 1, 2,
              4, 2, 0, 0, 0, 1, 4, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1])
n, S = len(y), y.sum()
assert (n, S) == (112, 191)
cs, ks = np.cumsum(y), np.arange(1, n + 1)
assert cs[40] == 127                                  # 1851-1891 (k = 41)
a0, b0 = 0.5, 1.0
lfact = special.gammaln(y + 1).sum()


def log_gamma_poisson(sh, rt):
    """log of int theta^sh e^{-rt theta} G(theta | a0, b0) dtheta (gamma-Poisson kernel)."""
    return a0 * np.log(b0) - special.gammaln(a0) + special.gammaln(a0 + sh) - (a0 + sh) * np.log(b0 + rt)


# exact marginal likelihood and exact p(k|y): theta1, theta2 integrate out in closed form
lk = -np.log(n) - lfact + log_gamma_poisson(cs, ks) + log_gamma_poisson(S - cs, n - ks)
logm_exact = special.logsumexp(lk)
pk = np.exp(lk - logm_exact)
ok(logm_exact, "-179.4590")
ok(ks[pk.argmax()], "41")
exact_pk = {41: "0.2482", 40: "0.1848", 39: "0.1414", 42: "0.1010", 37: "0.0898", 36: "0.0745"}
for kv, pr in exact_pk.items():
    ok(pk[kv - 1], pr)
ok(np.sum(pk * (a0 + cs) / (b0 + ks)), "3.0500")
ok(np.sum(pk * (a0 + S - cs) / (b0 + n - ks)), "0.9147")

# Gibbs sampler
rng = np.random.default_rng(2026)
G, burn = 10000, 1000
k = n // 2
draws = np.empty((G, 3))
for g in range(G + burn):
    t1 = rng.gamma(a0 + cs[k - 1], 1 / (b0 + k))
    t2 = rng.gamma(a0 + S - cs[k - 1], 1 / (b0 + n - k))
    lp = ks * (t2 - t1) + cs * np.log(t1 / t2)
    p = np.exp(lp - lp.max())
    k = rng.choice(ks, p=p / p.sum())
    if g >= burn:
        draws[g - burn] = (t1, t2, k)
th1, th2, kk = draws[:, 0], draws[:, 1], draws[:, 2].astype(int)
ok(th1.mean(), "3.0506"); ok(th1.std(ddof=1), "0.2809")
ok(th2.mean(), "0.9166"); ok(th2.std(ddof=1), "0.1163")
for v, pr in zip(np.quantile(th1, [0.025, 0.975]), ["2.530", "3.635"]):
    ok(v, pr)
for v, pr in zip(np.quantile(th2, [0.025, 0.975]), ["0.701", "1.156"]):
    ok(v, pr)
ok(kk.mean(), "40.14")
gibbs_pk = {41: "0.2471", 40: "0.1849", 39: "0.1433", 42: "0.0987", 37: "0.0881", 36: "0.0742"}
for kv, pr in gibbs_pk.items():
    ok(np.mean(kk == kv), pr)
ok(np.mean((kk >= 36) & (kk <= 46)), "0.98")   # years 1886-1896

# Chib (1995) at theta* = posterior means; theta1, theta2 independent given k -> Rao-Blackwell average
t1s, t2s = th1.mean(), th2.mean()
loglik = special.logsumexp(-np.log(n) + cs * np.log(t1s) - ks * t1s
                           + (S - cs) * np.log(t2s) - (n - ks) * t2s) - lfact
lprior = stats.gamma.logpdf(t1s, a0, scale=1 / b0) + stats.gamma.logpdf(t2s, a0, scale=1 / b0)
dens = (stats.gamma.pdf(t1s, a0 + cs[kk - 1], scale=1 / (b0 + kk))
        * stats.gamma.pdf(t2s, a0 + S - cs[kk - 1], scale=1 / (b0 + n - kk)))
lpost = np.log(dens.mean())
ok(loglik, "-172.2563"); ok(lprior, "-5.6261"); ok(lpost, "1.5765")
ok(loglik + lprior - lpost, "-179.4589")

# ---------------------------------------------------------------- Q6  ISLP 5.2
for nn, pr_out in [(5, "0.32768"), (100, "0.366032"), (10000, "0.367861")]:
    ok((1 - 1 / nn) ** nn, pr_out)
for nn, pr_in in [(5, "0.67232"), (100, "0.633968"), (10000, "0.632139")]:
    ok(1 - (1 - 1 / nn) ** nn, pr_in)
ok(1 - np.exp(-1), "0.632121")
plot_pts = {1: "1.0000", 2: "0.7500", 3: "0.7037", 5: "0.6723", 10: "0.6513", 20: "0.6415", 50: "0.6358",
            100: "0.6340", 1000: "0.6323", 10000: "0.6321", 100000: "0.6321"}
for nn, pr in plot_pts.items():
    ok(1 - (1 - 1 / nn) ** nn, pr)
# (h) the printed code: rng.choice(100, replace=True) draws ONE index per loop
rng = np.random.default_rng(10)
store = np.empty(10000)
for i in range(10000):
    store[i] = np.sum(rng.choice(100, replace=True) == 4) > 0
ok(np.mean(store), "0.0089")
# (h) intended code: a full bootstrap sample of size 100 per loop
rng = np.random.default_rng(10)
store = np.empty(10000)
for i in range(10000):
    store[i] = np.sum(rng.choice(100, size=100, replace=True) == 4) > 0
ok(np.mean(store), "0.6362")

# ---------------------------------------------------------------- Q7  ISLP 5.9 (Boston medv)
medv = pd.read_csv(HERE / "data" / "Boston.csv")["medv"].to_numpy()
N = len(medv)
assert N == 506
mu, sd = medv.mean(), medv.std(ddof=1)
se = sd / np.sqrt(N)
ok(mu, "22.5328"); ok(sd, "9.1971"); ok(np.sqrt(N), "22.4944"); ok(se, "0.4089")
ok(2 * se, "0.8177"); ok(mu - 2 * se, "21.7151"); ok(mu + 2 * se, "23.3505")
rng = np.random.default_rng(1)
B = 10000
boot = medv[rng.integers(0, N, size=(B, N))]
se_b_mean = boot.mean(1).std(ddof=1)
se_b_med = np.median(boot, 1).std(ddof=1)
se_b_p10 = np.percentile(boot, 10, axis=1).std(ddof=1)
ok(se_b_mean, "0.4098"); ok(2 * se_b_mean, "0.8196")
ok(mu - 2 * se_b_mean, "21.7132"); ok(mu + 2 * se_b_mean, "23.3524")
ok(np.median(medv), "21.2"); ok(se_b_med, "0.3796")
ok(np.percentile(medv, 10), "12.75"); ok(se_b_p10, "0.5080")

# ---------------------------------------------------------------- Q8  Bolfarine 1.4 (n = 10, in units of sigma^4)
ok(2 / 9, "0.2222"); ok(19 / 100, "0.19")

# ---------------------------------------------------------------- Q9  Bolfarine 1.9
ok((2 - np.sqrt(2)) / 4, "0.1464"); ok((2 + np.sqrt(2)) / 4, "0.8536")
# MSE(theta1) = theta(1-theta), MSE(theta2) = (1/2 - theta)^2: equal at the two roots
for r in [(2 - np.sqrt(2)) / 4, (2 + np.sqrt(2)) / 4]:
    assert abs(r * (1 - r) - (0.5 - r) ** 2) < 1e-12

# ---------------------------------------------------------------- Q10 Bolfarine 1.12 (Monte Carlo check of the MSEs)
rng = np.random.default_rng(7)
theta, nn, R = 1.0, 10, 200000
X = rng.uniform(0, theta, size=(R, nn))
mse1 = np.mean((2 * X.mean(1) - theta) ** 2)
mse2 = np.mean(((nn + 1) / nn * X.max(1) - theta) ** 2)
ok(theta**2 / (3 * nn), "0.0333"); ok(theta**2 / (nn * (nn + 2)), "0.0083")
ok(mse1, "0.0333"); ok(mse2, "0.0084"); ok(3 / (nn + 2), "0.25")

# ---------------------------------------------------------------- Q12 Bolfarine 2.4: P(X1=2, X2=0 | T=2) = theta/(theta+2)
ok(1 / 3, "0.3333"); ok(2 / 4, "0.5")

# ---------------------------------------------------------------- Q14 Bolfarine 3.6: MSE gap 1/n^2 (Monte Carlo)
rng = np.random.default_rng(3)
mu0, nn, R = 1.0, 5, 400000
xb = rng.normal(mu0, 1 / np.sqrt(nn), size=R)
mse_mle = np.mean((xb**2 - mu0**2) ** 2)
mse_ub = np.mean((xb**2 - 1 / nn - mu0**2) ** 2)
ok(4 * mu0**2 / nn + 3 / nn**2, "0.92"); ok(4 * mu0**2 / nn + 2 / nn**2, "0.88")
ok(mse_mle, "0.92"); ok(mse_ub, "0.88")

# ---------------------------------------------------------------- Q17 Morettin-Singer 6.15 (numerical identity check)
rng = np.random.default_rng(5)
x = rng.normal(size=30)
yy = 1 + 2 * x + rng.normal(size=30)
fit = sm.OLS(yy, sm.add_constant(x)).fit()
sqtot = np.sum((yy - yy.mean()) ** 2)
sqres = np.sum(fit.resid**2)
sqreg = np.sum((fit.fittedvalues - yy.mean()) ** 2)
assert abs(sqtot - sqres - sqreg) < 1e-9
assert abs(np.sum(fit.resid)) < 1e-9 and abs(np.sum(fit.resid * fit.fittedvalues)) < 1e-9

# ---------------------------------------------------------------- Q18 ISLP 13.1 (FWER of m true nulls)
alpha = 0.05
ok(10 * alpha, "0.5"); ok(1 - (1 - alpha) ** 2, "0.0975"); ok(2 * alpha, "0.10")
z_a = stats.norm.ppf(1 - alpha)
ok(z_a, "1.6449")


def fwer_two_onesided(rho):
    """1 - P(Z1 <= z_a, Z2 <= z_a) for a standard bivariate normal with correlation rho (quadrature)."""
    if abs(rho) < 1e-12:
        both = stats.norm.cdf(z_a) ** 2
    else:
        both = integrate.quad(lambda u: stats.norm.pdf(u) * stats.norm.cdf((z_a - rho * u) / np.sqrt(1 - rho**2)),
                              -np.inf, z_a, epsabs=1e-13, epsrel=1e-12)[0]
    return 1 - both


for rho, pr in [(0.9, "0.0681"), (0.5, "0.0878"), (0.0, "0.0975"), (-0.5, "0.0999"), (-0.9, "0.1000")]:
    ok(fwer_two_onesided(rho), pr)

# ---------------------------------------------------------------- Q19 ISLP 13.8 (fund managers, cherry-picking)
rng = np.random.default_rng(1)          # the book's code
n_f, m_f = 20, 100
Xf = rng.normal(size=(n_f, m_f))
tt = stats.ttest_1samp(Xf, 0)
pf = tt.pvalue
assert list(np.histogram(pf, bins=10, range=(0, 1))[0]) == [11, 12, 12, 13, 9, 14, 5, 5, 12, 7]
ok(98 / 10, "9.8"); ok(stats.chi2.sf(9.8, 9), "0.367")
ps = np.sort(pf)
for v, pr in zip(ps[:5], ["0.0008", "0.0096", "0.0229", "0.0355", "0.0503"]):
    ok(v, pr)
assert (pf < 0.05).sum() == 4
for meth in ["bonferroni", "holm", "fdr_bh"]:
    assert multipletests(pf, 0.05, method=meth)[0].sum() == 0
ok(0.05 / 100, "0.0005")
for j, pr in [(1, "0.0005"), (2, "0.0010"), (3, "0.0015"), (4, "0.0020")]:
    ok(0.05 * j / 100, pr)
assert ps[4] >= 0.05 * 5 / 100 and all(ps[j] >= 0.05 * (j + 1) / 100 for j in range(100))
assert pf.argmin() + 1 == 15
ok(tt.statistic[pf.argmin()], "-3.98")
best = np.argsort(-Xf.mean(0))[:10]
assert list(best + 1) == [28, 45, 81, 21, 12, 10, 9, 57, 68, 16]
ok(Xf.mean(0)[best[0]], "0.487"); ok(Xf.mean(0)[best[-1]], "0.288")
pbs = np.sort(pf[best])
for v, pr in zip(pbs[:4], ["0.0096", "0.0355", "0.0755", "0.0780"]):
    ok(v, pr)
for meth in ["bonferroni", "holm", "fdr_bh"]:
    assert multipletests(pf[best], 0.05, method=meth)[0].sum() == 0
assert all(pbs[j] >= 0.05 * (j + 1) / 10 for j in range(10))
# (f) the whole experiment repeated 10,000 times
rng = np.random.default_rng(2026)
R = 10000
hit_all = hit_holm = hit_bh = 0
for _ in range(10):
    Xr = rng.normal(size=(R // 10, n_f, m_f))
    mu_r = Xr.mean(1)
    pr_ = 2 * stats.t.sf(np.abs(mu_r / (Xr.std(1, ddof=1) / np.sqrt(n_f))), n_f - 1)
    hit_all += np.sum(pr_.min(1) <= 0.05 / m_f)
    top = np.sort(np.take_along_axis(pr_, np.argsort(-mu_r, 1)[:, :10], 1), 1)
    hit_holm += np.sum(top[:, 0] <= 0.05 / 10)
    hit_bh += np.sum((top <= 0.05 * np.arange(1, 11) / 10).any(1))
ok(hit_all / R, "0.0538"); ok(np.sqrt(hit_all / R * (1 - hit_all / R) / R), "0.0023")
ok(hit_holm / R, "0.2251"); ok(hit_bh / R, "0.2527")

# ---------------------------------------------------------------- Q20 original: four U(0, theta) estimators
for nn in range(1, 60):          # ranking of (c), in units of theta^2
    m1, m2, m3, m4 = (1 + 3 * nn) / (12 * nn), 2 / ((nn + 1) * (nn + 2)), 1 / (3 * nn), 1 / (nn * (nn + 2))
    if nn == 1:
        assert np.allclose([m1, m2, m3, m4], 1 / 3)
    elif nn == 2:
        assert np.isclose(m2, m3) and m4 < m2 < m1 and np.isclose(m4, 1 / 8) and np.isclose(m1, 7 / 24)
    else:
        assert m4 < m2 < m3 < m1
th, nn = 3.0, 10
c5 = (nn + 2) / (nn + 1)
E_th = [th / 2, nn * th / (nn + 1), th, th, c5 * nn * th / (nn + 1)]
V_x = nn * th**2 / ((nn + 1) ** 2 * (nn + 2))
SD_th = [np.sqrt(th**2 / (12 * nn)), np.sqrt(V_x), np.sqrt(th**2 / (3 * nn)), np.sqrt(th**2 / (nn * (nn + 2))), c5 * np.sqrt(V_x)]
MSE_th = [(1 + 3 * nn) * th**2 / (12 * nn), 2 * th**2 / ((nn + 1) * (nn + 2)), th**2 / (3 * nn), th**2 / (nn * (nn + 2)), th**2 / (nn + 1) ** 2]
assert np.allclose(MSE_th, [SD_th[k] ** 2 + (E_th[k] - th) ** 2 for k in range(5)])
ok(nn * (nn + 2) / (nn + 1) ** 2, "0.9917"); ok(MSE_th[0] / MSE_th[3], "31")
rng = np.random.default_rng(2026)
xu = rng.uniform(0, th, size=(100000, nn))
est = np.column_stack([xu.mean(1), xu.max(1), 2 * xu.mean(1), 1.1 * xu.max(1), 12 / 11 * xu.max(1)])
tab = [("1.499", "1.500", "0.274", "0.274", "2.3281", "2.3250"), ("2.728", "2.727", "0.249", "0.249", "0.1360", "0.1364"),
       ("2.998", "3.000", "0.548", "0.548", "0.3006", "0.3000"), ("3.001", "3.000", "0.274", "0.274", "0.0749", "0.0750"),
       ("2.976", "2.975", "0.271", "0.272", "0.0742", "0.0744")]
for k, (em, et, sm, st, mm, mt) in enumerate(tab):
    ok(est[:, k].mean(), em); ok(E_th[k], et); ok(est[:, k].std(ddof=1), sm); ok(SD_th[k], st)
    ok(((est[:, k] - th) ** 2).mean(), mm); ok(MSE_th[k], mt)

# ---------------------------------------------------------------- Q21 original: parametric bootstrap, failure for the max
for nn, pr in [(10, "0.6513"), (50, "0.6358"), (100, "0.6340")]:
    ok(1 - (1 - 1 / nn) ** nn, pr)
ok(1 - np.exp(-1), "0.6321")
nn, B, cc = 50, 10000, 51 / 50
rng = np.random.default_rng(2026)
xs50 = rng.uniform(0, 3, size=nn)
xmax = xs50.max(); t4 = cc * xmax
ok(xmax, "2.9009"); ok(t4, "2.9589")
xb = xs50[rng.integers(0, nn, size=(B, nn))]
ok(np.mean(xb.max(1) == xmax), "0.6405"); ok((cc * xb.max(1)).std(ddof=1), "0.0586")
xpb = rng.uniform(0, t4, size=(B, nn))
ok((cc * xpb.max(1)).std(ddof=1), "0.0583")
ok(t4 / np.sqrt(nn * (nn + 2)), "0.0580"); ok(3 / np.sqrt(nn * (nn + 2)), "0.0588")
ok(0.068 / 0.274, "0.25")
ok(1 - (nn / (nn + 1)) ** nn, "0.6285")
rng = np.random.default_rng(7)
cover = 0
for _ in range(1000):
    xr = rng.uniform(0, 3, size=nn)
    lo, hi = np.percentile(cc * xr[rng.integers(0, nn, size=(1000, nn))].max(1), [2.5, 97.5])
    cover += lo <= 3 <= hi
ok(cover / 1000, "0.617"); ok(np.sqrt(cover / 1000 * (1 - cover / 1000) / 1000), "0.015")
qhi, qlo = 0.975 ** (1 / nn), 0.025 ** (1 / nn)
ok(qhi, "0.99949"); ok(qlo, "0.92888")
ok(xmax / qhi, "2.9024"); ok(xmax / qlo, "3.1230")
assert abs(stats.beta.cdf(qhi, nn, 1) - stats.beta.cdf(qlo, nn, 1) - 0.95) < 1e-12

# ---------------------------------------------------------------- Q22 Bolfarine 6.11 (+ coal-mining change point)


def lr_two_poisson(sx, nx, sy, ny):
    """-2 log lambda for H0: theta1 = theta2 with two Poisson samples (sums sx, sy; sizes nx, ny)."""
    t0_ = (sx + sy) / (nx + ny)
    return 2 * (sx * np.log(sx / nx / t0_) + sy * np.log(sy / ny / t0_))


ok(3.8 / 5, "0.76"); ok(4.8 / 8, "0.6"); ok(8.6 / 13, "0.6615")
G_lit = lr_two_poisson(3.8, 5, 4.8, 8)
ok(G_lit, "0.1172"); ok(stats.chi2.sf(G_lit, 1), "0.7321"); ok(stats.chi2.ppf(0.95, 1), "3.841")
ok(57.4 / 13, "4.4154")
G_mean = lr_two_poisson(19.0, 5, 38.4, 8)
ok(G_mean, "0.7108"); ok(stats.chi2.sf(G_mean, 1), "0.3992")
ok(y.var(ddof=1) / y.mean(), "1.5916")
disp = (n - 1) * y.var(ddof=1) / y.mean()
ok(disp, "176.66"); ok(stats.chi2.sf(disp, n - 1), "0.00007")
G_k = np.array([lr_two_poisson(cs[k - 1], k, S - cs[k - 1], n - k) for k in range(1, n)])
kbest = int(G_k.argmax()) + 1
assert (kbest, 1850 + kbest, cs[kbest - 1], S - cs[kbest - 1]) == (41, 1891, 127, 64)
ok(127 / 41, "3.0976"); ok(64 / 71, "0.9014"); ok(G_k.max(), "69.99"); ok(G_k.max(), "70.0")
rng = np.random.default_rng(2026)
yb = rng.poisson(S / n, size=(10000, n))
cb = np.cumsum(yb, 1)
kk_ = np.arange(1, n)
Sb = cb[:, -1:]
with np.errstate(divide="ignore", invalid="ignore"):
    part = (np.where(cb[:, :-1] > 0, cb[:, :-1] * np.log(cb[:, :-1] / kk_), 0)
            + np.where(Sb - cb[:, :-1] > 0, (Sb - cb[:, :-1]) * np.log((Sb - cb[:, :-1]) / (n - kk_)), 0))
sup_G = 2 * (part.max(1) - Sb[:, 0] * np.log(Sb[:, 0] / n))
ok(np.quantile(sup_G, 0.95), "9.58"); assert sup_G.max() < G_k.max()

# ---------------------------------------------------------------- Q23 ISLP 6.8 (stepwise selection and lasso)
rng = np.random.default_rng(2026)
X68 = rng.normal(size=100)
eps68 = rng.normal(size=100)
P68 = np.column_stack([X68**k for k in range(1, 11)])
Y68 = 1 + 2 * X68 - 3 * X68**2 + 0.5 * X68**3 + eps68
Y7 = 1 + 0.5 * X68**7 + eps68


def ols_sub(yv, cols):
    """OLS of yv on an intercept and the powers in cols (0-based); returns (RSS, coefficients)."""
    A = np.column_stack([np.ones(100)] + [P68[:, j] for j in cols])
    coef = np.linalg.lstsq(A, yv, rcond=None)[0]
    r = yv - A @ coef
    return r @ r, coef


def stepwise(yv, direction):
    """Forward or backward stepwise path M_0..M_10 (lists of 0-based columns), each step minimising RSS."""
    if direction == "forward":
        cur, path = [], [[]]
        for _ in range(10):
            cur = cur + [min((j for j in range(10) if j not in cur), key=lambda j: ols_sub(yv, cur + [j])[0])]
            path.append(cur)
        return path
    cur, path = list(range(10)), [list(range(10))]
    for _ in range(10):
        drop = min(cur, key=lambda j: ols_sub(yv, [k for k in cur if k != j])[0])
        cur = [k for k in cur if k != drop]
        path.append(cur)
    return path[::-1]


def crit(yv, path):
    """C_p, BIC and adjusted R^2 (ISLP (6.2)-(6.4)) along a path, sigma^2 from the full model."""
    s2 = ols_sub(yv, range(10))[0] / (100 - 11)
    tss = np.sum((yv - yv.mean()) ** 2)
    out = []
    for cols in path:
        rss_, d = ols_sub(yv, cols)[0], len(cols)
        out.append(((rss_ + 2 * d * s2) / 100, (rss_ + np.log(100) * d * s2) / 100,
                    1 - rss_ / (100 - d - 1) / (tss / 99)))
    return s2, np.array(out)


s2_68, cf = crit(Y68, fw := stepwise(Y68, "forward"))
ok(s2_68, "1.4537")
assert [fw[d][-1] + 1 for d in range(1, 11)] == [2, 3, 1, 5, 6, 9, 8, 10, 7, 4]
for v, pr in zip(cf[:, 0], ["16.4365", "11.2013", "2.6443", "1.4131", "1.4403", "1.4552", "1.4841", "1.5058",
                            "1.5326", "1.5557", "1.5846"]):
    ok(v, pr)
assert cf[:, 0].argmin() == cf[:, 1].argmin() == cf[:, 2].argmax() == 3
coef = dict(zip([0] + [j + 1 for j in fw[3]], ols_sub(Y68, fw[3])[1]))
for k, pr in [(0, "1.1236"), (1, "1.7927"), (2, "-3.0366"), (3, "0.5396")]:
    ok(coef[k], pr)
_, cb_ = crit(Y68, bw := stepwise(Y68, "backward"))
assert [sorted(set(bw[d]) - set(bw[d - 1]))[0] + 1 for d in range(1, 11)] == [2, 1, 5, 7, 9, 8, 10, 6, 4, 3]
for v, pr in zip(cb_[:, 0], ["16.4365", "11.2013", "2.6493", "1.6376", "1.4870", "1.4863", "1.5016", "1.4983",
                             "1.5267", "1.5555", "1.5846"]):
    ok(v, pr)
assert cb_[:, 0].argmin() == 5 and cb_[:, 1].argmin() == 4 and cb_[:, 2].argmax() == 7
assert sorted(j + 1 for j in bw[4]) == [1, 2, 5, 7]
coefb = dict(zip([0] + [j + 1 for j in bw[5]], ols_sub(Y68, bw[5])[1]))
for k, pr in [(0, "1.1115"), (1, "2.0411"), (2, "-3.0175"), (5, "0.2763"), (7, "-0.0475"), (9, "0.0025")]:
    ok(coefb[k], pr)


def lasso_path(Z, yc):
    """Exact lasso path for (1/2n)||yc - Z b||^2 + lam ||b||_1 by LARS with the lasso modification.

    Z: standardised predictors (n x p); yc: centred response. Returns the knots lam_0 > ... >= 0
    and the coefficient vectors at the knots; the path is linear in lam between knots.
    """
    nz, p = Z.shape
    beta = np.zeros(p)
    c = Z.T @ yc
    lam = np.abs(c).max()
    act = [int(np.abs(c).argmax())]
    lams, betas = [lam / nz], [beta.copy()]
    while lam > 1e-12:
        d = np.linalg.solve(Z[:, act].T @ Z[:, act], np.sign(c[act]))
        a = Z.T @ (Z[:, act] @ d)
        gam, event = lam, None
        for j in set(range(p)) - set(act):
            for g in ((lam - c[j]) / (1 - a[j]), (lam + c[j]) / (1 + a[j])):
                if 1e-14 < g < gam:
                    gam, event = g, ("add", j)
        for i, j in enumerate(act):
            g = -beta[j] / d[i]
            if 1e-14 < g < gam:
                gam, event = g, ("drop", j)
        beta[act] += gam * d
        lam -= gam
        c = Z.T @ (yc - Z @ beta)
        lams.append(max(lam, 0) / nz); betas.append(beta.copy())
        if event is None:
            break
        if event[0] == "add":
            act.append(event[1])
        else:
            act.remove(event[1]); beta[event[1]] = 0.0
    return np.array(lams), np.array(betas)


def beta_at(lams, betas, lam):
    """Lasso coefficients at penalty lam, interpolated linearly between path knots."""
    if lam >= lams[0]:
        return np.zeros(betas.shape[1])
    k = np.searchsorted(-lams, -lam)
    w = (lams[k - 1] - lam) / (lams[k - 1] - lams[k])
    return betas[k - 1] + w * (betas[k] - betas[k - 1])


def lasso_cv(yv):
    """10-fold CV over 60 log-spaced lambdas; returns grid, CV curve, chosen index, coefficients."""
    mP, sP = P68.mean(0), P68.std(0)
    Z = (P68 - mP) / sP
    yc = yv - yv.mean()
    lams = np.abs(Z.T @ yc).max() / 100 * np.logspace(0, -4, 60)
    folds = np.random.default_rng(2026).permutation(100) % 10
    cvv = np.zeros(60)
    for k in range(10):
        tr, te = folds != k, folds == k
        m_, s_ = P68[tr].mean(0), P68[tr].std(0)
        kl, kb = lasso_path((P68[tr] - m_) / s_, yv[tr] - yv[tr].mean())
        for i, lam in enumerate(lams):
            cvv[i] += np.sum((yv[te] - yv[tr].mean() - ((P68[te] - m_) / s_) @ beta_at(kl, kb, lam)) ** 2) / 100
    i = int(cvv.argmin())
    kl, kb = lasso_path(Z, yc)
    bz = beta_at(kl, kb, lams[i])
    g = Z.T @ (yc - Z @ bz) / 100                     # KKT: |g_j| <= lam, = lam*sign(b_j) when b_j != 0
    assert np.all(np.abs(g) <= lams[i] + 1e-9) and np.allclose(g[bz != 0], lams[i] * np.sign(bz[bz != 0]))
    borig = bz / sP
    return lams, cvv, i, borig, yv.mean() - borig @ mP


lams68, cv68, i68, b68, b0_68 = lasso_cv(Y68)
ok(lams68[i68], "0.02122"); ok(cv68[i68], "1.4272")
assert list(np.flatnonzero(b68) + 1) == [1, 2, 3]
for v, pr in zip([b0_68, *b68[:3]], ["1.0865", "1.8037", "-2.9897", "0.5213"]):
    ok(v, pr)
cv_file = HERE / "data" / "L01-I68-lasso-cv.dat"
cv_text = "lam cv\n" + "".join(f"{l:.6g} {v:.6g}\n" for l, v in zip(lams68, cv68))
assert cv_file.read_text() == cv_text, f"{cv_file} is stale; regenerate it from lasso_cv(Y68)"
assert cv68.max() < 40                                    # the dashed marker spans [0, 40]
assert cv68[lams68 < 0.0011].min() > 14 and lams68[lams68 < 0.0011].max() > 0.00109
fw7 = stepwise(Y7, "forward")
_, c7 = crit(Y7, fw7)
assert fw7[1] == [6] and c7[:, 0].argmin() == 1
ok(c7[1, 0], "1.3727")
for v, pr in zip(ols_sub(Y7, [6])[1], ["1.1020", "0.5000"]):
    ok(v, pr)
lams7, cv7, i7, b7, b0_7 = lasso_cv(Y7)
ok(lams7[i7], "0.02958"); ok(cv7[i7], "1.4737")
assert list(np.flatnonzero(b7) + 1) == [1, 6, 7]
for v, pr in zip([b0_7, b7[0], b7[5], b7[6]], ["1.1002", "-0.0712", "0.0009", "0.4997"]):
    ok(v, pr)

# ---------------------------------------------------------------- Q24 Wooldridge 11.4 (random walk vs stable AR(1))
ok(np.sqrt(1000 / 1100), "0.9535"); ok(np.sqrt(10 / 15), "0.8165")
rng = np.random.default_rng(2026)
walks = rng.normal(size=(100000, 15)).cumsum(1)
ok(np.corrcoef(walks[:, 9], walks[:, 14])[0, 1], "0.8160"); ok(walks[:, 9].var(), "9.97")
rho = 0.9
v10, v15 = (1 - rho**20) / (1 - rho**2), (1 - rho**30) / (1 - rho**2)
ok(1 / (1 - rho**2), "5.2632"); ok(v10, "4.6233"); ok(v15, "5.0400")
ok(rho**5 * np.sqrt(v10 / v15), "0.5655"); ok(rho**5, "0.5905")

# ---------------------------------------------------------------- Q25 Tsay 8.5 (seasonal VAR, numerical illustration)
phi0 = np.array([1.0, 0.5])
P4 = np.array([[0.6, 0.2], [0.1, 0.5]])
Sig = np.array([[1.0, 0.3], [0.3, 0.5]])
assert np.allclose(sorted(np.linalg.eigvals(P4).real), [0.4, 0.7])
ok(np.linalg.det(P4), "0.28"); ok(np.trace(P4), "1.1")
mu = np.linalg.solve(np.eye(2) - P4, phi0)
G0 = np.linalg.solve(np.eye(4) - np.kron(P4, P4), Sig.ravel("F")).reshape(2, 2, order="F")
assert np.allclose(G0, P4 @ G0 @ P4.T + Sig)
assert np.allclose(G0, sum(np.linalg.matrix_power(P4, j) @ Sig @ np.linalg.matrix_power(P4, j).T for j in range(200)))
for v, pr in zip(mu, ["3.3333", "1.6667"]):
    ok(v, pr)
for v, pr in zip(G0.ravel(), ["1.8830", "0.7232", "0.7232", "0.7882"]):
    ok(v, pr)
for v, pr in zip((P4 @ G0).ravel(), ["1.2744", "0.5916", "0.5499", "0.4664"]):
    ok(v, pr)

print(f"All {N_OK} printed values reproduced.")
