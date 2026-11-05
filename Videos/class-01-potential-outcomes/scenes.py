"""Scenes for class-01-potential-outcomes. One Scene per beat; durations come from beats.json.

Colour roles (fixed): ORANGE y0 (untreated world) · BLUE y1 (treated world) · GREEN causal
effects · RED selection bias · PURPLE heterogeneity bias · GREY muted / unobserved ·
YELLOW the live line or object of attention.
"""
from itertools import combinations

from manim import *
from video_explainer import Beat, Stage, axes_panel, note, table

Y0C, Y1C, EFF, BIAS, HET, FOCUS = ORANGE, BLUE, GREEN, RED, PURPLE, YELLOW
GREYED = "#3d3d3d"
NAMES = ["Ana", "Bruno", "Carla", "Davi", "Elisa", "Fábio", "Gabi", "Hugo"]
Y0 = [3, 2, 4, 3, 8, 9, 7, 8]
Y1 = [5, 5, 6, 4, 8, 8, 8, 9]
D_SELF = [1, 1, 1, 1, 0, 0, 0, 0]
D_MIRROR = [0, 0, 0, 0, 1, 1, 1, 1]
D_COIN = [1, 0, 0, 0, 1, 1, 0, 1]          # Ana, Elisa, Fábio, Hugo treated
HEADS = {"y0": "y₀", "y1": "y₁", "d": "d", "eff": "y₁ − y₀"}
COLS = {"y0": Y0C, "y1": Y1C, "eff": EFF}


# ------------------------------------------------------------------ helpers

def num(v):
    return str(v).replace("-", "−")


def po_table(cols=("y0", "y1", "d"), d=D_SELF, rh=0.48, fs=20):
    """Potential-outcomes table; .cells[(r, c)] gives each Text (r = 0 is the header)."""
    rows, colours = [], {}
    for i, name in enumerate(NAMES):
        vals = {"y0": Y0[i], "y1": Y1[i], "d": d[i], "eff": Y1[i] - Y0[i]}
        rows.append([name] + [num(vals[c]) for c in cols])
        for j, c in enumerate(cols, 1):
            colours[(i, j)] = COLS.get(c, WHITE)
    g = table(["person"] + [HEADS[c] for c in cols], rows,
              col_widths=[1.6] + [1.2] * len(cols), row_height=rh, font_size=fs,
              cell_colours=colours)
    texts = [m for m in g.submobjects if isinstance(m, Text)]
    n = len(cols) + 1
    g.cells = {divmod(k, n): m for k, m in enumerate(texts)}
    for j, c in enumerate(cols, 1):
        g.cells[(0, j)].set_color(COLS.get(c, WHITE))
    g.colidx = {c: j for j, c in enumerate(cols, 1)}
    return g


def unseen(g, d):
    """Cells nobody can observe: y0 of the treated, y1 of the untreated."""
    out = []
    for i in range(8):
        key = "y0" if d[i] == 1 else "y1"
        out.append(g.cells[(i + 1, g.colidx[key])])
    return out


def grey_now(cells):
    for c in cells:
        c.set_color(GREYED)


def hide(group, mobs):
    group.remove(*mobs)
    return mobs


def column(texs, slot, size=30, colours=None, buff=0.35):
    """MathTex lines stacked and pre-positioned in a slot, revealed later with add_to."""
    colours = colours or {}
    g = VGroup(*[MathTex(t, font_size=size, color=colours.get(k, WHITE))
                 for k, t in enumerate(texs)]).arrange(DOWN, aligned_edge=LEFT, buff=buff)
    Stage.fit(g, slot)
    return g


def deriv(texs, size=34):
    """Numbered derivation rows, laid out once and fitted to the main slot."""
    rows = VGroup()
    for k, tx in enumerate(texs, 1):
        line = MathTex(tx, font_size=size)
        tag = MathTex(f"({k})", font_size=int(size * 0.7), color=GREY)
        rows.add(VGroup(line, tag.next_to(line, RIGHT, buff=0.45)))
    rows.arrange(DOWN, aligned_edge=LEFT, buff=0.3)
    Stage.fit(rows, "main")
    return rows


def nt(s, colour=GREY):
    return note(s, colour)


def mnote(tex, colour=WHITE):
    return MathTex(tex, font_size=34, color=colour)


def reg(st, slot, mob):
    """Register mob in a slot without its default FadeIn (for Grow/Transform reveals)."""
    st.add_to(slot, mob)
    return mob


def step_line(st, rows, k):
    """Derive row k from row k-1: the manipulation morphs, the old line goes muted."""
    reg(st, "main", rows[k])
    return [TransformFromCopy(rows[k - 1][0], rows[k][0]), FadeIn(rows[k][1]),
            rows[k - 1].animate.set_color(GREY)]


def card(head, body, sign, colour):
    box = RoundedRectangle(corner_radius=0.2, width=3.9, height=3.6, color=GREY)
    h = Text(head, font_size=26, color=WHITE)
    bd = Text(body, font_size=19, color=GREY_A, line_spacing=0.9)
    sg = MathTex(sign, font_size=34, color=colour)
    VGroup(h, bd, sg).arrange(DOWN, buff=0.45).move_to(box)
    return VGroup(box, h, bd, sg)


# ===================================================================== Act I

class B01ColdOpen(Scene):
    def construct(self):
        st, b = Stage(self), Beat(self, "B01ColdOpen")
        t = table(["group", "sample size", "mean health", "std. error"],
                  [["Hospital", "7,774", "2.79", "0.014"],
                   ["No hospital", "90,049", "2.07", "0.003"]],
                  col_widths=[2.8, 2.4, 2.6, 2.4], row_height=0.8, font_size=26)
        cells = [m for m in t.submobjects if isinstance(m, Text)]
        b.step(st.show("title", Text("National Health Interview Survey, 2005", font_size=30,
                                     color=GREY)), t=0.7, hold=1)
        show = st.show("main", t)
        r1, r2 = hide(t, cells[4:8]), hide(t, cells[8:12])
        b.step(show, t=0.8, hold=1)
        b.step([FadeIn(VGroup(*r1))], t=0.7, hold=1.5)
        st.add_to("main", VGroup(*r1))
        b.step([FadeIn(VGroup(*r2))], t=0.7, hold=1.5)
        st.add_to("main", VGroup(*r2))
        b.step(st.show("note", nt("health: 1 = excellent … 5 = poor")), t=0.7, hold=1.5)
        b.step([Indicate(r1[2], color=FOCUS)], t=0.8, hold=1)
        b.step([Indicate(r2[2], color=FOCUS)], t=0.8, hold=1)
        b.step(st.show("note", nt("gap 0.71 · t = 58.9")), t=0.7, hold=1.5)
        b.step([r1[2].animate.set_color(BIAS)], t=0.6, hold=1)
        b.step(st.show("note", nt("taken at face value: hospitals make people sick", BIAS)),
               t=0.7, hold=1.5)
        b.step([Circumscribe(VGroup(r1[2], r2[2]), color=FOCUS)], t=0.9, hold=1)
        b.step(st.show("note", nt("Do you believe it?", FOCUS)), t=0.7, hold=2)
        b.run()


class B02BrazilToo(Scene):
    def construct(self):
        st, b = Stage(self), Beat(self, "B02BrazilToo")
        ax, panel = axes_panel([0, 3.6, 1], [0, 20, 5], y_label="% hospitalised", width=8.0,
                               height=4.0)
        b.step(st.show("title", Text("Brazil · PNS 2013 · IBGE SIDRA table 5082",
                                     font_size=28, color=GREY)), t=0.7, hold=1)
        b.step(st.show("main", panel), t=0.8, hold=1)
        bars, vals, cats = [], [], []
        for x, v, lab in ((0.8, 4.5, "very good / good"), (1.8, 8.8, "regular"),
                          (2.8, 18.8, "bad / very bad")):
            h = ax.c2p(0, v)[1] - ax.c2p(0, 0)[1]
            bar = Rectangle(width=0.9, height=h, fill_color=BLUE, fill_opacity=0.8,
                            stroke_width=0).move_to(ax.c2p(x, 0), aligned_edge=DOWN)
            bars.append(bar)
            vals.append(Text(f"{v}%", font_size=24).next_to(bar, UP, buff=0.12))
            cats.append(Text(lab, font_size=20, color=GREY_A).next_to(ax.c2p(x, 0), DOWN,
                                                                       buff=0.2))
        for k in range(3):
            reg(st, "main", bars[k]); st.add_to("main", cats[k]); st.add_to("main", vals[k])
        b.step([GrowFromEdge(bars[0], DOWN), FadeIn(cats[0])], t=0.8, hold=1)
        b.step([FadeIn(vals[0])], t=0.6, hold=1.5)
        b.step([GrowFromEdge(bars[1], DOWN), FadeIn(cats[1])], t=0.8, hold=1)
        b.step([FadeIn(vals[1])], t=0.6, hold=1.5)
        b.step([GrowFromEdge(bars[2], DOWN), FadeIn(cats[2])], t=0.8, hold=1)
        b.step([FadeIn(vals[2])], t=0.6, hold=1.5)
        b.step(st.show("note", nt("12.06 million Brazilians hospitalised that year")),
               t=0.7, hold=2)
        b.step([Indicate(bars[2], color=FOCUS)], t=0.8, hold=1.5)
        b.step(st.show("note", nt("read it the other way: poor health → hospital", FOCUS)),
               t=0.7, hold=3)
        b.step(st.show("note", nt("we want: hospital → health")), t=0.7, hold=3)
        b.step(st.show("note", nt("both arrows connect the same two variables")), t=0.7,
               hold=3)
        b.run()


class B03WrongFirstAttempt(Scene):
    def construct(self):
        st, b = Stage(self), Beat(self, "B03WrongFirstAttempt")
        rows = [["1,000", "0.71", "6.0"], ["10,000", "0.71", "18.8"],
                ["100,000", "0.71", "59.6"], ["1,000,000", "0.71", "188.3"]]
        t = table(["sample size", "gap", "t statistic"], rows, col_widths=[3.2, 2.2, 2.8],
                  row_height=0.7, font_size=26)
        cells = [m for m in t.submobjects if isinstance(m, Text)]
        b.step(st.show("title", Text("Wrong first attempt: collect more data", font_size=30,
                                     color=BIAS)), t=0.7, hold=1)
        show = st.show("main", t)
        rr = [hide(t, cells[3 + 3 * k: 6 + 3 * k]) for k in range(4)]
        b.step(show, t=0.8, hold=1)
        for grp in rr:
            st.add_to("main", VGroup(*grp))
        b.step([FadeIn(VGroup(*rr[0]))], t=0.6, hold=1.5)
        b.step([FadeIn(VGroup(*rr[1]))], t=0.6, hold=1)
        b.step([FadeIn(VGroup(*rr[2]))], t=0.6, hold=1)
        b.step([FadeIn(VGroup(*rr[3]))], t=0.6, hold=1)
        b.step(st.show("note", nt("illustrative: t grows with √n, the gap stays put")), t=0.7,
               hold=1.5)
        b.step([Circumscribe(VGroup(*[g[1] for g in rr]), color=FOCUS)], t=0.9, hold=2)
        b.step(st.show("note", nt("precision ≠ identification", FOCUS)), t=0.7, hold=3)
        faqs = VGroup(*[Text(s, font_size=26) for s in (
            "1 · What is the causal relationship of interest?",
            "2 · What experiment would ideally capture it?",
            "3 · What is your identification strategy?",
            "4 · What is your mode of statistical inference?")]).arrange(
            DOWN, aligned_edge=LEFT, buff=0.45)
        b.step(st.show("main", faqs) + st.show("note", nt("Angrist & Pischke, Ch. 1")),
               t=0.8, hold=1)
        hidden = hide(faqs, list(faqs.submobjects))
        for f in hidden:
            st.add_to("main", f)
        b.step([FadeIn(hidden[0])], t=0.6, hold=1)
        b.step([FadeIn(hidden[1])], t=0.6, hold=1)
        b.step([FadeIn(hidden[2])], t=0.6, hold=1)
        b.step([FadeIn(hidden[3])], t=0.6, hold=1)
        b.step([hidden[0].animate.set_color(FOCUS), hidden[1].animate.set_color(FOCUS)]
               + st.show("note", nt("today: questions 1 and 2")), t=0.7, hold=2)
        b.run()


# ==================================================================== Act II

class B04TwoWorlds(Scene):
    def construct(self):
        st, b = Stage(self), Beat(self, "B04TwoWorlds")
        ana = VGroup(Dot(radius=0.14, color=WHITE), Text("Ana", font_size=28))
        ana[1].next_to(ana[0], DOWN, buff=0.15)
        b.step(st.show("title", Text("Two potential outcomes", font_size=30, color=GREY)),
               t=0.7, hold=1)
        b.step(st.show("main", ana), t=0.7, hold=1.5)
        b.step([ana.animate.shift(LEFT * 4.5)], t=0.8, hold=0.5)
        o = ana[0].get_center() + LEFT * 4.5
        up = Arrow(o, o + RIGHT * 4.6 + UP * 1.6, buff=0.2, color=Y1C)
        dn = Arrow(o, o + RIGHT * 4.6 + DOWN * 1.6, buff=0.2, color=Y0C)
        hos = Text("hospital", font_size=24, color=Y1C).next_to(up, UP, buff=0.1)
        hom = Text("home", font_size=24, color=Y0C).next_to(dn, DOWN, buff=0.1)
        y1 = MathTex(r"y_{1,\text{Ana}}", font_size=40, color=Y1C).next_to(up.get_end(),
                                                                       RIGHT, buff=0.3)
        y0 = MathTex(r"y_{0,\text{Ana}}", font_size=40, color=Y0C).next_to(dn.get_end(),
                                                                       RIGHT, buff=0.3)
        for m in (up, hos, dn, hom, y1, y0):
            reg(st, "main", m)
        b.step([GrowArrow(up), FadeIn(hos)], t=0.8, hold=1.5)
        b.step([GrowArrow(dn), FadeIn(hom)], t=0.8, hold=1.5)
        b.step([Write(y1)], t=0.8, hold=1.5)
        b.step([Write(y0)], t=0.8, hold=1.5)
        b.step(st.show("note", mnote(r"\text{effect for Ana} = y_{1,\text{Ana}} - "
                                     r"y_{0,\text{Ana}}", EFF)), t=0.8, hold=3)
        b.step([up.animate.set_color(FOCUS)], t=0.6, hold=1)
        b.step([dn.animate.set_opacity(0.15), hom.animate.set_opacity(0.15)], t=0.8, hold=1)
        b.step([y0.animate.set_opacity(0.15)], t=0.6, hold=1)
        b.step(st.show("note", nt("the other branch is not unknown. It is gone.", BIAS)),
               t=0.7, hold=3)
        b.step(st.show("note", nt("Neyman (1923) · Rubin (1974): the potential outcomes "
                                  "framework")), t=0.7, hold=3)
        b.step([Circumscribe(VGroup(y1, y0), color=FOCUS)], t=0.9, hold=2)
        b.step(st.show("note", nt("every unit carries two outcomes; treatment picks one",
                                  FOCUS)), t=0.7, hold=2)
        b.run()


class B05TheTable(Scene):
    def construct(self):
        st, b = Stage(self), Beat(self, "B05TheTable")
        g = po_table()
        b.step(st.show("title", Text("Eight people, both worlds visible", font_size=30,
                                     color=GREY)), t=0.7, hold=1)
        show = st.show("main", g)
        rows = [hide(g, [g.cells[(r, c)] for c in range(3)]) for r in range(1, 9)]
        dcol = hide(g, [g.cells[(r, 3)] for r in range(0, 9)])
        b.step(show, t=0.8, hold=1)
        for grp in rows + [dcol]:
            st.add_to("main", VGroup(*grp))
        b.step(st.show("note", nt("health index 0–10, higher = healthier")), t=0.7, hold=2)
        b.step([FadeIn(VGroup(*rows[0]))], t=0.6, hold=1.2)
        b.step([FadeIn(VGroup(*rows[1]))], t=0.6, hold=1)
        b.step([FadeIn(VGroup(*rows[2]))], t=0.6, hold=1)
        b.step([FadeIn(VGroup(*rows[3]))], t=0.6, hold=1)
        b.step([Circumscribe(VGroup(*[rows[k][1] for k in range(4)]), color=FOCUS)], t=0.9,
               hold=1.5)
        b.step([FadeIn(VGroup(*rows[4], *rows[5]))], t=0.6, hold=1.2)
        b.step([FadeIn(VGroup(*rows[6], *rows[7]))], t=0.6, hold=1.2)
        b.step([FadeIn(VGroup(*dcol))], t=0.7, hold=1.5)
        b.step([Indicate(VGroup(*dcol[1:5]), color=FOCUS)], t=0.8, hold=1)
        b.step(st.show("note", nt("the sick went; the healthy stayed home")), t=0.7, hold=2)
        b.step(st.show("note", mnote(r"y_{0i}:\ \text{health without}\quad y_{1i}:\ "
                                     r"\text{health with}\quad d_i:\ \text{received}")),
               t=0.8, hold=3)
        b.step([Circumscribe(g, color=GREY)], t=0.9, hold=1)
        b.run()


class B06FundamentalProblem(Scene):
    def construct(self):
        st, b = Stage(self), Beat(self, "B06FundamentalProblem")
        g = po_table()
        hid = unseen(g, D_SELF)
        b.step(st.show("title", Text("What could we actually see?", font_size=30,
                                     color=GREY)), t=0.7, hold=1)
        b.step(st.show("main", g), t=0.8, hold=1.5)
        b.step([hid[0].animate.set_color(GREYED)], t=0.6, hold=1.2)
        b.step([hid[1].animate.set_color(GREYED)], t=0.6, hold=0.8)
        b.step([hid[2].animate.set_color(GREYED)], t=0.6, hold=0.8)
        b.step([hid[3].animate.set_color(GREYED)], t=0.6, hold=0.8)
        b.step([hid[4].animate.set_color(GREYED)], t=0.6, hold=1.2)
        b.step([hid[5].animate.set_color(GREYED)], t=0.6, hold=0.8)
        b.step([hid[6].animate.set_color(GREYED)], t=0.6, hold=0.8)
        b.step([hid[7].animate.set_color(GREYED)], t=0.6, hold=0.8)
        b.step(st.show("note", nt("exactly half the table is missing")), t=0.7, hold=2)
        b.step(st.show("note", nt("Holland (1986): the fundamental problem of causal "
                                  "inference", FOCUS)), t=0.7, hold=3)
        b.step(st.show("note", nt("not a data problem, not a sample-size problem: "
                                  "built into the definition")), t=0.7, hold=3)
        b.step(st.show("note", nt("individual effects are out of reach")), t=0.7, hold=3)
        b.run()


class B07SwitchingEquation(Scene):
    def construct(self):
        st, b = Stage(self), Beat(self, "B07SwitchingEquation")
        rows = deriv([
            r"y_i = \begin{cases} y_{1i} & \text{if } d_i = 1 \\ y_{0i} & \text{if } d_i = 0"
            r"\end{cases}",
            r"y_i = d_i\, y_{1i} + (1 - d_i)\, y_{0i}",
            r"y_i = d_i\, y_{1i} + y_{0i} - d_i\, y_{0i}",
            r"y_i = y_{0i} + (y_{1i} - y_{0i})\, d_i",
            r"\text{Ana: } 5 = 3 + 2 \cdot 1",
            r"\text{Elisa: } 8 = 8 + 0 \cdot 0"])
        b.step(st.show("title", Text("The switching equation (MHE eq. 2.1.1)", font_size=30,
                                     color=GREY)), t=0.7, hold=1)
        b.step([FadeIn(reg(st, "main", rows[0]))], t=0.8, hold=1.5)
        b.step(st.show("note", nt("treatment picks the column")), t=0.6, hold=1.5)
        b.step(step_line(st, rows, 1), t=1.2, hold=2)
        b.step(st.show("note", nt("d is 0 or 1: write the choice as a sum")), t=0.6,
               hold=2)
        b.step(step_line(st, rows, 2), t=1.2, hold=1.5)
        b.step(st.show("note", nt("multiply out")), t=0.6, hold=1)
        b.step([Indicate(rows[2][0], color=FOCUS)], t=0.7, hold=0.5)
        b.step(step_line(st, rows, 3), t=1.2, hold=1.5)
        b.step(st.show("note", nt("collect the terms in dᵢ")), t=0.6, hold=1)
        b.step([Circumscribe(rows[3][0], color=FOCUS)], t=0.9, hold=1)
        b.step([FadeIn(reg(st, "main", rows[4]))], t=0.7, hold=2)
        b.step([FadeIn(reg(st, "main", rows[5]))], t=0.7, hold=2)
        res = MathTex(r"y_i", "=", r"y_{0i}", "+", r"(y_{1i} - y_{0i})", r"\, d_i",
                      font_size=60)
        res[2].set_color(Y0C)
        res[4].set_color(EFF)
        b.step(st.show("main", res) + st.show("note", nt("MHE eq. 2.1.1")), t=0.9, hold=2)
        b.step(st.show("note", nt("everyone starts at y₀; treatment adds their own effect")),
               t=0.7, hold=3)
        b.step([Indicate(res[4], color=EFF)], t=0.8, hold=2)
        b.step(st.show("note", nt("the effect is in the data, but not person by person",
                                  FOCUS)), t=0.7, hold=3)
        b.run()


class B08Estimands(Scene):
    def construct(self):
        st, b = Stage(self), Beat(self, "B08Estimands")
        g = po_table(cols=("y0", "y1", "d", "eff"))
        e = g.colidx["eff"]
        b.step(st.show("title", Text("Three averages of the same effects", font_size=30,
                                     color=GREY)), t=0.7, hold=1)
        show = st.show("left", g)
        effs = hide(g, [g.cells[(r, e)] for r in range(1, 9)])
        b.step(show, t=0.8, hold=1)
        for m in effs:
            st.add_to("left", m)
        b.step([FadeIn(VGroup(*effs[:4]))], t=0.7, hold=2)
        b.step([Indicate(VGroup(*effs[:4]), color=EFF)], t=0.7, hold=1)
        b.step([FadeIn(VGroup(*effs[4:6]))], t=0.6, hold=1)
        b.step([Indicate(effs[5], color=BIAS)], t=0.8, hold=1)
        b.step([FadeIn(VGroup(*effs[6:]))], t=0.6, hold=1)
        sums = column([r"\tfrac{2+3+2+1+0-1+1+1}{8} = 1.125",
                       r"\tfrac{2+3+2+1}{4} = 2",
                       r"\tfrac{0-1+1+1}{4} = 0.25"], "right", size=32)
        b.step([FadeIn(reg(st, "right", sums[0]))], t=0.7, hold=2.5)
        b.step([Circumscribe(VGroup(*effs), color=EFF)], t=0.9, hold=1.5)
        b.step([FadeIn(reg(st, "right", sums[1])),
                Indicate(VGroup(*effs[:4]), color=FOCUS)], t=0.8, hold=2)
        b.step([FadeIn(reg(st, "right", sums[2])),
                Indicate(VGroup(*effs[4:]), color=FOCUS)], t=0.8, hold=2)
        names = column([r"\text{ATE} = E[y_{1i}-y_{0i}] = 1.125",
                        r"\text{ATT} = E[y_{1i}-y_{0i}\mid d_i=1] = 2",
                        r"\text{ATU} = E[y_{1i}-y_{0i}\mid d_i=0] = 0.25"], "right", size=28,
                       colours={0: EFF, 1: EFF, 2: EFF})
        b.step(st.clear("right") + [FadeIn(reg(st, "right", names[0]))], t=0.8, hold=2.5)
        b.step([FadeIn(reg(st, "right", names[1]))], t=0.7, hold=2)
        b.step([FadeIn(reg(st, "right", names[2]))], t=0.7, hold=2)
        b.step([Indicate(names[0], color=FOCUS)], t=0.7, hold=1)
        b.step(st.show("note", nt("those who expect to gain seek treatment")), t=0.7,
               hold=3)
        b.step([Circumscribe(names[1], color=FOCUS)], t=0.9, hold=1)
        b.step(st.show("note", nt("ATT ≠ ATE: different questions, different answers")),
               t=0.7, hold=2.5)
        b.step(st.show("note", nt("keep it open: ATT · send everyone: ATE · extend care: "
                                  "ATU")), t=0.7, hold=4)
        b.step([Indicate(names[2], color=FOCUS)], t=0.8, hold=2)
        b.run()


# =================================================================== Act III

class B09NaiveOnTable(Scene):
    def construct(self):
        st, b = Stage(self), Beat(self, "B09NaiveOnTable")
        g = po_table()
        grey_now(unseen(g, D_SELF))
        y1, y0 = g.colidx["y1"], g.colidx["y0"]
        calc = column([r"\bar y_{\,d=1} = \tfrac{5+5+6+4}{4} = 5",
                       r"\bar y_{\,d=0} = \tfrac{8+9+7+8}{4} = 8",
                       r"5 - 8 = -3", r"\text{ATT} = +2"], "right", size=32,
                      colours={2: FOCUS, 3: EFF})
        b.step(st.show("title", Text("What the data show", font_size=30, color=GREY)),
               t=0.7, hold=1)
        b.step(st.show("left", g), t=0.8, hold=1.5)
        b.step([Indicate(VGroup(*[g.cells[(r, y1)] for r in range(1, 5)]), color=FOCUS)],
               t=0.8, hold=1)
        b.step([FadeIn(reg(st, "right", calc[0]))], t=0.7, hold=1.5)
        b.step([Indicate(VGroup(*[g.cells[(r, y0)] for r in range(5, 9)]), color=FOCUS)],
               t=0.8, hold=1)
        b.step([FadeIn(reg(st, "right", calc[1]))], t=0.7, hold=1.5)
        b.step([FadeIn(reg(st, "right", calc[2]))], t=0.7, hold=1.5)
        b.step(st.show("note", nt("the comparison says: the hospital lowers health by 3",
                                  BIAS)), t=0.7, hold=2.5)
        b.step(st.show("note", nt("true effect on each treated person: +2, +3, +2, +1",
                                  EFF)), t=0.7, hold=2.5)
        b.step([FadeIn(reg(st, "right", calc[3]))], t=0.7, hold=2)
        b.step(st.show("note", nt("wrong size and wrong sign", BIAS)), t=0.7, hold=2)
        b.step([Circumscribe(calc[2], color=BIAS)], t=0.9, hold=1)
        b.step(st.show("note", nt("five hidden points: where do they come from?", FOCUS)),
               t=0.7, hold=3)
        b.run()


class B10DerivationATT(Scene):
    def construct(self):
        st, b = Stage(self), Beat(self, "B10DerivationATT")
        rows = deriv([
            r"\text{Naive} = E[y_i\mid d_i{=}1] - E[y_i\mid d_i{=}0]",
            r"= E[y_{1i}\mid d_i{=}1] - E[y_{0i}\mid d_i{=}0]",
            r"= E[y_{1i}\mid d_i{=}1] - E[y_{0i}\mid d_i{=}1] + E[y_{0i}\mid d_i{=}1]"
            r" - E[y_{0i}\mid d_i{=}0]",
            r"= E[y_{1i}-y_{0i}\mid d_i{=}1] + \{E[y_{0i}\mid d_i{=}1] - E[y_{0i}\mid "
            r"d_i{=}0]\}",
            r"= \text{ATT} + \text{selection bias}"], size=32)
        b.step(st.show("title", Text("Decomposing the naive comparison (MHE p. 11)",
                                     font_size=30, color=GREY)), t=0.7, hold=1)
        b.step([FadeIn(reg(st, "main", rows[0]))], t=0.8, hold=2)
        b.step(st.show("note", nt("start from what the survey computed")), t=0.6, hold=1.5)
        b.step([Indicate(rows[0][0], color=FOCUS)], t=0.7, hold=1)
        b.step(step_line(st, rows, 1), t=1.2, hold=2)
        b.step(st.show("note", nt("switching equation: treated show y₁, untreated show y₀")),
               t=0.6, hold=2)
        b.step([Indicate(rows[1][0], color=FOCUS)], t=0.7, hold=1)
        b.step(st.show("note", mnote(r"\text{bridge: } E[y_{0i}\mid d_i{=}1]\ \ "
                                     r"\text{(treated people, untreated world)}", FOCUS)),
               t=0.8, hold=3)
        b.step(st.show("note", nt("add it and subtract it: adding zero changes nothing")),
               t=0.6, hold=2)
        b.step([Indicate(rows[1][0], color=GREY)], t=0.6, hold=0.5)
        b.step(step_line(st, rows, 2), t=1.4, hold=2.5)
        b.step([Indicate(rows[2][0], color=FOCUS)], t=0.7, hold=1)
        b.step(st.show("note", nt("group: same conditioning → linearity of expectations")),
               t=0.6, hold=1.5)
        b.step(step_line(st, rows, 3), t=1.4, hold=2.5)
        b.step([Indicate(rows[3][0], color=FOCUS)], t=0.7, hold=1)
        b.step(step_line(st, rows, 4), t=1.2, hold=2)
        b.step([Circumscribe(rows[4][0], color=FOCUS)], t=0.9, hold=1)
        res = MathTex(r"E[y_i|d_i{=}1]-E[y_i|d_i{=}0]", "=",
                      r"E[y_{1i}-y_{0i}|d_i{=}1]", "+",
                      r"E[y_{0i}|d_i{=}1]-E[y_{0i}|d_i{=}0]", font_size=40)
        res[2].set_color(EFF)
        res[4].set_color(BIAS)
        b.step(st.show("main", res) + st.show("note", nt("an identity: nothing assumed")),
               t=0.9, hold=2)
        b.step([Indicate(res[0], color=FOCUS)], t=0.7, hold=1.5)
        br1 = Brace(res[2], DOWN, color=EFF)
        l1 = Text("ATT", font_size=26, color=EFF).next_to(br1, DOWN, buff=0.12)
        br2 = Brace(res[4], DOWN, color=BIAS)
        l2 = Text("selection bias", font_size=26, color=BIAS).next_to(br2, DOWN, buff=0.12)
        for m in (br1, l1, br2, l2):
            st.add_to("main", m)
        b.step([GrowFromCenter(br1), FadeIn(l1)], t=0.8, hold=2)
        b.step([GrowFromCenter(br2), FadeIn(l2)], t=0.8, hold=2)
        b.step([Circumscribe(VGroup(br1, l1, br2, l2), color=GREY)], t=0.9, hold=1.5)
        b.step(st.show("note", nt("both terms in the bias are untreated outcomes")), t=0.7,
               hold=3)
        b.step([Circumscribe(res[4], color=BIAS)], t=0.9, hold=1)
        b.step(st.show("note", nt("in a world without hospitals, would the treated look "
                                  "different?", FOCUS)), t=0.7, hold=4)
        b.run()


class B11PlugNumbers(Scene):
    def construct(self):
        st, b = Stage(self), Beat(self, "B11PlugNumbers")
        b.step(st.show("title", Text("Putting the table into the identity", font_size=30,
                                     color=GREY)), t=0.7, hold=1)
        f = MathTex(r"\text{Naive}", "=", r"\text{ATT}", "+", r"\text{selection bias}",
                    font_size=52)
        f[2].set_color(EFF)
        f[4].set_color(BIAS)
        b.step(st.show("main", f), t=0.8, hold=1.5)
        b.step(st.show("note", mnote(r"\text{Naive} = 5 - 8 = -3")), t=0.7, hold=2)
        b.step(st.show("note", mnote(r"\text{ATT} = \tfrac{2+3+2+1}{4} = 2", EFF)), t=0.7,
               hold=2)
        b.step(st.show("note", mnote(r"\text{SB} = \tfrac{3+2+4+3}{4} - \tfrac{8+9+7+8}{4}"
                                     r" = 3 - 8 = -5", BIAS)), t=0.7, hold=3)
        nums = MathTex("-3", "=", "2", "+", "(-5)", font_size=60)
        nums[2].set_color(EFF)
        nums[4].set_color(BIAS)
        Stage.fit(nums, "main")
        st._held["main"] = nums
        b.step([TransformMatchingShapes(f, nums)], t=1.2, hold=2)
        ax, panel = axes_panel([0, 4, 1], [-6, 3, 1], width=8.0, height=4.2)
        ax.y_axis.add_numbers(font_size=18)
        b.step(st.show("main", panel) + st.show("note", nt("bars: what the data mix "
                                                           "together")), t=0.8, hold=1)

        def bar(x, v, colour):
            top, bot = ax.c2p(x, max(v, 0)), ax.c2p(x, min(v, 0))
            return Rectangle(width=0.9, height=top[1] - bot[1], fill_color=colour,
                             fill_opacity=0.85, stroke_width=0).move_to(
                (top + bot) / 2)

        g, r, n = bar(1, 2, EFF), bar(2, -5, BIAS), bar(3, -3, GREY)
        lg = Text("ATT +2", font_size=22, color=EFF).next_to(g, UP, buff=0.1)
        lr = Text("selection bias −5", font_size=22, color=BIAS).next_to(r, DOWN, buff=0.1)
        ln = Text("naive −3", font_size=22, color=GREY_A).next_to(n, DOWN, buff=0.1)
        for m in (g, r, n, lg, lr, ln):
            reg(st, "main", m)
        b.step([GrowFromEdge(g, DOWN), FadeIn(lg)], t=0.8, hold=1.5)
        b.step([GrowFromEdge(r, UP), FadeIn(lr)], t=0.8, hold=1.5)
        b.step([TransformFromCopy(VGroup(g, r), n), FadeIn(ln)], t=1.2, hold=2)
        b.step([Indicate(g, color=EFF)], t=0.8, hold=1)
        b.step(st.show("note", nt("a real, positive effect under a bias twice its size")),
               t=0.7, hold=3)
        b.step([Indicate(r, color=BIAS)], t=0.8, hold=1)
        b.step(st.show("note", nt("the hospital beds held the sick, not a random draw",
                                  FOCUS)), t=0.7, hold=3)
        b.run()


class B12SignOfBias(Scene):
    def construct(self):
        st, b = Stage(self), Beat(self, "B12SignOfBias")
        cards = VGroup(
            card("Job training", "trainees: low earnings\npotential to begin with",
                 r"\text{bias} < 0", BIAS),
            card("Hormone therapy", "users differed in ways\nthat flattered it",
                 r"\text{bias} > 0", BIAS),
            card("Class size", "weaker students placed\nin smaller classes",
                 r"\text{bias} < 0", BIAS)).arrange(RIGHT, buff=0.3)
        Stage.fit(cards, "main")
        b.step(st.show("title", Text("The sign of the bias (MHE pp. 12–16)", font_size=30,
                                     color=GREY)), t=0.7, hold=1)
        b.step([FadeIn(reg(st, "main", VGroup(cards[0][0], cards[0][1])))], t=0.7, hold=1)
        b.step([FadeIn(reg(st, "main", cards[0][2]))], t=0.6, hold=2)
        b.step([FadeIn(reg(st, "main", cards[0][3]))], t=0.6, hold=1.5)
        b.step([Indicate(cards[0][3], color=FOCUS)], t=0.6, hold=0.5)
        b.step(st.show("note", nt("randomised evaluations: mostly positive effects", EFF)),
               t=0.7, hold=1.5)
        b.step([FadeIn(reg(st, "main", VGroup(cards[1][0], cards[1][1])))], t=0.7, hold=1)
        b.step([FadeIn(reg(st, "main", cards[1][2]))], t=0.6, hold=2)
        b.step([FadeIn(reg(st, "main", cards[1][3]))], t=0.6, hold=1.5)
        b.step(st.show("note", nt("the trial: few benefits, serious side effects")), t=0.7,
               hold=1.5)
        b.step([FadeIn(reg(st, "main", VGroup(cards[2][0], cards[2][1])))], t=0.7, hold=1)
        b.step([FadeIn(reg(st, "main", cards[2][2]))], t=0.6, hold=2)
        b.step([FadeIn(reg(st, "main", cards[2][3]))], t=0.6, hold=1.5)
        b.step([Indicate(VGroup(cards[0][3], cards[1][3], cards[2][3]), color=FOCUS)],
               t=0.8, hold=1)
        b.step(st.show("note", nt("no general rule: ask who walks through the door, and why",
                                  FOCUS)), t=0.7, hold=3)
        b.run()


class B12bMirror(Scene):
    def construct(self):
        st, b = Stage(self), Beat(self, "B12bMirror")
        g = po_table(d=D_MIRROR)
        hid = unseen(g, D_MIRROR)
        calc = column([r"\bar y_{\,d=1} = \tfrac{8+8+8+9}{4} = 8.25",
                       r"\bar y_{\,d=0} = \tfrac{3+2+4+3}{4} = 3",
                       r"\text{Naive} = +5.25"], "right", size=32, colours={2: FOCUS})
        ident = column([r"\text{ATT} = \tfrac{0-1+1+1}{4} = 0.25",
                        r"\text{SB} = 8 - 3 = +5", r"0.25 + 5 = 5.25\ \checkmark"], "right",
                       size=32, colours={0: EFF, 1: BIAS})
        b.step(st.show("title", Text("Same people, opposite selection", font_size=30,
                                     color=GREY)), t=0.7, hold=1)
        b.step(st.show("left", g), t=0.8, hold=1.5)
        b.step([Indicate(VGroup(*[g.cells[(r, 3)] for r in range(1, 9)]), color=FOCUS)]
               + st.show("note", nt("only the d column changed")), t=0.8, hold=2)
        b.step([m.animate.set_color(GREYED) for m in hid], t=0.8, hold=1.5)
        b.step([FadeIn(reg(st, "right", calc[0]))], t=0.7, hold=1.5)
        b.step([FadeIn(reg(st, "right", calc[1]))], t=0.7, hold=1.5)
        b.step([FadeIn(reg(st, "right", calc[2]))], t=0.7, hold=1.5)
        b.step(st.show("note", nt("a clinic that looks miraculous", FOCUS)), t=0.7, hold=1.5)
        b.step(st.clear("right") + [FadeIn(reg(st, "right", ident[0]))], t=0.8, hold=2)
        b.step([FadeIn(reg(st, "right", ident[1]))], t=0.7, hold=2)
        b.step([FadeIn(reg(st, "right", ident[2]))], t=0.7, hold=1.5)
        b.step(st.show("note", nt("one selection rule: −3 · the other: +5.25")), t=0.7,
               hold=3)
        b.step([Circumscribe(ident[1], color=BIAS)], t=0.9, hold=1)
        b.step(st.show("note", nt("the naive comparison measures the selection rule",
                                  FOCUS)), t=0.7, hold=3)
        b.run()


class B13DerivationATE(Scene):
    def construct(self):
        st, b = Stage(self), Beat(self, "B13DerivationATE")
        rows = deriv([
            r"\text{ATE} = \pi\,\text{ATT} + (1-\pi)\,\text{ATU}",
            r"\text{ATE} = \text{ATT} - (1-\pi)\,\text{ATT} + (1-\pi)\,\text{ATU}",
            r"\text{ATE} = \text{ATT} - (1-\pi)(\text{ATT}-\text{ATU})",
            r"\text{ATT} = \text{ATE} + (1-\pi)(\text{ATT}-\text{ATU})",
            r"\text{Naive} = \text{ATT} + \text{SB}",
            r"\text{Naive} = \text{ATE} + \text{SB} + (1-\pi)(\text{ATT}-\text{ATU})"],
            size=36)
        b.step(st.show("title", Text("From the ATT to the ATE", font_size=30, color=GREY)),
               t=0.7, hold=1)
        b.step(st.show("note", mnote(r"\pi = P(d_i = 1) = \tfrac{1}{2}")), t=0.7, hold=1.5)
        b.step([FadeIn(reg(st, "main", rows[0]))], t=0.8, hold=1.5)
        b.step(st.show("note", nt("law of iterated expectations")), t=0.6, hold=1.5)
        b.step([Indicate(rows[0][0], color=FOCUS)], t=0.7, hold=1)
        b.step(step_line(st, rows, 1), t=1.2, hold=2)
        b.step(st.show("note", mnote(r"\pi\,\text{ATT} = \text{ATT} - (1-\pi)\,\text{ATT}")),
               t=0.6, hold=1)
        b.step(step_line(st, rows, 2), t=1.2, hold=2)
        b.step(st.show("note", nt("collect the terms in (1 − π)")), t=0.6, hold=1)
        b.step(step_line(st, rows, 3), t=1.2, hold=2)
        b.step([Indicate(rows[3][0], color=FOCUS)], t=0.7, hold=1)
        b.step([FadeIn(reg(st, "main", rows[4]))]
               + st.show("note", nt("our identity from before")), t=0.8, hold=1.5)
        b.step(step_line(st, rows, 5), t=1.4, hold=2.5)
        b.step([Circumscribe(rows[5][0], color=FOCUS)], t=0.9, hold=1.5)
        res = MathTex(r"\text{Naive}", "=", r"\text{ATE}", "+", r"\text{SB}", "+",
                      r"(1-\pi)(\text{ATT}-\text{ATU})", font_size=50)
        res[2].set_color(EFF)
        res[4].set_color(BIAS)
        res[6].set_color(HET)
        b.step(st.show("main", res), t=0.9, hold=1.5)
        br1 = Brace(res[4], DOWN, color=BIAS)
        l1 = Text("selection bias", font_size=24, color=BIAS).next_to(br1, DOWN, buff=0.12)
        br2 = Brace(res[6], DOWN, color=HET)
        l2 = Text("heterogeneity bias", font_size=24, color=HET).next_to(br2, DOWN,
                                                                        buff=0.12)
        for m in (br1, l1, br2, l2):
            st.add_to("main", m)
        b.step([GrowFromCenter(br1), FadeIn(l1)]
               + st.show("note", nt("baseline difference: groups differ untreated")),
               t=0.8, hold=2.5)
        b.step([GrowFromCenter(br2), FadeIn(l2)]
               + st.show("note", nt("difference in gains: groups would gain different "
                                    "amounts")), t=0.8, hold=2.5)
        b.step(st.show("note", nt("same effect for all → ATT = ATU → term vanishes")),
               t=0.7, hold=2.5)
        b.step([Indicate(res[2], color=EFF)], t=0.7, hold=1)
        b.step(st.show("note", nt("selection on gains → ATT > ATU → term > 0", FOCUS)),
               t=0.7, hold=3)
        b.step([Circumscribe(res[6], color=HET)], t=0.9, hold=1)
        b.run()


class B14PlugATE(Scene):
    def construct(self):
        st, b = Stage(self), Beat(self, "B14PlugATE")
        b.step(st.show("title", Text("Every term from the table", font_size=30, color=GREY)),
               t=0.6, hold=0.5)
        f = MathTex(r"\text{Naive}", "=", r"\text{ATE}", "+", r"\text{SB}", "+",
                    r"(1-\pi)(\text{ATT}-\text{ATU})", font_size=48)
        f[2].set_color(EFF)
        f[4].set_color(BIAS)
        f[6].set_color(HET)
        b.step(st.show("main", f), t=0.7, hold=1)
        b.step(st.show("note", mnote(r"\text{ATE} = 1.125", EFF)), t=0.6, hold=1)
        b.step(st.show("note", mnote(r"\text{SB} = -5", BIAS)), t=0.6, hold=1)
        b.step(st.show("note", mnote(r"\tfrac{1}{2}\times(2 - 0.25) = 0.875", HET)), t=0.6,
               hold=1.5)
        nums = MathTex("-3", "=", "1.125", "-", "5", "+", "0.875", font_size=60)
        nums[2].set_color(EFF)
        nums[4].set_color(BIAS)
        nums[6].set_color(HET)
        Stage.fit(nums, "main")
        st._held["main"] = nums
        b.step([TransformMatchingShapes(f, nums)], t=1.0, hold=1.5)
        b.step([Indicate(nums[2], color=EFF)], t=0.6, hold=0.8)
        b.step([Indicate(nums[4], color=BIAS)], t=0.6, hold=0.8)
        b.step([Indicate(nums[6], color=HET)], t=0.6, hold=0.8)
        b.step(st.show("note", nt("average effect · baseline difference · difference in "
                                  "gains")), t=0.6, hold=2)
        b.step([Circumscribe(nums[0], color=FOCUS)], t=0.7, hold=1)
        b.step(st.show("note", nt("the same −3 the survey would report", FOCUS)), t=0.6,
               hold=1.5)
        b.run()


# ==================================================================== Act IV

class B15Independence(Scene):
    def construct(self):
        st, b = Stage(self), Beat(self, "B15Independence")
        g = po_table()
        dcells = [g.cells[(r, 3)] for r in range(1, 9)]
        b.step(st.show("title", Text("Take the decision away from the people", font_size=30,
                                     color=GREY)), t=0.7, hold=1)
        b.step(st.show("left", g), t=0.8, hold=1.5)
        b.step(st.show("note", nt("self-selection: the sick chose the hospital")), t=0.7,
               hold=1.5)
        b.step([Indicate(VGroup(*dcells), color=FOCUS)], t=0.8, hold=1)
        new = [Text(str(v), font_size=20, color=FOCUS).move_to(c)
               for v, c in zip(D_COIN, dcells)]
        b.step([Transform(c, n) for c, n in zip(dcells, new)]
               + st.show("note", nt("now a coin decides: heads, hospital")), t=1.0, hold=2.5)
        b.step(st.show("note", nt("the coin cannot see y₀ or y₁")), t=0.7, hold=2)
        stmt = column([r"(y_{0i},\, y_{1i}) \perp d_i",
                       r"E[y_{0i}\mid d_i{=}1] = E[y_{0i}\mid d_i{=}0]"], "right", size=34)
        b.step([FadeIn(reg(st, "right", stmt[0]))], t=0.8, hold=2.5)
        b.step([Circumscribe(stmt[0], color=FOCUS)], t=0.9, hold=1)
        b.step(st.show("note", nt("NOT: d unrelated to the observed outcome", BIAS)), t=0.7,
               hold=2.5)
        b.step(st.show("note", nt("IS: d unrelated to the outcomes people would have had",
                                  EFF)), t=0.7, hold=3)
        b.step([FadeIn(reg(st, "right", stmt[1]))], t=0.8, hold=2)
        b.step([Indicate(stmt[1], color=FOCUS)], t=0.8, hold=1)
        b.step(st.show("note", nt("after the coin, d says nothing about the person", FOCUS)),
               t=0.7, hold=2.5)
        b.run()


class B16DerivationRandom(Scene):
    def construct(self):
        st, b = Stage(self), Beat(self, "B16DerivationRandom")
        rows = deriv([
            r"\text{SB} = E[y_{0i}\mid d_i{=}1] - E[y_{0i}\mid d_i{=}0]",
            r"\text{SB} = E[y_{0i}] - E[y_{0i}] = 0",
            r"\text{ATT} = E[y_{1i}\mid d_i{=}1] - E[y_{0i}\mid d_i{=}1]",
            r"\text{ATT} = E[y_{1i}] - E[y_{0i}] = \text{ATE}",
            r"\text{ATU} = \text{ATE} \ \Rightarrow\ \text{ATT} - \text{ATU} = 0",
            r"\text{Naive} = E[y_i\mid d_i{=}1] - E[y_i\mid d_i{=}0] = \text{ATE}"], size=36)
        b.step(st.show("title", Text("Random assignment solves the selection problem",
                                     font_size=30, color=GREY)), t=0.7, hold=1)
        b.step([FadeIn(reg(st, "main", rows[0]))], t=0.8, hold=1.5)
        b.step(st.show("note", mnote(r"(y_{0i}, y_{1i}) \perp d_i")), t=0.6, hold=1)
        b.step(step_line(st, rows, 1), t=1.2, hold=2)
        b.step(st.show("note", nt("conditioning on d changes nothing")), t=0.6, hold=1.5)
        b.step([Indicate(rows[1][0], color=EFF)], t=0.8, hold=1)
        b.step([FadeIn(reg(st, "main", rows[2]))], t=0.8, hold=2)
        b.step(step_line(st, rows, 3), t=1.2, hold=2)
        b.step(st.show("note", nt("same argument for both potential outcomes")), t=0.6,
               hold=1.5)
        b.step([Indicate(rows[3][0], color=EFF)], t=0.7, hold=1)
        b.step([FadeIn(reg(st, "main", rows[4]))], t=0.8, hold=2)
        b.step([FadeIn(reg(st, "main", rows[5]))], t=0.8, hold=2)
        res = MathTex(r"\text{Naive}", "=", r"\text{ATE}", font_size=72)
        res[2].set_color(EFF)
        b.step(st.show("main", res), t=0.9, hold=1.5)
        b.step(st.show("note", nt("random assignment eliminates selection bias (MHE p. 12)",
                                  EFF)), t=0.7, hold=3)
        b.step([Circumscribe(res, color=FOCUS)], t=0.9, hold=1)
        b.step(st.show("note", nt("the benchmark for every method in this course", FOCUS)),
               t=0.7, hold=3)
        b.run()


class B16bIdealExperiment(Scene):
    def construct(self):
        st, b = Stage(self), Beat(self, "B16bIdealExperiment")

        def box(s, colour=GREY):
            t = Text(s, font_size=22, line_spacing=0.9)
            r = RoundedRectangle(corner_radius=0.15, width=t.width + 0.5,
                                 height=t.height + 0.4, color=colour)
            return VGroup(r, t.move_to(r))

        start = box("ER patients:\nadmission genuinely uncertain")
        coin = VGroup(Circle(radius=0.38, color=GOLD, fill_color=GOLD, fill_opacity=0.35))
        adm = box("admit", Y1C)
        hom = box("treat, send home", Y0C)
        out = box("same health question,\n12 months later")
        cmp_ = box("compare the two means", FOCUS)
        start.move_to(LEFT * 5)
        coin.move_to(LEFT * 2.4)
        adm.move_to(UP * 1.3 + RIGHT * 0.2)
        hom.move_to(DOWN * 1.3 + RIGHT * 0.2)
        out.move_to(RIGHT * 3.2)
        cmp_.move_to(RIGHT * 3.2 + DOWN * 1.9)
        a1 = Arrow(start.get_right(), coin.get_left(), buff=0.1)
        a2 = Arrow(coin.get_right(), adm.get_left(), buff=0.1, color=Y1C)
        a3 = Arrow(coin.get_right(), hom.get_left(), buff=0.1, color=Y0C)
        a4 = Arrow(adm.get_right(), out.get_left(), buff=0.1)
        a5 = Arrow(hom.get_right(), out.get_left(), buff=0.1)
        a6 = Arrow(out.get_bottom(), cmp_.get_top(), buff=0.1)
        diagram = VGroup(start, a1, coin, a2, adm, a3, hom, a4, a5, out, a6, cmp_)
        Stage.fit(diagram, "main")
        b.step(st.show("title", Text("The ideal experiment (MHE Ch. 1, question 2)",
                                     font_size=30, color=GREY)), t=0.7, hold=1)
        b.step([FadeIn(reg(st, "main", start))], t=0.7, hold=2)
        b.step([GrowArrow(reg(st, "main", a1)), FadeIn(reg(st, "main", coin))], t=0.8,
               hold=1.5)
        b.step([GrowArrow(reg(st, "main", a2)), FadeIn(reg(st, "main", adm))], t=0.7,
               hold=1)
        b.step([GrowArrow(reg(st, "main", a3)), FadeIn(reg(st, "main", hom))], t=0.7,
               hold=1)
        b.step([GrowArrow(reg(st, "main", a4)), GrowArrow(reg(st, "main", a5)),
                FadeIn(reg(st, "main", out))], t=0.8, hold=1.5)
        b.step([GrowArrow(reg(st, "main", a6)), FadeIn(reg(st, "main", cmp_))], t=0.7,
               hold=1.5)
        b.step(st.show("note", nt("1 · the margin where policy actually operates")), t=0.7,
               hold=2.5)
        b.step([Indicate(start, color=FOCUS)], t=0.8, hold=1)
        b.step(st.show("note", nt("2 · chance assigns treatment: selection bias = 0", EFF)),
               t=0.7, hold=2.5)
        b.step([Indicate(coin, color=FOCUS)], t=0.8, hold=1)
        b.step(st.show("note", nt("3 · the outcome is measured the same way in both arms")),
               t=0.7, hold=2.5)
        b.step(st.show("note", nt("no ethics committee would approve it", BIAS)), t=0.7,
               hold=2.5)
        b.step(st.show("note", nt("every later method imitates this coin", FOCUS)), t=0.7,
               hold=3)
        b.run()


def _all_gaps():
    gaps = []
    for treated in combinations(range(8), 4):
        t1 = sum(Y1[i] for i in treated) / 4
        t0 = sum(Y0[i] for i in range(8) if i not in treated) / 4
        gaps.append(t1 - t0)
    return gaps


class B17CoinFlips(Scene):
    def construct(self):
        st, b = Stage(self), Beat(self, "B17CoinFlips")
        g = po_table(d=D_COIN)
        grey_now(unseen(g, D_COIN))
        calc = column([r"\bar y_{\,d=1} = \tfrac{5+8+8+9}{4} = 7.5",
                       r"\bar y_{\,d=0} = \tfrac{2+4+3+7}{4} = 4",
                       r"7.5 - 4 = 3.5", r"\text{ATE} = 1.125"], "right", size=32,
                      colours={2: FOCUS, 3: EFF})
        b.step(st.show("title", Text("One experiment, then all seventy", font_size=30,
                                     color=GREY)), t=0.7, hold=1)
        b.step(st.show("left", g), t=0.8, hold=1.5)
        b.step([FadeIn(reg(st, "right", calc[0]))], t=0.7, hold=1.5)
        b.step([FadeIn(reg(st, "right", calc[1]))], t=0.7, hold=1.5)
        b.step([FadeIn(reg(st, "right", calc[2]))], t=0.7, hold=1)
        b.step([FadeIn(reg(st, "right", calc[3]))], t=0.7, hold=1)
        b.step(st.show("note", nt("one experiment: off by more than two points", BIAS)),
               t=0.7, hold=2)
        gaps = _all_gaps()
        counts = {}
        for v in gaps:
            k = round(v * 4) / 4
            counts[k] = counts.get(k, 0) + 1
        ax, panel = axes_panel([-3.5, 5.75, 1], [0, max(counts.values()) + 1, 2],
                               x_label="difference in means", width=9.0, height=3.8)
        ax.x_axis.add_numbers(range(-3, 6), font_size=18)
        panel[1].next_to(ax.x_axis, DOWN, buff=0.2)
        b.step(st.show("main", panel)
               + st.show("note", mnote(r"\binom{8}{4} = 70 \text{ possible experiments}")),
               t=0.8, hold=1.5)
        bars = VGroup(*[Rectangle(width=ax.x_axis.unit_size * 0.22,
                                  height=ax.c2p(0, c)[1] - ax.c2p(0, 0)[1],
                                  fill_color=GREY_B, fill_opacity=0.85, stroke_width=0)
                        .move_to(ax.c2p(x, 0), aligned_edge=DOWN)
                        for x, c in sorted(counts.items())])
        reg(st, "main", bars)
        b.step([LaggedStart(*[GrowFromEdge(r, DOWN) for r in bars], lag_ratio=0.05)],
               t=1.6, hold=2)
        mark = Dot(ax.c2p(3.5, 0), color=FOCUS, radius=0.1)
        ml = Text("our draw: 3.5", font_size=20, color=FOCUS).next_to(
            ax.c2p(3.5, max(counts.values()) + 1), UP, buff=0.1)
        reg(st, "main", mark); reg(st, "main", ml)
        b.step([FadeIn(mark), FadeIn(ml)], t=0.7, hold=1.5)
        b.step(st.show("note", nt("from −3 at one end to +5.25 at the other")), t=0.7,
               hold=2)
        line = DashedLine(ax.c2p(1.125, 0), ax.c2p(1.125, max(counts.values()) + 1),
                          color=EFF)
        ll = Text("mean = 1.125 = ATE", font_size=20, color=EFF).next_to(line, UP, buff=0.1)
        reg(st, "main", line); reg(st, "main", ll)
        b.step([Create(line), FadeIn(ll)], t=0.8, hold=3)
        b.step(st.show("note", nt("unbiased: right on average, not every time", EFF)),
               t=0.7, hold=3)
        b.step(st.show("note", nt("8 people: chance is large · 11,600 children: small")),
               t=0.7, hold=3)
        b.run()


class B17bSampleSize(Scene):
    def construct(self):
        st, b = Stage(self), Beat(self, "B17bSampleSize")
        sds = [(8, 1.608), (80, 0.479), (800, 0.151), (8000, 0.048)]
        ax, panel = axes_panel([-3, 5.5, 1], [0, 5, 1], x_label="difference in means",
                               width=8.0, height=3.8)
        ax.x_axis.add_numbers(range(-3, 6), font_size=18)
        panel[1].next_to(ax.x_axis, DOWN, buff=0.2)
        rows = []
        for k, (n, sd) in enumerate(sds):
            y = 4 - k
            seg = Line(ax.c2p(1.125 - 2 * sd, y), ax.c2p(1.125 + 2 * sd, y), color=Y1C,
                       stroke_width=8)
            dot = Dot(ax.c2p(1.125, y), color=WHITE, radius=0.07)
            lab = Text(f"n = {n:,}   sd = {sd:.2f}", font_size=20).next_to(
                ax.c2p(5.5, y), RIGHT, buff=0.15)
            rows.append(VGroup(seg, dot, lab))
        centre = DashedLine(ax.c2p(1.125, 0.3), ax.c2p(1.125, 4.7), color=EFF)
        comp = VGroup(panel, *rows, centre)
        b.step(st.show("title", Text("How fast chance shrinks", font_size=30, color=GREY)),
               t=0.7, hold=1)
        show = st.show("main", comp)
        hide(comp, rows + [centre])
        for m in rows + [centre]:
            reg(st, "main", m)
        b.step(show + st.show("note", nt("each bar: ±2 standard deviations of the "
                                         "estimate")), t=0.8, hold=2)
        b.step([Create(rows[0][0]), FadeIn(rows[0][1:])], t=0.8, hold=2)
        b.step([Create(rows[1][0]), FadeIn(rows[1][1:])], t=0.8, hold=1.5)
        b.step([Create(rows[2][0]), FadeIn(rows[2][1:])], t=0.8, hold=1.5)
        b.step([Create(rows[3][0]), FadeIn(rows[3][1:])], t=0.8, hold=1.5)
        b.step([Create(centre)] + st.show("note", nt("every distribution centred on 1.125",
                                                     EFF)), t=0.8, hold=2)
        b.step(st.show("note", nt("spread ∝ 1 / √n: ×100 people → ÷10 spread")), t=0.7,
               hold=3)
        b.step([Indicate(rows[0][2], color=FOCUS), Indicate(rows[2][2], color=FOCUS)],
               t=0.8, hold=1.5)
        b.step(st.show("note", nt("start of class: ever more precise about a biased number",
                                  BIAS)), t=0.7, hold=2.5)
        b.step(st.show("note", nt("here: ever more precise about the right number", EFF)),
               t=0.7, hold=2.5)
        b.step(st.show("note", nt("identification first, precision second", FOCUS)), t=0.7,
               hold=3)
        b.step([Circumscribe(rows[3], color=FOCUS)], t=0.9, hold=1)
        b.run()


class B18SUTVA(Scene):
    def construct(self):
        st, b = Stage(self), Beat(self, "B18SUTVA")
        hus = VGroup(Dot(radius=0.14, color=Y1C),
                     Text("husband: hospital", font_size=24, color=Y1C))
        hus[1].next_to(hus[0], DOWN, buff=0.15)
        eli = VGroup(Dot(radius=0.14, color=Y0C), Text("Elisa: home", font_size=24,
                                                       color=Y0C))
        eli[1].next_to(eli[0], DOWN, buff=0.15)
        hus.move_to(LEFT * 3.5)
        eli.move_to(RIGHT * 3.5)
        arr = CurvedArrow(hus[0].get_center() + RIGHT * 0.3 + UP * 0.2,
                          eli[0].get_center() + LEFT * 0.3 + UP * 0.2, angle=-PI / 4,
                          color=BIAS)
        lab = Text("infection", font_size=22, color=BIAS).next_to(arr, UP, buff=0.1)
        scene_ = VGroup(hus, eli, arr, lab)
        Stage.fit(scene_, "main")
        b.step(st.show("title", Text("The assumption inside the table: SUTVA", font_size=30,
                                     color=GREY)), t=0.7, hold=1)
        b.step([FadeIn(reg(st, "main", hus)), FadeIn(reg(st, "main", eli))], t=0.8,
               hold=1.5)
        b.step([Create(reg(st, "main", arr)), FadeIn(reg(st, "main", lab))], t=0.8,
               hold=2)
        b.step(st.show("note", mnote(r"y_{0,\text{Elisa}}\ \text{now depends on}\ "
                                     r"d_{\text{husband}}", BIAS)), t=0.7, hold=2.5)
        b.step(st.show("note", mnote(r"2^8 = 256\ \text{treatment patterns, an outcome for "
                                     r"each}")), t=0.7, hold=2.5)
        parts = VGroup(Text("1 · no interference between units", font_size=30),
                       Text("2 · no hidden versions of treatment", font_size=30)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.6)
        Stage.fit(parts, "main")
        b.step(st.clear("main") + st.show("note", nt("stable unit treatment value "
                                                     "assumption (Rubin)")), t=0.7, hold=1)
        b.step([FadeIn(reg(st, "main", parts[0]))], t=0.7, hold=2)
        b.step([FadeIn(reg(st, "main", parts[1]))], t=0.7, hold=2)
        b.step(st.show("note", nt("not tested by the data: a judgement about the setting",
                                  FOCUS)), t=0.7, hold=2.5)
        b.step(st.show("note", nt("can fail: vaccines · classroom peers · market spillovers")),
               t=0.7, hold=3)
        b.step([Indicate(parts[0], color=FOCUS)], t=0.8, hold=1)
        b.step([Indicate(parts[1], color=FOCUS)], t=0.8, hold=1)
        b.run()


# ===================================================================== Act V

class B19STARBalance(Scene):
    def construct(self):
        st, b = Stage(self), Beat(self, "B19STARBalance")
        rows = [["free lunch", ".47", ".48", ".50", ".09"],
                ["white / Asian", ".68", ".67", ".66", ".26"],
                ["age in 1985", "5.44", "5.43", "5.42", ".32"],
                ["attrition rate", ".49", ".52", ".53", ".02"],
                ["class size, K", "15.10", "22.40", "22.80", ".00"],
                ["percentile score, K", "54.70", "48.90", "50.00", ".00"]]
        t = table(["variable", "small", "regular", "regular/aide", "p-value"], rows,
                  col_widths=[3.6, 1.6, 1.6, 2.2, 1.6], row_height=0.6, font_size=22)
        cells = [m for m in t.submobjects if isinstance(m, Text)]
        b.step(st.show("title", Text("Tennessee STAR · MHE Table 2.2.1 (Krueger 1999)",
                                     font_size=28, color=GREY)), t=0.7, hold=1)
        b.step(st.show("note", nt("≈ 11,600 children · ≈ 12 million dollars · random "
                                  "within schools")), t=0.7, hold=3)
        show = st.show("main", t)
        rr = [hide(t, cells[5 + 5 * k: 10 + 5 * k]) for k in range(6)]
        b.step(show, t=0.8, hold=1.5)
        for grp in rr:
            st.add_to("main", VGroup(*grp))
        b.step([FadeIn(VGroup(*rr[0]))], t=0.6, hold=1.5)
        b.step([FadeIn(VGroup(*rr[1]))], t=0.6, hold=1)
        b.step([FadeIn(VGroup(*rr[2]))], t=0.6, hold=1)
        b.step(st.show("note", nt("balanced: no significant differences", EFF)), t=0.7,
               hold=2)
        b.step([Circumscribe(VGroup(rr[0][4], rr[1][4], rr[2][4]), color=EFF)], t=0.9,
               hold=1.5)
        b.step([FadeIn(VGroup(*rr[3]))], t=0.6, hold=1.5)
        b.step([Indicate(rr[3][4], color=BIAS)], t=0.7, hold=1)
        b.step(st.show("note", nt("attrition lower in small classes: kindergarten results "
                                  "most reliable")), t=0.7, hold=2.5)
        b.step([FadeIn(VGroup(*rr[4]))], t=0.6, hold=1.5)
        b.step([Circumscribe(VGroup(*rr[4]), color=FOCUS)], t=0.9, hold=1)
        b.step(st.show("note", nt("the experiment created the variation it intended")),
               t=0.7, hold=2)
        b.step([FadeIn(VGroup(*rr[5]))], t=0.6, hold=2)
        b.step([Circumscribe(VGroup(*rr[5]), color=FOCUS)], t=0.9, hold=2)
        b.run()


class B20STAREffect(Scene):
    def construct(self):
        st, b = Stage(self), Beat(self, "B20STAREffect")
        rows = [["small class", "4.82", "5.37", "5.36", "5.37"],
                ["   (s.e.)", "(2.19)", "(1.26)", "(1.21)", "(1.19)"],
                ["regular/aide", ".12", ".29", ".53", ".31"],
                ["   (s.e.)", "(2.23)", "(1.13)", "(1.09)", "(1.07)"],
                ["school fixed effects", "no", "yes", "yes", "yes"],
                ["student controls", "no", "no", "yes", "yes"],
                ["teacher controls", "no", "no", "no", "yes"]]
        t = table(["regressor", "(1)", "(2)", "(3)", "(4)"], rows,
                  col_widths=[3.8, 1.6, 1.6, 1.6, 1.6], row_height=0.56, font_size=22)
        texts = [m for m in t.submobjects if isinstance(m, Text)]
        body = texts[5:]
        col = {c: [body[r * 5 + c] for r in range(7)] for c in range(5)}
        b.step(st.show("title", Text("STAR: effect on kindergarten scores · MHE Table 2.2.2",
                                     font_size=28, color=GREY)), t=0.7, hold=1)
        show = st.show("main", t)
        hidden = [hide(t, col[c]) for c in (1, 2, 3, 4)]
        b.step(show, t=0.8, hold=1.5)
        for grp in hidden:
            st.add_to("main", VGroup(*grp))
        b.step([FadeIn(VGroup(*hidden[0]))], t=0.7, hold=2)
        b.step([FadeIn(VGroup(*hidden[1]))], t=0.7, hold=2)
        b.step([Indicate(hidden[1][4], color=FOCUS)], t=0.7, hold=1)
        b.step([FadeIn(VGroup(*hidden[2]))], t=0.7, hold=1.5)
        b.step([Indicate(VGroup(hidden[2][5], hidden[3][6]), color=FOCUS)], t=0.7,
               hold=1)
        b.step([FadeIn(VGroup(*hidden[3]))], t=0.7, hold=1.5)
        b.step([Circumscribe(VGroup(*[h[0] for h in hidden]), color=EFF)], t=0.9, hold=2)
        b.step(st.show("note", nt("the estimate barely moves: controls unrelated to "
                                  "treatment")), t=0.7, hold=2.5)
        b.step([Circumscribe(VGroup(*[h[1] for h in hidden]), color=FOCUS)], t=0.9, hold=1.5)
        b.step(st.show("note", nt("s.e. 2.19 → 1.19: controls explain variance, not bias",
                                  FOCUS)), t=0.7, hold=3)
        b.step(st.show("note", nt("≈ 5 percentile points ≈ 0.2 standard deviations", EFF)),
               t=0.7, hold=2.5)
        b.step([Indicate(VGroup(*[h[2] for h in hidden]), color=GREY)], t=0.8, hold=1)
        b.step(st.show("note", nt("regular/aide: small and not significant")), t=0.7,
               hold=2)
        b.run()


class B21RegressionForm(Scene):
    def construct(self):
        st, b = Stage(self), Beat(self, "B21RegressionForm")
        rows = deriv([
            r"y_i = y_{0i} + (y_{1i} - y_{0i})\, d_i",
            r"y_i = y_{0i} + \rho\, d_i \qquad (y_{1i} - y_{0i} = \rho)",
            r"y_{0i} = \alpha + \eta_i, \qquad \alpha = E[y_{0i}]",
            r"y_i = \alpha + \rho\, d_i + \eta_i",
            r"E[y_i\mid d_i{=}1] - E[y_i\mid d_i{=}0] = \rho + E[\eta_i\mid d_i{=}1] - "
            r"E[\eta_i\mid d_i{=}0]",
            r"E[\eta_i\mid d_i{=}1] - E[\eta_i\mid d_i{=}0] = E[y_{0i}\mid d_i{=}1] - "
            r"E[y_{0i}\mid d_i{=}0]"], size=32)
        b.step(st.show("title", Text("Regression and potential outcomes (MHE eq. 2.3.1)",
                                     font_size=30, color=GREY)), t=0.7, hold=1)
        b.step([FadeIn(reg(st, "main", rows[0]))], t=0.8, hold=1.5)
        b.step(st.show("note", nt("start from the switching equation")), t=0.6, hold=1)
        b.step(step_line(st, rows, 1), t=1.2, hold=2)
        b.step(st.show("note", nt("constant effect, for now")), t=0.6, hold=1.5)
        b.step([FadeIn(reg(st, "main", rows[2]))]
               + st.show("note", nt("mean plus a random part")), t=0.8, hold=2)
        b.step(step_line(st, rows, 3), t=1.2, hold=2)
        b.step(st.show("note", nt("equation 2.3.1: regress y on the treatment dummy")),
               t=0.6, hold=2)
        b.step([Circumscribe(rows[3][0], color=FOCUS)], t=0.9, hold=1)
        b.step([FadeIn(reg(st, "main", rows[4]))], t=0.8, hold=2.5)
        b.step([FadeIn(reg(st, "main", rows[5]))]
               + st.show("note", nt("η is y₀ minus a constant")), t=0.8, hold=2.5)
        res = MathTex(r"\text{selection bias}", r"\ \Longleftrightarrow\ ",
                      r"d_i\ \text{correlated with}\ \eta_i", font_size=48)
        res[0].set_color(BIAS)
        b.step(st.show("main", res), t=0.9, hold=2)
        b.step(st.show("note", nt("the sick have low η, and the sick have d = 1", BIAS)),
               t=0.7, hold=2.5)
        b.step(st.show("note", nt("randomisation breaks the correlation → coefficient on "
                                  "d recovers ρ", EFF)), t=0.7, hold=3)
        b.step([Circumscribe(res, color=FOCUS)], t=0.9, hold=1)
        b.run()


# ==================================================================== Act VI

class B21bRecap(Scene):
    def construct(self):
        st, b = Stage(self), Beat(self, "B21bRecap")
        items = VGroup(*[Text(s, font_size=24, line_spacing=0.9) for s in (
            "1 · write y₀, y₁, d and the switching equation for any causal question",
            "2 · define and compute ATE, ATT, ATU; match each to a policy question",
            "3 · derive naive = ATT + SB = ATE + SB + (1 − π)(ATT − ATU); sign SB",
            "4 · show randomisation kills both terms; know what it does not solve")]
                       ).arrange(DOWN, aligned_edge=LEFT, buff=0.55)
        Stage.fit(items, "main")
        b.step(st.show("title", Text("What you should be able to do", font_size=30,
                                     color=GREY)), t=0.7, hold=1)
        b.step([FadeIn(reg(st, "main", items[0]))], t=0.7, hold=2.5)
        b.step([Indicate(items[0], color=FOCUS)], t=0.7, hold=0.5)
        b.step([FadeIn(reg(st, "main", items[1]))], t=0.7, hold=2.5)
        b.step([Indicate(items[1], color=FOCUS)], t=0.7, hold=0.5)
        b.step([FadeIn(reg(st, "main", items[2]))], t=0.7, hold=3)
        b.step([Indicate(items[2], color=FOCUS)], t=0.7, hold=0.5)
        b.step([FadeIn(reg(st, "main", items[3]))], t=0.7, hold=3)
        b.step([Indicate(items[3], color=FOCUS)], t=0.7, hold=0.5)
        b.step(st.show("note", nt("SUTVA · attrition · precision: not solved by the coin")),
               t=0.7, hold=1.5)
        b.step(st.show("note", nt("shaky? rewatch the derivation that goes with it",
                                  FOCUS)), t=0.7, hold=2)
        b.step([Circumscribe(items, color=GREY)], t=0.9, hold=1)
        b.run()


class B22Closing(Scene):
    def construct(self):
        st, b = Stage(self), Beat(self, "B22Closing")
        g = po_table(rh=0.38, fs=18)
        grey_now(unseen(g, D_SELF))
        f = MathTex(r"\text{observed gap}", "=", r"\text{ATT}", "+",
                    r"\text{selection bias}", font_size=40)
        f[2].set_color(EFF)
        f[4].set_color(BIAS)
        pic = VGroup(g, f).arrange(DOWN, buff=0.35)
        Stage.fit(pic, "main")
        coin = Circle(radius=0.28, color=GOLD, fill_color=GOLD, fill_opacity=0.6).next_to(
            f[4], RIGHT, buff=0.25)
        strike = Line(f[4].get_left(), f[4].get_right(), color=GOLD, stroke_width=6)
        b.step(st.show("title", Text("The picture to keep", font_size=30, color=GREY)),
               t=0.7, hold=1)
        b.step([FadeIn(reg(st, "main", g))], t=0.8, hold=2)
        b.step([Indicate(VGroup(*unseen(g, D_SELF)), color=GREY)], t=0.8, hold=1)
        b.step(st.show("note", nt("every causal effect compares two worlds; each person "
                                  "lives in one")), t=0.7, hold=2.5)
        b.step([Write(reg(st, "main", f))], t=1.0, hold=2)
        b.step([Indicate(f[2], color=EFF)], t=0.7, hold=1)
        b.step([Indicate(f[4], color=BIAS)], t=0.7, hold=1)
        b.step([FadeIn(reg(st, "main", coin), shift=DOWN * 0.3)], t=0.8, hold=1)
        b.step([Create(reg(st, "main", strike))], t=0.8, hold=1.5)
        b.step(st.show("note", nt("assigned by chance, not by choice: the gap tells the "
                                  "truth", EFF)), t=0.7, hold=2.5)
        b.step(st.show("note", nt("next class: no coin. Can controls stand in for one?",
                                  FOCUS)), t=0.7, hold=2)
        b.step([Circumscribe(pic, color=GREY)], t=0.9, hold=3)
        b.run()
