"""Reproduce and assert every number printed in Listas/lista-L02-book-exercises.tex.

Unit L02 (Class 2, introduction to statistical learning): ISLP 2.1-7.9 and 4.1-4.14,
Wooldridge 17.C1/C4/C5, Morettin & Singer 8.9/8.4/8.6/8.11.

Run from anywhere:  python Listas/L02-book-exercises-check.py
Data: Listas/data/*.csv|*.xls (provenance in Listas/data/README.md) and the `wooldridge`
package (pip install wooldridge). scikit-learn is not used: LDA, QDA, naive Bayes, KNN and
cross-validation are written with numpy/statsmodels below.
Fails with AssertionError naming the first printed number the code does not reproduce.
"""
from itertools import combinations
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.api as sm
from scipy import stats
from scipy.interpolate import BSpline

DATA = Path(__file__).resolve().parent / "data"
R = {}  # name -> computed value; compared with EXPECTED at the end


# ----------------------------------------------------------------------------- helpers
def folds(n, k, seed):
    """Fold label 0..k-1 for each of n observations: a random permutation cut into k equal parts."""
    return np.random.default_rng(seed).permutation(n) % k


def lda_fit(X, y, prior=None):
    """Two-class Gaussian LDA (pooled covariance, divisor n-2). prior=None uses class shares.

    Returns a function x -> P(Y=1|x). prior=(0.5, 0.5) gives Fisher's rule (8.18) of MS."""
    X0, X1 = X[y == 0], X[y == 1]
    m0, m1 = X0.mean(0), X1.mean(0)
    S = ((X0 - m0).T @ (X0 - m0) + (X1 - m1).T @ (X1 - m1)) / (len(y) - 2)
    p1 = y.mean() if prior is None else prior[1]
    Si = np.linalg.inv(np.atleast_2d(S))
    def post(Z):
        d1 = Z @ Si @ m1 - 0.5 * m1 @ Si @ m1 + np.log(p1)
        d0 = Z @ Si @ m0 - 0.5 * m0 @ Si @ m0 + np.log(1 - p1)
        return 1 / (1 + np.exp(d0 - d1))
    return post


def qda_fit(X, y, nb=False):
    """Two-class QDA (class covariances, divisor n_k-1); nb=True gives Gaussian naive Bayes
    (diagonal covariances, divisor n_k, as sklearn's GaussianNB)."""
    par = []
    for k in (0, 1):
        Xk = X[y == k]
        m = Xk.mean(0)
        S = np.diag(Xk.var(0, ddof=0)) if nb else np.atleast_2d(np.cov(Xk.T, ddof=1))
        par.append((m, np.linalg.inv(S), np.linalg.slogdet(S)[1], np.log(len(Xk) / len(y))))
    def post(Z):
        d = [-0.5 * np.einsum("ij,jk,ik->i", Z - m, Si, Z - m) - 0.5 * ld + lp for m, Si, ld, lp in par]
        return 1 / (1 + np.exp(d[0] - d[1]))
    return post


def logit_fit(X, y):
    # IRLS with a pseudo-inverse: stays defined when a CV fold makes two dummies collinear
    res = sm.GLM(y, sm.add_constant(X, has_constant="add"), family=sm.families.Binomial()).fit()
    return lambda Z: res.predict(sm.add_constant(Z, has_constant="add"))


def knn_pred(Xtr, ytr, Xte, K):
    """KNN vote with the K nearest training points; distance ties broken by training order
    (stable sort, as sklearn's brute-force search). Vote ties go to class 1 (>= 0.5)."""
    d = ((Xte[:, None, :] - Xtr[None, :, :]) ** 2).sum(-1)
    nn = np.argsort(d, axis=1, kind="stable")[:, :K]
    return (ytr[nn].mean(1) > 0.5).astype(int)


def confusion(pred, truth):
    """[[pred0&true0, pred0&true1], [pred1&true0, pred1&true1]] (rows = predicted)."""
    return np.array([[np.sum((pred == a) & (truth == b)) for b in (0, 1)] for a in (0, 1)])


def ols_rss(B, y):
    beta = np.linalg.lstsq(B, y, rcond=None)[0]
    return float(((y - B @ beta) ** 2).sum()), beta


def poly_basis(x, d, center, scale):
    z = (x - center) / scale
    return np.column_stack([z ** j for j in range(d + 1)])


def bs_basis(x, df, xall):
    """Cubic B-spline basis with df columns (no intercept column), interior knots at the
    quantiles of xall, boundary knots at its range: the construction of ISLP/patsy bs(df=)."""
    inner = np.quantile(xall, np.linspace(0, 1, df - 3 + 2)[1:-1])
    lo, hi = xall.min(), xall.max()
    t = np.r_[[lo] * 4, inner, [hi] * 4]
    B = BSpline.design_matrix(np.clip(x, lo, hi), t, 3).toarray()
    return np.column_stack([np.ones(len(x)), B[:, 1:]]), inner


def cv_mse(basis_fn, x, y, k, seed):
    f = folds(len(y), k, seed)
    err = 0.0
    for j in range(k):
        tr, te = f != j, f == j
        _, b = ols_rss(basis_fn(x[tr]), y[tr])
        err += ((y[te] - basis_fn(x[te]) @ b) ** 2).sum()
    return err / len(y)


def cv_accuracy(fit, X, y, k, seed, threshold=0.5):
    """k-fold CV predictions (P(Y=1|x) > threshold) and their accuracy."""
    f = folds(len(y), k, seed)
    pred = np.empty(len(y), dtype=int)
    for j in range(k):
        tr, te = f != j, f == j
        pred[te] = (fit(X[tr], y[tr])(X[te]) > threshold).astype(int)
    return pred, float((pred == y).mean())


def mcnemar(n12, n21):
    M = (n12 - n21) ** 2 / (n12 + n21)
    N = n12 + n21
    p_exact = min(1.0, 2 * stats.binom.cdf(min(n12, n21), N, 0.5))
    return M, stats.chi2.sf(M, 1), p_exact


# ----------------------------------------------------------------------------- ISLP 5.5
dflt = pd.read_csv(DATA / "Default.csv")
yD = (dflt["default"] == "Yes").astype(int).to_numpy()
XD = dflt[["income", "balance"]].to_numpy()
XDs = np.column_stack([XD, (dflt["student"] == "Yes").astype(int)])
full = sm.Logit(yD, sm.add_constant(XD)).fit(disp=0)
R["5.5a_b0"], R["5.5a_binc"], R["5.5a_bbal"] = full.params
R["5.5a_seinc"], R["5.5a_sebal"] = full.bse[1:]
R["5.5a_eta"] = full.params @ [1, 40000, 2000]
for s in (1, 2, 3, 4):
    idx = np.random.default_rng(s).permutation(len(yD))
    tr, va = idx[:5000], idx[5000:]
    for tag, X in (("", XD), ("stu", XDs)):
        p = logit_fit(X[tr], yD[tr])(X[va])
        err = float(((p > 0.5).astype(int) != yD[va]).mean())
        R[f"5.5_err{tag}_s{s}"] = err
        if s == 1 and tag == "":
            R["5.5b_nmis"] = int(round(err * 5000))
            R["5.5b_cm"] = confusion((p > 0.5).astype(int), yD[va])
R["5.5c_mean"] = np.mean([R[f"5.5_err_s{s}"] for s in (1, 2, 3, 4)])
R["5.5d_mean"] = np.mean([R[f"5.5_errstu_s{s}"] for s in (1, 2, 3, 4)])
R["5.5_null"] = yD.mean()

# ----------------------------------------------------------------------------- ISLP 5.8
rng = np.random.default_rng(1)
x58 = rng.normal(size=100)
y58 = x58 - 2 * x58 ** 2 + rng.normal(size=100)
R["5.8_xbar"], R["5.8_ybar"] = x58.mean(), y58.mean()
R["5.8_ymin"], R["5.8_ymax"] = y58.min(), y58.max()
for d in (1, 2, 3, 4):
    B = np.column_stack([x58 ** j for j in range(d + 1)])
    H = B @ np.linalg.solve(B.T @ B, B.T)
    res = y58 - H @ y58
    R[f"5.8_cv{d}"] = np.mean((res / (1 - np.diag(H))) ** 2)
    brute = np.mean([(y58[i] - B[i] @ ols_rss(np.delete(B, i, 0), np.delete(y58, i))[1]) ** 2
                     for i in range(100)])
    assert abs(brute - R[f"5.8_cv{d}"]) < 1e-10, "LOOCV shortcut (5.2) disagrees with brute force"
    fit = sm.OLS(y58, B).fit()
    for j in range(d + 1):
        R[f"5.8_b{d}{j}"], R[f"5.8_t{d}{j}"], R[f"5.8_p{d}{j}"] = fit.params[j], fit.tvalues[j], fit.pvalues[j]
    R[f"5.8_hmax{d}"] = np.diag(H).max()

# ----------------------------------------------------------------------------- ISLP 7.6
wage = pd.read_csv(DATA / "Wage.csv")
age, wg = wage["age"].to_numpy(float), wage["wage"].to_numpy()
ca, sa = age.mean(), age.std()
for d in range(1, 11):
    R[f"7.6_cv{d}"] = cv_mse(lambda a, d=d: poly_basis(a, d, ca, sa), age, wg, 10, 1)
R["7.6_dbest"] = min(range(1, 11), key=lambda d: R[f"7.6_cv{d}"])
rss = {d: ols_rss(poly_basis(age, d, ca, sa), wg)[0] for d in range(1, 6)}
s2 = rss[5] / (len(wg) - 6)
for d in range(1, 6):
    R[f"7.6_rss{d}"] = rss[d]
R["7.6_s2"] = s2
for s in (1, 2, 3, 4, 5):
    R[f"7.6_dbest_s{s}"] = min(range(1, 11), key=lambda d: cv_mse(lambda a, d=d: poly_basis(a, d, ca, sa), age, wg, 10, s))
for d in range(2, 6):
    R[f"7.6_F{d}"] = (rss[d - 1] - rss[d]) / s2
    R[f"7.6_pF{d}"] = stats.f.sf(R[f"7.6_F{d}"], 1, len(wg) - 6)
fit4 = sm.OLS(wg, np.column_stack([age ** j for j in range(5)])).fit()
grid76 = np.arange(18, 81, 4)
R["7.6_curve"] = np.column_stack([grid76 ** j for j in range(5)]) @ fit4.params
fine = np.linspace(18, 80, 6201)
R["7.6_peak_age"] = fine[np.argmax(np.column_stack([fine ** j for j in range(5)]) @ fit4.params)]
lo_a, hi_a = age.min(), age.max()
for c in range(2, 11):
    edges = np.linspace(lo_a, hi_a, c + 1)
    step = lambda a, e=edges: np.column_stack([np.ones(len(a))] + [((a > e[j]) & (a <= e[j + 1])).astype(float)
                                                                   for j in range(1, len(e) - 1)])
    R[f"7.6_cvstep{c}"] = cv_mse(step, age, wg, 10, 1)
R["7.6_cbest"] = min(range(2, 11), key=lambda c: R[f"7.6_cvstep{c}"])
edges = np.linspace(lo_a, hi_a, R["7.6_cbest"] + 1)
bins = np.clip(np.searchsorted(edges, age, side="left") - 1, 0, R["7.6_cbest"] - 1)
R["7.6_edges"] = edges
R["7.6_steplevels"] = np.array([wg[bins == j].mean() for j in range(R["7.6_cbest"])])

# ----------------------------------------------------------------------------- ISLP 7.9
bos = pd.read_csv(DATA / "Boston.csv")
dis, nox = bos["dis"].to_numpy(), bos["nox"].to_numpy()
fit3 = sm.OLS(nox, np.column_stack([dis ** j for j in range(4)])).fit()
for j in range(4):
    R[f"7.9a_b{j}"], R[f"7.9a_se{j}"], R[f"7.9a_p{j}"] = fit3.params[j], fit3.bse[j], fit3.pvalues[j]
R["7.9a_r2"], R["7.9a_rss"] = fit3.rsquared, fit3.ssr
cd_, sd_ = dis.mean(), dis.std()
for d in range(1, 11):
    R[f"7.9b_rss{d}"] = ols_rss(poly_basis(dis, d, cd_, sd_), nox)[0]
    R[f"7.9c_cv{d}"] = cv_mse(lambda a, d=d: poly_basis(a, d, cd_, sd_), dis, nox, 10, 1)
R["7.9c_dbest"] = min(range(1, 11), key=lambda d: R[f"7.9c_cv{d}"])
B4, knot4 = bs_basis(dis, 4, dis)
fit_bs = sm.OLS(nox, B4).fit()
R["7.9d_knot"] = knot4[0]
for j in range(5):
    R[f"7.9d_b{j}"], R[f"7.9d_se{j}"] = fit_bs.params[j], fit_bs.bse[j]
R["7.9d_rss"], R["7.9d_r2"] = fit_bs.ssr, fit_bs.rsquared
for df in range(3, 11):
    R[f"7.9e_rss{df}"] = ols_rss(bs_basis(dis, df, dis)[0], nox)[0]
    R[f"7.9f_cv{df}"] = cv_mse(lambda a, df=df: bs_basis(a, df, dis)[0], dis, nox, 10, 1)
R["7.9f_dfbest"] = min(range(3, 11), key=lambda df: R[f"7.9f_cv{df}"])
grid79 = np.arange(1.25, 12.25, 1.0)
R["7.9a_curve"] = np.column_stack([grid79 ** j for j in range(4)]) @ fit3.params
R["7.9d_curve"] = bs_basis(grid79, 4, dis)[0] @ fit_bs.params

# ----------------------------------------------------------------------------- ISLP 4.9 / 4.12
R["4.9a"] = 0.37 / 1.37
R["4.9b"] = 0.16 / 0.84
R["4.12e_agree"] = 1.0

# ----------------------------------------------------------------------------- ISLP 4.13
wk = pd.read_csv(DATA / "Weekly.csv")
yW = (wk["Direction"] == "Up").astype(int).to_numpy()
R["4.13a_n"], R["4.13a_up"] = len(wk), yW.mean()
R["4.13a_corr_year_vol"] = np.corrcoef(wk["Year"], wk["Volume"])[0, 1]
R["4.13a_vol90"] = wk.loc[wk.Year == 1990, "Volume"].mean()
R["4.13a_vol10"] = wk.loc[wk.Year == 2010, "Volume"].mean()
R["4.13a_maxlagcorr"] = np.abs(wk[["Lag1", "Lag2", "Lag3", "Lag4", "Lag5", "Today"]].corr().to_numpy()
                               - np.eye(6)).max()
cols = ["Lag1", "Lag2", "Lag3", "Lag4", "Lag5", "Volume"]
fb = sm.Logit(yW, sm.add_constant(wk[cols].to_numpy())).fit(disp=0)
for j, nm in enumerate(["const"] + cols):
    R[f"4.13b_b_{nm}"], R[f"4.13b_p_{nm}"] = fb.params[j], fb.pvalues[j]
cm = confusion((fb.predict() > 0.5).astype(int), yW)
R["4.13c_cm"], R["4.13c_acc"] = cm, np.trace(cm) / cm.sum()
R["4.13c_sens"], R["4.13c_spec"] = cm[1, 1] / cm[:, 1].sum(), cm[0, 0] / cm[:, 0].sum()
trW, teW = (wk.Year <= 2008).to_numpy(), (wk.Year > 2008).to_numpy()


def held_out(fitter, cols_, K=None, transform=None):
    X = wk[cols_].to_numpy(float) if transform is None else transform(wk)
    if K is not None:
        pred = knn_pred(X[trW], yW[trW], X[teW], K)
    else:
        pred = (fitter(X[trW], yW[trW])(X[teW]) > 0.5).astype(int)
    c = confusion(pred, yW[teW])
    return c, np.trace(c) / c.sum()


R["4.13_ntest"], R["4.13_uptest"] = int(teW.sum()), yW[teW].mean()
for tag, f in (("d", logit_fit), ("e", lda_fit), ("f", qda_fit), ("h", lambda X, y: qda_fit(X, y, nb=True))):
    R[f"4.13{tag}_cm"], R[f"4.13{tag}_acc"] = held_out(f, ["Lag2"])
R["4.13g_cm"], R["4.13g_acc"] = held_out(None, ["Lag2"], K=1)
lg = sm.Logit(yW[trW], sm.add_constant(wk.loc[trW, "Lag2"].to_numpy())).fit(disp=0)
R["4.13d_b0"], R["4.13d_b1"], R["4.13d_p1"] = lg.params[0], lg.params[1], lg.pvalues[1]
l2 = wk["Lag2"].to_numpy()
R["4.13e_mu0"], R["4.13e_mu1"] = l2[trW & (yW == 0)].mean(), l2[trW & (yW == 1)].mean()
R["4.13e_pi1"] = yW[trW].mean()
x0_, x1_ = l2[trW & (yW == 0)], l2[trW & (yW == 1)]
R["4.13e_s2"] = (((x0_ - x0_.mean()) ** 2).sum() + ((x1_ - x1_.mean()) ** 2).sum()) / (trW.sum() - 2)
R["4.13e_logpi"] = np.log(R["4.13e_pi1"] / (1 - R["4.13e_pi1"]))
R["4.13e_thr"] = (R["4.13e_mu0"] + R["4.13e_mu1"]) / 2 - R["4.13e_s2"] * R["4.13e_logpi"] / (R["4.13e_mu1"] - R["4.13e_mu0"])
R["4.13d_thr"] = -R["4.13d_b0"] / R["4.13d_b1"]
R["4.13f_v0"], R["4.13f_v1"] = x0_.var(ddof=1), x1_.var(ddof=1)
R["4.13j_se"] = np.sqrt(0.625 * 0.375 / 104)
for K in (1, 3, 5, 10, 20, 50, 100, 150):
    R[f"4.13j_knn{K}"] = held_out(None, ["Lag2"], K=K)[1]
sets = {"Lag1+Lag2": ["Lag1", "Lag2"], "Lag2+Lag2sq": None, "Lag1..Lag5+Volume": cols}
sq = lambda d: np.column_stack([d["Lag2"], d["Lag2"] ** 2])
for nm, cs in sets.items():
    tf = sq if cs is None else None
    for tag, f in (("logit", logit_fit), ("lda", lda_fit), ("qda", qda_fit)):
        R[f"4.13j_{tag}_{nm}"] = held_out(f, cs or ["Lag2"], transform=tf)[1]
R["4.13j_best_knn_K"] = max((1, 3, 5, 10, 20, 50, 100, 150), key=lambda K: R[f"4.13j_knn{K}"])

# ----------------------------------------------------------------------------- ISLP 4.14
auto = pd.read_csv(DATA / "Auto.csv")
R["4.14a_median"] = auto["mpg"].median()
yA = (auto["mpg"] > R["4.14a_median"]).astype(int).to_numpy()
R["4.14a_n"], R["4.14a_n1"] = len(yA), int(yA.sum())
feats = ["cylinders", "displacement", "horsepower", "weight", "acceleration", "year", "origin"]
for c in feats:
    R[f"4.14b_corr_{c}"] = np.corrcoef(auto[c], yA)[0, 1]
    R[f"4.14b_m0_{c}"], R[f"4.14b_m1_{c}"] = auto.loc[yA == 0, c].mean(), auto.loc[yA == 1, c].mean()
use = ["cylinders", "displacement", "horsepower", "weight"]
XA = auto[use].to_numpy(float)
idx = np.random.default_rng(1).permutation(len(yA))
trA, teA = idx[:196], idx[196:]
R["4.14c_n1train"] = int(yA[trA].sum())
for tag, f in (("d", lda_fit), ("e", qda_fit), ("f", logit_fit), ("g", lambda X, y: qda_fit(X, y, nb=True))):
    p = (f(XA[trA], yA[trA])(XA[teA]) > 0.5).astype(int)
    R[f"4.14{tag}_err"] = float((p != yA[teA]).mean())
    R[f"4.14{tag}_nerr"] = int((p != yA[teA]).sum())
mu, sd = XA[trA].mean(0), XA[trA].std(0)
Zs = (XA - mu) / sd
for K in (1, 3, 5, 10, 20, 50, 100):
    p = knn_pred(Zs[trA], yA[trA], Zs[teA], K)
    R[f"4.14h_err{K}"] = float((p != yA[teA]).mean())

# ----------------------------------------------------------------------------- Wooldridge
import wooldridge as wd

ps = wd.data("pntsprd")
Xp = sm.add_constant(ps[["spread"]])
o = sm.OLS(ps["favwin"], Xp).fit()
orob = sm.OLS(ps["favwin"], Xp).fit(cov_type="HC1")
R["C1_n"] = len(ps)
R["C1_b0"], R["C1_b1"] = o.params
R["C1_se0"], R["C1_se1"] = o.bse
R["C1_rse0"], R["C1_rse1"] = orob.bse
R["C1_t0"] = (o.params.iloc[0] - 0.5) / o.bse.iloc[0]
R["C1_rt0"] = (o.params.iloc[0] - 0.5) / orob.bse.iloc[0]
R["C1_pt0"] = 2 * stats.t.sf(abs(R["C1_t0"]), len(ps) - 2)
R["C1_prt0"] = 2 * stats.norm.sf(abs(R["C1_rt0"]))
R["C1_t1"], R["C1_rt1"] = o.tvalues.iloc[1], orob.tvalues.iloc[1]
R["C1_r2"] = o.rsquared
R["C1_lpm10"] = o.params.iloc[0] + 10 * o.params.iloc[1]
pr = sm.Probit(ps["favwin"], Xp).fit(disp=0)
R["C1_pb0"], R["C1_pb1"] = pr.params
R["C1_pse0"], R["C1_pse1"] = pr.bse
R["C1_pz0"], R["C1_pp0"] = pr.tvalues.iloc[0], pr.pvalues.iloc[0]
R["C1_pz1"] = pr.tvalues.iloc[1]
R["C1_pidx10"] = pr.params.iloc[0] + 10 * pr.params.iloc[1]
R["C1_pr10"] = stats.norm.cdf(R["C1_pidx10"])
pr2 = sm.Probit(ps["favwin"], sm.add_constant(ps[["spread", "favhome", "fav25", "und25"]])).fit(disp=0)
R["C1_llr"], R["C1_llu"] = pr.llf, pr2.llf
R["C1_LR"] = 2 * (pr2.llf - pr.llf)
R["C1_pLR"] = stats.chi2.sf(R["C1_LR"], 3)
for nm in ("favhome", "fav25", "und25"):
    R[f"C1_u_{nm}"], R[f"C1_up_{nm}"] = pr2.params[nm], pr2.pvalues[nm]

cr = wd.data("crime1")
base = ["pcnv", "avgsen", "tottime", "ptime86", "qemp86", "inc86", "black", "hispan", "born60"]
quad = ["pcnvsq", "pt86sq", "inc86sq"]
pois = sm.families.Poisson()
pr_r = sm.GLM(cr["narr86"], sm.add_constant(cr[base]), family=pois).fit()
pr_u = sm.GLM(cr["narr86"], sm.add_constant(cr[base + quad]), family=pois).fit()
R["C4_llr"], R["C4_llu"] = pr_r.llf, pr_u.llf  # full log-likelihood; llr matches Table 17.5
for nm in quad + ["pcnv", "ptime86", "inc86"]:
    R[f"C4_b_{nm}"], R[f"C4_se_{nm}"] = pr_u.params[nm], pr_u.bse[nm]
yh = pr_u.predict()
n, k = len(cr), len(base + quad)
R["C4_sum"] = np.sum((cr["narr86"] - yh) ** 2 / yh)
R["C4_s2"] = R["C4_sum"] / (n - k - 1)
R["C4_s"] = np.sqrt(R["C4_s2"])
R["C4_params"], R["C4_bse"] = pr_u.params.to_numpy(), pr_u.bse.to_numpy()
R["C4_bse_adj"] = R["C4_s"] * R["C4_bse"]
yhr = pr_r.predict()
R["C4_s_restricted"] = np.sqrt(np.sum((cr["narr86"] - yhr) ** 2 / yhr) / (n - 9 - 1))
R["C4_LR"] = 2 * (pr_u.llf - pr_r.llf)
R["C4_QLR"] = R["C4_LR"] / R["C4_s2"]
R["C4_pQLR"] = stats.chi2.sf(R["C4_QLR"], 3)
R["C4_crit5"] = stats.chi2.ppf(0.95, 3)
for nm in ("pcnv", "ptime86", "inc86"):
    R[f"C4_tp_{nm}"] = -pr_u.params[nm] / (2 * pr_u.params[{"pcnv": "pcnvsq", "ptime86": "pt86sq",
                                                             "inc86": "inc86sq"}[nm]])

fe = wd.data("fertil1")
v13 = ["educ", "age", "agesq", "black", "east", "northcen", "west", "farm", "othrural", "town",
       "smcity", "y74", "y76", "y78", "y80", "y82", "y84"]
po = sm.GLM(fe["kids"], sm.add_constant(fe[v13]), family=sm.families.Poisson()).fit()
ol = sm.OLS(fe["kids"], sm.add_constant(fe[v13])).fit()
R["C5_n"] = len(fe)
for nm in ("y82", "y84", "black", "educ"):
    R[f"C5_b_{nm}"], R[f"C5_se_{nm}"] = po.params[nm], po.bse[nm]
R["C5_pct_y82"] = 100 * (np.exp(po.params["y82"]) - 1)
R["C5_pct_black"] = 100 * (np.exp(po.params["black"]) - 1)
R["C5_ols_y82"], R["C5_ybar"] = ol.params["y82"], fe["kids"].mean()
yhk = po.predict()
R["C5_params"], R["C5_bse"] = po.params.to_numpy(), po.bse.to_numpy()
R["C5_sum"] = np.sum((fe["kids"] - yhk) ** 2 / yhk)
R["C5_s2"] = R["C5_sum"] / (len(fe) - len(v13) - 1)
R["C5_s"] = np.sqrt(R["C5_s2"])
R["C5_r2pois"] = np.corrcoef(fe["kids"], yhk)[0, 1] ** 2
R["C5_r2ols"] = ol.rsquared
R["C5_meanfit"] = yhk.mean()

# ----------------------------------------------------------------------------- Morettin & Singer
disco = pd.read_excel(DATA / "disco.xls", sheet_name="dados")
xd, yd = disco["distanciaA"].to_numpy(), disco["deslocamento"].to_numpy()
R["MS9_n"], R["MS9_n1"] = len(yd), int(yd.sum())


def knn_loocv_ties(x, y, K):
    """LOOCV KNN in one dimension, R class::knn style: every point tied with the K-th
    distance votes; an exactly split vote is assigned to class 0 (the majority class)."""
    pred = np.empty(len(y), dtype=int)
    for i in range(len(y)):
        d = np.abs(np.delete(x, i) - x[i])
        yy = np.delete(y, i)
        dk = np.sort(d)[K - 1]
        share = yy[d <= dk + 1e-12].mean()
        pred[i] = int(share > 0.5)
    return pred


for K in range(1, 6):
    p = knn_loocv_ties(xd, yd, K)
    R[f"MS9_acc{K}"] = float((p == yd).mean())
R["MS9_Kbest"] = max(range(1, 6), key=lambda K: (R[f"MS9_acc{K}"], -K))
pbest = knn_loocv_ties(xd, yd, R["MS9_Kbest"])
c9 = confusion(pbest, yd)  # rows predicted 0/1, columns true 0/1
R["MS9_cm"] = c9
# Book layout (Tabela 8.2): n11 = pred sim & true sim, n12 = pred sim & true nao, n21 = pred nao & true sim
n11, n12, n21, n22 = c9[1, 1], c9[1, 0], c9[0, 1], c9[0, 0]
R["MS9_M"], R["MS9_pM"], R["MS9_pexact"] = mcnemar(n12, n21)
R["MS9_sens"], R["MS9_spec"] = n11 / (n11 + n21), n22 / (n12 + n22)

ini = pd.read_excel(DATA / "inibina.xls", sheet_name="dados")
yi = (ini["resposta"] == "positiva").astype(int).to_numpy()
Xi = ini[["inibpre", "inibpos"]].to_numpy(float)
R["MS4_n"], R["MS4_n1"] = len(yi), int(yi.sum())
R["MS4_resub"] = float(((lda_fit(Xi, yi)(Xi) > 0.5).astype(int) == yi).mean())
R["MS4_resub_difinib"] = float(((lda_fit((Xi[:, 1] - Xi[:, 0])[:, None], yi)((Xi[:, 1] - Xi[:, 0])[:, None])
                                  > 0.5).astype(int) == yi).mean())
ks, seeds = (2, 4, 8, 16, 32), (1, 2, 3, 4, 5)
for kk in ks:
    for s in seeds:
        R[f"MS4_acc_k{kk}_s{s}"] = cv_accuracy(lda_fit, Xi, yi, kk, s)[1]
    vals = [R[f"MS4_acc_k{kk}_s{s}"] for s in seeds]
    R[f"MS4_mean_k{kk}"], R[f"MS4_range_k{kk}"] = np.mean(vals), max(vals) - min(vals)

end = pd.read_excel(DATA / "endometriose2.xls", sheet_name="dados")
R["MS6_nraw"] = len(end)
end = end.dropna(subset=["idade", "dismenorreia"])
end = end[end["tipoesteril"] != "sim"].reset_index(drop=True)
R["MS6_n"], R["MS6_n1"] = len(end), int((end["endometriose"] == "sim").sum())
ye = (end["endometriose"] == "sim").astype(int).to_numpy()
blocks = {
    "idade": end[["idade"]].to_numpy(float),
    "dormenstrual": (end[["dormenstrual"]] == "sim").to_numpy(float),
    "dismenorreia": pd.get_dummies(end["dismenorreia"])[["leve", "moderada", "intensa", "incapacitante"]]
    .to_numpy(float),
    "tipoesteril": pd.get_dummies(end["tipoesteril"])[["primaria", "secundaria"]].to_numpy(float),
}
names = list(blocks)
R["MS6_null"] = 1 - ye.mean()
models = [c for r in range(1, 5) for c in combinations(names, r)]
for m in models:
    X = np.column_stack([blocks[b] for b in m])
    key = "+".join(m)
    R[f"MS6_acc_{key}"] = cv_accuracy(logit_fit, X, ye, 5, 1)[1]
    R[f"MS6_rep_{key}"] = np.mean([cv_accuracy(logit_fit, X, ye, 5, s)[1] for s in (1, 2, 3, 4, 5)])
R["MS6_best"] = max(models, key=lambda m: R["MS6_acc_" + "+".join(m)])
R["MS6_best_rep"] = max(models, key=lambda m: R["MS6_rep_" + "+".join(m)])
Xall = np.column_stack([blocks[b] for b in names])
fl = sm.Logit(ye, sm.add_constant(np.column_stack([blocks["dismenorreia"], blocks["tipoesteril"]]))).fit(disp=0)
R["MS6_best_params"], R["MS6_best_p"] = fl.params, fl.pvalues
R["MS6_eta_mod_prim"] = fl.params[0] + fl.params[2] + fl.params[5]
R["MS6_eta_mod_nao"] = fl.params[0] + fl.params[2]
R["MS6_cells_pos"] = int(((fl.predict() > 0.5)).sum())

clfs = {"logit": logit_fit, "bayes": lda_fit, "fisher": lambda X, y: lda_fit(X, y, prior=(0.5, 0.5))}
preds = {}
for nm, f in clfs.items():
    accs, sens, spec = [], [], []
    for s in (1, 2, 3, 4, 5):
        p, a = cv_accuracy(f, Xall, ye, 5, s)
        if s == 1:
            preds[nm] = p
        accs.append(a)
        sens.append(np.mean(p[ye == 1] == 1))
        spec.append(np.mean(p[ye == 0] == 0))
    R[f"MS11_acc_{nm}"], R[f"MS11_sens_{nm}"], R[f"MS11_spec_{nm}"] = np.mean(accs), np.mean(sens), np.mean(spec)
for a, b in (("logit", "bayes"), ("logit", "fisher"), ("bayes", "fisher")):
    ca_, cb_ = preds[a] == ye, preds[b] == ye
    n12_, n21_ = int(np.sum(ca_ & ~cb_)), int(np.sum(~ca_ & cb_))
    R[f"MS11_n12_{a}_{b}"], R[f"MS11_n21_{a}_{b}"] = n12_, n21_
    if n12_ + n21_ > 0:
        R[f"MS11_M_{a}_{b}"], R[f"MS11_pM_{a}_{b}"], R[f"MS11_pex_{a}_{b}"] = mcnemar(n12_, n21_)
R["MS11_agree_logit_bayes"] = float(np.mean(preds["logit"] == preds["bayes"]))


# ----------------------------------------------------------------------------- values printed rescaled
R["5.5a_binc_e5"], R["5.5a_bbal_e3"] = 1e5 * R["5.5a_binc"], 1e3 * R["5.5a_bbal"]
R["5.5a_seinc_e6"], R["5.5a_sebal_e4"] = 1e6 * R["5.5a_seinc"], 1e4 * R["5.5a_sebal"]
R["5.5a_z"] = full.tvalues[1:]
R["5.5a_or100"] = np.exp(100 * R["5.5a_bbal"])
for j, v in enumerate(fit4.params):
    R[f"7.6_fit4_{j}"] = v
for d in range(1, 11):
    R[f"7.9c_cv{d}_e3"] = 1e3 * R[f"7.9c_cv{d}"]
for df in range(3, 11):
    R[f"7.9f_cv{df}_e3"] = 1e3 * R[f"7.9f_cv{df}"]
R["C4_inc86sq_e5"] = 1e5 * np.array([R["C4_params"][12], R["C4_bse"][12], R["C4_bse_adj"][12]])
R["C5_exp_y82"], R["C5_exp_black"] = np.exp(R["C5_b_y82"]), np.exp(R["C5_b_black"])
for kk in ks:
    R[f"MS4_cnt_k{kk}"] = np.array([32 * R[f"MS4_acc_k{kk}_s{s}"] for s in seeds])
    R[f"MS4_rangecnt_k{kk}"] = 32 * R[f"MS4_range_k{kk}"]
R["7.6_agemeans"] = wage.groupby("age")["wage"].mean().to_numpy()


# ----------------------------------------------------------------------------- report / assert
def show():
    for k_, v in R.items():
        if isinstance(v, np.ndarray):
            print(k_, "=", np.array2string(np.asarray(v, dtype=float), precision=6, max_line_width=200))
        elif isinstance(v, (float, np.floating)):
            print(k_, "=", f"{v:.6f}")
        else:
            print(k_, "=", v)


# Printed value and number of decimals shown in the .tex; a computed value must round to it.
EXPECTED = {
    '5.5a_b0': (-11.5405, 4),
    '5.5a_binc_e5': (2.0809, 4),
    '5.5a_bbal_e3': (5.6471, 4),
    '5.5a_or100': (1.7589, 4),
    '5.5c_mean': (0.027, 4),
    '5.5d_mean': (0.0273, 4),
    '5.5_null': (0.0333, 4),
    '5.5a_seinc_e6': (4.985, 3),
    '5.5a_sebal_e4': (2.274, 3),
    '5.5a_z': ([4.17, 24.84], 2),
    '5.5b_cm': ([[4813.0, 110.0], [22.0, 55.0]], 0),
    '5.5b_nmis': (132.0, 0),
    '5.5_err_s1': (0.0264, 4),
    '5.5_err_s2': (0.0256, 4),
    '5.5_err_s3': (0.0296, 4),
    '5.5_err_s4': (0.0264, 4),
    '5.5_errstu_s1': (0.027, 4),
    '5.5_errstu_s2': (0.0264, 4),
    '5.5_errstu_s3': (0.0294, 4),
    '5.5_errstu_s4': (0.0264, 4),
    '5.8_ymin': (-14.864, 3),
    '5.8_ymax': (2.097, 3),
    '5.8_hmax4': (0.836, 3),
    '5.8_cv1': (6.633, 4),
    '5.8_cv2': (1.1229, 4),
    '5.8_cv3': (1.3018, 4),
    '5.8_cv4': (1.3324, 4),
    '5.8_t10': (-5.94, 2),
    '5.8_t11': (6.75, 2),
    '5.8_p10': (0.0, 3),
    '5.8_p11': (0.0, 3),
    '5.8_t20': (-0.61, 2),
    '5.8_t21': (7.65, 2),
    '5.8_t22': (-22.07, 2),
    '5.8_p20': (0.543, 3),
    '5.8_p21': (0.0, 3),
    '5.8_p22': (0.0, 3),
    '5.8_t30': (-0.48, 2),
    '5.8_t31': (5.95, 2),
    '5.8_t32': (-20.67, 2),
    '5.8_t33': (-1.07, 2),
    '5.8_p30': (0.635, 3),
    '5.8_p31': (0.0, 3),
    '5.8_p32': (0.0, 3),
    '5.8_p33': (0.287, 3),
    '5.8_t40': (0.74, 2),
    '5.8_t41': (4.42, 2),
    '5.8_t42': (-11.34, 2),
    '5.8_t43': (0.47, 2),
    '5.8_t44': (2.31, 2),
    '5.8_p40': (0.46, 3),
    '5.8_p41': (0.0, 3),
    '5.8_p42': (0.0, 3),
    '5.8_p43': (0.642, 3),
    '5.8_p44': (0.023, 3),
    '7.6_cv1': (1675.48, 2),
    '7.6_cv2': (1599.65, 2),
    '7.6_cv3': (1594.81, 2),
    '7.6_cv4': (1593.32, 2),
    '7.6_cv5': (1593.23, 2),
    '7.6_cv6': (1592.32, 2),
    '7.6_cv7': (1592.06, 2),
    '7.6_cv8': (1592.7, 2),
    '7.6_cv9': (1590.97, 2),
    '7.6_cv10': (1592.11, 2),
    '7.6_rss1': (5022216.1, 2),
    '7.6_rss2': (4793430.09, 2),
    '7.6_rss3': (4777674.4, 2),
    '7.6_rss4': (4771604.25, 2),
    '7.6_rss5': (4770321.69, 2),
    '7.6_s2': (1593.29, 2),
    '7.6_F2': (143.59, 2),
    '7.6_peak_age': (48.35, 2),
    '7.6_dbest': (9.0, 0),
    '7.6_cbest': (8.0, 0),
    '7.6_dbest_s1': (9.0, 0),
    '7.6_dbest_s2': (6.0, 0),
    '7.6_dbest_s3': (9.0, 0),
    '7.6_dbest_s4': (9.0, 0),
    '7.6_dbest_s5': (9.0, 0),
    '7.6_F3': (9.889, 3),
    '7.6_F4': (3.81, 3),
    '7.6_F5': (0.805, 3),
    '7.6_pF3': (0.0017, 4),
    '7.6_pF4': (0.051, 4),
    '7.6_pF5': (0.3697, 4),
    '7.6_fit4_0': (-184.154, 3),
    '7.6_fit4_1': (21.2455, 4),
    '7.6_fit4_2': (-0.563859, 6),
    '7.6_fit4_3': (0.00681069, 8),
    '7.6_fit4_4': (-3.20383e-05, 10),
    '7.6_cvstep2': (1733.16, 2),
    '7.6_cvstep3': (1681.8, 2),
    '7.6_cvstep4': (1634.27, 2),
    '7.6_cvstep5': (1629.82, 2),
    '7.6_cvstep6': (1621.38, 2),
    '7.6_cvstep7': (1609.87, 2),
    '7.6_cvstep8': (1599.57, 2),
    '7.6_cvstep9': (1607.75, 2),
    '7.6_cvstep10': (1602.75, 2),
    '7.6_edges': ([18.0, 25.75, 33.5, 41.25, 49.0, 56.75, 64.5, 72.25, 80.0], 2),
    '7.6_steplevels': ([76.28, 102.12, 116.51, 119.78, 116.42, 120.38, 105.23, 91.51], 2),
    '7.6_curve': ([51.93, 75.35, 92.12, 103.68, 111.25, 115.87, 118.41, 119.49, 119.57, 118.9, 117.55, 115.36, 112.01, 106.95, 99.46, 88.6], 2),
    '7.6_agemeans': ([64.5, 54.0, 69.0, 75.9, 72.3, 74.7, 85.7, 85.5, 98.7, 93.7, 98.7, 100.1, 106.5, 104.4, 101.2, 108.1, 111.0, 111.4, 117.2, 110.2, 132.2, 116.1, 117.3, 115.2, 117.8, 125.2, 116.0, 122.5, 123.1, 119.2, 114.4, 120.1, 112.7, 120.0, 108.4, 122.8, 119.2, 117.4, 115.9, 123.2, 115.2, 125.4, 119.4, 124.1, 116.9, 127.6, 102.7, 95.8, 119.3, 112.7, 101.0, 92.5, 90.8, 99.5, 123.4, 83.6, 106.2, 69.4, 109.2, 99.7, 86.1], 1),
    '7.9a_b0': (0.9341, 4),
    '7.9a_b1': (-0.1821, 4),
    '7.9a_se0': (0.0207, 4),
    '7.9a_se1': (0.0147, 4),
    '7.9a_r2': (0.7148, 4),
    '7.9a_rss': (1.9341, 4),
    '7.9d_knot': (3.2074, 4),
    '7.9d_rss': (1.9228, 4),
    '7.9d_r2': (0.7164, 4),
    '7.9a_curve': ([0.7391, 0.6254, 0.5436, 0.4884, 0.4545, 0.4366, 0.4294, 0.4275, 0.4256, 0.4185, 0.4008], 4),
    '7.9d_curve': ([0.7242, 0.631, 0.5438, 0.4844, 0.4507, 0.4357, 0.4321, 0.433, 0.4311, 0.4193, 0.3905], 4),
    '7.9d_b0': (0.7345, 4),
    '7.9d_b1': (-0.0581, 4),
    '7.9d_b2': (-0.4636, 4),
    '7.9d_b3': (-0.1998, 4),
    '7.9d_b4': (-0.3888, 4),
    '7.9d_se0': (0.0146, 4),
    '7.9d_se1': (0.0219, 4),
    '7.9d_se2': (0.0237, 4),
    '7.9d_se3': (0.0431, 4),
    '7.9d_se4': (0.0455, 4),
    '7.9b_rss1': (2.7686, 4),
    '7.9b_rss2': (2.0353, 4),
    '7.9b_rss3': (1.9341, 4),
    '7.9b_rss4': (1.933, 4),
    '7.9b_rss5': (1.9153, 4),
    '7.9b_rss6': (1.8783, 4),
    '7.9b_rss7': (1.8495, 4),
    '7.9b_rss8': (1.8356, 4),
    '7.9b_rss9': (1.8333, 4),
    '7.9b_rss10': (1.8322, 4),
    '7.9e_rss3': (1.9341, 4),
    '7.9e_rss4': (1.9228, 4),
    '7.9e_rss5': (1.8402, 4),
    '7.9e_rss6': (1.834, 4),
    '7.9e_rss7': (1.8299, 4),
    '7.9e_rss8': (1.817, 4),
    '7.9e_rss9': (1.8257, 4),
    '7.9e_rss10': (1.7925, 4),
    '7.9a_b2': (0.02193, 5),
    '7.9a_se2': (0.00293, 5),
    '7.9a_b3': (-0.000885, 6),
    '7.9a_se3': (0.000173, 6),
    '7.9c_cv1_e3': (5.526, 3),
    '7.9c_cv2_e3': (4.065, 3),
    '7.9c_cv3_e3': (3.852, 3),
    '7.9c_cv4_e3': (3.867, 3),
    '7.9c_cv5_e3': (4.184, 3),
    '7.9c_cv6_e3': (5.811, 3),
    '7.9c_cv7_e3': (8.736, 3),
    '7.9c_cv8_e3': (8.281, 3),
    '7.9c_cv9_e3': (12.092, 3),
    '7.9c_cv10_e3': (3.987, 3),
    '7.9f_cv3_e3': (3.852, 3),
    '7.9f_cv4_e3': (3.875, 3),
    '7.9f_cv5_e3': (3.688, 3),
    '7.9f_cv6_e3': (3.687, 3),
    '7.9f_cv7_e3': (3.7, 3),
    '7.9f_cv8_e3': (3.69, 3),
    '7.9f_cv9_e3': (3.715, 3),
    '7.9f_cv10_e3': (3.695, 3),
    '7.9c_dbest': (3.0, 0),
    '7.9f_dfbest': (6.0, 0),
    '4.9a': (0.2701, 4),
    '4.9b': (0.1905, 4),
    '4.13a_n': (1089.0, 0),
    '4.13_ntest': (104.0, 0),
    '4.13c_cm': ([[54.0, 48.0], [430.0, 557.0]], 0),
    '4.13d_cm': ([[9.0, 5.0], [34.0, 56.0]], 0),
    '4.13e_cm': ([[9.0, 5.0], [34.0, 56.0]], 0),
    '4.13f_cm': ([[0.0, 0.0], [43.0, 61.0]], 0),
    '4.13g_cm': ([[22.0, 31.0], [21.0, 30.0]], 0),
    '4.13h_cm': ([[0.0, 0.0], [43.0, 61.0]], 0),
    '4.13a_up': (0.5556, 4),
    '4.13a_corr_year_vol': (0.8419, 4),
    '4.13a_vol90': (0.1548, 4),
    '4.13a_vol10': (4.5578, 4),
    '4.13a_maxlagcorr': (0.0757, 4),
    '4.13c_acc': (0.5611, 4),
    '4.13c_sens': (0.9207, 4),
    '4.13c_spec': (0.1116, 4),
    '4.13d_thr': (-3.4987, 4),
    '4.13e_thr': (-3.5265, 4),
    '4.13f_v0': (4.8378, 4),
    '4.13f_v1': (5.3707, 4),
    '4.13j_se': (0.0475, 4),
    '4.13d_acc': (0.625, 4),
    '4.13e_acc': (0.625, 4),
    '4.13f_acc': (0.5865, 4),
    '4.13g_acc': (0.5, 4),
    '4.13h_acc': (0.5865, 4),
    '4.13b_b_const': (0.2669, 4),
    '4.13b_b_Lag1': (-0.0413, 4),
    '4.13b_b_Lag2': (0.0584, 4),
    '4.13b_b_Lag3': (-0.0161, 4),
    '4.13b_b_Lag4': (-0.0278, 4),
    '4.13b_b_Lag5': (-0.0145, 4),
    '4.13b_b_Volume': (-0.0227, 4),
    '4.13b_p_const': (0.0019, 4),
    '4.13b_p_Lag1': (0.1181, 4),
    '4.13b_p_Lag2': (0.0296, 4),
    '4.13b_p_Lag3': (0.5469, 4),
    '4.13b_p_Lag4': (0.2937, 4),
    '4.13b_p_Lag5': (0.5833, 4),
    '4.13b_p_Volume': (0.5377, 4),
    '4.13d_b0': (0.203257, 6),
    '4.13d_b1': (0.058095, 6),
    '4.13e_mu0': (-0.035683, 6),
    '4.13e_mu1': (0.260366, 6),
    '4.13e_pi1': (0.552284, 6),
    '4.13e_s2': (5.132198, 6),
    '4.13e_logpi': (0.209904, 6),
    '4.13d_p1': (0.043, 3),
    '4.13j_knn1': (0.5, 4),
    '4.13j_knn3': (0.5577, 4),
    '4.13j_knn5': (0.5385, 4),
    '4.13j_knn10': (0.5673, 4),
    '4.13j_knn20': (0.5962, 4),
    '4.13j_knn50': (0.5577, 4),
    '4.13j_knn100': (0.5673, 4),
    '4.13j_knn150': (0.625, 4),
    '4.13j_logit_Lag1+Lag2': (0.5769, 4),
    '4.13j_logit_Lag2+Lag2sq': (0.625, 4),
    '4.13j_logit_Lag1..Lag5+Volume': (0.4615, 4),
    '4.13j_lda_Lag1+Lag2': (0.5769, 4),
    '4.13j_lda_Lag2+Lag2sq': (0.6154, 4),
    '4.13j_lda_Lag1..Lag5+Volume': (0.4615, 4),
    '4.13j_qda_Lag1+Lag2': (0.5577, 4),
    '4.13j_qda_Lag2+Lag2sq': (0.625, 4),
    '4.13j_qda_Lag1..Lag5+Volume': (0.4327, 4),
    '4.14a_median': (22.75, 2),
    '4.14b_m0_cylinders': (6.77, 2),
    '4.14b_m0_displacement': (273.16, 2),
    '4.14b_m0_horsepower': (130.11, 2),
    '4.14b_m0_weight': (3620.4, 2),
    '4.14b_m0_acceleration': (14.59, 2),
    '4.14b_m0_year': (74.4, 2),
    '4.14b_m0_origin': (1.16, 2),
    '4.14b_m1_cylinders': (4.18, 2),
    '4.14b_m1_displacement': (115.67, 2),
    '4.14b_m1_horsepower': (78.83, 2),
    '4.14b_m1_weight': (2334.77, 2),
    '4.14b_m1_acceleration': (16.5, 2),
    '4.14b_m1_year': (77.56, 2),
    '4.14b_m1_origin': (1.99, 2),
    '4.14b_corr_cylinders': (-0.759, 3),
    '4.14b_corr_displacement': (-0.753, 3),
    '4.14b_corr_horsepower': (-0.667, 3),
    '4.14b_corr_weight': (-0.758, 3),
    '4.14b_corr_acceleration': (0.347, 3),
    '4.14b_corr_year': (0.43, 3),
    '4.14b_corr_origin': (0.514, 3),
    '4.14a_n': (392.0, 0),
    '4.14a_n1': (196.0, 0),
    '4.14c_n1train': (94.0, 0),
    '4.14d_nerr': (24.0, 0),
    '4.14e_nerr': (22.0, 0),
    '4.14f_nerr': (25.0, 0),
    '4.14g_nerr': (23.0, 0),
    '4.14d_err': (0.1224, 4),
    '4.14e_err': (0.1122, 4),
    '4.14f_err': (0.1276, 4),
    '4.14g_err': (0.1173, 4),
    '4.14h_err1': (0.1122, 4),
    '4.14h_err3': (0.102, 4),
    '4.14h_err5': (0.102, 4),
    '4.14h_err10': (0.1173, 4),
    '4.14h_err20': (0.1173, 4),
    '4.14h_err50': (0.1224, 4),
    '4.14h_err100': (0.1071, 4),
    'C1_n': (553.0, 0),
    'C1_b0': (0.576949, 6),
    'C1_se0': (0.028235, 6),
    'C1_rse0': (0.031657, 6),
    'C1_pb0': (-0.010593, 6),
    'C1_pb1': (0.092463, 6),
    'C1_pse0': (0.103747, 6),
    'C1_pidx10': (0.914037, 6),
    'C1_b1': (0.0193655, 7),
    'C1_se1': (0.0023, 4),
    'C1_rse1': (0.0019, 4),
    'C1_t0': (2.7254, 4),
    'C1_rt0': (2.4307, 4),
    'C1_pt0': (0.0066, 4),
    'C1_prt0': (0.0151, 4),
    'C1_r2': (0.1107, 4),
    'C1_lpm10': (0.7706, 4),
    'C1_pse1': (0.0122, 4),
    'C1_pz0': (-0.1021, 4),
    'C1_pr10': (0.8197, 4),
    'C1_llr': (-263.5622, 4),
    'C1_llu': (-262.6418, 4),
    'C1_LR': (1.8408, 4),
    'C1_t1': (8.28, 2),
    'C1_rt1': (10.08, 2),
    'C1_pp0': (0.919, 3),
    'C1_pLR': (0.606, 3),
    'C1_up_favhome': (0.278, 3),
    'C1_up_fav25': (0.985, 3),
    'C1_up_und25': (0.38, 3),
    'C4_params': ([-0.7099, 1.1531, -0.0256, 0.0122, 0.6837, 0.023, -0.0121, 0.5914, 0.422, -0.0929, -1.7951, -0.1034, 0.0], 4),
    'C4_bse': ([0.0702, 0.2823, 0.0215, 0.0158, 0.0912, 0.0327, 0.0018, 0.0744, 0.0748, 0.0642, 0.3072, 0.0162, 0.0], 4),
    'C4_bse_adj': ([0.0828, 0.3329, 0.0253, 0.0186, 0.1076, 0.0386, 0.0022, 0.0877, 0.0883, 0.0758, 0.3623, 0.0191, 0.0], 4),
    'C4_s2': (1.3912, 4),
    'C4_s': (1.1795, 4),
    'C4_s_restricted': (1.2316, 4),
    'C4_tp_pcnv': (0.3212, 4),
    'C4_tp_ptime86': (3.3047, 4),
    'C4_inc86sq_e5': ([2.068, 0.614, 0.724], 3),
    'C4_llu': (-2168.866, 3),
    'C4_llr': (-2248.761, 3),
    'C4_sum': (3772.81, 2),
    'C4_LR': (159.79, 2),
    'C4_QLR': (114.86, 2),
    'C4_crit5': (7.81, 2),
    'C4_tp_inc86': (292.0, 0),
    'C5_params': ([-3.0605, -0.0482, 0.2045, -0.0022, 0.3603, 0.0878, 0.1417, 0.0795, -0.0148, -0.0573, 0.0307, 0.0741, 0.0933, -0.0288, -0.0157, -0.0197, -0.1926, -0.2144], 4),
    'C5_bse': ([1.2107, 0.0072, 0.0548, 0.0006, 0.0611, 0.0527, 0.0475, 0.0657, 0.0576, 0.0692, 0.0486, 0.0615, 0.0631, 0.0676, 0.0687, 0.069, 0.0675, 0.0695], 4),
    'C5_s2': (0.8915, 4),
    'C5_s': (0.9442, 4),
    'C5_r2pois': (0.1209, 4),
    'C5_r2ols': (0.1295, 4),
    'C5_pct_y82': (-17.52, 2),
    'C5_pct_black': (43.38, 2),
    'C5_sum': (990.43, 2),
    'C5_ols_y82': (-0.522, 3),
    'C5_ybar': (2.743, 3),
    'C5_exp_y82': (0.824806, 6),
    'C5_exp_black': (1.433828, 6),
    'C5_n': (1129.0, 0),
    'MS9_n': (104.0, 0),
    'MS9_n1': (29.0, 0),
    'MS9_Kbest': (4.0, 0),
    'MS9_cm': ([[73.0, 14.0], [2.0, 15.0]], 0),
    'MS9_acc1': (0.8173, 4),
    'MS9_acc2': (0.8173, 4),
    'MS9_acc3': (0.7885, 4),
    'MS9_acc4': (0.8462, 4),
    'MS9_acc5': (0.8077, 4),
    'MS9_pM': (0.0027, 4),
    'MS9_pexact': (0.0042, 4),
    'MS9_sens': (0.5172, 4),
    'MS9_spec': (0.9733, 4),
    'MS9_M': (9.0, 2),
    'MS4_n': (32.0, 0),
    'MS4_n1': (19.0, 0),
    'MS4_cnt_k2': ([25.0, 21.0, 24.0, 19.0, 22.0], 0),
    'MS4_cnt_k4': ([25.0, 24.0, 21.0, 22.0, 22.0], 0),
    'MS4_cnt_k8': ([24.0, 23.0, 23.0, 24.0, 22.0], 0),
    'MS4_cnt_k16': ([24.0, 21.0, 23.0, 22.0, 22.0], 0),
    'MS4_cnt_k32': ([22.0, 22.0, 22.0, 22.0, 22.0], 0),
    'MS4_rangecnt_k2': (6.0, 0),
    'MS4_rangecnt_k4': (4.0, 0),
    'MS4_rangecnt_k8': (2.0, 0),
    'MS4_rangecnt_k16': (3.0, 0),
    'MS4_rangecnt_k32': (0.0, 0),
    'MS4_resub': (0.78125, 5),
    'MS4_mean_k2': (0.69375, 5),
    'MS4_mean_k4': (0.7125, 5),
    'MS4_mean_k8': (0.725, 5),
    'MS4_mean_k16': (0.7, 5),
    'MS4_mean_k32': (0.6875, 5),
    'MS4_resub_difinib': (0.8125, 4),
    'MS6_nraw': (1872.0, 0),
    'MS6_n': (1866.0, 0),
    'MS6_n1': (492.0, 0),
    'MS6_cells_pos': (132.0, 0),
    'MS6_null': (0.7363, 4),
    'MS6_best_params': ([-2.4112, 0.2264, 2.1984, 2.1561, 1.5647, 1.3996, -0.0655], 4),
    'MS6_eta_mod_prim': (1.1868, 4),
    'MS6_eta_mod_nao': (-0.2128, 4),
    'MS6_acc_idade': (0.7363, 4),
    'MS6_rep_idade': (0.7363, 4),
    'MS6_acc_dormenstrual': (0.7363, 4),
    'MS6_rep_dormenstrual': (0.7363, 4),
    'MS6_acc_dismenorreia': (0.7358, 4),
    'MS6_rep_dismenorreia': (0.7277, 4),
    'MS6_acc_tipoesteril': (0.7497, 4),
    'MS6_rep_tipoesteril': (0.7497, 4),
    'MS6_acc_idade+dormenstrual': (0.7363, 4),
    'MS6_rep_idade+dormenstrual': (0.7363, 4),
    'MS6_acc_idade+dismenorreia': (0.7476, 4),
    'MS6_rep_idade+dismenorreia': (0.7447, 4),
    'MS6_acc_idade+tipoesteril': (0.746, 4),
    'MS6_rep_idade+tipoesteril': (0.7468, 4),
    'MS6_acc_dormenstrual+dismenorreia': (0.7353, 4),
    'MS6_rep_dormenstrual+dismenorreia': (0.7273, 4),
    'MS6_acc_dormenstrual+tipoesteril': (0.7588, 4),
    'MS6_rep_dormenstrual+tipoesteril': (0.7588, 4),
    'MS6_acc_dismenorreia+tipoesteril': (0.7685, 4),
    'MS6_rep_dismenorreia+tipoesteril': (0.7685, 4),
    'MS6_acc_idade+dormenstrual+dismenorreia': (0.7481, 4),
    'MS6_rep_idade+dormenstrual+dismenorreia': (0.7448, 4),
    'MS6_acc_idade+dormenstrual+tipoesteril': (0.7588, 4),
    'MS6_rep_idade+dormenstrual+tipoesteril': (0.7588, 4),
    'MS6_acc_idade+dismenorreia+tipoesteril': (0.7503, 4),
    'MS6_rep_idade+dismenorreia+tipoesteril': (0.7559, 4),
    'MS6_acc_dormenstrual+dismenorreia+tipoesteril': (0.768, 4),
    'MS6_rep_dormenstrual+dismenorreia+tipoesteril': (0.7681, 4),
    'MS6_acc_idade+dormenstrual+dismenorreia+tipoesteril': (0.7503, 4),
    'MS6_rep_idade+dormenstrual+dismenorreia+tipoesteril': (0.755, 4),
    'MS11_acc_logit': (0.755, 4),
    'MS11_acc_bayes': (0.7534, 4),
    'MS11_acc_fisher': (0.698, 4),
    'MS11_sens_logit': (0.2337, 4),
    'MS11_sens_bayes': (0.2854, 4),
    'MS11_sens_fisher': (0.7646, 4),
    'MS11_spec_logit': (0.9416, 4),
    'MS11_spec_bayes': (0.921, 4),
    'MS11_spec_fisher': (0.6741, 4),
    'MS11_n12_logit_bayes': (19.0, 0),
    'MS11_n21_logit_bayes': (28.0, 0),
    'MS11_n12_logit_fisher': (365.0, 0),
    'MS11_n21_logit_fisher': (270.0, 0),
    'MS11_n12_bayes_fisher': (346.0, 0),
    'MS11_n21_bayes_fisher': (242.0, 0),
    'MS11_M_logit_bayes': (1.7234, 4),
    'MS11_M_logit_fisher': (14.2126, 4),
    'MS11_M_bayes_fisher': (18.3946, 4),
    'MS11_pM_logit_bayes': (0.189, 3),
    'MS11_agree_logit_bayes': (0.975, 3),
    'MS11_pM_logit_fisher': (0.00016, 5),
    'MS11_pM_bayes_fisher': (1.8e-05, 6),
}

if __name__ == "__main__":
    if not EXPECTED:
        show()
    else:
        bad = 0
        for k_, (val, dec) in EXPECTED.items():
            got = np.asarray(R[k_], dtype=float)
            ok = np.all(np.abs(got - np.asarray(val, dtype=float)) <= 0.5 * 10.0 ** (-dec) + 1e-9)
            if not ok:
                print(f"MISMATCH {k_}: printed {val}, computed {got}")
                bad += 1
        assert bad == 0, f"{bad} printed numbers not reproduced"
        print(f"PASS: {len(EXPECTED)} printed numbers reproduced")
