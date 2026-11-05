"""Step 6 verification for the two Classes 3+4 companions (Notas/L03/companions/).

For each page: recompute every read-out in Python (numpy/scipy) from the model's expressions,
run the page's own `<script id="model">` block under node, and assert that both give the same
printed strings at both ends of the control ranges, the default, and landmark vectors. Then load
the full page script against a stub DOM, sweep every control end to end (and the landmark
buttons), and assert no NaN/undefined/Infinity/empty read-out reaches the page and that Reset
restores the default state. Finally assert the defaults reproduce the sources' numbers
(slide 40: 890.0 / 17.9; Greenberg Table 3.2).

Reuses the node runner, the stub DOM and the JS-rounding helper of
Notas/L01/companions/check_companions.py (loaded by path; it has the same module name).
Run: python Notas/L03/companions/check_companions.py   (needs node on PATH; exits non-zero on failure)
"""
import importlib.util
import json
import pathlib
import re
import sys

import numpy as np
from scipy import integrate, stats
from scipy.special import betaln, gammaln

HERE = pathlib.Path(__file__).resolve().parent
_spec = importlib.util.spec_from_file_location("l01cc", HERE.parents[1] / "L01" / "companions" / "check_companions.py")
l01 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(l01)
scripts, node, fx, compare, STUB = l01.scripts, l01.node, l01.fx, l01.compare, l01.STUB

PC_PAGE = HERE / "companion-normal-prior-conflict.html"
BF_PAGE = HERE / "companion-bayes-factor-coins.html"


def fs(x, d):
    s = fx(x, d)
    return s[1:] if re.fullmatch(r"-0\.?0*", s) else s


def fg(x):
    """Page's fg: 3 dp, or toExponential(2) when 0 < |x| < 0.001 or |x| >= 1e4."""
    if x != 0 and (abs(x) < 0.001 or abs(x) >= 1e4):
        return re.sub(r"e([+-])0*(\d)", r"e\1\2", f"{x:.2e}")
    return fx(x, 3)


# ---------- L03-a prior conflict ----------
def grid_post(x, sig, mu0, tau0, nu, kind, n=4001):
    """Same quadrature as the page: trapezoid on n points over min(x,mu0)-10w .. max(x,mu0)+10w."""
    w = max(sig, tau0)
    lo, hi = min(x, mu0) - 10 * w, max(x, mu0) + 10 * w
    h = (hi - lo) / (n - 1)
    th = lo + np.arange(n) * h
    s2 = tau0**2 * (nu - 2) / nu
    nlog = lambda t, m, v: -0.5 * (np.log(2 * np.pi) + np.log(v)) - (t - m) ** 2 / (2 * v)
    if kind == "n":
        lp = nlog(th, mu0, tau0**2)
    else:
        z = (th - mu0) / np.sqrt(s2)
        lp = gammaln((nu + 1) / 2) - gammaln(nu / 2) - 0.5 * np.log(nu * np.pi * s2) - (nu + 1) / 2 * np.log1p(z * z / nu)
    lp = lp + nlog(x, th, sig**2)
    d = np.exp(lp - lp.max())
    trap = lambda f: float(np.sum(h * (f[1:] + f[:-1]) / 2))
    Z = trap(d)
    mean = trap(th * d) / Z
    sd = np.sqrt(max(trap(th * th * d) / Z - mean**2, 0))
    inc = h * (d[1:] + d[:-1]) / 2 / Z
    i = int(np.argmax(th[1:] >= x))                      # first i with th[i+1] >= x
    P = float(inc[:i].sum() + inc[i] * (x - th[i]) / h)
    return mean, sd, P


def pc_python(x, sig, mu0, tau0, nu):
    v = sig**2 + tau0**2
    w = sig**2 / v
    n_mean, n_sd = w * mu0 + (1 - w) * x, np.sqrt(w * tau0**2)
    _, _, nP = grid_post(x, sig, mu0, tau0, nu, "n")
    t_mean, t_sd, tP = grid_post(x, sig, mu0, tau0, nu, "t")
    pull = "— (x = μ₀)" if x == mu0 else fs((x - t_mean) / (x - mu0), 3)
    return {"nMean": fs(n_mean, 1), "nSd": fs(n_sd, 1), "w": fx(w, 3), "nP": fx(nP, 3), "tMean": fs(t_mean, 1),
            "tSd": fs(t_sd, 1), "tP": fx(tP, 3), "tPull": pull, "s": fx(np.sqrt(tau0**2 * (nu - 2) / nu), 1),
            "predSd": fx(np.sqrt(v), 1), "z": fs((x - mu0) / np.sqrt(v), 2), "gap": fs(t_mean - n_mean, 1)}, (n_mean, t_mean, tP)


def t_post_quad(x, sig, mu0, tau0, nu):
    """Independent check by adaptive quadrature: posterior mean and P(theta < x) under the t prior."""
    s = np.sqrt(tau0**2 * (nu - 2) / nu)
    f = lambda t: stats.t.pdf((t - mu0) / s, nu) / s * stats.norm.pdf(x, t, sig)
    lo, hi = min(x, mu0) - 40 * max(sig, tau0), max(x, mu0) + 40 * max(sig, tau0)
    pts = sorted({x, mu0})
    Z = integrate.quad(f, lo, hi, points=pts, limit=400)[0]
    return (integrate.quad(lambda t: t * f(t), lo, hi, points=pts, limit=400)[0] / Z,
            integrate.quad(f, lo, x, limit=400)[0] / Z)


PC_VECS = {  # (x, sig, mu0, tau0, nu)
    "low ends": (600, 5, 600, 5, 3),
    "default": (850, 40, 900, 20, 5),
    "high ends": (1100, 120, 1100, 200, 60),
    "strong conflict": (1100, 40, 900, 20, 5),
    "mixed ends": (600, 5, 1100, 200, 3),
    "physicist B": (850, 40, 800, 80, 5),
}


def check_pc():
    model, ui = scripts(PC_PAGE)
    keys = ("x", "sig", "mu0", "tau0", "nu")
    vecs = [dict(zip(keys, v)) for v in PC_VECS.values()]
    js = node(model + f"\nconsole.log(JSON.stringify({json.dumps(vecs)}.map(readouts)));")
    out = {}
    for (name, v), pg in zip(PC_VECS.items(), js):
        py, raw = pc_python(*v)
        compare("prior conflict", name, py, pg)
        out[name] = (v, py, pg)
        if name in ("default", "strong conflict", "physicist B"):
            qm, qp = t_post_quad(*v)
            assert abs(raw[1] - qm) < 0.05 and abs(raw[2] - qp) < 1e-3, (name, raw, qm, qp)
    d, b = js[1], js[5]
    assert (d["nMean"], d["nSd"], d["w"], d["tMean"], d["s"]) == ("890.0", "17.9", "0.800", "891.1", "15.5"), d
    assert (b["nMean"], b["nSd"]) == ("840.0", "35.8"), b
    assert js[0]["tPull"] == js[2]["tPull"] == "— (x = μ₀)"
    sc = js[3]
    assert float(sc["tMean"]) - float(sc["nMean"]) > 50 and float(sc["tPull"]) < float(sc["w"])  # t prior gives way
    sweep = r"""
const OUTS = ["ans-n","ans-t","verdict","side1","side2","o-x","o-sig","o-mu0","o-tau0","o-nu","tbl","pd","pm","tnote"];
const D0 = snap(); check("load");
for(const [id, vs] of [["x",[600,1100]],["sig",[5,120]],["mu0",[600,1100]],["tau0",[5,200]],["nu",[3,60]]]){
  for(const v of vs){ fire("reset","click"); set(id, v); check(id + "=" + v); } }
fire("reset","click");
for(let x=600; x<=1100; x+=25){ set("x", x); check("x=" + x); }
for(const b of ["go-a","go-b","go-eq"]){ fire(b,"click"); check(b); }
fire("reset","click"); fire("go-eq","click"); const eq = els["verdict"].textContent;
fire("reset","click"); set("x", 1100); const strong = els["verdict"].textContent;
fire("reset","click");
console.log(JSON.stringify({bad, reset: snap() === D0, eq, strong}));
"""
    r = node(STUB + model + ui + sweep)
    assert not r["bad"], r["bad"][:10]
    assert r["reset"], "Reset did not restore the default state"
    assert r["eq"].startswith("No conflict") and r["strong"].startswith("Strong conflict"), r
    return out


# ---------- L03-b Bayes factor ----------
def jeffreys(L):
    if L == 0:
        return "neither model favoured"
    a, side = abs(L), "M1" if L > 0 else "M2"
    g = ("decisive support" if a > 2 else "very strong evidence" if a > 1.5 else "strong evidence" if a > 1
         else "substantial evidence" if a > 0.5 else "weak evidence")
    return f"{g} for {side}"


def bf_python(m, s1, s2, la, lo):
    al = 10.0**la
    lm1 = (betaln(al + s1 + s2, al + 2 * m - s1 - s2) - betaln(al, al)) / np.log(10)
    lm2 = (betaln(al + s1, al + m - s1) + betaln(al + s2, al + m - s2) - 2 * betaln(al, al)) / np.log(10)
    L = lm1 - lm2
    xl = lambda x, y: 0.0 if x == 0 else x * np.log(y)
    n, s = 2 * m, s1 + s2
    ll1 = xl(s, s / n) + xl(n - s, 1 - s / n)
    ll2 = xl(s1, s1 / m) + xl(m - s1, 1 - s1 / m) + xl(s2, s2 / m) + xl(m - s2, 1 - s2 / m)
    bic = (ll1 - ll2 + 0.5 * np.log(n)) / np.log(10)
    with np.errstate(over="ignore"):
        post = 1 / (1 + 10.0 ** (-(L + lo)))
        B = 10.0**L
    return {"L": fs(L, 3), "B": fg(B), "post": fg(post), "label": jeffreys(L), "bic": fs(bic, 3), "lm1": fs(lm1, 3),
            "lm2": fs(lm2, 3), "al": fg(al), "odds": fg(10.0**lo), "th1": fx(s1 / m, 3), "th2": fx(s2 / m, 3),
            "th": fx((s1 + s2) / (2 * m), 3)}


BF_VECS = {  # (m, s1, s2, la, lo)
    "low ends": (1, 0, 0, -1.0, -2.0),
    "default": (10, 2, 8, 0.0, 0.0),
    "high ends": (200, 200, 200, 1.301, 2.0),
    "opposite extremes": (200, 0, 200, 0.0, 0.0),
    "fair-coin prior": (100, 50, 50, 1.301, 0.0),
}
TABLE32 = [(10, 1, 9, "-2.506"), (10, 2, 8, "-1.200"), (10, 3, 7, "-0.348"), (10, 4, 6, "0.138"), (10, 5, 5, "0.297"),
           (100, 10, 90, "-30.775"), (100, 20, 80, "-15.793"), (100, 30, 70, "-6.316"), (100, 40, 60, "-0.975"),
           (100, 50, 50, "0.756")]


def check_bf():
    model, ui = scripts(BF_PAGE)
    keys = ("m", "s1", "s2", "la", "lo")
    allv = list(BF_VECS.values()) + [(m, a, b, 0.0, 0.0) for m, a, b, _ in TABLE32]
    js = node(model + f"\nconsole.log(JSON.stringify({json.dumps([dict(zip(keys, v)) for v in allv])}.map(readouts)));")
    out = {}
    for i, (v, pg) in enumerate(zip(allv, js)):
        name = list(BF_VECS)[i] if i < len(BF_VECS) else f"Table 3.2 {v[:3]}"
        py = bf_python(*v)
        compare("bayes factor", name, py, pg)
        if i < len(BF_VECS):
            out[name] = (v, py, pg)
    for (m, a, b, printed), pg in zip(TABLE32, js[len(BF_VECS):]):
        assert pg["L"] == printed, (m, a, b, pg["L"], printed)
    d = js[1]
    assert d["L"] == "-1.200" and d["label"] == "strong evidence for M2" and d["al"] == "1.000"
    sweep = r"""
const OUTS = ["ans","verdict","side1","side2","o-m","o-s1","o-s2","o-la","o-lo","tbl","pb","pp","tnote"];
const D0 = snap(); check("load");
for(const [id, vs] of [["m",[1,200]],["s1",[0,10]],["s2",[0,10]],["la",[-1,1.301]],["lo",[-2,2]]]){
  for(const v of vs){ fire("reset","click"); set(id, v); check(id + "=" + v); } }
fire("reset","click");
for(let m=1; m<=200; m+=7){ set("m", m); set("s1", m); set("s2", 0); check("m=" + m); }
fire("reset","click");
for(let s=0; s<=10; s++){ set("s2", s); check("s2=" + s); }
for(let i=0; i<10; i++){ fire("row" + i,"click"); check("row" + i); }
const row9 = els["ans"].textContent;
fire("reset","click"); set("m", 4); const clamped = [els["s1"].value, els["s2"].value, els["s2"].max];
fire("reset","click");
console.log(JSON.stringify({bad, reset: snap() === D0, row9, clamped}));
"""
    r = node(STUB + model + ui + sweep)
    assert not r["bad"], r["bad"][:10]
    assert r["reset"], "Reset did not restore the default state"
    assert r["row9"] == "0.756", r["row9"]
    assert [str(c) for c in r["clamped"]] == ["2", "4", "4"], r["clamped"]   # s2 = 8 clamped to m = 4
    return out


def report(title, out, keys):
    print(f"\n{title}")
    for name, (v, py, pg) in out.items():
        print(f"  {name} {v}")
        for k in keys:
            print(f"    {k:<7} python {py[k]:<34} page {pg[k]}")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    pc = check_pc()
    report("L03-a The Prior-Conflict Dial", pc, ["nMean", "nSd", "w", "tMean", "tSd", "tP", "tPull", "z"])
    bf = check_bf()
    report("L03-b The Bayes-Factor Dial", bf, ["L", "B", "post", "label", "bic"])
    print("\nALL CHECKS PASSED")
