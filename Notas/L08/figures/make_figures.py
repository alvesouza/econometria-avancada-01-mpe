"""Figures for the Class 8 notes (Notas/L08). Run: python Notas/L08/figures/make_figures.py

build() writes eight PNGs beside this file and asserts at least one plotted number per figure.
Every curve is the model's exact expression; the one simulation (the Dickey-Fuller density) is
seeded and says so in its title.

Sources: ar-ma.pdf slides 18-52; ar2-forecast.html; unitroot.pdf; seasonal.pdf;
garchmodeling.html; GARCH11-SVar1.html; Tsay AFTS 3e Ch. 2 (pp. 40-103) and Ch. 3 (pp. 110-166);
Wooldridge 6e Table 18.2 (p. 575). Numbers: .agent/plans/notas-L08.md "Numbers fixed".
"""
import math
import pathlib
import sys

import numpy as np
from scipy import stats

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))
from _figstyle import C, apply, save  # noqa: E402

import matplotlib.pyplot as plt  # noqa: E402


# ---------- shared model functions ----------
def ar2_acf(p1, p2, k):
    """Theoretical ACF rho_0..rho_k of a stationary AR(2): T eq. (2.13), rho_1 = p1/(1-p2)."""
    r = np.empty(k + 1)
    r[0], r[1] = 1.0, p1 / (1 - p2)
    for j in range(2, k + 1):
        r[j] = p1 * r[j - 1] + p2 * r[j - 2]
    return r


def ar2_gamma0(p1, p2, s2=1.0):
    """Stationary variance of an AR(2) (ar-ma.pdf slide 19; ar2-forecast.html, corrected form)."""
    return (1 - p2) * s2 / ((1 + p2) * ((1 - p2) ** 2 - p1 ** 2))


def cycle_length(p1, p2):
    """Average cycle length 2*pi/acos(p1/(2 sqrt(-p2))) for complex roots (T p. 42)."""
    return 2 * math.pi / math.acos(p1 / (2 * math.sqrt(-p2)))


def pacf_from_acf(rho, kmax):
    """Durbin-Levinson: phi_kk from rho_1..rho_kmax (the PACF of T p. 46 as a function of the ACF)."""
    out, phi = [], np.zeros(0)
    for k in range(1, kmax + 1):
        if k == 1:
            phikk = rho[1]
            phi = np.array([phikk])
        else:
            phikk = (rho[k] - phi @ rho[k - 1:0:-1]) / (1 - phi @ rho[1:k])
            phi = np.append(phi - phikk * phi[::-1], phikk)
        out.append(phikk)
    return np.array(out)


def psi_weights(ar, ma, n):
    """psi_0..psi_{n-1} of (1 - sum ar B^i) r = (1 - sum ma B^i) a (Tsay's MA sign), T eq. (2.29)."""
    psi = np.zeros(n)
    psi[0] = 1.0
    for j in range(1, n):
        s = -ma[j - 1] if j <= len(ma) else 0.0
        s += sum(ar[i] * psi[j - 1 - i] for i in range(min(len(ar), j)))
        psi[j] = s
    return psi


def acf_linear(psi, k):
    """rho_0..rho_k of a linear process from its psi weights: L01-07 (4)."""
    g = np.array([psi[: len(psi) - l] @ psi[l:] for l in range(k + 1)])
    return g / g[0]


def arfima_acf(d, k):
    """rho_0..rho_k of (1-B)^d x = a: rho_j = rho_{j-1} (j-1+d)/(j-d) (T p. 102, property 3)."""
    r = np.empty(k + 1)
    r[0] = 1.0
    for j in range(1, k + 1):
        r[j] = r[j - 1] * (j - 1 + d) / (j - d)
    return r


# ---------- note 01 ----------
def fig_ar2_triangle_acf():
    """Stationarity region of the AR(2) and the ACF of the deck's two parameter sets (slides 20-22)."""
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(10.4, 4.2), gridspec_kw={"width_ratios": [1, 1.25]})
    x = np.linspace(-2, 2, 401)
    a1.fill(np.r_[-2, 0, 2], np.r_[-1, 1, -1], color=C["good"], alpha=0.10, lw=0)
    a1.plot([-2, 0, 2, -2], [-1, 1, -1, -1], color=C["good"], lw=1.6)
    a1.plot(x, -x ** 2 / 4, color=C["ref"], ls="--", lw=1.3)
    a1.text(-0.95, -0.84, "complex roots:\n" + r"$\phi_2<-\phi_1^2/4$", ha="center", fontsize=8.5, color=C["ref"])
    a1.text(0.62, 0.62, r"$\phi_2=1-\phi_1$", fontsize=9, color=C["good"], rotation=-38)
    a1.text(-1.45, 0.35, r"$\phi_2=1+\phi_1$", fontsize=9, color=C["good"], rotation=38)
    a1.text(-1.25, -1.16, r"$\phi_2=-1$", ha="center", fontsize=9, color=C["good"])
    pts = {(1.75, -0.80): C["main"], (0.90, 0.05): C["warn"], (0.869, -0.274): C["hi"], (0.6, -0.4): C["ref"]}
    labels = {(1.75, -0.80): "slides: (1.75, −0.80)\nk = %.1f" % cycle_length(1.75, -0.8),
              (0.90, 0.05): "slides: (0.90, 0.05)\nreal roots",
              (0.869, -0.274): "GNP factor\nk = %.2f" % cycle_length(0.869, -0.274),
              (0.6, -0.4): "Tsay Fig. 2.4(b)\nk = %.2f" % cycle_length(0.6, -0.4)}
    offs = {(1.75, -0.80): (-112, -8), (0.90, 0.05): (-30, 14), (0.869, -0.274): (8, 4), (0.6, -0.4): (-88, 4)}
    for p, col in pts.items():
        a1.scatter(*p, color=col, zorder=5, s=36)
        a1.annotate(labels[p], p, xytext=offs[p], textcoords="offset points", fontsize=8.2, color=col)
    a1.set(xlim=(-2.2, 2.2), ylim=(-1.35, 1.25), xlabel=r"$\phi_1$", ylabel=r"$\phi_2$",
           title="Stationarity triangle (both roots outside the unit circle)")
    for (p1, p2), col, lab in [((1.75, -0.80), C["main"], r"$\phi=(1.75,-0.80)$, complex"),
                               ((0.90, 0.05), C["warn"], r"$\phi=(0.90,0.05)$, real")]:
        r = ar2_acf(p1, p2, 150)
        a2.plot(np.arange(151), r, color=col, label=lab)
    a2.axhline(0, color=C["ref"], lw=0.8)
    a2.set(xlabel="lag $\\ell$", ylabel=r"$\rho_\ell$", title=r"Exact ACF: $\rho_\ell=\phi_1\rho_{\ell-1}+\phi_2\rho_{\ell-2}$")
    a2.legend(fontsize=8.5)
    save(fig, "L08-ar2-triangle-acf")
    r1 = ar2_acf(1.75, -0.8, 150)
    assert abs(r1[1] - 0.9722) < 5e-5 and abs(r1[2] - 0.9014) < 5e-5 and abs(r1.min() + 0.1866) < 5e-5 and r1.argmin() == 15
    assert abs(cycle_length(0.869, -0.274) - 10.62) < 5e-3 and abs(cycle_length(1.75, -0.8) - 30.09) < 5e-3
    assert abs(math.sqrt(ar2_gamma0(1.75, -0.8)) - 7.1207) < 5e-5


# ---------- note 02 ----------
def fig_identification():
    """ACF and PACF for AR(1), AR(2), MA(1), ARMA(1,1): the identification table (T p. 63, p. 66)."""
    K = 12
    models = [("AR(1), $\\phi_1=0.8$", [0.8], []), ("AR(2), $(0.6,-0.4)$", [0.6, -0.4], []),
              ("MA(1), $\\theta_1=0.6$", [], [0.6]), ("ARMA(1,1), $(0.8, 0.4)$", [0.8], [0.4])]
    fig, axes = plt.subplots(2, 4, figsize=(11.6, 4.6), sharey=True)
    lags = np.arange(1, K + 1)
    out = {}
    for j, (name, ar, ma) in enumerate(models):
        rho = acf_linear(psi_weights(ar, ma, 4000), K)
        pac = pacf_from_acf(rho, K)
        out[name] = (rho, pac)
        for i, (vals, lab) in enumerate([(rho[1:], "ACF"), (pac, "PACF")]):
            ax = axes[i, j]
            ax.vlines(lags, 0, vals, color=C["main"] if i == 0 else C["hi"], lw=2.4)
            ax.axhline(0, color=C["ref"], lw=0.8)
            ax.set_ylim(-0.75, 1.0)
            if i == 0:
                ax.set_title(name, fontsize=10)
            if j == 0:
                ax.set_ylabel(lab)
            if i == 1:
                ax.set_xlabel("lag")
    fig.suptitle("Exact ACF (top) and PACF (bottom): AR cuts off in the PACF, MA in the ACF, ARMA in neither",
                 fontsize=11, y=1.02)
    save(fig, "L08-identification-acf-pacf")
    rho_ma, pac_ma = out["MA(1), $\\theta_1=0.6$"]
    assert abs(rho_ma[1] + 0.6 / 1.36) < 1e-9 and abs(rho_ma[2]) < 1e-12
    rho_ar, pac_ar = out["AR(2), $(0.6,-0.4)$"]
    assert abs(pac_ar[1] + 0.4) < 1e-9 and np.all(np.abs(pac_ar[2:]) < 1e-9)
    rho_arma, _ = out["ARMA(1,1), $(0.8, 0.4)$"]
    assert abs(rho_arma[1] - 0.52308) < 5e-6 and abs(rho_arma[2] - 0.8 * rho_arma[1]) < 1e-9


def fig_ar2_forecast():
    """h-step forecast distributions of ar2-forecast.html: mean recursion, Var = sigma^2 sum psi^2."""
    p1, p2, yn, yn1, H = 1.75, -0.8, -5.487150, -3.508837, 50
    ys = [yn1, yn]
    for _ in range(H):
        ys.append(p1 * ys[-1] + p2 * ys[-2])
    E = np.array(ys[2:])
    V = np.cumsum(psi_weights([p1, p2], [], H) ** 2)
    z = stats.norm.ppf(0.95)
    sd_inf = math.sqrt(ar2_gamma0(p1, p2))
    h = np.arange(1, H + 1)
    fig, ax = plt.subplots(figsize=(8.4, 4.0))
    ax.fill_between(h, E - z * np.sqrt(V), E + z * np.sqrt(V), color=C["main"], alpha=0.16, lw=0, label="5%–95% band")
    ax.plot(h, E, color=C["main"], label=r"$E(y_{n+h}\mid y_{1:n})$")
    ax.plot([-1, 0], [yn1, yn], "o", color=C["ink"], ms=4, label=r"$y_{n-1}, y_n$")
    for v in (-z * sd_inf, 0, z * sd_inf):
        ax.axhline(v, color=C["good"], ls=":" if v else "-", lw=1.1)
    ax.text(H, z * sd_inf + 0.6, r"stationary $\pm1.645\times7.12$", ha="right", color=C["good"], fontsize=9)
    ax.set(xlabel="horizon $h$", ylabel="$y$", title=r"AR(2) $\phi=(1.75,-0.80)$: forecasts revert to 0 in damped cycles")
    ax.legend(fontsize=8.5, loc="lower right")
    save(fig, "L08-ar2-forecast-fan")
    assert np.allclose(E[:4], [-6.7954429, -7.5023051, -7.6926796, -7.4603452], atol=1e-6)
    assert np.allclose(V[:4], [1, 4.0625, 9.18140625, 15.73180664], atol=1e-7)
    assert abs(math.sqrt(V[-1]) - 7.1206) < 1e-4 and abs(sd_inf - 7.12069) < 1e-5


# ---------- note 03 ----------
def fig_unit_root():
    """Forecast-error bands (exact) and the Dickey-Fuller t law (seeded MC) vs N(0,1)."""
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(10.8, 4.0))
    l = np.arange(0, 121)
    mu, s = 0.0103, 0.0637                      # 3M monthly log returns, T eq. (2.37)
    sd_rw = s * np.sqrt(l)
    phi = 0.9
    sd_ar = s * np.sqrt((1 - phi ** (2 * l)) / (1 - phi ** 2))
    a1.plot(l, mu * l, color=C["warn"], label=r"RW with drift: mean $p_h+0.0103\,\ell$")
    a1.fill_between(l, mu * l - 2 * sd_rw, mu * l + 2 * sd_rw, color=C["warn"], alpha=0.14, lw=0)
    a1.plot(l, mu * l + 2 * sd_ar, color=C["good"], ls="--",
            label=r"trend-stationary, AR(1) $\phi=0.9$ about the trend: $\pm2$ sd")
    a1.plot(l, mu * l - 2 * sd_ar, color=C["good"], ls="--")
    a1.plot(l, 2 * sd_rw, color=C["ref"], lw=1, ls=":", label=r"$\pm2\sigma\sqrt{\ell}$ (driftless RW)")
    a1.plot(l, -2 * sd_rw, color=C["ref"], lw=1, ls=":")
    a1.set(xlabel=r"horizon $\ell$ (months)", ylabel=r"log price relative to $p_h$",
           title=r"Forecast bands: $\sigma\sqrt{\ell}$ grows, AR band stops at $\sigma/\sqrt{1-\phi^2}$")
    a1.legend(fontsize=7.8, loc="upper left")
    # Dickey-Fuller with a constant: Delta y_t = c + u y_{t-1} + e_t under H0: u = 0, y a driftless RW.
    rng = np.random.default_rng(2026)
    T, R = 250, 20000
    y = rng.standard_normal((R, T)).cumsum(axis=1)
    dy, yl = np.diff(y, axis=1), y[:, :-1]
    n = T - 1
    ylc = yl - yl.mean(axis=1, keepdims=True)           # partial out the constant
    b = (ylc * dy).sum(1) / (ylc ** 2).sum(1)
    resid = dy - dy.mean(1, keepdims=True) - b[:, None] * ylc
    se = np.sqrt((resid ** 2).sum(1) / (n - 2) / (ylc ** 2).sum(1))
    t = b / se
    grid = np.linspace(-5, 3, 400)
    kde = stats.gaussian_kde(t)
    a2.plot(grid, kde(grid), color=C["warn"], label="Dickey–Fuller $t$ (MC, seed 2026, $T=250$)")
    a2.plot(grid, stats.norm.pdf(grid), color=C["ref"], label="$N(0,1)$")
    q05 = np.quantile(t, 0.05)
    a2.axvline(-2.86, color=C["warn"], ls="--", lw=1.2)
    a2.axvline(-1.645, color=C["ref"], ls="--", lw=1.2)
    a2.text(-2.92, 0.47, "−2.86\n(W Table 18.2)", ha="right", fontsize=8.5, color=C["warn"])
    p_wrong = float((t < -1.645).mean())
    a2.text(-1.58, 0.47, f"−1.645: rejects a true\nunit root {p_wrong:.0%} of the time", fontsize=8.5, color=C["ref"])
    a2.set(xlabel=r"$t$ ratio of $\hat u$ in $\Delta y_t=c+u\,y_{t-1}+e_t$", ylabel="density", ylim=(0, 0.56),
           title="Under $H_0:u=0$ the $t$ ratio is not $N(0,1)$")
    a2.legend(fontsize=8, loc="center left")
    save(fig, "L08-unit-root-bands-df")
    assert abs(q05 + 2.86) < 0.05 and abs(np.quantile(t, 0.01) + 3.43) < 0.06
    assert 0.44 < p_wrong < 0.49
    assert abs(sd_ar[-1] - s / math.sqrt(1 - phi ** 2)) < 1e-6 and abs(sd_rw[100] - 0.637) < 1e-9


# ---------- note 04 ----------
def fig_long_memory():
    """ARFIMA(0,d,0) ACF vs AR(1) with the same rho_1: hyperbolic vs geometric decay (T p. 102)."""
    K = 200
    k = np.arange(K + 1)
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(10.6, 4.0))
    cols = {0.1: C["ref"], 0.25: C["main"], 0.4: C["warn"]}
    for d, col in cols.items():
        r = arfima_acf(d, K)
        phi = d / (1 - d)
        a1.plot(k[:61], r[:61], color=col, label=fr"$d={d}$: $\rho_1={phi:.3f}$")
        a1.plot(k[:61], phi ** k[:61], color=col, ls=":", lw=1.4)
        a2.loglog(k[1:], r[1:], color=col, label=fr"$d={d}$, slope $2d-1={2 * d - 1:.1f}$")
        a2.loglog(k[1:], phi ** k[1:], color=col, ls=":", lw=1.2)
    a1.set(xlabel="lag $k$", ylabel=r"$\rho_k$", title="Solid: ARFIMA(0,d,0). Dotted: AR(1) with the same $\\rho_1$")
    a1.legend(fontsize=8.5)
    a2.set(ylim=(1e-4, 1.2), xlabel="lag $k$ (log)", ylabel=r"$\rho_k$ (log)",
           title=r"Log–log: $\rho_k\sim c\,k^{2d-1}$ is a straight line")
    a2.legend(fontsize=8.5, loc="lower left")
    save(fig, "L08-long-memory-acf")
    r4 = arfima_acf(0.4, K)
    assert abs(arfima_acf(0.25, 1)[1] - 1 / 3) < 1e-12 and abs(r4[1] - 2 / 3) < 1e-12
    slope = (math.log(r4[200]) - math.log(r4[100])) / math.log(2)
    assert abs(slope - (2 * 0.4 - 1)) < 0.01                  # rho_k ~ k^{2d-1}
    assert r4[100] > 0.2 and (2 / 3) ** 100 < 1e-17


# ---------- note 05 ----------
def fig_airline_acf():
    """Exact ACF of w_t = (1 - theta B)(1 - Theta B^s) a_t (T p. 84) for the two fitted airline models."""
    fig, axes = plt.subplots(1, 2, figsize=(10.6, 3.8), sharey=True)
    out = {}
    for ax, (name, th, TH, s, K) in zip(axes, [("Johnson & Johnson, $s=4$: $(0.678, 0.314)$", 0.678, 0.314, 4, 12),
                                               ("AirPassengers, $s=12$: $(0.3864, 0.5885)$", 0.3864, 0.5885, 12, 30)]):
        ma = np.zeros(s + 1)
        ma[0], ma[s - 1], ma[s] = th, TH, -th * TH        # (1 - th B)(1 - TH B^s) = 1 - th B - TH B^s + th TH B^{s+1}
        rho = acf_linear(psi_weights([], list(ma), s + 2 + K), K)
        lags = np.arange(1, K + 1)
        colors = [C["warn"] if l in (1, s - 1, s, s + 1) else C["ref"] for l in lags]
        ax.vlines(lags, 0, rho[1:], colors=colors, lw=3)
        ax.axhline(0, color=C["ref"], lw=0.8)
        for l in (1, s - 1, s, s + 1):
            dx = -9 if l == s - 1 else 9 if l == s + 1 else 0
            ax.annotate(f"{rho[l]:.3f}", (l, rho[l]), xytext=(dx, 6 if rho[l] > 0 else -12), textcoords="offset points",
                        ha="center", fontsize=8, color=C["warn"])
        ax.set(title=name, xlabel="lag", ylim=(-0.54, 0.22))
        out[s] = rho
    axes[0].set_ylabel(r"$\rho_\ell$ of $w_t=(1-B^s)(1-B)x_t$")
    fig.suptitle("Airline model: nonzero ACF only at lags 1, s−1, s, s+1, with $\\rho_{s\\pm1}=\\rho_1\\rho_s$",
                 fontsize=11, y=1.03)
    save(fig, "L08-airline-acf")
    r4, r12 = out[4], out[12]
    assert abs(r4[1] + 0.4645) < 5e-5 and abs(r4[4] + 0.2858) < 5e-5 and abs(r4[3] - 0.1328) < 5e-5
    assert abs(r12[13] - r12[1] * r12[12]) < 1e-12 and abs(r12[12] + 0.4371) < 5e-5 and abs(r12[2]) < 1e-12


# ---------- note 06 ----------
def fig_garch_persistence_kurtosis():
    """Variance term structure (T eq. 3.17, 3.22) and the moment-existence region (T pp. 132, 166)."""
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(10.8, 4.2))
    L = np.arange(1, 121)
    cases = [("Tsay Ex. 3.3: $\\alpha_1+\\beta_1=0.9727$", 0.000086, 0.1216, 0.8511, C["main"]),
             ("Petrobras normal: 0.9800", 2.254954e-05, 0.1031668, 0.8768059, C["good"]),
             ("Tsay IGARCH: 1", 0.000119, 0.1941, 0.8059, C["warn"])]
    rows = {}
    for lab, w, a, b, col in cases:
        p = a + b
        if abs(p - 1) < 1e-12:
            s1 = 2 * math.sqrt(0.00314)            # start at twice Tsay's GARCH sigma_inf (no IGARCH sigma_inf exists)
            var = s1 ** 2 + (L - 1) * w
            ratio = np.sqrt(var / 0.00314)
        else:
            sinf2 = w / (1 - p)
            s1 = 2 * math.sqrt(sinf2)
            var = sinf2 + p ** (L - 1) * (s1 ** 2 - sinf2)
            ratio = np.sqrt(var / sinf2)
        rows[lab] = ratio
        a1.plot(L, ratio, color=col, label=lab)
    a1.axhline(1, color=C["ref"], lw=1, ls=":")
    a1.set(xlabel=r"horizon $\ell$", ylabel=r"$\sigma_h(\ell)/\sigma_\infty$ (IGARCH: Tsay's GARCH $\sigma_\infty$)",
           title=r"Start at $\sigma_h(1)=2\sigma_\infty$: decay at rate $\alpha_1+\beta_1$")
    a1.legend(fontsize=8)
    al = np.linspace(0, 0.6, 400)
    a2.fill_between(al, 0, np.clip(1 - al, 0, None), color=C["good"], alpha=0.09, lw=0)
    a2.plot(al, 1 - al, color=C["warn"], lw=1.6, label=r"$\alpha_1+\beta_1=1$ (IGARCH)")
    bg = -al + np.sqrt(np.clip(1 - 2 * al ** 2, 0, None))      # 1 - 2a^2 - (a+b)^2 = 0
    nu = 7.0
    bt = -al + np.sqrt(np.clip(1 - 2 * al ** 2 * (nu - 1) / (nu - 4), 0, None))
    okg, okt = 1 - 2 * al ** 2 >= 0, 1 - 2 * al ** 2 * (nu - 1) / (nu - 4) >= 0
    a2.plot(al[okg], bg[okg], color=C["main"], label=r"finite $E a_t^4$, Gaussian: $1-2\alpha_1^2-(\alpha_1+\beta_1)^2=0$")
    a2.plot(al[okt], bt[okt], color=C["hi"], ls="--", label=r"same, Student-$t_7$ innovations")
    pts = [("Tsay 3.3", 0.1216, 0.8511), ("PBR normal", 0.1031668, 0.8768059), ("PBR $t$", 0.07428964, 0.9094674),
           ("Intel ARCH(1)", 0.356, 0.0)]
    for lab, a, b in pts:
        a2.scatter(a, b, color=C["ink"], s=18, zorder=5)
        off = {"PBR $t$": (-38, 6), "PBR normal": (-70, -12), "Tsay 3.3": (6, -2)}.get(lab, (5, 5))
        a2.annotate(lab, (a, b), xytext=off, textcoords="offset points", fontsize=8)
    a2.set(xlim=(0, 0.6), ylim=(0, 1.02), xlabel=r"$\alpha_1$", ylabel=r"$\beta_1$",
           title="Below each curve the fourth moment exists")
    a2.legend(fontsize=7.4, loc="upper right")
    save(fig, "L08-garch-persistence-kurtosis")
    w, a, b = 0.000086, 0.1216, 0.8511
    assert abs((a + b) - 0.9727) < 1e-12 and abs(w / (1 - a - b) - 0.003150) < 5e-7
    hl = math.log(0.5) / math.log(a + b)
    assert abs(hl - 25.04) < 0.01
    tsay = rows[cases[0][0]]
    assert abs(tsay[0] - 2) < 1e-12 and abs(tsay[1] ** 2 - (1 + 3 * 0.9727)) < 1e-9   # (1 + p^(l-1)(4-1))
    assert 1 - 2 * a ** 2 - (a + b) ** 2 > 0 and abs(6 * a ** 2 / (1 - 2 * a ** 2 - (a + b) ** 2) - 3.654) < 1e-3


# ---------- notes 07 and 08 ----------
def fig_news_impact_sv_memory():
    """News impact (GARCH, GJR, EGARCH; garchmodeling.html PBR fits) and ACF of a_t^2, GARCH vs SV."""
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(10.8, 4.2))
    # Petrobras 2000-2021, garchmodeling.html (normal errors, no mean)
    w, a, b = 2.254954e-05, 0.1031668, 0.8768059
    wg, ag, gg, bg = 2.327038e-05, 0.09234234, 0.2083503, 0.8817760
    we, ae, be, ge = -0.15392, -0.05549, 0.97741, 0.18138
    s2_g = w / (1 - a - b)
    # fGarch's leverage=TRUE, delta=2 is APARCH: s2_t = w + a(|a_{t-1}| - g a_{t-1})^2 + b s2_{t-1}, so
    # E(|z| - g z)^2 = 1 + g^2 and the GJR-equivalent coefficients are a(1-g)^2 and 4ag.
    s2_gjr = wg / (1 - ag * (1 + gg ** 2) - bg)
    s2_e = math.exp(we / (1 - be))                        # E[g(eps)] = 0 in log sigma^2 = w + a eps + g(|eps| - E|eps|) + b log s2
    z = np.linspace(-5, 5, 401)                           # yesterday's standardized shock
    nic_g = w + a * s2_g * z ** 2 + b * s2_g
    nic_gjr = wg + ag * (np.abs(z) - gg * z) ** 2 * s2_gjr + bg * s2_gjr
    # rugarch eGARCH: log s2_t = w + a z + g(|z| - E|z|) + b log s2_{t-1}
    nic_e = np.exp(we + ae * z + ge * (np.abs(z) - math.sqrt(2 / math.pi)) + be * math.log(s2_e))
    for y, col, lab, ref in [(nic_g, C["main"], "GARCH(1,1)", s2_g), (nic_gjr, C["warn"], "GJR-GARCH(1,1)", s2_gjr),
                             (nic_e, C["hi"], "EGARCH(1,1)", s2_e)]:
        a1.plot(z, y / ref, color=col, label=lab)
    a1.axvline(0, color=C["ref"], lw=0.8)
    a1.set(xlabel=r"yesterday's standardized shock $\varepsilon_{t-1}$ (at $\sigma_{t-1}=\sigma_\infty$)",
           ylabel=r"$\sigma_t^2/\sigma_\infty^2$", title="News impact (Petrobras fits)")
    a1.legend(fontsize=8.5)
    # ACF of squared shocks. GARCH-t ML on standardized PBR (GARCH11-SVar1.html); SV-t posterior means.
    k = np.arange(1, 101)
    at, bt = 0.073478, 0.910218
    rho1 = at * (1 - at * bt - bt ** 2) / (1 - 2 * at * bt - bt ** 2)
    acf_g = rho1 * (at + bt) ** (k - 1)
    phi, sig = 0.9842135, 0.1387539
    s2h = sig ** 2 / (1 - phi ** 2)
    acf_sv = (np.exp(s2h * phi ** k) - 1) / (3 * np.exp(s2h) - 1)
    a2.plot(k, acf_g, color=C["main"], label=fr"GARCH(1,1): $\rho_1={rho1:.3f}$, decay $(\alpha_1+\beta_1)^{{k-1}}$, 0.984")
    a2.plot(k, acf_sv, color=C["warn"], label=fr"SV-AR(1): $\rho_1={acf_sv[0]:.3f}$, $\phi=0.984$, $\sigma_h^2={s2h:.3f}$")
    a2.set(xlabel="lag $k$", ylabel=r"corr$(a_t^2, a_{t-k}^2)$", ylim=(0, 0.25),
           title="Memory of squared shocks")
    a2.legend(fontsize=8)
    save(fig, "L08-news-impact-sv-memory")
    assert abs(rho1 - 0.2037) < 5e-5 and abs(acf_sv[0] - 0.1828) < 5e-5 and abs(s2h - 0.6146) < 5e-5
    i0, im = 200, 160                                          # z = 0 and z = -1
    assert abs(nic_g[i0] / s2_g - (w / s2_g + b)) < 1e-12 and nic_gjr[im] > nic_gjr[400 - im]
    assert nic_e[im] > nic_e[400 - im] and abs(nic_g[im] - nic_g[400 - im]) < 1e-15
    assert abs(ag * (1 + gg ** 2) + bg - 0.97813) < 5e-6 and abs(ag * (1 - gg) ** 2 - 0.05787) < 5e-6
    assert abs(4 * ag * gg - 0.07696) < 5e-6


def build():
    apply()
    fig_ar2_triangle_acf()
    fig_identification()
    fig_ar2_forecast()
    fig_unit_root()
    fig_long_memory()
    fig_airline_acf()
    fig_garch_persistence_kurtosis()
    fig_news_impact_sv_memory()


if __name__ == "__main__":
    build()
