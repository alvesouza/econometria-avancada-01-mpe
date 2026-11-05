"""Reproduce and assert every number printed in Listas/lista-L03-book-exercises.tex (unit L03,
Classes 3+4, Bayesian learning).

Run from anywhere:  python Listas/L03-book-exercises-check.py
Each block prints the numbers quoted in the solutions and asserts them; closed forms are also
checked against an independent route (quadrature, brute force, exact enumeration). MCMC and
simulation blocks use fixed seeds; their printed values are asserted to the printed rounding,
and against the exact answer within a Monte Carlo tolerance. Prints PASS at the end.
Data: Listas/data/babies.data (StatLabs "Birth weight II", see Listas/data/README.md);
coal-mining counts embedded below (Carlin, Gelfand and Smith 1992, 1851-1962).
"""
from math import exp, lgamma, log
from pathlib import Path

import numpy as np
from scipy import integrate, stats
from scipy.special import gammaln, logsumexp

DATA = Path(__file__).resolve().parent / "data"


def close(a, b, tol, what):
    """Assert |a - b| <= tol; `what` names the quantity in the failure message."""
    assert abs(a - b) <= tol, f"{what}: got {a!r}, expected {b!r} (tol {tol})"


# British coal-mining disasters per year, 1851-1962 (n = 112, total 191).
COAL = np.array([4, 5, 4, 1, 0, 4, 3, 4, 0, 6, 3, 3, 4, 0, 2, 6, 3, 3, 5, 4, 5, 3, 1, 4, 4, 1, 5, 5,
                 3, 4, 2, 5, 2, 2, 3, 4, 2, 1, 3, 2, 2, 1, 1, 1, 1, 3, 0, 0, 1, 0, 1, 1, 0, 0, 3, 1,
                 0, 3, 2, 2, 0, 1, 1, 1, 0, 1, 0, 1, 0, 0, 0, 2, 1, 0, 0, 0, 1, 1, 0, 2, 3, 3, 1, 1,
                 2, 1, 1, 1, 1, 2, 4, 2, 0, 0, 0, 1, 4, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1])
assert COAL.size == 112 and COAL.sum() == 191 and COAL[:40].sum() == 125  # lecturer's slide totals


# ---------------------------------------------------------------- Greenberg 2.2 and 3.2
def g22_g32():
    y = COAL[:41]                      # 1851-1891, the series in Aula/class-01 class1-poisson.html
    n, s = y.size, int(y.sum())
    a, b = 2.0, 1.0                    # illustrative prior G(2, 1)
    a1, b1 = a + s, b + n
    w = b / (b + n)
    post_mean = a1 / b1
    print(f"G2.2: n={n} s={s} ybar={s/n:.6f} a1={a1:.0f} b1={b1:.0f} w={w:.6f} "
          f"post_mean={post_mean:.6f} weighted={w*a/b + (1-w)*s/n:.6f}")
    close(s, 127, 0, "G2.2 sum"); close(s / n, 3.097561, 5e-7, "G2.2 ybar")
    close(w, 0.023810, 5e-7, "G2.2 w"); close(post_mean, 3.071429, 5e-7, "G2.2 mean")
    close(w * a / b + (1 - w) * s / n, post_mean, 1e-12, "G2.2 weighted average")
    # G3.2: negative binomial predictive, checked against direct integration over theta.
    pmf = lambda k: exp(lgamma(a1 + k) - lgamma(a1) - lgamma(k + 1)
                        + a1 * log(b1 / (b1 + 1)) - k * log(b1 + 1))
    for k in (0, 3, 7):
        num, _ = integrate.quad(lambda t: stats.poisson.pmf(k, t) * stats.gamma.pdf(t, a1, scale=1 / b1),
                                0, 30, points=[post_mean], limit=200)
        close(pmf(k), num, 1e-9, f"G3.2 predictive pmf at {k}")
    pmean, pvar = a1 / b1, a1 / b1 * (1 + 1 / b1)
    print(f"G3.2: P(y=0)={pmf(0):.6f} P(y=3)={pmf(3):.6f} mean={pmean:.6f} var={pvar:.6f}")
    close(pmf(0), 0.048054, 5e-7, "G3.2 P0"); close(pmf(3), 0.221297, 5e-7, "G3.2 P3")
    close(pvar, 3.144558, 5e-7, "G3.2 var")
    ks = np.arange(0, 80)
    pm = np.array([pmf(int(k)) for k in ks])
    close(pm.sum(), 1.0, 1e-10, "G3.2 pmf sums to 1")
    close((ks * pm).sum(), pmean, 1e-9, "G3.2 mean")
    close(((ks - pmean) ** 2 * pm).sum(), pvar, 1e-9, "G3.2 var by summation")


# ---------------------------------------------------------------- Greenberg 3.3
def g33():
    rng = np.random.default_rng(33)
    mu0, s20, n = 1.0, 4.0, 5
    y = rng.normal(2.0, 1.0, n)
    s2n = 1 / (1 / s20 + n)
    mun = s2n * (mu0 / s20 + y.sum())
    ynew = 2.7
    num, _ = integrate.quad(lambda m: stats.norm.pdf(ynew, m, 1) * stats.norm.pdf(m, mun, s2n ** 0.5),
                            -np.inf, np.inf)
    close(stats.norm.pdf(ynew, mun, (1 + s2n) ** 0.5), num, 1e-10, "G3.3 predictive density")


# ---------------------------------------------------------------- Greenberg 3.8
def g38():
    rows = []
    for m, e in ((100, 10), (200, 20)):
        for p in (0.9, 0.8, 0.7, 0.6, 0.5):
            e1 = round(p * e); e2 = e - e1
            lb = (lgamma(e + 1) + (e + 2) * log(m + 1) - (e + 1) * log(2 * m + 1)
                  - lgamma(e1 + 1) - lgamma(e2 + 1)) / log(10)
            rows.append((m, e, p, e1, e2, lb))
    # independent route: integrate the two marginal likelihoods numerically (per-page factorials cancel)
    for m, e, p, e1, e2, lb in rows:
        m1, _ = integrate.quad(lambda t: t ** e * np.exp(-2 * m * t) * np.exp(-t), 0, 1, epsabs=0, epsrel=1e-12, limit=200)
        f = lambda t, k: t ** k * np.exp(-m * t) * np.exp(-t)
        m2 = (integrate.quad(f, 0, 1, args=(e1,), epsabs=0, epsrel=1e-12, limit=200)[0]
              * integrate.quad(f, 0, 1, args=(e2,), epsabs=0, epsrel=1e-12, limit=200)[0])
        close(log(m1 / m2) / log(10), lb, 1e-6, f"G3.8 quadrature m={m} p={p}")
    print("G3.8: " + "; ".join(f"m={m} e1={e1} e2={e2} log10B12={lb:.3f}" for m, e, p, e1, e2, lb in rows))
    expected = [-0.283, 0.370, 0.796, 1.039, 1.118, -1.717, -0.310, 0.593, 1.105, 1.271]
    # pieces of the worked cell m=100, e1=9, e2=1 printed in the solution
    for got, e in ((lgamma(11), 15.104413), (12 * log(101), 55.381446), (11 * log(201), 58.336354),
                   (lgamma(10), 12.801827), (log(101), 4.615121), (log(201), 5.303305), (log(10), 2.302585)):
        close(got, e, 5e-7, "G3.8 worked piece")
    close(lgamma(11) + 12 * log(101) - 11 * log(201) - lgamma(10), -0.652323, 5e-7, "G3.8 worked numerator")
    for r, x in zip(rows, expected):
        close(r[5], x, 5e-4, f"G3.8 table m={r[0]} p={r[2]}")
    return rows


# ---------------------------------------------------------------- Greenberg 4.5
def g45():
    rng = np.random.default_rng(45)
    n, K = 12, 3
    X = np.column_stack([np.ones(n), rng.normal(size=(n, K - 1))])
    y = X @ np.array([1.0, -0.5, 2.0]) + rng.normal(size=n)
    b0, B0, a0, d0 = np.zeros(K), 2.0 * np.eye(K), 4.0, 3.0
    B1 = np.linalg.inv(X.T @ X + np.linalg.inv(B0))
    bbar = B1 @ (X.T @ y + np.linalg.solve(B0, b0))
    a1 = a0 + n
    d1 = d0 + y @ y + b0 @ np.linalg.solve(B0, b0) - bbar @ np.linalg.solve(B1, bbar)
    logml = (-n / 2 * log(np.pi) + 0.5 * np.linalg.slogdet(B1)[1] - 0.5 * np.linalg.slogdet(B0)[1]
             + lgamma(a1 / 2) - lgamma(a0 / 2) + a0 / 2 * log(d0) - a1 / 2 * log(d1))
    # independent route: y ~ multivariate t_{a0}(X b0, (d0/a0)(I + X B0 X'))
    S = d0 / a0 * (np.eye(n) + X @ B0 @ X.T)
    close(logml, stats.multivariate_t.logpdf(y, X @ b0, S, df=a0), 1e-9, "G4.5 marginal likelihood")


# ---------------------------------------------------------------- Greenberg 5.4
def g54():
    rng = np.random.default_rng(54)
    c = stats.beta.pdf(0.5, 3, 3)
    draws, tried = [], 0
    while len(draws) < 500:
        u1, u2 = rng.uniform(), rng.uniform()
        tried += 1
        if u2 <= stats.beta.pdf(u1, 3, 3) / c:
            draws.append(u1)
    d = np.array(draws)
    print(f"G5.4: c={c:.4f} tried={tried} acc={500/tried:.4f} mean={d.mean():.4f} "
          f"var={d.var(ddof=1):.5f} (true 0.5, {1/28:.5f})")
    close(c, 1.8750, 1e-12, "G5.4 c")
    close(d.mean(), 0.5045, 5e-5, "G5.4 mean"); close(d.var(ddof=1), 0.03883, 5e-6, "G5.4 var")
    close(500 / tried, 0.5556, 5e-5, "G5.4 acceptance")
    close(d.mean(), 0.5, 3 * (1 / 28 / 500) ** 0.5, "G5.4 mean vs truth")
    close((1 / 28 / 500) ** 0.5, 0.0085, 5e-5, "G5.4 se of mean"); close(1 / 28, 0.03571, 5e-6, "G5.4 true var")
    close(1 / 1.875, 0.5333, 5e-5, "G5.4 1/c")


# ---------------------------------------------------------------- Greenberg 6.2
def g62():
    a, b = 0.25, 0.125                 # the matrix (6.2) is (6.10) with alpha=0.25, beta=0.125
    P = np.array([[1 - a, a], [b, 1 - b]])
    pi = np.array([b, a]) / (a + b)
    close(np.abs(pi @ P - pi).max(), 0, 1e-15, "G6.2 invariance")
    P50 = np.linalg.matrix_power(P, 50)
    close(np.abs(P50 - pi).max(), 0, 1e-8, "G6.2 limit")
    print(f"G6.2: pi=({pi[0]:.6f}, {pi[1]:.6f}) lambda2={1-a-b:.3f} P^50 row1={P50[0].round(6)}")
    flip = np.array([[0, 1], [1, 0]])
    assert (np.linalg.matrix_power(flip, 101) == flip).all() and (np.linalg.matrix_power(flip, 100) == np.eye(2)).all()


# ---------------------------------------------------------------- Greenberg 7.3
def g73(G=10_000, burn=1_000, seed=73):
    y, n = COAL, COAL.size
    S = np.concatenate([[0], np.cumsum(y)])          # S[k] = y_1 + ... + y_k
    a10 = a20 = 0.5; b10 = b20 = 1.0
    k_grid = np.arange(1, n + 1)
    rng = np.random.default_rng(seed)
    k = n // 2
    out = np.empty((G, 3))
    for g in range(G + burn):
        t1 = rng.gamma(a10 + S[k], 1 / (b10 + k))
        t2 = rng.gamma(a20 + S[n] - S[k], 1 / (b20 + n - k))
        logp = k_grid * (t2 - t1) + S[1:] * np.log(t1 / t2)
        p = np.exp(logp - logp.max()); p /= p.sum()
        k = rng.choice(k_grid, p=p)
        if g >= burn:
            out[g - burn] = t1, t2, k
    t1s, t2s, ks = out[:, 0], out[:, 1], out[:, 2].astype(int)
    # exact posterior of k and exact marginal likelihood (theta's integrated analytically)
    sumlogfact = gammaln(y + 1).sum()
    logpyk = (a10 * log(b10) - lgamma(a10) + gammaln(a10 + S[1:]) - (a10 + S[1:]) * np.log(b10 + k_grid)
              + a20 * log(b20) - lgamma(a20) + gammaln(a20 + S[n] - S[1:])
              - (a20 + S[n] - S[1:]) * np.log(b20 + n - k_grid) - sumlogfact)
    logm_exact = logsumexp(logpyk) - log(n)
    pk = np.exp(logpyk - logsumexp(logpyk))
    Et1 = (pk * (a10 + S[1:]) / (b10 + k_grid)).sum()
    Et2 = (pk * (a20 + S[n] - S[1:]) / (b20 + n - k_grid)).sum()
    # Chib (1995): log m = log f(y|t*) + log pi(t*) - log pi(t*|y), ordinate Rao-Blackwellised over k draws
    s1, s2 = t1s.mean(), t2s.mean()
    loglik = logsumexp(-k_grid * s1 + S[1:] * log(s1) - (n - k_grid) * s2 + (S[n] - S[1:]) * log(s2)) \
        - log(n) - sumlogfact
    logprior = stats.gamma.logpdf(s1, a10, scale=1 / b10) + stats.gamma.logpdf(s2, a20, scale=1 / b20)
    ord_ = stats.gamma.logpdf(s1, a10 + S[ks], scale=1 / (b10 + ks)) \
        + stats.gamma.logpdf(s2, a20 + S[n] - S[ks], scale=1 / (b20 + n - ks))
    logpost = logsumexp(ord_) - log(G)
    logm_chib = loglik + logprior - logpost
    kvals, kcnt = np.unique(ks, return_counts=True)
    top = kvals[np.argsort(-kcnt)][:4]
    res = dict(t1=s1, t2=s2, t1sd=t1s.std(ddof=1), t2sd=t2s.std(ddof=1),
               t1ci=np.quantile(t1s, [0.025, 0.975]), t2ci=np.quantile(t2s, [0.025, 0.975]),
               Et1=Et1, Et2=Et2, kmode=int(top[0]), pk_mc={int(v): (ks == v).mean() for v in top},
               pk_ex={int(v): pk[v - 1] for v in top}, loglik=loglik, logprior=logprior,
               logpost=logpost, logm_chib=logm_chib, logm_exact=logm_exact)
    print(f"G7.3: E[t1]={s1:.4f} (exact {Et1:.4f}) sd={res['t1sd']:.4f} CI={res['t1ci'].round(3)}; "
          f"E[t2]={s2:.4f} (exact {Et2:.4f}) sd={res['t2sd']:.4f} CI={res['t2ci'].round(3)}")
    print("      p(k|y) MC/exact: " + ", ".join(f"k={v} (year {1850+v}): {res['pk_mc'][v]:.4f}/{res['pk_ex'][v]:.4f}" for v in top))
    print(f"      Chib: loglik={loglik:.4f} logprior={logprior:.4f} logpost={logpost:.4f} "
          f"logm={logm_chib:.4f}; exact logm={logm_exact:.4f}")
    close(s1, 3.0512, 5e-5, "G7.3 E t1"); close(s2, 0.9144, 5e-5, "G7.3 E t2")
    close(Et1, 3.0500, 5e-5, "G7.3 exact E t1"); close(Et2, 0.9147, 5e-5, "G7.3 exact E t2")
    close(s1, Et1, 0.02, "G7.3 MC vs exact t1"); close(s2, Et2, 0.01, "G7.3 MC vs exact t2")
    assert res["kmode"] == 41
    close(res["pk_ex"][41], 0.2482, 5e-5, "G7.3 exact p(k=41)")
    close(res["pk_mc"][41], 0.2514, 5e-5, "G7.3 MC p(k=41)")
    close(logm_exact, -179.4590, 5e-5, "G7.3 exact log m")
    close(logm_chib, -179.4592, 5e-5, "G7.3 Chib log m")
    close(logm_chib, logm_exact, 0.01, "G7.3 Chib vs exact")
    close(res["t1sd"], 0.2861, 5e-5, "G7.3 sd t1"); close(res["t2sd"], 0.1170, 5e-5, "G7.3 sd t2")
    for got, e in zip([*res["t1ci"], *res["t2ci"]], [2.513, 3.628, 0.702, 1.157]):
        close(got, e, 5e-4, "G7.3 CI")
    for kk, (mc, ex) in {40: (0.1903, 0.1848), 39: (0.1374, 0.1414), 42: (0.0991, 0.1010)}.items():
        close(res["pk_mc"][kk], mc, 5e-5, f"G7.3 MC p(k={kk})"); close(res["pk_ex"][kk], ex, 5e-5, f"G7.3 exact p(k={kk})")
    close(loglik, -172.2568, 5e-5, "G7.3 loglik"); close(logprior, -5.6234, 5e-5, "G7.3 logprior")
    close(logpost, 1.5790, 5e-5, "G7.3 logpost")
    return res


# ---------------------------------------------------------------- Greenberg 7.5
def g75(G=10_000, burn=1_000, seed=75):
    rng = np.random.default_rng(seed)
    rows = {}
    for s2 in (0.1, 1.0, 10.0, 100.0):
        x, acc = 0.0, 0
        out = np.empty(G)
        for g in range(G + burn):
            prop = x + rng.normal(0, s2 ** 0.5)
            if np.log(rng.uniform()) <= abs(x) - abs(prop):      # log f(prop) - log f(x)
                x = prop; acc += g >= burn
            if g >= burn:
                out[g - burn] = x
        z = out - out.mean()
        acf = lambda L: (z[L:] @ z[:-L]) / (z @ z)
        rows[s2] = (out.mean(), out.var(ddof=1), acf(1), acf(10), acc / G)
    print("G7.5: " + "; ".join(f"s2={s2}: mean={m:.3f} var={v:.3f} r1={r1:.3f} r10={r10:.3f} acc={a:.3f}"
                               for s2, (m, v, r1, r10, a) in rows.items()))
    expected = {0.1: (-0.306, 2.317, 0.983, 0.852, 0.8835), 1.0: (-0.097, 1.908, 0.880, 0.285, 0.6970),
                10.0: (-0.056, 1.976, 0.668, 0.025, 0.3928), 100.0: (-0.062, 2.120, 0.714, 0.018, 0.1577)}
    for s2, vals in expected.items():
        for got, exp_, nm in zip(rows[s2], vals, ("mean", "var", "r1", "r10", "acc")):
            close(got, exp_, 5e-4, f"G7.5 s2={s2} {nm}")
    return rows


# ---------------------------------------------------------------- Greenberg 7.7/7.8
def g78(n=50, G=10_000, burn=1_000, seed=78):
    rng = np.random.default_rng(seed)
    beta_true = rng.gamma(2.0, 1.0)                    # beta ~ G(2, 1)
    s2_true = 1 / rng.gamma(2.5, 1 / 1.5)              # sigma^2 ~ IG(5/2, 3/2)
    x = rng.normal(size=n)
    y = beta_true * x + rng.normal(0, s2_true ** 0.5, n)
    Sxx, Sxy, Syy = x @ x, x @ y, y @ y
    logpost = lambda b, s2: np.log(b) - b - (Syy - 2 * b * Sxy + b * b * Sxx) / (2 * s2)

    def mode_scale(s2):
        bh = ((Sxy - s2) + np.sqrt((Sxy - s2) ** 2 + 4 * s2 * Sxx)) / (2 * Sxx)
        return bh, 1 / (1 / bh ** 2 + Sxx / s2)

    b, s2, acc = max(Sxy / Sxx, 0.1), 1.0, 0
    out = np.empty((G, 2))
    for g in range(G + burn):
        s2 = 1 / rng.gamma(2.5 + n / 2, 1 / (1.5 + (Syy - 2 * b * Sxy + b * b * Sxx) / 2))
        bh, V = mode_scale(s2)
        sd = V ** 0.5
        lo = stats.t.cdf(-bh / sd, 5)
        prop = bh + sd * stats.t.ppf(rng.uniform(lo, 1.0), 5)
        logq = lambda v: stats.t.logpdf((v - bh) / sd, 5)
        if np.log(rng.uniform()) <= logpost(prop, s2) - logpost(b, s2) + logq(b) - logq(prop):
            b = prop; acc += g >= burn
        if g >= burn:
            out[g - burn] = b, s2
    bs, s2s = out[:, 0], out[:, 1]
    res = dict(beta_true=beta_true, s2_true=s2_true, bmean=bs.mean(), bsd=bs.std(ddof=1),
               bci=np.quantile(bs, [0.025, 0.975]), s2mean=s2s.mean(), s2sd=s2s.std(ddof=1),
               s2ci=np.quantile(s2s, [0.025, 0.975]), acc=acc / G, ols=Sxy / Sxx,
               s2ols=(Syy - Sxy ** 2 / Sxx) / (n - 1))
    print(f"G7.8: beta_true={beta_true:.4f} s2_true={s2_true:.4f} OLS={res['ols']:.4f} s2_OLS={res['s2ols']:.4f}; "
          f"E[beta|y]={res['bmean']:.4f} sd={res['bsd']:.4f} CI={res['bci'].round(4)}; "
          f"E[s2|y]={res['s2mean']:.4f} sd={res['s2sd']:.4f} CI={res['s2ci'].round(4)}; acc={res['acc']:.4f}")
    # the 7.7 formula is the sigma^2 = 1 case
    bh1, V1 = mode_scale(1.0)
    db = 1e-6
    close((logpost(bh1 + db, 1.0) - logpost(bh1 - db, 1.0)) / (2 * db), 0, 1e-5, "G7.7 mode")
    close(-1 / ((logpost(bh1 + 1e-4, 1.0) - 2 * logpost(bh1, 1.0) + logpost(bh1 - 1e-4, 1.0)) / 1e-8),
          V1, 1e-4, "G7.7 scale")
    for k, v in dict(beta_true=0.9369, s2_true=0.9079, ols=0.9788, s2ols=1.0762, bmean=0.9806,
                     bsd=0.1785, s2mean=1.0702, s2sd=0.2121, acc=0.9267).items():
        close(res[k], v, 5e-5, f"G7.8 {k}")
    close(res["bci"][0], 0.6329, 5e-5, "G7.8 bci lo"); close(res["bci"][1], 1.3353, 5e-5, "G7.8 bci hi")
    close(res["s2ci"][0], 0.7373, 5e-5, "G7.8 s2ci lo"); close(res["s2ci"][1], 1.5616, 5e-5, "G7.8 s2ci hi")
    return res


# ---------------------------------------------------------------- Greenberg 8.1
def g81(G=10_000, burn=1_000, seed=81):
    raw = np.loadtxt(DATA / "babies.data", skiprows=1)
    bwt, gest, parity, age, height, weight, smoke = raw.T
    keep = (gest != 999) & (age != 99) & (height != 99) & (weight != 999) & (smoke != 9)
    X = np.column_stack([np.ones(keep.sum()), gest[keep], parity[keep], age[keep], height[keep],
                         weight[keep], smoke[keep]])
    y = bwt[keep]
    n, K = X.shape
    b0, B0inv = np.zeros(K), np.eye(K) / 1e4          # beta ~ N(0, 10^4 I)
    a0, d0 = 6.0, 1800.0                              # sigma^2 ~ IG(a0/2, d0/2), prior mean 450
    XtX, Xty = X.T @ X, X.T @ y
    ols = np.linalg.solve(XtX, Xty)
    e = y - X @ ols
    ols_se = np.sqrt(np.diag(np.linalg.inv(XtX)) * (e @ e) / (n - K))
    rng = np.random.default_rng(seed)
    s2 = (e @ e) / (n - K)
    out = np.empty((G, K + 1))
    for g in range(G + burn):
        B1 = np.linalg.inv(XtX / s2 + B0inv)
        bbar = B1 @ (Xty / s2 + B0inv @ b0)
        beta = bbar + np.linalg.cholesky(B1) @ rng.normal(size=K)
        r = y - X @ beta
        s2 = 1 / rng.gamma((a0 + n) / 2, 2 / (d0 + r @ r))
        if g >= burn:
            out[g - burn, :K], out[g - burn, K] = beta, s2
    names = ["const", "gestation", "parity", "age", "height", "weight", "smoke", "sigma2"]
    mean, sd = out.mean(0), out.std(0, ddof=1)
    ci = np.quantile(out, [0.025, 0.975], axis=0)
    p_neg = (out[:, 6] < 0).mean()
    print(f"G8.1: n={n} K={K}")
    for j, nm in enumerate(names):
        o = f" OLS={ols[j]:.4f} (se {ols_se[j]:.4f})" if j < K else ""
        print(f"      {nm:9s} mean={mean[j]:.4f} sd={sd[j]:.4f} CI=({ci[0, j]:.4f}, {ci[1, j]:.4f}){o}")
    print(f"      P(beta_smoke<0|y)={p_neg:.4f}")
    assert n == 1174 and K == 7
    exp_mean = [-78.6033, 0.4421, -3.3401, -0.0114, 1.1342, 0.0508, -8.4084, 251.1114]
    exp_sd = [14.1929, 0.0292, 1.1372, 0.0864, 0.2039, 0.0254, 0.9465, 10.3514]
    for j in range(K + 1):
        close(mean[j], exp_mean[j], 5e-5, f"G8.1 mean {names[j]}")
        close(sd[j], exp_sd[j], 5e-5, f"G8.1 sd {names[j]}")
    close(ci[0, 6], -10.2359, 5e-5, "G8.1 smoke lo"); close(ci[1, 6], -6.5505, 5e-5, "G8.1 smoke hi")
    close(ols[6], -8.4007, 5e-5, "G8.1 OLS smoke"); close(ols_se[6], 0.9538, 5e-5, "G8.1 OLS se smoke")
    close(mean[6], ols[6], 0.05, "G8.1 posterior mean near OLS")
    exp_lo = [-106.1171, 0.3845, -5.5466, -0.1791, 0.7389, 0.0008, -10.2359, 231.6747]
    exp_hi = [-51.1482, 0.4982, -1.1178, 0.1587, 1.5368, 0.1019, -6.5505, 272.2228]
    exp_ols = [-80.4109, 0.4440, -3.3272, -0.0090, 1.1540, 0.0502, -8.4007]
    exp_se = [14.3466, 0.0291, 1.1289, 0.0858, 0.2050, 0.0252, 0.9538]
    for j in range(K + 1):
        close(ci[0, j], exp_lo[j], 5e-5, f"G8.1 lo {names[j]}"); close(ci[1, j], exp_hi[j], 5e-5, f"G8.1 hi {names[j]}")
    for j in range(K):
        close(ols[j], exp_ols[j], 5e-5, f"G8.1 OLS {names[j]}"); close(ols_se[j], exp_se[j], 5e-5, f"G8.1 se {names[j]}")
    close(mean[6] * 28.3495, -238.37, 5e-3, "G8.1 smoke in grams"); close((~keep).sum(), 62, 0, "G8.1 dropped rows")
    assert p_neg == 1.0
    return dict(mean=mean, sd=sd, ci=ci, ols=ols, ols_se=ols_se, n=n)


# ---------------------------------------------------------------- Tsay 12.1
def t121():
    prec = 1 / 25 + 1 / 4
    var = 1 / prec
    w = (1 / 4) / prec
    print(f"T12.1: precision={prec:.2f} var={var:.6f} weight={w:.6f} (25/29={25/29:.6f})")
    close(var, 100 / 29, 1e-12, "T12.1 var"); close(w, 25 / 29, 1e-12, "T12.1 weight")
    close(var, 3.448276, 5e-7, "T12.1 var dec"); close(w, 0.862069, 5e-7, "T12.1 w dec")
    x = 1.7                                            # brute force at one data point
    grid = np.linspace(-30, 30, 200_001)
    dens = stats.norm.pdf(x, grid, 2) * stats.norm.pdf(grid, 0, 5)
    dens /= np.trapezoid(dens, grid)
    m = np.trapezoid(grid * dens, grid)
    close(m, w * x, 1e-6, "T12.1 brute mean")
    close(np.trapezoid((grid - m) ** 2 * dens, grid), var, 1e-6, "T12.1 brute var")


# ---------------------------------------------------------------- Tsay 12.2
def t122(n=500, G=2_000, burn=100, seed=122):
    rng = np.random.default_rng(seed)
    beta_t, phi_t, p = np.array([1.0, 2.0]), np.array([0.5, -0.3]), 2
    X = np.column_stack([np.ones(n), rng.normal(size=n)])
    z = np.zeros(n + 100)
    a = rng.normal(size=n + 100)
    for t in range(2, n + 100):
        z[t] = phi_t @ z[t - 2:t][::-1] + a[t]
    y = X @ beta_t + z[100:]
    bo, Sinv = np.zeros(2), np.eye(2) / 100            # beta ~ N(0, 100 I)
    phio, Ainv = np.zeros(p), np.eye(p)                # phi ~ N(0, I)
    v, lam = 3.0, 1.0                                  # v*lam/sigma^2 ~ chi2_v
    lagmat = lambda u: np.column_stack([u[p - j - 1:len(u) - j - 1] for j in range(p)])  # u_{t-1..t-p}
    beta = np.linalg.lstsq(X, y, rcond=None)[0]
    phi, s2 = np.zeros(p), 1.0
    out = np.empty((G, 5))
    for g in range(G + burn):
        # beta | phi, s2: filter y and x by phi(B), t = p+1..n
        yo = y[p:] - lagmat(y) @ phi
        Xo = X[p:] - np.einsum("j,jtk->tk", phi, np.stack([X[p - j - 1:n - j - 1] for j in range(p)]))
        Sst = np.linalg.inv(Xo.T @ Xo / s2 + Sinv)
        beta = Sst @ (Xo.T @ yo / s2 + Sinv @ bo) + np.linalg.cholesky(Sst) @ rng.normal(size=2)
        # phi | beta, s2: AR(p) regression on z_t = y_t - x_t'beta
        zz = y - X @ beta
        W, zt = lagmat(zz), zz[p:]
        Ast = np.linalg.inv(W.T @ W / s2 + Ainv)
        phi = Ast @ (W.T @ zt / s2 + Ainv @ phio) + np.linalg.cholesky(Ast) @ rng.normal(size=p)
        # s2 | beta, phi: (v lam + sum a_t^2)/s2 ~ chi2_{v + n - p}
        at = zt - W @ phi
        s2 = (v * lam + at @ at) / rng.chisquare(v + n - p)
        if g >= burn:
            out[g - burn] = *beta, *phi, s2
    m, sd = out.mean(0), out.std(0, ddof=1)
    print("T12.2: posterior means " + ", ".join(f"{nm}={mm:.4f} (sd {ss:.4f})" for nm, mm, ss in
                                               zip(["b0", "b1", "phi1", "phi2", "s2"], m, sd)))
    truth = np.array([1.0, 2.0, 0.5, -0.3, 1.0])
    assert (np.abs(m - truth) < 2 * sd).all(), "T12.2 Gibbs does not recover the truth"
    for got, e in zip(sd, [0.0550, 0.0394, 0.0415, 0.0413, 0.0669]):
        close(got, e, 5e-5, "T12.2 posterior sd")
    for got, exp_ in zip(m, [1.0317, 2.0554, 0.5182, -0.3652, 1.0533]):
        close(got, exp_, 5e-5, "T12.2 posterior mean")


# ---------------------------------------------------------------- Tsay 12.3
def t123():
    rng = np.random.default_rng(123)
    phi, s2, n, h, p = np.array([0.6, -0.2]), 1.0, 120, 60, 2
    x = np.zeros(n + 50)
    for t in range(2, n + 50):
        x[t] = phi @ x[t - 2:t][::-1] + rng.normal()
    x = x[50:]
    mu_o, Sig_o = np.array([0.0, 0.0]), 4.0 * np.eye(2)
    psi = np.concatenate([[1.0], -phi])                # a_t = sum_k psi_k x_{t-k}
    C, d = [], []
    for t in range(h, h + p + 2):                      # equations t = h, ..., h+p+1
        c = [psi[t - h] if 0 <= t - h <= p else 0.0, psi[t - h - 1] if 0 <= t - h - 1 <= p else 0.0]
        known = sum(psi[k] * x[t - k] for k in range(p + 1) if t - k not in (h, h + 1))
        C.append(c); d.append(-known)
    C, d = np.array(C), np.array(d)
    Prec = np.linalg.inv(Sig_o) + C.T @ C / s2
    Sig_s = np.linalg.inv(Prec)
    mu_s = Sig_s @ (np.linalg.solve(Sig_o, mu_o) + C.T @ d / s2)
    CtC = C.T @ C
    close(CtC[0, 0], 1 + phi @ phi, 1e-12, "T12.3 C'C 11"); close(CtC[1, 1], 1 + phi @ phi, 1e-12, "T12.3 C'C 22")
    close(CtC[0, 1], -phi[0] + phi[0] * phi[1], 1e-12, "T12.3 C'C 12")

    def logpost(m):                                    # brute force: prior x full AR(p) likelihood
        xx = x.copy(); xx[h], xx[h + 1] = m
        a = xx[p:] - np.column_stack([xx[p - 1:-1], xx[p - 2:-2]]) @ phi
        dm = m - mu_o
        return -0.5 * dm @ np.linalg.solve(Sig_o, dm) - 0.5 * (a @ a) / s2
    for _ in range(5):
        m = rng.normal(size=2) * 3
        close(logpost(m) - logpost(mu_s), -0.5 * (m - mu_s) @ Prec @ (m - mu_s), 1e-9, "T12.3 posterior")


# ---------------------------------------------------------------- Bolfarine 4.3, 4.5, 4.9, 4.10, 5.11
def bolfarine():
    m = 10
    R = lambda t: t * (1 - t) / m
    exact = sum(stats.binom.pmf(k, m, 0.3) * (0.3 - k / m) ** 2 for k in range(m + 1))
    close(R(0.3), exact, 1e-12, "B4.3 risk")
    close(integrate.quad(R, 0, 1)[0], 1 / (6 * m), 1e-12, "B4.3 Bayes risk")
    a, b = 3.0, 2.0                                    # B4.5: Bayes risk of X = E[theta] = a/b
    close(integrate.quad(lambda t: t * stats.gamma.pdf(t, a, scale=1 / b), 0, np.inf)[0], a / b, 1e-9, "B4.5")
    risk_bayes = integrate.quad(lambda t: stats.gamma.pdf(t, a, scale=1 / b) * sum(
        stats.poisson.pmf(k, t) * (t - (a + k) / (b + 1)) ** 2 for k in range(80)), 0, 40)[0]
    close(risk_bayes, a / (b * (b + 1)), 1e-8, "B4.5 Bayes-estimator risk")
    close((2 / 3) ** 4, 0.1975, 5e-5, "B4.9 x=3")
    for nn, s in ((1, 0), (1, 3), (4, 7)):              # B4.9: E[e^-theta | x] = ((n+1)/(n+2))^(s+1)
        num = integrate.quad(lambda t: np.exp(-t) * stats.gamma.pdf(t, s + 1, scale=1 / (nn + 1)), 0, np.inf)[0]
        close(num, ((nn + 1) / (nn + 2)) ** (s + 1), 1e-10, "B4.9")
    aa, bb, nn, xm = 1.0, 2.0, 5, 1.7                  # B4.10: Pareto posterior mean
    M = max(aa, xm)
    dens = lambda t: (nn + bb) * M ** (nn + bb) / t ** (nn + bb + 1)
    close(integrate.quad(dens, M, np.inf)[0], 1.0, 1e-9, "B4.10 normalised")
    close(integrate.quad(lambda t: t * dens(t), M, np.inf)[0], (nn + bb) * M / (nn + bb - 1), 1e-8, "B4.10 mean")
    lo, hi = stats.gamma.ppf([0.025, 0.975], 19, scale=1 / 11)   # B5.11: posterior Gama(19, 11)
    c_lo, c_hi = stats.chi2.ppf([0.025, 0.975], 38)
    print(f"B5.11: chi2_38 quantiles=({c_lo:.4f}, {c_hi:.4f}) interval=({lo:.4f}, {hi:.4f}) "
          f"mean={19/11:.4f} MLE={18/10:.4f}")
    close(c_lo / 22, lo, 1e-12, "B5.11 chi2 route"); close(c_hi / 22, hi, 1e-12, "B5.11 chi2 route")
    close(c_lo, 22.8785, 5e-5, "B5.11 c_lo"); close(c_hi, 56.8955, 5e-5, "B5.11 c_hi")
    close(lo, 1.0399, 5e-5, "B5.11 lo"); close(hi, 2.5862, 5e-5, "B5.11 hi")
    close(19 / 11, 1.7273, 5e-5, "B5.11 mean")


# ---------------------------------------------------------------- Morettin-Singer B.16, B.19/B.20, C.5
def ms_b16(N=1_000, seed=16):
    rng = np.random.default_rng(seed)
    acc, tried = [], 0
    while len(acc) < N:
        xg = rng.exponential(1.0)
        tried += 1
        if xg <= 1 and rng.uniform() <= xg ** 2:       # accept with prob x^2 1(x <= 1)
            acc.append(xg)
    d = np.array(acc)
    Z = 2 - 5 / np.e
    m1 = (6 - 16 / np.e) / Z
    m2 = (24 - 65 / np.e) / Z
    print(f"MS B.16: Z={Z:.6f} tried={tried} acc={N/tried:.4f} mean={d.mean():.4f} (true {m1:.4f}) "
          f"var={d.var(ddof=1):.4f} (true {m2-m1**2:.4f})")
    close(Z, integrate.quad(lambda t: t * t * np.exp(-t), 0, 1)[0], 1e-12, "B.16 Z")
    close(Z, 0.160603, 5e-7, "B.16 Z dec"); close(m1, 0.7094, 5e-5, "B.16 true mean")
    close(m2 - m1 ** 2, 0.0437, 5e-5, "B.16 true var")
    close(N / tried, 0.1505, 5e-5, "B.16 acceptance"); close(d.mean(), 0.7105, 5e-5, "B.16 mean")
    close(d.var(ddof=1), 0.0443, 5e-5, "B.16 var")
    close(d.mean(), m1, 3 * (0.0437 / N) ** 0.5, "B.16 mean vs truth")
    assert tried == 6644
    close(5 / np.e, 1.839397, 5e-7, "B.16 5/e"); close(16 / np.e, 5.886071, 5e-7, "B.16 16/e")
    close(65 / np.e, 23.912164, 5e-7, "B.16 65/e")
    close(6 - 16 / np.e, 0.113929, 5e-7, "B.16 int x^3"); close(24 - 65 / np.e, 0.087836, 5e-7, "B.16 int x^4")
    close(m2, 0.546917, 5e-6, "B.16 E x^2"); close(m1 ** 2, 0.503225, 5e-6, "B.16 mean^2"); close(m1, 0.709383, 5e-6, "B.16 mean 6dp")
    close(N / Z, 6226.5, 0.05, "B.16 expected trials")
    close((N * (1 - Z)) ** 0.5 / Z, 180.4, 0.05, "B.16 sd trials")
    close(Z / (1 - np.exp(-1)), 0.2541, 5e-5, "B.16 truncated-proposal acceptance")


def ms_b19(N=10_000, seed=19):
    rng = np.random.default_rng(seed)
    pi = np.array([0.2, 0.3, 0.1, 0.1, 0.3]); g = np.full(5, 0.2)
    c = (pi / g).max()
    vals, iters = np.empty(N, int), np.empty(N, int)
    for i in range(N):
        k = 0
        while True:
            k += 1
            j = rng.integers(5)
            if rng.uniform() <= pi[j] / (c * g[j]):
                break
        vals[i], iters[i] = j + 1, k
    freq = np.bincount(vals, minlength=6)[1:] / N
    print(f"MS B.19/B.20: c={c:.2f} mean iterations={iters.mean():.4f} freq={freq.round(4)}")
    close(c, 1.5, 1e-12, "B.19 c")
    close(iters.mean(), 1.5026, 5e-5, "B.19 mean iters"); close(iters.mean(), c, 0.05, "B.19 vs c")
    for got, e in zip(freq, [0.1993, 0.3045, 0.0985, 0.0995, 0.2982]):
        close(got, e, 5e-5, "B.19 freq")
    assert np.abs(freq - pi).max() < 0.015


def ms_c5(N=200, burn=50, seed=5):
    y1, y2, y3, y4 = 125, 18, 20, 34
    rng = np.random.default_rng(seed)
    th = 0.5
    out = np.empty((N, 2))
    for i in range(N):
        x2 = rng.binomial(y1, th / (2 + th))             # z | theta, y
        th = rng.beta(x2 + y4 + 1, y2 + y3 + 1)          # theta | z, y (flat prior)
        out[i] = x2, th
    keep = out[burn:]
    kern = lambda t: np.exp(y1 * np.log(2 + t) + (y2 + y3) * np.log(1 - t) + y4 * np.log(t) - 160)
    Z = integrate.quad(kern, 0, 1)[0]
    pm = integrate.quad(lambda t: t * kern(t), 0, 1)[0] / Z
    psd = (integrate.quad(lambda t: t * t * kern(t), 0, 1)[0] / Z - pm ** 2) ** 0.5
    print(f"MS C.5: draws kept={len(keep)} mean theta={keep[:,1].mean():.4f} sd={keep[:,1].std(ddof=1):.4f} "
          f"mean z={keep[:,0].mean():.2f}; exact posterior mean={pm:.4f} sd={psd:.4f}; first 5 theta={out[:5,1].round(4)}")
    close(keep[:, 1].mean(), 0.6155, 5e-5, "C.5 mean"); close(keep[:, 1].std(ddof=1), 0.0523, 5e-5, "C.5 sd")
    close(keep[:, 0].mean(), 29.36, 5e-3, "C.5 mean z")
    close(pm, 0.6228, 5e-5, "C.5 exact mean"); close(psd, 0.0509, 5e-5, "C.5 exact sd")
    close(keep[:, 1].mean(), pm, 0.02, "C.5 MC vs exact")
    for got, e in zip(out[:5, 1], [0.5649, 0.5648, 0.5233, 0.6507, 0.6390]):
        close(got, e, 5e-5, "C.5 first draws")
    close(keep[:, 1].std(ddof=1) / len(keep) ** 0.5, 0.0043, 5e-5, "C.5 naive se")


if __name__ == "__main__":
    g22_g32(); g33(); g38(); g45(); g54(); g62(); g73(); g75(); g78(); g81()
    t121(); t122(); t123(); bolfarine(); ms_b16(); ms_b19(); ms_c5()
    print("PASS")
