"""Reproduce and assert every number printed in Listas/lista-poisson-monte-carlo.tex.

Run from anywhere: ``python Listas/poisson-monte-carlo-check.py``. Each ``ok(value, "printed")``
asserts that ``value`` rounds to the printed string (tolerance = half a unit of the last printed
decimal), so a change in data, seed or library that moves a printed digit aborts the script.
Proofs are checked numerically (``close``): closed forms against enumeration, quadrature or
seeded simulation.

Data: British coal-mining disasters 1851-1962 (Jarrett 1979; Carlin, Gelfand and Smith 1992),
typed below and verified in .agent/notes/coal-mining-data.md. Every stochastic result uses a
fixed NumPy seed (``np.random.default_rng``); another NumPy version may change the random
stream and fail those lines.
"""
import numpy as np
import statsmodels.api as sm
from scipy import integrate, optimize, special, stats

N_OK = 0
np.seterr(divide="ignore", invalid="ignore")      # 0 log 0 branches are masked by np.where


def ok(value, printed):
    """Assert ``value`` matches the printed decimal string ``printed`` to its last digit."""
    global N_OK
    dec = len(printed.split(".")[1]) if "." in printed else 0
    tol = 0.5 * 10 ** (-dec) + 1e-12
    assert abs(float(value) - float(printed)) <= tol, f"{value!r} does not print as {printed}"
    N_OK += 1


def close(a, b, rtol=1e-9, atol=1e-12):
    """Assert two numerically computed quantities agree (closed form vs independent route)."""
    global N_OK
    assert np.allclose(a, b, rtol=rtol, atol=atol), f"{a!r} != {b!r}"
    N_OK += 1


Y = np.array([4, 5, 4, 1, 0, 4, 3, 4, 0, 6, 3, 3, 4, 0, 2, 6, 3, 3, 5, 4, 5, 3, 1, 4, 4, 1, 5, 5, 3, 4,
              2, 5, 2, 2, 3, 4, 2, 1, 3, 2, 2, 1, 1, 1, 1, 3, 0, 0, 1, 0, 1, 1, 0, 0, 3, 1, 0, 3, 2, 2,
              0, 1, 1, 1, 0, 1, 0, 1, 0, 0, 0, 2, 1, 0, 0, 0, 1, 1, 0, 2, 3, 3, 1, 1, 2, 1, 1, 1, 1, 2,
              4, 2, 0, 0, 0, 1, 4, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1])
assert (len(Y), Y.sum(), Y[:41].sum(), Y[:40].sum()) == (112, 191, 127, 125)
Y41 = Y[:41]                                    # 1851-1891
Z975, Z95 = stats.norm.ppf(0.975), stats.norm.ppf(0.95)
R = {}                                          # every printed number, keyed by question
pois = stats.poisson


# ================================================================ Block 1
def cond_pmf(t, theta, w2):
    """P(X1=x1, X2=x2 | X1 + w2*X2 = t) for X1, X2 i.i.d. Poisson(theta), by enumeration."""
    pts = [(t - w2 * x2, x2) for x2 in range(t // w2 + 1)]
    pr = np.array([pois.pmf(a, theta) * pois.pmf(b, theta) for a, b in pts])
    return pts, pr / pr.sum()


# Q1  B 2.4: T = X1 + 2 X2 versus S = X1 + X2
for th in (1.0, 2.0):
    pts, pr = cond_pmf(2, th, 2)
    R[f"q1_T2_{th:g}"] = pr[pts.index((2, 0))]
    close(pr[pts.index((2, 0))], th / (th + 2))
    pts, pr = cond_pmf(4, th, 2)
    for (a, b), v in zip(pts, pr):
        R[f"q1_T4_{th:g}_{a}{b}"] = v
    pts, pr = cond_pmf(4, th, 1)                # S = 4: Binomial(4, 1/2) whatever theta
    close(pr, stats.binom.pmf([4 - b for _, b in pts], 4, 0.5))

# Q2  B 2.6: information identity, Poisson(3) (holds) and U(0, 2) (fails)
th = 3.0
x = np.arange(0, 400)
f = pois.pmf(x, th)
score, hess = x / th - 1, -x / th ** 2
R["q2_Es2"], R["q2_mEh"], R["q2_Es"] = np.sum(f * score ** 2), -np.sum(f * hess), np.sum(f * score)
close(R["q2_Es2"], 1 / th); close(R["q2_mEh"], 1 / th); close(R["q2_Es"], 0.0, atol=1e-12)
th = 2.0                                        # U(0, theta): log f = -log theta on (0, theta)
R["q2_U_Es2"] = integrate.quad(lambda u: (-1 / th) ** 2 / th, 0, th)[0]
R["q2_U_mEh"] = -integrate.quad(lambda u: (1 / th ** 2) / th, 0, th)[0]
R["q2_U_Es"] = integrate.quad(lambda u: (-1 / th) / th, 0, th)[0]

# Q3  B 2.5: CR bound for theta; Xbar attains it, S^2 does not (theta = 2, n = 10)
th, n, Rr = 2.0, 10, 200_000
rng = np.random.default_rng(3)
X = rng.poisson(th, size=(Rr, n))
xb, s2 = X.mean(1), X.var(1, ddof=1)
R["q3_CR"], R["q3_vS2"] = th / n, th / n + 2 * th ** 2 / (n - 1)
R["q3_mean_xb"], R["q3_var_xb"] = xb.mean(), xb.var(ddof=1)
R["q3_mean_s2"], R["q3_var_s2"] = s2.mean(), s2.var(ddof=1)
# exact Var(S^2) by the central-moment formula mu4/n - sigma^4 (n-3)/(n(n-1)) for Poisson
close(R["q3_vS2"], (th + 3 * th ** 2) / n - th ** 2 * (n - 3) / (n * (n - 1)))

# Q4  original: estimating psi = exp(-theta) = P(X = 0)
th, n = 1.5, 10
R["q4_psi"] = np.exp(-th)
R["q4_Emle"] = np.exp(n * th * (np.exp(-1 / n) - 1))
R["q4_biasmle"] = R["q4_Emle"] - R["q4_psi"]
R["q4_varU"] = np.exp(-2 * th) * (np.exp(th / n) - 1)
R["q4_CR"] = np.exp(-2 * th) * th / n
R["q4_ratio"] = R["q4_varU"] / R["q4_CR"]
R["q4_mseMLE"] = (np.exp(n * th * (np.exp(-2 / n) - 1)) - 2 * R["q4_psi"] * R["q4_Emle"]
                  + R["q4_psi"] ** 2)
tt = np.arange(0, 200)                          # exact checks by summing over T ~ Poisson(n theta)
pt = pois.pmf(tt, n * th)
close(np.sum(pt * np.exp(-tt / n)), R["q4_Emle"])
close(np.sum(pt * (1 - 1 / n) ** tt), R["q4_psi"])
close(np.sum(pt * (1 - 1 / n) ** (2 * tt)) - R["q4_psi"] ** 2, R["q4_varU"])
rng = np.random.default_rng(4)
T = rng.poisson(th, size=(200_000, n)).sum(1)
mle, umvu = np.exp(-T / n), (1 - 1 / n) ** T
R["q4_sim_mle_mean"], R["q4_sim_umvu_mean"] = mle.mean(), umvu.mean()
R["q4_sim_umvu_var"], R["q4_sim_mle_mse"] = umvu.var(ddof=1), np.mean((mle - R["q4_psi"]) ** 2)
for nn in (1, 2, 5, 10, 50, 1000):              # ratio decreasing in n, -> 1
    R[f"q4_ratio_n{nn}"] = (np.exp(th / nn) - 1) / (th / nn)


# ================================================================ Block 2
# Q6  B 6.5: UMP test for theta0 = 1, n = 25, alpha = 0.05
n, th0, al = 25, 1.0, 0.05
R["q6_c"] = th0 + Z95 * np.sqrt(th0 / n)
R["q6_z15"] = (round(R["q6_c"], 6) - 1.5) / np.sqrt(1.5 / n)
pw_clt = lambda t: 1 - stats.norm.cdf((R["q6_c"] - t) / np.sqrt(t / n))
cT = int(pois.ppf(1 - al, n * th0))             # smallest c with P(T > c) <= alpha
while pois.sf(cT, n * th0) > al:
    cT += 1
while pois.sf(cT - 1, n * th0) <= al:
    cT -= 1
R["q6_cT"] = cT
R["q6_size_exact"] = pois.sf(cT, n * th0)
gam = (al - pois.sf(cT, n * th0)) / pois.pmf(cT, n * th0)
R["q6_gamma"] = gam
for t in (1.0, 1.2, 1.5, 2.0):
    R[f"q6_pclt_{t:g}"] = pw_clt(t)
    R[f"q6_pex_{t:g}"] = pois.sf(cT, n * t)
    R[f"q6_prand_{t:g}"] = pois.sf(cT, n * t) + gam * pois.pmf(cT, n * t)
close(R["q6_prand_1"], al)
R["q6_plot"] = [(t, pw_clt(t)) for t in np.round(np.arange(0.8, 2.21, 0.1), 1)]

# Q7  B 6.11: two-sample Poisson LR test with the printed sums 3.8 and 4.8
n, m, sx, sy = 5, 8, 3.8, 4.8
xb, yb, th0h = sx / n, sy / m, (sx + sy) / (n + m)
R["q7_xb"], R["q7_yb"], R["q7_th0"] = xb, yb, th0h
R["q7_t1"], R["q7_t2"] = sx * np.log(xb / th0h), sy * np.log(yb / th0h)
R["q7_LR"] = 2 * (R["q7_t1"] + R["q7_t2"])
R["q7_p"] = stats.chi2.sf(R["q7_LR"], 1)
R["q7_crit"] = stats.chi2.ppf(0.95, 1)


def lr2(sx, sy, n, m):
    """-2 log Lambda for H0: theta1 = theta2, two Poisson samples summarized by their totals."""
    th0 = (sx + sy) / (n + m)
    t = lambda s, k: np.where(s > 0, s * np.log(np.where(s > 0, s, 1) / (k * th0)), 0.0)
    return 2 * (t(sx, n) + t(sy, m))


rng = np.random.default_rng(7)
for th in (0.66, 3.0):
    sxs, sys_ = rng.poisson(n * th, 100_000), rng.poisson(m * th, 100_000)
    R[f"q7_size_{th:g}"] = np.mean(lr2(sxs, sys_, n, m) > R["q7_crit"])

# Q8  original: Wald, score and exact (Garwood) intervals; exact coverage for n = 10
def intervals(t, n, z=Z975, al=0.05):
    """Wald, score and Garwood 95% intervals for a Poisson mean from the total t of n counts."""
    xb = t / n
    wald = (xb - z * np.sqrt(xb / n), xb + z * np.sqrt(xb / n))
    ctr, hw = xb + z ** 2 / (2 * n), z * np.sqrt(xb / n + z ** 2 / (4 * n ** 2))
    score = (ctr - hw, ctr + hw)
    lo = 0.0 if t == 0 else stats.gamma.ppf(al / 2, t) / n
    exact = (lo, stats.gamma.ppf(1 - al / 2, t + 1) / n)
    return wald, score, exact


def coverage(th, n):
    """Exact coverage of the three intervals: sum of P(T = t) over t whose interval covers th."""
    tmax = int(pois.ppf(1 - 1e-12, n * th)) + 5
    cov = np.zeros(3)
    for t in range(tmax + 1):
        p = pois.pmf(t, n * th)
        for j, (lo, hi) in enumerate(intervals(t, n)):
            cov[j] += p * (lo <= th <= hi)
    return cov


for th in (0.1, 1.0, 5.0):
    cov = coverage(th, 10)
    for j, nm in enumerate(("wald", "score", "exact")):
        R[f"q8_cov_{nm}_{th:g}"] = cov[j]
# Garwood identity P(T <= t; mu) = P(Gamma(t + 1, 1) > mu)
for t, mu in [(0, 0.7), (3, 2.5), (12, 9.1)]:
    close(pois.cdf(t, mu), stats.gamma.sf(mu, t + 1))
for nm, (lo, hi) in zip(("wald", "score", "exact"), intervals(127, 41)):
    R[f"q8_coal_{nm}_lo"], R[f"q8_coal_{nm}_hi"] = lo, hi
R["q8_zero_score_hi"] = intervals(0, 12)[1][1]


# ================================================================ Block 3
# Q10  Greenberg 3.8: Bayes factors (G(1,1) priors), plus a prior-sampling Monte Carlo check
def log10B(m, e1, e2):
    """log10 B12 of Greenberg 3.8 from the closed form (per-page factorials cancel)."""
    e = e1 + e2
    return (special.gammaln(e + 1) + (e + 2) * np.log(m + 1) - (e + 1) * np.log(2 * m + 1)
            - special.gammaln(e1 + 1) - special.gammaln(e2 + 1)) / np.log(10)


for m, e in ((100, 10), (200, 20)):
    for p in (0.9, 0.8, 0.7, 0.6, 0.5):
        e1 = round(p * e)
        R[f"q10_{m}_{p:g}"] = log10B(m, e1, e - e1)
        m1 = integrate.quad(lambda t: t ** e * np.exp(-(2 * m + 1) * t), 0, 1, epsabs=0, epsrel=1e-12, limit=200)[0]
        g = lambda t, k: t ** k * np.exp(-(m + 1) * t)
        m2 = (integrate.quad(g, 0, 1, args=(e1,), epsabs=0, epsrel=1e-12, limit=200)[0]
              * integrate.quad(g, 0, 1, args=(e - e1,), epsabs=0, epsrel=1e-12, limit=200)[0])
        close(np.log10(m1 / m2), R[f"q10_{m}_{p:g}"], rtol=1e-6)
R["q10_num"] = special.gammaln(11) + 12 * np.log(101) - 11 * np.log(201) - special.gammaln(10)
rng = np.random.default_rng(10)
G, m, e1, e2 = 1_000_000, 100, 9, 1
h1 = lambda t, k, rate: np.exp(k * np.log(t) - rate * t)
d1 = h1(rng.exponential(1.0, G), e1 + e2, 2 * m)
d2a, d2b = h1(rng.exponential(1.0, G), e1, m), h1(rng.exponential(1.0, G), e2, m)
m1h, m2a, m2b = d1.mean(), d2a.mean(), d2b.mean()
R["q10_mc"] = np.log10(m1h / (m2a * m2b))
cv2 = lambda d: d.var(ddof=1) / (G * d.mean() ** 2)       # squared relative MC error
R["q10_mc_se"] = np.sqrt(cv2(d1) + cv2(d2a) + cv2(d2b)) / np.log(10)

# Q11  Greenberg 7.3: Gibbs sampler for the switch point (same code and seed as L01)
y, n, S = Y, 112, 191
cs, ks = np.cumsum(y), np.arange(1, n + 1)
a0, b0 = 0.5, 1.0
lfact = special.gammaln(y + 1).sum()
lgp = lambda sh, rt: (a0 * np.log(b0) - special.gammaln(a0) + special.gammaln(a0 + sh)
                      - (a0 + sh) * np.log(b0 + rt))
lk = -np.log(n) - lfact + lgp(cs, ks) + lgp(S - cs, n - ks)
R["q11_logm"] = special.logsumexp(lk)
pk = np.exp(lk - R["q11_logm"])
for kv in (41, 40, 39, 42, 37, 36):
    R[f"q11_pk_{kv}"] = pk[kv - 1]
R["q11_Et1"], R["q11_Et2"] = np.sum(pk * (a0 + cs) / (b0 + ks)), np.sum(pk * (a0 + S - cs) / (b0 + n - ks))
rng = np.random.default_rng(2026)
G, burn, k = 10000, 1000, n // 2
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
R["q11_m1"], R["q11_s1"], R["q11_m2"], R["q11_s2"] = th1.mean(), th1.std(ddof=1), th2.mean(), th2.std(ddof=1)
R["q11_q1"], R["q11_q2"] = np.quantile(th1, [0.025, 0.975]), np.quantile(th2, [0.025, 0.975])
R["q11_kmean"] = kk.mean()
for kv in (41, 40, 39, 42, 37, 36):
    R[f"q11_gpk_{kv}"] = np.mean(kk == kv)
R["q11_p3646"] = np.mean((kk >= 36) & (kk <= 46))
t1s, t2s = th1.mean(), th2.mean()
R["q11_loglik"] = special.logsumexp(-np.log(n) + cs * np.log(t1s) - ks * t1s
                                    + (S - cs) * np.log(t2s) - (n - ks) * t2s) - lfact
R["q11_lprior"] = stats.gamma.logpdf(t1s, a0, scale=1 / b0) + stats.gamma.logpdf(t2s, a0, scale=1 / b0)
dens = (stats.gamma.pdf(t1s, a0 + cs[kk - 1], scale=1 / (b0 + kk))
        * stats.gamma.pdf(t2s, a0 + S - cs[kk - 1], scale=1 / (b0 + n - kk)))
R["q11_lpost"] = np.log(dens.mean())
R["q11_chib"] = R["q11_loglik"] + R["q11_lprior"] - R["q11_lpost"]
# added part: numerical standard error of E(theta1 | y) by batch means (50 batches of 200)
bm = th1.reshape(50, 200).mean(1)
R["q11_nse_bm"], R["q11_nse_iid"] = bm.std(ddof=1) / np.sqrt(50), th1.std(ddof=1) / np.sqrt(G)
R["q11_ineff"] = (R["q11_nse_bm"] / R["q11_nse_iid"]) ** 2
R["q11_tv"] = 0.5 * np.abs(np.bincount(kk, minlength=n + 1)[1:] / G - pk).sum()
# Q13(d): theta1, theta2 dependent after integrating k out (exact mixture moments)
m1k, m2k = (a0 + cs) / (b0 + ks), (a0 + S - cs) / (b0 + n - ks)
v1 = np.sum(pk * ((a0 + cs) / (b0 + ks) ** 2 + m1k ** 2)) - np.sum(pk * m1k) ** 2
v2 = np.sum(pk * ((a0 + S - cs) / (b0 + n - ks) ** 2 + m2k ** 2)) - np.sum(pk * m2k) ** 2
R["q13_corr"] = (np.sum(pk * m1k * m2k) - np.sum(pk * m1k) * np.sum(pk * m2k)) / np.sqrt(v1 * v2)
for kv in (36, 44):
    R[f"q13_m1_{kv}"], R[f"q13_m2_{kv}"] = m1k[kv - 1], m2k[kv - 1]


# Q12  original: change point, likelihood-ratio statistic and its null distribution
def lr_tau(y):
    """Lambda_tau = -2 log LR of 'one rate' vs 'rate changes after tau', tau = 1..n-1."""
    n, S = len(y), y.sum()
    tau = np.arange(1, n)
    s1 = np.cumsum(y)[:-1]
    xlogy = lambda a, b: np.where(a > 0, a * np.log(np.where(a > 0, a, 1) / b), 0.0)
    return 2 * (xlogy(s1, tau * S / n) + xlogy(S - s1, (n - tau) * S / n))


Lam = lr_tau(Y)
R["q12_tauhat"], R["q12_Lmax"] = np.argmax(Lam) + 1, Lam.max()
R["q12_L41"] = Lam[40]
p41, pi41 = 127 / 191, 41 / 112                  # KL form: Lambda = 2 S KL(Bern(p) || Bern(pi))
close(Lam[40], 2 * 191 * (p41 * np.log(p41 / pi41) + (1 - p41) * np.log((1 - p41) / (1 - pi41))))
R["q12_th1"], R["q12_th2"], R["q12_th"] = 127 / 41, 64 / 71, 191 / 112
R["q12_pbin"] = stats.binom.sf(126, 191, 41 / 112)
R["q12_Ebin"] = 191 * 41 / 112
rng = np.random.default_rng(12)
mx = np.array([lr_tau(rng.poisson(191 / 112, 112)).max() for _ in range(2000)])
R["q12_q95"], R["q12_overrej"] = np.quantile(mx, 0.95), np.mean(mx > stats.chi2.ppf(0.95, 1))
R["q12_pmax"] = np.mean(mx >= R["q12_Lmax"])


# ================================================================ Block 4
# Q14  Greenberg 2.2 on coal 1851-1891 with G(0.5, 1): closed form vs grid
n41, s41 = 41, 127
R["q14_w"], R["q14_pm"] = 1 / (1 + n41), (0.5 + s41) / (1 + n41)
grid = np.linspace(1e-6, 10, 200_001)
ker = np.exp((0.5 + s41 - 1) * np.log(grid) - (1 + n41) * grid - 300)
R["q14_grid_pm"] = integrate.trapezoid(grid * ker, grid) / integrate.trapezoid(ker, grid)
for nn in (1, 10, 41, 112, 1000):
    R[f"q14_w_{nn}"] = 1 / (1 + nn)

# Q15  Greenberg 3.2: predictive negative binomial, alpha1 = 127.5, beta1 = 42
a1, b1 = 127.5, 42.0
pnb = lambda yv: stats.nbinom.pmf(yv, a1, b1 / (b1 + 1))
for yv in range(4):
    R[f"q15_p{yv}"] = pnb(yv)
    close(pnb(yv), integrate.quad(lambda t: pois.pmf(yv, t) * stats.gamma.pdf(t, a1, scale=1 / b1),
                                   0, 10, epsrel=1e-11)[0], rtol=1e-8)
R["q15_mean"], R["q15_var"] = a1 / b1, a1 / b1 * (1 + 1 / b1)
rng = np.random.default_rng(15)
yp = rng.poisson(rng.gamma(a1, 1 / b1, 1_000_000))
R["q15_mc_mean"], R["q15_mc_var"] = yp.mean(), yp.var(ddof=1)
for yv in range(4):
    R[f"q15_mc_p{yv}"] = np.mean(yp == yv)

# Q16  Greenberg 3.5: posterior median minimizes expected absolute loss
post = stats.gamma(a1, scale=1 / b1)
R["q16_median"], R["q16_mean"], R["q16_mode"] = post.median(), post.mean(), (a1 - 1) / b1
eal = lambda d: integrate.quad(lambda t: abs(t - d) * post.pdf(t), 0, 10, points=[d], epsrel=1e-12)[0]
res = optimize.minimize_scalar(eal, bounds=(2.5, 3.5), method="bounded", options={"xatol": 1e-10})
R["q16_argmin"] = res.x
R["q16_eal_med"], R["q16_eal_mean"], R["q16_eal_mode"] = eal(post.median()), eal(post.mean()), eal((a1 - 1) / b1)
# derivative of the expected loss = 2F(d) - 1
close((eal(3.0 + 1e-5) - eal(3.0 - 1e-5)) / 2e-5, 2 * post.cdf(3.0) - 1, rtol=1e-5)

# Q17  Bolfarine 4.9 / 5.12: Poisson, exponential(1) prior, one observation x = 4
x = 4
R["q17_bayesP0"] = (2 / 3) ** (x + 1)
close(R["q17_bayesP0"], integrate.quad(lambda t: np.exp(-t) * stats.gamma.pdf(t, x + 1, scale=0.5), 0, 60)[0])
pg = stats.gamma(x + 1, scale=0.5)
R["q17_lo"], R["q17_hi"] = pg.ppf(0.025), pg.ppf(0.975)
close(R["q17_lo"], stats.chi2.ppf(0.025, 10) / 4); close(R["q17_hi"], stats.chi2.ppf(0.975, 10) / 4)
R["q17_chi_lo"], R["q17_chi_hi"] = stats.chi2.ppf(0.025, 10), stats.chi2.ppf(0.975, 10)


def hpd(dist, cred=0.95):
    """Shortest interval with posterior probability cred for a unimodal continuous dist."""
    L = lambda pl: dist.ppf(pl + cred) - dist.ppf(pl)
    pl = optimize.minimize_scalar(L, bounds=(1e-9, 1 - cred - 1e-9), method="bounded",
                                  options={"xatol": 1e-12}).x
    return dist.ppf(pl), dist.ppf(pl + cred)


R["q17_hpd_lo"], R["q17_hpd_hi"] = hpd(pg)
close(pg.pdf(R["q17_hpd_lo"]), pg.pdf(R["q17_hpd_hi"]), rtol=1e-4)
R["q17_len_eq"], R["q17_len_hpd"] = R["q17_hi"] - R["q17_lo"], R["q17_hpd_hi"] - R["q17_hpd_lo"]
for th in (0.5, 1.0, 4.0, 8.0):
    xs = np.arange(0, 200)
    lo, hi = stats.gamma.ppf(0.025, xs + 1, scale=0.5), stats.gamma.ppf(0.975, xs + 1, scale=0.5)
    R[f"q17_cov_{th:g}"] = np.sum(pois.pmf(xs, th) * ((lo <= th) & (th <= hi)))

# Q18  original: Bayes estimators and frequentist risk, alpha = 2, beta = 1, n = 10
al, be, n = 2.0, 1.0, 10
A, Bq, C = n * be ** 2, -(be ** 2 + 2 * n * be + 2 * n * al * be), n * al ** 2
R["q18_A"], R["q18_B"], R["q18_C"] = A, Bq, C
R["q18_disc"] = Bq ** 2 - 4 * A * C
R["q18_r1"], R["q18_r2"] = (-Bq - np.sqrt(R["q18_disc"])) / (2 * A), (-Bq + np.sqrt(R["q18_disc"])) / (2 * A)
R["q18_lim1"], R["q18_lim2"] = ((1 + al) - np.sqrt(1 + 2 * al)) / be, ((1 + al) + np.sqrt(1 + 2 * al)) / be
R["q18_bayesrisk_B"], R["q18_bayesrisk_mle"] = al / (be * (be + n)), al / (be * n)
riskB = lambda t: (n * t + (al - be * t) ** 2) / (be + n) ** 2
close(riskB(R["q18_r1"]), R["q18_r1"] / n); close(riskB(R["q18_r2"]), R["q18_r2"] / n)
close(integrate.quad(lambda t: riskB(t) * stats.gamma.pdf(t, al, scale=1 / be), 0, 80)[0], R["q18_bayesrisk_B"])
rng = np.random.default_rng(18)
for th in (1.0, 2.0, 5.0, 6.0):
    T = rng.poisson(n * th, 400_000)
    R[f"q18_riskB_{th:g}"], R[f"q18_simB_{th:g}"] = riskB(th), np.mean(((al + T) / (be + n) - th) ** 2)
    R[f"q18_riskM_{th:g}"], R[f"q18_simM_{th:g}"] = th / n, np.mean((T / n - th) ** 2)


# ================================================================ Block 5
# Q20-Q21  Greenberg 5.6-5.7: GHK importance sampling for a bivariate normal rectangle
mu1, mu2, s11, s12, s22 = 1.0, -0.5, 2.0, 1.0, 3.0
a1, b1, a2, b2 = 0.2, 2.0, -1.0, 5.0
s22c = s22 - s12 ** 2 / s11
a1p, b1p = (a1 - mu1) / np.sqrt(s11), (b1 - mu1) / np.sqrt(s11)
Phi, phi = stats.norm.cdf, stats.norm.pdf


def inner(y1):
    """Phi(b2'|y1) - Phi(a2'|y1): conditional probability of a2 < x2 <= b2 given y1."""
    m2c = mu2 + (s12 / s11) * (mu1 + np.sqrt(s11) * y1 - mu1)
    return Phi((b2 - m2c) / np.sqrt(s22c)) - Phi((a2 - m2c) / np.sqrt(s22c))


R["q20_s22c"], R["q20_a1p"], R["q20_b1p"] = s22c, a1p, b1p
R["q20_mass1"] = Phi(b1p) - Phi(a1p)
R["q21_exact"] = integrate.quad(lambda u: phi(u) * inner(u), a1p, b1p, epsabs=0, epsrel=1e-13)[0]
mvn = stats.multivariate_normal([mu1, mu2], [[s11, s12], [s12, s22]])
rect = mvn.cdf([b1, b2]) - mvn.cdf([a1, b2]) - mvn.cdf([b1, a2]) + mvn.cdf([a1, a2])
close(rect, R["q21_exact"], rtol=1e-5)
# variance of one GHK term versus one crude indicator (exact, by quadrature)
m2_ghk = integrate.quad(lambda u: phi(u) / R["q20_mass1"] * (inner(u) * R["q20_mass1"]) ** 2,
                        a1p, b1p, epsabs=0, epsrel=1e-12)[0]
R["q20_var_ghk"] = m2_ghk - R["q21_exact"] ** 2
R["q20_var_crude"] = R["q21_exact"] * (1 - R["q21_exact"])
R["q20_var_ratio"] = R["q20_var_crude"] / R["q20_var_ghk"]
R["q20_bound"] = R["q21_exact"] * (R["q20_mass1"] - R["q21_exact"])
assert R["q20_var_ghk"] <= R["q20_bound"] <= R["q20_var_crude"]
rng = np.random.default_rng(21)
G = 10_000
u = rng.uniform(size=G)
y1 = stats.norm.ppf(Phi(a1p) + u * (Phi(b1p) - Phi(a1p)))          # (5.1): truncated N(0,1)
terms = inner(y1) * R["q20_mass1"]
R["q21_est"], R["q21_nse"] = terms.mean(), terms.std(ddof=1) / np.sqrt(G)
R["q20_trunc_mean"] = y1.mean()
R["q20_trunc_exact"] = stats.truncnorm(a1p, b1p).mean()
x = mvn.rvs(size=G, random_state=rng)                                # crude MC, same G
ind = (a1 < x[:, 0]) & (x[:, 0] <= b1) & (a2 < x[:, 1]) & (x[:, 1] <= b2)
R["q21_crude"], R["q21_crude_se"] = ind.mean(), ind.std(ddof=1) / np.sqrt(G)


# Q22  Morettin & Singer B.15: inverse-transform generator for Poisson(2)
def rpois_inv(u, lam):
    """Inverse transform: smallest j with F(j) > u, using p_{j+1} = p_j lam/(j+1); also #comparisons."""
    j, p = 0, np.exp(-lam)
    F = p
    while u >= F:
        p *= lam / (j + 1)
        j += 1
        F += p
    return j, j + 1


rng = np.random.default_rng(22)
u5 = rng.uniform(size=5)
R["q22_u5"], R["q22_x5"] = u5, [rpois_inv(v, 2.0)[0] for v in u5]
big = np.array([rpois_inv(v, 2.0) for v in rng.uniform(size=100_000)])
R["q22_mean"], R["q22_var"], R["q22_ncomp"] = big[:, 0].mean(), big[:, 0].var(ddof=1), big[:, 1].mean()
obs = np.array([np.sum(big[:, 0] == j) for j in range(7)] + [np.sum(big[:, 0] >= 7)])
expd = 100_000 * np.r_[pois.pmf(np.arange(7), 2.0), pois.sf(6, 2.0)]
R["q22_chi2"] = np.sum((obs - expd) ** 2 / expd)
R["q22_pval"] = stats.chi2.sf(R["q22_chi2"], 7)
R["q22_cdf"] = pois.cdf(np.arange(6), 2.0)

# Q23  Morettin & Singer B.18: half-normal by accept-reject with g(x) = exp(-x)
R["q23_c"] = np.sqrt(2 * np.e / np.pi)
R["q23_acc"] = 1 / R["q23_c"]
xs = np.linspace(0, 6, 60001)
close(np.max(np.sqrt(2 / np.pi) * np.exp(-xs ** 2 / 2 + xs)), R["q23_c"], rtol=1e-8)
rng = np.random.default_rng(23)
acc, tries = [], 0
while len(acc) < 10_000:
    xp, uu = rng.exponential(1.0), rng.uniform()
    tries += 1
    if uu <= np.exp(-(xp - 1) ** 2 / 2):
        acc.append(xp)
Xh = np.array(acc)
Zs = np.where(rng.uniform(size=Xh.size) <= 0.5, Xh, -Xh)
R["q23_acc_emp"], R["q23_meanX"], R["q23_meanX_exact"] = 10_000 / tries, Xh.mean(), np.sqrt(2 / np.pi)
R["q23_meanZ"], R["q23_varZ"] = Zs.mean(), Zs.var(ddof=1)
R["q23_ks_p_X"] = stats.kstest(Xh, stats.halfnorm.cdf).pvalue
R["q23_ks_p_Z"] = stats.kstest(Zs, stats.norm.cdf).pvalue

# Q24  original: importance sampling for a Poisson tail, lambda = 2, k = 10
lam, kq, G = 2.0, 10, 100_000
p = pois.sf(kq - 1, lam)
R["q24_p"] = p
R["q24_var_naive"], R["q24_rse_naive"] = p * (1 - p), np.sqrt((1 - p) / (p * G))
var_is = lambda mu: np.exp(mu - 2 * lam + lam ** 2 / mu) * pois.sf(kq - 1, lam ** 2 / mu) - p ** 2
wk = lambda mu: np.exp(mu - lam) * (lam / mu) ** kq
R["q24_var_is10"], R["q24_rse_is10"] = var_is(10.0), np.sqrt(var_is(10.0) / G) / p
R["q24_wk10"], R["q24_bound10"] = wk(10.0), wk(10.0) * p - p ** 2
mus = np.linspace(2.5, 20, 3501)
R["q24_mu_opt"] = mus[np.argmin([var_is(mu) for mu in mus])]
R["q24_var_opt"] = var_is(R["q24_mu_opt"])
for mu in (2.0, 5.0, 10.0, 15.0):          # exact second moment versus enumeration
    xx = np.arange(kq, 400)
    close(np.sum(np.exp(2 * pois.logpmf(xx, lam) - pois.logpmf(xx, mu))) - p ** 2, var_is(mu), rtol=1e-8)
    R[f"q24_var_is_{mu:g}"] = var_is(mu)
close(var_is(lam), p * (1 - p))
rng = np.random.default_rng(24)
xn = rng.poisson(lam, G)
R["q24_naive"], R["q24_naive_se"] = np.mean(xn >= kq), np.sqrt(np.mean(xn >= kq) * (1 - np.mean(xn >= kq)) / G)
R["q24_naive_hits"] = int(np.sum(xn >= kq))
xi = rng.poisson(10.0, G)
wi = (xi >= kq) * np.exp(10.0 - lam) * (lam / 10.0) ** xi
R["q24_is"], R["q24_is_se"] = wi.mean(), wi.std(ddof=1) / np.sqrt(G)
R["q24_G10"] = (1 - p) / (0.01 * p)
R["q24_ratio"] = R["q24_var_naive"] / R["q24_var_is10"]
R["q24_is_z"] = (R["q24_is"] - p) / R["q24_is_se"]


# ================================================================ Block 6
# Q26  ISLP 5.2 (as in L01) plus the distinct-observation count of a bootstrap sample
for nn in (5, 100, 10000):
    R[f"q26_out_{nn}"], R[f"q26_in_{nn}"] = (1 - 1 / nn) ** nn, 1 - (1 - 1 / nn) ** nn
R["q26_lim"] = 1 - np.exp(-1)
R["q26_plot"] = {nn: 1 - (1 - 1 / nn) ** nn for nn in (1, 2, 3, 5, 10, 20, 50, 100, 1000, 10000, 100000)}
rng = np.random.default_rng(10)
store = np.empty(10000)
for i in range(10000):
    store[i] = np.sum(rng.choice(100, replace=True) == 4) > 0
R["q26_printed_code"] = store.mean()
rng = np.random.default_rng(10)
store = np.empty(10000)
for i in range(10000):
    store[i] = np.sum(rng.choice(100, size=100, replace=True) == 4) > 0
R["q26_fixed_code"] = store.mean()
nn = 100
ED = nn * (1 - (1 - 1 / nn) ** nn)
VD = nn * (nn - 1) * (1 - 2 / nn) ** nn + nn * (1 - 1 / nn) ** nn - nn ** 2 * (1 - 1 / nn) ** (2 * nn)
R["q26_ED"], R["q26_sdD"] = ED, np.sqrt(VD)
rng = np.random.default_rng(26)
D = np.array([np.unique(rng.choice(nn, size=nn, replace=True)).size for _ in range(10000)])
R["q26_simD_mean"], R["q26_simD_sd"] = D.mean(), D.std(ddof=1)

# Q27  ISLP 5.4: bootstrap SD of a Poisson-regression prediction (coal data, log-linear trend)
t = np.arange(1, 113)
Xd = sm.add_constant((t - 56.5) / 10)
fit = sm.GLM(Y, Xd, family=sm.families.Poisson()).fit()
x0 = np.array([1.0, (50 - 56.5) / 10])                               # year 1900
R["q27_b0"], R["q27_b1"] = fit.params
R["q27_se_b0"], R["q27_se_b1"] = fit.bse
R["q27_mu0"] = np.exp(x0 @ fit.params)
R["q27_se_delta"] = R["q27_mu0"] * np.sqrt(x0 @ fit.cov_params() @ x0)
R["q27_pearson_phi"] = fit.pearson_chi2 / fit.df_resid
rng = np.random.default_rng(27)
Bb = 2000
pred = np.empty(Bb)
for b in range(Bb):
    idx = rng.integers(0, 112, 112)
    pb = sm.GLM(Y[idx], Xd[idx], family=sm.families.Poisson()).fit().params
    pred[b] = np.exp(x0 @ pb)
R["q27_boot_sd"] = pred.std(ddof=1)
R["q27_boot_q"] = np.quantile(pred, [0.025, 0.975])
R["q27_delta_phi"] = R["q27_se_delta"] * np.sqrt(R["q27_pearson_phi"])
R["q27_pred_sd"] = np.sqrt(R["q27_mu0"] + R["q27_boot_sd"] ** 2)

# Q28  original: nonparametric versus parametric bootstrap for a Poisson mean (coal 1851-1891)
n, xb = 41, Y41.mean()
s2hat = Y41.var(ddof=0)
R["q28_xb"], R["q28_s2hat"], R["q28_s2"] = xb, s2hat, Y41.var(ddof=1)
R["q28_v_np"], R["q28_v_par"] = s2hat / n, xb / n
R["q28_disp"] = s2hat / xb
R["q28_psi"] = np.exp(-xb)
R["q28_Epsi_star"] = np.exp(n * xb * (np.exp(-1 / n) - 1))
R["q28_bias"] = R["q28_Epsi_star"] - R["q28_psi"]
R["q28_bc"] = 2 * R["q28_psi"] - R["q28_Epsi_star"]
R["q28_bias_approx"] = np.exp(-xb) * xb / (2 * n)
rng = np.random.default_rng(28)
Bb = 20_000
xnp = rng.choice(Y41, size=(Bb, n), replace=True).mean(1)
xpar = rng.poisson(xb, size=(Bb, n)).mean(1)
R["q28_sim_v_np"], R["q28_sim_v_par"] = xnp.var(ddof=1), xpar.var(ddof=1)
R["q28_sim_bias"] = np.exp(-xpar).mean() - R["q28_psi"]
close(np.sum(pois.pmf(np.arange(400), n * xb) * np.exp(-np.arange(400) / n)), R["q28_Epsi_star"])


# ================================================================ Block 7
# Q30  Greenberg 6.8: invariant density pi(y) = 2(1 - y) of the kernel p(x, y)
kern = lambda x, y: np.where(y < x, np.exp(1 - x), np.exp(1 - x) - np.exp(y - x))
for yv in (0.1, 0.5, 0.9):
    close(integrate.quad(lambda x: 2 * (1 - x) * kern(x, yv), 0, 1, points=[yv], epsabs=0,
                         epsrel=1e-12)[0], 2 * (1 - yv), rtol=1e-9)
for xv in (0.3, 0.7):
    close(integrate.quad(lambda y: kern(xv, y), 0, 1, points=[xv], epsabs=0, epsrel=1e-12)[0], 1.0)


def draw_kernel(x, u):
    """Inverse-CDF draw of y from p(x, .): F(y) = y e^{1-x} (y <= x), y e^{1-x} - e^{y-x} + 1 (y > x)."""
    if u <= x * np.exp(1 - x):
        return u * np.exp(x - 1)
    return optimize.brentq(lambda y: y * np.exp(1 - x) - np.exp(y - x) + 1 - u, x, 1.0, xtol=1e-14)


rng = np.random.default_rng(30)
chain = np.empty(20_000)
xc = 0.5
for g in range(21_000):
    xc = draw_kernel(xc, rng.uniform())
    if g >= 1000:
        chain[g - 1000] = xc
R["q30_mean"], R["q30_P05"] = chain.mean(), np.mean(chain < 0.5)
R["q30_bm_nse"] = chain.reshape(50, 400).mean(1).std(ddof=1) / np.sqrt(50)
R["q30_lag1"] = np.corrcoef(chain[:-1], chain[1:])[0, 1]

# Q31  Greenberg 7.4 / Algorithm 7.5: independence MH for Beta(3, 4), U(0, 1) proposal
fb = lambda v: v ** 2 * (1 - v) ** 3
rng = np.random.default_rng(31)
xc, acc, out = 0.5, 0, np.empty(5000)
for g in range(5500):
    U1, U2 = rng.uniform(), rng.uniform()
    if U1 <= fb(U2) / fb(xc):
        xc = U2
        acc += g >= 500
    if g >= 500:
        out[g - 500] = xc
R["q31_acc"], R["q31_mean"], R["q31_true"] = acc / 5000, out.mean(), 3 / 7
bd = stats.beta(3, 4)
R["q31_acc_exact"] = integrate.dblquad(lambda yv, xv: bd.pdf(xv) * min(1.0, fb(yv) / fb(xv)), 0, 1, 0, 1,
                                       epsabs=1e-11)[0]

# Q32  Greenberg 7.6: Beta(3.7, 4.8) target
ft = stats.beta(3.7, 4.8)
R["q32_true"] = 3.7 / 8.5
ratio45 = lambda v: ft.pdf(v) / stats.beta(4, 5).pdf(v)
R["q32_ratio45_small"], R["q32_ratio45_mid"] = ratio45(1e-8), ratio45(0.5)
xs_ = 0.7 / 1.5
R["q32_xstar"] = xs_
R["q32_c34"] = ft.pdf(xs_) / stats.beta(3, 4).pdf(xs_)
close(R["q32_c34"], np.max(ft.pdf(np.linspace(1e-6, 1 - 1e-6, 200001)) / stats.beta(3, 4).pdf(np.linspace(1e-6, 1 - 1e-6, 200001))), rtol=1e-8)
R["q32_acc34"] = 1 / R["q32_c34"]
rng = np.random.default_rng(32)
draws, tries = [], 0
while len(draws) < 10_000:
    yv, uu = rng.beta(3, 4), rng.uniform()
    tries += 1
    if uu <= ft.pdf(yv) / (R["q32_c34"] * stats.beta(3, 4).pdf(yv)):
        draws.append(yv)
R["q32_ar_mean"], R["q32_ar_acc"] = np.mean(draws), 10_000 / tries
R["q32_ar_se"] = np.std(draws, ddof=1) / 100
wq = lambda v: ft.pdf(v) / stats.beta(4, 5).pdf(v)
xc, acc, out = 0.5, 0, np.empty(10_000)
for g in range(11_000):
    yv = rng.beta(4, 5)
    if rng.uniform() <= min(1.0, wq(yv) / wq(xc)):
        xc = yv
        acc += g >= 1000
    if g >= 1000:
        out[g - 1000] = xc
R["q32_mh_mean"], R["q32_mh_acc"] = out.mean(), acc / 10_000
run = np.cumsum(out) / np.arange(1, 10_001)
for it in (1000, 2500, 5000, 10000):
    R[f"q32_run_{it}"] = run[it - 1]
R["q32_mh_nse"] = out.reshape(50, 200).mean(1).std(ddof=1) / np.sqrt(50)

# Q33  original: random-walk MH on log(theta) for the coal posterior Gamma(127.5, 42)
aP, bP = 127.5, 42.0
R["q33_exact_mean"], R["q33_bug_mean"] = aP / bP, (aP - 1) / bP
logpost = lambda th: (aP - 1) * np.log(th) - bP * th


def rw_log(s, jac, seed, G=50_000, burn=2_000):
    """RW-MH with theta' = theta e^u, u ~ N(0, s^2); jac=False drops the theta'/theta factor."""
    rng = np.random.default_rng(seed)
    th, acc, out = 1.0, 0, np.empty(G)
    for g in range(G + burn):
        prop = th * np.exp(s * rng.standard_normal())
        la = logpost(prop) - logpost(th) + (np.log(prop / th) if jac else 0.0)
        if np.log(rng.uniform()) <= la:
            th = prop
            acc += g >= burn
        if g >= burn:
            out[g - burn] = th
    return acc / G, out.mean(), out.reshape(50, G // 50).mean(1).std(ddof=1) / np.sqrt(50)


for s in (0.02, 0.2, 1.0):
    R[f"q33_acc_{s:g}"], R[f"q33_mean_{s:g}"], R[f"q33_nse_{s:g}"] = rw_log(s, True, 33)
R["q33_bug_acc"], R["q33_bug_mean_sim"], R["q33_bug_nse"] = rw_log(0.2, False, 33)
R["q33_bug_z_target"] = (R["q33_bug_mean_sim"] - R["q33_bug_mean"]) / R["q33_bug_nse"]
R["q33_bug_z_true"] = (R["q33_exact_mean"] - R["q33_bug_mean_sim"]) / R["q33_bug_nse"]


# ================================================================ programming parts of the conceptual questions
# Q5: exact variance of the unbiased estimator T(T-1)/n^2 of theta^2 versus the CR bound 4 theta^3 / n
th, n = 2.0, 10
tt = np.arange(0, 400)
pt = pois.pmf(tt, n * th)
est = tt * (tt - 1) / n ** 2
close(np.sum(pt * est), th ** 2)
R["q5_var"], R["q5_CR"] = np.sum(pt * est ** 2) - th ** 4, 4 * th ** 3 / n
close(R["q5_var"], 4 * th ** 3 / n + 2 * th ** 2 / n ** 2)          # closed form printed in the key
R["q5_ratio"] = R["q5_var"] / R["q5_CR"]

# Q9: size of the GLR test of B Exemplo 6.5.5 (theta0 = 5, n = 50) by simulation
rng = np.random.default_rng(9)
xb9 = rng.poisson(5.0 * 50, 100_000) / 50
lr9 = 2 * 50 * (xb9 * np.log(xb9 / 5.0) - (xb9 - 5.0))
R["q9_size"] = np.mean(lr9 > R["q7_crit"])

# Q13: posterior correlation of theta1, theta2 from the Gibbs draws of Question 11
R["q13_corr_gibbs"] = np.corrcoef(th1, th2)[0, 1]

# Q19: frequentist bias of the posterior mean (alpha = 2, beta = 1, n = 10) at theta = 1
rng = np.random.default_rng(19)
S19 = rng.poisson(10 * 1.0, 400_000)
R["q19_bias_sim"], R["q19_bias"] = np.mean((2 + S19) / 11) - 1.0, (2 - 1.0) / 11

# Q25: number of proposals per accepted draw in the half-normal accept-reject of Question 23
rng = np.random.default_rng(25)
x25 = rng.exponential(1.0, 2_000_000)
acc25 = rng.uniform(size=x25.size) <= np.exp(-(x25 - 1) ** 2 / 2)
pos = np.flatnonzero(acc25)[:100_000]
waits = np.diff(np.r_[-1, pos])
R["q25_mean_wait"], R["q25_var_wait"] = waits.mean(), waits.var(ddof=1)
R["q25_var_geom"] = R["q23_c"] * (R["q23_c"] - 1)

# Q29: bootstrap SE of xbar (coal 1851-1891) as B grows, versus its B -> infinity limit
R["q29_ideal"] = np.sqrt(R["q28_v_np"])
rng = np.random.default_rng(29)
for Bq in (100, 1000, 10000):
    R[f"q29_se_{Bq}"] = rng.choice(Y41, size=(Bq, 41), replace=True).mean(1).std(ddof=1)

# Q34: systematic-scan Gibbs on a 2x2 joint law is pi-invariant but not reversible
pj = np.array([[0.3, 0.2], [0.1, 0.4]])                       # p(x, y), x rows, y columns
states = [(0, 0), (0, 1), (1, 0), (1, 1)]
pi4 = np.array([pj[s] for s in states])
Px = np.array([[pj[x2, y1] / pj[:, y1].sum() if y2 == y1 else 0.0 for (x2, y2) in states]
               for (x1, y1) in states])                         # update x given y
Py = np.array([[pj[x1, y2] / pj[x1, :].sum() if x2 == x1 else 0.0 for (x2, y2) in states]
               for (x1, y1) in states])                         # update y given x
P = Px @ Py
R["q34_inv_err"] = np.abs(pi4 @ P - pi4).max()
F34 = pi4[:, None] * P
R["q34_asym"] = np.abs(F34 - F34.T).max()
R["q34_P"] = P
close(np.abs(pi4[:, None] * Px - (pi4[:, None] * Px).T).max(), 0.0)  # each single update is reversible


# ================================================================ printed values
# Every number printed in the .tex, as printed (string), keyed by the computed result above.
PRINTED = {
    # Block 1
    "q1_T2_1": "0.3333", "q1_T2_2": "0.5000", "q1_T4_1_40": "0.04", "q1_T4_1_21": "0.48",
    "q1_T4_1_02": "0.48", "q1_T4_2_40": "0.10", "q1_T4_2_21": "0.60", "q1_T4_2_02": "0.30",
    "q2_Es2": "0.333333", "q2_mEh": "0.333333", "q2_Es": "0.000000", "q2_U_Es2": "0.25",
    "q2_U_mEh": "-0.25", "q2_U_Es": "-0.5",
    "q3_CR": "0.2", "q3_vS2": "1.088889", "q3_mean_xb": "2.0014", "q3_var_xb": "0.1997",
    "q3_mean_s2": "1.9995", "q3_var_s2": "1.0871",
    "q4_psi": "0.223130", "q4_Emle": "0.239923", "q4_biasmle": "0.016792", "q4_varU": "0.008057",
    "q4_CR": "0.007468", "q4_ratio": "1.078895", "q4_mseMLE": "0.008657",
    "q4_sim_mle_mean": "0.239825", "q4_sim_umvu_mean": "0.223033", "q4_sim_umvu_var": "0.008042",
    "q4_sim_mle_mse": "0.008638", "q4_ratio_n1": "2.321126", "q4_ratio_n2": "1.489333",
    "q4_ratio_n5": "1.166196", "q4_ratio_n10": "1.078895", "q4_ratio_n50": "1.015151",
    "q4_ratio_n1000": "1.000750",
    # Block 2
    "q6_c": "1.328971", "q6_z15": "-0.698223", "q6_cT": "33", "q6_size_exact": "0.049780",
    "q6_gamma": "0.010133", "q6_pclt_1": "0.050000", "q6_pex_1": "0.049780", "q6_prand_1": "0.050000",
    "q6_pclt_1.2": "0.278042", "q6_pex_1.2": "0.255551", "q6_prand_1.2": "0.256158",
    "q6_pclt_1.5": "0.757481", "q6_pex_1.5": "0.738112", "q6_prand_1.5": "0.738642",
    "q6_pclt_2": "0.991165", "q6_pex_2": "0.993021", "q6_prand_2": "0.993047",
    "q7_xb": "0.76", "q7_yb": "0.6", "q7_th0": "0.661538", "q7_t1": "0.527251", "q7_t2": "-0.468665",
    "q7_LR": "0.117173", "q7_p": "0.7321", "q7_crit": "3.841459", "q7_size_0.66": "0.06949",
    "q7_size_3": "0.05167",
    "q8_cov_wald_0.1": "0.631526", "q8_cov_score_0.1": "0.919699", "q8_cov_exact_0.1": "0.981012",
    "q8_cov_wald_1": "0.925728", "q8_cov_score_1": "0.962622", "q8_cov_exact_1": "0.975386",
    "q8_cov_wald_5": "0.948781", "q8_cov_score_5": "0.944398", "q8_cov_exact_5": "0.952638",
    "q8_coal_wald_lo": "2.558837", "q8_coal_wald_hi": "3.636285", "q8_coal_score_lo": "2.603651",
    "q8_coal_score_hi": "3.685165", "q8_coal_exact_lo": "2.582297", "q8_coal_exact_hi": "3.685510",
    "q8_zero_score_hi": "0.320122",
    # Block 3
    "q10_100_0.9": "-0.283", "q10_100_0.8": "0.370", "q10_100_0.7": "0.796", "q10_100_0.6": "1.039",
    "q10_100_0.5": "1.118", "q10_200_0.9": "-1.717", "q10_200_0.8": "-0.310", "q10_200_0.7": "0.593",
    "q10_200_0.6": "1.105", "q10_200_0.5": "1.271", "q10_num": "-0.652323", "q10_mc": "-0.28295",
    "q10_mc_se": "0.00312",
    "q11_logm": "-179.4590", "q11_Et1": "3.0500", "q11_Et2": "0.9147", "q11_pk_41": "0.2482",
    "q11_pk_40": "0.1848", "q11_pk_39": "0.1414", "q11_pk_42": "0.1010", "q11_pk_37": "0.0898",
    "q11_pk_36": "0.0745", "q11_m1": "3.0506", "q11_s1": "0.2809", "q11_m2": "0.9166", "q11_s2": "0.1163",
    "q11_kmean": "40.14", "q11_gpk_41": "0.2471", "q11_gpk_40": "0.1849", "q11_gpk_39": "0.1433",
    "q11_gpk_42": "0.0987", "q11_gpk_37": "0.0881", "q11_gpk_36": "0.0742", "q11_p3646": "0.98",
    "q11_loglik": "-172.2563", "q11_lprior": "-5.6261", "q11_lpost": "1.5765", "q11_chib": "-179.4589",
    "q11_nse_bm": "0.003035", "q11_nse_iid": "0.002809", "q11_ineff": "1.167", "q11_tv": "0.0077",
    "q12_tauhat": "41", "q12_Lmax": "69.99", "q12_th1": "3.097561", "q12_th2": "0.901408",
    "q12_th": "1.705357", "q12_Ebin": "69.92", "q12_q95": "10.08", "q12_overrej": "0.5675",
    "q12_pmax": "0.0",
    "q13_corr": "0.060", "q13_m1_36": "3.18", "q13_m2_36": "0.97", "q13_m1_44": "2.90", "q13_m2_44": "0.89",
    # Block 4
    "q14_w": "0.023810", "q14_pm": "3.035714", "q14_grid_pm": "3.035714", "q14_w_1": "0.500000",
    "q14_w_10": "0.090909", "q14_w_41": "0.023810", "q14_w_112": "0.008850", "q14_w_1000": "0.000999",
    "q15_p0": "0.049780", "q15_p1": "0.147604", "q15_p2": "0.220548", "q15_p3": "0.221403",
    "q15_mean": "3.035714", "q15_var": "3.107993", "q15_mc_mean": "3.035098", "q15_mc_var": "3.101461",
    "q15_mc_p0": "0.049581", "q15_mc_p1": "0.147294", "q15_mc_p2": "0.221058", "q15_mc_p3": "0.221849",
    "q16_median": "3.027781", "q16_argmin": "3.027781", "q16_mean": "3.035714", "q16_mode": "3.011905",
    "q16_eal_med": "0.214276", "q16_eal_mean": "0.214369", "q16_eal_mode": "0.214650",
    "q17_bayesP0": "0.131687", "q17_chi_lo": "3.246973", "q17_chi_hi": "20.483177", "q17_lo": "0.811743",
    "q17_hi": "5.120794", "q17_hpd_lo": "0.603480", "q17_hpd_hi": "4.715108", "q17_len_hpd": "4.111628",
    "q17_len_eq": "4.309051", "q17_cov_0.5": "0.985612", "q17_cov_1": "0.996340", "q17_cov_4": "0.761820",
    "q17_cov_8": "0.407449",
    "q18_A": "10", "q18_B": "-61", "q18_C": "40", "q18_disc": "2121", "q18_r1": "0.747284",
    "q18_r2": "5.352716", "q18_lim1": "0.763932", "q18_lim2": "5.236068", "q18_bayesrisk_B": "0.181818",
    "q18_bayesrisk_mle": "0.2", "q18_riskB_1": "0.090909", "q18_simB_1": "0.091203",
    "q18_riskM_1": "0.1", "q18_simM_1": "0.100222", "q18_riskB_2": "0.165289", "q18_simB_2": "0.164913",
    "q18_riskM_2": "0.2", "q18_simM_2": "0.199545", "q18_riskB_5": "0.487603", "q18_simB_5": "0.487363",
    "q18_riskM_5": "0.5", "q18_simM_5": "0.499468", "q18_riskB_6": "0.628099", "q18_simB_6": "0.629657",
    "q18_riskM_6": "0.6", "q18_simM_6": "0.602826",
    # Block 5
    "q20_s22c": "2.5", "q20_a1p": "-0.565685", "q20_b1p": "0.707107", "q20_mass1": "0.474446",
    "q21_exact": "0.300105", "q20_var_ghk": "0.000797", "q20_var_crude": "0.210042",
    "q20_var_ratio": "263.6", "q20_bound": "0.052321", "q20_trunc_mean": "0.0655",
    "q20_trunc_exact": "0.0617", "q21_est": "0.300411", "q21_nse": "0.000282", "q21_crude": "0.3019",
    "q21_crude_se": "0.0046",
    "q22_mean": "1.99556", "q22_var": "2.01146", "q22_ncomp": "2.99556", "q22_chi2": "12.44",
    "q22_pval": "0.0869",
    "q23_c": "1.315489", "q23_acc": "0.760173", "q23_acc_emp": "0.762195", "q23_meanX": "0.793801",
    "q23_meanX_exact": "0.797885", "q23_meanZ": "0.019998", "q23_varZ": "0.990055",
    "q23_ks_p_X": "0.4935", "q23_ks_p_Z": "0.3449",
    "q24_rse_naive": "0.4637", "q24_G10": "2150527", "q24_rse_is10": "0.006778", "q24_mu_opt": "10.035",
    "q24_ratio": "4680.5", "q24_naive": "0.000040", "q24_naive_se": "0.000020", "q24_naive_hits": "4",
    # Block 6
    "q26_out_5": "0.32768", "q26_in_5": "0.67232", "q26_out_100": "0.366032", "q26_in_100": "0.633968",
    "q26_out_10000": "0.367861", "q26_in_10000": "0.632139", "q26_lim": "0.632121",
    "q26_printed_code": "0.0089", "q26_fixed_code": "0.6362", "q26_ED": "63.396766", "q26_sdD": "3.120912",
    "q26_simD_mean": "63.3994", "q26_simD_sd": "3.1583",
    "q27_b0": "0.363109", "q27_se_b0": "0.084922", "q27_b1": "-0.183776", "q27_se_b1": "0.024728",
    "q27_mu0": "1.620223", "q27_se_delta": "0.125930", "q27_boot_sd": "0.134530",
    "q27_pearson_phi": "1.133236", "q27_delta_phi": "0.134057", "q27_pred_sd": "1.2800",
    "q28_xb": "3.097561", "q28_s2hat": "2.478287", "q28_s2": "2.540244", "q28_v_np": "0.060446",
    "q28_v_par": "0.075550", "q28_disp": "0.800077", "q28_psi": "0.045159", "q28_Epsi_star": "0.046883",
    "q28_bias": "0.001724", "q28_bias_approx": "0.001706", "q28_bc": "0.043435",
    "q28_sim_v_np": "0.060686", "q28_sim_v_par": "0.076385", "q28_sim_bias": "0.001655",
    # Block 7
    "q30_mean": "0.334981", "q30_P05": "0.74745", "q30_bm_nse": "0.001868", "q30_lag1": "0.0768",
    "q31_acc": "0.5682", "q31_mean": "0.432394", "q31_true": "0.428571", "q31_acc_exact": "0.572589",
    "q32_true": "0.435294", "q32_ratio45_small": "169.2", "q32_ratio45_mid": "0.9528",
    "q32_xstar": "0.466667", "q32_c34": "1.115321", "q32_acc34": "0.896603", "q32_ar_acc": "0.894775",
    "q32_ar_mean": "0.434564", "q32_ar_se": "0.001621", "q32_mh_acc": "0.9645", "q32_mh_mean": "0.437056",
    "q32_mh_nse": "0.001744", "q32_run_1000": "0.4284", "q32_run_2500": "0.4333",
    "q32_run_5000": "0.4375", "q32_run_10000": "0.4371",
    "q33_exact_mean": "3.035714", "q33_bug_mean": "3.011905", "q33_acc_0.02": "0.9284",
    "q33_mean_0.02": "3.037804", "q33_nse_0.02": "0.011093", "q33_acc_0.2": "0.4636",
    "q33_mean_0.2": "3.037605", "q33_nse_0.2": "0.001913", "q33_acc_1": "0.1127", "q33_mean_1": "3.032593",
    "q33_nse_1": "0.005092", "q33_bug_acc": "0.4664", "q33_bug_mean_sim": "3.015205",
    "q33_bug_nse": "0.002112", "q33_bug_z_target": "1.6", "q33_bug_z_true": "9.7",
}
for key, printed in PRINTED.items():
    ok(R[key], printed)
# composite claims printed in the text
ok(R["q11_q1"][0], "2.530"); ok(R["q11_q1"][1], "3.635"); ok(R["q11_q2"][0], "0.701"); ok(R["q11_q2"][1], "1.156")
ok(R["q12_pbin"] * 1e17, "5.4")
ok(R["q24_p"] * 1e5, "4.649808"); ok(R["q24_var_is10"] * 1e9, "9.9339"); ok(R["q24_wk10"] * 1e4, "3.0525")
ok(R["q24_bound10"] * 1e8, "1.2031"); ok(R["q24_is"] * 1e5, "4.6844"); ok(R["q24_is_se"] * 1e7, "3.165")
for mu, pr in ((2, "4.6496e-05"), (5, "8.4535e-08"), (10, "9.9339e-09"), (15, "2.8585e-08")):
    m_, e_ = pr.split("e")
    ok(R[f"q24_var_is_{mu}"] / 10 ** int(e_), m_)
ok(R["q27_boot_q"][0], "1.3633"); ok(R["q27_boot_q"][1], "1.8748")
for (t, v), pr in zip(R["q6_plot"], ["0.0016", "0.0119", "0.0500", "0.1375", "0.2780", "0.4495", "0.6180",
                                    "0.7575", "0.8580", "0.9226", "0.9604", "0.9808", "0.9912", "0.9961",
                                    "0.9983"]):
    ok(v, pr)
for nn, pr in zip((1, 2, 3, 5, 10, 20, 50, 100, 1000, 10000, 100000),
                  ("1.0000", "0.7500", "0.7037", "0.6723", "0.6513", "0.6415", "0.6358", "0.6340", "0.6323",
                   "0.6321", "0.6321")):
    ok(R["q26_plot"][nn], pr)
assert R["q22_x5"] == [1, 1, 0, 2, 2]
for v, pr in zip(R["q22_u5"], ("0.366347", "0.199295", "0.088558", "0.653192", "0.459337")):
    ok(v, pr)
for v, pr in zip(R["q22_cdf"][:4], ("0.135335", "0.406006", "0.676676", "0.857123")):
    ok(v, pr)
# claims stated in words
assert max(abs(R[f"q15_mc_p{k}"] - R[f"q15_p{k}"]) for k in range(4)) <= 0.0006
assert abs(R["q21_est"] - R["q21_exact"]) / R["q21_nse"] < 1.2                 # "about 1.1 n.s.e."
assert 15.5 < R["q21_crude_se"] / R["q21_nse"] < 17                          # "sixteen times larger"
assert abs(R["q24_is_z"]) < 1.2 and abs(R["q30_mean"] - 1 / 3) < R["q30_bm_nse"]
assert abs(R["q32_ar_mean"] - R["q32_true"]) < R["q32_ar_se"]
assert abs(R["q32_mh_mean"] - R["q32_true"]) < 1.1 * R["q32_mh_nse"]
assert 5.5 < R["q33_nse_0.02"] / R["q33_nse_0.2"] < 6.0                      # "about six times"
assert R["q33_nse_0.2"] < min(R["q33_nse_0.02"], R["q33_nse_1"])
assert abs(R["q33_mean_0.2"] - R["q33_exact_mean"]) < 1.1 * R["q33_nse_0.2"]
assert R["q12_overrej"] > 0.05 and R["q12_q95"] > R["q7_crit"]
assert R["q17_len_hpd"] < R["q17_len_eq"]
assert R["q18_r1"] < al / be < R["q18_r2"] and R["q18_riskB_6"] > R["q18_riskM_6"]
assert all(R[f"q18_riskB_{t:g}"] < R[f"q18_riskM_{t:g}"] for t in (1.0, 2.0, 5.0))
assert R["q28_bias"] > 0 and R["q8_cov_exact_0.1"] >= 0.95 and R["q8_cov_exact_1"] >= 0.95
assert R["q8_cov_wald_0.1"] <= 1 - np.exp(-1.0) + 1e-12
assert R["q20_var_ghk"] < R["q20_bound"] < R["q20_var_crude"]
# programming parts of the conceptual questions
for key, pr in (("q5_var", "3.28"), ("q5_CR", "3.2"), ("q5_ratio", "1.025"), ("q9_size", "0.04866"),
                ("q13_corr_gibbs", "0.0708"), ("q19_bias_sim", "0.090347"), ("q19_bias", "0.090909"),
                ("q25_mean_wait", "1.31879"), ("q25_var_wait", "0.42047"), ("q25_var_geom", "0.41502"),
                ("q29_ideal", "0.245858"), ("q29_se_100", "0.259285"), ("q29_se_1000", "0.242725"),
                ("q29_se_10000", "0.244059"), ("q34_asym", "0.053333")):
    ok(R[key], pr)
assert R["q34_inv_err"] < 1e-15 and abs(R["q13_corr_gibbs"] - R["q13_corr"]) < 0.02
# worked pieces printed in the solutions
for v, pr in ((special.gammaln(11), "15.104413"), (12 * np.log(101), "55.381446"), (np.log(101), "4.615121"),
              (11 * np.log(201), "58.336354"), (np.log(201), "5.303305"), (special.gammaln(10), "12.801827"),
              (np.log(10), "2.302585"), (25 * R["q6_c"], "33.22"), (np.sqrt(R["q20_var_ratio"]), "16.2"),
              (1 / np.sqrt(127.5), "0.089"), (np.exp(8) * 0.2 ** 10 * 1e4, "3.0525"),
              (0.2 + 8 / 9, "1.088889"), (1 - np.exp(-1.0), "0.6321"), (Z975, "1.959964"), (Z95, "1.644854")):
    ok(v, pr)
print(f"poisson-monte-carlo-check: all {N_OK} checks passed")
