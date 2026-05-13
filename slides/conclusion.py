from manim import *
from manim_slides import Slide


class Conclusion(Slide):
    def construct(self):
        heading = Text(
            "Conclusion",
            font_size=46,
            weight=BOLD,
        ).to_edge(UP, buff=0.6)
        self.play(Write(heading))
        self.next_slide()

        rqs = [
            ("RQ1", "Force evaluation dominates · optimise traversal.", BLUE_B),
            ("RQ2", "Faster than native Metal at N ≥ 5 K · bounded overhead.", YELLOW_B),
            ("RQ3", "1.4× browser overhead at large N · viable today.", GREEN_B),
        ]

        rq_lines = VGroup()
        for tag, body, color in rqs:
            tag_t = Text(tag, font_size=26, weight=BOLD, color=color)
            body_t = Text(body, font_size=22)
            row = VGroup(tag_t, body_t).arrange(RIGHT, buff=0.4, aligned_edge=DOWN)
            rq_lines.add(row)

        rq_lines.arrange(DOWN, aligned_edge=LEFT, buff=0.45).next_to(heading, DOWN, buff=0.8)

        for r in rq_lines:
            self.play(FadeIn(r, shift=UP * 0.15), run_time=0.5)
            self.next_slide()

        # bottom line
        bottom_line = Text(
            "WebGPU is good enough for interactive galactic dynamics —\n"
            "no specialised hardware, no vendor lock-in.",
            font_size=22,
            slant=ITALIC,
            color=ORANGE,
        )
        bottom_box = SurroundingRectangle(
            bottom_line, color=ORANGE, buff=0.3, corner_radius=0.1, stroke_width=2
        )
        bottom = VGroup(bottom_box, bottom_line).next_to(rq_lines, DOWN, buff=0.6)
        self.play(FadeIn(bottom, shift=UP * 0.2))
        self.next_slide()

        # thank-you
        thanks = Text("Thank you.", font_size=32, weight=BOLD).to_edge(DOWN, buff=0.7)
        questions = Text("Questions?", font_size=24, slant=ITALIC, color=GREY_B).to_edge(
            DOWN, buff=0.3
        )
        self.play(Write(thanks))
        self.play(FadeIn(questions))
        self.next_slide()
