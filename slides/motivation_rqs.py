from manim import *
from manim_slides import Slide


class ResearchQuestions(Slide):
    def construct(self):
        heading = Text(
            "Three research questions",
            font_size=40,
            weight=BOLD,
        ).to_edge(UP, buff=0.6)
        self.play(Write(heading))
        self.next_slide()

        rqs = [
            (
                "RQ1",
                "Scalability & bottlenecks",
                "Where does the time go in a fully GPU-resident\nBarnes–Hut pipeline?",
                BLUE_B,
            ),
            (
                "RQ2",
                "Abstraction overhead",
                "How much does WebGPU cost relative to\nnative Metal?",
                YELLOW_B,
            ),
            (
                "RQ3",
                "Browser feasibility",
                "Is browser execution viable at scientifically\nmeaningful N?",
                GREEN_B,
            ),
        ]

        boxes = VGroup()
        for tag, title, body, color in rqs:
            tag_text = Text(tag, font_size=30, weight=BOLD, color=color)
            title_text = Text(title, font_size=26, weight=BOLD)
            body_text = Text(body, font_size=22, color=GREY_B)

            label_row = VGroup(tag_text, title_text).arrange(RIGHT, buff=0.4, aligned_edge=DOWN)
            content = VGroup(label_row, body_text).arrange(
                DOWN, aligned_edge=LEFT, buff=0.2
            )

            box = SurroundingRectangle(
                content, color=color, buff=0.3, corner_radius=0.1, stroke_width=2.5
            )
            group = VGroup(box, content)
            boxes.add(group)

        boxes.arrange(DOWN, buff=0.4).next_to(heading, DOWN, buff=0.6)

        # scale to fit if needed
        if boxes.height > 5.0:
            boxes.scale(5.0 / boxes.height)

        for group in boxes:
            self.play(FadeIn(group, shift=UP * 0.2), run_time=0.6)
            self.next_slide()
