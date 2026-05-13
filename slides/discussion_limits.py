from manim import *
from manim_slides import Slide


class Limitations(Slide):
    def construct(self):
        heading = Text(
            "Limitations",
            font_size=42,
            weight=BOLD,
        ).to_edge(UP, buff=0.6)
        self.play(Write(heading))
        self.next_slide()

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
            bullet = Text("·", font_size=28, weight=BOLD, color=ORANGE)
            h_t = Text(headline, font_size=22, weight=BOLD)
            s_t = Text(sub, font_size=18, color=GREY_B)
            text = VGroup(h_t, s_t).arrange(DOWN, aligned_edge=LEFT, buff=0.05)
            row = VGroup(bullet, text).arrange(RIGHT, aligned_edge=UP, buff=0.3)
            bullets.add(row)

        bullets.arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(heading, DOWN, buff=0.7)
        if bullets.height > 5.5:
            bullets.scale(5.5 / bullets.height)

        for b in bullets:
            self.play(FadeIn(b, shift=RIGHT * 0.2), run_time=0.35)
        self.next_slide()
