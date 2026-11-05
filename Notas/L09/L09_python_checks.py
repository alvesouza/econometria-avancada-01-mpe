"""Class 9 (L09) reference implementation, with assert self-checks against the sources' numbers.

Run:  python Notas/L09/L09_python_checks.py      (stops at the first failed assert)

Sections §1-§7 are the code blocks of L09-10-python.md, in the same order. The model routines
(companion, psi, fevd, minnesota_posterior, lagmat) and the printed matrices are imported from
figures/make_figures.py (reuse, not a copy; importing it draws nothing). Equation numbers "(k)"
refer to the section note named in each header. Simulations are seeded.
"""
import pathlib
import sys

import numpy as np
from scipy import stats
import statsmodels.api as sm
from statsmodels.tsa.api import VAR
from statsmodels.tsa.vector_ar.var_model import VARProcess
from statsmodels.tsa.vector_ar.svar_model import SVAR

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / "figures"))
import make_figures as mf  # noqa: E402  printed matrices + model routines

sys.stdout.reconfigure(encoding="utf-8")


def near(x, printed, tol=5e-4):
    """True when x matches a printed number to within tol (default: half a unit in the 3rd decimal)."""
    return abs(float(x) - float(printed)) <= tol


def ok(msg):
    print("ok", msg)


# §1 · VAR(p) as a multivariate regression: OLS = MLE = SUR/GLS (L09-01 (11)-(13))
rng = np.random.default_rng(2025)
Lc = np.linalg.cholesky(mf.SIG_S)
Y = np.zeros((1200, 3))
for t in range(2, 1200):
    Y[t] = mf.MU_S + mf.B1_S @ Y[t - 1] + mf.B2_S @ Y[t - 2] + Lc @ rng.standard_normal(3)
Y = Y[200:]                                              # 1000 observations, as on slide 13
X, Yr = mf.lagmat(Y, 2)                                  # constant, lag 1, lag 2
Bhat_T = np.linalg.solve(X.T @ X, X.T @ Yr)              # (11): (X'X)^{-1} X'Y, one column per equation
res = VAR(Y).fit(2, trend="c")
assert np.allclose(Bhat_T, res.params, atol=1e-10)      # statsmodels params: rows = regressors
U = Yr - X @ Bhat_T
S_ml = U.T @ U / len(Yr)
Sig_inv = np.linalg.inv(S_ml)
n = 300                                                  # GLS on the first 300 rows (the n x n Kronecker is big)
Xg, Yg = X[:n], Yr[:n]
Bg = np.linalg.solve(Xg.T @ Xg, Xg.T @ Yg)
y_vec = Yg.T.reshape(-1)                                 # vec(Y): equation 1's n values, then 2's, 3's
Z = np.kron(np.eye(3), Xg)
gls = np.linalg.solve(Z.T @ np.kron(Sig_inv, np.eye(n)) @ Z, Z.T @ np.kron(Sig_inv, np.eye(n)) @ y_vec)
assert np.allclose(gls, Bg.T.reshape(-1), atol=1e-8)     # (12): GLS = OLS, Sigma drops out
cov = np.kron(res.sigma_u, np.linalg.inv(X.T @ X))       # (13): Sigma (x) (X'X)^{-1}
assert np.allclose(np.sqrt(np.diag(cov)), res.bse.T.reshape(-1), rtol=1e-8)
assert np.max(np.abs(Bhat_T[1:4].T - mf.B1_S)) < 0.1     # T = 1000 recovers slide 13's B1
ok("§1 OLS = statsmodels VAR = GLS on (5); se = sqrt diag(Sigma (x) (X'X)^-1)")

# §2 · Companion form, stationarity, means, forecasts (L09-01 (2), (14)-(18))
ev = np.linalg.eigvals(mf.companion([mf.B1_S, mf.B2_S]))
assert near(np.abs(ev).max(), 0.9099, 5e-5) and near(np.sort(np.abs(ev))[-2], 0.5329, 5e-5)
# (15): nonzero eigenvalues are reciprocals of the roots of |I - B1 z - B2 z^2| = 0
for lam in ev[np.abs(ev) > 1e-9]:
    z = 1 / lam
    assert abs(np.linalg.det(np.eye(3) - mf.B1_S * z - mf.B2_S * z**2)) < 1e-9
m = np.linalg.solve(np.eye(3) - mf.B1_S - mf.B2_S, mf.MU_S)
assert np.allclose(m, [6.875, 14.375, 30.9375])
assert near(np.abs(np.linalg.eigvals(mf.companion([mf.G1, mf.G2, mf.G3]))).max(), 0.6107, 5e-5)
# Tsay VAR(1), IBM and S&P 500 (pp. 414-416)
Phi = np.array([[-0.0320, 0.1503], [-0.0223, 0.1020]])
phi0 = np.array([1.0614, 0.4087])
mt = np.linalg.solve(np.eye(2) - Phi, phi0)
assert near(mt[0], 1.0909, 5e-4) and near(mt[1], 0.4280, 5e-4)     # 6-step forecasts printed
r = 3.5432 / np.hypot(3.5432, 4.2280)                                # innovation correlation 0.642
s1, s2 = 7.0078, 5.5247                                              # residual scales printed
Sig_t = np.array([[s1**2, r * s1 * s2], [r * s1 * s2, s2**2]])
G0 = np.linalg.solve(np.eye(4) - np.kron(Phi, Phi), Sig_t.reshape(-1, order="F")).reshape(2, 2, order="F")
assert near(np.sqrt(G0[0, 0]), 7.0436) and near(np.sqrt(G0[1, 1]), 5.5454, 2e-4)
mse2 = Sig_t + Phi @ Sig_t @ Phi.T                                   # (18), h = 2
assert near(np.sqrt(mse2[0, 0]), 7.0434) and near(np.sqrt(mse2[1, 1]), 5.5453, 2e-4)
# parameter counts (slides 27, 45)
assert [q * q + q * (q + 1) // 2 for q in (3, 20, 131)] == [15, 610, 25807] and 7 + 6 * 49 == 301
ok("§2 companion roots, mean (6.875, 14.375, 30.94), Tsay forecast limits 7.0436 / 5.5454")

# §3 · VMA weights, orthogonalised IRFs, FEVD, recursive SVAR (L09-02 (3), (6), (8); L09-03 (9)-(11))
P = mf.psi([mf.G1, mf.G2, mf.G3], 6)
proc = VARProcess(np.array([mf.G1, mf.G2, mf.G3]), np.zeros(3), mf.SH)
assert np.allclose(np.array(P), proc.ma_rep(5))                      # (3) = statsmodels ma_rep
assert near(P[2][0, 0], 0.2495, 5e-5) and near(P[3][0, 1], 0.3335, 5e-5)
Th = proc.orth_ma_rep(5)
assert np.allclose(Th[1], P[1] @ np.linalg.cholesky(mf.SH)) and near(Th[1][2, 1], 0.4496, 5e-5)
L0 = np.array([[6.9973, 0], [3.5432, 4.2280]])                       # Tsay impRes lag 0
T1 = Phi @ L0
assert all(near(a, b, 5e-4) for a, b in zip(T1.ravel(), [0.3088, 0.6353, 0.2050, 0.4312]))
f1, f20 = mf.fevd([mf.R1, mf.R2, mf.R3], mf.SR, 1), mf.fevd([mf.R1, mf.R2, mf.R3], mf.SR, 20)
assert near(f1[1, 0], 0.07578528, 1e-6) and near(f1[2, 1], 0.1599804, 1e-6)
assert near(f20[0, 0], 0.8774260, 1e-3) and near(f20[1, 0], 0.2657297, 1e-3) and near(f20[2, 2], 0.43585314, 1e-3)
# Tsay Ex. 8.3: both recursive orderings
Phi83, phi083, S83 = np.array([[0.2, 0.3], [-0.6, 1.1]]), np.array([0.2, 0.4]), np.array([[2.0, 1.0], [1.0, 1.0]])
Lunit = np.array([[1.0, 0.0], [0.5, 1.0]])                      # unit-diagonal L, ordering (r1, r2)
Gd = np.linalg.inv(Lunit) @ S83 @ np.linalg.inv(Lunit).T
assert np.allclose(Gd, np.diag([2.0, 0.5]))
assert np.allclose(np.linalg.inv(Lunit) @ phi083, [0.2, 0.3]) and np.allclose(np.linalg.inv(Lunit) @ Phi83, [[0.2, 0.3], [-0.7, 0.95]])
Pm = np.array([[0, 1], [1, 0]])
Linv_b = np.array([[1.0, 0.0], [-1.0, 1.0]])
assert np.allclose(Linv_b @ Pm @ S83 @ Pm @ Linv_b.T, np.eye(2))
assert np.allclose(Linv_b @ Pm @ phi083, [0.4, -0.2]) and np.allclose(Linv_b @ Pm @ Phi83 @ Pm, [[1.1, -0.6], [-0.8, 0.8]])
# statsmodels SVAR with a lower-triangular A recovers A^{-1} = Cholesky of Sigma-hat (L09-03 (9))
rng = np.random.default_rng(83)
Ls = np.linalg.cholesky(S83)
Ysv = np.zeros((3000, 2))
for t in range(1, 3000):
    Ysv[t] = phi083 + Phi83 @ Ysv[t - 1] + Ls @ rng.standard_normal(2)
mask = np.array([["E", 0], ["E", "E"]], dtype=object)
sres = SVAR(Ysv[100:], svar_type="A", A=mask).fit(maxlags=1, trend="c", A_guess=np.array([1.0, -0.5, 1.0]))
Ainv = np.linalg.inv(sres.A)
Pchol = np.linalg.cholesky(VAR(Ysv[100:]).fit(1, trend="c").sigma_u)
assert np.allclose(np.abs(Ainv), np.abs(Pchol), atol=0.02)
ok("§3 Psi recursion = ma_rep; Tsay Theta_1; FEVD = MTS table; Ex. 8.3 orderings; SVAR A^-1 = chol")

# §4 · Minnesota posterior, limits in lambda, SSVS inclusion probability (L09-04 (2), (7)-(9), (15))
rng = np.random.default_rng(9)                           # the figure's simulation, same seed
Ym = np.zeros((260, 3))
for t in range(2, 260):
    Ym[t] = mf.MU_S + mf.B1_S @ Ym[t - 1] + mf.B2_S @ Ym[t - 2] + Lc @ rng.standard_normal(3)
Ym = Ym[200:]
Xm, Yrm = mf.lagmat(Ym, 2)
s2 = []
for i in range(3):
    Xi, yi = mf.lagmat(Ym[:, [i]], 2)
    e = yi[:, 0] - Xi @ np.linalg.lstsq(Xi, yi, rcond=None)[0][:, 0]
    s2.append(e.var(ddof=3))
s2 = np.array(s2)
assert np.allclose(s2, [0.266, 0.1257, 0.8046], atol=5e-4)


def minnesota_eq(i, lam, theta=0.5, p=2):
    """Posterior mean of equation i under (2), constant variance 1e6, theta = 0.5 (illustrative)."""
    g0 = np.zeros(1 + 3 * p)
    g0[1 + i] = 1.0
    v0 = [1e6] + [(lam / k) ** 2 * (1 if j == i else theta**2 * s2[i] / s2[j]) for k in range(1, p + 1) for j in range(3)]
    return mf.minnesota_posterior(Yrm[:, i], Xm, g0, np.array(v0), s2[i])[0]


ols = np.linalg.lstsq(Xm, Yrm[:, 0], rcond=None)[0]
assert np.allclose(ols[1:5], [0.647, 0.379, -0.021, -0.292], atol=5e-4)
for lam, row in ((0.05, [0.926, 0.000, -0.010, -0.018]), (0.2, [0.690, 0.055, -0.043, -0.115]),
                 (1.0, [0.649, 0.284, -0.038, -0.262])):
    assert np.allclose(minnesota_eq(0, lam)[1:5], row, atol=5e-4), (lam, minnesota_eq(0, lam)[1:5])
assert np.allclose(minnesota_eq(0, 1e-6)[1:], [1, 0, 0, 0, 0, 0], atol=1e-6)      # lambda -> 0: prior
assert np.allclose(minnesota_eq(0, 1e4)[1:], ols[1:], atol=1e-5)                    # lambda -> inf: OLS
assert near(0.1 * np.sqrt(s2[0] / s2[1]), 0.145) and near(0.1 * np.sqrt(s2[0] / s2[2]), 0.057)
# (9): scalar shrinkage weight equals (7) with one regressor
x1 = Xm[:, 1]
y1 = Yrm[:, 0] - Yrm[:, 0].mean()
x1 = x1 - x1.mean()
v0, b0, sig2 = 0.04, 1.0, s2[0]
post = mf.minnesota_posterior(y1, x1[:, None], np.array([b0]), np.array([v0]), sig2)[0][0]
bhat = x1 @ y1 / (x1 @ x1)
w = (sig2 / (x1 @ x1)) / (sig2 / (x1 @ x1) + v0)
assert near(post, w * b0 + (1 - w) * bhat, 1e-12)
# SSVS (15) with c0 = 0.1, c1 = 10, q = 1/2
incl = lambda z: 0.1 * stats.norm.pdf(z / 10) / (0.1 * stats.norm.pdf(z / 10) + 10 * stats.norm.pdf(10 * z))
assert near(incl(0.2), 0.069) and near(incl(0.5), 0.9996, 5e-5)
zstar = np.sqrt(2 * np.log(100) / (100 - 0.01))
assert near(zstar, 0.3035, 5e-5) and near(incl(zstar), 0.5, 1e-12)
ok("§4 Minnesota table, both limits, scalar weight (9), SSVS 0.069 / 0.9996 / z* = 0.3035")

# §5 · Factor model algebra (L09-05 (2)-(9))
beta = np.array([[0.99, 0], [0, 0.99], [0.90, 0], [0, 0.90], [0.50, 0.50]])
psi_ = np.array([0.01, 0.05, 0.10, 0.15, 0.20])
Om = beta @ beta.T + np.diag(psi_)
assert near(Om[0, 0], 0.9901, 1e-12) and near(Om[0, 2], 0.891, 1e-12) and near(Om[4, 4], 0.70, 1e-12)
comm = (beta**2).sum(1) / np.diag(Om)
assert np.allclose(comm, [0.990, 0.951, 0.890, 0.844, 0.714], atol=5e-4)
Vf = np.linalg.inv(np.eye(2) + beta.T @ np.diag(1 / psi_) @ beta)
assert np.allclose(Vf, [[0.00923, -0.00042], [-0.00042, 0.03671]], atol=5e-6)
Qr, _ = np.linalg.qr(np.random.default_rng(5).standard_normal((2, 2)))           # random rotation
assert np.allclose((beta @ Qr.T) @ (beta @ Qr.T).T, beta @ beta.T)                 # (4)
for mm, kk in {6: 3, 12: 7, 20: 14, 50: 40}.items():
    assert int(np.floor((2 * mm + 1 - np.sqrt(8 * mm + 1)) / 2)) == kk             # (7)
fx_load = {"US": (0.99, 0.00, 0.05), "JAP": (0.46, 0.42, 0.62), "FRA": (0.39, 0.91, 0.04)}
assert [round(a * a + b * b + s, 3) for a, b, s in fx_load.values()] == [1.030, 1.008, 1.020]
assert near(0.41 * 0.40 + 0.77 * 0.77, 0.757)
ok("§5 Omega, communalities, V_f, rotation invariance, k bound, exchange-rate check")

# §6 · Kalman filter, steady state, ARIMA link, discounting (L09-06 (8)-(14), (18); (3))
se, sn = 0.4803, 0.0735
q = (sn / se) ** 2
pstar = (q + np.sqrt(q * q + 4 * q)) / 2
Kstar = pstar / (pstar + 1)
assert near(q, 0.023418, 5e-7) and near(pstar, 0.165186, 5e-7) and near(Kstar, 0.14177, 5e-6)
assert near(1 - Kstar, 0.858)                                                     # = theta-hat of (11.6)
sa, th = 0.5184, 0.858
assert near(np.sqrt(th * sa**2), 0.4802) and near(np.sqrt((1 + th**2) * sa**2 - 2 * th * sa**2), 0.0736)


def kalman_llevel(y, s2e, s2n, m1, P1):
    """Local-level Kalman filter, Tsay eq. (11.14). Returns filtered means, gains, log-likelihood (11.25)."""
    mu, P, out, Ks, ll = m1, P1, [], [], 0.0
    for yt in y:
        v, V = yt - mu, P + s2e
        K = P / V
        ll += -0.5 * (np.log(2 * np.pi) + np.log(V) + v * v / V)
        mu_f, P_f = mu + K * v, P * (1 - K)
        out.append(mu_f)
        Ks.append(K)
        mu, P = mu_f, P_f + s2n
    return np.array(out), np.array(Ks), ll


rng = np.random.default_rng(11)
state = np.cumsum(sn * rng.standard_normal(340))
yk = state + se * rng.standard_normal(340)
filt, Ks, ll = kalman_llevel(yk, se**2, sn**2, 0.0, 10.0)
mod = sm.tsa.UnobservedComponents(yk, level="llevel")
mod.ssm.initialize_known(np.array([0.0]), np.array([[10.0]]))
sres_k = mod.smooth([se**2, sn**2])
assert np.allclose(filt, sres_k.filtered_state[0], atol=1e-8) and near(ll, sres_k.llf_obs.sum(), 1e-6)  # llf drops t = 1 (loglikelihood_burn)
assert abs(Ks[14] - Kstar) < 0.005 and near(Ks[0], 10 / (10 + se**2), 1e-12)     # "within about 15 days"
# (18): discounting makes P_{t|t-1} = P_{t-1|t-1}/delta
delta, Pf = 0.99, 0.37
assert near(Pf + (1 / delta - 1) * Pf, Pf / delta, 1e-15)
# (3): Uhlig scalar case, E theta = a/(a+1/2) for theta ~ Beta(a, 1/2)
a = (5 + 2) / 2
assert near(stats.beta(a, 0.5).mean(), a / (a + 0.5), 1e-12) and near(a / (a + 0.5), 7 / 8, 1e-12)
ok("§6 K* = 0.1418 = 1 - 0.858; filter = statsmodels UnobservedComponents; discount and Uhlig identities")

# §7 · EWMA, DCC and GARCH persistence, FSV implied correlation (L09-07 (1)-(2), (6), (11)-(12))
rng = np.random.default_rng(7)
A = rng.standard_normal((400, 2))
lam_e = 0.94
t0 = 400
w = (1 - lam_e) * lam_e ** np.arange(t0 - 1) / (1 - lam_e ** (t0 - 1))
S_direct = sum(wj * np.outer(A[t0 - 1 - j], A[t0 - 1 - j]) for j, wj in enumerate(w))
S_rec = np.outer(A[0], A[0])
for t in range(1, t0):
    S_rec = (1 - lam_e) * np.outer(A[t], A[t]) + lam_e * S_rec
assert np.allclose(S_direct, S_rec, atol=1e-9) and near(w.sum(), 1.0, 1e-12)     # (1) = (2) for large t
s_engle, s_tt = 0.8703852 + 0.03813264, 0.7017527 + 0.049999
assert near(np.log(0.5) / np.log(s_engle), 7.22, 5e-3) and near(np.log(0.5) / np.log(s_tt), 2.43, 5e-3)
assert near(s_engle**10, 0.383) and near(s_tt**10, 0.058)
om, al, be = 1.29849458, 0.1061140, 0.8432337
assert near(om / (1 - al - be), 25.635, 5e-3) and near(np.log(0.5) / np.log(al + be), 13.33, 5e-3)
assert 0.1964253 + 0.8065090 > 1
nu = 5.464443
assert near(3 * (nu - 2) / (nu - 4), 7.1, 0.05)
rho11 = lambda b1, b2, p1, p2, h: b1 * b2 * h / np.sqrt((b1**2 * h + p1) * (b2**2 * h + p2))
rho12 = lambda b1, b2, p1, p2, h: np.sign(b1 * b2) / np.sqrt((1 + p1 / b1**2 / h) * (1 + p2 / b2**2 / h))
hh = np.exp(np.linspace(-6, 3, 200))
assert np.allclose(rho11(0.99, 0.9, 0.01, 0.1, hh), rho12(0.99, 0.9, 0.01, 0.1, hh))
assert np.all(np.diff(rho11(0.99, 0.9, 0.01, 0.1, hh)) > 0)                        # increasing in h
assert near(rho11(0.99, 0.9, 0.01, 0.1, 1.0), 0.9387, 5e-5) and near(rho11(0.99, 0.9, 0.01, 0.1, 0.05), 0.4893, 5e-5)
ok("§7 EWMA recursion, DCC half-lives 7.22 / 2.43, GARCH 25.6 and 13.3 days, FSV correlation (11) = (12)")

print("ALL L09 CHECKS PASSED")
