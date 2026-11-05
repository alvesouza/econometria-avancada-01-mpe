"""Step 6 verification for the Class 7 companions (Notas/L07/companions/).

Runs each page's own <script> blocks under node with a stub DOM (harness of Notas/L02/companions/
check_companions.py), then checks:
  * every read-out against an independent numpy/scipy recomputation at three control vectors (both
    ends of the ranges and the defaults) plus the landmarks, and the displayed answer strings;
  * the Partial-Pooling Dial's marginal p(tau | y) against scipy's multivariate normal density (a
    different route from the page's determinant-lemma formula) on the page's own grid;
  * the Censoring Dial against Monte Carlo (P(y = 0), the OLS slope) and its Phi against scipy;
  * every control sweeps (changes a read-out and a chart), reset restores defaults, no NaN/undefined.

Usage: python Notas/L07/companions/check_companions.py   (needs node on PATH; numpy, scipy)
Fails with AssertionError naming the first disagreement.
"""
import json
import pathlib
import subprocess
import tempfile

import numpy as np
from scipy import stats

HERE = pathlib.Path(__file__).resolve().parent
PAGE_A = HERE / "companion-partial-pooling.html"
PAGE_B = HERE / "companion-tobit-censoring.html"

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


def fmt2(x):
    return ("−" if x < 0 and round(abs(x), 2) != 0 else "") + f"{abs(x):.2f}"


def fmt3(x):
    return ("−" if x < 0 and round(abs(x), 3) != 0 else "") + f"{abs(x):.3f}"


# ---------------------------------------------------------------- page A: the Partial-Pooling Dial
Y8 = np.array([28.39, 7.94, -2.75, 6.82, -0.64, 0.63, 18.01, 12.16])
S8 = np.array([14.9, 10.2, 16.3, 11.0, 9.4, 11.4, 10.4, 17.6])


def py_A(tau, A, kap, sch):
    """Independent route: scipy multivariate normal for p(tau | y); explicit normal-normal algebra given tau."""
    kappa = 2 ** (kap / 10)
    d = S8 ** 2 / kappa
    g = np.linspace(0, 100, 2001)
    lp = np.array([stats.multivariate_normal(np.zeros(8), np.diag(d + t ** 2) + 1e6).logpdf(Y8) if t < A else -np.inf
                   for t in g])
    p = np.exp(lp - lp[np.isfinite(lp)].max())
    p /= np.trapezoid(p, g)
    cdf = np.concatenate([[0], np.cumsum((p[1:] + p[:-1]) / 2 * np.diff(g))])
    med = float(np.interp(0.5, cdf, g))

    def cond(t):
        prec = 1e-6 + np.sum(1 / (d + t ** 2))
        mu = np.sum(Y8 / (d + t ** 2)) / prec
        B = d / (d + t ** 2) if t > 0 else np.ones(8)
        return mu, 1 / prec, B, (1 - B) * Y8 + B * mu, np.sqrt((1 - B) * d + B ** 2 / prec)

    mu, vmu, B, mean, sd = cond(tau)
    fb = np.trapezoid(np.array([cond(t)[3] for t in g]) * p[:, None], g, axis=0)
    return dict(mu=mu, vmu=vmu, B=B[sch], mean=mean[sch], sd=sd[sch], fb=fb[sch], median=med)


def check_A():
    expr = ("(() => { const r = compute(__p); return {mu:r.mu, vmu:r.vmu, B:r.B, mean:r.mean, sd:r.sd, fb:r.fb,"
            " median:r.median}; })()")
    vectors = {"low ends": dict(tau=0.0, A=5, kap=-20, sch=0), "default": dict(tau=5.2, A=100, kap=0, sch=0),
               "high ends": dict(tau=40.0, A=100, kap=40, sch=7), "school C at default": dict(tau=5.2, A=100, kap=0, sch=2)}
    jobs = [dict(p=p, expr=expr, ui=p) for p in vectors.values()]
    ranges = dict(tau=(0.0, 40.0), A=(5, 100), kap=(-20, 40), sch=(0, 7))
    base = vectors["default"]
    for k, (lo, hi) in ranges.items():
        for v in (lo, hi):
            jobs.append(dict(p={**base, k: v}, expr=expr, ui={**base, k: v}))
    out = run_node(PAGE_A, jobs)
    print("Partial-Pooling Dial: page (node) vs python")
    for (name, p), o in zip(vectors.items(), out):
        js, py = o["model"], py_A(**p)
        for key in ("mu", "vmu", "B", "mean", "sd"):
            close(js[key], py[key], f"A {name} {key}", rtol=1e-9, atol=1e-10)
        for key in ("fb", "median"):
            close(js[key], py[key], f"A {name} {key}", rtol=1e-6, atol=1e-6)
        shown = o["text"]["ans"].split()[0]
        assert shown == fmt2(py["mean"]), f"A {name}: page shows {shown}, python {fmt2(py['mean'])}"
        no_garbage(o["text"], f"A {name}")
        print(f"  {name:20s} {p} | E(theta|y,tau) {fmt2(py['mean'])} (page {shown}) B {py['B']:.4f}/{js['B']:.4f} "
              f"mu {py['mu']:.3f}/{js['mu']:.3f} fully Bayes {py['fb']:.3f}/{js['fb']:.3f} median tau {py['median']:.3f}/{js['median']:.3f}")
        if name == "low ends":
            assert "Complete pooling" in o["text"]["verdict"] and abs(js["mean"] - js["mu"]) < 1e-12
        if name == "default":
            assert abs(js["median"] - 5.228) < 2e-3 and round(js["median"], 1) == 5.2   # default tau = rounded median
            assert "τ at the posterior median" in o["text"]["chips"] and "● τ at" in o["text"]["chips"]
        if name == "school C at default":
            assert js["mean"] > Y8[2] and "<strong>up</strong>" in o["text"]["verdict"]
    sw = out[len(vectors):-1]
    for i, k in enumerate(ranges):
        a, b = sw[2 * i], sw[2 * i + 1]
        assert a["model"] != b["model"], f"A control {k} inert"
        assert a["text"]["paths"] != b["text"]["paths"] or a["text"]["post"] != b["text"]["post"] or a["text"]["tbl"] != b["text"]["tbl"], f"A control {k} moves nothing"
        no_garbage(a["text"], f"A sweep {k} low")
        no_garbage(b["text"], f"A sweep {k} high")
    rs = out[-1]["reset"]
    assert {k: float(rs[k]) for k in ranges} == {k: float(v) for k, v in base.items()}, rs


# ---------------------------------------------------------------- page B: the Censoring Dial
def py_B(beta, sig, a, x0):
    """scipy for everything; the pointwise terms in 50-digit mpmath (exact reference even at z = -120)."""
    import mpmath as mp
    mp.mp.dps = 50
    zm = mp.mpf(beta) * mp.mpf(x0) / mp.mpf(sig)
    lm = mp.npdf(zm) / mp.ncdf(zm)
    epos_m, dpos_m = mp.mpf(beta) * x0 + mp.mpf(sig) * lm, mp.mpf(beta) * (1 - lm * (zm + lm))
    s = np.hypot(beta, sig)
    m = a * beta
    p0 = stats.norm.cdf(-m / s)
    z = beta * x0 / sig
    lam = np.exp(stats.norm.logpdf(z) - stats.norm.logcdf(z))
    return dict(p0=p0, olsSlope=beta * stats.norm.sf(-m / s), z=z, lam=lam, ppos=stats.norm.cdf(z),
                epos=float(epos_m), eall=stats.norm.cdf(z) * beta * x0 + sig * stats.norm.pdf(z),
                dall=beta * stats.norm.cdf(z), dpos=float(dpos_m),
                Ey=stats.norm.cdf(m / s) * m + s * stats.norm.pdf(m / s))


def check_B():
    expr = "(() => { const r = compute(__p); return r; })()"
    vectors = {"low ends": dict(beta=0.1, sig=0.1, a=-4.0, x0=-3.0), "default": dict(beta=2.0, sig=0.5, a=0.7, x0=0.0),
               "high ends": dict(beta=4.0, sig=3.0, a=4.0, x0=3.0), "landmark a = 0": dict(beta=2.0, sig=0.5, a=0.0, x0=0.0),
               "landmark a = 1.3": dict(beta=2.0, sig=0.5, a=1.3, x0=0.0), "deep tail z = -120": dict(beta=4.0, sig=0.1, a=0.0, x0=-3.0)}
    zs = [float(z) for z in np.arange(-40, 40.0001, 0.01)]
    jobs = [dict(p={"z": zs}, expr="[__p.z.map(Phi), __p.z.map(mills)]", ui=None)]
    jobs += [dict(p=p, expr=expr, ui=p) for p in vectors.values()]
    ranges = dict(beta=(0.1, 4.0), sig=(0.1, 3.0), a=(-4.0, 4.0), x0=(-3.0, 3.0))
    base = vectors["default"]
    for k, (lo, hi) in ranges.items():
        for v in (lo, hi):
            jobs.append(dict(p={**base, k: v}, expr=expr, ui={**base, k: v}))
    out = run_node(PAGE_B, jobs)
    Phi_js, mills_js = (np.array([float(v) for v in arr]) for arr in out[0]["model"])
    zz = np.array(zs)
    e1 = np.max(np.abs(Phi_js - stats.norm.cdf(zz)))
    mills_py = np.exp(stats.norm.logpdf(zz) - stats.norm.logcdf(zz))
    ok = mills_py > 1e-300                                   # lambda underflows to 0 for z > ~38 on both sides
    e2 = np.max(np.abs(mills_js[ok] / mills_py[ok] - 1))
    assert np.all(np.abs(mills_js[~ok]) < 1e-300)
    print(f"Censoring Dial: max |Phi_page - scipy| = {e1:.2e}; max relative error of lambda over [-40, 40] = {e2:.2e}")
    assert e1 < 1e-13 and e2 < 1e-10
    for (name, p), o in zip(vectors.items(), out[1:1 + len(vectors)]):
        js, py = o["model"], py_B(**p)
        for key in py:
            close(js[key], py[key], f"B {name} {key}", rtol=1e-9, atol=1e-12)
        shown = o["text"]["ans"].split()[0]
        assert shown == fmt3(py["p0"]), f"B {name}: page shows {shown}, python {fmt3(py['p0'])}"
        no_garbage(o["text"], f"B {name}")
        print(f"  {name:20s} {p} | P(y=0) {fmt3(py['p0'])} (page {shown}) OLS slope {py['olsSlope']:.4f}/{js['olsSlope']:.4f} "
              f"E(y|x0) {py['eall']:.4f}/{js['eall']:.4f} dE/dx {py['dall']:.4f}/{js['dall']:.4f}")
    # landmarks: slide 9's 0.5, 0.25, 0.1
    landmark = {"default": 0.25, "landmark a = 0": 0.5, "landmark a = 1.3": 0.10}
    for (name, p), o in zip(vectors.items(), out[1:1 + len(vectors)]):
        if name in landmark:
            assert round(o["model"]["p0"], 2) == landmark[name], (name, o["model"]["p0"])
            assert "chip on" in o["text"]["chips"]
    # Monte Carlo at the defaults: P(y = 0) and the population OLS slope
    rng = np.random.default_rng(13)
    x = rng.normal(0.7, 1, 2_000_000)
    y = np.maximum(0, 2 * x + 0.5 * rng.normal(size=x.size))
    d = out[2]["model"]
    assert abs(np.mean(y == 0) - d["p0"]) < 1.5e-3 and abs(np.polyfit(x, y, 1)[0] - d["olsSlope"]) < 4e-3
    print(f"  Monte Carlo (2e6 draws, seed 13): P(y=0) {np.mean(y == 0):.4f} vs {d['p0']:.4f}; OLS slope {np.polyfit(x, y, 1)[0]:.4f} vs {d['olsSlope']:.4f}")
    sw = out[1 + len(vectors):-1]
    for i, k in enumerate(ranges):
        a, b = sw[2 * i], sw[2 * i + 1]
        assert a["model"] != b["model"], f"B control {k} inert"
        assert a["text"]["means"] != b["text"]["means"] or a["text"]["dist"] != b["text"]["dist"], f"B control {k} moves no chart"
        no_garbage(a["text"], f"B sweep {k} low")
        no_garbage(b["text"], f"B sweep {k} high")
    rs = out[-1]["reset"]
    assert {k: float(rs[k]) for k in ranges} == {k: float(v) for k, v in base.items()}, rs


if __name__ == "__main__":
    check_A()
    check_B()
    print("ALL CHECKS PASSED")
