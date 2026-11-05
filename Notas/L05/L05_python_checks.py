"""Classes 5+6 (L05) reference implementation with self-checks against the sources' printed numbers.

Run: python Notas/L05/L05_python_checks.py   (numpy, scipy, pandas, statsmodels, linearmodels)
Every section asserts the numbers of one section note and prints a one-line summary; the first
mismatch aborts with an AssertionError naming it. Shown section by section in L05-10-python.md.

Reused, not rewritten: figures/make_figures.py (imported as mf) supplies the Simpson weights, the
collider correlation, the exact OVB moments and their Monte Carlo, the IV plims and calibration
constants, the DiD cell means and the RDD local-polynomial fit. Importing it draws nothing.
"""
import itertools
import pathlib
import sys

import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
from linearmodels.iv import IV2SLS
from scipy import stats

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent / "figures"))
import make_figures as mf  # noqa: E402

DATA = mf.DATA


def near(x, printed, dec):
    """True when x rounds to the printed value at `dec` decimals (half a unit in the last place)."""
    return abs(x - printed) <= 0.5 * 10.0 ** -dec + 1e-9


def check(x, printed, dec, what):
    assert near(x, printed, dec), f"{what}: computed {x!r}, source prints {printed}"


# ============================================================================ 1 · DAGs and d-separation (L05-01)
def ancestors(dag, nodes):
    """All ancestors of `nodes` (inclusive) in `dag`, a dict child -> set of parents."""
    out, stack = set(nodes), list(nodes)
    while stack:
        for p in dag.get(stack.pop(), set()):
            if p not in out:
                out.add(p)
                stack.append(p)
    return out


def d_separated(dag, x, y, z):
    """True when x and y are d-separated given the set z (moral graph of the ancestral set, z deleted).

    dag: dict child -> set of parents (every node a key). Lauritzen's criterion, equivalent to the
    path-blocking definition on slide p. 11.
    """
    keep = ancestors(dag, {x, y} | set(z))
    adj = {v: set() for v in keep}
    for c in keep:
        ps = dag[c] & keep
        for p in ps:
            adj[c].add(p)
            adj[p].add(c)
        for p, q in itertools.combinations(ps, 2):      # marry the parents
            adj[p].add(q)
            adj[q].add(p)
    seen, stack = {x}, [x]
    while stack:
        for v in adj[stack.pop()] - set(z):
            if v == y:
                return False
            if v not in seen:
                seen.add(v)
                stack.append(v)
    return True


def paths(dag, x, y):
    """All simple paths between x and y in the skeleton, each as a list of (node, arrow-to-next) pairs."""
    nb = {v: set() for v in dag}
    for c, ps in dag.items():
        for p in ps:
            nb[c].add(p)
            nb[p].add(c)
    out = []

    def walk(path):
        if path[-1] == y:
            out.append(list(path))
            return
        for v in nb[path[-1]]:
            if v not in path:
                walk(path + [v])
    walk([x])
    return out


def junctions(dag):
    """Every (a, b, c) with a - b - c adjacent and a, c distinct, classified chain / fork / collider."""
    nb = {v: set() for v in dag}
    for c, ps in dag.items():
        for p in ps:
            nb[c] |= {p}
            nb[p] |= {c}
    kinds = {"chain": 0, "fork": 0, "collider": 0}
    for b in dag:
        for a, c in itertools.combinations(sorted(nb[b]), 2):
            into = (a in dag[b]) + (c in dag[b])               # arrows pointing into b
            kinds["collider" if into == 2 else "fork" if into == 0 else "chain"] += 1
    return kinds


# slide p. 11 (example 1) and p. 12 (example 2); slide p. 9 (Harrison's DAG)
EX1 = {"Z": set(), "X": set(), "W": {"Z", "X"}, "U": {"W"}, "Y": {"X"}}
EX2 = {"T": set(), "Z": {"T"}, "X": set(), "W": {"Z", "X"}, "U": {"W"}, "Y": {"X", "T"}}
HARRISON = {"Z1": set(), "Z2": set(), "Z3": {"Z1", "Z2"}, "X": {"Z1", "Z3"}, "W": {"X"}, "Y": {"W", "Z2", "Z3"}}


def section1():
    # example 1
    assert d_separated(EX1, "Z", "Y", [])
    assert not d_separated(EX1, "Z", "Y", ["W"]) and not d_separated(EX1, "Z", "Y", ["U"])
    assert d_separated(EX1, "Z", "Y", ["W", "X"])
    # example 2: the slide's two lists, every set checked
    connected = [["W"], ["U"], ["W", "U"], ["W", "T"], ["U", "T"], ["W", "U", "T"], ["W", "X"], ["U", "X"], ["W", "U", "X"]]
    separated = [["T"], ["X", "T"], ["W", "X", "T"], ["U", "X", "T"], ["W", "U", "X", "T"]]
    assert not d_separated(EX2, "Z", "Y", [])
    assert all(not d_separated(EX2, "Z", "Y", s) for s in connected)
    assert all(d_separated(EX2, "Z", "Y", s) for s in separated)
    # exhaustive: these are ALL the separating subsets of {T, W, U, X}
    allsep = [set(s) for k in range(5) for s in itertools.combinations("TWUX", k) if d_separated(EX2, "Z", "Y", s)]
    assert sorted(map(sorted, allsep)) == sorted(map(sorted, map(set, separated)))
    # Harrison: 5 paths X ... Y and 15 junctions = 7 chains, 3 forks, 5 colliders (slides pp. 9-10)
    assert len(paths(HARRISON, "X", "Y")) == 5
    assert junctions(HARRISON) == {"chain": 7, "fork": 3, "collider": 5}
    # back-door sets for X -> Y: delete X's outgoing edge and test X indep Y | S
    bd = {k: (v - {"X"} if k == "W" else set(v)) for k, v in HARRISON.items()}
    bd["W"] = set()
    valid = {s: d_separated(bd, "X", "Y", list(s)) for s in [(), ("Z3",), ("Z1", "Z3"), ("Z2", "Z3"), ("Z1",), ("Z2",)]}
    assert valid == {(): False, ("Z3",): False, ("Z1", "Z3"): True, ("Z2", "Z3"): True, ("Z1",): False, ("Z2",): False}

    # the SEM of slide p. 10 with noise propagating (the equations as written), noise variance = variance of
    # the systematic part (the R code's sig.* rule): exact population covariance, then population regressions
    names = ["z1", "z2", "z3", "x", "w", "y"]
    B = np.zeros((6, 6))
    B[2, 0], B[2, 1] = 3, -1.5
    B[3, 0], B[3, 2] = 2, 2.5
    B[4, 3] = 3
    B[5, 4], B[5, 1], B[5, 2] = 2, 2, -3
    S = np.zeros((6, 6))
    S[0, 0], S[1, 1] = 1.72**2, 1.89**2
    for k in range(2, 6):
        b = B[k, :k]
        S[k, :k] = S[:k, :k] @ b
        S[:k, k] = S[k, :k]
        S[k, k] = 2 * (b @ S[:k, :k] @ b)                         # systematic + equal noise variance

    def coef_x(adj):
        idx = [3] + [names.index(c) for c in adj]
        return np.linalg.solve(S[np.ix_(idx, idx)], S[idx, 5])[0]
    pop = {tuple(a): coef_x(a) for a in ([], ["z3"], ["z1", "z3"], ["z2", "z3"], ["z1"], ["z2"])}
    assert abs(pop[("z1", "z3")] - 6) < 1e-10 and abs(pop[("z2", "z3")] - 6) < 1e-10   # total effect 3 x 2 = 6
    check(pop[("z3",)], 6.0051, 4, "M-bias from conditioning on the collider Z3 alone")
    check(pop[()], 5.4381, 4, "no adjustment")
    print(f"1 DAGs: slide d-separation lists confirmed (exhaustive); Harrison 7/3/5 junctions; X->Y effect 6: "
          f"adjust {{Z1,Z3}} or {{Z2,Z3}} 6.0000, {{Z3}} alone {pop[('z3',)]:.4f}, {{Z1}} {pop[('z1',)]:.4f}, "
          f"{{Z2}} {pop[('z2',)]:.4f}, none {pop[()]:.4f}")
    return pop


# ============================================================================ 2 · potential outcomes, adjustment, IPW (L05-02)
def drug_data():
    """700 rows (A = drug, G = 1 woman, Y = recovered) rebuilt from the slide p. 6 counts."""
    cells = [  # (A, G, recovered, n)
        (1, 0, 81, 87), (0, 0, 234, 270), (1, 1, 192, 263), (0, 1, 55, 80)]
    rows = []
    for a, g, r, n in cells:
        rows += [(a, g, 1)] * r + [(a, g, 0)] * (n - r)
    return pd.DataFrame(rows, columns=["A", "G", "Y"])


def section2():
    d = drug_data()
    assert len(d) == 700 and (d.G == 1).sum() == 343 and (d.A == 1).sum() == 350
    naive = d[d.A == 1].Y.mean() - d[d.A == 0].Y.mean()
    check(d[d.A == 1].Y.mean(), 0.78, 2, "drug 78%")
    check(d[d.A == 0].Y.mean(), 0.83, 2, "no drug 83%")
    pg = d.G.value_counts(normalize=True)
    strat = sum(pg[g] * (d[(d.A == 1) & (d.G == g)].Y.mean() - d[(d.A == 0) & (d.G == g)].Y.mean()) for g in (0, 1))
    e = d.groupby("G").A.mean()                                       # propensity e(g) = P(A = 1 | G = g)
    eg = d.G.map(e)
    ipw = np.mean(d.A * d.Y / eg - (1 - d.A) * d.Y / (1 - eg))
    ipw2 = np.mean(d.Y * (d.A - eg) / (eg * (1 - eg)))                  # second form of the proposition
    check(naive, -0.0457, 4, "naive gap")
    check(strat, 0.0537, 4, "adjustment formula")
    assert abs(ipw - strat) < 1e-12 and abs(ipw2 - strat) < 1e-12
    check(e[0], 0.2437, 4, "e(men) = 87/357")
    check(e[1], 0.7668, 4, "e(women) = 263/343")
    # ATT by standardising to the treated's gender mix
    pg1 = d[d.A == 1].G.value_counts(normalize=True)
    att = sum(pg1[g] * (d[(d.A == 1) & (d.G == g)].Y.mean() - d[(d.A == 0) & (d.G == g)].Y.mean()) for g in (0, 1))
    check(att, 0.0480, 4, "ATT")
    print(f"2 potential outcomes: naive {naive:+.4f}; adjusted ATE {strat:+.4f} = IPW {ipw:+.4f}; ATT {att:+.4f}; "
          f"e(men) {e[0]:.4f}, e(women) {e[1]:.4f}")


# ============================================================================ 3 · omitted variables (L05-03)
def section3():
    # omitted-variable.html: (y, x, z) ~ N(0, [[1, sxy, syz], [sxy, 1, rho], [syz, rho, 1]])
    sxy, syz, rho = 0.4, 0.5, 0.3
    S = np.array([[1, sxy, syz], [sxy, 1, rho], [syz, rho, 1]])
    s, Sxx = S[0, 1:], S[1:, 1:]
    coef = np.linalg.solve(Sxx, s)
    var = 1 - s @ coef
    assert np.allclose(coef, [(sxy - syz * rho) / (1 - rho**2), (syz - sxy * rho) / (1 - rho**2)])
    assert abs(var - (1 - rho**2 - sxy**2 - syz**2 + 2 * sxy * syz * rho) / (1 - rho**2)) < 1e-12
    assert abs(var - (1 - rho - sxy**2 - syz**2 + 2 * sxy * syz * rho) / (1 - rho**2)) > 0.05   # the page's "1 - rho" is a slip
    # OVB identity: short slope sxy = beta + gamma * rho
    b, g = coef
    assert abs(sxy - (b + g * rho)) < 1e-12
    # the site's simulation: exact mean beta + gamma rho and the Monte Carlo (shared with the figure)
    rhos = np.array([0.0, 0.5, 0.95])
    short, long_ = mf.ovb_mc(rhos)
    ms, ss, ml, sl = mf.ovb_exact(rhos)
    assert np.all(np.abs(short.mean(1) - ms) < 4 * ss / np.sqrt(mf.OVB_REPS))
    assert np.allclose(ms, [0.75, 1.35, 1.89]) and np.allclose(sl, [0.19245, 0.22222, 0.61633], atol=5e-5)
    # MHE Table 3.2.1: the drops attributed to the added controls
    check(0.132 - 0.114, 0.018, 3, "background controls")
    check(0.114 - 0.087, 0.027, 3, "AFQT")
    check(0.087 - 0.066, 0.021, 3, "occupation (bad control)")
    # proxy control (3.2.15): coefficient beta - gamma*pi1/pi2; with beta=.1, gamma=.05, pi1=.2, pi2=1
    beta, gamma, pi1, pi2 = 0.10, 0.05, 0.2, 1.0
    check(beta - gamma * pi1 / pi2, 0.09, 3, "proxy-control coefficient")
    print(f"3 OVB: conditional-mean coefficients and Var(y|x,z) checked (page's '1 - rho' is a slip); "
          f"short means {np.round(short.mean(1), 3)} vs exact {ms}")


# ============================================================================ 4 · errors in variables (L05-04)
def section4():
    rng = np.random.default_rng(11)
    n = 400_000
    beta, sx, su = 1.5, 1.0, 0.75
    lam = sx**2 / (sx**2 + su**2)
    check(lam, 0.64, 2, "reliability 1/(1+0.5625)")
    x = rng.normal(0, sx, n)
    y = 2 + beta * x + rng.normal(0, 1, n)
    w1 = x + rng.normal(0, su, n)
    w2 = x + rng.normal(0, su, n)                                    # second, independent measurement
    b_naive = np.cov(w1, y)[0, 1] / np.var(w1, ddof=1)
    b_iv = np.cov(w2, y)[0, 1] / np.cov(w2, w1)[0, 1]                # w2 instruments w1 (W section 15-4)
    assert abs(b_naive - beta * lam) < 0.01 and abs(b_iv - beta) < 0.01
    # error in y only: unbiased, noisier
    b_y = np.cov(x, y + rng.normal(0, 2, n))[0, 1] / np.var(x, ddof=1)
    assert abs(b_y - beta) < 0.02
    # with a control (W 9.36): x* = 0.8 x2 + r, Var(r) = 0.36
    x2 = rng.normal(size=n)
    xs = 0.8 * x2 + rng.normal(0, 0.6, n)
    y2 = beta * xs + 0.5 * x2 + rng.normal(size=n)
    x1 = xs + rng.normal(0, su, n)
    b = smf.ols("y ~ x1 + x2", pd.DataFrame(dict(y=y2, x1=x1, x2=x2))).fit().params.x1
    lam_r = 0.36 / (0.36 + su**2)
    assert abs(b - beta * lam_r) < 0.01
    print(f"4 attenuation: lambda {lam:.3f} -> naive {b_naive:.3f} (beta {beta}); IV with 2nd measure {b_iv:.3f}; "
          f"with a control lambda_r {lam_r:.3f} -> {b:.3f}")


# ============================================================================ 5 · instrumental variables (L05-05)
CONTROLS = "exper + expersq + black + smsa + south + smsa66 + reg662 + reg663 + reg664 + reg665 + reg666 + reg667 + reg668 + reg669"


def card():
    return pd.read_csv(DATA / "card.csv", na_values=".")


def section5():
    c = card()
    assert len(c) == 3010
    ols = smf.ols("lwage ~ educ + " + CONTROLS, c).fit()
    check(ols.params.educ, 0.0746933, 7, "OLS educ")
    check(ols.bse.educ, 0.0034983, 7, "OLS se")
    fs = smf.ols("educ ~ nearc4 + " + CONTROLS, c).fit()
    check(fs.params.nearc4, 0.320, 3, "first stage (W p. 473)")
    check(fs.tvalues.nearc4, 3.64, 2, "first-stage t")
    check(fs.rsquared, 0.477, 3, "first-stage R2")
    check(fs.tvalues.nearc4**2, 13.256, 3, "weak-instrument F")
    rf = smf.ols("lwage ~ nearc4 + " + CONTROLS, c).fit()
    ils = rf.params.nearc4 / fs.params.nearc4                         # indirect least squares (MHE 4.1.5)
    iv = IV2SLS.from_formula("lwage ~ 1 + " + CONTROLS + " + [educ ~ nearc4]", c).fit(cov_type="unadjusted", debiased=True)
    check(iv.params.educ, 0.1315038, 7, "IV educ")
    check(iv.std_errors.educ, 0.0549637, 7, "IV se")
    assert abs(ils - iv.params.educ) < 1e-10
    # 2SLS by hand: second stage on fitted educ gives the same point estimate (SEs differ, MHE p. 91)
    c2 = c.assign(educ_hat=fs.fittedvalues)
    check(smf.ols("lwage ~ educ_hat + " + CONTROLS, c2).fit().params.educ_hat, 0.1315038, 7, "manual 2SLS")
    # control-function (Wu-Hausman) test: t^2 on the first-stage residual
    c3 = c.assign(vhat=fs.resid)
    t = smf.ols("lwage ~ educ + vhat + " + CONTROLS, c3).fit().tvalues.vhat
    check(t**2, 1.168, 3, "Wu-Hausman")
    lo, hi = iv.params.educ - 1.96 * iv.std_errors.educ, iv.params.educ + 1.96 * iv.std_errors.educ
    check(lo, 0.024, 3, "CI low (W p. 474)")
    check(hi, 0.239, 3, "CI high")
    check(iv.std_errors.educ / ols.bse.educ, 15.7, 1, "SE ratio")
    # BIC-selected specification of the site
    sel = "exper + expersq + black + smsa + south + reg663"
    iv_s = IV2SLS.from_formula("lwage ~ 1 + " + sel + " + [educ ~ nearc4]", c).fit(cov_type="unadjusted", debiased=True)
    check(iv_s.params.educ, 0.1365294, 7, "IV selected")
    check(smf.ols("educ ~ nearc4 + " + sel, c).fit().tvalues.nearc4**2, 16.621, 3, "F selected")
    # MHE Table 4.1.2 Wald estimate
    check(-0.01349 / -0.1514, 0.0891, 4, "Wald (MHE p. 96)")
    # simple (no-controls) Wald with nearc4
    m = c.groupby("nearc4")[["lwage", "educ"]].mean()
    wald = (m.lwage[1] - m.lwage[0]) / (m.educ[1] - m.educ[0])
    check(wald, 0.188, 3, "simple Wald")
    # companion calibration: moments of the residuals after partialling out the controls
    X = np.column_stack([np.ones(len(c))] + [c[v].values for v in CONTROLS.split(" + ")])
    res = lambda v: v - X @ np.linalg.lstsq(X, v, rcond=None)[0]
    xr, yr, zr = res(c.educ.values * 1.0), res(c.lwage.values), res(c.nearc4.values * 1.0)
    V = lambda a, b: np.mean(a * b)
    sz2, d1 = V(zr, zr), V(zr, xr) / V(zr, zr)
    sx2 = V(xr, xr) - d1**2 * sz2
    b1 = V(zr, yr) / V(zr, xr)
    cxy = V(xr, yr) - b1 * V(xr, xr)
    sy2 = V(yr, yr) - b1**2 * V(xr, xr) - 2 * b1 * cxy
    rho = cxy / np.sqrt(sx2 * sy2)
    got = np.array([np.sqrt(sz2), np.sqrt(sx2), np.sqrt(sy2), b1, d1, rho])
    want = np.array([mf.IV_SZ, mf.IV_SX, mf.IV_SY, mf.IV_B1, mf.IV_D1, mf.IV_RHO])
    assert np.allclose(got, want, atol=5e-7), got
    o, i, lx = mf.iv_plims(rho, d1=d1, b1=b1, sz=np.sqrt(sz2), sx=np.sqrt(sx2), sy=np.sqrt(sy2))
    check(o, 0.0746933, 7, "calibrated OLS plim")
    check(i, 0.1315038, 7, "calibrated IV plim")
    # slide p. 19 / Greenberg p. 173: y on (x, z) gives beta1 + sigma_xy / sigma_x^2 on x (seeded Gaussian check)
    rng = np.random.default_rng(3)
    n = 400_000
    zz = rng.normal(size=n)
    ex, ey = rng.multivariate_normal([0, 0], [[1, 0.6], [0.6, 1]], n).T
    xx = 0.5 * zz + ex
    yy = 1.0 * xx + ey
    bxz = np.linalg.lstsq(np.column_stack([xx, zz]), yy, rcond=None)[0]
    assert abs(bxz[0] - 1.6) < 0.01 and abs(bxz[1] + 0.3) < 0.01         # 1 + 0.6, -0.6 * 0.5
    assert abs(np.cov(zz, yy)[0, 1] / np.cov(zz, xx)[0, 1] - 1.0) < 0.01
    print(f"5 IV: OLS {ols.params.educ:.7f}, IV {iv.params.educ:.7f} (se {iv.std_errors.educ:.7f}), first stage "
          f"{fs.params.nearc4:.3f} (t {fs.tvalues.nearc4:.2f}, F {fs.tvalues.nearc4**2:.3f}), Wu-Hausman {t**2:.3f}, "
          f"CI ({lo:.3f}, {hi:.3f}); simple Wald {wald:.4f}; calibration rho {rho:.4f}")


# ============================================================================ 6 · difference-in-differences (L05-06)
def section6():
    d, m = mf.did_cells()
    A = m[1, 1] - m[1, 0]
    B = m[0, 1] - m[0, 0]
    check(A, 0.4666667, 7, "A")
    check(B, -2.2833333, 7, "B")
    check(A - B, 2.75, 7, "DiD")
    # the other order of differencing (W p. 410)
    assert abs(((m[1, 1] - m[0, 1]) - (m[1, 0] - m[0, 0])) - (A - B)) < 1e-12
    d = d.assign(inter=d.time * d.treatment)
    r = smf.ols("outcome ~ time + treatment + inter", d).fit()
    for k, v, se in (("Intercept", 23.380, 1.098), ("time", -2.283, 1.553), ("treatment", -2.949, 1.224), ("inter", 2.750, 1.731)):
        check(r.params[k], v, 3, k)
        check(r.bse[k], se, 3, k + " se")
    check(np.sqrt(r.scale), 9.511, 3, "residual se")
    check(r.rsquared, 0.007587, 6, "R2")
    # regression parameters = cell-mean contrasts (MHE p. 175, W Table 13.3)
    assert abs(r.params.Intercept - m[0, 0]) < 1e-9 and abs(r.params.treatment - (m[1, 0] - m[0, 0])) < 1e-9
    assert abs(r.params.time - (m[0, 1] - m[0, 0])) < 1e-9
    # MHE Table 5.2.1 (Card-Krueger's own sample)
    check((21.03 - 20.44) - (21.17 - 23.33), 2.75, 2, "MHE table arithmetic")
    # flat-prior posterior P(beta4 > 0) under the normal approximation used on slide p. 25
    p = stats.norm.cdf(r.params.inter / r.bse.inter)
    check(p, 0.944, 3, "P(effect > 0)")
    print(f"6 DiD: cells PA {m[0, 0]:.3f}->{m[0, 1]:.3f}, NJ {m[1, 0]:.3f}->{m[1, 1]:.3f}; DiD {A - B:.4f} "
          f"(se {r.bse.inter:.3f}, t {r.tvalues.inter:.3f}); P(beta4>0) {p:.3f}")


# ============================================================================ 7 · regression discontinuity (L05-07)
def section7():
    d = pd.read_csv(DATA / "age-mva-internal.txt", sep=r"\s+")
    age = d.age.values
    out = {}
    for col in ("mva", "internal"):
        y = d[col].values
        j, se, s, n, b = mf.rdd_fit(age, y)
        jq, seq, sq, _, _ = mf.rdd_fit(age, y, p=2, inter=True)
        out[col] = (j, se, s, jq, seq, sq)
    j, se, s, jq, seq, sq = out["mva"]
    check(j, 4.534, 3, "MVA linear jump")
    check(j / s, 3.411, 3, "MVA stdevs (site legend)")
    check(jq / sq, 3.508, 3, "MVA quadratic stdevs")
    ji, sei, si, jqi, seqi, sqi = out["internal"]
    check(ji / si, 0.380, 3, "DIC stdevs")
    check(jqi / sqi, 1.026, 3, "DIC quadratic stdevs")
    # the slide p. 33 code divides the MVA jump by the DIC sigma for the linear DIC legend
    check(j / si, 4.394, 3, "slide's nsig1 = delta/sigma1 slip")
    # linear fit without interaction: jump = coefficient on over21 directly (D defined as age > 21)
    f = smf.ols("mva ~ age + over21", d.assign(over21=(d.age > 21).astype(int))).fit()
    assert abs(f.params.over21 - j) < 1e-10
    check(f.params.age, -3.149, 3, "MVA age slope")
    # local linear with separate slopes at a few bandwidths (note 07 table)
    ll = {b: mf.rdd_fit(age, d.mva.values, b=b, inter=True)[:2] for b in (0.5, 1.0, 2.0)}
    # placebo cutoffs (no rule changes there): linear with interactions on the side's own data
    plac = {a0: mf.rdd_fit(age, d.mva.values, a0=a0, b=1.0, inter=True)[:2] for a0 in (20.0, 22.0)}
    print(f"7 RDD: MVA linear {j:.3f} (se {se:.3f}, {j / s:.3f} sd), quadratic {jq:.3f} (se {seq:.3f}, {jq / sq:.3f} sd); "
          f"internal {ji:.3f} / {jqi:.3f}; local linear MVA b=0.5 {ll[0.5][0]:.3f}({ll[0.5][1]:.3f}), "
          f"b=1 {ll[1.0][0]:.3f}({ll[1.0][1]:.3f}), b=2 {ll[2.0][0]:.3f}({ll[2.0][1]:.3f}); "
          f"placebo a0=20 {plac[20.0][0]:.3f}({plac[20.0][1]:.3f}), a0=22 {plac[22.0][0]:.3f}({plac[22.0][1]:.3f})")
    return ll, plac


if __name__ == "__main__":
    section1()
    section2()
    section3()
    section4()
    section5()
    section6()
    section7()
    print("ALL L05 CHECKS PASSED")
