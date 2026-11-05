"""Check script for Listas/lista-L05-book-exercises.tex (unit L05, Classes 5+6).

Reproduces and asserts every number printed in the answer key: the arithmetic on the MHE
tables, the Wooldridge computer exercises (CARD, KIELMC) and the KIELMC regressions behind
Wooldridge Problem 13.2, plus numerical checks of the Greenberg Ch. 11 derivations.
Run from the project root or from Listas/:  python Listas/L05-book-exercises-check.py
Fails with AssertionError naming the first mismatch. Data: Aula/class-05-06/materials/card.csv
(CARD) and Listas/data/kielmc.csv (KIELMC, from the `wooldridge` package; see data/README.md).
"""
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
from linearmodels.iv import IV2SLS
from scipy import integrate, stats

ROOT = Path(__file__).resolve().parents[1]


def chk(name, value, expected, tol):
    """Assert |value - expected| <= tol and print the pair; `name` labels the printed line."""
    assert abs(value - expected) <= tol, f"{name}: got {value!r}, expected {expected!r} (tol {tol})"
    print(f"ok  {name:<44} {value: .6f}  (printed {expected})")


# ---------------------------------------------------------------- MHE Tables 2.2.1-2.2.2
print("== Q1  MHE Tables 2.2.1-2.2.2 (STAR)")
chk("t small, col (1)", 4.82 / 2.19, 2.2009, 5e-5)
chk("CI low col (1)", 4.82 - 1.96 * 2.19, 0.5276, 5e-5)
chk("CI high col (1)", 4.82 + 1.96 * 2.19, 9.1124, 5e-5)
chk("t small, col (4)", 5.37 / 1.19, 4.5126, 5e-5)
chk("CI low col (4)", 5.37 - 1.96 * 1.19, 3.0376, 5e-5)
chk("CI high col (4)", 5.37 + 1.96 * 1.19, 7.7024, 5e-5)
chk("t regular/aide col (1)", 0.12 / 2.23, 0.0538, 5e-5)
chk("sqrt(0.69/0.75)", np.sqrt(0.69 / 0.75), 0.95917, 5e-6)
chk("predicted se col (3)", 1.26 * np.sqrt(0.69 / 0.75), 1.20855, 5e-6)
chk("sigma = 5.37/0.2", 5.37 / 0.2, 26.85, 1e-9)
chk("sd of uniform percentile", 100 / np.sqrt(12), 28.8675, 5e-5)
chk("raw score gap small-regular", 54.70 - 48.90, 5.80, 1e-9)
chk("1.96*2.19", 1.96 * 2.19, 4.2924, 1e-9)
chk("1.96*1.19", 1.96 * 1.19, 2.3324, 1e-9)
chk("1.96*0.009 (Q2)", 1.96 * 0.009, 0.01764, 1e-9)
chk("1.96*1.36 (Q4)", 1.96 * 1.36, 2.6656, 1e-9)
chk("1.25^2 (Q4)", 1.25**2, 1.5625, 1e-12)
chk("0.54^2 (Q4)", 0.54**2, 0.2916, 1e-12)
chk("sum (Q4)", 1.5625 + 0.2916, 1.8541, 1e-12)
chk("2018/302 (Q6)", 2018 / 302, 6.6821, 5e-5)
chk("0.103-0.075 (Q3)", 0.103 - 0.075, 0.028, 1e-12)

# ---------------------------------------------------------------- MHE Table 3.2.1
print("== Q2  MHE Table 3.2.1 (OVB)")
chk("bias from AFQT, (3)-(4)", 0.114 - 0.087, 0.027, 1e-12)
chk("implied gamma = 0.027/0.15", 0.027 / 0.15, 0.18, 1e-12)
chk("bias from family bkgd, (2)-(3)", 0.131 - 0.114, 0.017, 1e-12)
chk("share of col (1) left in col (5)", 0.066 / 0.132, 0.50, 1e-12)
chk("CI low col (4)", 0.087 - 1.96 * 0.009, 0.06936, 1e-9)
chk("CI high col (4)", 0.087 + 1.96 * 0.009, 0.10464, 1e-9)

# ---------------------------------------------------------------- MHE Tables 4.1.1-4.1.3
print("== Q3  MHE Tables 4.1.1-4.1.3 (IV / Wald)")
chk("ln wage gap from means", 5.8916 - 5.9051, -0.0135, 1e-9)
chk("educ gap from means", 12.6881 - 12.8394, -0.1513, 1e-9)
chk("Wald 4.1.2 = -0.01349/-0.1514", -0.01349 / -0.1514, 0.089102, 5e-7)
chk("approx se = 0.00337/0.1514", 0.00337 / 0.1514, 0.022259, 5e-7)
chk("sqrt(0.024^2-0.0004^2)", np.sqrt(0.024**2 - 0.0004**2), 0.023997, 5e-7)
chk("Hausman-type t, 4.1.1 (3) vs (1)", (0.103 - 0.075) / np.sqrt(0.024**2 - 0.0004**2), 1.1668, 5e-5)
chk("Wald 1981", -435.8 / 0.159, -2740.88, 5e-3)
chk("Wald 1971", -325.9 / 0.159, -2049.69, 5e-3)
chk("approx se Wald 1981", 210.5 / 0.159, 1323.90, 5e-3)
chk("approx se Wald 1971", 46.6 / 0.159, 293.08, 5e-3)
chk("Wald 1981 / mean", 2740.88 / 16461, 0.16651, 5e-6)
chk("Wald 1971 / mean", 2049.69 / 3338, 0.61405, 5e-6)
chk("t eligibility 1981", -435.8 / 210.5, -2.0703, 5e-5)
chk("t eligibility 1969", -2.0 / 34.5, -0.0580, 5e-5)
chk("t first stage", 0.159 / 0.040, 3.975, 1e-9)

# ---------------------------------------------------------------- MHE Table 5.2.1
print("== Q4  MHE Table 5.2.1 (DiD)")
chk("NJ change", 21.03 - 20.44, 0.59, 1e-9)
chk("PA change", 21.17 - 23.33, -2.16, 1e-9)
chk("DiD via changes", (21.03 - 20.44) - (21.17 - 23.33), 2.75, 1e-9)
chk("DiD via gaps", -0.14 - (-2.89), 2.75, 1e-9)
chk("t DiD", 2.76 / 1.36, 2.0294, 5e-5)
chk("CI low DiD", 2.76 - 1.96 * 1.36, 0.0944, 5e-5)
chk("CI high DiD", 2.76 + 1.96 * 1.36, 5.4256, 5e-5)
chk("se DiD, independent samples", np.sqrt(1.25**2 + 0.54**2), 1.36165, 5e-6)

# ---------------------------------------------------------------- MHE Figure 6.1.2
print("== Q5  MHE Figure 6.1.2 (sharp RD), values read off the figure")
chk("jump in P(win)", 0.58 - 0.14, 0.44, 1e-9)

# ---------------------------------------------------------------- MHE Table 6.2.1
print("== Q6  MHE Table 6.2.1 (fuzzy RD)")
for e, m in [(40, 40), (41, 20.5), (80, 40), (81, 27), (120, 40), (121, 30.25)]:
    chk(f"Maimonides m(e={e})", e / ((e - 1) // 40 + 1), m, 1e-12)
chk("7-pupil cut, col (4)", 7 * 0.230, 1.61, 1e-9)
chk("7-pupil cut, slope -.25", 7 * 0.25, 1.75, 1e-12)
chk("effect size 1.75/9.6", 1.75 / 9.6, 0.18229, 5e-6)
chk("t col (4)", -0.230 / 0.092, -2.5, 1e-9)
chk("t col (8)", -0.270 / 0.281, -0.9609, 5e-5)
chk("se ratio (8)/(5)", 0.281 / 0.113, 2.4867, 5e-5)
chk("sqrt(2018/302)", np.sqrt(2018 / 302), 2.5850, 5e-5)

# ---------------------------------------------------------------- CARD (W 15.C3, 15.C5)
card = pd.read_csv(ROOT / "Aula/class-05-06/materials/card.csv", lineterminator="\r", na_values=".")
assert len(card) == 3010
regs = "+".join(f"reg66{i}" for i in range(2, 10))
X = "exper+expersq+black+smsa+south+smsa66+" + regs

print("== Q7  W 15.C3")
iq = card.dropna(subset=["IQ"])
a = smf.ols("IQ~nearc4", iq).fit()
chk("n with IQ", a.nobs, 2061, 0)
chk("(ii) intercept", a.params["Intercept"], 100.611, 5e-4)
chk("(ii) se intercept", a.bse["Intercept"], 0.627, 5e-4)
chk("(ii) nearc4", a.params["nearc4"], 2.596, 5e-4)
chk("(ii) se nearc4", a.bse["nearc4"], 0.745, 5e-4)
chk("(ii) t nearc4", a.tvalues["nearc4"], 3.483, 5e-4)
chk("(ii) R2", a.rsquared, 0.0059, 5e-5)
chk("(ii) p nearc4", a.pvalues["nearc4"], 0.0005, 5e-5)
chk("(ii) t by hand 2.5962/0.7455", 2.5962 / 0.7455, 3.4825, 5e-5)
chk("(ii) df geography F denom", a.nobs - 11, 2050, 0)
b =smf.ols("IQ~nearc4+smsa66+" + regs, iq).fit()
chk("(iii) intercept", b.params["Intercept"], 104.773, 5e-4)
chk("(iii) nearc4", b.params["nearc4"], 0.348, 5e-4)
chk("(iii) se nearc4", b.bse["nearc4"], 0.814, 5e-4)
chk("(iii) t nearc4", b.tvalues["nearc4"], 0.427, 5e-4)
chk("(iii) p nearc4", b.pvalues["nearc4"], 0.669, 5e-4)
chk("(iii) smsa66", b.params["smsa66"], 1.089, 5e-4)
chk("(iii) se smsa66", b.bse["smsa66"], 0.809, 5e-4)
chk("(iii) reg665", b.params["reg665"], -8.475, 5e-4)
chk("(iii) reg667", b.params["reg667"], -8.394, 5e-4)
chk("(iii) R2", b.rsquared, 0.0626, 5e-5)
F = b.f_test("smsa66=0," + ",".join(f"reg66{i}=0" for i in range(2, 10)))
chk("(iii) F geography (9 df)", float(np.squeeze(F.fvalue)), 13.80, 5e-3)
assert float(np.squeeze(F.pvalue)) < 0.001
chk("(iii) t by hand 0.3479/0.8144", 0.3479 / 0.8144, 0.4272, 5e-5)
chk("(iii) nearc4 4 dp", b.params["nearc4"], 0.3479, 5e-5)
chk("(iii) se nearc4 4 dp", b.bse["nearc4"], 0.8144, 5e-5)
chk("(ii) nearc4 4 dp", a.params["nearc4"], 2.5962, 5e-5)
chk("(ii) se nearc4 4 dp", a.bse["nearc4"], 0.7455, 5e-5)
chk("corr(nearc4, smsa66)", iq[["nearc4", "smsa66"]].corr().iloc[0, 1], 0.412, 5e-4)

print("== Q8  W 15.C5")
ols = smf.ols("lwage~educ+" + X, card).fit()
chk("Table 15.1 OLS educ", ols.params["educ"], 0.0747, 5e-5)
chk("Table 15.1 OLS se", ols.bse["educ"], 0.0035, 5e-5)
iv1 = IV2SLS.from_formula("lwage~1+" + X + "+[educ~nearc4]", card).fit(cov_type="unadjusted", debiased=True)
chk("Table 15.1 IV educ", iv1.params["educ"], 0.1315, 5e-5)
chk("Table 15.1 IV se", iv1.std_errors["educ"], 0.0550, 5e-5)
rf = smf.ols("educ~nearc4+" + X, card).fit()
chk("(i) RF nearc4", rf.params["nearc4"], 0.320, 5e-4)
chk("(i) RF se nearc4", rf.bse["nearc4"], 0.088, 5e-4)
chk("(i) RF t nearc4", rf.tvalues["nearc4"], 3.64, 5e-3)
chk("(i) RF intercept", rf.params["Intercept"], 16.638, 5e-4)
chk("(i) RF exper", rf.params["exper"], -0.413, 5e-4)
chk("(i) RF R2", rf.rsquared, 0.477, 5e-4)
card["v2hat"] = rf.resid
cf = smf.ols("lwage~educ+" + X + "+v2hat", card).fit()
chk("(i) CF educ = IV", cf.params["educ"], 0.1315, 5e-5)
chk("(i) CF v2hat", cf.params["v2hat"], -0.0571, 5e-5)
chk("(i) CF se v2hat", cf.bse["v2hat"], 0.0528, 5e-5)
chk("(i) CF t v2hat", cf.tvalues["v2hat"], -1.081, 5e-4)
chk("(i) CF p v2hat", cf.pvalues["v2hat"], 0.280, 5e-4)
chk("(i) t by hand", -0.05706 / 0.05281, -1.0805, 5e-5)
chk("(i) v2hat 5 dp", cf.params["v2hat"], -0.05706, 5e-6)
chk("(i) se v2hat 5 dp", cf.bse["v2hat"], 0.05281, 5e-6)
cfr = smf.ols("lwage~educ+" + X + "+v2hat", card).fit(cov_type="HC1")
chk("(i) robust t v2hat", cfr.tvalues["v2hat"], -1.101, 5e-4)
iv2 = IV2SLS.from_formula("lwage~1+" + X + "+[educ~nearc4+nearc2]", card).fit(cov_type="unadjusted", debiased=True)
chk("(ii) 2SLS educ", iv2.params["educ"], 0.1571, 5e-5)
chk("(ii) 2SLS se educ", iv2.std_errors["educ"], 0.0526, 5e-5)
chk("(ii) change in educ coef", 0.1571 - 0.1315, 0.0256, 1e-9)
fs = smf.ols("educ~nearc4+nearc2+" + X, card).fit()
chk("(ii) FS nearc4", fs.params["nearc4"], 0.321, 5e-4)
chk("(ii) FS se nearc4", fs.bse["nearc4"], 0.088, 5e-4)
chk("(ii) FS nearc2", fs.params["nearc2"], 0.123, 5e-4)
chk("(ii) FS se nearc2", fs.bse["nearc2"], 0.077, 5e-4)
card["u2sls"] = iv2.resids
ov = smf.ols("u2sls~nearc4+nearc2+" + X, card).fit()
chk("(iii) R2 aux", ov.rsquared, 0.00041467, 5e-9)
chk("(iii) nR2", ov.nobs * ov.rsquared, 1.248, 5e-4)
chk("(iii) nR2 by hand", 3010 * 0.00041467, 1.24816, 5e-6)
chk("(iii) p chi2(1)", stats.chi2.sf(ov.nobs * ov.rsquared, 1), 0.264, 5e-4)
chk("(iii) chi2(1) 5% crit", stats.chi2.ppf(0.95, 1), 3.841, 5e-4)
chk("(iii) linearmodels Sargan", iv2.sargan.stat, 1.248, 5e-4)

# ---------------------------------------------------------------- KIELMC (W 13.2, 13.C3)
k = pd.read_csv(ROOT / "Listas/data/kielmc.csv")
assert len(k) == 321

print("== Q9  W 13.2 (reproducing the book's equations from KIELMC)")
m1 = smf.ols("lprice~nearinc+y81nrinc", k).fit()
m2 = smf.ols("lprice~y81+y81nrinc", k).fit()
m9 = smf.ols("lprice~y81+nearinc+y81nrinc", k).fit()
for name, got, exp in [("eq1 const", m1.params["Intercept"], 11.49), ("eq1 nearinc", m1.params["nearinc"], -0.547),
                       ("eq1 y81*nearinc", m1.params["y81nrinc"], 0.394), ("eq2 const", m2.params["Intercept"], 11.18),
                       ("eq2 y81", m2.params["y81"], 0.563), ("eq2 y81*nearinc", m2.params["y81nrinc"], -0.403),
                       ("13.9 const", m9.params["Intercept"], 11.29), ("13.9 y81", m9.params["y81"], 0.457),
                       ("13.9 nearinc", m9.params["nearinc"], -0.340), ("13.9 y81*nearinc", m9.params["y81nrinc"], -0.063)]:
    chk(name, got, exp, 5.01e-3)
chk("eq1 se const (book prints .26)", m1.bse["Intercept"], 0.026, 5e-4)
chk("eq2 se const (book prints .27)", m2.bse["Intercept"], 0.027, 5e-4)
chk("eq1 R2", m1.rsquared, 0.220, 5e-4)
chk("eq2 R2", m2.rsquared, 0.337, 5e-4)
chk("delta0+delta1", 0.457 + (-0.063), 0.394, 1e-12)
chk("beta1+delta1", -0.340 + (-0.063), -0.403, 1e-12)
cells = k.groupby(["nearinc", "y81"]).size()
chk("n far 1978", cells[(0, 0)], 123, 0)
chk("n far 1981", cells[(0, 1)], 102, 0)
chk("n near 1978", cells[(1, 0)], 56, 0)
chk("n near 1981", cells[(1, 1)], 40, 0)
chk("eq1 const from (13.9)", 11.29 + 0.457 * 102 / 225, 11.4972, 5e-5)
chk("eq2 const from (13.9)", 11.29 - 0.340 * 56 / 179, 11.1836, 5e-5)

print("== Q11 W 13.C3")
c2 = smf.ols("lprice~y81+ldist+y81ldist", k).fit()
for name, got, exp in [("(ii) const", c2.params["Intercept"], 8.058), ("(ii) se const", c2.bse["Intercept"], 0.508),
                       ("(ii) y81", c2.params["y81"], -0.011), ("(ii) se y81", c2.bse["y81"], 0.805),
                       ("(ii) ldist", c2.params["ldist"], 0.317), ("(ii) se ldist", c2.bse["ldist"], 0.052),
                       ("(ii) y81*ldist", c2.params["y81ldist"], 0.048), ("(ii) se y81*ldist", c2.bse["y81ldist"], 0.082),
                       ("(ii) R2", c2.rsquared, 0.396)]:
    chk(name, got, exp, 5.01e-4)
chk("(ii) t y81*ldist", c2.tvalues["y81ldist"], 0.589, 5e-4)
chk("(ii) p y81*ldist", c2.pvalues["y81ldist"], 0.556, 5e-4)
chk("(ii) t ldist", c2.tvalues["ldist"], 6.15, 5e-3)
chk("(ii) y81*ldist 4 dp", c2.params["y81ldist"], 0.0482, 5e-5)
chk("(ii) se y81*ldist 4 dp", c2.bse["y81ldist"], 0.0818, 5e-5)
chk("(ii) t by hand 0.0482/0.0818", 0.0482 / 0.0818, 0.589, 5e-4)
c3 = smf.ols("lprice~y81+ldist+y81ldist+age+agesq+rooms+baths+lintst+lland+larea", k).fit()
for name, got, exp in [("(iii) y81", c3.params["y81"], -0.2254), ("(iii) se y81", c3.bse["y81"], 0.4947),
                       ("(iii) ldist", c3.params["ldist"], 0.0009), ("(iii) se ldist", c3.bse["ldist"], 0.0446),
                       ("(iii) y81*ldist", c3.params["y81ldist"], 0.0625), ("(iii) se y81*ldist", c3.bse["y81ldist"], 0.0503),
                       ("(iii) lintst", c3.params["lintst"], -0.0600), ("(iii) larea", c3.params["larea"], 0.3507),
                       ("(iii) R2", c3.rsquared, 0.7870)]:
    chk(name, got, exp, 5.01e-5)
chk("(iii) t y81*ldist", c3.tvalues["y81ldist"], 1.242, 5e-4)
chk("(iii) p y81*ldist", c3.pvalues["y81ldist"], 0.215, 5e-4)
chk("(iii) t ldist", c3.tvalues["ldist"], 0.021, 5e-4)
chk("corr(ldist, lintst)", k[["ldist", "lintst"]].corr().iloc[0, 1], 0.781, 5e-4)

# ---------------------------------------------------------------- Greenberg Ch. 11 (numerical checks)
print("== Q12-Q15 Greenberg 11.1-11.4 (numerical checks of the derived densities)")
rng = np.random.default_rng(5)
s_jj, s_jv = 1.7, 0.6                        # sigma_jj, sigma_jv (variance of v fixed at 1)
om = s_jj - s_jv**2                          # omega_jj
xb, zg, y = 0.4, -0.3, 1.1                   # x'beta_j, x'gamma1+z'gamma2, observed y_ji
Sig = np.array([[s_jj, s_jv], [s_jv, 1.0]])
mvn = stats.multivariate_normal([xb, zg], Sig)
# (11.4): f(y | s*) from the joint equals N(x'b + s_jv e, omega)
for sstar in (-0.8, 0.5):
    cond = mvn.pdf([y, sstar]) / stats.norm.pdf(sstar, zg, 1.0)
    chk(f"(11.4) cond. density, s*={sstar}", cond, stats.norm.pdf(y, xb + s_jv * (sstar - zg), np.sqrt(om)), 1e-12)
# (11.8): integrate the joint over the s* region and compare with N(y|x'b, s_jj) Phi((2j-1) mu/phi)
mu = zg + s_jv / s_jj * (y - xb)
phi = np.sqrt(1 - s_jv**2 / s_jj)
for j, (lo, hi) in [(0, (-np.inf, 0.0)), (1, (0.0, np.inf))]:
    num = integrate.quad(lambda s: mvn.pdf([y, s]), lo, hi)[0]
    chk(f"(11.8) j={j}", num, stats.norm.pdf(y, xb, np.sqrt(s_jj)) * stats.norm.cdf((2 * j - 1) * mu / phi), 1e-9)
# (11.6)-(11.7) and Algorithm 11.1 steps: log kernel minus claimed log density is constant in the argument
n, m0, M0, nu0, d0 = 6, 0.2, 2.0, 4.0, 8.0
E = rng.normal(size=n)
w = rng.normal(size=n)                       # w = Y_j - X_j beta_j
A = np.eye(n) + M0 * np.outer(E, E)


def logmarg(o):
    """log N(Y | X b + m0 E, o (I + E M0 E')): the marginal (11.6)-(11.7) evaluated at omega=o."""
    return stats.multivariate_normal(m0 * E, o * A).logpdf(w)


def logmarg_mc(o, draws=400_000):
    """Same marginal by Monte Carlo integration over sigma_jv ~ N(m0, o M0)."""
    sv = rng.normal(m0, np.sqrt(o * M0), draws)
    ll = stats.norm.logpdf(w[None, :], sv[:, None] * E[None, :], np.sqrt(o)).sum(1)
    return np.log(np.mean(np.exp(ll - ll.max()))) + ll.max()


chk("(11.6)-(11.7) marginal vs Monte Carlo", logmarg_mc(1.3), logmarg(1.3), 2e-2)
d_j =(w - m0 * E) @ np.linalg.solve(A, w - m0 * E)
ig = stats.invgamma((nu0 + n) / 2, scale=(d0 + d_j) / 2)
diffs = [logmarg(o) + stats.invgamma(nu0 / 2, scale=d0 / 2).logpdf(o) - ig.logpdf(o) for o in (0.5, 1.0, 2.5, 7.0)]
chk("step 11.1(a) IG kernel (spread)", max(diffs) - min(diffs), 0.0, 1e-9)
o = 1.3
C = 1 / (1 / M0 + E @ E)
c = C * (m0 / M0 + E @ w)
diffs = [stats.norm.logpdf(w, sv * E, np.sqrt(o)).sum() + stats.norm.logpdf(sv, m0, np.sqrt(o * M0))
         - stats.norm.logpdf(sv, c, np.sqrt(o * C)) for sv in (-1.0, 0.0, 0.7, 2.0)]
chk("step 11.1(b) normal kernel (spread)", max(diffs) - min(diffs), 0.0, 1e-9)
p, nobs = 3, 8                               # step 11.2 with a 3-dim beta and 2x3 X_ji blocks
Xs = rng.normal(size=(nobs, 2, p))
ys = rng.normal(size=(nobs, 2))
Sigs = [Sig if i % 2 else np.array([[0.9, -0.3], [-0.3, 1.0]]) for i in range(nobs)]
b0, B0 = np.zeros(p), 4 * np.eye(p)
Bpost = np.linalg.inv(np.linalg.inv(B0) + sum(Xs[i].T @ np.linalg.solve(Sigs[i], Xs[i]) for i in range(nobs)))
bhat = Bpost @ (np.linalg.solve(B0, b0) + sum(Xs[i].T @ np.linalg.solve(Sigs[i], ys[i]) for i in range(nobs)))
post = stats.multivariate_normal(bhat, Bpost)


def logker(beta):
    """Log prior plus log likelihood of beta in step 11.2 (SUR form)."""
    return stats.multivariate_normal(b0, B0).logpdf(beta) + sum(
        stats.multivariate_normal(Xs[i] @ beta, Sigs[i]).logpdf(ys[i]) for i in range(nobs))


diffs = [logker(bb) - post.logpdf(bb) for bb in rng.normal(size=(4, p))]
chk("step 11.2 normal kernel (spread)", max(diffs) - min(diffs), 0.0, 1e-9)
diffs = [mvn.logpdf([y, s]) - stats.norm.logpdf(s, mu, phi) for s in (-1.5, -0.2, 0.3, 1.9)]
chk("step 11.3 s* | y kernel (spread)", max(diffs) - min(diffs), 0.0, 1e-9)

print("\nALL CHECKS PASSED")
