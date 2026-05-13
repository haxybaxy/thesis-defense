from manim import *
from manim_slides import Slide


class FutureWork(Slide):
    def construct(self):
        heading = Text(
            "Future work",
            font_size=42,
            weight=BOLD,
        ).to_edge(UP, buff=0.6)
        self.play(Write(heading))
        self.next_slide()

        items = [
            ("Adaptive per-particle timesteps", "Dense cores → small Δt; diffuse halos → large Δt"),
            ("Cross-hardware benchmarking", "NVIDIA / Vulkan · Intel Arc · Firefox · mobile GPUs"),
            ("Quadrupole moments", "3×3 symmetric tensor per node; wider θ at same accuracy"),
            ("64-bit precision", "Once WebGPU exposes f64 in compute shaders"),
            ("Multi-component galaxy models", "Bulge + disk + dark-matter halo"),
        ]

        rows = VGroup()
        for i, (headline, sub) in enumerate(items, start=1):
            num = Text(f"{i}.", font_size=26, weight=BOLD, color=BLUE_B)
            h_t = Text(headline, font_size=22, weight=BOLD)
            s_t = Text(sub, font_size=17, color=GREY_B)
            text = VGroup(h_t, s_t).arrange(DOWN, aligned_edge=LEFT, buff=0.06)
            row = VGroup(num, text).arrange(RIGHT, aligned_edge=UP, buff=0.3)
            rows.add(row)

        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.35).next_to(heading, DOWN, buff=0.7)
        if rows.height > 5.5:
            rows.scale(5.5 / rows.height)

        for r in rows:
            self.play(FadeIn(r, shift=RIGHT * 0.2), run_time=0.35)
            self.next_slide()
