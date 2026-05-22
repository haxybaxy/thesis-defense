from manim import *
from manim_slides import Slide

from _text import CleanText


class WebGPUvsMetal(Slide):
    def construct(self):
        heading = CleanText(
            "RQ2: WebGPU vs native Metal",
            font_size=40,
            weight=BOLD,
        ).to_edge(UP, buff=0.6)
        self.add(heading)

        chart = (
            ImageMobject("assets/fig_metal_comparison.png")
            .scale_to_fit_height(5.2)
            .next_to(heading, DOWN, buff=0.35)
        )
        self.add(chart)

        self.wait(0.1)
        self.next_slide()
