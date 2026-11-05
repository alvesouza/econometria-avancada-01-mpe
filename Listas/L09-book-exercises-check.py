"""Reproduce and assert every number printed in Listas/lista-L09-book-exercises.tex.

Purpose: the L09 book-exercise answer key (Tsay AFTS 3e Ch. 8-10, Greenberg 1e Ch. 10)
prints VAR / VMA / cointegration / factor-model / multivariate-volatility estimates.
This script recomputes each one from the raw data in Listas/data/ and aborts on the
first mismatch (AssertionError naming the quantity).

Usage:  python Listas/L09-book-exercises-check.py            # recompute + assert
        python Listas/L09-book-exercises-check.py --print    # also print every value
        python Listas/L09-book-exercises-check.py --dump DIR # also write plot coordinates

Failures: AssertionError when a recomputed value differs from the printed one by more
than its tolerance (half a unit in the last printed decimal unless stated); FileNotFoundError
when a data file is missing from Listas/data/ (see Listas/data/README.md for sources).
Runtime: about 3-6 minutes (the multivariate GARCH likelihoods are pure NumPy recursions).
"""
import sys, warnings
from pathlib import Path
import numpy as np, pandas as pd
from scipy import stats, optimize, linalg
from scipy.signal import lfilter
from statsmodels.tsa.api import VAR
from statsmodels.tsa.vector_ar.vecm import VECM
from statsmodels.tools.numdiff import approx_hess

warnings.filterwarnings("ignore")
np.set_printoptions(precision=4, suppress=True, linewidth=160)
DATA = Path(__file__).resolve().parent / "data"
PRINT = "--print" in sys.argv or "--discover" in sys.argv
DISCOVER = "--discover" in sys.argv  # print only, never assert (used while writing the key)
DUMP = Path(sys.argv[sys.argv.index("--dump") + 1]) if "--dump" in sys.argv else None
LOG2PI = np.log(2 * np.pi)
N_CHECKS = 0


def chk(name, val, exp, dec, slack=0.5):
    """Assert val rounds to exp at `dec` decimals (tolerance slack*10^-dec, plus float noise)."""
    global N_CHECKS
    val, exp = np.asarray(val, float), np.asarray(exp, float)
    tol = slack * 10.0 ** (-dec) + 1e-9
    if PRINT:
        print(f"{name}: {np.round(val, dec).tolist()}")
    if DISCOVER:
        return
    assert val.shape == exp.shape, f"{name}: shape {val.shape} != {exp.shape}"
    ok = (np.abs(val - exp) <= tol) | (np.isnan(val) & np.isnan(exp))   # nan = s.e. of a parameter on its bound
    assert np.all(ok), f"{name}: computed {np.round(val, dec + 2).tolist()} vs printed {exp.tolist()}"
    N_CHECKS += 1


# ----------------------------------------------------------------------------- helpers
def ccm(x, l):
    """Lag-l sample cross-covariance matrix, Tsay Eq. (8.5): sum (r_t - rbar)(r_{t-l} - rbar)' / T."""
    x = x - x.mean(0)
    return x[l:].T @ x[: len(x) - l] / len(x)


def Qk(x, m):
    """Multivariate portmanteau Q_k(m), Tsay Eq. (8.7)."""
    T = len(x)
    G0i = np.linalg.inv(ccm(x, 0))
    return T * T * sum(np.trace(ccm(x, l).T @ G0i @ ccm(x, l) @ G0i) / (T - l) for l in range(1, m + 1))


def rec(u, b, y0):
    """y_0 = y0, y_t = b*y_{t-1} + u_t (t >= 1): a scalar GARCH-type recursion via lfilter."""
    y = np.empty(len(u))
    y[0] = y0
    y[1:] = lfilter([1.0], [1.0, -b], u[1:], zi=[b * y0])[0]
    return y


def gauss_nll(a, S):
    """Gaussian negative log-likelihood of shocks a (T x k) with covariances S (T x k x k)."""
    sign, ld = np.linalg.slogdet(S)
    if np.any(sign <= 0) or not np.all(np.isfinite(ld)):
        return 1e10
    q = np.einsum("ti,tij,tj->t", a, np.linalg.inv(S), a)
    return 0.5 * np.sum(ld + q + a.shape[1] * LOG2PI)


def std_resid(a, S):
    """Standardized residuals S_t^{-1/2} a_t with the symmetric square root (Tsay p. 533)."""
    w, V = np.linalg.eigh(S)
    return np.einsum("tij,tj->ti", V, np.einsum("tji,tj->ti", V, a) / np.sqrt(w))


def adequacy(e, ms=(5, 10)):
    """Q_k(m) of standardized residuals e and of e**2, with chi2(k^2 m) p values."""
    k = e.shape[1]
    out = []
    for m in ms:
        q1, q2 = Qk(e, m), Qk(e ** 2, m)
        out += [q1, stats.chi2.sf(q1, k * k * m), q2, stats.chi2.sf(q2, k * k * m)]
    return np.array(out)


def fit(nll, x0, bounds=None):
    """Minimize nll: L-BFGS-B, then Nelder-Mead polish, then L-BFGS-B again."""
    opt = dict(maxiter=20000, maxfun=200000)
    r = optimize.minimize(nll, x0, method="L-BFGS-B", bounds=bounds, options=opt)
    r2 = optimize.minimize(nll, r.x, method="Nelder-Mead", bounds=bounds, options=dict(maxiter=60000, xatol=1e-9, fatol=1e-10))
    if r2.fun < r.fun:
        r = r2
    r3 = optimize.minimize(nll, r.x, method="L-BFGS-B", bounds=bounds, options=opt)
    return r3 if r3.fun <= r.fun else r


def se(nll, x):
    """Asymptotic standard errors from the inverse numerical Hessian of nll at x."""
    return np.sqrt(np.diag(np.linalg.inv(approx_hess(x, nll))))


def dump(name, x, cols, step=3, fmt="%.2f"):
    """Write 'x y' coordinate strings (every `step`-th point) for pgfplots."""
    if DUMP is None:
        return
    DUMP.mkdir(parents=True, exist_ok=True)
    with open(DUMP / f"{name}.txt", "w") as f:
        for j, c in enumerate(cols):
            pts = " ".join(f"({x[i]:.2f},{fmt % c[i]})" for i in range(0, len(x), step))
            f.write(f"% series {j}\n{pts}\n")


def load_ret(fname, cols):
    d = pd.read_csv(DATA / fname, sep=r"\s+")
    return 100 * np.log1p(d[cols].values)


# ============================================================================ T 8.1
def e81():
    d = pd.read_csv(DATA / "m-mrk2vw.txt", sep=r"\s+")
    r = d.iloc[:, 1:].values
    T, k = r.shape
    chk("8.1 T", T, 588.0, 0)
    chk("8.1 mean", r.mean(0), [0.967, 1.17, 0.721, 0.124, 0.449, 0.725], 3)
    chk("8.1 cov", np.cov(r.T)[np.tril_indices(6)],
        [49.58, 23.87, 39.59, 17.93, 17.43, 41.37, 10.23, 8.82, 23.55, 72.82, 12.69, 11.85, 25.22, 54.19, 85.3, 14.3, 14.25, 20.49, 20.07, 21.85, 19.94], 2)
    chk("8.1 corr", np.corrcoef(r.T)[np.tril_indices(6, -1)],
        [0.539, 0.396, 0.431, 0.17, 0.164, 0.429, 0.195, 0.204, 0.425, 0.688, 0.455, 0.507, 0.713, 0.527, 0.53], 3)
    q1, q6 = Qk(r, 1), Qk(r, 6)
    chk("8.1 Q(1),Q(6)", [q1, q6], [87.42, 285.07], 2)
    chk("8.1 crit 36,216", [stats.chi2.ppf(0.95, 36), stats.chi2.ppf(0.95, 216)], [51.0, 251.29], 2)
    chk("8.1 p Q(1) x1e6", stats.chi2.sf(q1, 36) * 1e6, 3.6, 1)
    chk("8.1 p Q(6)", stats.chi2.sf(q6, 216), 0.0011, 4)
    chk("8.1 bound", 2 / np.sqrt(T), 0.0825, 4)
    sd = r.std(0)
    sig = []
    for l in range(1, 7):
        rho = ccm(r, l) / np.outer(sd, sd)
        for i, j in np.argwhere(np.abs(rho) > 2 / np.sqrt(T)):
            sig.append((l, i + 1, j + 1, rho[i, j]))
    chk("8.1 significant (lag,i,j)", [s[:3] for s in sig],
        [[1.0, 4.0, 3.0], [1.0, 4.0, 6.0], [1.0, 5.0, 6.0], [1.0, 6.0, 6.0], [3.0, 3.0, 2.0], [3.0, 4.0, 1.0], [5.0, 3.0, 4.0], [5.0, 6.0, 4.0], [6.0, 6.0, 2.0]], 0)
    chk("8.1 significant rho", [s[3] for s in sig], [0.159, 0.164, 0.104, 0.1, -0.087, 0.121, 0.102, 0.094, -0.086], 3)


# ============================================================================ T 8.2
def vma_cond(y, q):
    """Conditional-likelihood VMA(q) (a_0 = ... = a_{1-q} = 0), Sigma concentrated out.
    Returns theta0, [Theta_1..Theta_q] (Tsay sign: r_t = theta0 + a_t - sum Theta_j a_{t-j}), Sigma, residuals, llf."""
    T, k = y.shape

    def resid(th):
        th0 = th[:k]
        Th = th[k:].reshape(q, k, k)
        a = np.zeros((T + q, k))
        yc = y - th0
        for t in range(T):
            acc = yc[t].copy()
            for j in range(q):
                acc += Th[j] @ a[q + t - 1 - j]
            a[q + t] = acc
        return a[q:]

    def nll(th):
        a = resid(th)
        if not np.all(np.isfinite(a)) or np.abs(a).max() > 1e6:
            return 1e10
        return 0.5 * T * np.linalg.slogdet(a.T @ a / T)[1]

    r = fit(nll, np.r_[y.mean(0), np.zeros(q * k * k)])
    a = resid(r.x)
    S = a.T @ a / T
    llf = -0.5 * T * (np.linalg.slogdet(S)[1] + k * LOG2PI + k)
    return r.x[:k], r.x[k:].reshape(q, k, k), S, a, llf, se(nll, r.x)


def e82():
    g = pd.read_csv(DATA / "m-gs1n10.txt", sep=r"\s+")
    c = np.diff(g[["gs1", "gs10"]].values, axis=0)
    T, k = c.shape
    chk("8.2 T", T, 678.0, 0)
    p0 = 10
    y = c[p0:]

    def sig(i):  # Tsay Eq. (8.17), common sample t = p0+1..T
        if i == 0:
            e = y - y.mean(0)
        else:
            X = np.column_stack([np.ones(len(y))] + [c[p0 - j: T - j] for j in range(1, i + 1)])
            e = y - X @ np.linalg.lstsq(X, y, rcond=None)[0]
        return e.T @ e / (len(y) - 2 * i - 1)

    M = [-(len(y) - k - i - 1.5) * np.log(np.linalg.det(sig(i)) / np.linalg.det(sig(i - 1))) for i in range(1, 9)]
    chk("8.2 M(i)", M, [135.33, 57.25, 13.38, 8.1, 4.44, 43.09, 0.87, 10.15], 2)
    chk("8.2 crit chi2(4)", stats.chi2.ppf(0.95, 4), 9.49, 2)
    sel = VAR(c).select_order(10)
    chk("8.2 aic,bic,hq order", [sel.aic, sel.bic, sel.hqic], [8.0, 2.0, 6.0], 0)
    res = VAR(c).fit(6)
    chk("8.2 nobs", res.nobs, 672.0, 0)
    chk("8.2 const", res.params[0], [-0.0025, 0.0006], 4)
    PHI = np.array([[0.353, 0.264, 0.006, 0.394], [-0.161, -0.229, 0.045, -0.316],
                    [0.091, -0.087, 0.016, 0.115], [0.003, -0.008, 0.023, -0.088],
                    [0.091, -0.190, 0.054, -0.087], [-0.214, 0.398, -0.110, 0.234]])
    chk("8.2 Phi table", res.coefs.reshape(6, 4), [[0.324, 0.337, -0.008, 0.434], [-0.15, -0.234, 0.057, -0.32], [-0.032, 0.165, -0.123, 0.22], [-0.122, 0.006, 0.0, -0.034], [0.224, -0.047, 0.161, -0.095], [-0.314, 0.126, -0.195, 0.113]], 3)
    chk("8.2 Phi1 4 dec", res.coefs[0].ravel(), [0.3243, 0.3366, -0.0085, 0.4338], 4)
    chk("8.2 tstat > 2 count", int((np.abs(res.tvalues[1:]) > 2).sum()), 12.0, 0)
    chk("8.2 Sigma", res.sigma_u[np.tril_indices(2)], [0.1425, 0.0723, 0.0623], 4)
    chk("8.2 resid corr", res.sigma_u[0, 1] / np.sqrt(res.sigma_u[0, 0] * res.sigma_u[1, 1]), 0.768, 3)
    gc12 = res.test_causality(0, [1], kind="wald")   # does c10 Granger-cause c1?
    gc21 = res.test_causality(1, [0], kind="wald")   # does c1 Granger-cause c10?
    chk("8.2 Granger Wald (10y->1y, 1y->10y)", [gc12.test_statistic, gc21.test_statistic], [19.33, 46.38], 2)
    chk("8.2 Granger p (10y->1y) x1e3, -log10 p (1y->10y)", [gc12.pvalue * 1e3, -np.log10(gc21.pvalue)], [3.65, 7.6], 2)
    e = res.resid
    chk("8.2 VAR Q(12) resid", Qk(e, 12), 55.65, 2)
    chk("8.2 VAR Q(12) p", stats.chi2.sf(Qk(e, 12), 4 * 6), 0.0003, 4)
    # structural form (Tsay Eq. 8.9-8.10): Sigma = L G L'
    S = res.sigma_u
    w = S[1, 0] / S[0, 0]
    g22 = S[1, 1] - S[1, 0] ** 2 / S[0, 0]
    chk("8.2 L21, g11, g22", [w, S[0, 0], g22], [0.5075, 0.1425, 0.0256], 4)
    Linv = np.array([[1, 0], [-w, 1]])
    star = np.array([Linv @ P for P in res.coefs])
    chk("8.2 structural row2", star[:, 1, :].ravel(),
        [-0.173, 0.263, 0.133, -0.201, -0.106, 0.136, 0.062, -0.037, 0.048, -0.071, -0.036, 0.05], 3)
    chk("8.2 structural const", (Linv @ res.params[0])[1], 0.0019, 4)
    sdc = c.std(0)
    sigl = [l for l in range(1, 13) if np.abs(ccm(c, l) / np.outer(sdc, sdc)).max() > 2 / np.sqrt(T)]
    chk("8.2 significant CCM lags of c", sigl, [1.0, 2.0, 3.0, 5.0, 6.0, 7.0, 9.0, 10.0, 11.0], 0)
    # (b) VMA by conditional likelihood, q = 1..3
    out = {}
    for q in (1, 2, 3):
        th0, Th, Sq, a, llf, s = vma_cond(c, q)
        ld = np.linalg.slogdet(Sq)[1]   # Tsay's criteria: ln|Sigma_ML| + penalty(k^2 q)
        out[q] = (th0, Th, Sq, a, llf, s, ld + 2 * k * k * q / T, ld + np.log(T) * k * k * q / T)
    chk("8.2 VMA AIC q=1..3", [out[q][6] for q in (1, 2, 3)], [-5.5199, -5.5365, -5.5274], 4)
    chk("8.2 VMA BIC q=1..3", [out[q][7] for q in (1, 2, 3)], [-5.4932, -5.4831, -5.4474], 4)
    th0, Th, Sq, a, llf, s, _, _ = out[2]
    chk("8.2 VMA2 theta0", th0, [-0.0026, 0.0011], 4)
    chk("8.2 VMA2 Theta1", Th[0].ravel(), [-0.324, -0.309, 0.013, -0.42], 3)
    chk("8.2 VMA2 Theta2", Th[1].ravel(), [0.083, -0.029, -0.028, 0.131], 3)
    chk("8.2 VMA2 se Theta", s[2:], [0.061, 0.094, 0.04, 0.062, 0.069, 0.096, 0.041, 0.058], 3, slack=1.5)
    chk("8.2 VMA2 Sigma", Sq[np.tril_indices(2)], [0.1507, 0.0777, 0.0657], 4)
    chk("8.2 VMA2 Q(12)", Qk(a, 12), 111.14, 2)
    chk("8.2 VMA2 Q(12) -log10 p (df 40), resid corr", [-np.log10(stats.chi2.sf(Qk(a, 12), 40)), Sq[0, 1] / np.sqrt(Sq[0, 0] * Sq[1, 1])], [7.89, 0.782], 3)
    # VAR(6) information criteria on its own sample, for the comparison
    ld6 = np.linalg.slogdet(res.sigma_u_mle)[1]
    chk("8.2 VAR6 AIC, BIC (Tsay)", [ld6 + 2 * k * k * 6 / res.nobs, ld6 + np.log(res.nobs) * k * k * 6 / res.nobs], [-5.5822, -5.4211], 4)
    return out


# ============================================================================ T 8.5 (algebra check)
def e85():
    """Numerical sanity check of the derivations (no printed numbers)."""
    Phi4 = np.array([[0.5, 0.2], [-0.3, 0.6]])
    Sig = np.array([[1.0, 0.3], [0.3, 2.0]])
    G0 = np.linalg.solve(np.eye(4) - np.kron(Phi4, Phi4), Sig.ravel()).reshape(2, 2)
    assert np.allclose(G0, Phi4 @ G0 @ Phi4.T + Sig)
    F = np.zeros((8, 8)); F[:2, 6:] = Phi4; F[2:, :6] = np.eye(6)
    nu = np.linalg.eigvals(F)
    lam = np.linalg.eigvals(Phi4)
    assert np.allclose(np.sort(np.abs(nu)), np.sort(np.repeat(np.abs(lam) ** 0.25, 4)))
    # Gamma_l by simulation: Gamma_4 = Phi4 Gamma_0, Gamma_1 = Gamma_2 = Gamma_3 = 0
    rng = np.random.default_rng(1)
    T = 400000
    a = rng.multivariate_normal([0, 0], Sig, T)
    x = np.zeros((T, 2))
    for t in range(4, T):
        x[t] = Phi4 @ x[t - 4] + a[t]
    x = x[1000:]
    G = lambda l: (x[l:] - x.mean(0)).T @ (x[: len(x) - l] - x.mean(0)) / len(x)
    assert np.allclose(G(0), G0, atol=0.05) and np.allclose(G(4), Phi4 @ G0, atol=0.05)
    assert np.allclose(G(1), 0, atol=0.05) and np.allclose(G(8), Phi4 @ Phi4 @ G0, atol=0.05)
    global N_CHECKS
    N_CHECKS += 1


# ============================================================================ T 8.7
def johansen_rc(x, p):
    """Johansen trace / max-eigenvalue statistics with a restricted constant (Tsay case 2).
    Implements Eqs. (8.40)-(8.42) with d_t moved inside the cointegrating relation."""
    dx = np.diff(x, axis=0)
    Y = dx[p - 1:]
    Z1 = np.column_stack([x[p - 1:-1], np.ones(len(Y))])
    Zd = np.column_stack([dx[p - 1 - j: len(dx) - j] for j in range(1, p)])
    P = Zd @ np.linalg.pinv(Zd)
    R0, R1 = Y - P @ Y, Z1 - P @ Z1
    n = len(Y)
    S00, S01, S11 = R0.T @ R0 / n, R0.T @ R1 / n, R1.T @ R1 / n
    lam, V = linalg.eigh(S01.T @ np.linalg.solve(S00, S01), S11)
    idx = np.argsort(lam)[::-1]
    lam, V = lam[idx][: x.shape[1]], V[:, idx]
    tr = [-n * np.sum(np.log(1 - lam[m:])) for m in range(len(lam))]
    mx = [-n * np.log(1 - lam[m]) for m in range(len(lam))]
    return lam, np.array(tr), np.array(mx), V[:, 0] / V[0, 0], n


def e87():
    x = np.loadtxt(DATA / "m-gs1n3-5304.txt")[:, :2]
    T, k = x.shape
    chk("8.7 T, last obs", [T, x[-1, 0], x[-1, 1]], [612.0, 1.19, 2.0], 2)
    sel = VAR(x).select_order(12)
    chk("8.7 aic,bic,hq order", [sel.aic, sel.bic, sel.hqic], [12.0, 3.0, 7.0], 0)
    chk("8.7 BIC(1..5)", [sel.ics["bic"][i] for i in range(1, 6)], [-5.599, -5.756, -5.788, -5.776, -5.744], 3)
    res = VAR(x).fit(3)
    chk("8.7 const", res.params[0], [0.0586, 0.0744], 4)
    chk("8.7 Phi1", res.coefs[0].ravel(), [1.16, 0.357, 0.018, 1.405], 3)
    chk("8.7 Phi2", res.coefs[1].ravel(), [-0.287, -0.507, 0.014, -0.7], 3)
    chk("8.7 Phi3", res.coefs[2].ravel(), [0.108, 0.158, 0.006, 0.248], 3)
    chk("8.7 se Phi1", res.stderr[1:3].T.ravel(), [0.11, 0.13, 0.092, 0.109], 3)
    chk("8.7 Sigma", res.sigma_u[np.tril_indices(2)], [0.1657, 0.1292, 0.1167], 4)
    chk("8.7 Sigma 5 dec", res.sigma_u[np.tril_indices(2)], [0.16573, 0.12922, 0.11669], 5)
    chk("8.7 VAR long-run mean", res.mean(), [5.671, 6.093], 3)
    q12 = Qk(res.resid, 12)
    chk("8.7 Q(12)", q12, 151.36, 2)
    chk("8.7 Q(12) p", stats.chi2.sf(q12, 36), 0.0, 4)
    eig = np.sort(np.abs(np.linalg.eigvals(np.block([[np.hstack(res.coefs)], [np.eye(4), np.zeros((4, 2))]]))))[::-1]
    chk("8.7 companion |eig| top2", eig[:2], [0.9856, 0.944], 4)
    # (b) IRFs
    psi = res.ma_rep(6)
    chk("8.7 Psi_1..6", psi[1:].reshape(6, 4),
        [[1.16, 0.357, 0.018, 1.405], [1.066, 0.41, 0.061, 1.28], [1.024, 0.276, 0.115, 1.075], [1.02, 0.198, 0.164, 0.974], [1.014, 0.2, 0.204, 0.943], [1.002, 0.217, 0.239, 0.916]], 3)
    P = np.linalg.cholesky(res.sigma_u)
    chk("8.7 P (chol)", [P[0, 0], P[1, 0], P[1, 1]], [0.4071, 0.3174, 0.1262], 4)
    oir = res.orth_ma_rep(6)
    chk("8.7 orth IRF 0..6", oir.reshape(7, 4),
        [[0.407, 0.0, 0.317, 0.126], [0.586, 0.045, 0.453, 0.177], [0.564, 0.052, 0.431, 0.162], [0.504, 0.035, 0.388, 0.136], [0.478, 0.025, 0.376, 0.123], [0.476, 0.025, 0.382, 0.119], [0.477, 0.027, 0.388, 0.116]], 3)
    # (c) forecasts
    fc, lo, hi = res.forecast_interval(x[-3:], 12, alpha=0.05)
    fse = np.sqrt(np.array([np.diag(m) for m in res.forecast_cov(12)]))
    chk("8.7 VAR fc", fc.ravel(),
        [1.149, 1.917, 1.21, 1.969, 1.308, 2.039, 1.386, 2.082, 1.442, 2.11, 1.495, 2.139, 1.552, 2.173, 1.611, 2.21, 1.668, 2.247, 1.725, 2.284, 1.78, 2.321, 1.835, 2.359], 3)
    chk("8.7 VAR fc se h=1,6,12", fse[[0, 5, 11]].ravel(), [0.407, 0.342, 1.242, 1.025, 1.681, 1.418], 3)
    # (d) Johansen restricted constant, p = 3
    lam, tr, mx, beta, n = johansen_rc(x, 3)
    chk("8.7 johansen n", n, 609.0, 0)
    chk("8.7 johansen eig", lam, [0.0435, 0.0061], 4)
    chk("8.7 johansen eig 6 dec, -ln(1-lam)", np.r_[lam, -np.log(1 - lam)], [0.043548, 0.006076, 0.044524, 0.006094], 6)
    chk("8.7 trace", tr, [30.83, 3.71], 2)
    chk("8.7 maxeig", mx, [27.12, 3.71], 2)
    chk("8.7 beta (unrestricted eigvec)", beta, [1.0, -1.0088, 0.475], 4)
    # (e) ECM
    vec = VECM(x, k_ar_diff=2, coint_rank=1, deterministic="ci").fit()
    b = vec.beta.ravel()
    chk("8.7 VECM beta", b, [1.0, -1.0088], 4)
    chk("8.7 VECM const", vec.const_coint.ravel()[0], 0.475, 4)
    chk("8.7 VECM alpha", vec.alpha.ravel(), [-0.0276, 0.0313], 4)
    chk("8.7 beta2, c0 5 dec", [b[1], vec.const_coint.ravel()[0]], [-1.00875, 0.47503], 5)
    ba = float(b @ vec.alpha.ravel())
    chk("8.7 beta'alpha, half-life", [ba, np.log(0.5) / np.log(1 + ba)], [-0.0592, 11.3638], 4)
    chk("8.7 VECM se alpha", vec.stderr_alpha.ravel(), [0.0329, 0.0276], 4)
    chk("8.7 VECM Gamma1", vec.gamma[:, :2].ravel(), [0.19, 0.336, -0.012, 0.442], 3)
    chk("8.7 VECM Gamma2", vec.gamma[:, 2:].ravel(), [-0.098, -0.175, 0.002, -0.262], 3)
    chk("8.7 VECM Sigma", vec.sigma_u[np.tril_indices(2)], [0.1648, 0.1285, 0.116], 4)
    chk("8.7 spread at origin", x[-1] @ b + vec.const_coint.ravel()[0], -0.3525, 4)
    # (f) ECM forecasts
    fe = vec.predict(steps=12)
    chk("8.7 ECM fc", fe.ravel(),
        [1.11, 1.884, 1.113, 1.89, 1.153, 1.912, 1.175, 1.911, 1.178, 1.896, 1.179, 1.881, 1.183, 1.871, 1.19, 1.863, 1.196, 1.856, 1.2, 1.848, 1.205, 1.841, 1.209, 1.834], 3)
    return res, vec


# ============================================================================ T 9.7
def e97():
    f = pd.read_csv(DATA / "m-fedip.txt", sep=r"\s+")
    chk("9.7 T macro", len(f), 594.0, 0)
    z = np.column_stack([np.diff(f["FF"].values), 100 * np.diff(np.log(f["IP"].values))])
    sel = VAR(z).select_order(12)
    chk("9.7 bic order", sel.bic, 2.0, 0)
    var = VAR(z).fit(sel.bic)
    chk("9.7 VAR(2) Sigma", var.sigma_u[np.tril_indices(2)], [0.2603, 0.0741, 0.666], 4)
    s = var.resid[-168:]
    R = 100 * pd.read_csv(DATA / "m-excess-c10sp-9003.txt", sep=r"\s+").iloc[:, :10].values
    T = len(R)
    G = np.column_stack([np.ones(T), s])
    xi = np.linalg.solve(G.T @ G, G.T @ R)
    E = R - G @ xi
    s2 = np.diag(E.T @ E) / (T - 3)
    Rc = R - R.mean(0)
    r2 = 1 - np.diag(E.T @ E) / np.diag(Rc.T @ Rc)
    sb = np.sqrt(np.outer(np.diag(np.linalg.inv(G.T @ G))[1:], s2))
    chk("9.7 beta FF", xi[1], [-2.52, -2.42, -0.5, -4.93, -13.34, -7.77, -4.91, -3.84, -4.22, -3.25], 2)
    chk("9.7 beta IP", xi[2], [-1.06, -0.06, -2.37, -1.77, 1.64, 1.5, -0.5, -0.35, -1.81, -0.94], 2)
    chk("9.7 t FF", xi[1] / sb[0], [-0.83, -0.57, -0.13, -1.34, -2.85, -1.72, -1.6, -1.4, -1.46, -1.53], 2)
    chk("9.7 t IP", xi[2] / sb[1], [-1.08, -0.04, -1.95, -1.49, 1.08, 1.03, -0.51, -0.39, -1.93, -1.37], 2)
    chk("9.7 sigma_i", np.sqrt(s2), [6.2, 8.73, 7.66, 7.52, 9.58, 9.24, 6.28, 5.6, 5.93, 4.34], 2)
    chk("9.7 R2", r2, [0.013, 0.002, 0.023, 0.027, 0.05, 0.021, 0.018, 0.014, 0.039, 0.028], 3)
    sd = np.sqrt(np.diag(E.T @ E))
    rc = (E.T @ E) / np.outer(sd, sd)
    rd = np.corrcoef(R.T)
    i_, j_ = np.unravel_index(np.argmax(np.abs(rc - np.eye(10))), rc.shape)
    chk("9.7 argmax resid corr pair", sorted([i_, j_]), [7.0, 8.0], 0)
    off = np.tril_indices(10, -1)
    chk("9.7 max |resid corr|, mean resid corr, mean data corr", [np.abs(rc[off]).max(), rc[off].mean(), rd[off].mean()],
        [0.736, 0.302, 0.308], 3)
    Sf = np.cov(s.T)
    Cm = xi[1:].T @ Sf @ xi[1:] + np.diag(s2)
    sdm = np.sqrt(np.diag(Cm))
    chk("9.7 max |model corr|", np.abs((Cm / np.outer(sdm, sdm))[off]).max(), 0.032, 3)


# ============================================================================ T 10.1-10.4 (IBM, HPQ, SP)
def ewma_S(a, lam):
    T, k = a.shape
    S0 = np.cov(a.T)
    S = np.empty((T, k, k))
    for i in range(k):
        for j in range(i + 1):
            S[:, i, j] = S[:, j, i] = rec(np.r_[0, (1 - lam) * a[:-1, i] * a[:-1, j]], lam, S0[i, j])
    return S


def sym2(v):
    return np.array([[v[0], v[1]], [v[1], v[2]]])


def dvec_S(a, A0, A1, B1):
    T, k = a.shape
    S0 = np.cov(a.T)
    S = np.empty((T, k, k))
    for i in range(k):
        for j in range(i + 1):
            S[:, i, j] = S[:, j, i] = rec(np.r_[0, A0[i, j] + A1[i, j] * a[:-1, i] * a[:-1, j]], B1[i, j], S0[i, j])
    return S


def bekk_S(a, C, A1, B1):
    T, k = a.shape
    S = np.empty((T, k, k))
    S[0] = np.cov(a.T)
    CC = C @ C.T
    for t in range(1, T):
        S[t] = CC + A1 @ np.outer(a[t - 1], a[t - 1]) @ A1.T + B1 @ S[t - 1] @ B1.T
    return S


def garch_var(a, w, al, be):
    """Univariate GARCH(1,1) variance path, started at the sample variance."""
    return rec(np.r_[0, w + al * a[:-1] ** 2], be, a.var())


def e10_ibm():
    R = load_ret("m-ibmhpqsp6208.txt", ["IBM", "HPQ", "SP"])
    T = len(R)
    years = 1962 + np.arange(T) / 12
    chk("10.x T", T, 564.0, 0)
    chk("10.x means, sds", np.r_[R.mean(0), R.std(0, ddof=1)], [0.622, 0.955, 0.45, 7.157, 9.716, 4.341], 3)
    chk("10.x Q(12) univariate", [Qk(R[:, [i]], 12) for i in range(3)], [7.08, 7.12, 11.4], 2)
    chk("10.x Q_3(5) returns", Qk(R, 5), 53.4, 2)

    # ---- 10.1 EWMA
    def nll_ewma(th):
        a = R - th[:3]
        return gauss_nll(a, ewma_S(a, th[3]))

    r = fit(nll_ewma, np.r_[R.mean(0), 0.95], bounds=[(None, None)] * 3 + [(0.5, 0.9999)])
    s = se(nll_ewma, r.x)
    chk("10.1 mu", r.x[:3], [0.631, 0.906, 0.397], 3, slack=1)
    chk("10.1 lambda, se", [r.x[3], s[3]], [0.9687, 0.0065], 4, slack=1)
    chk("10.1 llf", -r.fun, -5316.8, 2, slack=1)
    chk("10.1 ln(lambda)", np.log(r.x[3]), -0.031781, 6, slack=60)
    chk("10.1 half-life", np.log(0.5) / np.log(r.x[3]), 21.8, 1, slack=1)
    a = R - r.x[:3]
    S = ewma_S(a, r.x[3])
    vol = np.sqrt(np.einsum("tii->ti", S))
    chk("10.1 vol min,max", np.r_[vol.min(0), vol.max(0)], [4.79, 7.44, 2.92, 12.18, 15.2, 6.31], 2, slack=1)
    dump("ewma", years, vol.T)

    # ---- 10.2 DVEC(1,1) IBM, HPQ
    X = R[:, :2]

    def nll_dvec(th):
        a = X - th[:2]
        return gauss_nll(a, dvec_S(a, sym2(th[2:5]), sym2(th[5:8]), sym2(th[8:11])))

    S0 = np.cov(X.T)
    x0 = np.r_[X.mean(0), 0.05 * S0[np.tril_indices(2)][[0, 1, 2]], [0.08] * 3, [0.85] * 3]
    r = fit(nll_dvec, x0)
    s = se(nll_dvec, r.x)
    chk("10.2 params", r.x, [0.703, 1.124, 2.998, 4.283, 6.158, 0.065, 0.066, 0.071, 0.874, 0.802, 0.864], 3, slack=2)
    chk("10.2 se", s, [0.284, 0.386, 1.616, 2.344, 2.566, 0.025, 0.024, 0.021, 0.053, 0.086, 0.04], 3, slack=3)
    chk("10.2 llf", -r.fun, -3873.45, 2, slack=1)
    a = X - r.x[:2]
    S = dvec_S(a, sym2(r.x[2:5]), sym2(r.x[5:8]), sym2(r.x[8:11]))
    e = std_resid(a, S)
    ad = adequacy(e)
    chk("10.2 Q stats", ad[[0, 2, 4, 6]], [18.54, 29.97, 31.91, 45.19], 2, slack=1)
    chk("10.2 Q pvals", ad[[1, 3, 5, 7]], [0.552, 0.07, 0.815, 0.264], 3, slack=1)
    lb = [stats.chi2.sf(Qk(e[:, [i]] ** 2, 12), 12) for i in range(2)]
    chk("10.2 univariate LB of squared std resid p", lb, [0.987, 0.248], 3, slack=1)
    vol = np.sqrt(np.einsum("tii->ti", S))
    corr = S[:, 0, 1] / (vol[:, 0] * vol[:, 1])
    chk("10.2 corr min,max,mean", [corr.min(), corr.max(), corr.mean()], [0.165, 0.704, 0.489], 3, slack=1)
    eig = np.linalg.eigvalsh(S).min()
    assert eig > 0
    dump("dvec_vol", years, vol.T)
    dump("dvec_corr", years, [corr], fmt="%.3f")

    # ---- 10.3 BEKK(1,1) SP, HPQ
    X = R[:, [2, 1]]

    def unpack(th):
        C = np.array([[th[2], 0], [th[3], th[4]]])
        return th[:2], C, th[5:9].reshape(2, 2), th[9:13].reshape(2, 2)

    def nll_bekk(th):
        mu, C, A1, B1 = unpack(th)
        a = X - mu
        return gauss_nll(a, bekk_S(a, C, A1, B1))

    Lc = np.linalg.cholesky(np.cov(X.T) * 0.05)
    x0 = np.r_[X.mean(0), Lc[0, 0], Lc[1, 0], Lc[1, 1], 0.3, 0, 0, 0.3, 0.9, 0, 0, 0.9]
    r = fit(nll_bekk, x0)
    for x1 in (np.r_[x0[:5], 0.2, 0.05, 0.05, 0.2, 0.95, 0, 0, 0.95], np.r_[x0[:5], 0.4, 0, 0, 0.4, 0.8, 0.1, -0.1, 0.8]):
        r1 = fit(nll_bekk, x1)   # extra starts: the BEKK likelihood is multimodal
        if r1.fun < r.fun:
            r = r1
    th = r.x.copy()
    # sign normalisation: (C, A1, B1) and (C D, -A1, -B1) give the same Sigma_t
    if th[5] < 0: th[5:9] *= -1
    if th[9] < 0: th[9:13] *= -1
    if th[2] < 0: th[2] *= -1; th[3] *= -1
    if th[4] < 0: th[4] *= -1
    assert abs(nll_bekk(th) - r.fun) < 1e-6
    s = se(nll_bekk, th)
    chk("10.3 params", th, [0.535, 1.128, 1.16, 1.13, 0.0, 0.427, -0.067, 0.586, 0.022, 0.847, 0.038, -0.311, 1.037], 3, slack=2)
    chk("10.3 se", s, [0.167, 0.389, 0.307, 0.94, 1.282, 0.06, 0.029, 0.155, 0.075, 0.03, 0.011, 0.076, 0.015], 3, slack=3)
    chk("10.3 llf", -r.fun, -3536.57, 2, slack=1)
    mu, C, A1, B1 = unpack(th)
    a = X - mu
    S = bekk_S(a, C, A1, B1)
    ad = adequacy(std_resid(a, S))
    chk("10.3 Q stats", ad[[0, 2, 4, 6]], [35.18, 13.02, 48.62, 32.83], 2, slack=1)
    chk("10.3 Q pvals", ad[[1, 3, 5, 7]], [0.019, 0.876, 0.165, 0.782], 3, slack=1)
    vol = np.sqrt(np.einsum("tii->ti", S))
    corr = S[:, 0, 1] / (vol[:, 0] * vol[:, 1])
    chk("10.3 corr min,max,mean", [corr.min(), corr.max(), corr.mean()], [0.333, 0.893, 0.607], 3, slack=1)
    CC = C @ C.T
    chk("10.3 spectral radius A1(x)A1+B1(x)B1", max(abs(np.linalg.eigvals(np.kron(A1, A1) + np.kron(B1, B1)))), 0.9524, 4)
    chk("10.3 CC'", CC[np.tril_indices(2)], [1.345, 1.311, 1.278], 3, slack=2)
    dump("bekk_vol", years, vol.T)
    dump("bekk_corr", years, [corr], fmt="%.3f")

    # ---- 10.4 CCC, IBM HPQ SP (diagonal GARCH(1,1) + constant R)
    def ccc_parts(th, X):
        k = X.shape[1]
        a = X - th[:k]
        V = np.column_stack([garch_var(a[:, i], *th[k + 3 * i: k + 3 * i + 3]) for i in range(k)])
        Rm = np.eye(k)
        Rm[np.tril_indices(k, -1)] = th[4 * k:]
        Rm = Rm + np.tril(Rm, -1).T
        return a, V, Rm

    def nll_ccc(th, X=R):
        a, V, Rm = ccc_parts(th, X)
        if np.any(V <= 0) or np.linalg.eigvalsh(Rm).min() <= 1e-6:
            return 1e10
        z = a / np.sqrt(V)
        k = X.shape[1]
        return 0.5 * np.sum(np.linalg.slogdet(Rm)[1] + np.log(V).sum(1) + np.einsum("ti,ij,tj->t", z, np.linalg.inv(Rm), z) + k * LOG2PI)

    k = 3
    v = R.var(0)
    x0 = np.r_[R.mean(0), np.ravel([[0.05 * v[i], 0.08, 0.87] for i in range(k)]), np.corrcoef(R.T)[np.tril_indices(k, -1)]]
    bnds = [(None, None)] * k + [(1e-6, None), (0, 1), (0, 1)] * k + [(-0.99, 0.99)] * 3
    r = fit(nll_ccc, x0, bnds)
    s = se(nll_ccc, r.x)
    chk("10.4 params", r.x, [0.783, 1.252, 0.53, 1.472, 0.057, 0.915, 4.424, 0.061, 0.892, 1.348, 0.056, 0.873, 0.494, 0.605, 0.623], 3, slack=2)
    chk("10.4 se", s, [0.275, 0.38, 0.172, 1.043, 0.022, 0.039, 2.049, 0.018, 0.033, 0.512, 0.019, 0.032, 0.032, 0.028, 0.026], 3, slack=3)
    chk("10.4 llf", -r.fun, -5291.05, 2, slack=1)
    a, V, Rm = ccc_parts(r.x, R)
    S = np.sqrt(V)[:, :, None] * Rm[None] * np.sqrt(V)[:, None, :]
    ad = adequacy(std_resid(a, S))
    chk("10.4 Q stats", ad[[0, 2, 4, 6]], [54.51, 53.86, 82.01, 93.85], 2, slack=1)
    chk("10.4 Q pvals", ad[[1, 3, 5, 7]], [0.156, 0.171, 0.714, 0.37], 3, slack=1)
    return R


# ============================================================================ T 10.5-10.6 (GE, IBM, SP 1926-2008)
def e10_ge():
    R = load_ret("m-geibmsp2608.txt", ["GE", "IBM", "SP"])
    T = len(R)
    chk("10.5 T", T, 996.0, 0)
    chk("10.5 means, sds", np.r_[R.mean(0), R.std(0, ddof=1)], [0.833, 1.089, 0.43, 7.672, 7.033, 5.537], 3)
    X0 = R[:, [0, 2]]
    chk("10.5 Q(12) GE, SP", [Qk(X0[:, [i]], 12) for i in range(2)], [42.25, 34.58], 2)
    chk("10.5 Q_2(5) returns, p", [Qk(X0, 5), stats.chi2.sf(Qk(X0, 5), 20) * 1e6], [64.51, 1.4], 2)
    # mean equation: VAR(3) by OLS; the volatility models are fitted to its residuals (two-step)
    vm = VAR(X0).fit(3)
    X = vm.resid
    T = len(X)
    chk("10.5 VAR(3) resid Q_2(5), p", [Qk(X, 5), stats.chi2.sf(Qk(X, 5), 20)], [25.75, 0.174], 3)

    # ---- 10.5 bivariate constant-correlation GARCH(1,1), Tsay Eq. (10.22); full and diagonal
    def parts(th, full):
        mu = th[:2]; a0 = th[2:4]
        if full:
            A1 = th[4:8].reshape(2, 2); B1 = th[8:12].reshape(2, 2); rho = th[12]
        else:
            A1 = np.diag(th[4:6]); B1 = np.diag(th[6:8]); rho = th[8]
        a = X - mu
        V = np.empty((T, 2)); V[0] = a.var(0)
        if full:
            for t in range(1, T):
                V[t] = a0 + A1 @ a[t - 1] ** 2 + B1 @ V[t - 1]
        else:
            for i in range(2):
                V[:, i] = garch_var(a[:, i], a0[i], A1[i, i], B1[i, i])
        return a, V, rho, a0, A1, B1

    def nll(th, full):
        a, V, rho, *_ = parts(th, full)
        if np.any(V <= 0) or abs(rho) >= 0.999:
            return 1e10
        z = a / np.sqrt(V)
        q = (z[:, 0] ** 2 + z[:, 1] ** 2 - 2 * rho * z[:, 0] * z[:, 1]) / (1 - rho ** 2)
        return 0.5 * np.sum(np.log(V).sum(1) + np.log(1 - rho ** 2) + q + 2 * LOG2PI)

    v = X.var(0)
    xd = np.r_[X.mean(0), 0.05 * v, 0.1, 0.1, 0.85, 0.85, 0.7]
    rd = fit(lambda t: nll(t, False), xd, [(None, None)] * 2 + [(1e-6, None)] * 2 + [(0, 1)] * 4 + [(-0.99, 0.99)])
    xf = np.r_[rd.x[:4], rd.x[4], 0.01, 0.01, rd.x[5], rd.x[6], 0.01, 0.01, rd.x[7], rd.x[8]]
    rf = fit(lambda t: nll(t, True), xf, [(None, None)] * 2 + [(1e-6, None)] * 2 + [(0, 1)] * 8 + [(-0.99, 0.99)])
    lr = 2 * (rd.fun - rf.fun)
    chk("10.5 llf diag, full, LR", [-rd.fun, -rf.fun, lr], [-5807.77, -5799.83, 15.9], 2, slack=1)
    chk("10.5 LR p (df 4)", stats.chi2.sf(lr, 4), 0.003, 3, slack=1)
    sd = se(lambda t: nll(t, False), rd.x)
    chk("10.5 diag params", rd.x, [0.343, 0.221, 3.657, 1.401, 0.093, 0.09, 0.835, 0.852, 0.781], 3, slack=2)
    chk("10.5 diag se", sd, [0.202, 0.136, 0.853, 0.299, 0.018, 0.015, 0.027, 0.021, 0.013], 3, slack=3)
    a, V, rho, a0, A1, B1 = parts(rd.x, False)
    S = np.empty((T, 2, 2))
    S[:, 0, 0], S[:, 1, 1] = V[:, 0], V[:, 1]
    S[:, 0, 1] = S[:, 1, 0] = rho * np.sqrt(V[:, 0] * V[:, 1])
    ad = adequacy(std_resid(a, S))
    chk("10.5 Q stats", ad[[0, 2, 4, 6]], [30.25, 16.56, 48.91, 33.03], 2, slack=1)
    chk("10.5 Q pvals", ad[[1, 3, 5, 7]], [0.066, 0.682, 0.158, 0.775], 3, slack=1)
    # standard errors over the interior parameters only (B1[0,1] sits on its bound 0)
    free = [i for i in range(13) if not (4 <= i < 12 and rf.x[i] < 1e-4)]
    chk("10.5 full boundary params", [i for i in range(13) if i not in free], [9.0], 0)
    def nll_free(z):
        t = rf.x.copy(); t[free] = z
        return nll(t, True)
    sf = np.full(13, np.nan); sf[free] = se(nll_free, rf.x[free])
    chk("10.5 full params", rf.x, [0.339, 0.22, 3.532, 0.315, 0.098, 0.028, 0.008, 0.076, 0.821, 0.0, 0.063, 0.767, 0.78], 3, slack=2)
    chk("10.5 full se", sf, [0.199, 0.135, 0.818, 0.696, 0.021, 0.033, 0.014, 0.023, 0.027, np.nan, 0.056, 0.084, 0.013], 3, slack=3)
    a, V, rho, a0, A1, B1 = parts(rf.x, True)
    S[:, 0, 0], S[:, 1, 1] = V[:, 0], V[:, 1]
    S[:, 0, 1] = S[:, 1, 0] = rho * np.sqrt(V[:, 0] * V[:, 1])
    ad = adequacy(std_resid(a, S))
    chk("10.5 full Q stats", ad[[0, 2, 4, 6]], [28.62, 7.98, 45.45, 21.76], 2, slack=1)
    chk("10.5 full Q pvals", ad[[1, 3, 5, 7]], [0.095, 0.992, 0.255, 0.992], 3, slack=1)
    chk("10.5 full eig(A1+B1)", np.sort(np.abs(np.linalg.eigvals(A1 + B1))), [0.8218, 0.9392], 4, slack=1)
    # 1-step forecast at origin T (Dec 2008), full model
    aT, VT = a[-1], V[-1]
    chk("10.5 full a_T, sigma_T", np.r_[aT, VT], [-6.67, -0.0, 134.63, 60.18], 2, slack=1)
    vf = a0 + A1 @ aT ** 2 + B1 @ VT
    chk("10.5 full forecast s11,s22,s12", [vf[0], vf[1], rho * np.sqrt(vf[0] * vf[1])], [118.41, 55.31, 63.12], 2, slack=1)  # text shows 63.12 from rounded inputs
    chk("10.5 full a0,A1,B1,rho 4 dec", rf.x[2:], [3.5323, 0.3147, 0.0976, 0.0281, 0.0076, 0.0758, 0.821, 0.0, 0.0633, 0.7665, 0.78], 4, slack=2)
    chk("10.5 full a_T, sigma_T 3 dec", np.r_[aT, VT], [-6.67, -0.005, 134.627, 60.177], 3, slack=2)
    chk("10.5 full forecast terms a0, A1 a^2, B1 sigma", np.r_[a0, A1 @ aT ** 2, B1 @ VT], [3.532, 0.315, 4.342, 0.339, 110.534, 54.654], 3)
    chk("10.5 full A21 5 dec", A1[1, 0], 0.00762, 5, slack=1)
    chk("10.5 full B11 5 dec, A11 5 dec", [B1[0, 0], A1[0, 0], B1[1, 0], B1[1, 1], A1[1, 1]], [0.82104, 0.0976, 0.06334, 0.76651, 0.07584], 5)
    a, V, rho, a0, A1, B1 = parts(rd.x, False)
    # 1-step forecast at origin T (Dec 2008), diagonal model
    aT, VT = a[-1], V[-1]
    chk("10.5 a_T, sigma_T", np.r_[aT, VT], [-6.67, -0.01, 122.82, 53.39], 2, slack=1)
    vf = a0 + np.diag(A1) * aT ** 2 + np.diag(B1) * VT
    cf = rho * np.sqrt(vf[0] * vf[1])
    chk("10.5 forecast s11,s22,s12", [vf[0], vf[1], cf], [110.31, 46.91, 56.17], 2, slack=1)

    # ---- 10.6 DCC (Tse-Tsui form, Tsay Eq. 10.32), GE IBM SP, two-step Gaussian QMLE
    k = 3
    R0 = R
    vm3 = VAR(R0).fit(3)
    R = vm3.resid       # shocks of the VAR(3) mean equation
    T = len(R)
    chk("10.6 Q_3(5) returns, VAR(3) resid, p", [Qk(R0, 5), Qk(R, 5), stats.chi2.sf(Qk(R, 5), 45)], [107.97, 45.721, 0.442], 3)
    uni = []
    for i in range(k):
        y = R[:, i]
        f = lambda t: (lambda vv: 1e10 if np.any(vv <= 0) else 0.5 * np.sum(np.log(vv) + (y - t[0]) ** 2 / vv + LOG2PI))(garch_var(y - t[0], *t[1:]))
        ri = fit(f, [y.mean(), 0.05 * y.var(), 0.1, 0.85], [(None, None), (1e-6, None), (0, 1), (0, 1)])
        uni.append((ri.x, -ri.fun, se(f, ri.x)))
    chk("10.6 univariate GARCH (mu,a0,a1,b1) x3", np.ravel([u[0] for u in uni]),
        [0.273, 1.461, 0.112, 0.866, 0.129, 3.242, 0.105, 0.828, 0.205, 0.608, 0.127, 0.86], 3, slack=2)
    eps = np.column_stack([(R[:, i] - uni[i][0][0]) / np.sqrt(garch_var(R[:, i] - uni[i][0][0], *uni[i][0][1:])) for i in range(k)])
    rbar = np.corrcoef(R0.T)   # Tsay: "sample correlation matrix of the returns"
    chk("10.6 rhobar", rbar[np.tril_indices(3, -1)], [0.556, 0.828, 0.645], 3)
    m = 4
    pairs = list(zip(*np.tril_indices(k, -1)))
    cs = lambda v: np.r_[0, np.cumsum(v)]
    psi = {}
    for (i, j) in pairs:  # psi_{ij,t-1}: correlation of eps over t-m..t-1 (no demeaning), t >= m
        sij = cs(eps[:, i] * eps[:, j]); sii = cs(eps[:, i] ** 2); sjj = cs(eps[:, j] ** 2)
        p = np.full(T, rbar[i, j])
        t = np.arange(m, T)
        p[t] = (sij[t] - sij[t - m]) / np.sqrt((sii[t] - sii[t - m]) * (sjj[t] - sjj[t - m]))
        psi[(i, j)] = p

    def dcc_rho(th):
        out = {}
        for (i, j) in pairs:
            u = (1 - th[0] - th[1]) * rbar[i, j] + th[1] * np.r_[rbar[i, j], psi[(i, j)][:-1]]
            out[(i, j)] = rec(u, th[0], rbar[i, j])
        Rt = np.repeat(np.eye(k)[None], T, 0)
        for (i, j) in pairs:
            Rt[:, i, j] = Rt[:, j, i] = out[(i, j)]
        return Rt

    def nll_dcc(th):
        if th[0] < 0 or th[1] < 0 or th[0] + th[1] >= 0.999:
            return 1e10
        Rt = dcc_rho(th)
        sign, ld = np.linalg.slogdet(Rt)
        if np.any(sign <= 0):
            return 1e10
        return 0.5 * np.sum(ld + np.einsum("ti,tij,tj->t", eps, np.linalg.inv(Rt), eps) - (eps ** 2).sum(1))

    r = fit(nll_dcc, [0.8, 0.05], [(0, 0.99), (0, 0.99)])
    s = se(nll_dcc, r.x)
    lr = 2 * (nll_dcc([0.0, 0.0]) - r.fun)
    chk("10.6 theta2 (on rho_{t-1}), theta1 (on psi_{t-1}) [Tsay Eq. 10.32 labels]", r.x, [0.9228, 0.0454], 4, slack=2)
    chk("10.6 se", s, [0.0146, 0.008], 4, slack=3)
    chk("10.6 LR vs constant", lr, 142.94, 2, slack=1)
    Rt = dcc_rho(r.x)
    rng_ = [(Rt[:, i, j].min(), Rt[:, i, j].max()) for (i, j) in pairs]
    chk("10.6 corr ranges", np.ravel(rng_), [0.181, 0.751, 0.465, 0.901, 0.335, 0.793], 3, slack=1)
    vols = np.column_stack([np.sqrt(garch_var(R[:, i] - uni[i][0][0], *uni[i][0][1:])) for i in range(k)])
    S = vols[:, :, None] * Rt * vols[:, None, :]
    a = R - np.array([u[0][0] for u in uni])
    ad = adequacy(std_resid(a, S))
    chk("10.6 Q stats", ad[[0, 2, 4, 6]], [57.68, 50.23, 97.58, 86.7], 2, slack=1)
    chk("10.6 Q pvals", ad[[1, 3, 5, 7]], [0.097, 0.274, 0.275, 0.579], 3, slack=1)


# ============================================================================ G 10.4 (simulation check)
def g104():
    """Gibbs sampler for SUR with AR(1) disturbances u_j = R u_{j-1} + e_j, R = diag(rho)."""
    rng = np.random.default_rng(2007)
    S_, J = 2, 400
    beta = np.array([1.0, 0.5, -1.0, 2.0])
    rho = np.array([0.6, -0.3])
    Sig = np.array([[1.0, 0.5], [0.5, 2.0]])
    xr = rng.normal(size=(J, S_))
    X = np.zeros((J, S_, 4))
    X[:, 0, 0] = 1; X[:, 0, 1] = xr[:, 0]; X[:, 1, 2] = 1; X[:, 1, 3] = xr[:, 1]
    u = np.zeros((J, S_))
    u[0] = rng.multivariate_normal([0, 0], Sig)
    e = rng.multivariate_normal([0, 0], Sig, J)
    for j in range(1, J):
        u[j] = rho * u[j - 1] + e[j]
    y = np.einsum("jsk,k->js", X, beta) + u
    # priors: beta ~ N(0, 100 I), rho ~ N(0, I) truncated to (-1,1)^S, Sigma^{-1} ~ W(nu0 = S+2, R0 = I)
    B0i, P0i, nu0, R0i = np.eye(4) / 100, np.eye(S_), S_ + 2, np.eye(S_)
    G, burn = 3000, 500
    b, r, Si = np.zeros(4), np.zeros(S_), np.eye(S_)
    draws = []
    for g in range(G):
        ys = y[1:] - r * y[:-1]
        Xs = X[1:] - r[None, :, None] * X[:-1]
        B1 = np.linalg.inv(np.einsum("jsk,st,jtl->kl", Xs, Si, Xs) + B0i)
        bb = B1 @ np.einsum("jsk,st,jt->k", Xs, Si, ys)
        b = rng.multivariate_normal(bb, B1)
        uu = y - np.einsum("jsk,k->js", X, b)
        U = uu[:-1]                                   # rows: diag(u_{j-1}) as regressor of rho
        P1 = np.linalg.inv(np.einsum("js,st,jt->st", U, Si, U) + P0i)
        rr = P1 @ np.einsum("js,st,jt->s", U, Si, uu[1:])
        while True:
            r = rng.multivariate_normal(rr, P1)
            if np.all(np.abs(r) < 1):
                break
        ee = uu[1:] - r * uu[:-1]
        R1 = np.linalg.inv(R0i + ee.T @ ee)
        Si = stats.wishart.rvs(df=nu0 + J - 1, scale=R1, random_state=rng)
        if g >= burn:
            Sg = np.linalg.inv(Si)
            draws.append(np.r_[b, r, Sg[0, 0], Sg[0, 1], Sg[1, 1]])
    draws = np.array(draws)
    pm, psd = draws.mean(0), draws.std(0)
    truth = np.r_[beta, rho, 1.0, 0.5, 2.0]
    assert np.all(np.abs(pm - truth) < 3.5 * psd), "G 10.4: posterior mean far from truth"
    chk("G10.4 post mean", pm, [1.156, 0.589, -0.902, 2.106, 0.561, -0.344, 0.869, 0.473, 1.835], 3, slack=2)
    chk("G10.4 post sd", psd, [0.107, 0.039, 0.051, 0.061, 0.038, 0.044, 0.061, 0.068, 0.132], 3, slack=2)


if __name__ == "__main__":
    only = sys.argv[sys.argv.index("--only") + 1].split(",") if "--only" in sys.argv else None
    for f in (e81, e82, e85, e87, e97, e10_ibm, e10_ge, g104):
        if only and f.__name__ not in only:
            continue
        f()
        print(f"{f.__name__}: OK")
    print(f"ALL CHECKS PASSED ({N_CHECKS} assertions)")
