"""Step 6 verification for the Class 2 companions (Notas/L02/companions/).

Runs each page's own <script> blocks under node with a stub DOM, then checks:
  * every read-out against an independent numpy/scipy recomputation, at three control vectors
    (both ends of the ranges and the default) plus edge cases, to far below the displayed precision,
    and the displayed strings themselves;
  * the Flexibility Dial against a seeded Monte Carlo at the defaults (bias^2 and variance within MC error);
  * the Two-Gaussian Classifier against direct numerical integration of the densities over the regions,
    and its Phi against scipy's normal CDF;
  * every control sweeps (changes a read-out), reset restores the defaults, no NaN/undefined in any text.

Usage: python Notas/L02/companions/check_companions.py   (needs node on PATH; numpy, scipy)
Fails with AssertionError naming the first disagreement.
"""
import json
import math
import pathlib
import subprocess
import tempfile

import numpy as np
from numpy.polynomial import chebyshev as C
from scipy import integrate, linalg, stats

HERE = pathlib.Path(__file__).resolve().parent
PAGE_A = HERE / "companion-bias-variance-polynomial.html"
PAGE_B = HERE / "companion-gaussian-discriminant.html"

# Loads every <script> of the page into one vm context with a stub DOM. Each job evaluates `expr`
# (pure model call, __p bound to job.p), then sets the inputs in job.ui, runs update(), and returns
# all element text. A final reset() reports the input values it restored.
HARNESS = r"""
const fs = require('fs'), vm = require('vm');
const html = fs.readFileSync(process.argv[2], 'utf8'), jobs = JSON.parse(fs.readFileSync(0, 'utf8'));
const els = {};
const mk = id => els[id] || (els[id] = {id, value:'', textContent:'', innerHTML:'', max:'', min:'',
  listeners:{}, addEventListener(t, f){ (this.listeners[t] = this.listeners[t] || []).push(f); }});
const ctx = vm.createContext({document:{getElementById:mk}, console});
for (const m of html.matchAll(/<script[^>]*>([\s\S]*?)<\/script>/g)) vm.runInContext(m[1], ctx);
const out = jobs.map(job => {
  ctx.__p = job.p;
  const model = job.expr ? vm.runInContext(job.expr, ctx) : null;
  if (job.ui) { for (const [k, v] of Object.entries(job.ui)) mk(k).value = String(v); vm.runInContext('update()', ctx); }
  const text = {}; for (const e of Object.values(els)) text[e.id] = e.textContent + ' ' + e.innerHTML;
  return {model, text, values:Object.fromEntries(Object.values(els).map(e => [e.id, e.value]))};
});
vm.runInContext('reset()', ctx);
out.push({reset:Object.fromEntries(Object.values(els).map(e => [e.id, e.value]))});
process.stdout.write(JSON.stringify(out, (k, v) => (typeof v === 'number' && !isFinite(v)) ? String(v) : v));
"""


def run_node(page, jobs):
    with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False, encoding="utf-8") as fh:
        fh.write(HARNESS)
        path = fh.name
    try:
        res = subprocess.run(["node", path, str(page)], input=json.dumps(jobs), capture_output=True,
                             text=True, encoding="utf-8", check=True)
    finally:
        pathlib.Path(path).unlink()
    return json.loads(res.stdout)


def close(js, py, what, rtol=1e-9, atol=1e-12):
    assert abs(js - py) <= atol + rtol * abs(py), f"{what}: page {js!r} vs python {py!r}"


def no_garbage(text, where):
    for k, v in text.items():
        for bad in ("NaN", "undefined", "Infinity"):
            assert bad not in v, f"{where}: '{bad}' in element #{k}: {v[:200]}"


# ---------------------------------------------------------------- page A: the Flexibility Dial
f_true = lambda x: 45 * np.tanh(x / 1.9 - 7) + 57
GRID = np.linspace(8, 18, 400)


def fmtE(v):  # mirrors the page's fmtE (magnitude picks the decimals; U+2212 minus)
    a = abs(v)
    s = f"{a:.3f}" if a < 10 else f"{a:.2f}" if a < 1000 else f"{a:.1f}"
    return ("−" if v < 0 and float(s) != 0 else "") + s


def py_A(d, n, sig):
    """Exact conditional-on-design terms, Chebyshev basis + Householder QR (the page uses Legendre + MGS)."""
    xs = np.linspace(8, 18, n)
    u, ug = (xs - 13) / 5, (GRID - 13) / 5
    dmax = min(15, n - 2)
    fx, fg = f_true(xs), f_true(GRID)
    curve = []
    for k in range(dmax + 1):
        B, Bg = C.chebvander(u, k), C.chebvander(ug, k)
        Q, R = np.linalg.qr(B)
        G = linalg.solve_triangular(R, Bg.T, trans="T").T  # Bg R^{-1}
        coef = Q.T @ fx
        mean, v1 = G @ coef, (G ** 2).sum(1)
        bias2, vari = np.mean((mean - fg) ** 2), sig ** 2 * np.mean(v1)
        resid = fx - Q @ coef
        curve.append(dict(bias2=bias2, vari=vari, test=bias2 + vari + sig ** 2,
                          train=sig ** 2 * (1 - (k + 1) / n) + resid @ resid / n))
    dd = min(d, dmax)
    dopt = int(np.argmin([c["test"] for c in curve]))
    return dict(d=dd, dmax=dmax, dopt=dopt, testOpt=curve[dopt]["test"], curve=curve, **curve[dd])


def check_A():
    exprA = ("(() => { const r = compute(__p); return {d:r.d, dmax:r.dmax, bias2:r.bias2, vari:r.vari, test:r.test,"
             " train:r.train, dopt:r.dopt, testOpt:r.testOpt, curve:r.curve}; })()")
    vectors = {"low ends": dict(d=0, n=10, sig=0.5), "default": dict(d=3, n=30, sig=4.0),
               "high ends": dict(d=15, n=200, sig=15.0), "d = n-2 at n = 10": dict(d=8, n=10, sig=4.0)}
    jobs = [dict(p=p, expr=exprA, ui=p) for p in vectors.values()]
    jobs.append(dict(p=dict(d=15, n=10, sig=4.0), expr=None, ui=dict(d=15, n=10, sig=4.0)))  # clamp test
    sweeps = [(k, lo, hi) for k, lo, hi in (("d", 0, 15), ("n", 10, 200), ("sig", 0.5, 15.0))]
    for k, lo, hi in sweeps:
        for v in (lo, hi):
            p = dict(d=3, n=30, sig=4.0)
            p[k] = v
            jobs.append(dict(p=p, expr=exprA, ui=p))
    out = run_node(PAGE_A, jobs)
    rows = []
    for (name, p), o in zip(vectors.items(), out):
        js, py = o["model"], py_A(**p)
        assert js["d"] == py["d"] and js["dmax"] == py["dmax"] and js["dopt"] == py["dopt"], (name, js["dopt"], py["dopt"])
        for key in ("bias2", "vari", "test", "train", "testOpt"):
            close(js[key], py[key], f"A {name} {key}")
            assert fmtE(js[key]) == fmtE(py[key]), f"A {name} {key} display"
        for kk, (cj, cp) in enumerate(zip(js["curve"], py["curve"])):
            for key in ("bias2", "vari", "test", "train"):
                close(cj[key], cp[key], f"A {name} curve d={kk} {key}")
        shown = o["text"]["etest"].split()[0]
        assert shown == fmtE(py["test"]), f"A {name}: page shows {shown}, python {fmtE(py['test'])}"
        for key, val in (("train", py["train"]), ("optimism", py["test"] - py["train"])):
            assert fmtE(val) in o["text"]["ident2"], f"A {name}: {key} {fmtE(val)} not in {o['text']['ident2']}"
        no_garbage(o["text"], f"A {name}")
        rows.append((name, p, py, js, shown))
    clamp = out[len(vectors)]
    assert str(clamp["values"]["d"]) == "8" and clamp["text"]["o-d"].startswith("8  (max 8)"), clamp["text"]["o-d"]
    no_garbage(clamp["text"], "A clamp")
    sw = out[len(vectors) + 1: len(vectors) + 1 + 2 * len(sweeps)]
    for i, (k, lo, hi) in enumerate(sweeps):
        a, b = sw[2 * i]["model"], sw[2 * i + 1]["model"]
        assert (a["test"], a["vari"]) != (b["test"], b["vari"]), f"A control {k} does not move the read-outs"
        ta, tb = sw[2 * i]["text"], sw[2 * i + 1]["text"]
        assert ta["fitplot"] != tb["fitplot"] and ta["errplot"] != tb["errplot"], f"A control {k} does not move both charts"
        no_garbage(sw[2 * i]["text"], f"A sweep {k}={lo}")
        no_garbage(sw[2 * i + 1]["text"], f"A sweep {k}={hi}")
    rs = out[-1]["reset"]
    assert (float(rs["d"]), float(rs["n"]), float(rs["sig"])) == (3, 30, 4), rs

    print("Flexibility Dial: page (node) vs python, displayed precision")
    for name, p, py, js, shown in rows:
        print(f"  {name:18s} d={p['d']:>2} n={p['n']:>3} sig={p['sig']:<4} | test {fmtE(py['test'])} (page {shown}) "
              f"bias2 {fmtE(py['bias2'])}/{fmtE(js['bias2'])} var {fmtE(py['vari'])}/{fmtE(js['vari'])} "
              f"train {fmtE(py['train'])}/{fmtE(js['train'])} d* {py['dopt']}/{js['dopt']} "
              f"test(d*) {fmtE(py['testOpt'])}/{fmtE(js['testOpt'])}")

    # Monte Carlo at the default, independent route: lstsq on a Chebyshev basis, simulated noise.
    d, n, sig, R = 3, 30, 4.0, 20000
    rng = np.random.default_rng(20261019)
    xs = np.linspace(8, 18, n)
    B, Bg = C.chebvander((xs - 13) / 5, d), C.chebvander((GRID - 13) / 5, d)
    Y = f_true(xs)[:, None] + sig * rng.standard_normal((n, R))
    preds = Bg @ np.linalg.lstsq(B, Y, rcond=None)[0]  # 400 x R
    m_hat, v_hat = preds.mean(1), preds.var(1, ddof=1)
    ex = py_A(d, n, sig)
    var_mc = v_hat.mean()
    bias2_mc = np.mean((m_hat - f_true(GRID)) ** 2) - var_mc / R  # remove E[(m_hat - E m_hat)^2] = var/R
    # pointwise exact bias and variance for the MC standard errors
    Q, Rr = np.linalg.qr(B)
    G = linalg.solve_triangular(Rr, Bg.T, trans="T").T
    bias_pt = G @ (Q.T @ f_true(xs)) - f_true(GRID)
    var_pt = sig ** 2 * (G ** 2).sum(1)
    se_var = np.mean(var_pt * math.sqrt(2 / (R - 1)))          # bound: sd of a mean <= mean of sds
    se_b2 = np.mean(np.sqrt(4 * bias_pt ** 2 * var_pt / R + 2 * (var_pt / R) ** 2))
    print(f"  Monte Carlo (R = {R}, seed 20261019): bias2 {bias2_mc:.4f} vs exact {ex['bias2']:.4f} (4 SE = {4*se_b2:.4f}); "
          f"var {var_mc:.4f} vs exact {ex['vari']:.4f} (4 SE = {4*se_var:.4f})")
    assert abs(bias2_mc - ex["bias2"]) < 4 * se_b2, "MC bias^2 disagrees"
    assert abs(var_mc - ex["vari"]) < 4 * se_var, "MC variance disagrees"


# ---------------------------------------------------------------- page B: the Two-Gaussian Classifier
def py_B(mu1, mu2, s1, s2, pi1, lr):
    """Roots of h(x) - k from logpdf values (exact for a quadratic), regions by sign tests, scipy CDFs."""
    r, pi2 = 10 ** (lr / 100), 1 - pi1
    k = math.log(pi2 / (pi1 * r))
    g = lambda x: stats.norm.logpdf(x, mu1, s1) - stats.norm.logpdf(x, mu2, s2) - k
    A, Bc, Cc = (g(1) + g(-1)) / 2 - g(0), (g(1) - g(-1)) / 2, g(0)
    if s1 == s2 and mu1 == mu2:
        roots = []
    elif s1 == s2:
        roots = [float(-Cc / Bc)]
    else:
        rts = np.roots([A, Bc, Cc])
        roots = sorted(float(z.real) for z in rts) if np.all(np.isreal(rts)) and Bc * Bc - 4 * A * Cc > 0 else []
    edges = [-np.inf] + roots + [np.inf]
    R1, R2 = [], []
    for lo, hi in zip(edges[:-1], edges[1:]):
        t = (lo + hi) / 2 if np.isfinite(lo) and np.isfinite(hi) else (hi - 1 if np.isfinite(hi) else lo + 1 if np.isfinite(lo) else 0.0)
        (R1 if g(t) >= 0 else R2).append((lo, hi))
    P = lambda R, mu, s: sum(stats.norm.cdf(hi, mu, s) - stats.norm.cdf(lo, mu, s) if (lo - mu) / s <= 0
                             else stats.norm.sf(lo, mu, s) - stats.norm.sf(hi, mu, s) for lo, hi in R)
    p21, p12, p11, p22 = P(R2, mu1, s1), P(R1, mu2, s2), P(R1, mu1, s1), P(R2, mu2, s2)
    # direct quadrature of the densities times the allocation indicator, breakpoints at the roots
    lo_, hi_ = min(mu1 - 12 * s1, mu2 - 12 * s2), max(mu1 + 12 * s1, mu2 + 12 * s2)
    pts = [x for x in roots if lo_ < x < hi_] or None
    q21 = integrate.quad(lambda x: stats.norm.pdf(x, mu1, s1) * (g(x) < 0), lo_, hi_, points=pts, limit=400, epsabs=1e-13)[0]
    q12 = integrate.quad(lambda x: stats.norm.pdf(x, mu2, s2) * (g(x) >= 0), lo_, hi_, points=pts, limit=400, epsabs=1e-13)[0]
    return dict(k=k, roots=roots, p21=p21, p12=p12, p11=p11, p22=p22, err=pi1 * p21 + pi2 * p12,
                cost=pi1 * r * p21 + pi2 * p12, thr=1 / (1 + r), q21=q21, q12=q12, nR1=len(R1))


def check_B():
    exprB = ("(() => { const m = compute(__p); return {k:m.k, roots:m.roots, p21:m.p21, p12:m.p12, p11:m.p11,"
             " p22:m.p22, err:m.err, cost:m.cost, thr:m.thr, kind:m.kind, nR1:m.R1.length}; })()")
    vectors = {
        "low ends": dict(mu1=-5, mu2=-5, s1=0.5, s2=0.5, pi1=0.01, lr=-100),
        "default": dict(mu1=1, mu2=5, s1=6, s2=2.5, pi1=0.5, lr=0),
        "high ends": dict(mu1=10, mu2=10, s1=10, s2=10, pi1=0.99, lr=100),
        "mixed ends": dict(mu1=-5, mu2=10, s1=10, s2=0.5, pi1=0.01, lr=100),
        "landmark sigma1=sigma2": dict(mu1=1, mu2=5, s1=6, s2=6, pi1=0.5, lr=0),
        "sigma1<sigma2": dict(mu1=1, mu2=5, s1=2.5, s2=6, pi1=0.3, lr=50),
        "no root": dict(mu1=1, mu2=1, s1=10, s2=0.5, pi1=0.99, lr=100),
    }
    zs = [float(z) for z in np.arange(-40, 40.0001, 0.01)] + [-1e300, 1e300]
    jobs = [dict(p={"z": zs}, expr="__p.z.map(Phi)", ui=None)]
    jobs += [dict(p=p, expr=exprB, ui=p) for p in vectors.values()]
    base = vectors["default"]
    ranges = dict(mu1=(-5, 10), mu2=(-5, 10), s1=(0.5, 10), s2=(0.5, 10), pi1=(0.01, 0.99), lr=(-100, 100))
    for k, (lo, hi) in ranges.items():
        for v in (lo, hi):
            jobs.append(dict(p={**base, k: v}, expr=exprB, ui={**base, k: v}))
    out = run_node(PAGE_B, jobs)

    phi_js = np.array([float(v) for v in out[0]["model"]])
    phi_err = np.max(np.abs(phi_js - stats.norm.cdf(np.array(zs))))
    print(f"Two-Gaussian Classifier: max |Phi_page - scipy.norm.cdf| over [-40, 40] = {phi_err:.2e}")
    assert phi_err < 1e-13, phi_err

    pct = lambda x: f"{100 * x:.2f}%"
    for (name, p), o in zip(vectors.items(), out[1:1 + len(vectors)]):
        js, py = o["model"], py_B(**p)
        assert len(js["roots"]) == len(py["roots"]) and js["nR1"] == py["nR1"], (name, js["roots"], py["roots"])
        for a, b in zip(js["roots"], py["roots"]):
            close(a, b, f"B {name} root", rtol=1e-9, atol=1e-9)
        for key in ("k", "p21", "p12", "p11", "p22", "err", "cost", "thr"):
            close(js[key], py[key], f"B {name} {key}", rtol=1e-10, atol=1e-12)
        close(py["q21"], py["p21"], f"B {name} quad p21", rtol=0, atol=1e-9)
        close(py["q12"], py["p12"], f"B {name} quad p12", rtol=0, atol=1e-9)
        shown = o["text"]["perr"].split()[0]
        assert shown == pct(py["err"]), f"B {name}: page shows {shown}, python {pct(py['err'])}"
        no_garbage(o["text"], f"B {name}")
        print(f"  {name:22s} {p} | {js['kind']:9s} cut-offs {[round(x, 3) for x in py['roots']]} "
              f"p21 {py['p21']:.4f}/{js['p21']:.4f} p12 {py['p12']:.4f}/{js['p12']:.4f} "
              f"error {pct(py['err'])} (page {shown}; quad {pct(p['pi1'] * py['q21'] + (1 - p['pi1']) * py['q12'])}) "
              f"cost {py['cost']:.4f}/{js['cost']:.4f}")
        if name == "landmark sigma1=sigma2":
            assert abs(js["roots"][0] - 3) < 1e-12 and "exactly at the midpoint" in o["text"]["ident3"]
        if name == "no root":
            assert js["kind"] == "none" and "class 1" in o["text"]["verdict"]
        if name == "low ends":
            assert js["kind"] == "flat" and "class 2" in o["text"]["verdict"]
    sw = out[1 + len(vectors):-1]
    for i, k in enumerate(ranges):
        a, b = sw[2 * i], sw[2 * i + 1]
        assert (a["model"]["err"], a["model"]["roots"]) != (b["model"]["err"], b["model"]["roots"]), f"B control {k} inert"
        assert a["text"]["dens"] != b["text"]["dens"] or a["text"]["post"] != b["text"]["post"], f"B control {k} moves no chart"
        no_garbage(a["text"], f"B sweep {k} low")
        no_garbage(b["text"], f"B sweep {k} high")
    rs = out[-1]["reset"]
    assert {k: float(rs[k]) for k in ranges} == {k: float(v) for k, v in base.items()}, rs


if __name__ == "__main__":
    check_A()
    check_B()
    print("ALL CHECKS PASSED")
