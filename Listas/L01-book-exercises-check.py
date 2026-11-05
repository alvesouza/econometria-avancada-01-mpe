"""Reproduce and assert every number printed in Listas/lista-L01-book-exercises.tex.

Run from anywhere: ``python Listas/L01-book-exercises-check.py``. Each ``ok(value, "printed")``
asserts that ``value`` rounds to the printed string (tolerance = half a unit of the last printed
decimal), so a change in data, seed or library that moves a printed digit aborts the script.

Data: Wooldridge PHILLIPS via the ``wooldridge`` package (pip install wooldridge);
ISLP Boston from Listas/data/Boston.csv (provenance in Listas/data/README.md); coal-mining
disasters 1851-1962 typed below (Jarrett 1979, verified in .agent/notes/coal-mining-data.md).
Stochastic results (Gibbs sampler, bootstrap) use fixed NumPy seeds and are asserted at the
printed precision; another NumPy version may change the random stream and fail those lines.
"""
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.api as sm
import wooldridge
from scipy import special, stats

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

print(f"All {N_OK} printed values reproduced.")
