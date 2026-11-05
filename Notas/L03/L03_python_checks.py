"""Classes 3+4 (L03) reference implementation, with assert self-checks against the decks' numbers.

Run:  python Notas/L03/L03_python_checks.py      (stops at the first failed assert; about 1 min)

Sections §1-§10 are the code blocks of L03-13-python.md, in the same order; equation numbers
"(k)" refer to the section note named in each header. Reused, not copied: the coal series and
its loader come from Notas/L01/companions/check_companions.py; the 68-women weight-gain data are
parsed at run time from the lecturer's page Aula/class-03-04/materials/hierarchical-gaussian-
linear-model.html. Every Monte Carlo draw is seeded; MC checks allow about four standard errors.
Python only: numpy, scipy, statsmodels (PyMC/ArviZ are not installed, so every sampler is
written out in NumPy).
"""
import pathlib
import re
import sys

import numpy as np
import statsmodels.api as sm
from scipy import integrate, optimize, stats
from scipy.special import betaln, gammaln, lambertw, logsumexp

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[1]
MAT = ROOT / "Aula" / "class-03-04" / "materials"
sys.path.insert(0, str(ROOT / "Notas" / "L01" / "companions"))
import check_companions as cc  # noqa: E402  coal series loaded from .agent/notes/coal-mining-data.md

sys.stdout.reconfigure(encoding="utf-8")


def near(x, printed, tol=5e-4):
    """True when x matches a printed value to `tol` (default: half a unit in the 3rd decimal)."""
    return abs(float(x) - float(printed)) <= tol


def ok(tag, **vals):
    print(f"ok  {tag:<28}" + "  ".join(f"{k}={v:.6g}" if isinstance(v, float) else f"{k}={v}"
                                       for k, v in vals.items()))


# ---------------------------------------------------------------- §1 Bayes' rule, discrete
def posterior(prior, like):
    """Bayes' rule on a finite parameter space: returns (posterior, predictive p(x)).

    prior: prior probabilities (sum to 1); like: p(x | theta_k) for the observed x.
    """
    prior, like = np.asarray(prior, float), np.asarray(like, float)
    joint = prior * like
    return joint / joint.sum(), joint.sum()


# Diego (ingredients deck, slides 5-25): theta = 1 ill. P(X=1|0)=0.40, P(X=0|1)=0.05; prior 0.70.
pX1 = np.array([0.40, 0.95])              # P(X=1 | theta=0), P(X=1 | theta=1)
pY1 = np.array([0.04, 0.99])              # second test: P(Y=1|0)=0.04, P(Y=0|1)=0.01
prior = np.array([0.30, 0.70])
post_x1, pred_x1 = posterior(prior, pX1)
post_x0, pred_x0 = posterior(prior, 1 - pX1)
post_xy, pred_y = posterior(post_x1, pY1)
post_y, _ = posterior(prior, pY1)
assert near(pred_x1, 0.785, 1e-12) and near(post_x1[1], 0.8471338, 1e-7)          # slides 12, 16
assert near(pred_x0, 0.215, 1e-12) and near(post_x0[0], 0.8372093, 1e-7)          # slide 19 prints 0.8373093
assert near(pred_y, 0.8447771, 1e-7) and near(post_xy[1], 0.992762, 1e-6)          # slides 21-22
assert near(post_y[1], 0.982979, 1e-6)                                             # slide 24
batch, _ = posterior(prior, pX1 * pY1)                                             # both tests at once
assert np.allclose(batch, post_xy)
assert near(pX1[1] / pX1[0], 2.375, 1e-12) and near((1 - pX1[0]) / (1 - pX1[1]), 12, 1e-12)  # ML ratios
ok("§1 Diego", pX1=pred_x1, post=post_x1[1], postX0=post_x0[0], postXY=post_xy[1], postY=post_y[1])

# Three coins (question0.pdf): P(head) = 0.5, 0.9, 1; uniform prior; n heads in a row.
p_head = np.array([0.5, 0.9, 1.0])
coins = {n: posterior(np.full(3, 1 / 3), p_head**n) for n in range(0, 11)}
post3, pred3 = coins[3]
assert near(pred3, 0.618, 1e-12) and np.allclose(post3, [0.0674, 0.3932, 0.5394], atol=5e-5)
post4_seq, _ = posterior(post3, p_head)                                            # update with the 4th head
assert np.allclose(post4_seq, coins[4][0])
ok("§1 three coins", P3H=pred3, c1=post3[0], c2=post3[1], c3=post3[2], c1_4=coins[4][0][0],
   c3_4=coins[4][0][2], c3_10=coins[10][0][2])

# Stone (2013), Figs 1.4 and 1.7: posterior = likelihood x prior / p(x), p(x) as printed.
assert near(0.8 * 0.1 / 0.081, 0.988) and near(0.9 * 0.001 / 0.081, 0.011)
assert near(0.6 * 0.9 / 0.61, 0.885) and near(0.7 * 0.1 / 0.61, 0.115)
two_disease, _ = posterior([0.1, 0.001], [0.8, 0.9])                               # renormalised on 2 diseases
ok("§1 Stone", chickenpox=0.8 * 0.1 / 0.081, smallpox=0.9 * 0.001 / 0.081, two_norm_c=two_disease[0])

# Discrete prior on theta (bernoulli-trials-discrete-prior.html): {0.3, 0.5, 0.8} w.p. {0.4, 0.5, 0.1}.
def discrete_theta_posterior(s, n, thetas=(0.3, 0.5, 0.8), prior=(0.4, 0.5, 0.1)):
    """Posterior over a finite set of Bernoulli probabilities after s successes in n trials."""
    t = np.asarray(thetas)
    return posterior(prior, t**s * (1 - t) ** (n - s))[0]


d40 = discrete_theta_posterior(40, 50)                                             # 80% heads in 50 trials
assert d40[2] > 0.999
ok("§1 discrete prior", s40n50_theta08=d40[2], s5n10_theta05=discrete_theta_posterior(5, 10)[1])

# ---------------------------------------------------------------- §2 conjugate updating
# Beta-Bernoulli, Greenberg Fig. 2.2: Beta(2,2) prior; n = 10, s = 3 and n = 50, s = 15.
def beta_update(a0, b0, s, n):
    """Beta(a0,b0) prior x Bernoulli likelihood with s successes in n trials -> Beta(a1,b1)."""
    return a0 + s, b0 + n - s


for (n, s, mean) in ((10, 3, 5 / 14), (50, 15, 17 / 54)):
    a1, b1 = beta_update(2, 2, s, n)
    w = (2 + 2) / (2 + 2 + n)                                                       # prior weight in (2.5)
    assert near(a1 / (a1 + b1), mean, 1e-12) and near(w * 0.5 + (1 - w) * s / n, mean, 1e-12)
a_seq = beta_update(*beta_update(2, 2, 3, 10), 12, 40)                              # 10 trials then 40 more
assert a_seq == beta_update(2, 2, 15, 50)                                          # sequential = batch
# Predictive P(y_{n+1}=1 | y) = posterior mean (G p. 33); check against the integral.
a1, b1 = beta_update(2, 2, 3, 10)
pred = integrate.quad(lambda t: t * stats.beta.pdf(t, a1, b1), 0, 1)[0]
assert near(pred, a1 / (a1 + b1), 1e-10)
# Uniform prior: mode = MLE s/n; mean (1+s)/(2+n) (sequential-bayes page).
a1, b1 = beta_update(1, 1, 1, 10)
assert near((a1 - 1) / (a1 + b1 - 2), 0.1, 1e-12) and near(a1 / (a1 + b1), 1 / 6, 1e-12)
ok("§2 beta-bernoulli", mean10=5 / 14, mean50=17 / 54, pred=pred)

# Gamma-Poisson: L01-04 coal 1851-1891 (n = 41, s = 127), Exp(1/2) = G(1, 1/2) prior.
a1, b1 = 1 + 127, 0.5 + 41
assert near(a1 / b1, 3.084) and near((a1 - 1) / b1, 3.060) and near(np.sqrt(a1) / b1, 0.273)
gmed = stats.gamma.ppf(0.5, a1, scale=1 / b1)
ok("§2 gamma-poisson (L01-04)", mean=a1 / b1, median=gmed, mode=(a1 - 1) / b1)

# Pareto-Uniform (sequential-bayes page, section 2): U(0, theta) data, Pareto(theta0, alpha0) prior.
def pareto_update(theta0, alpha0, x):
    """Pareto(theta0, alpha0) prior x U(0,theta) likelihood -> Pareto(max(theta0, x_(n)), alpha0 + n)."""
    return max(theta0, float(np.max(x))), alpha0 + len(x)


def pareto_mean(t, a):
    return a * t / (a - 1)


rng = np.random.default_rng(165431)                                                # seed of the R page; draws differ
xu = rng.uniform(0, 2, 50)
t1, al1 = pareto_update(1.5, 0.1, xu)
q = stats.pareto.ppf([0.05, 0.5, 0.95], al1, scale=t1)
assert near(q[1], t1 * 2 ** (1 / al1), 1e-10)                                      # median theta1 2^(1/alpha1)
mc = stats.pareto.rvs(al1, scale=t1, size=400_000, random_state=1).mean()
assert abs(mc - pareto_mean(t1, al1)) < 4 * t1 * np.sqrt(al1 / ((al1 - 1) ** 2 * (al1 - 2))) / np.sqrt(4e5)
assert pareto_mean(t1, al1) > t1 > t1 * al1 / (al1 + 1)                            # the page's (alpha1+1) form is below the support
ok("§2 pareto-uniform", xmax=float(xu.max()), theta1=t1, alpha1=al1, mean=pareto_mean(t1, al1),
   q05=q[0], q50=q[1], q95=q[2])

# ---------------------------------------------------------------- §3 normal measurement, four priors
SIG, X0 = 40.0, 850.0                       # x | theta ~ N(theta, 40^2), x = 850 (slides 28, 39)
PRI = {"A": (900.0, 20.0), "B": (800.0, 80.0)}


def normal_posterior(x, sig, mu0, tau0):
    """Conjugate normal update (3)-(5) of L03-03: returns (mean, sd, weight on the prior mean)."""
    w = sig**2 / (sig**2 + tau0**2)
    return w * mu0 + (1 - w) * x, np.sqrt(w * tau0**2), w


mA, sA, wA = normal_posterior(X0, SIG, *PRI["A"])
mB, sB, wB = normal_posterior(X0, SIG, *PRI["B"])
assert near(mA, 890, 1e-9) and near(sA, 17.9, 0.05) and near(mB, 840, 1e-9) and near(sB, 35.7, 0.1)
assert near(np.hypot(SIG, 20), 44.72, 0.005) and near(np.hypot(SIG, 80), 89.44, 0.005)  # predictive sd
TH = np.linspace(400, 1300, 180001)


def t_prior(th, mu=900.0, s2=240.0, nu=5):
    return stats.t.pdf((th - mu) / np.sqrt(s2), nu) / np.sqrt(s2)


def prior_D(th):
    return (stats.norm.pdf(th, 900, 20) + stats.norm.pdf(th, 800, 80) + t_prior(th)) / 3


def grid_summary(prior_vals, lo=600.0, hi=1000.0, x=X0, sig=SIG):
    """Posterior mean, median, P(theta < x), 5% quantile on [lo, hi] by quadrature on TH."""
    keep = (TH >= lo) & (TH <= hi)
    th, dens = TH[keep], (prior_vals * stats.norm.pdf(x, TH, sig))[keep]
    cdf = integrate.cumulative_trapezoid(dens, th, initial=0)
    dens, cdf = dens / cdf[-1], cdf / cdf[-1]
    return (integrate.trapezoid(th * dens, th), np.interp(0.5, cdf, th), np.interp(x, th, cdf),
            np.interp(0.05, cdf, th))


SIR = {"A": (890.06, 890.10, 0.01, 860.52), "B": (840.02, 840.09, 0.61, 781.18),   # fisicos-ABCD.html
       "C": (891.16, 892.45, 0.02, 860.30), "D": (876.15, 884.35, 0.19, 806.53)}
EXACT = {"A": grid_summary(stats.norm.pdf(TH, 900, 20)), "B": grid_summary(stats.norm.pdf(TH, 800, 80)),
         "C": grid_summary(t_prior(TH)), "D": grid_summary(prior_D(TH))}
for k, (mean, med, p, q05) in EXACT.items():
    m0, md0, p0, q0 = SIR[k]
    assert abs(mean - m0) < 0.3 and abs(med - md0) < 0.6 and abs(p - p0) < 0.006 and abs(q05 - q0) < 1.0, (k, EXACT[k])
assert near(5 / 3 * 240, 400, 1e-12)                                               # V(prior C) = V(prior A), slide 45
ok("§3 physicists", A=EXACT["A"][0], B=EXACT["B"][0], C=EXACT["C"][0], Cmed=EXACT["C"][1],
   D=EXACT["D"][0], Dmed=EXACT["D"][1], PDltx=EXACT["D"][2], sdA=sA, sdB=sB)


def post_mean_t(x):
    return grid_summary(t_prior(TH), lo=400, hi=1300, x=x)[0]


for x in (900.0, 1200.0):                       # far conflict: the t prior lets the data win
    assert abs(post_mean_t(x) - normal_posterior(x, SIG, 900, 20)[0]) < (0.5 if x == 900 else 1e9)
assert post_mean_t(1100.0) > normal_posterior(1100.0, SIG, 900, 20)[0] + 20
ok("§3 bounded influence", tmean_x1100=post_mean_t(1100.0), nmean_x1100=normal_posterior(1100.0, SIG, 900, 20)[0])

# ---------------------------------------------------------------- §4 Bayes estimators and loss
POST = stats.beta(2, 10)                        # uniform prior, n = 10, s = 1 (L01-01's sample)
mean, med, mode = POST.mean(), POST.median(), (2 - 1) / (2 + 10 - 2)
a_grid = np.linspace(0.0005, 0.6, 2400)
tq = np.linspace(0, 1, 20001)
fq = POST.pdf(tq)
quad_loss = [integrate.trapezoid((a - tq) ** 2 * fq, tq) for a in a_grid]
abs_loss = [integrate.trapezoid(np.abs(a - tq) * fq, tq) for a in a_grid]
eps = 0.01
zo_loss = [1 - (POST.cdf(a + eps) - POST.cdf(a - eps)) for a in a_grid]
assert abs(a_grid[np.argmin(quad_loss)] - mean) < 5e-4 and abs(a_grid[np.argmin(abs_loss)] - med) < 5e-4
assert abs(a_grid[np.argmin(zo_loss)] - mode) < 2e-3
assert near(min(quad_loss), POST.var(), 1e-6)                                      # minimum expected loss = V(theta|x)
qa, qb = 1.0, 3.0                                                                  # bilinear: a|.| above, b|.| below
lin_loss = [integrate.trapezoid(np.where(tq > a, qa * (tq - a), qb * (a - tq)) * fq, tq) for a in a_grid]
assert abs(a_grid[np.argmin(lin_loss)] - POST.ppf(qa / (qa + qb))) < 5e-4
ok("§4 loss functions", mean=mean, median=med, mode=mode, minquad=min(quad_loss), q25=POST.ppf(0.25))

# Exp-Gamma (notas-bayesianas slides 4-5, 13-15): theta ~ G(a0,b0), x_i ~ Exp(theta).
rng = np.random.default_rng(7)
xe = rng.exponential(1 / 2.0, 30)
a0, b0 = 2.0, 1.0
bayes, mle = (a0 + len(xe)) / (b0 + xe.sum()), len(xe) / xe.sum()
assert abs(bayes - mle) < 0.2 and near((0 + len(xe)) / (0 + xe.sum()), mle, 1e-12)  # vague prior -> MLE
# B Thm 4.4.1 / Ex. 4.4.1: uniform prior, Bernoulli, Bayes risk of (S+1)/(n+2) is 1/(6(n+2)).
n = 10
risk = lambda th: (n * th * (1 - th) + (1 - 2 * th) ** 2) / (n + 2) ** 2            # MSE of (S+1)/(n+2)
assert near(integrate.quad(risk, 0, 1)[0], 1 / (6 * (n + 2)), 1e-12)
assert integrate.quad(lambda th: th * (1 - th) / n, 0, 1)[0] > 1 / (6 * (n + 2))   # MLE's Bayes risk is larger
ok("§4 exp-gamma, Bayes risk", bayes=bayes, mle=mle, risk_bayes=1 / 72, risk_mle=1 / 60)

# Bayesian intervals (B Ex. 5.5.1; G §3.2.2): equal-tail vs HPD for Beta(2,10).
et = POST.ppf([0.025, 0.975])
res = optimize.minimize_scalar(lambda lo: POST.ppf(POST.cdf(lo) + 0.95) - lo, bounds=(0, POST.ppf(0.05)),
                               method="bounded")
hpd = (res.x, POST.ppf(POST.cdf(res.x) + 0.95))
assert hpd[1] - hpd[0] < et[1] - et[0] and near(POST.pdf(hpd[0]), POST.pdf(hpd[1]), 1e-3)
ok("§4 intervals", et_lo=et[0], et_hi=et[1], hpd_lo=hpd[0], hpd_hi=hpd[1])

# ---------------------------------------------------------------- §5 Bayes factors
def log10_bf_coins(m, s1, s2, alpha=1.0):
    """log10 B12 for M1: theta1 = theta2 vs M2: theta1 != theta2, Beta(alpha, alpha) priors (G p. 37-38)."""
    lm1 = betaln(alpha + s1 + s2, alpha + 2 * m - s1 - s2) - betaln(alpha, alpha)
    lm2 = sum(betaln(alpha + s, alpha + m - s) - betaln(alpha, alpha) for s in (s1, s2))
    return (lm1 - lm2) / np.log(10)


TABLE32 = {0.1: (-2.506, -30.775), 0.2: (-1.200, -15.793), 0.3: (-0.348, -6.316),
           0.4: (0.138, -0.975), 0.5: (0.297, 0.756)}
for p, (b10, b100) in TABLE32.items():
    for m, printed in ((10, b10), (100, b100)):
        got = log10_bf_coins(m, round(p * m), round((1 - p) * m))
        assert near(got, printed), (p, m, got, printed)
# Greenberg's own form (Gamma functions, (3.5)) equals the Beta-function form.
m, s1, s2 = 10, 2, 8
g_m1 = gammaln(s1 + s2 + 1) + gammaln(2 * m - s1 - s2 + 1) - gammaln(2 * m + 2)
g_m2 = sum(gammaln(s + 1) + gammaln(m - s + 1) - gammaln(m + 2) for s in (s1, s2))
assert near((g_m1 - g_m2) / np.log(10), log10_bf_coins(m, s1, s2), 1e-12)


def log10_bf_bic(m, s1, s2):
    """Large-sample approximation: log LR - (d1 - d2)/2 log n with n = 2m tosses (G p. 37)."""
    ll = lambda s, k: (s * np.log(s / k) if s else 0) + ((k - s) * np.log(1 - s / k) if k - s else 0)
    return (ll(s1 + s2, 2 * m) - ll(s1, m) - ll(s2, m) + 0.5 * np.log(2 * m)) / np.log(10)


ok("§5 table 3.2", m10_p01=log10_bf_coins(10, 1, 9), m100_p01=log10_bf_coins(100, 10, 90),
   m10_p05=log10_bf_coins(10, 5, 5), bic_m100_p05=log10_bf_bic(100, 50, 50), exact_m100_p05=log10_bf_coins(100, 50, 50))
# Posterior model probability with even prior odds; improper prior constants c1/c2 rescale B12 (G §4.2).
b = 10 ** log10_bf_coins(10, 2, 8)
assert near(1 / (1 + 1 / b), b / (1 + b), 1e-15)
# Three coins as three models: the marginal likelihood of "3 heads" under each coin is the likelihood itself.
assert near(0.729 / 0.125, 5.832, 1e-12)
ok("§5 coins as models", BF_c3_c1=1 / 0.125, BF_c2_c1=0.729 / 0.125, PM1_2v8=b / (1 + b))

# ---------------------------------------------------------------- §6 Monte Carlo
# pi by hit-or-miss (slides 53-56): theta = P(x^2+y^2<1) = pi/4, se of 4*theta_hat.
se = lambda M: 4 * np.sqrt(np.pi / 4 * (1 - np.pi / 4) / M)
assert near(se(1000), 0.0519, 5e-5) and near(se(10000), 0.0164, 5e-5)
rng = np.random.default_rng(12345)
u = rng.uniform(size=(10000, 2))
pi_hat = 4 * np.mean((u**2).sum(1) < 1)
assert abs(pi_hat - np.pi) < 4 * se(10000)
ok("§6 pi", se1000=se(1000), se10000=se(10000), pi_hat=pi_hat, z_deck=(3.196 - np.pi) / se(1000))

# Accept-reject, Beta(3,3) from U(0,1) (G Algorithm 5.3): c = 1.875, acceptance 1/c.
c = stats.beta.pdf(0.5, 3, 3)
assert near(c, 1.875, 1e-12) and near(1 / c, 0.5333) and near(stats.beta.pdf(0.15, 3, 3), 0.4877, 5e-5)
rng = np.random.default_rng(1)
u1, u2 = rng.uniform(size=(2, 200_000))
acc = u2 <= stats.beta.pdf(u1, 3, 3) / c
assert abs(acc.mean() - 1 / c) < 4 * np.sqrt(0.5333 * 0.4667 / 2e5)
assert abs(u1[acc].mean() - 0.5) < 0.003 and abs(u1[acc].var() - 1 / 28) < 0.0008  # Beta(3,3): var 1/28
# N(0,1) from a Laplace proposal (G Algorithm 5.4): with the normalised target c = sqrt(2e/pi).
c_norm = np.sqrt(2 * np.e / np.pi)
assert near(c_norm, 1.3155, 5e-5) and near(np.sqrt(np.e / (2 * np.pi)), 0.6577, 5e-5)
rng = np.random.default_rng(2)
xL, uL = rng.exponential(size=200_000), rng.uniform(size=200_000)
accL = uL <= np.exp(xL - xL**2 / 2 - 0.5)                                          # Greenberg's test (5.2)
assert abs(accL.mean() - 1 / c_norm) < 0.004 and abs(accL.mean() - 0.6577) > 0.09   # 0.760, not 0.6577
assert abs(np.mean(xL[accL] ** 2) - 1) < 0.01
ok("§6 accept-reject", c_beta=c, acc_beta=acc.mean(), c_norm=c_norm, acc_norm=accL.mean())

# Importance sampling (G Algorithm 5.5): E[(1+x^2)^-1], x ~ Exp(1) truncated to [0,1]; h = Beta(2,3).
exact = integrate.quad(lambda x: np.exp(-x) / (1 + x**2), 0, 1)[0] / (1 - np.exp(-1))
rng = np.random.default_rng(3)
xb = rng.beta(2, 3, 10_000)
wts = np.exp(-xb) / (1 - np.exp(-1)) / stats.beta.pdf(xb, 2, 3)
g_is = np.mean(wts / (1 + xb**2))
se_is = np.std(wts / (1 + xb**2), ddof=1) / 100
# h(x) = 12x(1-x)^2 vanishes at 0 where f g does not: E_h[(f g / h)^2] = int f^2 g^2 / h diverges like log,
# so the estimator has infinite variance and its printed se (here and in G p. 71) is not reliable.
var_dens = lambda x: (np.exp(-x) / (1 - np.exp(-1)) / (1 + x**2)) ** 2 / stats.beta.pdf(x, 2, 3)
growth = integrate.quad(lambda t: var_dens(np.exp(t)) * np.exp(t), np.log(1e-8), np.log(1e-4))[0]                                           # ~ f(0)^2/12 * log(1e4)
assert near(exact, 0.8302) and abs(g_is - exact) < 0.05
assert abs(growth - (1 / (1 - np.exp(-1))) ** 2 / 12 * np.log(1e4)) < 0.01
ok("§6 importance sampling", exact=exact, estimate=g_is, se_printed=se_is, var_growth=growth)

# Composition: t_nu as a normal scale mixture (G §4.5, §5.2).
rng = np.random.default_rng(4)
lam = rng.gamma(5 / 2, 2 / 5, 400_000)                                             # G(nu/2, nu/2), rate nu/2
tdraw = rng.normal(0, 1 / np.sqrt(lam))
assert abs(np.var(tdraw) - 5 / 3) < 0.03 and abs(np.mean(np.abs(tdraw) > 2.571) - 0.05) < 0.002
ok("§6 composition t5", var=float(np.var(tdraw)), tail=float(np.mean(np.abs(tdraw) > 2.571)))

# SIR (MS §B.6.2; fisicos-ABCD.html): physicist C's posterior from U(600,1000) proposals.
rng = np.random.default_rng(125532)
th = rng.uniform(600, 1000, 1_000_000)
w = stats.norm.pdf(X0, th, SIG) * t_prior(th)
draws = rng.choice(th, size=1_000_000, p=w / w.sum())
assert abs(draws.mean() - EXACT["C"][0]) < 0.15
ess = w.sum() ** 2 / (w**2).sum()
ok("§6 SIR physicist C", mean=float(draws.mean()), exact=EXACT["C"][0], ess=float(ess))

# Zero-inflated Poisson (ZIP-fishing.html): the frequency table gives 45 groups, not 42.
counts = {0: 24, 1: 6, 2: 2, 3: 4, 4: 2, 5: 3, 7: 1, 8: 1, 14: 1, 16: 1}
yz = np.repeat(list(counts), list(counts.values()))
n, n0, ybar, s2 = len(yz), int((yz == 0).sum()), yz.mean(), yz.var(ddof=1)
zbar = yz.sum() / (n - n0)
lam_mle = float(np.real(lambertw(-zbar * np.exp(-zbar)))) + zbar
pi_mle = 1 - ybar / lam_mle
lam_mm, pi_mm = (s2 + ybar**2) / ybar - 1, (s2 - ybar) / (s2 + ybar**2 - ybar)
assert n == 45 and near(lam_mle, 4.223) and near(pi_mle, 0.526) and near(lam_mm, 7.159) and near(pi_mm, 0.721)
assert near(lam_mle / (1 - np.exp(-lam_mle)), zbar, 1e-10)                         # the score equation


def zip_loglik(lam, pi):
    """ZIP log-likelihood: n0 log(pi + (1-pi)e^-lam) + (n-n0)[log(1-pi) - lam] + sum(y) log(lam) + const."""
    return n0 * np.log(pi + (1 - pi) * np.exp(-lam)) + (n - n0) * (np.log(1 - pi) - lam) + yz.sum() * np.log(lam)


L, P = np.meshgrid(np.linspace(1, 8, 701), np.linspace(0.1, 0.9, 801), indexing="ij")
lw = zip_loglik(L, P)
wz = np.exp(lw - lw.max())
wz /= wz.sum()
zip_post = (float((wz * L).sum()), float((wz * P).sum()))
ok("§6 ZIP", n=n, lam_mle=lam_mle, pi_mle=pi_mle, lam_mm=lam_mm, pi_mm=pi_mm, Elam=zip_post[0], Epi=zip_post[1])

# Correlation coefficient (correlationcoefficient.html): 14 standardised height/weight pairs.
hw = np.array([178, 70, 175, 80, 184, 82, 200, 89, 183, 80, 173, 65, 185, 70, 162, 70, 190, 85,
               174, 80, 180, 87, 165, 74, 176, 72, 174, 63, 197, 120], float).reshape(15, 2)[:14]
z = (hw - hw.mean(0)) / hw.std(0, ddof=1)
S11, S12 = (z**2).sum(), (z[:, 0] * z[:, 1]).sum()
rho = np.linspace(-0.9999, 0.9999, 200001)
loglik_rho = -len(z) / 2 * np.log(1 - rho**2) - (S11 - 2 * rho * S12) / (2 * (1 - rho**2))


def rho_quantiles(logprior):
    lp = loglik_rho + logprior
    d = np.exp(lp - lp.max())
    cdf = integrate.cumulative_trapezoid(d, rho, initial=0)
    return np.interp([0.025, 0.5, 0.975], cdf / cdf[-1], rho)


q_unif = rho_quantiles(0 * rho)
q_page = rho_quantiles(-0.5 * np.log(1 + rho**2))                                  # what the page codes
q_arcs = rho_quantiles(-0.5 * np.log(1 - rho**2))                                  # the stated arc-sine prior
assert np.allclose(q_unif, [0.102, 0.569, 0.784], atol=0.015)
assert np.allclose(q_page, [0.081, 0.558, 0.783], atol=0.015)
ok("§6 correlation", r=float(np.corrcoef(z.T)[0, 1]), unif=str(np.round(q_unif, 3)),
   page=str(np.round(q_page, 3)), arcsine=str(np.round(q_arcs, 3)))

# ---------------------------------------------------------------- §7 Markov chains and Gibbs
P2 = np.array([[0.750, 0.250], [0.125, 0.875]])                                    # G (6.2)
evals, evecs = np.linalg.eig(P2.T)
pi_inv = np.real(evecs[:, np.argmax(np.real(evals))])
pi_inv /= pi_inv.sum()
assert np.allclose(pi_inv, [1 / 3, 2 / 3]) and np.allclose(pi_inv @ P2, pi_inv)
assert np.allclose(np.linalg.matrix_power(P2, 10), [[0.339, 0.661], [0.330, 0.670]], atol=5e-4)
assert np.allclose(np.linalg.matrix_power(P2, 20), [[1 / 3, 2 / 3]] * 2, atol=5e-4)
assert near(sorted(np.real(evals))[0], 0.625, 1e-12)                               # second root 1 - 0.25 - 0.125
ok("§7 two-state chain", pi1=pi_inv[0], P10_11=np.linalg.matrix_power(P2, 10)[0, 0], root2=0.625)
# AR(1) has invariant density N(0, s^2/(1-phi^2)) (G pp. 85-86): one step of the kernel preserves it.
phi, s_ar = 0.9, 1.0
v_inv = s_ar**2 / (1 - phi**2)
assert near(phi**2 * v_inv + s_ar**2, v_inv, 1e-12)


def gibbs_normal(y, mu0, h0, a0, d0, G, B, seed):
    """Algorithm 7.3: y_i ~ N(mu, 1/h), mu ~ N(mu0, 1/h0), h ~ G(a0/2, d0/2); returns (mu, h) draws."""
    rng = np.random.default_rng(seed)
    n, yb, mu = len(y), y.mean(), y.mean()
    out = np.empty((G, 2))
    for g in range(B + G):
        h = rng.gamma((a0 + n) / 2, 2 / (d0 + ((y - mu) ** 2).sum()))
        mu = rng.normal((h0 * mu0 + h * n * yb) / (h0 + h * n), 1 / np.sqrt(h0 + h * n))
        if g >= B:
            out[g - B] = mu, h
    return out


rng = np.random.default_rng(100)
yn = rng.normal(1.6, 0.2, 100)                                                     # exemplo1 data design (Stan file)
gn = gibbs_normal(yn, 1.7, 1 / 0.3**2, 2.0, 2 * 0.04, 5000, 1000, seed=101)
assert abs(gn[:, 0].mean() - yn.mean()) < 0.01 and abs(1 / np.sqrt(gn[:, 1].mean()) - yn.std()) < 0.02
ok("§7 normal mean-precision", mu=float(gn[:, 0].mean()), ybar=float(yn.mean()), sigma=float(1 / np.sqrt(gn[:, 1].mean())))

# Switch point (G (7.3)-(7.4)) on the coal data, with the L01-04 prior G(1, 1/2) for both rates.
Y, YEARS = cc.Y, cc.YEARS
N, S = len(Y), np.cumsum(Y)
A0, B0 = 1.0, 0.5
k = np.arange(1, N + 1)


def switch_exact_logpost():
    """log p(k | y), k = 1..n, rates integrated out analytically (gamma integrals); uniform prior on k."""
    Sk, Rk = S, S[-1] - S
    return (gammaln(A0 + Sk) - (A0 + Sk) * np.log(B0 + k) + gammaln(A0 + Rk) - (A0 + Rk) * np.log(B0 + N - k))


lpk = switch_exact_logpost()
pk = np.exp(lpk - logsumexp(lpk))


def gibbs_switch(G, B, seed):
    """Three-block Gibbs for (lambda1, lambda2, k): two gamma draws and one discrete draw per sweep."""
    rng = np.random.default_rng(seed)
    kk, out = N // 2, np.empty((G, 3))
    for g in range(B + G):
        l1 = rng.gamma(A0 + S[kk - 1], 1 / (B0 + kk))
        l2 = rng.gamma(A0 + S[-1] - S[kk - 1], 1 / (B0 + N - kk))
        lp = k * (l2 - l1) + S * np.log(l1 / l2)
        kk = rng.choice(k, p=np.exp(lp - logsumexp(lp)))
        if g >= B:
            out[g - B] = l1, l2, kk
    return out


gs = gibbs_switch(20000, 1000, seed=31415)
freq = np.bincount(gs[:, 2].astype(int), minlength=N + 1)[1:] / len(gs)
tv = 0.5 * np.abs(freq - pk).sum()
kmode = int(k[np.argmax(pk)])
assert YEARS[kmode - 1] == 1891 and tv < 0.03
E_l1 = float((pk * (A0 + S) / (B0 + k)).sum())
E_l2 = float((pk * (A0 + S[-1] - S) / (B0 + N - k)).sum())
assert abs(gs[:, 0].mean() - E_l1) < 0.02 and abs(gs[:, 1].mean() - E_l2) < 0.01
win = (YEARS >= 1886) & (YEARS <= 1896)
ok("§7 switch point", mode_year=int(YEARS[kmode - 1]), p_mode=float(pk.max()), p_1886_96=float(pk[win].sum()),
   E_l1=E_l1, E_l2=E_l2, gibbs_l1=float(gs[:, 0].mean()), gibbs_l2=float(gs[:, 1].mean()), TV=float(tv))


def acf(x, lags):
    x = x - x.mean()
    return np.array([np.dot(x[:-h], x[h:]) / np.dot(x, x) if h else 1.0 for h in lags])


def batch_nse(x, nb=100):
    """Numerical standard error by batch means (G §7.3): sd of batch means / sqrt(number of batches)."""
    bm = x[: len(x) // nb * nb].reshape(nb, -1).mean(1)
    return bm.std(ddof=1) / np.sqrt(nb)


def gibbs_binormal(rho, G, x2_0, seed):
    """Two-block Gibbs for N2(0, [[1, rho], [rho, 1]]) (G p. 94): x1 | x2 ~ N(rho x2, 1 - rho^2)."""
    rng = np.random.default_rng(seed)
    x2, out, sd = x2_0, np.empty(G), np.sqrt(1 - rho**2)
    for g in range(G):
        x1 = rng.normal(rho * x2, sd)
        x2 = rng.normal(rho * x1, sd)
        out[g] = x1
    return out


for rho_ in (0.5, 0.9):
    ch = gibbs_binormal(rho_, 200_000, -2.0, seed=5)
    assert abs(acf(ch, [1])[0] - rho_**2) < 0.01
    iff = (1 + rho_**2) / (1 - rho_**2)
    assert abs(batch_nse(ch) ** 2 * len(ch) / ch.var() - iff) / iff < 0.25
assert 0.5**6 < 0.05 < 0.5**4 and 0.999 ** 40 > 0.9                               # G p. 103: lag 3 vs lag 20
ok("§7 Gibbs mixing", lag1_rho05=0.25, IF_rho05=(1 + 0.25) / (1 - 0.25), IF_rho0999=(1 + 0.998001) / (1 - 0.998001))

# ---------------------------------------------------------------- §8 Metropolis-Hastings
def mh_independence_beta34(G, B, seed):
    """Algorithm 7.5: target Beta(3,4) kernel, U(0,1) independence proposal; returns draws, acceptance."""
    rng = np.random.default_rng(seed)
    x, out, nacc = 0.5, np.empty(G), 0
    for g in range(B + G):
        y, u = rng.uniform(), rng.uniform()
        if u <= (y**2 * (1 - y) ** 3) / (x**2 * (1 - x) ** 3):
            x, nacc = y, nacc + (g >= B)
        if g >= B:
            out[g - B] = x
    return out, nacc / G


mh, acc_rate = mh_independence_beta34(5000, 500, seed=6)
f34 = stats.beta(3, 4).pdf
tg = np.linspace(0, 1, 2001)
acc_exact = integrate.trapezoid(integrate.trapezoid(np.minimum.outer(f34(tg), f34(tg)), tg), tg)  # E min(1, f(y)/f(x))
assert near(acc_exact, 0.57, 0.01) and abs(acc_rate - acc_exact) < 0.03 and abs(mh.mean() - 3 / 7) < 0.015
ok("§8 independence MH", acc_exact=acc_exact, acc_sim=acc_rate, mean=float(mh.mean()), true=3 / 7)


def rw_accept_exact(s):
    """Stationary acceptance of random-walk MH, N(0,1) target, N(0,s^2) increments: (2/pi) arctan(2/s)."""
    return 2 / np.pi * np.arctan(2 / s)


def rw_mh_normal(s, G, seed):
    rng = np.random.default_rng(seed)
    x, out, nacc = 0.0, np.empty(G), 0
    for g in range(G):
        y = x + s * rng.normal()
        if np.log(rng.uniform()) <= (x**2 - y**2) / 2:
            x, nacc = y, nacc + 1
        out[g] = x
    return out, nacc / G


for s_ in (0.5, 2.38, 8.0):
    ch, a = rw_mh_normal(s_, 200_000, seed=8)
    xg, ug = np.linspace(-9, 9, 1801), np.linspace(-9 * s_, 9 * s_, 3601)        # E min(1, f(x+u)/f(x))
    XG, UG = np.meshgrid(xg, ug, indexing="ij")
    integrand = np.minimum(1, np.exp((XG**2 - (XG + UG) ** 2) / 2)) * stats.norm.pdf(XG) * stats.norm.pdf(UG, 0, s_)
    num = integrate.trapezoid(integrate.trapezoid(integrand, ug, axis=1), xg)
    assert near(num, rw_accept_exact(s_), 2e-4) and abs(a - rw_accept_exact(s_)) < 0.006
assert near(rw_accept_exact(2.38), 0.4449, 5e-5)
ok("§8 random-walk MH", acc_s05=rw_accept_exact(0.5), acc_s238=rw_accept_exact(2.38), acc_s8=rw_accept_exact(8.0))

# Bayesian logit by random-walk MH with a tailored scale (G §8.2.3), on seeded data: posterior ~ MLE.
rng = np.random.default_rng(9)
nl = 2000
Xl = np.column_stack([np.ones(nl), rng.normal(0, 1, nl), rng.binomial(1, 0.5, nl)])
yl = rng.binomial(1, 1 / (1 + np.exp(-(Xl @ np.array([-1.0, 0.8, 0.5])))))
glm = sm.Logit(yl, Xl).fit(disp=0)


def log_post_logit(b, B0inv=np.eye(3) / 100):
    eta = Xl @ b
    return yl @ eta - np.logaddexp(0, eta).sum() - 0.5 * b @ B0inv @ b             # N(0, 100 I) prior


Lch = np.linalg.cholesky(glm.cov_params() * 2.38**2 / 3)
b, lp, draws_l, nacc = glm.params.copy(), log_post_logit(glm.params), np.empty((10000, 3)), 0
for g in range(11000):
    prop = b + Lch @ rng.normal(size=3)
    lpp = log_post_logit(prop)
    if np.log(rng.uniform()) <= lpp - lp:
        b, lp, nacc = prop, lpp, nacc + 1
    if g >= 1000:
        draws_l[g - 1000] = b
assert np.allclose(draws_l.mean(0), glm.params, atol=0.03) and 0.2 < nacc / 11000 < 0.5
ok("§8 logit RW-MH", mle=str(np.round(glm.params, 3)), post=str(np.round(draws_l.mean(0), 3)), acc=nacc / 11000)
# The site page (Bayesian-logistic-regression.html): GLM vs UPG posterior means, slope ratio.
assert near(-10.82 / -11.304484, 0.957, 5e-4) and near(3.82 / 4.055082, 0.942, 5e-4)

# ---------------------------------------------------------------- §9 hierarchical models
YH = np.array([4, 1, 18, 7, 24, 16, 6, 19, 15, 13, 25, 11, 4])
NH = np.array([129, 35, 228, 84, 291, 270, 46, 293, 241, 105, 353, 250, 41])
assert YH.sum() == 163 and NH.sum() == 2366 and near(6 / 46, 0.13043, 5e-6) and near(1 / 35, 0.02857, 5e-6)
MU = np.linspace(0.0005, 0.25, 1000)
LE = np.linspace(np.log(0.5), np.log(1e7), 1400)                                   # grid on log(eta)
MM, EE = np.meshgrid(MU, np.exp(LE), indexing="ij")
a_, b_ = MM * EE, (1 - MM) * EE
loglik_h = sum(betaln(a_ + yi, b_ + ni - yi) - betaln(a_, b_) for yi, ni in zip(YH, NH))
logprior_h = np.log(10) - 2 * np.log(10 + EE) + np.log(EE)                         # p(eta) d eta, in log eta
lpost = loglik_h + logprior_h
wh = np.exp(lpost - lpost.max())
wh /= wh.sum()


def grid_quantile(vals, weights, qs):
    o = np.argsort(vals.ravel())
    cw = np.cumsum(weights.ravel()[o])
    return np.interp(qs, cw, vals.ravel()[o])


q_mu = grid_quantile(MM, wh, [0.05, 0.5, 0.95])
q_eta = grid_quantile(EE, wh, [0.05, 0.5, 0.95])
sd_beta = np.sqrt(a_ * b_ / (EE**2 * (EE + 1)))
q_sd = grid_quantile(sd_beta, wh, [0.05, 0.5, 0.95])
Ep = np.array([(wh * (a_ + yi) / (EE + ni)).sum() for yi, ni in zip(YH, NH)])
assert np.allclose(q_mu, [0.0595, 0.0715, 0.0874], atol=0.0015)                   # Stan, page section 6
assert abs(q_eta[1] / 225.7 - 1) < 0.15 and abs(q_sd[1] - 0.0170) < 0.0015
Emu = float((wh * MM).sum())
assert np.all(np.abs(Ep - Emu) <= np.abs(YH / NH - Emu) + 1e-12) and Ep.std() < (YH / NH).std() / 2  # shrinkage
ok("§9 beta-binomial grid", mu=str(np.round(q_mu, 4)), eta=str(np.round(q_eta, 1)), sd=str(np.round(q_sd, 4)),
   Ep_roosevelt=float(Ep[6]), Ep_harlem=float(Ep[1]), pooled=YH.sum() / NH.sum(), Emu=Emu,
   sd_phat=float((YH / NH).std()), sd_Ep=float(Ep.std()))

# Hierarchical Gaussian linear model (hierarchical-gaussian-linear-model.html): parse the page's data.
page = (MAT / "hierarchical-gaussian-linear-model.html").read_text(encoding="utf-8")


def r_matrix(name):
    """Read `name <- matrix(c(...),7,68)` from the page's R code (column-major, NA allowed)."""
    body = re.search(rf"{name} &lt;- matrix\(c\((.*?)\),7,68\)", page, re.S).group(1)
    vals = [np.nan if v.strip() == "NA" else float(v) for v in body.replace("\n", " ").split(",")]
    return np.array(vals).reshape(68, 7)                                           # row i = woman i


yw, xw = r_matrix("y"), r_matrix("x")
nobs = (~np.isnan(yw)).sum(1)
assert nobs.sum() == 427 and np.bincount(nobs)[5:].tolist() == [8, 33, 27]
rows = [(np.column_stack([np.ones(m), xw[i, :m]]), yw[i, :m]) for i, m in enumerate(nobs)]
Xp, yp = np.vstack([r[0] for r in rows]), np.concatenate([r[1] for r in rows])
ols = sm.OLS(yp, Xp).fit()
assert near(ols.params[0], -4.526386, 5e-6) and near(ols.params[1], 0.476334, 5e-6) and near(np.sqrt(ols.scale), 3.611520, 5e-6)


def gibbs_hier_gauss(G, B, seed, Pa=1.0, Pb=1.0, a=1.0, b=1.0):
    """Random-coefficient Gibbs: (alpha_i, beta_i) | . ~ N2; alpha, beta | . ~ N; tau's ~ G; sigma2 ~ IG."""
    rng = np.random.default_rng(seed)
    I, n = len(rows), len(yp)
    XtX = [X.T @ X for X, _ in rows]
    Xty = [X.T @ yv for X, yv in rows]
    ind = np.array([[np.polyfit(X[:, 1], yv, 1)[::-1] for X, yv in rows]])[0]
    al, be = ind[:, 0].mean(), ind[:, 1].mean()
    ta, tb, s2 = 1 / ind[:, 0].var(ddof=1), 1 / ind[:, 1].var(ddof=1), ols.scale
    out = np.empty((G, 5))
    coef = np.empty((I, 2))
    for g in range(B + G):
        iA = np.diag([ta, tb])
        for i in range(I):
            V = np.linalg.inv(iA + XtX[i] / s2)
            coef[i] = V @ (iA @ [al, be] + Xty[i] / s2) + np.linalg.cholesky(V) @ rng.normal(size=2)
        al = rng.normal(ta * coef[:, 0].sum() / (ta * I + Pa), 1 / np.sqrt(ta * I + Pa))
        be = rng.normal(tb * coef[:, 1].sum() / (tb * I + Pb), 1 / np.sqrt(tb * I + Pb))
        ta = rng.gamma(a + I / 2, 1 / (b + ((coef[:, 0] - al) ** 2).sum() / 2))
        tb = rng.gamma(a + I / 2, 1 / (b + ((coef[:, 1] - be) ** 2).sum() / 2))
        rss = sum(((yv - X @ cf) ** 2).sum() for (X, yv), cf in zip(rows, coef))
        s2 = 1 / rng.gamma(a + n / 2, 1 / (b + rss / 2))
        if g >= B:
            out[g - B] = al, be, 1 / np.sqrt(ta), 1 / np.sqrt(tb), np.sqrt(s2)
    return out


hg = gibbs_hier_gauss(3000, 500, seed=2025)
med_hg = np.median(hg, 0)
assert abs(med_hg[1] - ols.params[1]) < 0.03 and med_hg[4] < np.sqrt(ols.scale)    # within-woman sd < pooled sd
ok("§9 hierarchical gaussian", alpha=med_hg[0], beta=med_hg[1], sd_alpha=med_hg[2], sd_beta=med_hg[3], sigma=med_hg[4])

# ---------------------------------------------------------------- §10 sparsity priors
def shrink_normal(y, v=1.0):
    return y * v / (1 + v)                                                          # y ~ N(theta,1), theta ~ N(0,v)


def shrink_laplace(y, b=1 / np.sqrt(2)):
    """E(theta | y) for y ~ N(theta, 1), theta ~ Laplace(0, b) (variance 2b^2), by quadrature."""
    f = lambda t, p: t**p * stats.norm.pdf(y - t) * np.exp(-abs(t) / b)
    return integrate.quad(f, -30, 30, args=(1,), points=[0, y])[0] / integrate.quad(f, -30, 30, args=(0,), points=[0, y])[0]


def shrink_horseshoe(y, tau=1.0):
    """E(theta | y) = y (1 - E(kappa | y)), kappa = 1/(1 + tau^2 lambda^2), lambda ~ C+(0,1), sigma = 1."""
    # prior p(kappa) propto kappa^{-1/2}(1-kappa)^{-1/2} / (1 - kappa + tau^2 kappa); p(y | kappa) propto
    # kappa^{1/2} exp(-kappa y^2/2); the (1-kappa)^{-1/2} factor goes to quad's algebraic weight.
    g = lambda kp, p: kp**p * np.exp(-kp * y**2 / 2) / (1 - kp + tau**2 * kp)
    num = integrate.quad(lambda kp: g(kp, 1), 0, 1, weight="alg", wvar=(0, -0.5))[0]
    den = integrate.quad(lambda kp: g(kp, 0), 0, 1, weight="alg", wvar=(0, -0.5))[0]
    return y * (1 - num / den)


for yy in (0.5, 2.0, 6.0):                                                          # tau = 1: Be(1/2,1/2) on kappa
    lam_ = stats.halfcauchy.rvs(size=400_000, random_state=11)
    kap = 1 / (1 + lam_**2)
    wk = np.sqrt(kap) * np.exp(-kap * yy**2 / 2)
    assert abs(shrink_horseshoe(yy) - yy * (1 - (wk * kap).sum() / wk.sum())) < 0.02
assert abs(shrink_horseshoe(8.0) - 8.0) < 0.35 and abs(shrink_horseshoe(0.5)) < 0.2
assert abs(shrink_laplace(8.0) - (8.0 - np.sqrt(2))) < 0.05                         # Laplace: constant pull 1/b = sqrt(2)
kap = 1 / (1 + stats.halfcauchy.rvs(size=400_000, random_state=12) ** 2)
assert abs(np.mean(kap < 0.1) - stats.beta.cdf(0.1, 0.5, 0.5)) < 0.003            # kappa ~ Be(1/2, 1/2)
ok("§10 shrinkage profiles", hs_y2=shrink_horseshoe(2.0), hs_y6=shrink_horseshoe(6.0), lap_y2=shrink_laplace(2.0),
   lap_y6=shrink_laplace(6.0), nor_y2=shrink_normal(2.0))
# Normal-gamma (Griffin & Brown 2010): beta | Psi ~ N(0, Psi), Psi ~ Ga(lambda, 1/(2 gamma^2)).
lam_ng, gam = 0.333, 1 / np.sqrt(2 * 0.333)                                         # variance 2 lambda gamma^2 = 1
psi = stats.gamma.rvs(lam_ng, scale=2 * gam**2, size=2_000_000, random_state=13)
bng = np.random.default_rng(14).normal(0, np.sqrt(psi))
assert abs(bng.var() - 2 * lam_ng * gam**2) < 0.02 and abs(stats.kurtosis(bng) - 3 / lam_ng) / (3 / lam_ng) < 0.15
ok("§10 normal-gamma", var=float(bng.var()), ex_kurt=float(stats.kurtosis(bng)), theory=3 / lam_ng)


def gibbs_sparse(X, y, prior, G, B, seed):
    """Gibbs for y = X beta + e: ridge (beta_j ~ N(0, s2 tau2)), Bayesian lasso (Park-Casella, exponential
    mixing with a G(1, 0.1) prior on lambda^2) or horseshoe (Makalic-Schmidt auxiliary variables)."""
    rng = np.random.default_rng(seed)
    n, p = X.shape
    XtX, Xty = X.T @ X, X.T @ y
    beta, s2, tau2, lam2, nu, xi, l2 = np.zeros(p), 1.0, 1.0, np.ones(p), np.ones(p), 1.0, 1.0
    out = np.empty((G, p))
    ig = lambda shape, scale: scale / rng.gamma(shape, size=np.shape(scale))   # one gamma per coordinate
    for g in range(B + G):
        dinv = {"ridge": np.full(p, 1 / tau2), "lasso": 1 / lam2, "horseshoe": 1 / (tau2 * lam2)}[prior]
        Lc = np.linalg.cholesky(XtX + np.diag(dinv))
        mean = np.linalg.solve(Lc.T, np.linalg.solve(Lc, Xty))
        beta = mean + np.sqrt(s2) * np.linalg.solve(Lc.T, rng.normal(size=p))
        rss = ((y - X @ beta) ** 2).sum()
        s2 = ig((n + p) / 2, (rss + (beta**2 * dinv).sum()) / 2)
        if prior == "ridge":
            tau2 = ig((p + 1) / 2, 1 / xi + (beta**2).sum() / (2 * s2))
            xi = ig(1, 1 + 1 / tau2)
        elif prior == "lasso":
            lam2 = 1 / rng.wald(np.sqrt(l2 * s2 / beta**2), l2)
            l2 = rng.gamma(1 + p, 1 / (0.1 + lam2.sum() / 2))
        else:
            lam2 = ig(1, 1 / nu + beta**2 / (2 * tau2 * s2))
            tau2 = ig((p + 1) / 2, 1 / xi + (beta**2 / lam2).sum() / (2 * s2))
            nu, xi = ig(1, 1 + 1 / lam2), ig(1, 1 + 1 / tau2)
        if g >= B:
            out[g - B] = beta
    return out


rng = np.random.default_rng(123456)                                                # sparseregression-simulation-R.txt design
nS, kmax = 200, 100
X1 = rng.normal(size=(nS, kmax))
beta_true = np.r_[1, 2, 3, np.zeros(kmax - 3)]
yS = X1 @ beta_true + rng.normal(0, 0.1, nS)
spread = {}
for kk in (10, 50):
    X = X1[:, :kk]
    for pr in ("ridge", "lasso", "horseshoe"):
        dr = gibbs_sparse(X, yS, pr, 1500, 500, seed=kk)
        pm = dr.mean(0)
        assert np.allclose(pm[:3], [1, 2, 3], atol=0.03), (kk, pr, pm[:3])
        spread[(kk, pr)] = float(np.median(np.abs(pm[3:])))
assert spread[(50, "horseshoe")] < spread[(50, "ridge")]
ok("§10 sparse regression", **{f"k{kk}_{pr}": v for (kk, pr), v in spread.items()})

# ---------------------------------------------------------------- §11 numbers of the L03-12 self-test
post_f, pred_f = posterior([0.99, 0.01], [0.03, 0.98])                            # Block A: fraud filter
odds2 = 0.01 / 0.99 * (0.98 / 0.03) ** 2
odds_2pct = 0.02 / 0.98 * 0.98 / 0.03
assert near(post_f[1], 0.248) and near(pred_f, 0.0395, 1e-12) and near(odds2 / (1 + odds2), 0.915)
assert near(odds_2pct / (1 + odds_2pct), 0.400)
b8 = stats.beta(8, 32)                                                              # Block B: Beta(2,8) + 6 of 30
assert near(b8.mean(), 0.200, 1e-12) and near(b8.median(), 0.195) and near(7 / 38, 0.184)
s2t = 0.25 * 3 / 5                                                                  # Block C: N(4, 0.5^2), x = 6
tt = np.linspace(-10, 20, 300001)
dt = stats.t.pdf((tt - 4) / np.sqrt(s2t), 5) / np.sqrt(s2t) * stats.norm.pdf(6, tt, 1)
t_mean = integrate.trapezoid(tt * dt, tt) / integrate.trapezoid(dt, tt)
assert near(normal_posterior(6, 1, 4, 0.5)[0], 4.4, 1e-12) and near(t_mean, 4.387)
bf_c = stats.norm.pdf(6, 4, 1) / stats.norm.pdf(6, 4, np.sqrt(1.25))
bf_d = stats.norm.pdf(6, 4, 1) / stats.norm.pdf(6, 4, np.sqrt(1 + 100**2))
assert near(bf_c, 0.75, 5e-3) and near(bf_d, 13.5, 0.05)
assert near((1 + 0.95**2) / (1 - 0.95**2), 19.5, 0.02)                             # Block D
ok("§11 self-test", fraud=post_f[1], two_flags=odds2 / (1 + odds2), median=b8.median(), t_mean=t_mean,
   bf=bf_c, bf_diffuse=bf_d)

print("\nALL L03 CHECKS PASSED")
