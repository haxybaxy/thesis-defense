#!/usr/bin/env python3
"""WebGPU vs native Metal figure for thesis defense slides.

Compares wgpu-native against the UniSim Metal Barnes-Hut baseline.
Shows 2x overhead at N=1K becoming 2.9x advantage at N=100K -- the
WebGPU abstraction is not a bottleneck once GPU compute dominates.

Data from capstone paper, sections/results.typ tab:metal-comparison.
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

OUT = Path(__file__).resolve().parent.parent / "assets" / "fig_metal_comparison.png"

N      = np.array([1_000,  5_000,  10_000, 50_000,  100_000])
metal  = np.array([2.94,   10.09,  21.35,  121.77,  516.78])
webgpu = np.array([5.86,   7.35,   11.00,  65.46,   180.11])

METAL_COLOR  = "#6b7280"  # neutral grey (baseline)
WEBGPU_COLOR = "#16a34a"  # GREEN_B (matches the RQ2 backends slide)
FAST_COLOR   = "#16a34a"

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

# Shade the region where WebGPU is faster (N >= 5000, all but the first point)
ax.fill_between(N[1:], webgpu[1:], metal[1:],
                color=FAST_COLOR, alpha=0.12,
                label="WebGPU faster")

ax.loglog(N, metal,  "s-", color=METAL_COLOR,  ms=9, lw=2.4,
          label="Metal (UniSim)")
ax.loglog(N, webgpu, "o-", color=WEBGPU_COLOR, ms=9, lw=2.4,
          label="WebGPU (wgpu-native)")

# Ratio callouts: 2.0x slower at N=1K, 2.9x faster at N=100K
ax.annotate(
    "$2.0\\times$ slower",
    xy=(N[0], webgpu[0]), xytext=(N[0] * 1.5, 1.6),
    fontsize=12, color="#374151", fontweight="bold",
    ha="left",
    arrowprops=dict(arrowstyle="->", color="#6b7280",
                    connectionstyle="arc3,rad=-0.25", lw=1.2),
)
ax.annotate(
    "$2.9\\times$ faster",
    xy=(N[-1], webgpu[-1]), xytext=(N[-2] * 0.5, 16),
    fontsize=12, color="#16a34a", fontweight="bold",
    ha="left",
    arrowprops=dict(arrowstyle="->", color="#16a34a",
                    connectionstyle="arc3,rad=-0.2", lw=1.2),
)

# Crossover vertical line — between N=1K (WebGPU slower) and N=5K (WebGPU faster)
cross_x = np.sqrt(1_000 * 5_000)  # geometric mean ~2236
ax.axvline(cross_x, color="#6b7280", ls=":", lw=1.4, alpha=0.7)
ax.text(cross_x * 1.05, 1.2, "crossover", color="#6b7280",
        fontsize=11, fontstyle="italic", ha="left", va="bottom")

ax.set_xlabel(r"$N$ (particles)")
ax.set_ylabel("ms / step")
ax.legend(loc="upper left", frameon=True, framealpha=0.95)
ax.set_xlim(N[0] * 0.55, N[-1] * 1.4)
ax.set_ylim(1.0, 900)

fig.tight_layout()
OUT.parent.mkdir(parents=True, exist_ok=True)
fig.savefig(OUT)
plt.close(fig)
print(f"wrote {OUT}")
