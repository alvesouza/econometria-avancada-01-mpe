"""Shared matplotlib look for every figure under Notas/<unit>/figures/.

Each unit's ``figures/make_figures.py`` does::

    import sys, pathlib
    sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))
    from _figstyle import C, apply, save

and then ``save(fig, "L01-poisson-pmf")`` writes ``<unit>/figures/L01-poisson-pmf.png``
next to the calling script. ``apply()`` must run before the first figure.
"""
import inspect
import pathlib

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

# Colour roles (same five roles the Manim kit uses): the object of attention,
# the thing that breaks, the result that survives, a neutral reference, a highlight.
C = {
    "main": "#1f5f8b",
    "warn": "#b4521a",
    "good": "#2f6b4f",
    "ref": "#6b7a88",
    "hi": "#8a5fb4",
    "ink": "#14202c",
    "grid": "#dfe5ea",
}
CYCLE = [C["main"], C["warn"], C["good"], C["hi"], C["ref"], "#c49a1c"]


def apply():
    """Set the shared rcParams. Call once, before building any figure."""
    plt.rcParams.update({
        "figure.figsize": (7.2, 4.2),
        "figure.dpi": 110,
        "savefig.dpi": 150,
        "savefig.bbox": "tight",
        "font.size": 10.5,
        "axes.titlesize": 11.5,
        "axes.titleweight": "semibold",
        "axes.labelcolor": C["ink"],
        "axes.edgecolor": C["ref"],
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.grid": True,
        "grid.color": C["grid"],
        "grid.linewidth": 0.8,
        "axes.prop_cycle": plt.cycler(color=CYCLE),
        "legend.frameon": False,
        "lines.linewidth": 2.0,
        "mathtext.fontset": "cm",
    })


def save(fig, name):
    """Write ``fig`` as ``<name>.png`` beside the calling script and close it.

    name: file stem, conventionally ``<UNIT>-<slug>`` (e.g. ``L01-poisson-pmf``).
    Returns the written path.
    """
    caller = pathlib.Path(inspect.stack()[1].filename).resolve().parent
    path = caller / f"{name}.png"
    fig.savefig(path)
    plt.close(fig)
    return path
