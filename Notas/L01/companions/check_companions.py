"""Step 6 verification for the two Class 1 companions (Notas/L01/companions/).

For each page: recompute every read-out in Python (numpy/scipy) from the model's expressions,
run the page's own `<script id="model">` block under node, and assert that both give the same
printed strings at three control vectors (both ends of the ranges and the default), plus the
degenerate vectors. Then load the full page script against a stub DOM, sweep every control end
to end (and the landmark buttons), and assert no NaN/undefined/Infinity ever reaches the page and
that Reset restores the default state. Finally assert the defaults reproduce the decks' numbers.

Run: python Notas/L01/companions/check_companions.py   (needs node on PATH; exits non-zero on failure)
"""
import json
import pathlib
import re
import subprocess
import sys
from decimal import ROUND_HALF_UP, Decimal
from fractions import Fraction

import numpy as np
from scipy.special import xlogy, logsumexp
from scipy.stats import chi2, norm

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[2]
CP_PAGE = HERE / "companion-poisson-change-point.html"
FE_PAGE = HERE / "companion-four-estimators-mse.html"


# ---------- helpers ----------
def scripts(page):
    html = page.read_text(encoding="utf-8")
    model = re.search(r'<script id="model">(.*?)</script>', html, re.S).group(1)
    ui = re.findall(r"<script>(.*?)</script>", html, re.S)[-1]
    return model, ui


def node(js):
    r = subprocess.run(["node", "-"], input=js, capture_output=True, text=True, encoding="utf-8")
    assert r.returncode == 0, r.stderr
    return json.loads(r.stdout)


def fx(x, d):
    """JS toFixed: exact binary value, ties away from zero (Python's format rounds ties to even: 0.0625 -> 0.062)."""
    return str(Decimal(float(x)).quantize(Decimal(1).scaleb(-d), rounding=ROUND_HALF_UP))


def fv(x):  # page's fv: 3 dp, or toExponential(2) below 0.001
    if x == 0 or abs(x) >= 0.001:
        return fx(x, 3)
    return re.sub(r"e([+-])0*(\d)", r"e\1\2", f"{x:.2e}")


def fs(x):
    s = fx(x, 3)
    return "0.000" if s == "-0.000" else s


def compare(name, vec, py, js):
    assert set(py) == set(js), f"{name} {vec}: key mismatch {set(py) ^ set(js)}"
    bad = {k: (py[k], js[k]) for k in py if py[k] != js[k]}
    assert not bad, f"{name} {vec}: python vs page differ {bad}"


STUB = r"""
const els = {};
function mk(id){ const h = {}; return {id, h, value:"", min:"", max:"", textContent:"", innerHTML:"", disabled:false, attrs:{},
  setAttribute(k,v){ this.attrs[k] = String(v); }, addEventListener(t,fn){ (h[t] = h[t] || []).push(fn); }}; }
globalThis.document = {getElementById: id => els[id] || (els[id] = mk(id))};
const fire = (id, t) => (els[id].h[t] || []).forEach(fn => fn());
const snap = () => Object.values(els).map(e => e.id + "|" + e.value + "|" + e.textContent + "|" + e.innerHTML + "|" + e.disabled + "|" + JSON.stringify(e.attrs)).join("\n");
const text = () => Object.values(els).map(e => e.textContent + " " + e.innerHTML).join("\n");
const bad = [];
function check(label){ const t = text(); const m = t.match(/NaN|undefined|Infinity|null/);
  if(m) bad.push(label + ": " + m[0]);
  for(const id of OUTS) if(!String(els[id].textContent || els[id].innerHTML).trim()) bad.push(label + ": empty " + id); }
function set(id, v){ els[id].value = v; fire(id, "input"); }
"""


# ---------- L01-a change point ----------
def coal_series():
    note = (ROOT / ".agent/notes/coal-mining-data.md").read_text(encoding="utf-8")
    vals = re.search(r"`(\d(?:,\d)+)`", note).group(1)
    return np.array([int(v) for v in vals.split(",")])


Y = coal_series()
YEARS = np.arange(1851, 1963)


def cp_python(a, b, tau, h, conf):
    y = Y[(YEARS >= a) & (YEARS <= b)]
    tau = min(max(tau, a), b - 1)
    ll = lambda seg: xlogy(seg.sum(), seg.sum() / len(seg)) - seg.sum()
    z = norm.ppf(1 - (1 - conf) / 2)
    taus = np.arange(a, b)
    lp = np.array([ll(y[: t - a + 1]) + ll(y[t - a + 1:]) for t in taus])
    im = int(np.argmax(lp))
    l0 = ll(y)
    i = tau - a
    lr = max(0.0, 2 * (lp[i] - l0))
    o = {"tau": str(tau), "LR1": fx(lr, 1), "LR2": fx(lr, 2),
         "LRmax": fx(max(0.0, 2 * (lp[im] - l0)), 2), "argmax": str(taus[im]), "gap": fx(lp[i] - lp[im], 2), "z": fx(z, 3)}
    wlo, whi = max(1890 - h, a), min(1890 + h, b - 1)
    if wlo > whi:
        o["w"] = "no τ in window"
    elif not (wlo <= tau <= whi):
        o["w"] = "τ outside window"
    else:
        win = lp[wlo - a: whi - a + 1]
        o["w"] = fx(np.exp(lp[i] - logsumexp(win)), 3)
    segs = {"full": y, "s1": y[: i + 1], "s2": y[i + 1:]}
    lam = {k: v.mean() for k, v in segs.items()}
    if lam["s2"] == 0:
        o["ratio"] = "undefined (both rates 0)" if lam["s1"] == 0 else "∞ (λ̂₂ = 0)"
    else:
        o["ratio"] = fx(lam["s1"] / lam["s2"], 3)
    for k, seg in segs.items():
        n, s, lm = len(seg), int(seg.sum()), seg.mean()
        se = np.sqrt(lm / n)
        lo = lm - z * se
        o[k + "_n"], o[k + "_s"], o[k + "_lam"], o[k + "_se"] = str(n), str(s), fx(lm, 3), fx(se, 3)
        o[k + "_ci"] = f"({fx(max(lo, 0.0), 3)}{'*' if lo < 0 or s == 0 else ''}, {fx(lm + z * se, 3)})"
        if n == 1:
            o[k + "_s2"] = o[k + "_idx"] = o[k + "_p"] = "n/a (n = 1)"
            continue
        s2 = seg.var(ddof=1)
        o[k + "_s2"] = fx(s2, 3)
        if s == 0:
            o[k + "_idx"] = o[k + "_p"] = "n/a (ȳ = 0)"
            continue
        p = chi2.sf((n - 1) * s2 / lm, n - 1)
        o[k + "_idx"] = fx(s2 / lm, 3)
        o[k + "_p"] = "< 0.001" if p < 0.0005 else fx(p, 3)
    return o


CP_VECS = {  # (a, b, tau, h, conf)
    "low ends": (1851, 1901, 1851, 1, 0.80),
    "default": (1851, 1962, 1891, 5, 0.95),
    "high ends": (1900, 1962, 1961, 40, 0.99),
    "degenerate: zero-count segment, empty window": (1900, 1961, 1960, 5, 0.95),
    "deck slide 14 split": (1851, 1962, 1890, 5, 0.95),
}


def check_cp():
    model, ui = scripts(CP_PAGE)
    page_data = re.search(r"const DIS = \[([\d,]+)\]", model).group(1)
    assert [int(v) for v in page_data.split(",")] == Y.tolist(), "embedded series differs from the verified note"
    assert len(Y) == 112 and Y.sum() == 191 and Y[:40].sum() == 125 and Y[:41].sum() == 127

    vecs = [dict(zip(("a", "b", "tau", "h", "conf"), v)) for v in CP_VECS.values()]
    deck18 = [dict(a=1851, b=1962, tau=t, h=5, conf=0.95) for t in range(1885, 1896)]
    js = node(model + f"\nconsole.log(JSON.stringify({json.dumps(vecs + deck18)}.map(readouts)));")
    out = {}
    for (name, v), pg in zip(CP_VECS.items(), js):
        py = cp_python(*v)
        compare("change point", name, py, pg)
        out[name] = (v, py, pg)
    zero = cp_python(*CP_VECS["degenerate: zero-count segment, empty window"])
    assert zero["s2_s"] == "0" and zero["s2_ci"] == "(0.000*, 0.000)" and zero["w"] == "no τ in window", zero

    d, s14 = js[1], js[4]
    assert (d["LR1"], d["LR2"], d["w"], d["s1_lam"], d["s2_lam"], d["ratio"], d["argmax"]) == \
        ("70.0", "69.99", "0.251", "3.098", "0.901", "3.436", "1891"), d
    assert (s14["full_lam"], s14["full_se"], s14["full_ci"], s14["full_s2"], s14["full_idx"], s14["full_p"]) == \
        ("1.705", "0.123", "(1.464, 1.947)", "2.714", "1.592", "< 0.001"), s14
    assert (s14["s1_lam"], s14["s1_se"], s14["s1_ci"], s14["s1_s2"], s14["s1_idx"], s14["s1_p"]) == \
        ("3.125", "0.280", "(2.577, 3.673)", "2.574", "0.824", "0.774"), s14
    assert (s14["s2_lam"], s14["s2_se"], s14["s2_ci"], s14["s2_s2"], s14["s2_idx"], s14["s2_p"]) == \
        ("0.917", "0.113", "(0.696, 1.138)", "1.063", "1.160", "0.168"), s14
    slide18 = [("3.229", "1.013", "-3.50", "0.008"), ("3.250", "0.974", "-1.02", "0.091"), ("3.216", "0.960", "-0.87", "0.105"),
               ("3.158", "0.959", "-1.89", "0.038"), ("3.154", "0.932", "-0.49", "0.154"), ("3.125", "0.917", "-0.26", "0.194"),
               ("3.098", "0.901", "0.00", "0.251"), ("3.048", "0.900", "-0.94", "0.098"), ("3.000", "0.899", "-1.86", "0.039"),
               ("2.955", "0.897", "-2.74", "0.016"), ("2.911", "0.896", "-3.59", "0.007")]
    for t, row, pg in zip(range(1885, 1896), slide18, js[len(vecs):]):
        assert (pg["s1_lam"], pg["s2_lam"], pg["gap"], pg["w"]) == row, (t, pg, row)

    sweep = r"""
const OUTS = ["lr","verdict","side1","side2","o-tau","o-a","o-b","o-h","o-conf","tbl","counts","profile","tnote"];
const D0 = snap(); check("load");
for(const [id, vs] of [["a",[1851,1900]],["b",[1901,1962]],["tau",[1800,2000]],["h",[1,40]],["conf",[0.80,0.99]]]){
  for(const v of vs){ fire("reset","click"); set(id, v); check(id + "=" + v); } }
fire("reset","click");
for(let t=1851; t<=1961; t++){ set("tau", t); check("tau=" + t); }
for(const [a,b] of [[1851,1901],[1900,1901],[1900,1962],[1851,1962],[1900,1961]]){
  for(const t of [a, b-1]){ set("a", a); set("b", b); set("tau", t); check(`a=${a} b=${b} tau=${t}`);
    fire("go-max","click"); check("go-max"); if(!els["go-1890"].disabled){ fire("go-1890","click"); check("go-1890"); } } }
fire("reset","click"); set("tau", 1890); const s1890 = els["side2"].textContent; set("tau", 1891); const s1891 = els["side2"].textContent;
fire("go-max","click"); const gm = els["tau"].value;
set("a", 1900); set("b", 1960); const dis = els["go-1890"].disabled;
fire("reset","click");
console.log(JSON.stringify({bad, reset: snap() === D0, s1890, s1891, gm, dis}));
"""
    r = node(STUB + model + ui + sweep)
    assert not r["bad"], r["bad"][:10]
    assert r["reset"], "Reset did not restore the default state"
    assert "at the 1890 split" in r["s1890"] and "1 year after the 1890 split" in r["s1891"], (r["s1890"], r["s1891"])
    assert "at the profile maximum 1891" in r["s1891"] and str(r["gm"]) == "1891", r
    assert r["dis"] is True, "1890 button must be disabled when 1890 is not an admissible cut"
    return out


# ---------- L01-b four estimators ----------
NAMES = ["θ̂₁", "θ̂₂", "θ̂₃", "θ̂₄"]


def moments(theta, n):
    """E and V from slide 3; works for float or Fraction theta."""
    E = [theta / 2, n * theta / (n + 1), theta, theta]
    V = [theta**2 / (12 * n), n * theta**2 / ((n + 1) ** 2 * (n + 2)), theta**2 / (3 * n), theta**2 / (n * (n + 2))]
    return E, V


def fe_python(theta, n, c):
    E, V = moments(theta, n)
    mse = [v + (e - theta) ** 2 for e, v in zip(E, V)]  # slide 4 decomposition, not the slide-4 closed forms
    Ef, Vf = moments(Fraction(1), n)
    msef = [v + (e - 1) ** 2 for e, v in zip(Ef, Vf)]
    order = sorted(range(4), key=lambda k: (msef[k], k))
    rank = NAMES[order[0]] + "".join((" = " if msef[k] == msef[j] else " < ") + NAMES[k] for j, k in zip(order, order[1:]))
    mse_c = lambda cc: cc**2 * V[1] + (cc * E[1] - theta) ** 2
    c_star, c_unb = (n + 2) / (n + 1), (n + 1) / n
    grid = np.linspace(0.5, 2.5, 200001)
    assert abs(grid[np.argmin(mse_c(grid))] - c_star) < 1e-4  # c* really minimises MSE(c x(n))
    boot = 1 - (1 - 1 / n) ** n
    o = {"ranking": rank, "c": fx(c, 3), "cUnb": fx(c_unb, 3), "cStar": fx(c_star, 3), "cE": fv(c * E[1]),
         "cBias": fs(c * E[1] - theta), "cSD": fv(c * np.sqrt(V[1])), "cMSE": fv(mse_c(c)), "cMin": fv(mse_c(c_star)),
         "cRel": fx(mse_c(c) / mse_c(c_star), 3), "boot": fx(boot, 3), "bootGap": fx(boot - (1 - np.exp(-1)), 3)}
    for k in range(4):
        o[f"E{k+1}"], o[f"bias{k+1}"], o[f"sd{k+1}"], o[f"mse{k+1}"] = fv(E[k]), fs(E[k] - theta), fv(np.sqrt(V[k])), fv(mse[k])
    return o


FE_VECS = {  # (theta, n, c)
    "low ends": (0.5, 1, 0.8),
    "default": (3.0, 10, 1.0),
    "high ends": (10.0, 100, 1.4),
    "n = 2 tie, c at c*": (3.0, 2, 4 / 3),
    "default, c at c*": (3.0, 10, 12 / 11),
}


def check_fe():
    model, ui = scripts(FE_PAGE)
    vecs = [dict(zip(("theta", "n", "c"), v)) for v in FE_VECS.values()]
    js = node(model + f"\nconsole.log(JSON.stringify({json.dumps(vecs)}.map(readouts)));")
    out = {}
    for (name, v), pg in zip(FE_VECS.items(), js):
        py = fe_python(*v)
        compare("four estimators", name, py, pg)
        out[name] = (v, py, pg)

    low, d, tie = js[0], js[1], js[3]
    assert (d["mse1"], d["mse2"], d["mse3"], d["mse4"]) == ("2.325", "0.136", "0.300", "0.075"), d
    assert (d["E1"], d["E2"], d["sd1"], d["sd2"], d["sd3"], d["sd4"]) == ("1.500", "2.727", "0.274", "0.249", "0.548", "0.274"), d
    assert d["boot"] == "0.651" and abs(1 - 0.9**10 - 0.6513) < 1e-4
    assert d["ranking"] == "θ̂₄ < θ̂₂ < θ̂₃ < θ̂₁", d["ranking"]
    assert low["ranking"] == "θ̂₁ = θ̂₂ = θ̂₃ = θ̂₄" and low["boot"] == "1.000", low
    assert tie["ranking"] == "θ̂₄ < θ̂₂ = θ̂₃ < θ̂₁" and tie["mse2"] == tie["mse3"] == fx(9 / 6, 3), tie
    assert d["cMSE"] == d["mse2"] and js[4]["cRel"] == "1.000"

    sweep = r"""
const OUTS = ["rank","verdict","side1","side2","o-theta","o-n","o-c","tbl","pn","pc","tnote"];
const D0 = snap(); check("load");
for(const [id, vs] of [["theta",[0.5,10]],["n",[1,100]],["c",[0.8,1.4]]]){
  for(const v of vs){ fire("reset","click"); set(id, v); check(id + "=" + v); } }
fire("reset","click");
for(const b of ["c-mle","c-unb","c-min"]){ fire(b,"click");
  for(let n=1; n<=100; n++){ set("n", n); check(b + " n=" + n); } }
fire("reset","click"); fire("c-min","click"); const atMin = els["side2"].textContent;
set("c", 1.000); const below = els["side2"].textContent; set("c", 1.2); const above = els["side2"].textContent;
fire("reset","click"); fire("c-unb","click"); set("n", 1); const slider = els["c"].value; const pressed = els["c-unb"].attrs["aria-pressed"];
fire("reset","click");
console.log(JSON.stringify({bad, reset: snap() === D0, atMin, below, above, slider, pressed}));
"""
    r = node(STUB + model + ui + sweep)
    assert not r["bad"], r["bad"][:10]
    assert r["reset"], "Reset did not restore the default state"
    assert "is at c*" in r["atMin"] and "below c* = 1.091" in r["below"] and "above c* = 1.091" in r["above"], r
    assert float(r["slider"]) == 1.4 and r["pressed"] == "true", r  # n = 1: unbiased c = 2 lies beyond the slider
    return out


def report(title, out, keys):
    print(f"\n{title}")
    for name, (v, py, pg) in out.items():
        print(f"  {name} {v}")
        for k in keys:
            print(f"    {k:<8} python {py[k]:<28} page {pg[k]}")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")  # read-outs contain τ, θ̂, λ̂; the Windows console default is cp1252
    cp = check_cp()
    report("L01-a The Change-Point Dial", cp,
           ["LR1", "LR2", "w", "s1_lam", "s2_lam", "ratio", "argmax", "s1_ci", "s2_ci", "s1_p", "s2_p", "full_p"])
    fe = check_fe()
    report("L01-b The Four Estimators", fe, ["ranking", "mse1", "mse2", "mse3", "mse4", "cMSE", "cStar", "cRel", "boot"])
    print("\nALL CHECKS PASSED")
