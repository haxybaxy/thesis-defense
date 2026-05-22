from manim import *
from manim_slides import Slide

from _text import CleanText


class TitleSlide(Slide):
    def construct(self):
        title = VGroup(
            CleanText("Hierarchical N-Body Simulation of", font_size=42, weight=BOLD),
            CleanText("Galactic Dynamics in WebGPU", font_size=42, weight=BOLD),
        ).arrange(DOWN, buff=0.15)

        subtitle = VGroup(
            CleanText("Enabling Scalable and Interactive Physics Simulations", font_size=24, slant=ITALIC),
            CleanText("on Modern Web Platforms", font_size=24, slant=ITALIC),
        ).arrange(DOWN, buff=0.1)

        author = CleanText("Zaid Alsaheb", font_size=32)
        advisor = CleanText("Advisor: Prof. Raul Pérez Peláez", font_size=24)

        group = VGroup(title, subtitle, author, advisor).arrange(DOWN, buff=0.4)
        group[2].shift(DOWN * 0.5)
        group[3].next_to(group[2], DOWN, buff=0.3)
        group.move_to(ORIGIN)

        self.add(group)
        self.wait(0.1)
        self.next_slide()
