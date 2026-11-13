"""Reproduce and assert every number printed in Listas/lista-L08-book-exercises.tex (L08 book exercises).

Run from anywhere: python Listas/L08-book-exercises-check.py
Data: Listas/data/ (Tsay FTS 3e files, incl. L08-m-fsp6508.txt for T 12.4 and L08-m-gmsp5008.txt for T 3.9;
TRAFFIC2 via the `wooldridge` package). See Listas/data/README.md. MCMC sections (T 12.4 SV, Bayesian GARCH,
Student-t SV on simulated data) use fixed NumPy seeds. GARCH-type models (incl. GARCH-M, EGARCH, TGARCH) are fitted
by conditional MLE in NumPy/SciPy (the `arch` package is not installed).
Exits with AssertionError on the first mismatch; prints "ALL CHECKS PASSED" otherwise.
"""
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.api as sm
from scipy.linalg import cho_solve_banded, cholesky_banded, solve_banded
from scipy.optimize import minimize
from scipy.signal import lfilter
from scipy.special import gammaln
from scipy.stats import t as student_t
from statsmodels.stats.diagnostic import acorr_ljungbox, het_arch
from statsmodels.tools.numdiff import approx_hess3
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.stattools import acf, pacf

warnings.filterwarnings("ignore")
DATA = Path(__file__).resolve().parent / "data"
N_CHECKS = 0
DISCOVER = "--discover" in __import__("sys").argv  # report all mismatches instead of stopping


def check(name, value, expected, dec):
    """Assert that `value` rounds to the printed `expected` with `dec` decimals (half-unit tolerance plus slack)."""
    global N_CHECKS
    tol = 0.6 * 10.0 ** (-dec)
    if DISCOVER and abs(float(value) - expected) > tol:
        print(f"  MISMATCH {name}: computed {value:.{dec + 3}f}, printed {expected}")
        return
    assert abs(float(value) - expected) <= tol, f"{name}: computed {value:.{dec + 3}f}, printed {expected}"
    N_CHECKS += 1


def lb(x, lags, df=0):
    """Ljung-Box Q(m) statistics and p-values for the lags in `lags`; `df` fitted ARMA coefficients are subtracted."""
    out = acorr_ljungbox(x, lags=lags, model_df=df)
    return out.lb_stat.values, out.lb_pvalue.values


# ----------------------------------------------------------------------------------------------
# Conditional MLE for AR(lags)-GARCH(p,q) with optional exogenous variance regressors.
# ----------------------------------------------------------------------------------------------
def ged_logpdf(z, v):
    """Log density of the standardized GED, Tsay (2010) Eq. (3.10); v is the shape (v = 2 is Gaussian)."""
    lam = np.sqrt(2 ** (-2 / v) * np.exp(gammaln(1 / v) - gammaln(3 / v)))
    return np.log(v) - 0.5 * np.abs(z / lam) ** v - np.log(lam) - (1 + 1 / v) * np.log(2) - gammaln(1 / v)


def std_t_logpdf(z, v):
    """Log density of the standardized Student-t with v > 2 degrees of freedom, Tsay (2010) Eq. (3.7)."""
    return (gammaln((v + 1) / 2) - gammaln(v / 2) - 0.5 * np.log((v - 2) * np.pi)
            - (v + 1) / 2 * np.log1p(z ** 2 / (v - 2)))


def garch_filter(th, r, ar_lags, p, q, X, dist):
    """Residuals a_t and variances sigma_t^2 for parameter vector th = (mu, phi, omega, alpha, beta, gamma, shape).

    The sample starts at t0 = max(ar_lags); pre-sample a^2 and sigma^2 are set to mean(a^2) (fGarch-style).
    X (n x k) enters the variance equation linearly and contemporaneously, aligned with r.
    """
    nar, nx = len(ar_lags), (0 if X is None else X.shape[1])
    i = 0
    mu = th[i]; i += 1
    phi = th[i:i + nar]; i += nar
    om = th[i]; i += 1
    al = th[i:i + p]; i += p
    be = th[i:i + q]; i += q
    ga = th[i:i + nx]; i += nx
    shape = th[i] if dist != "norm" else None
    t0 = max(ar_lags) if nar else 0
    a = r[t0:] - mu - sum(phi[j] * r[t0 - l:len(r) - l] for j, l in enumerate(ar_lags))
    n = len(a)
    s0 = np.mean(a ** 2)
    xv = np.zeros(n) if nx == 0 else X[t0:] @ ga
    s2 = np.empty(n)
    for t in range(n):
        v = om + xv[t]
        for k in range(p):
            v += al[k] * (a[t - 1 - k] ** 2 if t - 1 - k >= 0 else s0)
        for k in range(q):
            v += be[k] * (s2[t - 1 - k] if t - 1 - k >= 0 else s0)
        s2[t] = v
    return a, s2, shape


def garch_nll(th, r, ar_lags, p, q, X, dist):
    """Negative conditional log-likelihood (Tsay 2010, Eqs. (3.6)-(3.10)); 1e10 if a variance is not positive."""
    a, s2, shape = garch_filter(th, r, ar_lags, p, q, X, dist)
    if np.any(s2 <= 0):
        return 1e10
    z = a / np.sqrt(s2)
    if dist == "norm":
        lp = -0.5 * np.log(2 * np.pi) - 0.5 * z ** 2
    elif dist == "ged":
        lp = ged_logpdf(z, shape)
    else:
        lp = std_t_logpdf(z, shape)
    return -np.sum(lp - 0.5 * np.log(s2))


def garch_fit(r, ar_lags=(), p=1, q=1, X=None, dist="norm"):
    """Fit AR(ar_lags)-GARCH(p,q) by conditional MLE (L-BFGS-B, then Nelder-Mead polish).

    r: returns; ar_lags: lags in the mean equation; p: ARCH order; q: GARCH order (0 gives ARCH(p));
    X: optional exogenous variance regressors; dist: 'norm', 'ged' or 't'.
    Returns dict with par, se (inverse numerical Hessian), llf, a, s2, z (standardized residuals).
    """
    r = np.asarray(r, float)
    ar_lags = list(ar_lags)
    nar, nx = len(ar_lags), (0 if X is None else X.shape[1])
    v = np.var(r)
    x0 = ([np.mean(r)] + [0.0] * nar + [0.1 * v if q else 0.5 * v] + [0.1 / p] * p + ([0.8 / q] * q if q else [])
          + [0.0] * nx + ([1.5] if dist == "ged" else [8.0] if dist == "t" else []))
    bounds = ([(None, None)] * (1 + nar) + [(1e-12, None)] + [(0, 1)] * (p + q) + [(None, None)] * nx
              + ([(0.3, 10)] if dist == "ged" else [(2.05, 100)] if dist == "t" else []))
    f = lambda th: garch_nll(th, r, ar_lags, p, q, X, dist)
    res = minimize(f, np.array(x0, float), method="L-BFGS-B", bounds=bounds, options=dict(maxiter=5000))
    res = minimize(f, res.x, method="Nelder-Mead", options=dict(maxiter=20000, xatol=1e-10, fatol=1e-10))
    se = np.sqrt(np.diag(np.linalg.inv(approx_hess3(res.x, f))))
    a, s2, _ = garch_filter(res.x, r, ar_lags, p, q, X, dist)
    return dict(par=res.x, se=se, llf=-res.fun, a=a, s2=s2, z=a / np.sqrt(s2))


# ==============================================================================================
# T 2.1  MA(1): R_t = a_t + 0.2 a_{t-1}, sigma_a = 0.025, a_100 = 0.01
# ==============================================================================================
th, sa, a100 = 0.2, 0.025, 0.01
check("2.1 fc1", th * a100, 0.002, 3)
check("2.1 fc2", 0.0, 0.0, 3)
check("2.1 sd1", sa, 0.025, 3)
check("2.1 sd2", sa * np.sqrt(1 + th ** 2), 0.025495, 6)
check("2.1 rho1", th / (1 + th ** 2), 0.19231, 5)

# ==============================================================================================
# T 2.2  r_t = 0.01 + 0.2 r_{t-2} + a_t, Var(a) = 0.02, r_100 = -0.01, r_99 = 0.02
# ==============================================================================================
c0, p2, va, r100, r99 = 0.01, 0.2, 0.02, -0.01, 0.02
check("2.2 mean", c0 / (1 - p2), 0.0125, 4)
check("2.2 var", va / (1 - p2 ** 2), 0.020833, 6)
check("2.2 fc1", c0 + p2 * r99, 0.014, 3)
check("2.2 fc2", c0 + p2 * r100, 0.008, 3)
check("2.2 sd", np.sqrt(va), 0.141421, 6)

# ==============================================================================================
# T 2.3  Monthly U.S. unemployment rate, ARIMA(2,1,2)x(1,0,1)_12
# ==============================================================================================
un = pd.read_csv(DATA / "m-unrate.txt", sep=r"\s+").Rate.values
check("2.3 n", len(un), 735, 0)
adf_u = sm.tsa.adfuller(un, regression="c", autolag="AIC")
print(f"[2.3] ADF level: t={adf_u[0]:.3f} p={adf_u[1]:.3f} lags={adf_u[2]}")
check("2.3 adf t", adf_u[0], -2.783, 3)
check("2.3 adf p", adf_u[1], 0.061, 3)
m23 = ARIMA(un, order=(2, 1, 2), seasonal_order=(1, 0, 1, 12)).fit()
print("[2.3] params", dict(zip(m23.param_names, m23.params.round(4))), "se", m23.bse.round(4))
for k, (e, s) in enumerate(zip([1.1701, -0.3104, -1.1809, 0.4923, 0.5505, -0.8134],
                               [0.1231, 0.1194, 0.1193, 0.1002, 0.0673, 0.0468])):
    check(f"2.3 par{k}", m23.params[k], e, 4)
    check(f"2.3 se{k}", m23.bse[k], s, 4)
check("2.3 sigma2", m23.params[6], 0.0369, 4)
q23, pv23 = lb(m23.resid[1:], [12, 24], df=6)
print("[2.3] LB", q23.round(2), pv23.round(3))
check("2.3 Q12", q23[0], 12.52, 2); check("2.3 p12", pv23[0], 0.051, 3)
check("2.3 Q24", q23[1], 26.43, 2); check("2.3 p24", pv23[1], 0.090, 3)
ph1, ph2 = m23.params[0], m23.params[1]
disc = ph1 ** 2 + 4 * ph2
print(f"[2.3] discriminant phi1^2+4phi2 = {disc:.4f}; inverse roots", np.roots([1, -ph1, -ph2]).round(4))
check("2.3 phi1^2", ph1 ** 2, 1.3691, 4)
check("2.3 disc", disc, 0.1277, 4)
inv = np.sort(np.roots([1, -ph1, -ph2]).real)[::-1]
check("2.3 root1", inv[0], 0.7637, 4); check("2.3 root2", inv[1], 0.4064, 4)
f23 = m23.get_forecast(4)
print("[2.3] forecasts", f23.predicted_mean.round(3), f23.se_mean.round(3))
for k, (e, s) in enumerate(zip([8.844, 9.023, 9.151, 9.257], [0.192, 0.270, 0.350, 0.437])):
    check(f"2.3 fc{k}", f23.predicted_mean[k], e, 3)
    check(f"2.3 fcse{k}", f23.se_mean[k], s, 3)

# ==============================================================================================
# T 2.4  CRSP deciles: Q(12) for Decile 2 and 10; model for Decile 2 with a January dummy
# ==============================================================================================
dec = pd.read_csv(DATA / "m-deciles08.txt", sep=r"\s+")
check("2.4 n", len(dec), 468, 0)
for col, eq, ep in [("CAP2RET", 55.74, 0.0000), ("CAP10RET", 10.69, 0.556)]:
    qq, pp = lb(dec[col].values, [12])
    print(f"[2.4] {col} Q(12)={qq[0]:.2f} p={pp[0]:.4f}")
    check(f"2.4 Q12 {col}", qq[0], eq, 2)
    check(f"2.4 p12 {col}", pp[0], ep, 3 if ep > 0 else 4)
d2 = dec.CAP2RET.values
acf2 = acf(d2, nlags=24)
print("[2.4] ACF D2 lags 1,12,24", acf2[[1, 12, 24]].round(3), "2/sqrt(T)", round(2 / np.sqrt(len(d2)), 3))
check("2.4 acf1", acf2[1], 0.204, 3); check("2.4 acf12", acf2[12], 0.231, 3); check("2.4 acf24", acf2[24], 0.130, 3)
check("2.4 band", 2 / np.sqrt(len(d2)), 0.092, 3)
ms = ARIMA(d2, order=(1, 0, 0), seasonal_order=(1, 0, 1, 12), trend="c").fit()
print("[2.4] seasonal ARMA", dict(zip(ms.param_names, ms.params.round(4))))
check("2.4 sar phi1", ms.params[1], 0.1981, 4); check("2.4 sar Phi", ms.params[2], 0.9894, 4)
check("2.4 sar Theta", ms.params[3], -0.9398, 4)
jan = (dec.date.astype(str).str[4:6] == "01").astype(float).values
m24 = ARIMA(d2, exog=jan, order=(0, 0, 1), trend="c").fit()
print("[2.4] Jan+MA(1)", dict(zip(m24.param_names, m24.params.round(5))), "se", m24.bse.round(5))
for k, (e, s) in enumerate(zip([0.00388, 0.07891, 0.23304], [0.00395, 0.00789, 0.03681])):
    check(f"2.4 par{k}", m24.params[k], e, 5); check(f"2.4 se{k}", m24.bse[k], s, 5)
check("2.4 sigma_a", np.sqrt(m24.params[3]), 0.0597, 4)
q24, pv24 = lb(m24.resid, [12, 24], df=1)
print("[2.4] LB resid", q24.round(2), pv24.round(3))
check("2.4 Q12r", q24[0], 14.50, 2); check("2.4 p12r", pv24[0], 0.207, 3)
check("2.4 Q24r", q24[1], 23.65, 2); check("2.4 p24r", pv24[1], 0.424, 3)
aT = m24.resid[-1]
print(f"[2.4] last residual a_T = {aT:.5f}")
check("2.4 aT", aT, -0.00406, 5)
ex = np.zeros(12); ex[0] = 1.0
f24 = m24.get_forecast(12, exog=ex)
print("[2.4] fc", f24.predicted_mean.round(5), f24.se_mean.round(5))
check("2.4 fc1", f24.predicted_mean[0], 0.08184, 5); check("2.4 fc2", f24.predicted_mean[1], 0.00388, 5)
check("2.4 se1", f24.se_mean[0], 0.05965, 5); check("2.4 se2", f24.se_mean[1], 0.06125, 5)
assert np.allclose(f24.predicted_mean[1:], m24.params[0]) and np.allclose(f24.se_mean[1:], f24.se_mean[1])

# ==============================================================================================
# T 2.5  IBM daily simple returns: ACF of |R_t| up to lag 100
# ==============================================================================================
ibm = pd.read_csv(DATA / "d-ibm3dx7008.txt", sep=r"\s+")
absr = np.abs(ibm.rtn.values)
check("2.5 n", len(absr), 9845, 0)
r100 = acf(absr, nlags=100)
band = 2 / np.sqrt(len(absr))
print("[2.5] ACF lags 1,2,5,10,20,50,100", r100[[1, 2, 5, 10, 20, 50, 100]].round(4), "min", r100[1:].min().round(4))
for lag, e in zip([1, 2, 5, 10, 20, 50, 100], [0.1947, 0.1638, 0.1723, 0.1311, 0.1379, 0.1089, 0.0786]):
    check(f"2.5 acf{lag}", r100[lag], e, 4)
check("2.5 min", r100[1:].min(), 0.0607, 4); check("2.5 band", band, 0.0202, 4)
check("2.5 n>band", (r100[1:] > band).sum(), 100, 0)
slope, icpt = np.polyfit(np.log(np.arange(1, 101)), np.log(r100[1:]), 1)
print(f"[2.5] log-log slope {slope:.4f}, d = {(slope + 1) / 2:.4f}; rho1^100 = {r100[1] ** 100:.2e}")
check("2.5 slope", slope, -0.2188, 4); check("2.5 d", (slope + 1) / 2, 0.3906, 4)

# ==============================================================================================
# T 2.6  power6: airline model ARIMA(0,1,1)x(0,1,1)_12
# ==============================================================================================
pw = np.loadtxt(DATA / "power6.txt")
check("2.6 n", len(pw), 264, 0)
dds = np.diff(pw)[12:] - np.diff(pw)[:-12]
a26 = acf(dds, nlags=24)
print("[2.6] ACF of (1-B)(1-B^12)x lags 1,12,13", a26[[1, 12, 13]].round(3), "band", round(2 / np.sqrt(len(dds)), 3))
check("2.6 acf1", a26[1], -0.332, 3); check("2.6 acf12", a26[12], -0.484, 3); check("2.6 acf13", a26[13], 0.206, 3)
check("2.6 band", 2 / np.sqrt(len(dds)), 0.126, 3)
m26 = ARIMA(pw, order=(0, 1, 1), seasonal_order=(0, 1, 1, 12)).fit()
print("[2.6] params", m26.params.round(4), "se", m26.bse.round(4))
check("2.6 theta", m26.params[0], -0.4874, 4); check("2.6 Theta", m26.params[1], -0.9572, 4)
check("2.6 se theta", m26.bse[0], 0.0574, 4); check("2.6 se Theta", m26.bse[1], 0.1301, 4)
check("2.6 sigma_a", np.sqrt(m26.params[2]), 0.0184, 4)
q26, pv26 = lb(m26.resid[13:], [12, 24], df=2)
print("[2.6] LB", q26.round(2), pv26.round(3))
check("2.6 Q12", q26[0], 12.85, 2); check("2.6 p12", pv26[0], 0.232, 3)
check("2.6 Q24", q26[1], 26.10, 2); check("2.6 p24", pv26[1], 0.247, 3)
f26 = m26.get_forecast(24)
FC26 = [9.8827, 9.8675, 9.8740, 9.8931, 9.9221, 10.0066, 10.0465, 10.0635, 10.0729, 10.0070, 9.9520, 9.9291,
        9.9115, 9.8963, 9.9029, 9.9219, 9.9509, 10.0355, 10.0753, 10.0923, 10.1017, 10.0358, 9.9808, 9.9579]
SE26 = [0.0185, 0.0208, 0.0228, 0.0247, 0.0265, 0.0281, 0.0297, 0.0311, 0.0326, 0.0339, 0.0352, 0.0365,
        0.0380, 0.0392, 0.0405, 0.0417, 0.0429, 0.0441, 0.0452, 0.0463, 0.0473, 0.0484, 0.0494, 0.0504]
print("[2.6] fc", f26.predicted_mean.round(4).tolist()); print("[2.6] se", f26.se_mean.round(4).tolist())
for k in range(24):
    check(f"2.6 fc{k + 1}", f26.predicted_mean[k], FC26[k], 4)
    check(f"2.6 se{k + 1}", f26.se_mean[k], SE26[k], 4)

# ==============================================================================================
# W 18.C13  TRAFFIC2: Dickey-Fuller tests for ltotacc and prcfat
# ==============================================================================================
import wooldridge  # noqa: E402

tr = wooldridge.data("traffic2")
check("C13 n", len(tr), 108, 0)


def df_reg(y, lags, trend):
    """OLS Dickey-Fuller regression of dy_t on const, y_{t-1}, dy_{t-1..lags} (and t), as in W Eq. (18.21)."""
    y = pd.Series(np.asarray(y, float))
    dy = y.diff()
    X = pd.DataFrame({"ylag": y.shift(1)})
    for j in range(1, lags + 1):
        X[f"dl{j}"] = dy.shift(j)
    if trend:
        X["t"] = np.arange(1, len(y) + 1)
    D = pd.concat([dy.rename("dy"), sm.add_constant(X)], axis=1).dropna()
    return sm.OLS(D.dy, D.drop(columns="dy")).fit()


C13 = {  # (variable, lags, trend): (n, coef on y_{t-1}, se, t, [extra checks])
    ("ltotacc", 0, 0): (107, -0.1923, 0.0581, -3.31),
    ("ltotacc", 2, 0): (105, -0.0850, 0.0566, -1.50),
    ("ltotacc", 2, 1): (105, -0.4253, 0.1160, -3.67),
    ("prcfat", 0, 0): (107, -0.2906, 0.0689, -4.22),
    ("prcfat", 2, 0): (105, -0.3837, 0.0809, -4.74),
    ("prcfat", 2, 1): (105, -0.4581, 0.0866, -5.29),
}
reg = {}
for (v, L, T), (n, b, s, tv) in C13.items():
    m = df_reg(tr[v], L, T)
    reg[(v, L, T)] = m
    print(f"[C13] {v} lags={L} trend={T}: n={int(m.nobs)} theta={m.params['ylag']:.4f} se={m.bse['ylag']:.4f} "
          f"t={m.tvalues['ylag']:.2f}")
    check(f"C13 n {v}{L}{T}", m.nobs, n, 0)
    check(f"C13 b {v}{L}{T}", m.params["ylag"], b, 4)
    check(f"C13 se {v}{L}{T}", m.bse["ylag"], s, 4)
    check(f"C13 t {v}{L}{T}", m.tvalues["ylag"], tv, 2)
m = reg[("ltotacc", 2, 0)]
print("[C13] ltotacc lags: t", m.tvalues[["dl1", "dl2"]].round(2).values)
check("C13 dl1 t", m.tvalues["dl1"], -4.75, 2); check("C13 dl2 t", m.tvalues["dl2"], -3.06, 2)
m = reg[("ltotacc", 2, 1)]
print("[C13] trend coef", round(m.params["t"], 4), "t", round(m.tvalues["t"], 2))
check("C13 trend b", m.params["t"], 0.0013, 4); check("C13 trend t", m.tvalues["t"], 3.31, 2)

# ==============================================================================================
# T 3.3 / 3.4  likelihood formulas: hand formula vs library densities at a random point
# ==============================================================================================
rng = np.random.default_rng(8)
rr = rng.standard_normal(50) * 0.05
mu_, ph_, a0_, a1_, b1_, nu_ = 0.001, 0.1, 1e-4, 0.1, 0.8, 7.0
aa = rr[1:] - mu_ - ph_ * rr[:-1]
s2 = np.empty(len(aa)); s2[0] = np.var(rr)
for t in range(1, len(aa)):
    s2[t] = a0_ + a1_ * aa[t - 1] ** 2 + b1_ * s2[t - 1]
ll_hand_n = -0.5 * np.sum(np.log(2 * np.pi) + np.log(s2) + aa ** 2 / s2)
ll_lib_n = np.sum(-0.5 * np.log(2 * np.pi * s2) - aa ** 2 / (2 * s2))
assert abs(ll_hand_n - ll_lib_n) < 1e-10
ll_hand_t = np.sum(gammaln((nu_ + 1) / 2) - gammaln(nu_ / 2) - 0.5 * np.log((nu_ - 2) * np.pi)
                   - 0.5 * np.log(s2) - (nu_ + 1) / 2 * np.log1p(aa ** 2 / ((nu_ - 2) * s2)))
scale = np.sqrt(s2 * (nu_ - 2) / nu_)  # a_t = sigma_t eps_t with Var(eps)=1  <=>  a_t / scale ~ t_nu
ll_lib_t = np.sum(student_t.logpdf(aa / scale, nu_) - np.log(scale))
assert abs(ll_hand_t - ll_lib_t) < 1e-10
N_CHECKS += 2

# ==============================================================================================
# T 3.6  Merck monthly log returns
# ==============================================================================================
mrk = pd.read_csv(DATA / "m-mrk4608.txt", sep=r"\s+")
rm = np.log1p(mrk.mrk.values)
check("3.6 n", len(rm), 751, 0)
acm = acf(rm, nlags=12)
print("[3.6] ACF lags 1..12", acm[1:].round(3), "band", round(2 / np.sqrt(len(rm)), 3))
check("3.6 acf1", acm[1], -0.078, 3); check("3.6 acf8", acm[8], 0.104, 3)
check("3.6 band", 2 / np.sqrt(len(rm)), 0.073, 3)
qm, pm = lb(rm, [6, 12])
print("[3.6] LB r", qm.round(2), pm.round(4))
check("3.6 Q6", qm[0], 10.19, 2); check("3.6 p6", pm[0], 0.117, 3)
check("3.6 Q12", qm[1], 27.24, 2); check("3.6 p12", pm[1], 0.007, 3)
m36 = ARIMA(rm, order=([1, 8], 0, 0), trend="c").fit()
print("[3.6] AR(1,8)", dict(zip(m36.param_names, m36.params.round(4))), "se", m36.bse.round(4))
check("3.6 c", m36.params[0], 0.0108, 4); check("3.6 phi1", m36.params[1], -0.0826, 4)
check("3.6 phi8", m36.params[2], 0.1094, 4); check("3.6 se1", m36.bse[1], 0.0339, 4)
check("3.6 se8", m36.bse[2], 0.0347, 4)
qe, pe = lb(m36.resid, [12], df=2)
print("[3.6] LB resid Q(12)", qe.round(2), pe.round(3))
check("3.6 Q12e", qe[0], 14.03, 2); check("3.6 p12e", pe[0], 0.172, 3)
e36 = m36.resid
qs, ps = lb(e36 ** 2, [6, 12])
print("[3.6] LB squared resid", qs.round(2), ps.round(4))
check("3.6 Q6s", qs[0], 17.81, 2); check("3.6 p6s", ps[0], 0.0067, 4)
check("3.6 Q12s", qs[1], 29.82, 2); check("3.6 p12s", ps[1], 0.0030, 4)
pe2 = pacf(e36 ** 2, nlags=12)
print("[3.6] PACF e^2 lags 1..6", pe2[1:7].round(3))
check("3.6 pacf1", pe2[1], 0.056, 3); check("3.6 pacf2", pe2[2], 0.056, 3); check("3.6 pacf3", pe2[3], 0.110, 3)
check("3.6 pacf4", pe2[4], 0.045, 3)
g36 = garch_fit(rm, ar_lags=[1, 8], p=3, q=0)
print("[3.6] AR(1,8)-ARCH(3)", g36["par"].round(5), "se", g36["se"].round(5), "llf", round(g36["llf"], 2))
for k, (e, s) in enumerate(zip([0.01170, -0.08134, 0.10145, 0.00404, 0.02741, 0.05283, 0.09608],
                               [0.00265, 0.03706, 0.03715, 0.00033, 0.03856, 0.03560, 0.04142])):
    check(f"3.6 g par{k}", g36["par"][k], e, 5); check(f"3.6 g se{k}", g36["se"][k], s, 5)
qz, pz = lb(g36["z"], [12], df=2); qz2, pz2 = lb(g36["z"] ** 2, [6, 12])
print("[3.6] LB z", qz.round(2), pz.round(3), "z^2", qz2.round(2), pz2.round(3))
check("3.6 Qz", qz[0], 14.14, 2); check("3.6 pz", pz[0], 0.167, 3)
check("3.6 Qz2 6", qz2[0], 1.64, 2); check("3.6 pz2 6", pz2[0], 0.949, 3)
check("3.6 Qz2 12", qz2[1], 11.20, 2); check("3.6 pz2 12", pz2[1], 0.512, 3)

# ==============================================================================================
# T 3.11  GM daily percentage log returns 1999-2008
# ==============================================================================================
gs = pd.read_csv(DATA / "d-gmsp9908.txt", sep=r"\s+")
check("3.11 n", len(gs), 2515, 0)
gm = 100 * np.log1p(gs.gm.values)
eg = gm - gm.mean()
lm = het_arch(eg, nlags=10)
qg2, pg2 = lb(eg ** 2, [10])
print(f"[3.11] ARCH-LM(10)={lm[0]:.1f} p={lm[1]:.2e}  F={lm[2]:.2f}  Q2(10)={qg2[0]:.1f}")
check("3.11 LM", lm[0], 625.2, 1); check("3.11 F", lm[2], 82.95, 2); check("3.11 Q2", qg2[0], 898.1, 1)
assert lm[1] < 1e-100
pg = pacf(eg ** 2, nlags=10)
PG = [0.193, 0.397, -0.013, -0.128, 0.139, 0.083, 0.089, 0.030, -0.000, 0.118]
print("[3.11] PACF a^2", pg[1:].round(3))
for k in range(10):
    check(f"3.11 pacf{k + 1}", pg[k + 1], PG[k], 3)
qgr, pgr = lb(gm, [10])
print(f"[3.11] Q(10) of r: {qgr[0]:.2f} p={pgr[0]:.4f}")
check("3.11 Qr", qgr[0], 28.40, 2); check("3.11 pr", pgr[0], 0.0016, 4)
g11n = garch_fit(gm)
print("[3.11] GARCH(1,1)-N", g11n["par"].round(4), "se", g11n["se"].round(4), "llf", round(g11n["llf"], 2))
for k, (e, s) in enumerate(zip([0.0245, 0.0942, 0.0701, 0.9207], [0.0437, 0.0208, 0.0091, 0.0097])):
    check(f"3.11 n par{k}", g11n["par"][k], e, 4); check(f"3.11 n se{k}", g11n["se"][k], s, 4)
check("3.11 n llf", g11n["llf"], -5853.30, 2)
check("3.11 n persist", g11n["par"][2] + g11n["par"][3], 0.9908, 4)
qz, pz = lb(g11n["z"], [10, 20]); qz2, pz2 = lb(g11n["z"] ** 2, [10, 20])
print("[3.11] LB z", qz.round(2), pz.round(3), "z^2", qz2.round(2), pz2.round(3))
check("3.11 n Qz10", qz[0], 12.78, 2); check("3.11 n pz10", pz[0], 0.236, 3)
check("3.11 n Qz20", qz[1], 26.92, 2); check("3.11 n pz20", pz[1], 0.137, 3)
check("3.11 n Qzz10", qz2[0], 1.79, 2); check("3.11 n pzz10", pz2[0], 0.998, 3)
check("3.11 n Qzz20", qz2[1], 9.01, 2); check("3.11 n pzz20", pz2[1], 0.983, 3)
zn = g11n["z"]
kurt = np.mean((zn - zn.mean()) ** 4) / np.var(zn) ** 2
print(f"[3.11] kurtosis of z = {kurt:.2f}")
check("3.11 kurt", kurt, 8.89, 2)
g11g = garch_fit(gm, dist="ged")
print("[3.11] GARCH(1,1)-GED", g11g["par"].round(4), "se", g11g["se"].round(4), "llf", round(g11g["llf"], 2))
for k, (e, s) in enumerate(zip([-0.0444, 0.0542, 0.0678, 0.9286, 1.2521], [0.0408, 0.0212, 0.0113, 0.0118, 0.0432])):
    check(f"3.11 g par{k}", g11g["par"][k], e, 4); check(f"3.11 g se{k}", g11g["se"][k], s, 4)
check("3.11 g llf", g11g["llf"], -5747.55, 2)
qz, pz = lb(g11g["z"], [10, 20]); qz2, pz2 = lb(g11g["z"] ** 2, [10, 20])
print("[3.11] GED LB z", qz.round(2), pz.round(3), "z^2", qz2.round(2), pz2.round(3))
check("3.11 g Qz10", qz[0], 13.09, 2); check("3.11 g pz10", pz[0], 0.219, 3)
check("3.11 g Qzz10", qz2[0], 1.86, 2); check("3.11 g pzz10", pz2[0], 0.997, 3)
check("3.11 g tstat v", (g11g["par"][4] - 2) / g11g["se"][4], -17.33, 2)

# ==============================================================================================
# T 3.12  S&P daily percentage simple returns: AR(2)-GARCH(1,1) and 1-4 step forecasts
# ==============================================================================================
sp = 100 * gs.sp.values
es = sp - sp.mean()
lms = het_arch(es, nlags=10)
qs2, _ = lb(es ** 2, [10])
print(f"[3.12] ARCH-LM(10)={lms[0]:.1f} F={lms[2]:.2f} Q2(10)={qs2[0]:.1f}")
check("3.12 LM", lms[0], 711.2, 1); check("3.12 F", lms[2], 98.88, 2); check("3.12 Q2", qs2[0], 2097.7, 1)
asp = acf(sp, nlags=2)
qsr, psr = lb(sp, [10])
print("[3.12] ACF r lags 1,2", asp[1:].round(3), "Q(10)", qsr.round(2), psr)
check("3.12 acf1", asp[1], -0.077, 3); check("3.12 acf2", asp[2], -0.091, 3); check("3.12 Qr", qsr[0], 57.06, 2)
g12 = garch_fit(sp, ar_lags=[1, 2])
mu, f1, f2, om, al, be = g12["par"]
print("[3.12] AR(2)-GARCH(1,1)", g12["par"].round(5), "se", g12["se"].round(5), "llf", round(g12["llf"], 2))
for k, (e, s) in enumerate(zip([0.0357, -0.0589, -0.0419, 0.0100, 0.0714, 0.9235],
                               [0.0179, 0.0210, 0.0208, 0.0031, 0.0094, 0.0101])):
    check(f"3.12 par{k}", g12["par"][k], e, 4); check(f"3.12 se{k}", g12["se"][k], s, 4)
qz, pz = lb(g12["z"], [10, 20], df=2); qz2, pz2 = lb(g12["z"] ** 2, [10, 20])
print("[3.12] LB z", qz.round(2), pz.round(3), "z^2", qz2.round(2), pz2.round(3))
check("3.12 Qz10", qz[0], 8.57, 2); check("3.12 pz10", pz[0], 0.380, 3)
check("3.12 Qz20", qz[1], 23.84, 2); check("3.12 pz20", pz[1], 0.160, 3)
check("3.12 Qzz10", qz2[0], 14.65, 2); check("3.12 pzz10", pz2[0], 0.145, 3)
check("3.12 Qzz20", qz2[1], 20.31, 2); check("3.12 pzz20", pz2[1], 0.438, 3)
rT, rT1, aT, s2T = sp[-1], sp[-2], g12["a"][-1], g12["s2"][-1]
print(f"[3.12] r_T={rT:.4f} r_T-1={rT1:.4f} a_T={aT:.4f} sigma2_T={s2T:.4f}")
check("3.12 rT", rT, 1.4158, 4); check("3.12 rT1", rT1, 2.4407, 4)
check("3.12 aT", aT, 1.5076, 4); check("3.12 s2T", s2T, 7.9263, 4)
rf = [rT1, rT]
for h in range(4):
    rf.append(mu + f1 * rf[-1] + f2 * rf[-2])
rf = rf[2:]
s2f = [om + al * aT ** 2 + be * s2T]
for h in range(3):
    s2f.append(om + (al + be) * s2f[-1])
print("[3.12] return fc", np.round(rf, 4), "vol fc", np.sqrt(s2f).round(4), "var fc", np.round(s2f, 4))
for k, (e, ev, es_) in enumerate(zip([-0.1499, -0.0148, 0.0429, 0.0338], [7.4920, 7.4634, 7.4349, 7.4065],
                                     [2.7372, 2.7319, 2.7267, 2.7215])):
    check(f"3.12 rfc{k}", rf[k], e, 4); check(f"3.12 vfc{k}", s2f[k], ev, 4); check(f"3.12 sfc{k}", np.sqrt(s2f[k]), es_, 4)
check("3.12 persist", al + be, 0.9949, 4)
for k, e in enumerate([0.03570, -0.05888, -0.04190, 0.00997, 0.07135, 0.92350]):
    check(f"3.12 par5 {k}", g12["par"][k], e, 5)
check("3.12 alpha+beta 5", al + be, 0.99485, 5)
check("3.12 uncond var", om / (1 - al - be), 1.93, 2)

# ==============================================================================================
# T 3.14  S&P AR(5) (lags 3,5)-GARCH(1,1)-GED -> spvol; GM GARCH(1,1)-GED with spvol in variance
# ==============================================================================================
spl = 100 * np.log1p(gs.sp.values)
g14a = garch_fit(spl, ar_lags=[3, 5], dist="ged")
print("[3.14a] S&P", g14a["par"].round(4), "se", g14a["se"].round(4), "llf", round(g14a["llf"], 2))
for k, (e, s) in enumerate(zip([0.0444, -0.0094, -0.0414, 0.0079, 0.0713, 0.9258, 1.4964],
                               [0.0175, 0.0207, 0.0209, 0.0033, 0.0108, 0.0113, 0.0603])):
    check(f"3.14a par{k}", g14a["par"][k], e, 4); check(f"3.14a se{k}", g14a["se"][k], s, 4)
qz, pz = lb(g14a["z"], [10], df=2); qz2, pz2 = lb(g14a["z"] ** 2, [10])
print("[3.14a] LB z", qz.round(2), pz.round(3), "z^2", qz2.round(2), pz2.round(3))
check("3.14a Qz", qz[0], 12.80, 2); check("3.14a Qzz", qz2[0], 11.49, 2)
spvol = np.sqrt(g14a["s2"])
g = gm[5:]
g14b = garch_fit(g, X=spvol[:, None], dist="ged")
g14o = garch_fit(g, dist="ged")
print("[3.14b] GM+spvol", g14b["par"].round(4), "se", g14b["se"].round(4), "llf", round(g14b["llf"], 2))
print("[3.14b] GM base ", g14o["par"].round(4), "se", g14o["se"].round(4), "llf", round(g14o["llf"], 2))
for k, (e, s) in enumerate(zip([-0.0485, 0.0214, 0.0677, 0.9254, 0.0499, 1.2478],
                               [0.0395, 0.0355, 0.0114, 0.0127, 0.0474, 0.0430])):
    check(f"3.14b par{k}", g14b["par"][k], e, 4); check(f"3.14b se{k}", g14b["se"][k], s, 4)
check("3.14b llf", g14b["llf"], -5733.16, 2); check("3.14b llf0", g14o["llf"], -5733.79, 2)
check("3.14b t gamma", g14b["par"][4] / g14b["se"][4], 1.05, 2)
check("3.14b LR", 2 * (g14b["llf"] - g14o["llf"]), 1.28, 2)
qz, pz = lb(g14b["z"], [10, 20]); qz2, pz2 = lb(g14b["z"] ** 2, [10, 20])
print("[3.14b] LB z", qz.round(2), pz.round(3), "z^2", qz2.round(2), pz2.round(3))
check("3.14b Qz10", qz[0], 12.44, 2); check("3.14b pz10", pz[0], 0.257, 3)
check("3.14b Qzz10", qz2[0], 1.87, 2); check("3.14b pzz10", pz2[0], 0.997, 3)
check("3.14b mean spvol", spvol.mean(), 1.1749, 4)
check("3.14b contrib", g14b["par"][4] * spvol.mean(), 0.0586, 4)

# ==============================================================================================
# W 12.4  ARCH(1) errors are serially uncorrelated but not independent (simulation illustration)
# ==============================================================================================
rng = np.random.default_rng(124)
n, a0, a1 = 200_000, 1.0, 0.5
u = np.empty(n); h = a0 / (1 - a1); u[0] = np.sqrt(h) * rng.standard_normal()
e = rng.standard_normal(n)
for t in range(1, n):
    u[t] = np.sqrt(a0 + a1 * u[t - 1] ** 2) * e[t]
r_u, r_u2 = acf(u, nlags=1)[1], acf(u ** 2, nlags=1)[1]
print(f"[W12.4] corr(u_t,u_t-1)={r_u:.3f}, corr(u_t^2,u_t-1^2)={r_u2:.3f}")
check("W12.4 r_u", r_u, 0.00, 2)
assert 0.3 < r_u2 < 0.6
N_CHECKS += 1

# ==============================================================================================
# Extra numbers quoted in the tex prose and hand-arithmetic lines
# ==============================================================================================
check("2.3 phi1 5d", ph1, 1.17009, 5); check("2.3 phi2 5d", ph2, -0.31036, 5)
check("2.3 phi1^2 5d", 1.17009 ** 2, 1.36911, 5); check("2.3 4phi2", 4 * -0.31036, -1.24144, 5)
check("2.3 disc 5d", 1.36911 - 1.24144, 0.12767, 5); check("2.3 sqrt disc", np.sqrt(0.12767), 0.35731, 5)
check("2.3 last x", un[-1], 8.6, 1)
check("2.4 p D2 x1e7", lb(d2, [12])[1][0] * 1e7, 1.3, 1)
check("2.4 sar const", ms.params[0], 0.0095, 4)
check("2.4 Jan t", m24.params[1] / m24.bse[1], 10.0, 1)
check("2.4 hand fc1", 0.00388 + 0.07891 + 0.23304 * -0.00406, 0.08184, 5)
check("2.4 hand se", 0.05965 * np.sqrt(1 + 0.23304 ** 2), 0.06125, 5)
check("2.4 chi2 12", __import__("scipy.stats").stats.chi2.ppf(0.95, 12), 21.03, 2)
check("2.5 rho1^100 x1e72", r100[1] ** 100 * 1e72, 9.0, 0)
a1d = acf(np.diff(pw), nlags=24)
check("2.6 acf d12", a1d[12], 0.757, 3); check("2.6 acf d24", a1d[24], 0.726, 3)
check("2.6 rho1rho12", -0.332 * -0.484, 0.161, 3)
check("2.6 yr shift", FC26[12] - FC26[0], 0.029, 3)
asum = g36["par"][4:7].sum()
check("3.6 alpha sum", 0.02741 + 0.05283 + 0.09608, 0.17632, 5)
check("3.6 1-sum", 1 - 0.17632, 0.82368, 5)
check("3.6 uncond", 0.00404 / 0.82368, 0.00490, 5)
check("3.6 uncond sd %", 100 * np.sqrt(g36["par"][3] / (1 - asum)), 7.0, 1)
check("3.6 t alpha3", g36["par"][6] / g36["se"][6], 2.32, 2)
check("3.11 dLL", g11g["llf"] - g11n["llf"], 105.75, 2)
check("3.11 band", 2 / np.sqrt(len(gm)), 0.040, 3)
for k, e in zip([3, 4, 5], [0.009968, 0.071347, 0.923498]):
    check(f"3.12 par6 {k}", g12["par"][k], e, 6)
check("3.12 aT 6d", aT, 1.507578, 6); check("3.12 s2T 6d", s2T, 7.926285, 6)
check("3.12 a+b 6d", al + be, 0.994845, 6)
check("3.12 hand r1 terms", -0.05888 * 1.4158, -0.08336, 5); check("3.12 hand r1 t2", -0.04190 * 2.4407, -0.10227, 5)
check("3.12 hand r1", 0.03570 - 0.08336 - 0.10227, -0.1499, 4)
check("3.12 hand r2", 0.03570 - 0.05888 * -0.1499 - 0.04190 * 1.4158, -0.0148, 4)
check("3.12 hand r3", 0.03570 - 0.05888 * -0.0148 - 0.04190 * -0.1499, 0.0429, 4)
check("3.12 hand r4", 0.03570 - 0.05888 * 0.0429 - 0.04190 * -0.0148, 0.0338, 4)
check("3.12 hand v1 a", 0.071347 * 1.507578 ** 2, 0.162157, 6)
check("3.12 hand v1 b", 0.923498 * 7.926285, 7.319908, 6)
v = 0.009968 + 0.162157 + 7.319908
check("3.12 hand v1", v, 7.492033, 6)
for k, e in enumerate([7.463380, 7.434874, 7.406515]):
    v = 0.009968 + 0.994845 * round(v, 6)
    check(f"3.12 hand v{k + 2}", v, e, 6)
check("3.12 ratio", s2T / (om / (1 - al - be)), 4.1, 1)
check("3.12 mean limit", mu / (1 - f1 - f2), 0.032, 3); check("3.12 1-f1-f2", 1 - f1 - f2, 1.1008, 4)
check("3.14 pz a", lb(g14a["z"], [10], df=2)[1][0], 0.119, 3); check("3.14 pzz a", lb(g14a["z"] ** 2, [10])[1][0], 0.320, 3)
check("3.14 alpha0 base", g14o["par"][1], 0.0540, 4)
check("3.14 hand contrib", 0.0499 * 1.1749, 0.0586, 4)
check("W12.4 8th moment", 105 * 0.5 ** 4, 6.56, 2)
check("W12.4 r_u 3d", r_u, -0.003, 3); check("W12.4 r_u2", r_u2, 0.458, 3)

# ==============================================================================================
# T 12.4  Ford monthly log returns 1965-2008: (a) GARCH(1,1), (b) SV-AR(1) by Gibbs (KSC mixture), (c) compare
# ==============================================================================================

fsp = pd.read_csv(DATA / "L08-m-fsp6508.txt", sep=r"\s+")
rf = 100 * np.log1p(fsp.F.values)
check("12.4 T", len(rf), 528, 0)
check("12.4 mean", rf.mean(), 0.429, 3); check("12.4 sd", rf.std(ddof=1), 9.543, 3); check("12.4 min", rf.min(), -86.48, 2)
check("12.4 min date", fsp.date.values[rf.argmin()], 20081031, 0)
qf, pf = lb(rf, [12]); qf2, pf2 = lb((rf - rf.mean()) ** 2, [12])
print(f"[12.4] LB r Q(12)={qf[0]:.2f} p={pf[0]:.3f}; LB e^2 Q(12)={qf2[0]:.2f} p={pf2[0]:.4f}")
check("12.4 Q12 r", qf[0], 14.99, 2); check("12.4 p r", pf[0], 0.242, 3)
check("12.4 Q12 e2", qf2[0], 31.40, 2); check("12.4 p e2", pf2[0], 0.0017, 4)
g124 = garch_fit(rf)
print("[12.4] GARCH(1,1)-N", g124["par"].round(4), "se", g124["se"].round(4), "llf", round(g124["llf"], 2))
for k, (e, s) in enumerate([(0.8818, 0.3378), (3.0047, 1.5608), (0.1430, 0.0333), (0.8381, 0.0390)]):
    check(f"12.4 garch par{k}", g124["par"][k], e, 4); check(f"12.4 garch se{k}", g124["se"][k], s, 4)
check("12.4 garch llf", g124["llf"], -1885.95, 2)
qz, pz = lb(g124["z"], [12]); qz2, pz2 = lb(g124["z"] ** 2, [12])
check("12.4 LB z", qz[0], 12.25, 2); check("12.4 LB z p", pz[0], 0.425, 3)
check("12.4 LB z2", qz2[0], 16.93, 2); check("12.4 LB z2 p", pz2[0], 0.152, 3)
check("12.4 kurt z", pd.Series(g124["z"]).kurt() + 3, 4.48, 2)
pers_g = g124["par"][2] + g124["par"][3]
check("12.4 garch pers", pers_g, 0.9811, 4)
check("12.4 garch uncond var", g124["par"][1] / (1 - pers_g), 159.2, 1)
check("12.4 sample var", rf.var(ddof=1), 91.07, 2)

# Kim, Shephard and Chib (1998) 7-component normal mixture for log(chi2_1): weights, means, variances.
KSC_Q = np.array([0.00730, 0.10556, 0.00002, 0.04395, 0.34001, 0.24566, 0.25750])
KSC_M = np.array([-10.12999, -3.97281, -8.56686, 2.77786, 0.61942, 1.79518, -1.08819]) - 1.2704
KSC_V = np.array([5.79596, 2.61369, 5.17950, 0.16735, 0.64009, 0.34023, 1.26261])
mix_mean = KSC_Q @ KSC_M
check("KSC mean = E log chi2_1", mix_mean, -1.2704, 4)               # psi(1/2) + log 2 = -1.27036
check("KSC var = pi^2/2", KSC_Q @ (KSC_V + KSC_M ** 2) - mix_mean ** 2, np.pi ** 2 / 2, 3)


def sv_gibbs(r, n_burn=2000, n_keep=10000, seed=2010):
    """Gibbs sampler for r_t = mu + sqrt(h_t) eps_t, ln h_t = al0 + al1 ln h_{t-1} + v_t, v_t ~ N(0, s2v).

    Priors as in Tsay (2010) Example 12.3: mu ~ N(0, 4); (al0, al1) ~ N((0, 0.6), diag(0.25, 0.04)) truncated
    to |al1| < 1; 10*0.1/s2v ~ chi2_10, i.e. s2v ~ IG(5, 0.5); ln h_1 ~ N(ln var(r), 10), not depending on theta.
    The ln h_t block uses the KSC mixture for log(r_t - mu)^2 and is drawn jointly from its Gaussian full
    conditional (tridiagonal precision, banded Cholesky); so the chain targets the mixture-approximated posterior.
    Returns (draws of (mu, al0, al1, s2v), posterior mean of sqrt(h_t) for t = 1..T).
    """
    rng = np.random.default_rng(seed)
    T = len(r)
    m0, C0 = np.log(np.var(r)), 10.0
    a_mean, a_prec = np.array([0.0, 0.6]), np.diag([1 / 0.25, 1 / 0.04])
    mu, al0, al1, s2v = r.mean(), 0.0, 0.9, 0.1
    x = np.full(T, m0)
    out, vol = np.empty((n_keep, 4)), np.zeros(T)
    for it in range(n_burn + n_keep):
        h = np.exp(x)
        prec = 1 / 4 + np.sum(1 / h)
        mu = rng.normal(np.sum(r / h) / prec, 1 / np.sqrt(prec))
        ys = np.log((r - mu) ** 2 + 1e-4)          # offset keeps log finite; negligible on the percent scale
        lp = np.log(KSC_Q) - 0.5 * np.log(KSC_V) - 0.5 * (ys[:, None] - x[:, None] - KSC_M) ** 2 / KSC_V
        p = np.exp(lp - lp.max(1, keepdims=True)); p /= p.sum(1, keepdims=True)
        s = (p.cumsum(1) < rng.random((T, 1))).sum(1)
        dq = np.full(T, (1 + al1 ** 2) / s2v); dq[0] = 1 / C0 + al1 ** 2 / s2v; dq[-1] = 1 / s2v
        b = np.full(T, al0 * (1 - al1) / s2v); b[0] = m0 / C0 - al1 * al0 / s2v; b[-1] = al0 / s2v
        U = cholesky_banded(np.vstack([np.r_[0.0, np.full(T - 1, -al1 / s2v)], dq + 1 / KSC_V[s]]))
        x = (cho_solve_banded((U, False), b + (ys - KSC_M[s]) / KSC_V[s])
             + solve_banded((0, 1), U, rng.standard_normal(T)))
        X, y = np.c_[np.ones(T - 1), x[:-1]], x[1:]
        V = np.linalg.inv(a_prec + X.T @ X / s2v)
        m = V @ (a_prec @ a_mean + X.T @ y / s2v)
        while True:
            al0, al1 = rng.multivariate_normal(m, V)
            if abs(al1) < 1:
                break
        e = y - al0 - al1 * x[:-1]
        s2v = (0.5 + e @ e / 2) / rng.gamma(5 + (T - 1) / 2)
        if it >= n_burn:
            out[it - n_burn] = mu, al0, al1, s2v
            vol += np.exp(x / 2)
    return out, vol / n_keep


sv, sv_vol = sv_gibbs(rf)
q = np.percentile(sv, [2.5, 97.5], axis=0)
print("[12.4] SV post mean", sv.mean(0).round(4), "sd", sv.std(0).round(4), "2.5%", q[0].round(4), "97.5%", q[1].round(4))
for k, (mn, sd, lo, hi) in enumerate([(0.663, 0.340, -0.004, 1.326), (0.373, 0.147, 0.138, 0.708),
                                      (0.911, 0.035, 0.831, 0.968), (0.091, 0.031, 0.048, 0.165)]):
    check(f"12.4 sv mean{k}", sv[:, k].mean(), mn, 3); check(f"12.4 sv sd{k}", sv[:, k].std(), sd, 3)
    check(f"12.4 sv lo{k}", q[0, k], lo, 3); check(f"12.4 sv hi{k}", q[1, k], hi, 3)
mu_h = sv[:, 1] / (1 - sv[:, 2]); s2_h = sv[:, 3] / (1 - sv[:, 2] ** 2)
uv_sv = np.exp(mu_h + s2_h / 2)                                   # E(a_t^2) = E(h_t) under the SV model
print(f"[12.4] SV mean ln h {np.median(mu_h):.3f}, var ln h {np.median(s2_h):.3f}, E h median {np.median(uv_sv):.2f}",
      np.percentile(uv_sv, [2.5, 97.5]).round(2))
check("12.4 sv E h median", np.median(uv_sv), 89.0, 1)
check("12.4 sv mu_h", np.median(mu_h), 4.220, 3); check("12.4 sv s2_h", np.median(s2_h), 0.542, 3)
check("12.4 sv E h lo", np.percentile(uv_sv, 2.5), 64.1, 1); check("12.4 sv E h hi", np.percentile(uv_sv, 97.5), 158.5, 1)
gvol = np.sqrt(g124["s2"])
corr_v = np.corrcoef(sv_vol, gvol)[0, 1]
i08 = int(np.where(fsp.date.values == 20081031)[0][0])
print(f"[12.4] corr(SV vol, GARCH vol)={corr_v:.3f}; mean vol SV {sv_vol.mean():.2f} GARCH {gvol.mean():.2f};"
      f" Oct-2008 SV {sv_vol[i08]:.2f} GARCH {gvol[i08]:.2f}; Nov-2008 SV {sv_vol[i08 + 1]:.2f} GARCH {gvol[i08 + 1]:.2f};"
      f" min SV {sv_vol.min():.2f} GARCH {gvol.min():.2f}")

# ==============================================================================================
# Original: Bayesian GARCH(1,1) for GM daily % log returns (Question 10 data), random-walk Metropolis-Hastings
# ==============================================================================================
def garch11_loglik(th, r):
    """Gaussian GARCH(1,1) log-likelihood, same start-up as garch_filter (pre-sample a^2 and sigma^2 = mean a^2).

    th = (mu, alpha0, alpha1, beta1). The variance recursion is a first-order linear filter in a_{t-1}^2.
    """
    mu, om, al, be = th
    a = r - mu
    s0 = np.mean(a ** 2)
    s2 = lfilter([1.0], [1.0, -be], om + al * np.r_[s0, a[:-1] ** 2], zi=[be * s0])[0]
    return -0.5 * np.sum(np.log(2 * np.pi) + np.log(s2) + a ** 2 / s2)


def garch11_logpost(th, r):
    """Log posterior: mu ~ N(0, 100); alpha0, alpha1, beta1 ~ N(0, 1000) on alpha0 > 0, alpha1 >= 0, beta1 >= 0,
    and alpha1 + beta1 < 1 (covariance stationarity). Returns -inf outside the support."""
    mu, om, al, be = th
    if om <= 0 or al < 0 or be < 0 or al + be >= 1:
        return -np.inf
    return garch11_loglik(th, r) - 0.5 * mu ** 2 / 100 - 0.5 * (om ** 2 + al ** 2 + be ** 2) / 1000


def rw_mh(logpost, th0, cov, n_burn=5000, n_keep=20000, seed=2015):
    """Random-walk Metropolis-Hastings with Gaussian proposal N(theta, cov); returns (draws, acceptance rate)."""
    rng = np.random.default_rng(seed)
    L = np.linalg.cholesky(cov)
    th, lp = np.array(th0, float), logpost(th0)
    out, acc = np.empty((n_keep, len(th))), 0
    for it in range(n_burn + n_keep):
        prop = th + L @ rng.standard_normal(len(th))
        lpp = logpost(prop)
        if np.log(rng.random()) < lpp - lp:
            th, lp = prop, lpp
            acc += it >= n_burn
        if it >= n_burn:
            out[it - n_burn] = th
    return out, acc / n_keep


check("BG loglik = garch_fit llf", garch11_loglik(g11n["par"], gm), g11n["llf"], 6)
cov_mle = np.linalg.inv(approx_hess3(g11n["par"], lambda th: garch_nll(th, gm, [], 1, 1, None, "norm")))
bg, bg_acc = rw_mh(lambda th: garch11_logpost(th, gm), g11n["par"], cov_mle)
bpers = bg[:, 2] + bg[:, 3]
buv = bg[:, 1] / (1 - bpers)
print("[BG] acc", round(bg_acc, 3), "mean", bg.mean(0).round(4), "sd", bg.std(0).round(4))
print("[BG] pers mean", bpers.mean().round(4), "sd", bpers.std().round(4), "q", np.percentile(bpers, [2.5, 50, 97.5]).round(4),
      "P(>0.99)", (bpers > 0.99).mean().round(3))
print("[BG] uncond var median", np.median(buv).round(2), "q", np.percentile(buv, [2.5, 97.5]).round(2))
check("12.4 corr vol", corr_v, 0.812, 3)
check("12.4 mean vol sv", sv_vol.mean(), 8.57, 2); check("12.4 mean vol garch", gvol.mean(), 8.95, 2)
check("12.4 Oct08 sv", sv_vol[i08], 27.89, 2); check("12.4 Oct08 garch", gvol[i08], 17.24, 2)
check("12.4 Nov08 sv", sv_vol[i08 + 1], 24.93, 2); check("12.4 Nov08 garch", gvol[i08 + 1], 36.65, 2)
check("12.4 min sv", sv_vol.min(), 5.54, 2); check("12.4 min garch", gvol.min(), 5.44, 2)
check("12.4 sd sample", np.sqrt(91.07), 9.54, 2); check("12.4 sd garch uv", np.sqrt(159.2), 12.6, 1)
check("12.4 sd sv E h", np.sqrt(89.0), 9.4, 1)
check("12.4 hand mu_h", 0.373 / (1 - 0.911), 4.19, 2); check("12.4 hand s2_h", 0.091 / (1 - 0.911 ** 2), 0.535, 3)
check("BG acc", bg_acc, 0.391, 3)
for k, (mn, sd) in enumerate([(0.0227, 0.0439), (0.1029, 0.0231), (0.0733, 0.0098), (0.9168, 0.0105)]):
    check(f"BG mean{k}", bg[:, k].mean(), mn, 4); check(f"BG sd{k}", bg[:, k].std(), sd, 4)
qp = np.percentile(bpers, [2.5, 50, 97.5])
check("BG pers mean", bpers.mean(), 0.9901, 4); check("BG pers sd", bpers.std(), 0.0043, 4)
check("BG pers lo", qp[0], 0.9811, 4); check("BG pers med", qp[1], 0.9902, 4); check("BG pers hi", qp[2], 0.9977, 4)
check("BG P>0.99", (bpers > 0.99).mean(), 0.517, 3)
qu = np.percentile(buv, [2.5, 97.5])
check("BG uv med", np.median(buv), 10.35, 2); check("BG uv lo", qu[0], 6.71, 2); check("BG uv hi", qu[1], 33.88, 2)
p11 = g11n["par"]; pers11 = p11[2] + p11[3]; uv11 = p11[1] / (1 - pers11)
gp, gu = np.array([0, 0, 1, 1.0]), np.array([0, 1 / (1 - pers11), uv11 / (1 - pers11), uv11 / (1 - pers11)])
se_p, se_u = np.sqrt(gp @ cov_mle @ gp), np.sqrt(gu @ cov_mle @ gu)
print(f"[BG] MLE pers {pers11:.4f} se {se_p:.4f}; uncond var {uv11:.2f} se {se_u:.2f}")
check("BG mle pers", pers11, 0.9908, 4); check("BG mle pers se", se_p, 0.0041, 4)
check("BG mle pers lo", pers11 - 1.96 * se_p, 0.9827, 4); check("BG mle pers hi", pers11 + 1.96 * se_p, 0.9988, 4)
check("BG mle uv", uv11, 10.20, 2); check("BG mle uv se", se_u, 3.26, 2)
check("BG mle uv lo", uv11 - 1.96 * se_u, 3.81, 2); check("BG mle uv hi", uv11 + 1.96 * se_u, 16.58, 2)
check("BG sample var", np.var(gm), 10.39, 2)
check("BG hand uv", 0.0942 / (1 - 0.9908), 10.2, 1)
check("BG mle pers dist to 1 in se", (1 - pers11) / se_p, 2.2, 1)
check("12.4 min %", rf.min(), -86.5, 1)
check("12.4 half-life garch", np.log(0.5) / np.log(0.9811), 36.3, 1)
check("12.4 half-life sv", np.log(0.5) / np.log(0.911), 7.4, 1)
check("12.4 sv kurtosis 3exp(s2_h)", 3 * np.exp(0.542), 5.16, 2)
check("12.4 sample kurtosis", pd.Series(rf).kurt() + 3, 16.27, 2)


# ==============================================================================================
# Block 5: GARCH variants (T 3.13 GARCH-M and EGARCH; T 3.9 TGARCH) and Student-t SV (original)
# ==============================================================================================
def vgarch_filter(th, r, kind, dist):
    """Residuals a_t and variances sigma_t^2 of a constant-mean GARCH(1,1) variant; th = (mu, kind params, shape).

    kind 'garchm': (c, alpha0, alpha1, beta1), r_t = mu + c sigma_t^2 + a_t (Tsay Eq. (3.23));
    kind 'egarch': (alpha0, alpha1, gamma1, beta1), ln s2_t = alpha0 + alpha1(|e| + gamma1 e)_{t-1} + beta1 ln s2_{t-1}
    (Tsay Eq. (3.28)); kind 'tgarch': (alpha0, alpha1, gamma1, beta1), Tsay Eq. (3.34); kind 'garch': (alpha0, alpha1,
    beta1), the TGARCH with gamma1 = 0. Pre-sample: s0 = mean((r - mean r)^2) replaces a_0^2 and sigma_0^2 (the start-up
    of garch_filter); TGARCH uses E(N_0) = 1/2; EGARCH sets e_0 = 0. Its own filter, because garch_filter has no
    variance-in-mean term, log variance or sign indicator.
    """
    mu = th[0]
    if kind == "garch":
        om, al, be = th[1:4]; ga, c, k = 0.0, 0.0, 4
    elif kind == "garchm":
        c, om, al, be = th[1:5]; ga, k = 0.0, 5
    else:
        om, al, ga, be = th[1:5]; c, k = 0.0, 5
    shape = th[k] if dist != "norm" else None
    m = r - mu
    s0 = np.mean((r - r.mean()) ** 2)
    n = len(r)
    a, s2 = np.empty(n), np.empty(n)
    for t in range(n):
        if kind == "egarch":
            if t:
                z = a[t - 1] / np.sqrt(s2[t - 1])
                s2[t] = np.exp(min(om + al * (abs(z) + ga * z) + be * np.log(s2[t - 1]), 50.0))
            else:
                s2[t] = np.exp(om + be * np.log(s0))
        elif t:
            s2[t] = om + (al + ga * (a[t - 1] < 0)) * a[t - 1] ** 2 + be * s2[t - 1]
        else:
            s2[t] = om + (al + ga / 2 + be) * s0
        a[t] = m[t] - c * s2[t]
    return a, s2, shape


def vgarch_fit(r, kind, dist="norm"):
    """Fit a GARCH(1,1) variant (see vgarch_filter) by conditional MLE: L-BFGS-B, then two Nelder-Mead polishes.

    r: returns; kind: 'garch', 'garchm', 'egarch' or 'tgarch'; dist: 'norm', 'ged' or 't' (standardized, Tsay
    Eqs. (3.7), (3.10)). Returns dict with par, se (inverse numerical Hessian), llf, a, s2, z.
    """
    r = np.asarray(r, float)
    v = np.var(r)
    x0, bd = {"garch": ([0.1 * v, 0.1, 0.8], [(1e-12, None), (0, 1), (0, 1)]),
              "garchm": ([0.0, 0.1 * v, 0.1, 0.8], [(None, None), (1e-12, None), (0, 1), (0, 1)]),
              "tgarch": ([0.1 * v, 0.05, 0.05, 0.8], [(1e-12, None), (0, 1), (0, 1), (0, 1)]),
              "egarch": ([0.1 * np.log(v), 0.1, 0.0, 0.9], [(None, None)] * 3 + [(-0.999, 0.999)])}[kind]
    x0 = [np.mean(r)] + x0 + ([1.5] if dist == "ged" else [8.0] if dist == "t" else [])
    bd = [(None, None)] + bd + ([(0.3, 10)] if dist == "ged" else [(2.05, 100)] if dist == "t" else [])

    def f(th):
        a, s2, shape = vgarch_filter(th, r, kind, dist)
        if not np.all(np.isfinite(s2)) or np.any(s2 <= 0):
            return 1e10
        z = a / np.sqrt(s2)
        lp = (-0.5 * np.log(2 * np.pi) - 0.5 * z ** 2 if dist == "norm" else ged_logpdf(z, shape) if dist == "ged"
              else std_t_logpdf(z, shape))
        val = -np.sum(lp - 0.5 * np.log(s2))
        return val if np.isfinite(val) else 1e10

    res = minimize(f, np.array(x0, float), method="L-BFGS-B", bounds=bd, options=dict(maxiter=5000))
    for _ in range(2):
        res = minimize(f, res.x, method="Nelder-Mead", options=dict(maxiter=40000, xatol=1e-10, fatol=1e-10))
    se = np.sqrt(np.diag(np.linalg.inv(approx_hess3(res.x, f))))
    a, s2, _ = vgarch_filter(res.x, r, kind, dist)
    return dict(par=res.x, se=se, llf=-res.fun, a=a, s2=s2, z=a / np.sqrt(s2))


def check_fit(tag, g, pars, ses, llf):
    """Assert the printed estimates (4 decimals), standard errors (4 decimals) and log-likelihood (2 decimals)."""
    print(f"[{tag}]", g["par"].round(5), "se", g["se"].round(5), "llf", round(g["llf"], 2))
    for k, (e, s) in enumerate(zip(pars, ses)):
        check(f"{tag} par{k}", g["par"][k], e, 4); check(f"{tag} se{k}", g["se"][k], s, 4)
    check(f"{tag} llf", g["llf"], llf, 2)


def check_lb(tag, z, lags, expected):
    """Assert Ljung-Box Q and p for z and z^2 at `lags`; expected = [(Q, p) for z..., (Q, p) for z^2...]."""
    qa, pa = lb(z, lags); qb, pb = lb(z ** 2, lags)
    print(f"[{tag}] LB z", qa.round(2), pa.round(3), "z^2", qb.round(2), pb.round(3))
    for k, (q_, p_) in enumerate(expected):
        qq, pp = (qa[k], pa[k]) if k < len(lags) else (qb[k - len(lags)], pb[k - len(lags)])
        check(f"{tag} Q{k}", qq, q_, 2); check(f"{tag} p{k}", pp, p_, 3)


# ---- T 3.13: GM daily percentage simple returns, GARCH-M and EGARCH ----
gms = 100 * gs.gm.values
qq, pp = lb(gms, [10])
check("3.13 Q10 r", qq[0], 30.44, 2); check("3.13 p10 r", pp[0], 0.0007, 4)
gm_m = {d: vgarch_fit(gms, "garchm", d) for d in ["norm", "ged", "t"]}
for d, e in zip(["norm", "ged", "t"], [-5852.29, -5747.51, -5726.07]):
    check(f"3.13 garchm llf {d}", gm_m[d]["llf"], e, 2)
check_fit("3.13 garchm t", gm_m["t"], [0.0293, -0.0118, 0.0357, 0.0671, 0.9337, 5.1114],
          [0.0525, 0.0078, 0.0191, 0.0115, 0.0113, 0.5062], -5726.07)
check_lb("3.13 garchm t", gm_m["t"]["z"], [10, 20], [(12.75, 0.238), (26.75, 0.142), (1.91, 0.997), (9.02, 0.983)])
check("3.13 t c", gm_m["t"]["par"][1] / gm_m["t"]["se"][1], -1.50, 2)
check("3.13 t nu-4", (gm_m["t"]["par"][5] - 4) / gm_m["t"]["se"][5], 2.20, 2)
gm_e = {d: vgarch_fit(gms, "egarch", d) for d in ["norm", "ged", "t"]}
for d, e in zip(["norm", "ged", "t"], [-5840.33, -5740.93, -5720.54]):
    check(f"3.13 egarch llf {d}", gm_e[d]["llf"], e, 2)
check_fit("3.13 egarch t", gm_e["t"], [-0.0490, -0.0795, 0.1177, -0.3389, 0.9965, 5.1797],
          [0.0378, 0.0139, 0.0201, 0.1062, 0.0026, 0.5165], -5720.54)
check_lb("3.13 egarch t", gm_e["t"]["z"], [10, 20], [(12.03, 0.283), (26.72, 0.143), (1.89, 0.997), (10.90, 0.949)])
eg = gm_e["t"]["par"]
check("3.13 t gamma", eg[3] / gm_e["t"]["se"][3], -3.19, 2)
for d, e in zip(["norm", "ged"], [-5.33, -3.79]):
    check(f"3.13 t gamma {d}", gm_e[d]["par"][3] / gm_e[d]["se"][3], e, 2)
check("3.13 ratio z=-2/+2", np.exp(-4 * eg[2] * eg[3]), 1.173, 3)
check("3.13 hand ratio", np.exp(-4 * 0.1177 * -0.3389), 1.173, 3)
check("3.13 alpha1(1-g)", eg[2] * (1 - eg[3]), 0.1576, 4); check("3.13 alpha1(1+g)", eg[2] * (1 + eg[3]), 0.0778, 4)

# ---- T 3.9: GM monthly percentage log returns 1950-2008, TGARCH(1,1) and 1-6 step volatility forecasts ----
gmm_d = pd.read_csv(DATA / "L08-m-gmsp5008.txt", sep=r"\s+")
gml = 100 * np.log1p(gmm_d.gm.values)
check("3.9 T", len(gml), 708, 0); check("3.9 mean", gml.mean(), 0.411, 3); check("3.9 sd", gml.std(ddof=1), 8.104, 3)
check("3.9 last r", gml[-1], -49.32, 2)
qq, pp = lb(gml, [12, 24]); q2, p2 = lb((gml - gml.mean()) ** 2, [12])
check("3.9 Q12 r", qq[0], 23.06, 2); check("3.9 p12 r", pp[0], 0.027, 3)
check("3.9 Q24 r", qq[1], 32.35, 2); check("3.9 p24 r", pp[1], 0.119, 3); check("3.9 Q12 r2", q2[0], 290.6, 1)
tg = {d: vgarch_fit(gml, "tgarch", d) for d in ["norm", "t"]}
check("3.9 tgarch llf norm", tg["norm"]["llf"], -2386.84, 2)
check_fit("3.9 tgarch t", tg["t"], [0.7425, 1.6798, 0.0477, 0.1030, 0.8786, 9.5764],
          [0.2401, 0.8912, 0.0278, 0.0471, 0.0345, 2.9478], -2379.03)
check_lb("3.9 tgarch t", tg["t"]["z"], [12, 24], [(15.43, 0.219), (26.10, 0.348), (11.47, 0.489), (20.86, 0.647)])
check("3.9 kurt z t", pd.Series(tg["t"]["z"]).kurt() + 3, 4.16, 2)
check("3.9 LR t vs norm", 2 * (tg["t"]["llf"] - tg["norm"]["llf"]), 15.61, 2)
gsym = vgarch_fit(gml, "garch", "t")
print("[3.9] symmetric GARCH(1,1)-t", gsym["par"].round(4), "llf", round(gsym["llf"], 2))
check("3.9 sym llf", gsym["llf"], -2381.93, 2)
mu9, om9, al9, ga9, be9, nu9 = tg["t"]["par"]
check("3.9 t gamma", ga9 / tg["t"]["se"][3], 2.19, 2)
check("3.9 LR gamma", 2 * (tg["t"]["llf"] - gsym["llf"]), 5.80, 2)
pers9 = al9 + ga9 / 2 + be9
check("3.9 pers", pers9, 0.9779, 4); check("3.9 uncond", om9 / (1 - pers9), 75.85, 2)
check("3.9 uncond sd", np.sqrt(om9 / (1 - pers9)), 8.71, 2)
aT9, s2T9 = tg["t"]["a"][-1], tg["t"]["s2"][-1]
print(f"[3.9] a_T={aT9:.6f} s2_T={s2T9:.6f} params6", np.round(tg["t"]["par"], 6))
check("3.9 aT", aT9, -50.059594, 6); check("3.9 s2T", s2T9, 670.470718, 6)
f9 = [om9 + (al9 + ga9 * (aT9 < 0)) * aT9 ** 2 + be9 * s2T9]
for _ in range(5):
    f9.append(om9 + pers9 * f9[-1])
print("[3.9] var fc", np.round(f9, 4), "vol fc", np.sqrt(f9).round(4))
for k, (ev, es_) in enumerate(zip([968.47, 948.70, 929.37, 910.47, 891.99, 873.91],
                                  [31.12, 30.80, 30.49, 30.17, 29.87, 29.56])):
    check(f"3.9 vfc{k + 1}", f9[k], ev, 2); check(f"3.9 sfc{k + 1}", np.sqrt(f9[k]), es_, 2)
for k, e in enumerate([1.679824, 0.047740, 0.102980, 0.878623]):
    check(f"3.9 par6 {k}", tg["t"]["par"][k + 1], e, 6)
check("3.9 hand a1+g1", 0.047740 + 0.102980, 0.150720, 6)
check("3.9 hand a2", 0.150720 * 50.059594 ** 2, 377.6987, 4)
check("3.9 hand bs2", 0.878623 * 670.470718, 589.0910, 4)
check("3.9 hand f1", 1.679824 + 377.6987 + 589.0910, 968.4695, 4)
check("3.9 hand pers", 0.047740 + 0.102980 / 2 + 0.878623, 0.9779, 4)

# ---- Original: Student-t stochastic volatility on simulated data, Gaussian SV vs SVt (NumPy Gibbs) ----
NU_GRID = np.arange(2.1, 60.0001, 0.05)


def svt_gibbs(y, student, n_burn=2000, n_keep=10000, seed=2022):
    """Gibbs sampler for y_t = exp(h_t/2) sqrt(lam_t) z_t, h_t = al0 + phi h_{t-1} + s_v eta_t (zero-mean returns).

    student=False fixes lam_t = 1 (Gaussian SV); True draws lam_t ~ IG(nu/2, nu/2) and nu (Student-t SV).
    Priors: (al0, phi) ~ N((0, 0.9), diag(1, 0.25)) truncated to |phi| < 1; s_v^2 ~ IG(2.5, 0.025); h_1 ~ N(ln var y, 10);
    nu ~ Exp(0.1) on NU_GRID (griddy Gibbs). The h block is that of sv_gibbs (KSC mixture on ln(y_t^2/lam_t), banded
    Cholesky); sv_gibbs is not reused because it has a mean mu, Tsay's priors and no lam_t / nu steps.
    Returns (draws of (mu_h, phi, s_v, nu), posterior mean of h_t, posterior mean of lam_t).
    """
    rng = np.random.default_rng(seed)
    T = len(y)
    m0, C0 = np.log(np.var(y)), 10.0
    a_mean, a_prec = np.array([0.0, 0.9]), np.diag([1 / 1.0, 1 / 0.25])
    al0, al1, s2v, nu = 0.0, 0.9, 0.05, 10.0
    lam, x = np.ones(T), np.full(T, m0)
    out, xs, lams = np.empty((n_keep, 4)), np.zeros(T), np.zeros(T)
    for it in range(n_burn + n_keep):
        ys = np.log(y ** 2 / lam + 1e-8)
        lp = np.log(KSC_Q) - 0.5 * np.log(KSC_V) - 0.5 * (ys[:, None] - x[:, None] - KSC_M) ** 2 / KSC_V
        p = np.exp(lp - lp.max(1, keepdims=True)); p /= p.sum(1, keepdims=True)
        s = (p.cumsum(1) < rng.random((T, 1))).sum(1)
        dq = np.full(T, (1 + al1 ** 2) / s2v); dq[0] = 1 / C0 + al1 ** 2 / s2v; dq[-1] = 1 / s2v
        b = np.full(T, al0 * (1 - al1) / s2v); b[0] = m0 / C0 - al1 * al0 / s2v; b[-1] = al0 / s2v
        U = cholesky_banded(np.vstack([np.r_[0.0, np.full(T - 1, -al1 / s2v)], dq + 1 / KSC_V[s]]))
        x = (cho_solve_banded((U, False), b + (ys - KSC_M[s]) / KSC_V[s])
             + solve_banded((0, 1), U, rng.standard_normal(T)))
        X, yy = np.c_[np.ones(T - 1), x[:-1]], x[1:]
        V = np.linalg.inv(a_prec + X.T @ X / s2v)
        m = V @ (a_prec @ a_mean + X.T @ yy / s2v)
        while True:
            al0, al1 = rng.multivariate_normal(m, V)
            if abs(al1) < 1:
                break
        e = yy - al0 - al1 * x[:-1]
        s2v = (0.025 + e @ e / 2) / rng.gamma(2.5 + (T - 1) / 2)
        if student:
            lam = (nu + y ** 2 * np.exp(-x)) / 2 / rng.gamma((nu + 1) / 2, size=T)
            S1, S2, g = np.log(lam).sum(), (1 / lam).sum(), NU_GRID / 2
            lk = T * (g * np.log(g) - gammaln(g)) - (g + 1) * S1 - g * S2 - 0.1 * NU_GRID
            w = np.exp(lk - lk.max()); w /= w.sum()
            nu = NU_GRID[min((w.cumsum() < rng.random()).sum(), len(NU_GRID) - 1)]
        if it >= n_burn:
            out[it - n_burn] = al0 / (1 - al1), al1, np.sqrt(s2v), nu
            xs += x; lams += lam
    return out, xs / n_keep, lams / n_keep


# Scale mixture: sqrt(lam) z with lam ~ IG(nu/2, nu/2) is t_nu (Monte Carlo quantiles vs exact).
rng = np.random.default_rng(6)
mix = np.sqrt(5 / rng.chisquare(5, 400_000)) * rng.standard_normal(400_000)
assert np.allclose(np.percentile(mix, [1, 5, 25, 75, 95, 99]), student_t.ppf([0.01, 0.05, 0.25, 0.75, 0.95, 0.99], 5),
                   atol=0.03)
N_CHECKS += 1
Ts, mu_s, phi_s, sv_s, nu_s = 2000, 0.0, 0.97, 0.15, 5.0
rng = np.random.default_rng(808)
hs = np.empty(Ts); hs[0] = mu_s + sv_s / np.sqrt(1 - phi_s ** 2) * rng.standard_normal()
for t in range(1, Ts):
    hs[t] = mu_s + phi_s * (hs[t - 1] - mu_s) + sv_s * rng.standard_normal()
lam_s = nu_s / rng.chisquare(nu_s, Ts)
ysim = np.exp(hs / 2) * np.sqrt(lam_s) * rng.standard_normal(Ts)
s2h_s = sv_s ** 2 / (1 - phi_s ** 2)
check("SVt s2_h true", s2h_s, 0.3807, 4); check("SVt kurt eps", 3 * (nu_s - 2) / (nu_s - 4), 9.0, 1)
check("SVt kurt theory", 3 * np.exp(s2h_s) * (nu_s - 2) / (nu_s - 4), 13.17, 2)
check("SVt kurt sample", pd.Series(ysim).kurt() + 3, 33.83, 2)
svg, hg, _ = svt_gibbs(ysim, False)
svt, ht, lt = svt_gibbs(ysim, True)
for tag, o in [("SV", svg), ("SVt", svt)]:
    qo = np.percentile(o, [2.5, 97.5], axis=0)
    print(f"[{tag}] mean", o.mean(0).round(3), "sd", o.std(0).round(3), "2.5%", qo[0].round(3), "97.5%", qo[1].round(3))
SV_TAB = {"SV": [(0.419, 0.093, 0.239, 0.607), (0.904, 0.031, 0.829, 0.953), (0.341, 0.060, 0.232, 0.474)],
          "SVt": [(0.166, 0.144, -0.116, 0.451), (0.972, 0.010, 0.948, 0.988), (0.147, 0.028, 0.100, 0.210),
                  (6.207, 1.048, 4.650, 8.500)]}
for tag, o in [("SV", svg), ("SVt", svt)]:
    qo = np.percentile(o, [2.5, 97.5], axis=0)
    for k, (mn, sd, lo, hi) in enumerate(SV_TAB[tag]):
        check(f"{tag} mean{k}", o[:, k].mean(), mn, 3); check(f"{tag} sd{k}", o[:, k].std(), sd, 3)
        check(f"{tag} lo{k}", qo[0, k], lo, 3); check(f"{tag} hi{k}", qo[1, k], hi, 3)
check("SVt P(nu<10)", (svt[:, 3] < 10).mean(), 0.992, 3)
check("SV rmse h", np.sqrt(np.mean((hg - hs) ** 2)), 0.549, 3)
check("SVt rmse h", np.sqrt(np.mean((ht - hs) ** 2)), 0.345, 3)
io = int(np.argmax(np.abs(ysim) * np.exp(-hs / 2)))
print(f"[SVt] outlier t={io + 1}: y={ysim[io]:.2f} lam={lam_s[io]:.2f} h={hs[io]:.2f}; post h SV {hg[io]:.2f} "
      f"SVt {ht[io]:.2f}; post lam {lt[io]:.2f}")
check("SVt outlier t", io + 1, 1925, 0); check("SVt outlier y", ysim[io], 23.41, 2)
check("SVt outlier lam", lam_s[io], 10.44, 2); check("SVt outlier h", hs[io], 1.66, 2)
check("SVt outlier post h SV", hg[io], 3.43, 2); check("SVt outlier post h SVt", ht[io], 1.40, 2)
check("SVt outlier post lam", lt[io], 30.61, 2)
check("SVt sd outlier", np.exp(hs[io] / 2), 2.29, 2)
check("SV implied s2_h", 0.341 ** 2 / (1 - 0.904 ** 2), 0.636, 3); check("SV implied kurt", 3 * np.exp(0.636), 5.67, 2)
check("SVt implied s2_h", 0.147 ** 2 / (1 - 0.972 ** 2), 0.391, 3)
check("SVt implied kurt", 3 * np.exp(0.391) * (6.207 - 2) / (6.207 - 4), 8.45, 2)
check("half-life SV", np.log(0.5) / np.log(0.904), 6.9, 1); check("half-life SVt", np.log(0.5) / np.log(0.972), 24.4, 1)
check("half-life true", np.log(0.5) / np.log(0.97), 22.8, 1)

print(f"ALL CHECKS PASSED ({N_CHECKS} checks)")
