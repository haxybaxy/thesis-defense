from manim import *
from manim_slides import Slide

from _text import CleanText


class BroaderImpact(Slide):
    def construct(self):
        heading = CleanText(
            "Broader impact",
            font_size=42,
            weight=BOLD,
        ).to_edge(UP, buff=0.6)

        items = [
            (
                "Access economics for scientific software",
                "\"Send a link\" delivery now viable — 1.4× native at 100K bodies",
                "replaces cross-OS native builds and per-user cloud GPU rentals",
            ),
            (
                "Cloud-to-client compute offloading",
                "SaaS GPU bills scale per user; client compute turns variable cost fixed",
                "2× ceiling at small N, 1.4× at large N quantifies the tradeoff",
            ),
            (
                "De-risking WebGPU adoption",
                "Non-trivial scientific workload — not a toy demo",
                "cross-backend data (Dawn · wgpu · Chrome · Safari) for build-vs-buy",
            ),
            (
                "Transferable methodology",
                "Same-kernel native-vs-browser benchmarking framework",
                "portable to MD, agent-based finance, FEA/CFD, game engines",
            ),
        ]

        rows = VGroup()
        for i, (headline, sub1, sub2) in enumerate(items, start=1):
            num = CleanText(f"{i}.", font_size=26, weight=BOLD, color=BLUE_B)
            h_t = CleanText(headline, font_size=22, weight=BOLD)
            s1_t = CleanText(sub1, font_size=17, color=GREY_B)
            s2_t = CleanText(sub2, font_size=17, color=GREY_B)
            text = VGroup(h_t, s1_t, s2_t).arrange(DOWN, aligned_edge=LEFT, buff=0.06)
            row = VGroup(num, text).arrange(RIGHT, aligned_edge=UP, buff=0.3)
            rows.add(row)

        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.35).next_to(heading, DOWN, buff=0.6)
        if rows.height > 5.5:
            rows.scale(5.5 / rows.height)

        self.add(heading, rows)
        self.wait(0.1)
        self.next_slide()
