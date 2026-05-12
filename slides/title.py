from manim import *
from manim_slides import Slide


class TitleSlide(Slide):
    def construct(self):
        title = Text("Thesis Title Goes Here", font_size=48, weight=BOLD)
        subtitle = Text("A short, descriptive subtitle", font_size=28, slant=ITALIC)
        author = Text("Your Name", font_size=32)
        advisor = Text("Advisor: Prof. Advisor Name", font_size=24)
        date = Text("Defense Date", font_size=24)

        title.to_edge(UP, buff=1.2)
        subtitle.next_to(title, DOWN, buff=0.4)
        author.next_to(subtitle, DOWN, buff=1.0)
        advisor.next_to(author, DOWN, buff=0.3)
        date.next_to(advisor, DOWN, buff=0.3)

        self.play(Write(title))
        self.play(FadeIn(subtitle, shift=UP * 0.3))
        self.next_slide()

        self.play(
            FadeIn(author, shift=UP * 0.2),
            FadeIn(advisor, shift=UP * 0.2),
            FadeIn(date, shift=UP * 0.2),
            lag_ratio=0.2,
        )
        self.next_slide()
