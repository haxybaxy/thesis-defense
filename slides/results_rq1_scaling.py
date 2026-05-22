from manim import *
from manim_slides import Slide

from _text import CleanText


class NScaling(Slide):
    def construct(self):
        heading = CleanText(
            "RQ1: Step time vs particle count",
            font_size=38,
            weight=BOLD,
        ).to_edge(UP, buff=0.6)
        self.add(heading)
        self.wait(0.1)

        scaling_img = ImageMobject(
            "assets/fig_n_scaling_plummer.png"
        ).scale_to_fit_height(5.2)
        scaling_img.move_to(DOWN * 0.2)
        self.add(scaling_img)

        self.wait(0.1)
        self.next_slide()
