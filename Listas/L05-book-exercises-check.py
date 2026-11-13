"""Check script for Listas/lista-L05-book-exercises.tex (unit L05, Classes 5+6).

Reproduces and asserts every number printed in the answer key: the arithmetic on the MHE
tables, the Wooldridge computer exercises (CARD, KIELMC) and the KIELMC regressions behind
Wooldridge Problem 13.2, numerical checks of the Greenberg Ch. 11 derivations, the attenuation
factor of Wooldridge Problem 9.7 (with a seeded simulation), the two original exercises
(DAG / collider bias simulation, Simpson's-paradox table), the arithmetic on MHE Table 7.2.1
(JTPA QTE, Q19) and the sharp-RDD regressions on the drinking-age data (Q20, original).
Simulations use fixed seeds; Q19 and Q20 are deterministic.
Run from the project root or from Listas/:  python Listas/L05-book-exercises-check.py
Fails with AssertionError naming the first mismatch. Data: Aula/class-05-06/materials/card.csv
(CARD), Listas/data/kielmc.csv (KIELMC, from the `wooldridge` package; see data/README.md) and
Aula/class-05-06/materials/age-mva-internal.txt (MLDA cells, class site).
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


def ols(y, *xs):
    """OLS slopes of y on a constant and the columns xs (constant dropped from the result)."""
    Xm = np.column_stack([np.ones(len(y)), *xs])
    return np.linalg.lstsq(Xm, y, rcond=None)[0][1:]


# ---------------------------------------------------------------- W 9.7 (attenuation, m measures)
print("== Q16 W 9.7 (CEV with m measures): analytic factor and simulation")
lam = lambda m, s2x=1.0, s2e=1.0: s2x / (s2x + s2e / m)   # plim(b1)/beta1
for m, printed in [(1, 0.5), (2, 0.6667), (4, 0.8), (10, 0.9091)]:
    chk(f"lambda_m, m={m}", lam(m), printed, 5e-5)
rng = np.random.default_rng(97)
nn, b0_, b1_ = 200_000, 1.0, 1.0
xs_ = rng.normal(0, 1, nn)
yv = b0_ + b1_ * xs_ + rng.normal(0, 1, nn)
zs = xs_[:, None] + rng.normal(0, 1, (nn, 10))             # 10 measures z_h = x* + e_h, var(e_h) = 1
for m, printed in [(1, 0.5010), (2, 0.6673), (4, 0.8007), (10, 0.9112)]:
    bm = ols(yv, zs[:, :m].mean(1))[0]
    chk(f"simulated b1, m={m} (vs lambda_m)", bm, lam(m), 1e-2)
    chk(f"simulated b1, m={m} (printed)", bm, printed, 5e-5)

# ---------------------------------------------------------------- original: DAG, d-separation, collider bias
print("== Q17 DAG: population coefficients and simulation (seed 17)")
rng = np.random.default_rng(17)
nn = 200_000
Z, W_ = rng.normal(size=nn), rng.normal(size=nn)
Xd = 0.8 * Z + 0.5 * W_ + rng.normal(size=nn)
M_ = 1.0 * Xd + rng.normal(size=nn)
Yd = 0.5 * M_ + 1.0 * Z + rng.normal(size=nn)
Cd = Xd + Yd + rng.normal(size=nn)
Dd = Cd + rng.normal(size=nn)
chk("Var(X)", 0.8**2 + 0.5**2 + 1, 1.89, 1e-12)
chk("Cov(X,Y)", 0.5 * 1.89 + 0.8, 1.745, 1e-12)
for name, got, pop, printed in [
    ("Y~X", ols(Yd, Xd)[0], 1.745 / 1.89, 0.9210),
    ("Y~X+Z", ols(Yd, Xd, Z)[0], 0.5, 0.4979),
    ("Y~X+Z+W", ols(Yd, Xd, Z, W_)[0], 0.5, 0.4974),
    ("Y~X+Z+M", ols(Yd, Xd, Z, M_)[0], 0.0, -0.0032),
    ("Y~X+Z+C", ols(Yd, Xd, Z, Cd)[0], -1 / 3, -0.3342),
    ("Y~X+Z+D", ols(Yd, Xd, Z, Dd)[0], -1 / 13, -0.0792),
    ("Z~W (independent)", ols(Z, W_)[0], 0.0, -0.0017),
    ("Z~W+X (X a collider)", ols(Z, W_, Xd)[0], -10 / 41, -0.2428),
]:
    chk(f"{name}: sim vs population", got, pop, 1e-2)
    chk(f"{name}: sim (printed)", got, printed, 5e-5)
chk("1.745/1.89", 1.745 / 1.89, 0.92328, 5e-6)
chk("0.8/1.89 (back-door bias)", 0.8 / 1.89, 0.42328, 5e-6)
chk("s = 1.25/2.25", 1.25 / 2.25, 0.55556, 5e-6)
chk("0.5-1.5*5/9", 0.5 - 1.5 * 5 / 9, -1 / 3, 1e-12)
chk("s' = 1.25/3.25", 1.25 / 3.25, 0.38462, 5e-6)
chk("0.5-1.5*5/13", 0.5 - 1.5 * 5 / 13, -1 / 13, 1e-12)
chk("-0.5*0.8/1.64", -0.5 * 0.8 / 1.64, -10 / 41, 1e-12)
chk("-1/13", -1 / 13, -0.07692, 5e-6)
chk("-10/41", -10 / 41, -0.24390, 5e-6)

# ---------------------------------------------------------------- original: Simpson's paradox
print("== Q18 Simpson's paradox (2x2x2 table)")
# rows: stratum (mild, severe); [recovered, total] for T=1 and T=0
tab = {"mild": {1: (180, 200), 0: (510, 600)}, "severe": {1: (240, 400), 0: (100, 200)}}
p = {(s, t): tab[s][t][0] / tab[s][t][1] for s in tab for t in (0, 1)}
chk("mild T=1", p["mild", 1], 0.90, 1e-12)
chk("mild T=0", p["mild", 0], 0.85, 1e-12)
chk("severe T=1", p["severe", 1], 0.60, 1e-12)
chk("severe T=0", p["severe", 0], 0.50, 1e-12)
agg = {t: sum(tab[s][t][0] for s in tab) / sum(tab[s][t][1] for s in tab) for t in (0, 1)}
chk("aggregate T=1 (420/600)", agg[1], 0.70, 1e-12)
chk("aggregate T=0 (610/800)", agg[0], 0.7625, 1e-12)
chk("aggregate difference", agg[1] - agg[0], -0.0625, 1e-12)
chk("P(severe|T=1)", 400 / 600, 2 / 3, 1e-12)
chk("P(severe|T=0)", 200 / 800, 0.25, 1e-12)
wts = {s: sum(tab[s][t][1] for t in (0, 1)) / 1400 for s in tab}
chk("P(mild)", wts["mild"], 4 / 7, 1e-12)
std = {t: sum(wts[s] * p[s, t] for s in tab) for t in (0, 1)}
chk("standardized T=1 (5.4/7)", std[1], 0.771429, 5e-7)
chk("standardized T=0 (4.9/7)", std[0], 0.700000, 5e-7)
chk("adjusted difference (1/14)", std[1] - std[0], 0.071429, 5e-7)
# decomposition of the aggregate gap: within-stratum effect at T=1 mix + composition of controls
chk("effect at treated mix (ATT)", (1 / 3) * 0.05 + (2 / 3) * 0.10, 0.083333, 5e-7)
chk("T=0 rate at treated mix", (1 / 3) * 0.85 + (2 / 3) * 0.50, 0.616667, 5e-7)
chk("composition term", (1 / 3) * 0.85 + (2 / 3) * 0.50 - 0.7625, -0.145833, 5e-7)
chk("ATT + composition", 0.083333 + -0.145833, -0.0625, 1e-6)

# ---------------------------------------------------------------- MHE Table 7.2.1 (JTPA, QTE)
print("== Q19 MHE Table 7.2.1 (JTPA): t-ratios, selection gaps, QTE vs effect quantiles")
qs = (0.15, 0.25, 0.50, 0.75, 0.85)
qr, qr_se = (1187, 2510, 4420, 4678, 4806), (205, 356, 651, 937, 1055)
qte, qte_se = (121, 702, 1544, 3131, 3378), (475, 670, 1073, 1376, 1811)
chk("t OLS", 3754 / 536, 7.004, 5e-4)
chk("t 2SLS", 1593 / 895, 1.780, 5e-4)
for q, b, s, printed in zip(qs, qr, qr_se, (5.790, 7.051, 6.790, 4.993, 4.555)):
    chk(f"t QR {q}", b / s, printed, 5e-4)
for q, b, s, printed in zip(qs, qte, qte_se, (0.255, 1.048, 1.439, 2.275, 1.865)):
    chk(f"t QTE {q}", b / s, printed, 5e-4)
chk("OLS - 2SLS", 3754 - 1593, 2161, 0)
for q, a, b, printed in zip(qs, qr, qte, (1066, 1808, 2876, 1547, 1428)):
    chk(f"QR - QTE {q}", a - b, printed, 0)
y0 = np.array([10, 20, 30, 40])
y1A, y1B = y0 + 5, np.array([45, 15, 25, 35])                # same marginal of y1 in A and B
assert sorted(y1A) == sorted(y1B)
for lab, y1 in (("A", y1A), ("B", y1B)):
    d_ = y1 - y0
    chk(f"{lab}: ATE", d_.mean(), 5, 1e-12)
    chk(f"{lab}: QTE(0.5)", np.median(y1) - np.median(y0), 5, 1e-12)
    chk(f"{lab}: median individual effect", np.median(d_), {"A": 5, "B": -5}[lab], 1e-12)
    chk(f"{lab}: share who lose", (d_ < 0).mean(), {"A": 0, "B": 0.75}[lab], 1e-12)

# ---------------------------------------------------------------- original: sharp RDD, MLDA and deaths
print("== Q20 sharp RDD at age 21 (age-mva-internal.txt); robust HC1 standard errors")
mlda = pd.read_csv(ROOT / "Aula/class-05-06/materials/age-mva-internal.txt", sep=r"\s+")
mlda["x"] = mlda["age"] - 21
mlda["D"] = (mlda["age"] >= 21).astype(int)
chk("cells", len(mlda), 48, 0)
chk("cells at or above 21", mlda["D"].sum(), 24, 0)
chk("cell width (years)", np.diff(mlda["age"]).mean(), 0.08219, 5e-5)


def rd(y, form, h=None):
    """OLS of `y` on the RD regressors in `form` within |age-21|<=h; returns (jump, HC1 se, n, fit)."""
    s = mlda if h is None else mlda[mlda["x"].abs() <= h]
    f = smf.ols(f"{y} ~ {form}", s).fit(cov_type="HC1")
    return f.params["D"], f.bse["D"], len(s), f


rho, se, _, fc = rd("mva", "D + x")
chk("MVA common slope: jump", rho, 4.534, 5e-4)
chk("MVA common slope: se", se, 0.717, 5e-4)
chk("MVA common slope: slope", fc.params["x"], -3.149, 5e-4)
chk("MVA left limit at 21", fc.params["Intercept"], 29.356, 5e-4)
chk("MVA jump / left limit", rho / fc.params["Intercept"], 0.154, 5e-4)
chk("MVA common slope: t", rho / se, 6.3, 5e-2)
chk("MVA common slope: sigma", np.sqrt(fc.mse_resid), 1.329, 5e-4)
chk("MVA jump / sigma (site)", rho / np.sqrt(fc.mse_resid), 3.411, 5e-4)
for h, (pr, ps, pn) in {2: (4.534, 0.680, 48), 1.5: (4.901, 0.819, 36),
                        1: (4.759, 1.133, 24), 0.5: (4.772, 1.457, 12)}.items():
    r, s, n, _ = rd("mva", "D + x + D:x", h)
    chk(f"MVA local linear h={h}: jump", r, pr, 5e-4)
    chk(f"MVA local linear h={h}: se", s, ps, 5e-4)
    chk(f"MVA local linear h={h}: n", n, pn, 0)
rq, sq, _, fq = rd("mva", "D + x + I(x**2) + D:x + D:I(x**2)")
chk("MVA quadratic: jump", rq, 4.663, 5e-4)
chk("MVA quadratic: se", sq, 1.093, 5e-4)
chk("MVA quadratic: jump / sigma (site)", rq / np.sqrt(fq.mse_resid), 3.508, 5e-4)
for h, (pr, ps) in {2: (0.392, 0.549), 1: (1.692, 0.762)}.items():
    r, s, _, _ = rd("internal", "D + x + D:x", h)
    chk(f"internal local linear h={h}: jump", r, pr, 5e-4)
    chk(f"internal local linear h={h}: se", s, ps, 5e-4)
chk("t at h=0.5 (4.772/1.457)", 4.772 / 1.457, 3.3, 5e-2)
chk("se ratio h=0.5 / h=2", 1.457 / 0.680, 2.14, 5e-3)
chk("internal t at h=1 (1.692/0.762)", 1.692 / 0.762, 2.2, 5e-2)
chk("internal/MVA jump at h=1", 1.692 / 4.759, 0.36, 5e-3)
ri, si, _, _ = rd("internal", "D + x + I(x**2) + D:x + D:I(x**2)")
chk("internal quadratic: jump", ri, 1.073, 5e-4)
chk("internal quadratic: se", si, 0.802, 5e-4)

print("\nALL CHECKS PASSED")
