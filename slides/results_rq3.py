from manim import *
from manim_slides import Slide

from _text import CleanText


class BrowserVsNative(Slide):
    def construct(self):
        heading = CleanText(
            "RQ3: Browser vs native",
            font_size=40,
            weight=BOLD,
        ).to_edge(UP, buff=0.6)
        self.add(heading)
        self.wait(0.1)
        self.next_slide()

        chart = (
            ImageMobject("assets/fig_web_native.png")
            .scale_to_fit_height(5.2)
            .next_to(heading, DOWN, buff=0.25)
        )
        self.add(chart)
        self.wait(0.1)
        self.next_slide()

        # surprise at N=1K (chart shows this only as a single sub-1.0 ratio point)
        surprise = CleanText(
            "Chrome is actually faster at N = 1 K",
            font_size=20,
            slant=ITALIC,
            color=GREEN_B,
        ).to_edge(DOWN, buff=0.4)
        self.add(surprise)
        self.wait(0.1)
        self.next_slide()
