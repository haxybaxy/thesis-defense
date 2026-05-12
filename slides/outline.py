from manim import *
from manim_slides import Slide


class Outline(Slide):
    def construct(self):
        heading = Text("Outline", font_size=44, weight=BOLD).to_edge(UP)
        self.play(Write(heading))
        self.next_slide()

        items = [
            "1. Motivation & Problem Statement",
            "2. Background & Related Work",
            "3. Approach",
            "4. Experiments & Results",
            "5. Discussion & Future Work",
        ]
        bullets = VGroup(
            *[Text(item, font_size=30) for item in items]
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.45).next_to(heading, DOWN, buff=0.8)

        for bullet in bullets:
            self.play(FadeIn(bullet, shift=RIGHT * 0.3), run_time=0.4)
            self.next_slide()

        highlight = SurroundingRectangle(bullets[2], color=YELLOW, buff=0.15)
        self.play(Create(highlight))
        self.next_slide()
