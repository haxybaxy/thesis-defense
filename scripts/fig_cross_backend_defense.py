#!/usr/bin/env python3
"""Cross-backend RQ2/Group 6 figure for thesis defense slides.

Four WebGPU implementations on the same Metal driver: Dawn, wgpu-native,
Chrome, Safari. Shows the 1.5x spread at N=100K and the scaling-slope
inversion between Dawn and wgpu-native.

Data from capstone paper, sections/results.typ tab:cross-backend.
Colors aligned to slides/results_rq2_backends.py (BLUE_C / GREEN_B / YELLOW_B / RED_B).
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

OUT = Path(__file__).resolve().parent.parent / "assets" / "fig_cross_backend.png"

N           = np.array([1_000,  10_000, 100_000])
dawn        = np.array([1.40,   8.54,   272.73])
wgpu_native = np.array([5.86,   11.00,  180.11])
chrome      = np.array([4.87,   17.81,  260.74])
safari      = np.array([9.52,   20.97,  281.59])

DAWN_COLOR    = "#3b82f6"  # BLUE_C
WGPU_COLOR    = "#16a34a"  # GREEN_B
CHROME_COLOR  = "#eab308"  # YELLOW_B (deepened)
SAFARI_COLOR  = "#ef4444"  # RED_B

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

fig, ax = plt.subplots(figsize=(8, 5.5))

ax.loglog(N, dawn,        "s-", color=DAWN_COLOR,   ms=9, lw=2.4, label="Dawn")
ax.loglog(N, wgpu_native, "o-", color=WGPU_COLOR,   ms=9, lw=2.4, label="wgpu-native")
ax.loglog(N, chrome,      "^-", color=CHROME_COLOR, ms=10, lw=2.4, label="Chrome")
ax.loglog(N, safari,      "D-", color=SAFARI_COLOR, ms=8, lw=2.4, label="Safari")

# Headline: 1.5x spread between fastest (wgpu-native) and slowest (Safari) at N=100K
gap_x = N[-1] * 1.35
ax.annotate(
    "", xy=(gap_x, safari[-1]), xytext=(gap_x, wgpu_native[-1]),
    arrowprops=dict(arrowstyle="<->", color="#374151", lw=1.6),
)
gap_mid = np.sqrt(safari[-1] * wgpu_native[-1])
ax.text(gap_x * 1.08, gap_mid, "$1.5\\times$\nspread",
        fontsize=13, color="#374151", fontweight="bold",
        va="center", ha="left")

ax.set_xlabel(r"$N$ (particles)")
ax.set_ylabel("ms / step")
ax.legend(loc="upper left", frameon=True, framealpha=0.95)
ax.set_xlim(N[0] * 0.7, N[-1] * 2.8)
ax.set_ylim(0.8, 600)

fig.tight_layout()
OUT.parent.mkdir(parents=True, exist_ok=True)
fig.savefig(OUT)
plt.close(fig)
print(f"wrote {OUT}")
