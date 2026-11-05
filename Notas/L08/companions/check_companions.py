"""Step 6 verification for the two Class 8 companions (Notas/L08/companions/).

For each page: recompute every read-out in Python from the model's expressions, run the page's own
`<script id="model">` block under node, and assert that both give the same printed strings at three
control vectors (both ends of the ranges and the default) plus degenerate vectors. Then load the
full page script against a stub DOM, sweep every control end to end (and the preset buttons), and
assert that no NaN/undefined/Infinity/null reaches the page and that Reset restores the default
state. Finally assert the defaults reproduce the sources (ar2-forecast.html; Tsay Ex. 2.1, Fig. 2.4,
Ex. 3.3 and Table 3.1; Tiao's kurtosis formula, Tsay p. 166).

Run: python Notas/L08/companions/check_companions.py   (needs node on PATH; exits non-zero on failure)
"""
import json
import math
import pathlib
import re
import subprocess
import sys
from decimal import ROUND_HALF_UP, Decimal

HERE = pathlib.Path(__file__).resolve().parent
AR_PAGE = HERE / "companion-ar2-dynamics.html"
GA_PAGE = HERE / "companion-garch-volatility.html"
TOL, Z90 = 1e-9, 1.6448536269514722


# ---------- helpers (same contract as Notas/L01/companions/check_companions.py) ----------
def scripts(page):
    html = page.read_text(encoding="utf-8")
    model = re.search(r'<script id="model">(.*?)</script>', html, re.S).group(1)
    ui = re.findall(r"<script>(.*?)</script>", html, re.S)[-1]
    return model, ui


def node(js):
    r = subprocess.run(["node", "-"], input=js, capture_output=True, text=True, encoding="utf-8")
    assert r.returncode == 0, r.stderr
    return json.loads(r.stdout)


def tofixed(x, d):
    """JS toFixed: exact binary value, ties away from zero."""
    return str(Decimal(float(x)).quantize(Decimal(1).scaleb(-d), rounding=ROUND_HALF_UP))


def toexp(x, d):
    """JS toExponential(d): exact binary value, ties away from zero, exponent without padding."""
    D = Decimal(float(x))
    sign, D = ("-" if D < 0 else ""), abs(D)
    e = D.adjusted()
    m = D.scaleb(-e).quantize(Decimal(1).scaleb(-d), rounding=ROUND_HALF_UP)
    if m >= 10:
        e += 1
        m = D.scaleb(-e).quantize(Decimal(1).scaleb(-d), rounding=ROUND_HALF_UP)
    return f"{sign}{m}e{'+' if e >= 0 else '-'}{abs(e)}"


def nozero(s):
    return s[1:] if re.fullmatch(r"-0\.?0*", s) else s


def compare(name, vec, py, js):
    assert set(py) == set(js), f"{name} {vec}: key mismatch {set(py) ^ set(js)}"
    bad = {k: (py[k], js[k]) for k in py if py[k] != js[k]}
    assert not bad, f"{name} {vec}: python vs page differ {bad}"


STUB = r"""
const els = {};
function mk(id){ const h = {}; return {id, h, value:"", checked:false, textContent:"", innerHTML:"", disabled:false, attrs:{},
  setAttribute(k,v){ this.attrs[k] = String(v); }, addEventListener(t,fn){ (h[t] = h[t] || []).push(fn); }}; }
globalThis.document = {getElementById: id => els[id] || (els[id] = mk(id))};
const fire = (id, t) => (els[id].h[t] || []).forEach(fn => fn());
const snap = () => Object.values(els).map(e => e.id + "|" + e.value + "|" + e.checked + "|" + e.textContent + "|" + e.innerHTML + "|" + e.disabled + "|" + JSON.stringify(e.attrs)).join("\n");
const text = () => Object.values(els).map(e => e.textContent + " " + e.innerHTML).join("\n");
const bad = [];
function check(label){ const t = text(); const m = t.match(/NaN|undefined|Infinity|null/);
  if(m) bad.push(label + ": " + m[0]);
  for(const id of OUTS) if(!String(els[id].textContent || els[id].innerHTML).trim()) bad.push(label + ": empty " + id); }
function set(id, v){ els[id].value = v; fire(id, "input"); }
"""


# ---------- L08-a The AR(2) Triangle ----------
def f3(x):
    if abs(x) >= 1e6:
        return toexp(x, 3)
    return nozero(tofixed(x, 3))


def ar_python(p1, p2, sigma, yn, yn1, H):
    """Read-outs of the AR(2) page, from Tsay eqs. 2.13-2.14, p. 42, eq. 2.34 and the ar2-forecast recursion."""
    if p2 == 0:
        kind, mods = ("none", []) if p1 == 0 else ("single", [abs(1 / p1)])
    else:
        disc = p1 * p1 + 4 * p2
        if disc < 0:
            kind, mods = "complex", [math.sqrt(-1 / p2)] * 2
        else:
            s = math.sqrt(disc)
            kind, mods = "real", sorted([abs((-p1 + s) / (2 * p2)), abs((-p1 - s) / (2 * p2))])
    m = min(mods) if mods else math.inf
    status = "stationary" if m > 1 + TOL else "unit" if m >= 1 - TOL else "explosive"
    k = 2 * math.pi / math.acos(p1 / (2 * math.sqrt(-p2))) if kind == "complex" else None
    o = {"kind": {"none": "white noise (no roots)", "single": "one real root", "real": "real roots",
                  "complex": "complex roots"}[kind]}
    ms = [f3(v) for v in mods]
    o["mods"] = "—" if kind == "none" else ms[0] if kind == "complex" else " and ".join(ms)
    o["charmod"] = "—" if kind == "none" else f3(1 / m)
    o["k"] = "—" if k is None else tofixed(k, 2)
    head = {"stationary": "Stationary", "unit": "Nonstationary · unit root", "explosive": "Explosive"}[status]
    o["verdict"] = ("Stationary · white noise (no roots)" if kind == "none" else
                    f"{head} · {o['kind']}, modulus {o['mods']}" + ("" if k is None else f" · cycle {tofixed(k, 1)} periods"))
    if status == "stationary":
        r1 = p1 / (1 - p2)
        g0 = (1 - p2) * sigma * sigma / ((1 + p2) * ((1 - p2) ** 2 - p1 * p1))
        o.update(rho1=f3(r1), rho2=f3(p1 * r1 + p2), g0=f3(g0), sd=f3(math.sqrt(g0)))
    else:
        o["rho1"] = o["rho2"] = "—"
        o["g0"] = o["sd"] = "∞ (unit root)" if status == "unit" else "— (explosive)"
    E, V, psi, a, b, cum = [], [], [1.0, p1], yn1, yn, 0.0
    for h in range(1, H + 1):
        e = p1 * b + p2 * a
        a, b = b, e
        E.append(e)
        if h >= 2:
            psi.append(p1 * psi[h - 1] + p2 * psi[h - 2])
        cum += psi[h - 1] ** 2
        V.append(sigma * sigma * cum)
    for h in range(1, 5):
        ok = h <= H
        o[f"E{h}"] = f3(E[h - 1]) if ok else "—"
        o[f"V{h}"] = f3(V[h - 1]) if ok else "—"
        o[f"lo{h}"] = f3(E[h - 1] - Z90 * math.sqrt(V[h - 1])) if ok else "—"
        o[f"hi{h}"] = f3(E[h - 1] + Z90 * math.sqrt(V[h - 1])) if ok else "—"
    eH, vH = E[-1], V[-1]
    o.update(EH=f3(eH), VH=f3(vH), sdH=f3(math.sqrt(vH)), loH=f3(eH - Z90 * math.sqrt(vH)), hiH=f3(eH + Z90 * math.sqrt(vH)))
    return o, status


AR_KEYS = ("p1", "p2", "sigma", "yn", "yn1", "H")
AR_VECS = {
    "low ends": (-2.5, -1.5, 0.1, -20, -20, 1),
    "default": (1.75, -0.8, 1.0, -5.48715, -3.508837, 50),
    "high ends": (2.5, 1.5, 5.0, 20, 20, 100),
    "unit root on the edge phi2 = 1 - phi1": (0.5, 0.5, 1.0, 1, 1, 30),
    "explosive, real": (1.0, 0.1, 1.0, 1, 1, 30),
    "explosive, complex": (0.5, -1.2, 1.0, 1, 0, 40),
    "real roots, stationary (slides)": (0.9, 0.05, 1.0, -5.48715, -3.508837, 50),
    "phi2 = 0": (0.5, 0.0, 1.0, 2, 1, 10),
    "phi2 = 0, phi1 = 1 (unit root)": (1.0, 0.0, 1.0, 2, 1, 10),
    "white noise": (0.0, 0.0, 1.0, 2, 1, 3),
    "complex roots on the unit circle": (0.0, -1.0, 1.0, 2, 1, 10),
    "GNP factor": (0.869, -0.274, 1.0, 1, 0, 20),
    "Tsay Fig. 2.4(b)": (0.6, -0.4, 1.0, 1, 0, 20),
}


def check_ar():
    model, ui = scripts(AR_PAGE)
    vecs = [dict(zip(AR_KEYS, v)) for v in AR_VECS.values()]
    js = node(model + f"\nconsole.log(JSON.stringify({json.dumps(vecs)}.map(readouts)));")
    out, st = {}, {}
    for (name, v), pg in zip(AR_VECS.items(), js):
        py, st[name] = ar_python(*v)
        compare("AR(2)", name, py, pg)
        out[name] = (v, py, pg)
    d = out["default"][2]
    assert d["verdict"] == "Stationary · complex roots, modulus 1.118 · cycle 30.1 periods", d["verdict"]
    assert (d["rho1"], d["rho2"], d["sd"], d["mods"], d["k"]) == ("0.972", "0.901", "7.121", "1.118", "30.09"), d
    assert [d[f"E{h}"] for h in range(1, 5)] == ["-6.795", "-7.502", "-7.693", "-7.460"], d
    assert [d[f"V{h}"] for h in range(1, 5)] == ["1.000", "4.063", "9.181", "15.732"], d
    assert out["GNP factor"][2]["k"] == "10.62" and out["Tsay Fig. 2.4(b)"][2]["k"] == "5.84"
    assert st["unit root on the edge phi2 = 1 - phi1"] == "unit" and out["unit root on the edge phi2 = 1 - phi1"][2]["g0"] == "∞ (unit root)"
    assert st["complex roots on the unit circle"] == "unit" and st["phi2 = 0, phi1 = 1 (unit root)"] == "unit"
    assert st["explosive, real"] == st["explosive, complex"] == st["low ends"] == st["high ends"] == "explosive"
    assert out["explosive, real"][2]["g0"] == "— (explosive)" and out["white noise"][2]["verdict"] == "Stationary · white noise (no roots)"
    assert out["real roots, stationary (slides)"][2]["kind"] == "real roots" and out["phi2 = 0"][2]["mods"] == "2.000"

    sweep = r"""
const OUTS = ["verdict","explain","side1","side2","o-p1","o-p2","o-sigma","o-H","tbl","tnote","ptri","pacf","pfan"];
const D0 = snap(); check("load");
for(const [id, vs] of [["p1",[-2.5,2.5]],["p2",[-1.5,1.5]],["sigma",[0.1,5]],["H",[1,100]],["yn",[-20,20,""]],["yn1",[-20,20,"x"]]]){
  for(const v of vs){ fire("reset","click"); set(id, v); check(id + "=" + v); } }
fire("reset","click"); set("H", 100); set("sigma", 5); set("yn", 20); set("yn1", -20);
for(let a=-2.5; a<=2.5001; a+=0.25) for(let b=-1.5; b<=1.5001; b+=0.25){ set("p1", a); set("p2", b); check(`p1=${a} p2=${b}`); }
for(const [a,b] of [[0.5,0.5],[1,0],[0,0],[0,-1],[-0.5,0.5],[2,-1]]){ set("p1", a); set("p2", b); check(`edge ${a},${b}`); }
fire("reset","click");
const pressed = {};
for(const b of ["pre-a","pre-b","pre-gnp","pre-tsay"]){ fire(b,"click"); check(b); pressed[b] = els[b].attrs["aria-pressed"]; }
fire("pre-gnp","click"); const gnp = els["side1"].textContent;
fire("reset","click"); set("p1", 0.5); set("p2", 0.5); const unitAcf = els["pacf"].innerHTML; const unitVerdict = els["verdict"].textContent;
fire("reset","click"); set("p1", 2.5); set("p2", 1.5); set("H", 100); const clip = els["clip"].textContent;
fire("reset","click"); set("yn", ""); const keep = els["tbl"].innerHTML;
fire("reset","click");
console.log(JSON.stringify({bad, reset: snap() === D0, pressed, gnp, unitAcf, unitVerdict, clip, keep}));
"""
    r = node(STUB + model + ui + sweep)
    assert not r["bad"], r["bad"][:10]
    assert r["reset"], "Reset did not restore the default state"
    assert all(v == "true" for v in r["pressed"].values()), r["pressed"]
    assert "cycle k = 10.62" in r["gnp"], r["gnp"]
    assert "no stationary ACF" in r["unitAcf"] and r["unitVerdict"].startswith("Nonstationary · unit root"), r["unitVerdict"]
    assert r["clip"].startswith("Off scale"), r["clip"]
    assert "-6.795" in r["keep"], "an empty y_n box must keep the last valid value"
    return out


# ---------- L08-b The Volatility Dial ----------
def gfx(x, d):
    if abs(x) >= 1e6:
        return toexp(x, 3)
    return nozero(tofixed(x, d))


def ga_python(a0, a1, b1, s1, normal, nu, L):
    """Read-outs of the GARCH page: Tsay eqs. 3.16-3.17, 3.22 and the kurtosis results of §3.16."""
    pers = a1 + b1
    regime = "stationary" if pers < 1 - TOL else "igarch" if pers <= 1 + TOL else "explosive"
    s2inf = a0 / (1 - pers) if regime == "stationary" else None
    v = [s1 * s1]
    for _ in range(2, max(L, 5) + 1):
        v.append(a0 + pers * v[-1])
    hl = None if regime != "stationary" else 0 if pers == 0 else math.log(0.5) / math.log(pers)
    condG = 1 - 2 * a1 * a1 - pers * pers
    kg = 6 * a1 * a1 / condG if condG > 0 else None
    K, cond, ka = 0.0, condG, kg
    if not normal:
        K = 6 / (nu - 4)
        cond = 1 - 2 * a1 * a1 * (nu - 1) / (nu - 4) - pers * pers
        # Tiao's form (Tsay p. 166): Ka = (K + Kg + 5/6 K Kg) / (1 - K Kg / 6), an independent path to the page's formula
        ka = (K + kg + 5 / 6 * K * kg) / (1 - K * kg / 6) if cond > 0 else None
    o = {"pers": tofixed(pers, 4),
         "regime": {"stationary": "covariance-stationary", "igarch": "IGARCH (unit root in variance)", "explosive": "explosive"}[regime]}
    o["hl"] = ("∞" if regime == "igarch" else "— (explosive)" if regime == "explosive" else
               "0 (no persistence)" if hl == 0 else tofixed(hl, 2))
    o["answer"] = (o["hl"] + " periods" if regime == "stationary" and hl != 0 else o["hl"]) + " · persistence " + o["pers"]
    o["sinf"] = gfx(math.sqrt(s2inf), 2) if regime == "stationary" else "none (IGARCH)" if regime == "igarch" else "none (explosive)"
    o["s2inf"] = gfx(s2inf, 3) if regime == "stationary" else "—"
    for l in range(1, 6):
        o[f"s{l}"] = gfx(math.sqrt(v[l - 1]), 3)
    o["sL"] = gfx(math.sqrt(v[L - 1]), 3)
    o["kg"] = "infinite fourth moment" if kg is None else gfx(kg, 3)
    o["ka"] = "infinite fourth moment" if ka is None else gfx(ka, 3)
    o["K"] = "0 (normal)" if normal else gfx(K, 3)
    o["cond"] = gfx(cond, 4)
    return o, regime, (math.sqrt(v[l - 1]) for l in range(1, 6))


GA_KEYS = ("a0", "a1", "b1", "s1", "normal", "nu", "L")
GA_VECS = {
    "low ends": (0.0001, 0.0, 0.0, 0.5, False, 4.1, 1),
    "default": (0.86, 0.1216, 0.8511, 5.36, True, 7.04, 60),
    "high ends": (5.0, 0.5, 0.9999, 20.0, False, 30.0, 500),
    "IGARCH exactly (Tsay p. 141)": (1.19, 0.1941, 0.8059, 5.36, True, 7.04, 60),
    "explosive": (0.86, 0.3, 0.8, 5.36, True, 7.04, 100),
    "beyond the Gaussian kurtosis boundary": (0.86, 0.4, 0.5, 5.36, True, 7.04, 60),
    "nu near 4": (0.86, 0.1216, 0.8511, 5.36, False, 4.1, 60),
    "ARCH(1), beta = 0": (0.5, 0.356, 0.0, 2.0, True, 7.04, 20),
    "PBR t preset": (0.1555, 0.0743, 0.9095, 3.10, False, 7.04, 60),
    "PBR normal preset": (0.2255, 0.1032, 0.8768, 3.36, True, 7.04, 60),
}


def check_ga():
    model, ui = scripts(GA_PAGE)
    vecs = [dict(zip(GA_KEYS, v)) for v in GA_VECS.values()]
    js = node(model + f"\nconsole.log(JSON.stringify({json.dumps(vecs)}.map(readouts)));")
    out, reg, path = {}, {}, {}
    for (name, v), pg in zip(GA_VECS.items(), js):
        py, reg[name], sp = ga_python(*v)
        path[name] = list(sp)
        compare("GARCH", name, py, pg)
        out[name] = (v, py, pg)
    d = out["default"][2]
    assert (d["pers"], d["sinf"], d["hl"], d["kg"]) == ("0.9727", "5.61", "25.04", "3.654"), d
    assert d["answer"] == "25.04 periods · persistence 0.9727", d["answer"]
    table31 = [5.36, 5.37, 5.37, 5.38, 5.38]                 # Tsay Table 3.1, p. 138 (in %)
    assert all(abs(x - t) <= 0.01 for x, t in zip(path["default"], table31)), path["default"]
    ig = out["IGARCH exactly (Tsay p. 141)"][2]
    assert reg["IGARCH exactly (Tsay p. 141)"] == "igarch" and ig["hl"] == "∞" and ig["sinf"] == "none (IGARCH)", ig
    assert abs(float(ig["s2"]) ** 2 - (5.36 ** 2 + 1.19)) < 5e-3                        # eq. (3.22)
    assert reg["explosive"] == reg["high ends"] == "explosive" and out["explosive"][2]["hl"] == "— (explosive)"
    assert out["beyond the Gaussian kurtosis boundary"][2]["ka"] == "infinite fourth moment"
    assert reg["beyond the Gaussian kurtosis boundary"] == "stationary"
    assert out["nu near 4"][2]["ka"] == "infinite fourth moment" and out["nu near 4"][2]["K"] == "60.000"
    assert out["low ends"][2]["hl"] == "0 (no persistence)" and out["low ends"][2]["ka"] == "60.000"
    a, b, nu = 0.0743, 0.9095, 7.04                           # PBR t preset; garchmodeling.html shape 7.04
    kg = 6 * a * a / (1 - 2 * a * a - (a + b) ** 2)
    assert out["PBR t preset"][2]["ka"] == tofixed((6 + (nu + 1) * kg) / (nu - 4 - kg), 3)  # Tsay's closing formula
    arch = out["ARCH(1), beta = 0"][2]
    assert arch["kg"] == tofixed(3 * (1 - 0.356 ** 2) / (1 - 3 * 0.356 ** 2) - 3, 3)       # ARCH(1) kurtosis, Tsay p. 118

    sweep = r"""
const OUTS = ["answer","explain","side1","side2","o-a1","o-b1","o-a0","o-s1","o-L","o-nu","tbl","tnote","pterm","pmap","thL"];
const D0 = snap(); check("load");
for(const [id, vs] of [["a1",[0,0.5]],["b1",[0,0.9999]],["a0",[0.0001,5]],["s1",[0.5,20]],["L",[1,500]],["nu",[4.1,30]]]){
  for(const v of vs){ fire("reset","click"); els["normal"].checked = false; fire("normal","change"); set(id, v); check(id + "=" + v);
    els["normal"].checked = true; fire("normal","change"); check(id + "=" + v + " normal"); } }
fire("reset","click"); set("L", 500);
for(const nrm of [true, false]){ els["normal"].checked = nrm; fire("normal","change");
  for(let a=0; a<=0.5001; a+=0.05) for(let b=0; b<=1.0; b+=0.1){ set("a1", a); set("b1", Math.min(b, 0.9999)); check(`a1=${a} b1=${b} normal=${nrm}`); } }
fire("reset","click");
const pressed = {};
for(const b of ["pre-tsay","pre-ig","pre-pbr","pre-pbrt"]){ fire(b,"click"); check(b); pressed[b] = els[b].attrs["aria-pressed"]; }
fire("pre-ig","click"); const ig = els["answer"].textContent + " | " + els["side1"].textContent;
fire("pre-pbrt","click"); const nuOff = els["nu"].disabled; const pbrt = els["side2"].textContent;
fire("reset","click"); const nuDefault = els["nu"].disabled;
console.log(JSON.stringify({bad, reset: snap() === D0, pressed, ig, nuOff, nuDefault, pbrt}));
"""
    r = node(STUB + model + ui + sweep)
    assert not r["bad"], r["bad"][:10]
    assert r["reset"], "Reset did not restore the default state"
    assert all(v == "true" for v in r["pressed"].values()), r["pressed"]
    assert r["ig"].startswith("∞ · persistence 1.0000") and "IGARCH" in r["ig"], r["ig"]
    assert r["nuOff"] is False and r["nuDefault"] is True, r
    assert out["PBR t preset"][2]["ka"] in r["pbrt"], r["pbrt"]
    return out


def report(title, out, keys):
    print(f"\n{title}")
    for name, (v, py, pg) in out.items():
        print(f"  {name} {v}")
        for k in keys:
            print(f"    {k:<8} python {py[k]:<62} page {pg[k]}")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")  # read-outs contain φ, σ, ∞; the Windows console default is cp1252
    ar = check_ar()
    report("L08-a The AR(2) Triangle", {k: ar[k] for k in ("low ends", "default", "high ends")},
           ["verdict", "rho1", "sd", "E1", "V4", "sdH"])
    ga = check_ga()
    report("L08-b The Volatility Dial", {k: ga[k] for k in ("low ends", "default", "high ends")},
           ["answer", "sinf", "s5", "sL", "kg", "ka"])
    print(f"\nDegenerate vectors checked: AR(2) {len(AR_VECS) - 3}, GARCH {len(GA_VECS) - 3}")
    print("\nALL CHECKS PASSED")
