"""Figures for the Class 9 notes (Notas/L09). Run: python Notas/L09/figures/make_figures.py

build() writes eight PNGs beside this file and asserts at least one plotted number per figure.
Every curve is the model's exact expression; the one simulation (Minnesota shrinkage path) is
seeded and says so in its title.

Sources: BVAR-part11.pdf (slides 8-13, 24, 33, 40-42); BVAR-part2.pdf (slides 15, 17, 22, 38);
VAR-Example.html (OLS B1-B3 and Sigma-hat of section 2.1; refined VAR and FEVD of section 3.2);
wti-sp500-timevaryingcovariance.html (dccPre / dccFit output); Tsay AFTS 3e Ex. 8.3 (p. 400),
Ex. 11.1 (pp. 559-560), eq. (11.14) (p. 563).
"""
import pathlib
import sys

import numpy as np

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))
from _figstyle import C, apply, save  # noqa: E402

import matplotlib.pyplot as plt  # noqa: E402

# ---- numbers printed in the sources -------------------------------------------------------
# BVAR-part11.pdf slide 13 (Lutkepohl Problem 2.3)
MU_S = np.array([2.0, 1.0, 0.0])
B1_S = np.array([[0.7, 0.1, 0.0], [0.0, 0.4, 0.1], [0.9, 0.0, 0.8]])
B2_S = np.array([[-0.2, 0.0, 0.0], [0.0, 0.1, 0.1], [0.0, 0.0, 0.0]])
SIG_S = np.array([[0.26, 0.03, 0.0], [0.03, 0.09, 0.0], [0.0, 0.0, 0.81]])
# VAR-Example.html section 2.1: OLS VAR(3), order (uk, us, ca)
G1 = np.array([[0.4308, 0.0587, 0.1274], [0.4380, 0.2405, 0.1747], [0.2938, 0.4887, 0.3231]])
G2 = np.array([[0.0008, -0.0439, 0.1482], [-0.2100, 0.1710, -0.0946], [-0.1665, 0.0228, -0.1915]])
G3 = np.array([[0.1010, 0.1866, -0.2989], [0.0184, -0.0306, -0.0968], [0.0422, -0.0858, 0.0840]])
SH = np.array([[0.52718715, 0.1543285, 0.07821377], [0.1543285, 0.5851116, 0.22866668],
               [0.07821377, 0.22866668, 0.49518778]])
# VAR-Example.html section 3.2: refVAR (zeros imposed) and its residual covariance
R1 = np.array([[0.446, 0.0, 0.141], [0.431, 0.231, 0.150], [0.306, 0.472, 0.327]])
R2 = np.array([[0.0, 0.0, 0.137], [-0.196, 0.139, 0.0], [-0.138, 0.0, -0.175]])
R3 = np.array([[0.0856, 0.193, -0.305], [0.0, 0.0, -0.145], [0.0, 0.0, 0.0]])
SR = np.array([[0.49497222, 0.1438478, 0.07301169], [0.14384784, 0.5516213, 0.21667644],
               [0.07301169, 0.21667644, 0.46840981]])
NAMES = ["UK", "US", "CA"]


def companion(Bs):
    """kp x kp companion matrix of a VAR(p) with coefficient list Bs = [B1, ..., Bp] (slide 8)."""
    k, p = Bs[0].shape[0], len(Bs)
    A = np.zeros((k * p, k * p))
    A[:k] = np.hstack(Bs)
    A[k:, :-k] = np.eye(k * (p - 1))
    return A


def psi(Bs, H):
    """VMA weights Psi_0..Psi_{H-1}: Psi_0 = I, Psi_s = sum_i B_i Psi_{s-i} (slide 10)."""
    k = Bs[0].shape[0]
    out = [np.eye(k)]
    for s in range(1, H):
        out.append(sum(B @ out[s - i] for i, B in enumerate(Bs, 1) if s - i >= 0))
    return out


def fevd(Bs, Sig, H):
    """FEVD shares omega_ij(H) with Cholesky orthogonalisation in the given order (slide 11)."""
    L = np.linalg.cholesky(Sig)
    num = sum((P @ L) ** 2 for P in psi(Bs, H))
    return num / num.sum(axis=1, keepdims=True)


def fig_companion_eigenvalues():
    """Eigenvalues of the companion matrix: slide VAR(2) and the UK/US/CA VAR(3)."""
    fig, ax = plt.subplots(figsize=(5.6, 5.2))
    t = np.linspace(0, 2 * np.pi, 400)
    ax.plot(np.cos(t), np.sin(t), color=C["ref"], lw=1.2, label="unit circle")
    e2 = np.linalg.eigvals(companion([B1_S, B2_S]))
    e3 = np.linalg.eigvals(companion([G1, G2, G3]))
    ax.scatter(e2.real, e2.imag, s=60, color=C["main"], label="slide VAR(2), $q=3$: 6 roots", zorder=5)
    ax.scatter(e3.real, e3.imag, s=46, marker="s", facecolor="none", edgecolor=C["warn"], lw=1.6,
               label="UK/US/CA VAR(3): 9 roots", zorder=5)
    m2, m3 = np.abs(e2).max(), np.abs(e3).max()
    ax.annotate(f"max modulus {m2:.4f}", (m2, 0), xytext=(0.45, -0.55), color=C["main"],
                arrowprops=dict(arrowstyle="->", color=C["main"]))
    ax.add_patch(plt.Circle((0, 0), m3, fill=False, ls=":", color=C["warn"]))
    ax.text(-0.95, 0.75, f"VAR(3): all inside\nradius {m3:.4f}", color=C["warn"], fontsize=9)
    ax.set(xlim=(-1.15, 1.15), ylim=(-1.15, 1.15), aspect="equal", xlabel="real part", ylabel="imaginary part",
           title="Stationarity: companion eigenvalues inside the unit circle")
    ax.legend(loc="lower left", fontsize=8.5)
    save(fig, "L09-companion-eigenvalues")
    assert abs(m2 - 0.9099) < 5e-5 and abs(m3 - 0.6107) < 5e-5
    assert abs(np.linalg.det(np.eye(3) - B1_S - B2_S) - 0.032) < 1e-12   # |Phi(1)| > 0, slide 9


def fig_irf_var3():
    """Reduced-form Psi_h and Cholesky-orthogonalised Theta_h = Psi_h L for the OLS VAR(3)."""
    H = 21
    P = psi([G1, G2, G3], H)
    L = np.linalg.cholesky(SH)
    Th = [p @ L for p in P]
    fig, axes = plt.subplots(3, 3, figsize=(9.6, 7.0), sharex=True, sharey=True)
    h = np.arange(H)
    for i in range(3):
        for j in range(3):
            ax = axes[i, j]
            ax.axhline(0, color=C["ref"], lw=0.8)
            ax.plot(h, [p[i, j] for p in P], color=C["ref"], marker="o", ms=2.5, lw=1.2, label=r"$\Psi_h$ (unit $u_j$)")
            ax.plot(h, [t[i, j] for t in Th], color=C["main"], lw=1.8, label=r"$\Theta_h=\Psi_hL$ (1-sd orth. shock)")
            ax.set_title(f"response of {NAMES[i]} to shock in {NAMES[j]}", fontsize=9)
    for ax in axes[-1]:
        ax.set_xlabel("horizon $h$ (quarters)")
    axes[0, 0].legend(fontsize=7.5, loc="upper right")
    fig.suptitle("UK/US/CA GDP growth (standardised): VAR(3) impulse responses, ordering UK, US, CA", y=1.0)
    fig.tight_layout()
    save(fig, "L09-irf-var3-gdp")
    assert np.allclose(P[1], G1) and abs(Th[1][2, 1] - 0.4496) < 5e-5 and abs(Th[0][0, 0] - 0.7261) < 5e-5
    assert max(abs(P[20]).max(), abs(Th[20]).max()) < 5e-3            # stationary: responses die out


def fig_fevd_var3():
    """FEVD of the refined VAR(3) (VAR-Example 3.2), stacked shares by horizon."""
    H = 20
    sh = np.array([fevd([R1, R2, R3], SR, k) for k in range(1, H + 1)])     # (H, 3, 3)
    fig, axes = plt.subplots(1, 3, figsize=(10.2, 3.6), sharey=True)
    cols = [C["main"], C["warn"], C["good"]]
    hh = np.arange(1, H + 1)
    for i, ax in enumerate(axes):
        ax.stackplot(hh, *[sh[:, i, j] for j in range(3)], colors=cols, alpha=0.85,
                     labels=[f"shock in {n}" for n in NAMES])
        ax.set(title=f"forecast-error variance of {NAMES[i]}", xlabel="horizon $H$", xlim=(1, H), ylim=(0, 1))
    axes[0].set_ylabel("share")
    axes[2].legend(loc="lower right", fontsize=8)
    fig.tight_layout()
    save(fig, "L09-fevd-var3-gdp")
    # VAR-Example.html section 3.2, FEVdec output (horizons 1 and 20)
    assert abs(sh[0, 1, 0] - 0.07578528) < 1e-6 and abs(sh[0, 2, 1] - 0.1599804) < 1e-6
    assert abs(sh[19, 0, 0] - 0.8774260) < 1e-3 and abs(sh[19, 2, 2] - 0.43585314) < 1e-3


def fig_cholesky_ordering():
    """Tsay Ex. 8.3: orthogonalised IRFs under orderings (r1, r2) and (r2, r1); impact vs rho."""
    Phi = np.array([[0.2, 0.3], [-0.6, 1.1]])
    Sig = np.array([[2.0, 1.0], [1.0, 1.0]])
    Pm = np.array([[0, 1], [1, 0]])
    La = np.linalg.cholesky(Sig)                         # columns: shock 1, shock 2
    Lb = (Pm @ np.linalg.cholesky(Pm @ Sig @ Pm))[:, ::-1]   # back to (r1, r2) rows; columns shock 1, shock 2
    H = 13
    h = np.arange(H)
    Ta = [np.linalg.matrix_power(Phi, k) @ La for k in h]
    Tb = [np.linalg.matrix_power(Phi, k) @ Lb for k in h]
    fig, axes = plt.subplots(1, 3, figsize=(11.2, 3.6))
    for ax, (i, j, ttl) in zip(axes[:2], ((0, 0, "response of $r_1$ to the $r_1$ shock"),
                                           (0, 1, "response of $r_1$ to the $r_2$ shock"))):
        ax.axhline(0, color=C["ref"], lw=0.8)
        ax.plot(h, [t[i, j] for t in Ta], color=C["main"], marker="o", ms=3, label="ordering $(r_1, r_2)$")
        ax.plot(h, [t[i, j] for t in Tb], color=C["warn"], marker="s", ms=3, ls="--", label="ordering $(r_2, r_1)$")
        ax.set(title=ttl, xlabel="horizon $h$")
    axes[0].legend(fontsize=8.5)
    rho = np.linspace(-0.99, 0.99, 400)
    s1 = np.sqrt(2.0)
    ax = axes[2]
    ax.plot(rho, np.full_like(rho, s1), color=C["main"], label=r"own impact, $(r_1,r_2)$: $\sigma_1$")
    ax.plot(rho, s1 * np.sqrt(1 - rho**2), color=C["warn"], label=r"own impact, $(r_2,r_1)$: $\sigma_1\sqrt{1-\rho^2}$")
    ax.plot(rho, s1 * rho, color=C["hi"], ls="--", label=r"cross impact, $(r_2,r_1)$: $\rho\sigma_1$")
    ax.axvline(0, color=C["good"], lw=1, ls=":")
    r0 = 1 / np.sqrt(2)
    ax.scatter([r0, r0], [s1 * np.sqrt(1 - r0**2), s1 * r0], color=C["ink"], zorder=5)
    ax.annotate("Ex. 8.3: $\\rho=1/\\sqrt{2}$", (r0, 1.0), xytext=(-0.95, 0.55), fontsize=8.5,
                arrowprops=dict(arrowstyle="->", color=C["ink"]))
    ax.set(title=r"impact on $r_1$ ($h=0$) against $\rho$", xlabel=r"innovation correlation $\rho$")
    ax.legend(fontsize=7.5, loc="lower right")
    fig.tight_layout()
    save(fig, "L09-cholesky-ordering")
    assert np.allclose(Ta[0], [[np.sqrt(2), 0], [1 / np.sqrt(2), 1 / np.sqrt(2)]])
    assert np.allclose(Tb[0], [[1, 1], [0, 1]]) and np.allclose(Tb[1], [[0.2, 0.5], [-0.6, 0.5]])
    assert np.allclose(Ta[0] @ Ta[0].T, Sig) and np.allclose(Tb[0] @ Tb[0].T, Sig)


def minnesota_posterior(y, X, gamma0, v0, s2):
    """Equation-by-equation Minnesota posterior with sigma_i^2 known (slide 24).

    y: (T,) one equation's response; X: (T, K) regressors (constant first);
    gamma0, v0: prior mean and prior variances (diagonal); s2: known error variance.
    Returns the posterior mean (K,) and covariance (K, K).
    """
    Vbar = np.linalg.inv(np.diag(1 / v0) + X.T @ X / s2)
    return Vbar @ (gamma0 / v0 + X.T @ y / s2), Vbar


def lagmat(Y, p):
    T = Y.shape[0]
    return np.hstack([np.ones((T - p, 1))] + [Y[p - k:T - k] for k in range(1, p + 1)]), Y[p:]


def fig_minnesota():
    """Prior sd by lag (exact) and the posterior-mean path in lambda (seeded simulation, slide 13 DGP)."""
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(10.4, 3.9))
    k = np.arange(1, 7)
    lam, theta = 0.2, 0.5
    for lam_, ls in ((0.2, "-"), (0.4, ":")):
        a1.plot(k, lam_ / k, color=C["main"], ls=ls, marker="o", label=fr"own lags, $\lambda={lam_}$: $\lambda/k$")
        a1.plot(k, theta * lam_ / k, color=C["warn"], ls=ls, marker="s",
                label=fr"other lags, $\lambda={lam_}$: $\theta\lambda/k$ ($\sigma_i=\sigma_j$)")
    a1.set(xlabel="lag $k$", ylabel="prior standard deviation", title=r"Minnesota prior sd ($\theta=0.5$)")
    a1.legend(fontsize=7.5)
    # simulation: T = 60 draws (after 200 burn-in) from the slide-13 VAR(2), seed 9
    rng = np.random.default_rng(9)
    Lc = np.linalg.cholesky(SIG_S)
    Y = np.zeros((260, 3))
    for t in range(2, 260):
        Y[t] = MU_S + B1_S @ Y[t - 1] + B2_S @ Y[t - 2] + Lc @ rng.standard_normal(3)
    Y = Y[200:]
    p = 2
    X, Yr = lagmat(Y, p)
    s2 = np.array([np.var(lagmat(Y[:, [i]], p)[1][:, 0] - lagmat(Y[:, [i]], p)[0]
                          @ np.linalg.lstsq(*lagmat(Y[:, [i]], p), rcond=None)[0][:, 0], ddof=p + 1)
                   for i in range(3)])                         # univariate AR(2) residual variances
    i = 0                                                        # equation 1
    g0 = np.zeros(1 + 3 * p)
    g0[1 + i] = 1.0                                              # random-walk centre: own first lag = 1
    lams = np.logspace(-3, 1, 120)
    paths = []
    for lm in lams:
        v0 = [1e6]
        for kk in range(1, p + 1):
            for j in range(3):
                v0.append((lm / kk) ** 2 * (1 if j == i else theta**2 * s2[i] / s2[j]))
        paths.append(minnesota_posterior(Yr[:, i], X, g0, np.array(v0), s2[i])[0])
    paths = np.array(paths)
    ols = np.linalg.lstsq(X, Yr[:, i], rcond=None)[0]
    labels = ["$B_1(1,1)$", "$B_1(1,2)$", "$B_1(1,3)$", "$B_2(1,1)$"]
    idx = [1, 2, 3, 4]
    cols = [C["main"], C["warn"], C["good"], C["hi"]]
    for lab, c, col in zip(labels, idx, cols):
        a2.semilogx(lams, paths[:, c], color=col, label=lab)
        a2.axhline(ols[c], color=col, ls=":", lw=1)
    a2.axhline(1, color=C["ref"], lw=0.8)
    a2.text(1.2e-3, 1.03, "prior mean of own lag = 1", fontsize=8, color=C["ref"])
    a2.set(xlabel=r"overall tightness $\lambda$ (log scale)", ylabel="posterior mean",
           title="Equation 1: from the random-walk prior to OLS\n(seeded simulation, $T=58$, slide-13 VAR(2))")
    a2.legend(fontsize=8, loc="center right")
    fig.tight_layout()
    save(fig, "L09-minnesota-shrinkage")
    assert abs(paths[0, 1] - 1) < 0.02 and np.max(np.abs(paths[0, 2:])) < 0.02     # lambda -> 0: prior
    assert np.allclose(paths[-1, 1:], ols[1:], atol=0.02)                          # lambda large: OLS
    assert abs(lam / 3 - 0.0667) < 1e-4


def fig_factor_correlation():
    """One-factor implied correlation against factor variance; bound on k against m."""
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(10.4, 3.9))
    lh = np.linspace(-6, 3, 500)
    h = np.exp(lh)
    rho = lambda b1, b2, p1, p2, hh: b1 * b2 * hh / np.sqrt((b1**2 * hh + p1) * (b2**2 * hh + p2))
    for (b1, b2, p1, p2, lab, col) in ((0.99, 0.90, 0.01, 0.10, "series 1 & 3 (slide 22)", C["main"]),
                                      (0.99, 0.90, 0.05, 0.15, "series 2 & 4 (slide 22)", C["warn"]),
                                      (1.0, 1.0, 1.0, 1.0, r"$\psi_i=\beta_i^2$: $h/(1+h)$", C["ref"])):
        a1.plot(lh, rho(b1, b2, p1, p2, h), color=col, label=lab)
    r1 = rho(0.99, 0.90, 0.01, 0.10, 1.0)
    a1.scatter([0], [r1], color=C["good"], zorder=5)
    a1.annotate(f"static FA, $h=1$: {r1:.3f}", (0, r1), xytext=(-5.6, 0.85), fontsize=8.5,
                arrowprops=dict(arrowstyle="->", color=C["good"]))
    a1.set(xlabel=r"factor log-variance $\lambda_t=\log h_t$", ylabel=r"implied correlation $\rho_t$",
           title="FSV: correlation rises with factor volatility", ylim=(0, 1.02))
    a1.legend(fontsize=8, loc="lower right")
    m = np.arange(2, 61)
    kmax = np.floor(((2 * m + 1) - np.sqrt(8 * m + 1)) / 2)
    a2.step(m, kmax, where="mid", color=C["main"], label=r"$k_{\max}=\lfloor(2m+1-\sqrt{8m+1})/2\rfloor$")
    pts = {6: 3, 12: 7, 20: 14, 50: 40}
    a2.scatter(list(pts), list(pts.values()), color=C["warn"], zorder=5, label="slide 17: 6→3, 12→7, 20→14, 50→40")
    a2.plot(m, m, color=C["ref"], ls=":", lw=1, label="$k=m$")
    a2.set(xlabel="number of series $m$", ylabel="largest admissible $k$",
           title=r"Identification bound: $m(k+1)-k(k-1)/2\leq m(m+1)/2$")
    a2.legend(fontsize=8)
    fig.tight_layout()
    save(fig, "L09-factor-correlation")
    assert abs(r1 - 0.9387) < 5e-5
    for mm, kk in pts.items():
        assert kmax[mm - 2] == kk
        assert mm * (mm + 1) / 2 - mm * (kk + 1) + kk * (kk - 1) / 2 >= 0 > mm * (mm + 1) / 2 - mm * (kk + 2) + (kk + 1) * kk / 2


def fig_kalman_gain():
    """Local-level model: steady-state Kalman gain vs signal-to-noise; the gain path for Tsay Ex. 11.1."""
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(10.4, 3.8))
    q = np.logspace(-4, 2, 400)
    pstar = (q + np.sqrt(q**2 + 4 * q)) / 2
    K = pstar / (pstar + 1)
    a1.semilogx(q, K, color=C["main"], label=r"$K^*=p^*/(p^*+1)$, $p^*=\frac{q+\sqrt{q^2+4q}}{2}$")
    se, sn = 0.4803, 0.0735                                    # Tsay Ex. 11.1 MLEs (p. 560)
    q0 = (sn / se) ** 2
    p0 = (q0 + np.sqrt(q0**2 + 4 * q0)) / 2
    K0 = p0 / (p0 + 1)
    a1.scatter([q0], [K0], color=C["warn"], zorder=5)
    a1.annotate(f"Alcoa RV: $q={q0:.4f}$, $K^*={K0:.3f}$\n$=1-\\hat\\theta=1-0.858$", (q0, K0),
                xytext=(2e-4, 0.55), fontsize=8.5, arrowprops=dict(arrowstyle="->", color=C["warn"]))
    a1.set(xlabel=r"signal-to-noise $q=\sigma_\eta^2/\sigma_e^2$", ylabel="steady-state gain $K^*$",
           title="How much of each surprise moves the state", ylim=(0, 1))
    a1.legend(fontsize=8, loc="upper left")
    # deterministic gain path from eq. (11.14): P_{t+1|t} = P_{t|t-1}(1-K_t) + s_eta^2
    T = 40
    for P1, col, lab in ((10.0, C["main"], r"$\Sigma_{1|0}=10$"), (0.0, C["good"], r"$\Sigma_{1|0}=0$")):
        P, Ks = P1, []
        for _ in range(T):
            Kt = P / (P + se**2)
            Ks.append(Kt)
            P = P * (1 - Kt) + sn**2
        a2.plot(np.arange(1, T + 1), Ks, color=col, marker="o", ms=2.5, label=lab)
    a2.axhline(K0, color=C["warn"], ls="--", lw=1, label=f"$K^*={K0:.4f}$")
    a2.set(xlabel="$t$", ylabel="$K_t$", title="Gain path, Tsay Ex. 11.1 parameters (no data needed)")
    a2.legend(fontsize=8)
    fig.tight_layout()
    save(fig, "L09-kalman-gain-snr")
    assert abs(K0 - 0.1418) < 5e-5 and abs((1 - K0) - 0.858) < 5e-4 and abs(Ks[-1] - K0) < 1e-4


def fig_dcc_persistence():
    """Expected reversion multipliers: DCC correlation (Engle, Tse-Tsui) and GARCH(1,1) variances."""
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(10.4, 3.8))
    h = np.arange(0, 41)
    hl = {}
    for (t1, t2, lab, col) in ((0.8703852, 0.03813264, "Engle DCC", C["main"]),
                               (0.7017527, 0.049999, "Tse-Tsui DCC", C["warn"])):
        s = t1 + t2
        hl[lab] = np.log(0.5) / np.log(s)
        a1.plot(h, s**h, color=col, label=fr"{lab}: $(\theta_1+\theta_2)^h$, $\theta_1+\theta_2={s:.4f}$")
        a1.axvline(hl[lab], color=col, ls=":", lw=1)
    a1.axhline(0.5, color=C["ref"], lw=0.8)
    a1.set(xlabel="horizon $h$ (trading days)", ylabel="share of today's deviation left",
           title="Correlation shocks: W&T Offshore vs S&P 500")
    a1.legend(fontsize=7.8)
    for (a, b, lab, col) in ((0.1061140, 0.8432337, "W&T Offshore", C["main"]),
                             (0.1964253, 0.8065090, "S&P 500", C["warn"])):
        s = a + b
        a2.plot(h, s**h, color=col, label=fr"{lab}: $\alpha+\beta={s:.4f}$")
    a2.axhline(1, color=C["ref"], lw=0.8)
    a2.set(xlabel="horizon $h$ (trading days)", ylabel=r"$(\alpha+\beta)^h$",
           title="GARCH(1,1)-t variance shocks (dccPre)")
    a2.legend(fontsize=8)
    fig.tight_layout()
    save(fig, "L09-dcc-garch-persistence")
    assert abs(hl["Engle DCC"] - 7.22) < 5e-3 and abs(hl["Tse-Tsui DCC"] - 2.43) < 5e-3
    assert 0.1964253 + 0.8065090 > 1 > 0.1061140 + 0.8432337


def build():
    apply()
    fig_companion_eigenvalues()
    fig_irf_var3()
    fig_fevd_var3()
    fig_cholesky_ordering()
    fig_minnesota()
    fig_factor_correlation()
    fig_kalman_gain()
    fig_dcc_persistence()


if __name__ == "__main__":
    build()
