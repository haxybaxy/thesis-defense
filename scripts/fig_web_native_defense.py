#!/usr/bin/env python3
"""Browser vs native (RQ3) figure for thesis defense slides.

Top panel: raw ms/step for native wgpu-native and Chrome.
Bottom panel: overhead ratio (Chrome / native) -- highlights the
non-monotonic U-shape: 0.8x at N=1K, peaks at 2.0x at N=5K, narrows
back to 1.4x at N=100K.

Data from capstone paper, sections/results.typ tab:web-native.
Colors aligned to slides/results_rq3.py (BLUE_C / YELLOW_B).
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

OUT = Path(__file__).resolve().parent.parent / "assets" / "fig_web_native.png"

N        = np.array([1_000,  5_000,  10_000, 50_000,  100_000])
native   = np.array([5.86,   7.35,   11.00,  65.46,   180.11])
chrome   = np.array([4.87,   14.34,  17.81,  94.93,   260.74])
overhead = chrome / native  # 0.83, 1.95, 1.62, 1.45, 1.45 ish

NATIVE_COLOR = "#3b82f6"  # BLUE_C
CHROME_COLOR = "#eab308"  # YELLOW_B (deepened)
PARITY_COLOR = "#dc2626"  # red, for the 1.0x reference line

# Conditional marker colors for the overhead points (matches the slide's logic)
overhead_colors = []
for r in overhead:
    if r < 1.0 or r <= 1.45:
        overhead_colors.append("#16a34a")   # green: good (under 1.5x)
    elif r < 1.8:
        overhead_colors.append("#eab308")   # yellow: moderate
    else:
        overhead_colors.append("#ef4444")   # red: peak

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

fig, (ax_t, ax_b) = plt.subplots(
    2, 1, figsize=(8, 7), sharex=True,
    gridspec_kw={"hspace": 0.08, "height_ratios": [1.5, 1]},
)

# ── Top: ms/step ────────────────────────────────────────────────────
ax_t.loglog(N, native, "s-", color=NATIVE_COLOR, ms=9, lw=2.4,
            label="Native (wgpu-native)")
ax_t.loglog(N, chrome, "o-", color=CHROME_COLOR, ms=9, lw=2.4,
            label="Browser (Chrome + WASM)")
ax_t.set_ylabel("ms / step")
ax_t.legend(loc="upper left", frameon=True, framealpha=0.95)
ax_t.set_ylim(2, 500)

# ── Bottom: overhead ratio ──────────────────────────────────────────
ax_b.semilogx(N, overhead, "-", color="#374151", lw=1.8, zorder=1)
ax_b.scatter(N, overhead, c=overhead_colors, s=110, zorder=2,
             edgecolors="#374151", linewidths=1.2)

# Reference line at parity (1.0x — browser equals native)
ax_b.axhline(1.0, color=PARITY_COLOR, ls="--", lw=1.6, alpha=0.85)
ax_b.text(N[-1] * 1.05, 1.0, "native\nparity",
          color=PARITY_COLOR, fontsize=11, fontweight="bold",
          va="center", ha="left")

# Callout the peak at N=5K
ax_b.annotate(
    "peak  $2.0\\times$",
    xy=(N[1], overhead[1]), xytext=(N[1] * 2.2, 2.2),
    fontsize=12, color="#ef4444", fontweight="bold",
    arrowprops=dict(arrowstyle="->", color="#ef4444",
                    connectionstyle="arc3,rad=-0.2", lw=1.2),
)
# Highlight the final convergence — annotation positioned ABOVE the data point
# so it's clearly in the >parity region, not confused with the <parity area
ax_b.annotate(
    "narrows to $1.4\\times$",
    xy=(N[-1], overhead[-1] * 1.03), xytext=(N[-2] * 0.5, 2.0),
    fontsize=12, color="#16a34a", fontweight="bold",
    ha="left",
    arrowprops=dict(arrowstyle="->", color="#16a34a",
                    connectionstyle="arc3,rad=-0.25", lw=1.2),
)

ax_b.set_xlabel(r"$N$ (particles)")
ax_b.set_ylabel("Chrome / Native")
ax_b.set_ylim(0.4, 2.6)
ax_b.set_xlim(N[0] * 0.7, N[-1] * 1.6)

fig.tight_layout()
OUT.parent.mkdir(parents=True, exist_ok=True)
fig.savefig(OUT)
plt.close(fig)
print(f"wrote {OUT}")
