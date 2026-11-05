"""Step 6 verification for the two Class 9 companions (Notas/L09/companions/).

For each page: recompute every read-out in Python (numpy) from the model's expressions, run the
page's own `<script id="model">` block under node, and assert that both give the same printed
strings at three control vectors (both ends of the ranges and the default) plus degenerate
vectors. Then load the full page script against a stub DOM, sweep every control end to end (and
the landmark buttons), assert that no NaN/undefined/Infinity/null reaches the page and that Reset
restores the default state. Finally assert the defaults reproduce the sources' numbers.

The node runner, the JS-toFixed formatter and the stub DOM are imported from the Class 1 check
(Notas/L01/companions/check_companions.py) — reuse, not a copy.

Run: python Notas/L09/companions/check_companions.py   (needs node on PATH; exits non-zero on failure)
"""
import json
import math
import pathlib
import re
import sys
from decimal import ROUND_HALF_UP, Decimal

import numpy as np

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "L01" / "companions"))
from check_companions import STUB, compare, fx, node, scripts  # noqa: E402

OD_PAGE = HERE / "companion-var-irf-ordering.html"
FV_PAGE = HERE / "companion-fsv-correlation.html"


def f3(x):
    s = fx(x, 3)
    return "0.000" if s == "-0.000" else s


# ---------- L09-a The Ordering Dial ----------
S1, S2, H, HMAX = math.sqrt(2), 1.0, 10, 12


def chol(rho, order):
    c = math.sqrt(1 - rho * rho)
    return np.array([[S1, 0], [rho * S2, S2 * c]]) if order == "12" else np.array([[S1 * c, rho * S1], [0, S2]])


def od_python(p11, p12, p21, p22, rho, order):
    Phi = np.array([[p11, p12], [p21, p22]])
    Sig = np.array([[2.0, rho * S1 * S2], [rho * S1 * S2, 1.0]])
    for o in ("12", "21"):
        assert np.allclose(chol(rho, o) @ chol(rho, o).T, Sig)          # both factors reproduce Sigma
    pct = lambda x: fx(100 * x, 1) + "%"

    def fevd(o):
        num = sum((np.linalg.matrix_power(Phi, h) @ chol(rho, o)) ** 2 for h in range(H))
        return num / num.sum(axis=1, keepdims=True)

    other = "21" if order == "12" else "12"
    Fc, Fo = fevd(order), fevd(other)
    F12, F21 = (Fc, Fo) if order == "12" else (Fo, Fc)
    ev = np.linalg.eigvals(Phi)
    ev = sorted(ev, key=lambda z: (-z.real, -z.imag))
    mx = max(abs(z) for z in ev)
    status = "unit root (on the boundary)" if abs(mx - 1) < 1e-9 else ("stationary" if mx < 1 else "explosive")

    def es(z):
        if abs(z.imag) < 1e-12:
            return f3(z.real)
        return f3(z.real) + (" + " if z.imag > 0 else " − ") + f3(abs(z.imag)) + "i"

    a, b = chol(rho, "12"), chol(rho, "21")
    T1 = Phi @ chol(rho, order)
    return {"ans": pct(Fc[0, 1]), "ansOther": pct(Fo[0, 1]), "f12_12": pct(F12[0, 1]), "f12_21": pct(F21[0, 1]),
            "f21_12": pct(F12[1, 0]), "f21_21": pct(F21[1, 0]), "gap": fx(100 * abs(F12[0, 1] - F21[0, 1]), 1),
            "eig1": es(ev[0]), "eig2": es(ev[1]), "maxmod": f3(mx), "status": status,
            "a11": f3(a[0, 0]), "a12": f3(a[0, 1]), "a21": f3(a[1, 0]), "a22": f3(a[1, 1]),
            "b11": f3(b[0, 0]), "b12": f3(b[0, 1]), "b21": f3(b[1, 0]), "b22": f3(b[1, 1]),
            "th1_12": f3(T1[0, 1]), "rho": "0.7071 (exact)" if abs(rho - 1 / math.sqrt(2)) < 1e-12 else fx(rho, 2)}


OD_VECS = {  # (p11, p12, p21, p22, rho, order)
    "low ends": (-1.5, -1.5, -1.5, -1.5, -0.95, "21"),
    "default (T Ex. 8.3)": (0.2, 0.3, -0.6, 1.1, 1 / math.sqrt(2), "12"),
    "high ends": (1.5, 1.5, 1.5, 1.5, 0.95, "12"),
    "rho = 0 landmark": (0.2, 0.3, -0.6, 1.1, 0.0, "21"),
    "degenerate: Phi = 0": (0.0, 0.0, 0.0, 0.0, 0.5, "12"),
    "unit root boundary": (1.0, 0.0, 0.0, 0.0, 0.3, "12"),
    "complex roots": (0.5, -0.8, 0.8, 0.5, -0.4, "21"),
}


def check_od():
    model, ui = scripts(OD_PAGE)
    keys = ("p11", "p12", "p21", "p22", "rho", "order")
    vecs = [dict(zip(keys, v)) for v in OD_VECS.values()]
    js = node(model + f"\nconsole.log(JSON.stringify({json.dumps(vecs)}.map(readouts)));")
    out = {}
    for (name, v), pg in zip(OD_VECS.items(), js):
        py = od_python(*v)
        compare("ordering dial", name, py, pg)
        out[name] = (v, py, pg)
    d, z = js[1], js[3]
    # T Ex. 8.3 (p. 400): impact matrices of both orderings, eigenvalues 0.8 and 0.5 (L01 §9.1)
    assert (d["a11"], d["a21"], d["a22"], d["b11"], d["b12"], d["b21"], d["b22"]) == \
        ("1.414", "0.707", "0.707", "1.000", "1.000", "0.000", "1.000"), d
    assert (d["eig1"], d["eig2"], d["status"], d["rho"]) == ("0.800", "0.500", "stationary", "0.7071 (exact)"), d
    assert z["gap"] == "0.0" and z["ans"] == z["ansOther"], z                 # rho = 0: orderings coincide
    assert js[5]["status"] == "unit root (on the boundary)" and js[2]["status"] == "explosive"
    assert js[6]["eig1"].endswith("i") and js[4]["ans"] == "0.0%"

    sweep = r"""
const OUTS = ["ans","verdict","side","tbl","irf","eig","o-p11","o-p12","o-p21","o-p22","o-rho","o-order"];
const D0 = snap(); check("load");
for(const [id, vs] of [["p11",[-1.5,1.5]],["p12",[-1.5,1.5]],["p21",[-1.5,1.5]],["p22",[-1.5,1.5]],["rho",[-0.95,0.95]]]){
  for(const v of vs){ fire("reset","click"); set(id, v); check(id + "=" + v); fire("ord21","click"); check(id + "=" + v + " ord21"); } }
fire("reset","click");
for(let r=-0.95; r<=0.951; r+=0.05){ set("rho", r.toFixed(2)); check("rho=" + r.toFixed(2)); }
fire("rho0","click"); const v0 = els["verdict"].textContent; const r0 = els["rho"].value;
fire("ex83","click"); const rx = els["o-rho"].textContent;
fire("reset","click"); set("p11", 1); set("p12", 0); set("p21", 0); set("p22", 0); const ur = els["verdict"].textContent;
fire("reset","click");
console.log(JSON.stringify({bad, reset: snap() === D0, v0, r0, rx, ur}));
"""
    r = node(STUB + model + ui + sweep)
    assert not r["bad"], r["bad"][:10]
    assert r["reset"], "Reset did not restore the default state"
    assert "ρ = 0, nothing to split" in r["v0"] and float(r["r0"]) == 0.0, r
    assert r["rx"] == "0.7071 (exact)" and "unit root" in r["ur"], r
    return out


# ---------- L09-b The Factor-Volatility Dial ----------
def tp3(x):
    """JS toPrecision(3) for 1e-6 <= x < 1000 (fixed notation, ties away from zero)."""
    e = math.floor(math.log10(abs(x)))
    s = str(Decimal(float(x)).quantize(Decimal(1).scaleb(e - 2), rounding=ROUND_HALF_UP))
    if len(s.replace(".", "").replace("-", "").lstrip("0")) > 3:      # rounding carried into a new digit
        s = str(Decimal(float(x)).quantize(Decimal(1).scaleb(e - 1), rounding=ROUND_HALF_UP))
    return s


def fv_python(b1, b2, p1, p2, lam):
    def mom(l):
        h = math.exp(l)
        v1, v2, c = b1 * b1 * h + p1, b2 * b2 * h + p2, b1 * b2 * h
        return h, v1, v2, c, (c / math.sqrt(v1 * v2) if v1 > 0 and v2 > 0 else None)

    h, v1, v2, c, rho = mom(lam)
    rho0 = mom(0)[4]
    if b1 == 0 or b2 == 0:
        hp = None
    else:
        a1, a2 = p1 / b1**2, p2 / b2**2
        if a1 == 0 and a2 == 0:
            hp = None
        else:
            x = 3 / (a1 + a2) if (a1 == 0 or a2 == 0) else (-(a1 + a2) + math.sqrt((a1 + a2) ** 2 + 12 * a1 * a2)) / (2 * a1 * a2)
            hp = -math.log(x)
            r_half = mom(hp)[4]
            assert abs(abs(r_half) - 0.5) < 1e-9                    # it really is the half-limit point
    limit = 0 if (b1 == 0 or b2 == 0) else int(np.sign(b1 * b2))
    sh = lambda num, den: (fx(100 * num / den, 1) + "%") if den > 0 else "n/a (zero variance)"
    return {"ans": "n/a (a series has zero variance)" if rho is None else f3(rho),
            "rho0": "n/a" if rho0 is None else f3(rho0), "h": tp3(h), "lam": fx(lam, 2),
            "v1": f3(v1), "v2": f3(v2), "cov": f3(c), "share1": sh(b1 * b1 * h, v1), "share2": sh(b2 * b2 * h, v2),
            "limit": str(limit), "half": "none (ρ does not depend on h)" if hp is None else fx(hp, 3),
            "side": "flat" if hp is None else ("at" if abs(lam - hp) < 1e-9 else ("above" if lam > hp else "below"))}


FV_VECS = {  # (b1, b2, p1, p2, lam)
    "low ends": (-1.5, -1.5, 0.0, 0.0, -6.0),
    "default (slide 22, rows 1 and 3)": (0.99, 0.90, 0.01, 0.10, 0.0),
    "high ends": (1.5, 1.5, 1.0, 1.0, 3.0),
    "calm factor (lambda = -3)": (0.99, 0.90, 0.01, 0.10, -3.0),
    "degenerate: zero variance": (0.0, 0.90, 0.0, 0.10, 0.0),
    "degenerate: zero loading": (0.0, 0.90, 0.5, 0.10, 1.0),
    "one idiosyncratic variance zero": (0.5, -0.8, 0.0, 0.3, -1.0),
}


def check_fv():
    model, ui = scripts(FV_PAGE)
    keys = ("b1", "b2", "p1", "p2", "lam")
    vecs = [dict(zip(keys, v)) for v in FV_VECS.values()]
    js = node(model + f"\nconsole.log(JSON.stringify({json.dumps(vecs)}.map(readouts)));")
    out = {}
    for (name, v), pg in zip(FV_VECS.items(), js):
        py = fv_python(*v)
        compare("factor-volatility dial", name, py, pg)
        out[name] = (v, py, pg)
    d = js[1]
    assert (d["ans"], d["rho0"], d["h"], d["share1"]) == ("0.939", "0.939", "1.00", "99.0%"), d   # L09-07 §5
    assert js[3]["ans"] == "0.488" and js[0]["ans"] == "1.000" and js[0]["half"].startswith("none"), js[3]
    assert js[4]["ans"].startswith("n/a") and js[5]["ans"] == "0.000" and js[5]["side"] == "flat"

    sweep = r"""
const OUTS = ["ans","verdict","side","curve","ell","o-b1","o-b2","o-p1","o-p2","o-lam"];
const D0 = snap(); check("load");
for(const [id, vs] of [["b1",[-1.5,0,1.5]],["b2",[-1.5,0,1.5]],["p1",[0,1]],["p2",[0,1]],["lam",[-6,3]]]){
  for(const v of vs){ fire("reset","click"); set(id, v); check(id + "=" + v); fire("gohalf","click"); check(id + "=" + v + " half"); } }
fire("reset","click");
for(let l=-6; l<=3.001; l+=0.05){ set("lam", l.toFixed(2)); check("lam=" + l.toFixed(2)); }
fire("reset","click"); set("b1", 0); set("p1", 0); check("zero variance"); const zv = els["ans"].textContent;
fire("reset","click"); fire("gohalf","click"); const hv = els["verdict"].textContent;
fire("go0","click"); const l0 = els["o-lam"].textContent;
fire("reset","click");
console.log(JSON.stringify({bad, reset: snap() === D0, zv, hv, l0}));
"""
    r = node(STUB + model + ui + sweep)
    assert not r["bad"], r["bad"][:10]
    assert r["reset"], "Reset did not restore the default state"
    assert r["zv"].startswith("n/a") and "at the half-limit point" in r["hv"] and r["l0"].startswith("0.00"), r
    return out


def report(title, out, keys):
    print(f"\n{title}")
    for name, (v, py, pg) in out.items():
        print(f"  {name} {v}")
        for k in keys:
            print(f"    {k:<8} python {py[k]:<36} page {pg[k]}")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    od = check_od()
    report("L09-a The Ordering Dial", od, ["ans", "ansOther", "maxmod", "status", "a11", "b12", "th1_12"])
    fv = check_fv()
    report("L09-b The Factor-Volatility Dial", fv, ["ans", "rho0", "h", "v1", "v2", "cov", "half", "side"])
    print("\nALL CHECKS PASSED")
