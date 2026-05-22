from manim import *
from manim_slides import Slide

from _text import CleanText


class DirectVsTree(Slide):
    def construct(self):
        heading = CleanText(
            "RQ1: Direct vs Tree — the real crossover",
            font_size=36,
            weight=BOLD,
        ).to_edge(UP, buff=0.6)
        self.add(heading)
        self.wait(0.1)
        self.next_slide()

        crossover_img = ImageMobject(
            "assets/fig_crossover.png"
        ).scale_to_fit_height(5.4)
        crossover_img.move_to(DOWN * 0.2)
        self.add(crossover_img)
        self.wait(0.1)
        self.next_slide()

        tag = CleanText(
            "The crossover is accuracy, not runtime.",
            font_size=22,
            slant=ITALIC,
            color=YELLOW_B,
        ).to_edge(DOWN, buff=0.35)
        self.add(tag)
        self.wait(0.1)
        self.next_slide()
