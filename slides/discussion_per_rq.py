from manim import *
from manim_slides import Slide


class PerRQDiscussion(Slide):
    def construct(self):
        heading = Text(
            "What the results mean",
            font_size=42,
            weight=BOLD,
        ).to_edge(UP, buff=0.6)
        self.play(Write(heading))
        self.next_slide()

        rqs = [
            (
                "RQ1",
                "Bottlenecks",
                "Force evaluation = 94–99% of step time.\nOptimise traversal. Ignore the tree build.",
                BLUE_B,
            ),
            (
                "RQ2",
                "Abstraction overhead",
                "2× slower at N=1K  →  2.9× FASTER at N=100K.\nBackend variation alone is 1.5×.",
                YELLOW_B,
            ),
            (
                "RQ3",
                "Browser feasibility",
                "1.4× overhead at scientifically meaningful N.\nGap narrows as N grows.",
                GREEN_B,
            ),
        ]

        boxes = VGroup()
        for tag, title, body, color in rqs:
            tag_t = Text(tag, font_size=30, weight=BOLD, color=color)
            title_t = Text(title, font_size=24, weight=BOLD)
            body_t = Text(body, font_size=20, color=GREY_B)
            header = VGroup(tag_t, title_t).arrange(RIGHT, buff=0.4, aligned_edge=DOWN)
            content = VGroup(header, body_t).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
            box = SurroundingRectangle(
                content, color=color, buff=0.3, corner_radius=0.1, stroke_width=2.5
            )
            boxes.add(VGroup(box, content))

        boxes.arrange(DOWN, buff=0.35).next_to(heading, DOWN, buff=0.5)
        if boxes.height > 5.4:
            boxes.scale(5.4 / boxes.height)

        for b in boxes:
            self.play(FadeIn(b, shift=UP * 0.15), run_time=0.5)
            self.next_slide()
