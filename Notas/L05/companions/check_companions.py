"""Step 6 verification for the Classes 5+6 companions (Notas/L05/companions/).

Runs each page's own <script> blocks under node with a stub DOM (harness copied from
Notas/L02/companions/check_companions.py), then checks:
  * every model read-out against an independent numpy recomputation at three control vectors
    (both ends of the ranges and the default) plus edge cases, and the displayed strings;
  * the Instrument Dial's defaults against card.csv (OLS 0.0746933, IV 0.1315038 from L05_python_checks);
  * the Discontinuity Window against mf.rdd_fit (numpy lstsq) and the site's printed jumps;
  * every control sweeps (changes a read-out), reset restores the defaults, no NaN/undefined in any text.

Usage: python Notas/L05/companions/check_companions.py   (needs node on PATH; numpy, pandas)
Fails with AssertionError naming the first disagreement.
"""
import json
import pathlib
import subprocess
import sys
import tempfile

import numpy as np

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "figures"))
import make_figures as mf  # noqa: E402

PAGE_A = HERE / "companion-iv-plims.html"
PAGE_B = HERE / "companion-rdd-window.html"

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


def fmt4(x):
    return ("−" if x < 0 else "") + f"{abs(x):.4f}"


def sg4(x):
    return ("−" if x < 0 else "+") + f"{abs(x):.4f}"


# ---------------------------------------------------------------- page A: the Instrument Dial
def py_A(b1, rho, d1, phi, n):
    """Independent recomputation by building the population covariance of (z, x, y) and taking moments."""
    sz, sx, sy = mf.IV_SZ, mf.IV_SX, mf.IV_SY
    # (z, ex, ey) covariance, then (z, x, y) = A (z, ex, ey)
    S0 = np.array([[sz**2, 0, 0], [0, sx**2, rho * sx * sy], [0, rho * sx * sy, sy**2]])
    A = np.array([[1, 0, 0], [d1, 1, 0], [b1 * d1 + phi, b1, 1]])
    S = A @ S0 @ A.T
    vz, vx, vy, czx, czy, cxy = S[0, 0], S[1, 1], S[2, 2], S[0, 1], S[0, 2], S[1, 2]
    ols = cxy / vx
    iv = czy / czx if d1 != 0 else None
    G = S[:2, :2][::-1, ::-1]                      # regressors (x, z)
    longx, longz = np.linalg.solve(G, [cxy, czy])
    R2 = czx**2 / (vz * vx)
    F = n * R2 / (1 - R2)
    se_ols = np.sqrt((vy - cxy**2 / vx) / (n * vx))
    se_iv = np.sqrt((vy - 2 * iv * cxy + iv**2 * vx) / (n * vx * R2)) if iv is not None else None
    return dict(ols=ols, iv=iv, longx=longx, longz=longz, R2=R2, F=F, seOls=se_ols, seIv=se_iv)


def check_A():
    expr = "(() => { const r = compute(__p); return r; })()"
    D = dict(b1=0.1315, rho=-0.2851, d1=0.3199, phi=0.0, n=3010)
    vectors = {"low ends": dict(b1=-0.1, rho=-0.9, d1=-1.5, phi=-0.1, n=100), "default": D,
               "high ends": dict(b1=0.4, rho=0.9, d1=1.5, phi=0.1, n=20000),
               "rho = 0, phi = 0": dict(D, rho=0.0), "weak, violated": dict(D, d1=0.05, phi=0.005)}
    jobs = [dict(p=p, expr=expr, ui=p) for p in vectors.values()]
    jobs.append(dict(p=dict(D, d1=0.0), expr=expr, ui=dict(D, d1=0.0)))                 # no instrument
    sweeps = [("b1", -0.1, 0.4), ("rho", -0.9, 0.9), ("d1", -1.5, 1.5), ("phi", -0.1, 0.1), ("n", 100, 20000)]
    for k, lo, hi in sweeps:
        for v in (lo, hi):
            jobs.append(dict(p=dict(D, **{k: v}), expr=expr, ui=dict(D, **{k: v})))
    out = run_node(PAGE_A, jobs)
    rows = []
    for (name, p), o in zip(vectors.items(), out):
        js, py = o["model"], py_A(**p)
        for key in ("ols", "iv", "longx", "longz", "R2", "F", "seOls", "seIv"):
            close(js[key], py[key], f"A {name} {key}", rtol=1e-6)
        assert o["text"]["biv"].strip() == "IV " + sg4(py["iv"] - p["b1"]), (name, o["text"]["biv"])
        assert o["text"]["bols"].strip() == "OLS " + sg4(py["ols"] - p["b1"]), (name, o["text"]["bols"])
        no_garbage(o["text"], f"A {name}")
        rows.append((name, p, py["ols"], py["iv"], js["ols"], js["iv"]))
    d = vectors["default"]
    pyd = py_A(**d)
    assert abs(pyd["ols"] - 0.0746933) < 5e-5 and abs(pyd["iv"] - 0.1315) < 1e-12, pyd
    zero = py_A(**vectors["rho = 0, phi = 0"])
    assert abs(zero["ols"] - zero["iv"]) < 1e-4                    # rho = 0: only the tiny phi-free gap 0
    noiv = out[len(vectors)]
    assert noiv["model"]["iv"] is None and noiv["model"]["hasIV"] is False and noiv["model"]["F"] == 0
    assert "IV not defined" in noiv["text"]["biv"]
    no_garbage(noiv["text"], "A no instrument")
    sw = out[len(vectors) + 1: len(vectors) + 1 + 2 * len(sweeps)]
    for i, (k, lo, hi) in enumerate(sweeps):
        ta, tb, t0 = sw[2 * i]["text"], sw[2 * i + 1]["text"], out[1]["text"]      # out[1] = defaults
        for tt, v in ((ta, lo), (tb, hi)):                     # each end vs the defaults (delta1 = +-1.5 are mirror images)
            assert tt["plims"] != t0["plims"] or tt["bias"] != t0["bias"], f"A control {k}={v} does not move a chart"
            assert tt["tbl"] != t0["tbl"], f"A control {k}={v} does not move the read-outs"
        no_garbage(ta, f"A sweep {k}={lo}")
        no_garbage(tb, f"A sweep {k}={hi}")
    rs = out[-1]["reset"]
    assert {k: float(rs[k]) for k in D} == {k: float(v) for k, v in D.items()}, rs
    return rows


# ---------------------------------------------------------------- page B: the Discontinuity Window
def py_B(outc, bw, ord, inter, a0):
    import pandas as pd
    d = pd.read_csv(mf.DATA / "age-mva-internal.txt", sep=r"\s+")
    j, se, s, n, _ = mf.rdd_fit(d.age.values, d[outc].values, a0=a0, b=bw + 1e-9, p=ord, inter=(inter == "on"))
    return dict(jump=j, se=se, sigma=s, n=n)


def check_B():
    expr = "(() => fit(__p))()"
    D = dict(outc="mva", bw=2.0, ord=1, inter="off", a0=21.0)
    vectors = {"default (site linear)": D, "low ends": dict(outc="internal", bw=0.3, ord=1, inter="off", a0=19.8),
               "high ends": dict(outc="mva", bw=2.0, ord=2, inter="on", a0=22.2),
               "site quadratic": dict(D, ord=2, inter="on"), "internal linear": dict(D, outc="internal"),
               "local linear b = 1": dict(D, bw=1.0, inter="on")}
    jobs = [dict(p=p, expr=expr, ui=p) for p in vectors.values()]
    bad = dict(outc="mva", bw=0.3, ord=2, inter="on", a0=19.8)                      # fewest residual df in the control space
    jobs.append(dict(p=bad, expr=expr, ui=bad))
    sweeps = [("outc", "mva", "internal"), ("bw", 0.3, 2.0), ("ord", 1, 2), ("inter", "off", "on"), ("a0", 19.8, 22.2)]
    for k, lo, hi in sweeps:
        for v in (lo, hi):
            jobs.append(dict(p=dict(D, **{k: v}), expr=expr, ui=dict(D, **{k: v})))
    out = run_node(PAGE_B, jobs)
    rows = []
    for (name, p), o in zip(vectors.items(), out):
        js, py = o["model"], py_B(**p)
        assert js["ok"], (name, js.get("why"))
        assert js["n"] == py["n"], (name, js["n"], py["n"])
        for key in ("jump", "se", "sigma"):
            close(js[key], py[key], f"B {name} {key}", rtol=1e-8)
        shown = o["text"]["jump"].strip()
        want = ("−" if py["jump"] < 0 else "") + f"{abs(py['jump']):.3f} ± {1.96 * py['se']:.3f}"
        assert shown == want, (name, shown, want)
        no_garbage(o["text"], f"B {name}")
        rows.append((name, p, py["jump"], py["se"], js["jump"], js["se"]))
    m = {name: o["model"] for name, o in zip(vectors, out)}
    assert abs(m["default (site linear)"]["jump"] - 4.534) < 5e-4 and abs(m["default (site linear)"]["z"] - 3.411) < 5e-4
    assert abs(m["site quadratic"]["z"] - 3.508) < 5e-4 and abs(m["internal linear"]["z"] - 0.380) < 5e-4
    nb = out[len(vectors)]
    py = py_B(**bad)
    assert nb["model"]["ok"] and nb["model"]["dof"] >= 1 and nb["model"]["n"] == py["n"]   # the narrowest window still fits
    close(nb["model"]["jump"], py["jump"], "B narrowest window jump", rtol=1e-7)
    no_garbage(nb["text"], "B degenerate window")
    sw = out[len(vectors) + 1: len(vectors) + 1 + 2 * len(sweeps)]
    for i, (k, lo, hi) in enumerate(sweeps):
        ta, tb = sw[2 * i]["text"], sw[2 * i + 1]["text"]
        assert ta["jump"] != tb["jump"] and ta["scatter"] != tb["scatter"], f"B control {k} does not move the page"
        no_garbage(ta, f"B sweep {k}={lo}")
        no_garbage(tb, f"B sweep {k}={hi}")
    rs = out[-1]["reset"]
    assert (rs["outc"], float(rs["bw"]), int(float(rs["ord"])), rs["inter"], float(rs["a0"])) == ("mva", 2.0, 1, "off", 21.0), rs
    return rows


if __name__ == "__main__":
    for name, p, po, pi, jo, ji in check_A():
        print(f"A {name:18s} {p}: python OLS {po:.6f} IV {pi:.6f} | page OLS {jo:.6f} IV {ji:.6f}")
    for name, p, pj, ps, jj, js in check_B():
        print(f"B {name:22s} {p}: python jump {pj:.4f} (se {ps:.4f}) | page {jj:.4f} ({js:.4f})")
    print("ALL L05 COMPANION CHECKS PASSED")
