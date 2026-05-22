import math
import random

from manim import *
from manim_slides import Slide

from _text import CleanText


class AllPairsForces(Slide):
    def construct(self):
        random.seed(42)

        heading = CleanText(
            "Every particle interacts with every other",
            font_size=32,
            weight=BOLD,
        ).to_edge(UP, buff=0.6)
        self.add(heading)

        N = 12
        positions = []
        for _ in range(N):
            r = random.uniform(0.4, 2.4)
            theta = random.uniform(0, 2 * math.pi)
            positions.append([r * math.cos(theta), r * math.sin(theta) - 0.2, 0])

        particles = VGroup(*[Dot(p, radius=0.10, color=BLUE_C) for p in positions])
        self.play(
            LaggedStart(*[FadeIn(d, scale=0.5) for d in particles], lag_ratio=0.05),
            run_time=1.2,
        )
        self.next_slide()

        lines = VGroup()
        for a in range(N):
            for b in range(a + 1, N):
                line = Line(
                    particles[a].get_center(),
                    particles[b].get_center(),
                    stroke_width=1.0,
                    color=YELLOW_E,
                ).set_opacity(0.45)
                lines.add(line)
        self.play(Create(lines, lag_ratio=0.005), run_time=2.5)
        self.next_slide()

        count_label = MathTex(
            rf"\binom{{{N}}}{{2}} = \frac{{{N} \cdot {N - 1}}}{{2}} = {N * (N - 1) // 2} \text{{ interactions}}",
            font_size=36,
        ).to_edge(DOWN, buff=0.8)
        self.play(Write(count_label))
        self.next_slide()

        general_label = MathTex(
            r"\binom{N}{2} = \frac{N(N-1)}{2} \;\sim\; \mathcal{O}(N^2)",
            font_size=44,
            color=RED,
        ).to_edge(DOWN, buff=0.8)
        self.play(Transform(count_label, general_label))
        self.next_slide()
