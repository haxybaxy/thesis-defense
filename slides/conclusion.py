from manim import *
from manim_slides import Slide

from _text import CleanText


class Conclusion(Slide):
    def construct(self):
        heading = CleanText(
            "WebGPU is a viable compute platform",
            font_size=40,
            weight=BOLD,
        ).to_edge(UP, buff=0.55)
        self.play(Write(heading))
        self.next_slide()

        # Three short stacked findings.
        findings = [
            ("WebGPU compute is viable", BLUE_B),
            ("Abstraction overhead is bounded", YELLOW_B),
            ("GPU-resident pipelines win", GREEN_B),
        ]
        finding_rows = VGroup()
        for text, color in findings:
            t = CleanText(text, font_size=28, weight=BOLD, color=color)
            box = SurroundingRectangle(
                t,
                color=color,
                buff=0.22,
                corner_radius=0.12,
                stroke_width=2,
            ).set_fill(BLACK, opacity=0.35)
            finding_rows.add(VGroup(box, t))

        finding_rows.arrange(DOWN, buff=0.32).next_to(heading, DOWN, buff=0.7)

        for row in finding_rows:
            self.play(FadeIn(row, shift=UP * 0.15), run_time=0.45)
            self.next_slide()

        # Practical contribution line.
        contribution = CleanText(
            "A real N-body simulation. Deployable as a URL. Runnable on a phone.",
            font_size=22,
            slant=ITALIC,
            color=ORANGE,
        )
        contribution_box = SurroundingRectangle(
            contribution,
            color=ORANGE,
            buff=0.25,
            corner_radius=0.1,
            stroke_width=2,
        )
        contribution_group = VGroup(contribution_box, contribution).next_to(
            finding_rows, DOWN, buff=0.55
        )
        self.play(FadeIn(contribution_group, shift=UP * 0.15))
        self.next_slide()

        # Thank-you beat.
        thanks = CleanText("Thank you.", font_size=34, weight=BOLD).to_edge(DOWN, buff=0.85)
        questions = CleanText(
            "Questions?", font_size=22, slant=ITALIC, color=GREY_B
        ).next_to(thanks, DOWN, buff=0.15)
        self.play(Write(thanks))
        self.play(FadeIn(questions))
        self.next_slide()
