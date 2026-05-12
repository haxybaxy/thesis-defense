from manim import *
from manim_slides import Slide


class TitleSlide(Slide):
    def construct(self):
        title = Text(
            "Hierarchical N-Body Simulation of\nGalactic Dynamics in WebGPU",
            font_size=42,
            weight=BOLD,
        )
        subtitle = Text(
            "Enabling Scalable and Interactive Physics Simulations\non Modern Web Platforms",
            font_size=24,
            slant=ITALIC,
        )
        author = Text("Zaid Alsaheb", font_size=32)
        advisor = Text("Advisor: Prof. Raul Pérez Peláez", font_size=24)

        title.to_edge(UP, buff=1.2)
        subtitle.next_to(title, DOWN, buff=0.4)
        author.next_to(subtitle, DOWN, buff=1.0)
        advisor.next_to(author, DOWN, buff=0.3)

        self.play(Write(title))
        self.play(FadeIn(subtitle, shift=UP * 0.3))
        self.next_slide()

        self.play(
            FadeIn(author, shift=UP * 0.2),
            FadeIn(advisor, shift=UP * 0.2),
            lag_ratio=0.2,
        )
        self.next_slide()
