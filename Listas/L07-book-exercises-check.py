"""Reproduce and assert every number printed in Listas/lista-L07-book-exercises.tex.

Unit L07 (Class 7): GLS with AR(1) errors, Student-t errors, hierarchical/panel models,
Tobit, probit/logit, logistic odds ratios. Run from any directory:

    python Listas/L07-book-exercises-check.py

Data: Wooldridge data sets from the `wooldridge` package (pip install wooldridge);
StatLabs "Birth weight II" in Listas/data/babies.data (provenance in Listas/data/README.md).
Every MCMC run uses a fixed seed; MCMC numbers are asserted with a Monte Carlo tolerance,
everything else to the rounding printed in the list. Exits non-zero on the first mismatch.
"""
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.api as sm
import wooldridge as wd
from linearmodels.panel import PanelOLS
from scipy import optimize, stats
from scipy.special import gammaln
from statsmodels.tools.numdiff import approx_hess

HERE = Path(__file__).resolve().parent
OUT = {}


def put(key, value):
    OUT[key] = float(value)


# ---------------------------------------------------------------- shared tools
def fgls_ar1(y, X, prais_winsten, tol=1e-10, maxit=500):
    """Iterated Cochrane-Orcutt (prais_winsten=False) or Prais-Winsten FGLS for AR(1) errors.

    y: (n,) response; X: (n,k) regressors including the constant column.
    rho is the no-intercept regression of u_t on u_{t-1} (W eq. 12.14), recomputed from the
    original-scale residuals after every FGLS step until it moves by less than `tol`.
    Returns (statsmodels OLS result on the quasi-differenced data, final rho, iterations).
    """
    b = np.linalg.lstsq(X, y, rcond=None)[0]
    rho = 0.0
    for it in range(1, maxit + 1):
        u = y - X @ b
        rho_new = (u[1:] @ u[:-1]) / (u[:-1] @ u[:-1])
        ys, Xs = y[1:] - rho_new * y[:-1], X[1:] - rho_new * X[:-1]
        if prais_winsten:
            c = np.sqrt(1 - rho_new**2)
            ys, Xs = np.r_[c * y[0], ys], np.vstack([c * X[0], Xs])
        res = sm.OLS(ys, Xs).fit()
        b = res.params
        if abs(rho_new - rho) < tol:
            return res, rho_new, it
        rho = rho_new
    raise RuntimeError("FGLS did not converge")


def tobit(y, X):
    """Type I Tobit (left-censored at 0) by ML. Returns (beta, sigma, cov of (beta, sigma), loglik).

    Optimised in (beta, log sigma); the covariance is the inverse numerical Hessian in
    (beta, sigma), i.e. the usual ML standard errors reported by Stata/R for sigma itself.
    """
    def ll(theta):
        b, s = theta[:-1], theta[-1]
        xb = X @ b
        return np.where(y <= 0, stats.norm.logcdf(-xb / s),
                        stats.norm.logpdf((y - xb) / s) - np.log(s)).sum()

    b0 = np.linalg.lstsq(X, y, rcond=None)[0]
    s0 = np.std(y - X @ b0)
    f = lambda t: -ll(np.r_[t[:-1], np.exp(t[-1])])
    r = optimize.minimize(f, np.r_[b0, np.log(s0)], method="BFGS",
                          options={"gtol": 1e-8, "maxiter": 10000})
    r = optimize.minimize(f, r.x, method="Nelder-Mead",
                          options={"xatol": 1e-10, "fatol": 1e-12, "maxiter": 20000}) \
        if not r.success else r
    theta = np.r_[r.x[:-1], np.exp(r.x[-1])]
    cov = np.linalg.inv(-approx_hess(theta, ll))
    return theta[:-1], theta[-1], cov, ll(theta)


def tobit_mean(X, b, s):
    """E(y|x) = Phi(xb/s) xb + s phi(xb/s), W eq. (17.25)."""
    xb = X @ b
    return stats.norm.cdf(xb / s) * xb + s * stats.norm.pdf(xb / s)


# ---------------------------------------------------------------- W 12.C2
def w12c2():
    d = wd.data("wageprc")
    lags = ["gwage"] + [f"gwage_{j}" for j in range(1, 13)]
    d = d[["gprice"] + lags].dropna()
    y, X = d.gprice.to_numpy(), sm.add_constant(d[lags]).to_numpy()
    ols = sm.OLS(y, X).fit()
    u = ols.resid
    t14 = sm.OLS(u[1:], sm.add_constant(u[:-1])).fit()
    put("c2_n", len(y))
    put("c2_ols_lrp", ols.params[1:].sum())
    put("c2_rho_test", t14.params[1]); put("c2_rho_se", t14.bse[1]); put("c2_rho_t", t14.tvalues[1])
    co, rho, it = fgls_ar1(y, X, prais_winsten=False)
    R = np.r_[0, np.ones(13)]
    lrp = R @ co.params
    se = np.sqrt(R @ co.cov_params() @ R)
    put("c2_co_rho", rho); put("c2_co_lrp", lrp); put("c2_co_lrp_se", se)
    put("c2_co_t1", (lrp - 1) / se); put("c2_co_df", co.df_resid)
    put("c2_co_crit", stats.t.ppf(0.975, co.df_resid))
    # modified (reparametrised) equation: coefficient on gwage is the LRP theta
    Z = X.copy()
    Z[:, 2:] = X[:, 2:] - X[:, [1]]
    co2, rho2, _ = fgls_ar1(y, Z, prais_winsten=False)
    assert abs(co2.params[1] - lrp) < 1e-8 and abs(co2.bse[1] - se) < 1e-8 and abs(rho2 - rho) < 1e-8
    for j in range(13):
        put(f"c2_co_d{j}", co.params[1 + j])
    put("c2_co_a0", co.params[0])


# ---------------------------------------------------------------- W 12.C10
def w12c10():
    d = wd.data("phillips")
    y, X = d.inf.to_numpy(), sm.add_constant(d.unem).to_numpy()
    ols = sm.OLS(y, X).fit()
    put("c10_n", len(y)); put("c10_ols_b0", ols.params[0]); put("c10_ols_b1", ols.params[1])
    put("c10_ols_se0", ols.bse[0]); put("c10_ols_se1", ols.bse[1]); put("c10_ols_r2", ols.rsquared)
    put("c10_ols_t1", ols.tvalues[1])
    u = ols.resid
    t14 = sm.OLS(u[1:], sm.add_constant(u[:-1])).fit()
    put("c10_rho", t14.params[1]); put("c10_rho_se", t14.bse[1]); put("c10_rho_t", t14.tvalues[1])
    pw, rpw, _ = fgls_ar1(y, X, prais_winsten=True)
    co, rco, _ = fgls_ar1(y, X, prais_winsten=False)
    put("c10_pw_b0", pw.params[0]); put("c10_pw_b1", pw.params[1]); put("c10_pw_se1", pw.bse[1])
    put("c10_pw_se0", pw.bse[0]); put("c10_pw_rho", rpw)
    put("c10_co_b0", co.params[0]); put("c10_co_b1", co.params[1]); put("c10_co_se1", co.bse[1])
    put("c10_co_rho", rco)
    # through 1996, to reproduce Table 12.2 (sanity check of the FGLS routine)
    e = d[d.year <= 1996]
    pw96, r96, _ = fgls_ar1(e.inf.to_numpy(), sm.add_constant(e.unem).to_numpy(), True)
    put("c10_pw96_b1", pw96.params[1]); put("c10_pw96_rho", r96)


# ---------------------------------------------------------------- W 17.C2
def w17c2():
    d = wd.data("loanapp")
    full = ["white", "hrat", "obrat", "loanprc", "unem", "male", "married", "dep", "sch",
            "cosign", "chist", "pubrec", "mortlat1", "mortlat2", "vr"]
    d1 = d[["approve", "white"]].dropna()
    pr1 = sm.Probit(d1.approve, sm.add_constant(d1.white)).fit(disp=0)
    lpm = sm.OLS(d1.approve, sm.add_constant(d1.white)).fit()
    put("c17_2_n1", len(d1))
    put("c17_2_p_b0", pr1.params.iloc[0]); put("c17_2_p_b1", pr1.params.iloc[1])
    put("c17_2_p_se1", pr1.bse.iloc[1])
    put("c17_2_pw", stats.norm.cdf(pr1.params.sum())); put("c17_2_pnw", stats.norm.cdf(pr1.params.iloc[0]))
    put("c17_2_lpm_b0", lpm.params.iloc[0]); put("c17_2_lpm_b1", lpm.params.iloc[1])
    d2 = d[["approve"] + full].dropna()
    X2 = sm.add_constant(d2[full])
    pr2 = sm.Probit(d2.approve, X2).fit(disp=0)
    lg2 = sm.Logit(d2.approve, X2).fit(disp=0)
    put("c17_2_n2", len(d2))
    put("c17_2_p2_w", pr2.params["white"]); put("c17_2_p2_wse", pr2.bse["white"])
    put("c17_2_p2_wt", pr2.tvalues["white"])
    put("c17_2_l2_w", lg2.params["white"]); put("c17_2_l2_wse", lg2.bse["white"])
    put("c17_2_l2_wt", lg2.tvalues["white"])
    put("c17_2_ratio", lg2.params["white"] / pr2.params["white"])
    for name, m, G in (("p", pr2, stats.norm.cdf), ("l", lg2, stats.logistic.cdf)):
        X1, X0 = X2.copy(), X2.copy()
        X1["white"], X0["white"] = 1, 0
        put(f"c17_2_ape_{name}", np.mean(G(X1 @ m.params) - G(X0 @ m.params)))
    lpm2 = sm.OLS(d2.approve, X2).fit()
    put("c17_2_lpm2_w", lpm2.params["white"])


# ---------------------------------------------------------------- W 17.C3
def w17c3():
    d = wd.data("fringe")
    y = d.pension.to_numpy()
    put("c17_3_n", len(y)); put("c17_3_zero_pct", 100 * np.mean(y == 0))
    put("c17_3_nzero", np.sum(y == 0))
    put("c17_3_min_pos", y[y > 0].min()); put("c17_3_max", y.max())
    xs = ["exper", "age", "tenure", "educ", "depends", "married", "white", "male"]
    X = sm.add_constant(d[xs]).to_numpy()
    b, s, V, ll = tobit(y, X)
    se = np.sqrt(np.diag(V))
    for j, n in enumerate(["const"] + xs):
        put(f"c17_3_b_{n}", b[j]); put(f"c17_3_se_{n}", se[j])
    put("c17_3_sigma", s); put("c17_3_sigma_se", se[-1]); put("c17_3_ll", ll)
    # (iii) white male vs nonwhite female; age 35, single, no dependents, educ 16, exper 10,
    # tenure 10 (tenure is not given in the statement: assumption stated in the solution)
    base = dict(const=1, exper=10, age=35, tenure=10, educ=16, depends=0, married=0)
    xwm = np.array([base.get(n, 0) for n in ["const"] + xs], float); xwm[-2:] = 1
    xnf = np.array([base.get(n, 0) for n in ["const"] + xs], float)
    for tag, x in (("wm", xwm), ("nf", xnf)):
        put(f"c17_3_xb_{tag}", x @ b); put(f"c17_3_z_{tag}", x @ b / s)
        put(f"c17_3_Phi_{tag}", stats.norm.cdf(x @ b / s)); put(f"c17_3_phi_{tag}", stats.norm.pdf(x @ b / s))
        put(f"c17_3_E_{tag}", tobit_mean(x[None, :], b, s)[0])
        put(f"c17_3_A_{tag}", stats.norm.cdf(x @ b / s) * (x @ b)); put(f"c17_3_B_{tag}", s * stats.norm.pdf(x @ b / s))
    put("c17_3_diff", OUT["c17_3_E_wm"] - OUT["c17_3_E_nf"])
    put("c17_3_xbdiff", OUT["c17_3_xb_wm"] - OUT["c17_3_xb_nf"])
    put("c17_3_t_white", b[7] / se[7]); put("c17_3_t_male", b[8] / se[8])
    Xu = sm.add_constant(d[xs + ["union"]]).to_numpy()
    bu, su, Vu, llu = tobit(y, Xu)
    put("c17_3_union", bu[-1]); put("c17_3_union_se", np.sqrt(Vu[-2, -2]))
    put("c17_3_union_t", bu[-1] / np.sqrt(Vu[-2, -2]))
    yr = d.peratio.to_numpy()
    br, sr, Vr, llr = tobit(yr, Xu)
    ser = np.sqrt(np.diag(Vr))
    put("c17_3_pe_white", br[7]); put("c17_3_pe_white_se", ser[7])
    put("c17_3_pe_male", br[8]); put("c17_3_pe_male_se", ser[8])
    put("c17_3_pe_union", br[9]); put("c17_3_pe_union_se", ser[9]); put("c17_3_pe_sigma", sr)
    put("c17_3_pe_white_t", br[7] / ser[7]); put("c17_3_pe_male_t", br[8] / ser[8])
    put("c17_3_pe_zero", np.sum(yr == 0)); put("c17_3_pe_max", yr.max())


# ---------------------------------------------------------------- W 17.C9
def w17c9():
    d = wd.data("apple")
    y = d.ecolbs.to_numpy()
    put("c17_9_n", len(y)); put("c17_9_nzero", np.sum(y == 0))
    pos = y[y > 0]
    vc = pd.Series(pos).value_counts()
    put("c17_9_npos", len(pos)); put("c17_9_ndistinct", pos.size and vc.size)
    put("c17_9_n1", vc.get(1.0, 0)); put("c17_9_n2", vc.get(2.0, 0)); put("c17_9_n3", vc.get(3.0, 0))
    put("c17_9_n5", vc.get(5.0, 0)); put("c17_9_n43", vc.iloc[3]); put("c17_9_v43", vc.index[3])
    put("c17_9_top_share", vc.iloc[:5].sum() / len(pos))
    xs = ["ecoprc", "regprc", "faminc", "hhsize"]
    X = sm.add_constant(d[xs]).to_numpy()
    b, s, V, ll = tobit(y, X)
    se = np.sqrt(np.diag(V))
    for j, n in enumerate(["const"] + xs):
        put(f"c17_9_b_{n}", b[j]); put(f"c17_9_se_{n}", se[j]); put(f"c17_9_t_{n}", b[j] / se[j])
    put("c17_9_sigma", s); put("c17_9_sigma_se", se[-1]); put("c17_9_ll", ll)
    br, sr, Vr, llr = tobit(y, X[:, :3])
    put("c17_9_ll_r", llr); put("c17_9_LR", 2 * (ll - llr)); put("c17_9_LR_p", stats.chi2.sf(2 * (ll - llr), 2))
    Rw = np.zeros((2, 6)); Rw[0, 3] = Rw[1, 4] = 1
    W = (Rw @ np.r_[b, s]) @ np.linalg.solve(Rw @ V @ Rw.T, Rw @ np.r_[b, s])
    put("c17_9_W", W); put("c17_9_W_p", stats.chi2.sf(W, 2))
    g = np.array([0, 1, 1, 0, 0, 0.0])  # H0: -beta1 = beta2  <=>  beta1 + beta2 = 0
    th = g @ np.r_[b, s]; th_se = np.sqrt(g @ V @ g)
    put("c17_9_theta", th); put("c17_9_theta_se", th_se); put("c17_9_theta_t", th / th_se)
    put("c17_9_theta_p", 2 * stats.norm.sf(abs(th / th_se)))
    m = tobit_mean(X, b, s)
    put("c17_9_Emin", m.min()); put("c17_9_Emax", m.max())
    put("c17_9_r2_tobit", np.corrcoef(y, m)[0, 1] ** 2)
    ols = sm.OLS(y, X).fit()
    for j, n in enumerate(["const"] + xs):
        put(f"c17_9_ols_{n}", ols.params[j]); put(f"c17_9_olsse_{n}", ols.bse[j])
    put("c17_9_r2_ols", ols.rsquared)
    # scale factor: average of Phi(x b / s) (APE of a continuous x_j on E(y|x) = beta_j * this)
    put("c17_9_scale", stats.norm.cdf(X @ b / s).mean())
    put("c17_9_sc_eco", b[1] * OUT["c17_9_scale"]); put("c17_9_sc_reg", b[2] * OUT["c17_9_scale"])


# ---------------------------------------------------------------- W 14.C5
def w14c5():
    d = wd.data("wagepan").set_index(["nr", "year"])
    yrs = [f"d8{j}" for j in range(1, 8)]
    occ = [f"occ{j}" for j in range(2, 10)]
    base = ["expersq", "married", "union"] + yrs
    fe0 = PanelOLS(d.lwage, d[base], entity_effects=True).fit()
    fe1 = PanelOLS(d.lwage, d[base + occ], entity_effects=True).fit()
    fe1c = PanelOLS(d.lwage, d[base + occ], entity_effects=True).fit(cov_type="clustered", cluster_entity=True)
    put("c14_5_u0", fe0.params["union"]); put("c14_5_u0_se", fe0.std_errors["union"])
    put("c14_5_m0", fe0.params["married"]); put("c14_5_m0_se", fe0.std_errors["married"])
    put("c14_5_u1", fe1.params["union"]); put("c14_5_u1_se", fe1.std_errors["union"])
    put("c14_5_u1_t", fe1.tstats["union"]); put("c14_5_u1_cse", fe1c.std_errors["union"])
    put("c14_5_m1", fe1.params["married"]); put("c14_5_m1_se", fe1.std_errors["married"])
    put("c14_5_e1", fe1.params["expersq"])
    # joint test of the eight occupation dummies (usual, non-robust Wald / F)
    b = fe1.params[occ].to_numpy(); V = fe1.cov.loc[occ, occ].to_numpy()
    F = b @ np.linalg.solve(V, b) / len(occ)
    put("c14_5_F", F); put("c14_5_F_p", stats.f.sf(F, len(occ), fe1.df_resid))
    put("c14_5_occ_switch", (d.groupby(level=0)[[f"occ{j}" for j in range(1, 10)]].std().sum(axis=1) > 0).mean())
    put("c14_5_N", d.index.get_level_values(0).nunique()); put("c14_5_nobs", len(d))


# ---------------------------------------------------------------- MS 6.18 and 6.21
def ms618():
    a, b, g = 0.69, 0.33, -0.03
    sb, sg = 0.10, 0.005
    z = stats.norm.ppf(0.975)
    put("ms18_odds_girl5", np.exp(a)); put("ms18_p_girl5", np.exp(a) / (1 + np.exp(a)))
    put("ms18_or_b", np.exp(b)); put("ms18_or_g", np.exp(g)); put("ms18_or_g5", np.exp(5 * g))
    put("ms18_or_10v15", np.exp(g * (10 - 15)))
    put("ms18_lb", b - 1.96 * sb); put("ms18_ub", b + 1.96 * sb)
    put("ms18_lg", g - 1.96 * sg); put("ms18_ug", g + 1.96 * sg)
    for k in ("lb", "ub", "lg", "ug"):
        put(f"ms18_e{k}", np.exp(OUT[f"ms18_{k}"]))
    eta = a + b * 1 + g * (15 - 5)
    put("ms18_eta", eta); put("ms18_odds15", np.exp(eta)); put("ms18_p15", np.exp(eta) / (1 + np.exp(eta)))
    assert abs(z - 1.96) < 1e-3


def ms621():
    mid = np.array([1, 4, 7, 10, 13, 16, 19, 22.0])
    yes = np.array([17, 26, 39, 27, 35, 37, 26, 23])
    no = np.array([215, 218, 137, 62, 36, 16, 13, 15])
    X = sm.add_constant(mid)
    m = sm.GLM(np.c_[yes, no], X, family=sm.families.Binomial()).fit()
    put("ms21_a", m.params[0]); put("ms21_b", m.params[1])
    put("ms21_sa", m.bse[0]); put("ms21_sb", m.bse[1]); put("ms21_zb", m.tvalues[1])
    put("ms21_or1", np.exp(m.params[1])); put("ms21_or5", np.exp(5 * m.params[1]))
    put("ms21_lb", m.params[1] - 1.96 * m.bse[1]); put("ms21_ub", m.params[1] + 1.96 * m.bse[1])
    put("ms21_elb", np.exp(OUT["ms21_lb"])); put("ms21_eub", np.exp(OUT["ms21_ub"]))
    put("ms21_dev", m.deviance); put("ms21_dev_p", stats.chi2.sf(m.deviance, 6))
    put("ms21_pearson", m.pearson_chi2)
    put("ms21_null_dev", m.null_deviance)
    put("ms21_LR", m.null_deviance - m.deviance)
    for x in (1, 22):
        e = m.params[0] + m.params[1] * x
        put(f"ms21_eta{x}", e); put(f"ms21_p{x}", 1 / (1 + np.exp(-e)))
    put("ms21_obs1", yes[0] / (yes[0] + no[0])); put("ms21_obs22", yes[-1] / (yes[-1] + no[-1]))
    put("ms21_n", (yes + no).sum())


# ---------------------------------------------------------------- Greenberg 8.1/8.3 (birth weight)
def log_ig(x, a, d):
    """log density of IG(a, d) in Greenberg's (shape, scale) form: d^a/Gamma(a) x^-(a+1) e^{-d/x}."""
    return a * np.log(d) - gammaln(a) - (a + 1) * np.log(x) - d / x


def log_mvn(x, m, S):
    L = np.linalg.cholesky(S)
    z = np.linalg.solve(L, x - m)
    return -0.5 * len(x) * np.log(2 * np.pi) - np.log(np.diag(L)).sum() - 0.5 * z @ z


def gibbs_reg(y, X, b0, B0, a0, d0, nu, G, burn, rng, beta_fixed=None):
    """Gibbs sampler for y = X beta + u, u_i ~ N(0, sigma2/lambda_i), lambda_i ~ G(nu/2, nu/2).

    nu=None gives Gaussian errors (lambda_i = 1). Priors beta ~ N(b0, B0), sigma2 ~ IG(a0/2, d0/2)
    (Greenberg eqs. 8.1 and 8.4). With beta_fixed the beta step is skipped (Chib reduced run).
    Returns draws of beta (G,K), sigma2 (G,), and the list of (beta_bar, B1) for Rao-Blackwell use.
    """
    n, K = X.shape
    B0i = np.linalg.inv(B0)
    beta = np.linalg.lstsq(X, y, rcond=None)[0] if beta_fixed is None else beta_fixed.copy()
    s2 = np.var(y - X @ beta)
    lam = np.ones(n)
    keep_b, keep_s, keep_rb = np.empty((G, K)), np.empty(G), []
    for g in range(G + burn):
        if beta_fixed is None:
            XL = X * lam[:, None]
            B1 = np.linalg.inv(XL.T @ X / s2 + B0i)
            bb = B1 @ (XL.T @ y / s2 + B0i @ b0)
            beta = rng.multivariate_normal(bb, B1)
        e = y - X @ beta
        s2 = 1 / rng.gamma((a0 + n) / 2, 2 / (d0 + (lam * e) @ e))
        if nu is not None:
            lam = rng.gamma((nu + 1) / 2, 2 / (nu + e**2 / s2))
        if g >= burn:
            i = g - burn
            keep_b[i], keep_s[i] = beta, s2
            if beta_fixed is None:
                keep_rb.append((lam.copy(), s2))
            else:
                keep_rb.append((a0 + n, d0 + (lam * e) @ e))
    return keep_b, keep_s, keep_rb


def g83():
    d = pd.read_csv(HERE / "data" / "babies.data", sep=r"\s+")
    ok = (d.gestation != 999) & (d.age != 99) & (d.height != 99) & (d.weight != 999) & (d.smoke != 9)
    d = d[ok]
    xs = ["gestation", "parity", "age", "height", "weight", "smoke"]
    y, X = d.bwt.to_numpy(float), sm.add_constant(d[xs]).to_numpy(float)
    n, K = X.shape
    put("g83_n", n)
    b0 = np.zeros(K)
    B0 = np.diag([100.0**2] + [10.0**2] * (K - 1))
    a0, d0 = 6.0, 1024.0  # prior E(sigma2) = d0/(a0-2) = 256 (prior sd of u about 16 oz)
    ols = sm.OLS(y, X).fit()
    put("g83_ols_smoke", ols.params[-1]); put("g83_ols_smoke_se", ols.bse[-1])
    put("g83_kurt", stats.kurtosis(ols.resid))
    G, burn = 10000, 1000
    res = {}
    for tag, nu in (("n", None), ("t", 5.0)):
        rng = np.random.default_rng(830 if nu is None else 835)
        bd, sd_, rb = gibbs_reg(y, X, b0, B0, a0, d0, nu, G, burn, rng)
        bstar, s2star = bd.mean(0), sd_.mean()
        put(f"g83_{tag}_smoke", bd[:, -1].mean()); put(f"g83_{tag}_smoke_sd", bd[:, -1].std())
        lo, hi = np.quantile(bd[:, -1], [0.025, 0.975])
        put(f"g83_{tag}_smoke_lo", lo); put(f"g83_{tag}_smoke_hi", hi)
        put(f"g83_{tag}_gest", bd[:, 1].mean()); put(f"g83_{tag}_s2", s2star)
        put(f"g83_{tag}_prob_neg", np.mean(bd[:, -1] < 0))
        # Chib (1995): log f(y) = log f(y|b*,s2*) + log pi(b*) + log pi(s2*) - log pi(b*,s2*|y)
        e = y - X @ bstar
        if nu is None:
            loglik = stats.norm.logpdf(e, scale=np.sqrt(s2star)).sum()
        else:
            loglik = stats.t.logpdf(e / np.sqrt(s2star), df=nu).sum() - 0.5 * n * np.log(s2star)
        logprior = log_mvn(bstar, b0, B0) + log_ig(s2star, a0 / 2, d0 / 2)
        # pi(b*|y): Rao-Blackwell average of N(b*| bbar(lam, s2), B1(lam, s2)) over the main run
        B0i = np.linalg.inv(B0)
        sub = rb[::10]
        vals = []
        for lam, s2 in sub:
            XL = X * lam[:, None]
            B1 = np.linalg.inv(XL.T @ X / s2 + B0i)
            vals.append(log_mvn(bstar, B1 @ (XL.T @ y / s2 + B0i @ b0), B1))
        vals = np.array(vals)
        log_pb = vals.max() + np.log(np.mean(np.exp(vals - vals.max())))
        # pi(s2*|b*, y): reduced run with beta fixed at b*
        rng2 = np.random.default_rng(8300 if nu is None else 8350)
        _, _, rb2 = gibbs_reg(y, X, b0, B0, a0, d0, nu, G // 2, burn, rng2, beta_fixed=bstar)
        v2 = np.array([log_ig(s2star, a1 / 2, d1 / 2) for a1, d1 in rb2])
        log_ps = v2.max() + np.log(np.mean(np.exp(v2 - v2.max())))
        logml = loglik + logprior - log_pb - log_ps
        res[tag] = logml
        put(f"g83_{tag}_loglik", loglik); put(f"g83_{tag}_logprior", logprior)
        put(f"g83_{tag}_logpost", log_pb + log_ps)
        put(f"g83_{tag}_logml", logml); put(f"g83_{tag}_log10ml", logml / np.log(10))
    put("g83_log10BF", (res["t"] - res["n"]) / np.log(10))


# ---------------------------------------------------------------- Greenberg 8.6 / 8.7 (Mroz)
def tn_draw(rng, mean, sd, lower, upper):
    """Inverse-cdf draw from N(mean, sd^2) truncated to (lower, upper) (Greenberg eq. 5.1)."""
    a, b = stats.norm.cdf((lower - mean) / sd), stats.norm.cdf((upper - mean) / sd)
    u = rng.uniform(a, b)
    return mean + sd * stats.norm.ppf(np.clip(u, 1e-300, 1 - 1e-16))


def g86():
    d = wd.data("mroz")
    y = d.hours.to_numpy(float)
    X = np.c_[np.ones(len(d)), (d.kidslt6 > 0), (d.kidsge6 > 0), d.age, d.huswage].astype(float)
    n, K = X.shape
    b0 = np.array([2000, -500, -300, -50, -50.0])
    B0 = np.diag([400.0**2, 2000, 2000, 2000, 2000])
    a0, d0 = 28.0, 39_200_000.0  # Greenberg p. 121
    C = y == 0
    put("g86_nC", C.sum())
    B0i = np.linalg.inv(B0)
    G, burn = 6000, 1000
    for tag, nu in (("n", None), ("t", 5.0)):  # Gaussian run reproduces Table 8.1 as a check
        rng = np.random.default_rng(86 if nu else 860)
        beta, s2, lam, ystar = b0.copy(), 1.4e6, np.ones(n), y.copy()
        keep = np.empty((G, K + 1))
        for g in range(G + burn):
            XL = X * lam[:, None]
            B1 = np.linalg.inv(XL.T @ X / s2 + B0i)
            beta = rng.multivariate_normal(B1 @ (XL.T @ ystar / s2 + B0i @ b0), B1)
            e = ystar - X @ beta
            s2 = 1 / rng.gamma((a0 + n) / 2, 2 / (d0 + (lam * e) @ e))
            if nu:
                lam = rng.gamma((nu + 1) / 2, 2 / (nu + e**2 / s2))
            m = X[C] @ beta
            ystar[C] = tn_draw(rng, m, np.sqrt(s2 / lam[C]), -np.inf, 0.0)
            if g >= burn:
                keep[g - burn] = np.r_[beta, np.sqrt(s2)]
        mu = keep.mean(0)
        for j in range(K):
            put(f"g86_{tag}_b{j+1}", mu[j])
        put(f"g86_{tag}_sigma", mu[-1])


def g87():
    d = wd.data("mroz")
    y = d.inlf.to_numpy()
    X = np.c_[np.ones(len(d)), d.educ, d.kidslt6, d.age].astype(float)
    n, K = X.shape
    b0, B0 = np.zeros(K), np.eye(K) * 10.0
    B0i = np.linalg.inv(B0)
    nu = 5.0
    rng = np.random.default_rng(87)
    beta, lam = np.zeros(K), np.ones(n)
    lo, hi = np.where(y == 1, 0.0, -np.inf), np.where(y == 1, np.inf, 0.0)
    G, burn = 6000, 1000
    keep = np.empty((G, K))
    for g in range(G + burn):
        ystar = tn_draw(rng, X @ beta, 1 / np.sqrt(lam), lo, hi)
        e = ystar - X @ beta
        lam = rng.gamma((nu + 1) / 2, 2 / (nu + e**2))
        XL = X * lam[:, None]
        B1 = np.linalg.inv(XL.T @ X + B0i)
        beta = rng.multivariate_normal(B1 @ (XL.T @ ystar + B0i @ b0), B1)
        if g >= burn:
            keep[g - burn] = beta
    mu, sd = keep.mean(0), keep.std(0)
    for j in range(K):
        put(f"g87_b{j+1}", mu[j]); put(f"g87_sd{j+1}", sd[j])
    pr = sm.Probit(y, X).fit(disp=0)
    for j in range(K):
        put(f"g87_probit{j+1}", pr.params[j])


# ---------------------------------------------------------------- expected values
# (key, number as printed in the .tex[, absolute tolerance]). Without a tolerance the check is
# half a unit in the last printed decimal. MCMC quantities carry an explicit Monte Carlo tolerance.
EXPECTED = [
    # Q1 W 12.C2
    ("c2_n", "273"), ("c2_ols_lrp", "1.1719"), ("c2_rho_test", "0.5027"), ("c2_rho_se", "0.0524"),
    ("c2_rho_t", "9.596"), ("c2_co_rho", "0.5086"),
    *[(f"c2_co_d{j}", v) for j, v in enumerate(
        "0.07919 0.07261 0.02390 0.03342 0.08010 0.11321 0.09716 0.10108 0.10634 0.16095 "
        "0.11210 0.09954 0.03018".split())],
    ("c2_co_lrp", "1.10978"), ("c2_co_lrp_se", "0.19068"), ("c2_co_t1", "0.5757"),
    ("c2_co_df", "258"), ("c2_co_crit", "1.969"),
    # Q2 W 12.C10
    ("c10_n", "56"), ("c10_ols_b0", "1.054"), ("c10_ols_b1", "0.502"), ("c10_ols_se0", "1.548"),
    ("c10_ols_se1", "0.266"), ("c10_ols_r2", "0.062"), ("c10_ols_t1", "1.89"), ("c10_rho", "0.5725"),
    ("c10_rho_se", "0.1084"), ("c10_rho_t", "5.283"), ("c10_pw_b0", "7.999"), ("c10_pw_b1", "-0.714"),
    ("c10_pw_se0", "2.048"), ("c10_pw_se1", "0.290"), ("c10_pw_rho", "0.7885"), ("c10_co_b0", "7.287"),
    ("c10_co_b1", "-0.664"), ("c10_co_se1", "0.294"), ("c10_co_rho", "0.7820"),
    ("c10_pw96_b1", "-0.7157"), ("c10_pw96_rho", "0.7805"),
    # Q4 W 17.C2
    ("c17_2_n1", "1989"), ("c17_2_p_b0", "0.546946"), ("c17_2_p_b1", "0.783946"), ("c17_2_p_se1", "0.0867"),
    ("c17_2_pw", "0.9084"), ("c17_2_pnw", "0.7078"), ("c17_2_lpm_b0", "0.7078"), ("c17_2_lpm_b1", "0.2006"),
    ("c17_2_n2", "1971"), ("c17_2_p2_w", "0.520253"), ("c17_2_p2_w", "0.5203"), ("c17_2_p2_wse", "0.096959"),
    ("c17_2_p2_wse", "0.0970"), ("c17_2_p2_wt", "5.366"), ("c17_2_l2_w", "0.937764"),
    ("c17_2_l2_wse", "0.1729"), ("c17_2_l2_wt", "5.42"), ("c17_2_ratio", "1.8025"),
    ("c17_2_ape_p", "0.1042"), ("c17_2_ape_l", "0.1009"), ("c17_2_lpm2_w", "0.1288"),
    # Q5 W 17.C3
    ("c17_3_n", "616"), ("c17_3_nzero", "172"), ("c17_3_zero_pct", "27.92"), ("c17_3_min_pos", "7.28"),
    ("c17_3_max", "2880.27"),
    *[(f"c17_3_b_{k}", v) for k, v in zip(
        "const exper age tenure educ depends married white male".split(),
        "-1252.43 5.20 -4.64 36.02 93.21 35.28 53.69 144.09 308.15".split())],
    *[(f"c17_3_se_{k}", v) for k, v in zip(
        "const exper age tenure educ depends married white male".split(),
        "219.08 6.01 5.71 4.56 10.89 21.92 71.73 102.08 69.89".split())],
    ("c17_3_sigma", "677.74"), ("c17_3_sigma", "677.738"), ("c17_3_sigma_se", "24.14"), ("c17_3_ll", "-3672.96"),
    ("c17_3_b_const", "-1252.429081"), ("c17_3_b_exper", "5.203458"), ("c17_3_b_age", "-4.638942"),
    ("c17_3_b_tenure", "36.023852"), ("c17_3_b_educ", "93.212632"), ("c17_3_b_white", "144.085454"),
    ("c17_3_b_male", "308.150549"), ("c17_3_b_white", "144.085"), ("c17_3_se_white", "102.079"),
    ("c17_3_b_male", "308.151"), ("c17_3_se_male", "69.892"), ("c17_3_t_white", "1.41"), ("c17_3_t_male", "4.41"),
    ("c17_3_xb_nf", "488.883"), ("c17_3_xb_wm", "941.119"), ("c17_3_z_wm", "1.3886"), ("c17_3_z_nf", "0.7213"),
    ("c17_3_Phi_wm", "0.917525"), ("c17_3_phi_wm", "0.152123"), ("c17_3_Phi_nf", "0.764651"),
    ("c17_3_phi_nf", "0.307553"), ("c17_3_E_wm", "966.60"), ("c17_3_E_nf", "582.27"),
    ("c17_3_diff", "384.33"), ("c17_3_xbdiff", "452.24"),
    ("c17_3_union", "439.05"), ("c17_3_union", "439.046"), ("c17_3_union_se", "62.49"),
    ("c17_3_union_se", "62.488"), ("c17_3_union_t", "7.03"),
    ("c17_3_pe_white", "0.0032"), ("c17_3_pe_white", "0.003179"), ("c17_3_pe_white_se", "0.0066"),
    ("c17_3_pe_white_se", "0.006566"), ("c17_3_pe_white_t", "0.48"), ("c17_3_pe_male", "0.0026"),
    ("c17_3_pe_male", "0.002594"), ("c17_3_pe_male_se", "0.0045"), ("c17_3_pe_male_se", "0.004531"),
    ("c17_3_pe_male_t", "0.57"), ("c17_3_pe_union", "0.0300"), ("c17_3_pe_union_se", "0.0042"),
    # Q6 W 17.C9
    ("c17_9_n", "660"), ("c17_9_nzero", "248"), ("c17_9_npos", "412"), ("c17_9_ndistinct", "22"),
    ("c17_9_n2", "98"), ("c17_9_n1", "76"), ("c17_9_n3", "47"), ("c17_9_n43", "31"), ("c17_9_n5", "30"),
    ("c17_9_v43", "1.3333"), ("c17_9_top_share", "0.6845"),
    *[(f"c17_9_b_{k}", v) for k, v in zip("const ecoprc regprc faminc hhsize".split(),
                                           "1.003 -5.821 5.655 0.0066 0.130".split())],
    *[(f"c17_9_se_{k}", v) for k, v in zip("const ecoprc regprc faminc hhsize".split(),
                                            "0.668 0.886 1.065 0.0040 0.095".split())],
    *[(f"c17_9_t_{k}", v) for k, v in zip("const ecoprc regprc faminc hhsize".split(),
                                           "1.50 -6.57 5.31 1.66 1.37".split())],
    ("c17_9_sigma", "3.441"), ("c17_9_sigma_se", "0.127"), ("c17_9_ll", "-1266.4422"), ("c17_9_ll_r", "-1269.0145"),
    ("c17_9_LR", "5.14"), ("c17_9_LR_p", "0.076"), ("c17_9_b_ecoprc", "-5.821484"), ("c17_9_b_regprc", "5.655171"),
    ("c17_9_theta", "-0.166313"), ("c17_9_theta_se", "0.591570"), ("c17_9_theta_t", "-0.2811"),
    ("c17_9_theta_p", "0.7786"), ("c17_9_Emin", "0.798"), ("c17_9_Emax", "3.328"), ("c17_9_r2_tobit", "0.0369"),
    *[(f"c17_9_ols_{k}", v) for k, v in zip("const ecoprc regprc faminc hhsize".split(),
                                             "1.630 -2.903 3.031 0.0028 0.054".split())],
    *[(f"c17_9_olsse_{k}", v) for k, v in zip("const ecoprc regprc faminc hhsize".split(),
                                               "0.450 0.588 0.711 0.0027 0.064".split())],
    ("c17_9_r2_ols", "0.0393"), ("c17_9_scale", "0.5484"), ("c17_9_scale", "0.548383"),
    ("c17_9_sc_eco", "-3.1924"), ("c17_9_sc_reg", "3.1012"),
    # Q7 W 14.C5
    ("c14_5_u0", "0.0800"), ("c14_5_u0_se", "0.0193"), ("c14_5_m0", "0.0467"), ("c14_5_m0_se", "0.0183"),
    ("c14_5_u1", "0.0804"), ("c14_5_u1", "0.080381"), ("c14_5_u1_se", "0.0194"), ("c14_5_u1_se", "0.019401"),
    ("c14_5_m1", "0.0459"), ("c14_5_m1_se", "0.0183"), ("c14_5_u1_t", "4.14"), ("c14_5_u1_cse", "0.0225"),
    ("c14_5_F", "1.21"), ("c14_5_F_p", "0.29"), ("c14_5_occ_switch", "0.888"), ("c14_5_N", "545"),
    ("c14_5_nobs", "4360"),
    # Q8 Greenberg 8.3 (MCMC: Monte Carlo tolerances)
    ("g83_n", "1174"), ("g83_ols_smoke", "-8.401"), ("g83_ols_smoke_se", "0.954"), ("g83_kurt", "0.41"),
    ("g83_n_smoke", "-8.31", 0.10), ("g83_n_smoke_sd", "0.95", 0.05), ("g83_n_smoke_lo", "-10.19", 0.15),
    ("g83_n_smoke_hi", "-6.47", 0.15), ("g83_n_prob_neg", "1.000", 0.001),
    ("g83_t_smoke", "-8.57", 0.10), ("g83_t_smoke_sd", "0.93", 0.05), ("g83_t_smoke_lo", "-10.36", 0.15),
    ("g83_t_smoke_hi", "-6.73", 0.15), ("g83_t_prob_neg", "1.000", 0.001),
    ("g83_n_loglik", "-4904.767", 0.5), ("g83_n_logprior", "-31.685", 0.2), ("g83_n_logpost", "2.493", 0.2),
    ("g83_n_logml", "-4938.945", 0.3), ("g83_n_log10ml", "-2144.957", 0.15),
    ("g83_t_loglik", "-4909.344", 0.5), ("g83_t_logprior", "-31.231", 0.2), ("g83_t_logpost", "2.594", 0.2),
    ("g83_t_logml", "-4943.169", 0.3), ("g83_t_log10ml", "-2146.791", 0.15), ("g83_log10BF", "-1.834", 0.15),
    # Q13 Greenberg 8.6 (Mroz Tobit; MCMC)
    ("g86_nC", "325"),
    *[(f"g86_n_b{j}", v, t) for j, v, t in zip(range(1, 6), "2052.4 -560.0 -296.7 -27.7 -32.4".split(),
                                               (20, 5, 5, 1, 2))],
    ("g86_n_sigma", "1297.7", 15),
    *[(f"g86_t_b{j}", v, t) for j, v, t in zip(range(1, 6), "2105.7 -567.7 -293.7 -28.6 -30.8".split(),
                                               (20, 5, 5, 1, 2))],
    ("g86_t_sigma", "1191.6", 15),
    # Q14 Greenberg 8.7 (Mroz robit; MCMC)
    *[(f"g87_b{j}", v, t) for j, v, t in zip(range(1, 5), "0.331 0.137 -0.957 -0.037".split(),
                                             (0.05, 0.005, 0.02, 0.002))],
    *[(f"g87_sd{j}", v, t) for j, v, t in zip(range(1, 5), "0.448 0.025 0.128 0.007".split(),
                                              (0.03, 0.003, 0.01, 0.001))],
    *[(f"g87_probit{j}", v) for j, v in zip(range(1, 5), "0.321 0.123 -0.867 -0.034".split())],
    # Q15 MS 6.18
    ("ms18_odds_girl5", "1.9937"), ("ms18_p_girl5", "0.6660"), ("ms18_or_b", "1.3910"), ("ms18_or_g", "0.9704"),
    ("ms18_or_g5", "0.8607"), ("ms18_or_10v15", "1.1618"), ("ms18_lb", "0.134"), ("ms18_ub", "0.526"),
    ("ms18_elb", "1.1434"), ("ms18_eub", "1.6922"), ("ms18_lg", "-0.0398"), ("ms18_ug", "-0.0202"),
    ("ms18_elg", "0.9610"), ("ms18_eug", "0.9800"), ("ms18_eta", "0.72"), ("ms18_odds15", "2.0544"),
    ("ms18_p15", "0.6726"),
    # Q16 MS 6.21
    ("ms21_a", "-2.6294"), ("ms21_sa", "0.1578"), ("ms21_b", "0.1802"), ("ms21_b", "0.180213"),
    ("ms21_sb", "0.0146"), ("ms21_sb", "0.014562"), ("ms21_zb", "12.38"), ("ms21_null_dev", "200.66"),
    ("ms21_dev", "13.83"), ("ms21_LR", "186.83"), ("ms21_or1", "1.1975"), ("ms21_or5", "2.4622"),
    ("ms21_lb", "0.15167"), ("ms21_ub", "0.20875"), ("ms21_elb", "1.1638"), ("ms21_eub", "1.2321"),
    ("ms21_eta1", "-2.449148"), ("ms21_p1", "0.0795"), ("ms21_obs1", "0.0733"), ("ms21_eta22", "1.335319"),
    ("ms21_p22", "0.7917"), ("ms21_obs22", "0.6053"), ("ms21_dev_p", "0.032"), ("ms21_pearson", "14.82"),
    ("ms21_n", "942"),
]

# Displayed arithmetic (estilo-avaliacao §4.4): each operation shown with printed numbers must give
# the printed result. (expression on printed numbers, printed result[, tolerance])
DISPLAYED = [
    ("0.502681/0.052386", "9.596"),
    ("0.07919+0.07261+0.02390+0.03342+0.08010+0.11321+0.09716+0.10108+0.10634+0.16095+0.11210"
     "+0.09954+0.03018", "1.10978"),
    ("(1.10978-1)/0.19068", "0.5757"), ("272-14", "258"),
    ("0.502/0.266", "1.89"), ("0.572472/0.108354", "5.283"), ("(-0.714)-(-0.716)", "0.002"),
    ("0.7885-0.7820", "0.0065"), ("(-0.664)-(-0.714)", "0.050"),
    ("0.546946+0.783946", "1.330892"), ("0.7078+0.2006", "0.9084"), ("0.520253/0.096959", "5.366"),
    ("0.937764/0.520253", "1.8025"),
    ("172/616*100", "27.92"), ("144.085/102.079", "1.41"), ("308.151/69.892", "4.41"),
    ("-1252.429081+5.203458*10-4.638942*35+36.023852*10+93.212632*16", "488.883"),
    ("488.883+144.085454+308.150549", "941.119"), ("941.119/677.738", "1.3886"),
    ("488.883/677.738", "0.7213"), ("0.917525*941.119", "863.5002"), ("677.738*0.152123", "103.0995"),
    ("863.5002+103.0995", "966.60"), ("0.764651*488.883", "373.8249"), ("677.738*0.307553", "208.4404"),
    ("373.8249+208.4404", "582.27"), ("966.60-582.27", "384.33"), ("439.046/62.488", "7.03"),
    ("0.003179/0.006566", "0.48"), ("0.002594/0.004531", "0.57"),
    ("282/412", "0.6845"), ("98+76+47+31+30", "282"), ("(-1266.4422)-(-1269.0145)", "2.5723"), ("2*(2.5723)", "5.14"),
    ("-5.821484+5.655171", "-0.166313"), ("-0.166313/0.591570", "-0.2811"),
    ("-5.821484*0.548383", "-3.1924"), ("5.655171*0.548383", "3.1012"),
    ("0.0804-0.0800", "0.0004"), ("0.080381/0.019401", "4.14"),
    ("512/2", "256"), ("-4904.767-31.685-2.493", "-4938.945"), ("-4909.344-31.231-2.594", "-4943.169"),
    ("-4938.945/2.302585", "-2144.957"), ("-4943.169/2.302585", "-2146.791"),
    ("(-2146.791)-(-2144.957)", "-1.834"), ("10**1.834", "68", 0.5),
    ("math.exp(0.69)", "1.9937"), ("1.9937/(1+1.9937)", "0.6660"), ("math.exp(0.33)", "1.3910"),
    ("math.exp(-0.03)", "0.9704"), ("1-math.exp(-0.15)", "0.139"), ("math.exp(-0.15)", "0.8607"),
    ("(-0.03)*(-5)", "0.15"), ("math.exp(0.15)", "1.1618"), ("0.33-1.96*0.10", "0.134"),
    ("0.33+1.96*0.10", "0.526"), ("math.exp(0.134)", "1.1434"), ("math.exp(0.526)", "1.6922"),
    ("-0.03-1.96*0.005", "-0.0398"), ("-0.03+1.96*0.005", "-0.0202"), ("math.exp(-0.0398)", "0.9610"),
    ("math.exp(-0.0202)", "0.9800"), ("0.69+0.33*1+(-0.03)*(15-5)", "0.72"), ("math.exp(0.72)", "2.0544"),
    ("2.0544/3.0544", "0.6726"), ("200.66-13.83", "186.83"), ("math.exp(0.180213)", "1.1975"),
    ("5*0.180213", "0.901065"), ("math.exp(0.901065)", "2.4622"), ("0.180213-1.96*0.014562", "0.15167"),
    ("0.180213+1.96*0.014562", "0.20875"), ("math.exp(0.15167)", "1.1638"), ("math.exp(0.20875)", "1.2321"),
    ("1/(1+math.exp(2.449148))", "0.0795"), ("17/232", "0.0733"), ("1/(1+math.exp(-1.335319))", "0.7917"),
    ("23/38", "0.6053"),
]


def _tol(printed):
    """Half a unit in the last printed decimal of `printed`."""
    dec = len(printed.split(".")[1]) if "." in printed else 0
    return 0.5 * 10 ** (-dec) + 1e-9


if __name__ == "__main__":
    import math  # noqa: F401  (used inside the DISPLAYED expressions)
    for f in (w12c2, w12c10, w17c2, w17c3, w17c9, w14c5, ms618, ms621, g83, g86, g87):
        f()
    bad = []
    for item in EXPECTED:
        key, printed = item[0], item[1]
        tol = item[2] if len(item) > 2 else _tol(printed)
        got = OUT.get(key)
        if got is None or abs(got - float(printed)) > tol:
            bad.append(f"MISMATCH {key}: printed {printed}, computed {got}")
    for item in DISPLAYED:
        expr, printed = item[0], item[1]
        tol = item[2] if len(item) > 2 else _tol(printed)
        val = eval(expr)
        if abs(val - float(printed)) > tol:
            bad.append(f"DISPLAYED {expr} = {val}, printed {printed}")
    for line in bad:
        print(line)
    if bad:
        raise SystemExit(1)
    print(f"All {len(EXPECTED)} printed numbers and {len(DISPLAYED)} displayed operations reproduced.")
