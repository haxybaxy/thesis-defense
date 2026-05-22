from manim import *
from manim_slides import Slide

from _text import CleanText


class IntegratorConcept(Slide):
    def construct(self):
        box = RoundedRectangle(
            width=2.6,
            height=1.1,
            corner_radius=0.18,
            color=BLUE_B,
            stroke_width=3,
        ).set_fill(BLUE_B, opacity=0.22)
        label = CleanText(
            "Integrator",
            font_size=24,
            weight=BOLD,
            color=BLUE_B,
        ).move_to(box.get_center())
        integrator = VGroup(box, label).move_to(UP * 0.6)
        self.add(integrator)
        continuous = CleanText(
            "Continuous time system",
            font_size=28,
            color=GRAY_A,
        )
        arrow = CleanText("→", font_size=32, color=GRAY_A)
        discrete = CleanText(
            "Discrete time approximation",
            font_size=28,
            color=YELLOW_B,
            weight=BOLD,
        )
        caption = VGroup(continuous, arrow, discrete).arrange(RIGHT, buff=0.35)
        caption.next_to(integrator, DOWN, buff=0.9)
        self.add(continuous)
        self.add(arrow)
        self.add(discrete)
        self.wait(0.1)
        self.next_slide()
