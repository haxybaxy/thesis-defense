from manim import *
from manim_slides import Slide

from _text import CleanText


class Limitations(Slide):
    def construct(self):
        heading = CleanText(
            "Limitations",
            font_size=42,
            weight=BOLD,
        ).to_edge(UP, buff=0.6)

        items = [
            ("Single hardware platform", "Apple M2 / Metal only"),
            ("32-bit float", "WebGPU has no f64 in compute shaders"),
            ("Monopole approximation", "GADGET-2 uses quadrupole"),
            ("UniSim baseline patched", "Tree-serialisation bug; fork used"),
            ("No WGSL subgroup ops", "Can't reduce traversal divergence"),
            ("Global fixed timestep", "Dense cores waste large Δt"),
        ]

        bullets = VGroup()
        for headline, sub in items:
            bullet = CleanText("·", font_size=28, weight=BOLD, color=ORANGE)
            h_t = CleanText(headline, font_size=22, weight=BOLD)
            s_t = CleanText(sub, font_size=18, color=GREY_B)
            text = VGroup(h_t, s_t).arrange(DOWN, aligned_edge=LEFT, buff=0.05)
            row = VGroup(bullet, text).arrange(RIGHT, aligned_edge=UP, buff=0.3)
            bullets.add(row)

        bullets.arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(heading, DOWN, buff=0.7)
        if bullets.height > 5.5:
            bullets.scale(5.5 / bullets.height)

        self.add(heading, bullets)
        self.wait(0.1)
        self.next_slide()
