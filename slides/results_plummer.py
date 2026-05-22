from manim import *
from manim_slides import Slide


class PlummerScenario(Slide):
    def construct(self):
        heading = Text(
            "The Plummer sphere — primary initial condition",
            font_size=34,
            weight=BOLD,
        ).to_edge(UP, buff=0.6)
        self.play(Write(heading))
        self.next_slide()

        plummer_visual = (
            ImageMobject("assets/plummer.png")
            .scale_to_fit_height(5.0)
            .move_to(DOWN * 0.3)
        )
        self.play(FadeIn(plummer_visual))
        self.next_slide()

        caption = Text(
            "Spherically symmetric  ·  analytic equilibrium  ·  N ∈ {100 … 100 K}",
            font_size=20,
            color=GREY_A,
            slant=ITALIC,
        ).to_edge(DOWN, buff=0.5)
        self.play(FadeIn(caption, shift=UP * 0.15))
        self.next_slide()
