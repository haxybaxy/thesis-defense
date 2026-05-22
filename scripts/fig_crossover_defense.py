#!/usr/bin/env python3
"""Direct vs Tree crossover figure for thesis defense slides.

Two-panel stacked plot: runtime (top) and energy drift (bottom) vs N.
Highlights that the real crossover is in accuracy, not runtime.

Data from capstone paper, sections/results.typ tab:crossover.
Colors match the slide cards in slides/results_rq1b.py
(blue for Direct, green for Tree).
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

OUT = Path(__file__).resolve().parent.parent / "assets" / "fig_crossover.png"

# Data — from sections/results.typ tab:crossover
N         = np.array([1_000,    5_000,    10_000,   50_000,   100_000])
direct_ms = np.array([1.53,     4.03,     7.46,     35.64,    140.37])
tree_ms   = np.array([5.86,     7.35,     11.00,    65.46,    180.11])
direct_de = np.array([2.25e-2,  1.21e-1,  2.11e-1,  9.88e-1,  2.01])
tree_de   = np.array([6.41e-5,  2.50e-4,  8.65e-3,  6.07e-2,  7.58e-2])

DIRECT_COLOR = "#1d4ed8"  # blue (matches BLUE_B card in slide)
TREE_COLOR   = "#16a34a"  # green (matches GREEN_B card in slide)
THRESH_COLOR = "#dc2626"  # red

plt.rcParams.update({
    "font.family": "serif",
    "font.serif": ["CMU Serif", "DejaVu Serif", "Times New Roman"],
    "font.size": 14,
    "axes.labelsize": 16,
    "axes.titlesize": 16,
    "legend.fontsize": 13,
    "xtick.labelsize": 12,
    "ytick.labelsize": 12,
    "figure.facecolor": "white",
    "axes.facecolor": "white",
    "savefig.facecolor": "white",
    "savefig.dpi": 300,
    "axes.grid": True,
    "grid.alpha": 0.3,
    "grid.linestyle": "--",
})

fig, (ax_t, ax_d) = plt.subplots(
    2, 1, figsize=(8, 7), sharex=True,
    gridspec_kw={"hspace": 0.08},
)

# ── Top: runtime ────────────────────────────────────────────────────
ax_t.loglog(N, direct_ms, "s-", color=DIRECT_COLOR, ms=9, lw=2.4,
            label=r"Direct  $O(N^2)$")
ax_t.loglog(N, tree_ms,   "o-", color=TREE_COLOR,   ms=9, lw=2.4,
            label=r"Tree  $O(N \log N)$")

ax_t.set_ylabel("ms / step")
ax_t.legend(loc="upper left", frameon=True, framealpha=0.95)
ax_t.set_ylim(0.8, 400)

# Annotate the closing gap at N=100K — sets up the bottom-panel story
ax_t.annotate(
    "runtime gap narrows\n($3.8\\times \\to 1.3\\times$)",
    xy=(N[-1], direct_ms[-1] * 0.85), xytext=(N[1] * 1.4, 1.6),
    fontsize=12, color="#374151",
    ha="left", va="center",
    arrowprops=dict(arrowstyle="->", color="#6b7280",
                    connectionstyle="arc3,rad=-0.3", lw=1.2),
)

# ── Bottom: energy drift ────────────────────────────────────────────
ax_d.loglog(N, direct_de, "s-", color=DIRECT_COLOR, ms=9, lw=2.4)
ax_d.loglog(N, tree_de,   "o-", color=TREE_COLOR,   ms=9, lw=2.4)

# Acceptability threshold
THRESHOLD = 1e-2
ax_d.axhline(THRESHOLD, color=THRESH_COLOR, lw=1.8, ls="--", alpha=0.85)
ax_d.text(N[0] * 0.85, THRESHOLD, "1% drift",
          color=THRESH_COLOR, fontsize=12, va="center", ha="left",
          fontweight="bold",
          bbox=dict(facecolor="white", edgecolor="none", pad=2, alpha=0.95))

# Headline callout: the 26× accuracy gap at N=100K.
# Double-headed vertical arrow between the two N=100K points.
gap_x = N[-1] * 1.18
ax_d.annotate(
    "", xy=(gap_x, direct_de[-1]), xytext=(gap_x, tree_de[-1]),
    arrowprops=dict(arrowstyle="<->", color="#374151", lw=1.6),
)
gap_mid = np.sqrt(direct_de[-1] * tree_de[-1])  # geometric mean on log axis
ax_d.text(gap_x * 1.04, gap_mid, "$26\\times$",
          fontsize=14, color="#374151", fontweight="bold",
          va="center", ha="left")

ax_d.set_xlabel(r"$N$ (particles)")
ax_d.set_ylabel(r"$|\Delta E / E_0|$")
ax_d.set_ylim(2e-5, 8)
ax_d.set_xlim(N[0] * 0.7, N[-1] * 1.6)
ax_t.set_xlim(N[0] * 0.7, N[-1] * 1.6)

fig.tight_layout()
OUT.parent.mkdir(parents=True, exist_ok=True)
fig.savefig(OUT)
plt.close(fig)
print(f"wrote {OUT}")
