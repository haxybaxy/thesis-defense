from manim import *
from manim_slides import Slide


class ExperimentalSetup(Slide):
    def construct(self):
        heading = Text(
            "Experimental setup",
            font_size=42,
            weight=BOLD,
        ).to_edge(UP, buff=0.6)
        self.play(Write(heading))
        self.next_slide()

        quadrants = [
            (
                "Hardware",
                ["Apple M2", "8-core GPU", "16 GB unified", "macOS 26.2"],
                BLUE_B,
            ),
            (
                "Software",
                ["Apple Clang 17  -O3", "wgpu-native + Dawn", "Chrome 146", "Safari 26.2"],
                YELLOW_B,
            ),
            (
                "Initial conditions",
                ["Plummer sphere", "Rotating disk", "Two-body (validation)", "N ∈ {100, …, 100 K}"],
                GREEN_B,
            ),
            (
                "Protocol",
                ["50 warm-up steps (dropped)", "100 measured steps", "Mean ± SD, 95% CI", "CV > 10% flagged"],
                PURPLE_B,
            ),
        ]

        cards = VGroup()
        for title, items, color in quadrants:
            title_t = Text(title, font_size=22, weight=BOLD, color=color)
            body = VGroup(*[Text(f"·  {i}", font_size=18) for i in items]).arrange(
                DOWN, aligned_edge=LEFT, buff=0.18
            )
            content = VGroup(title_t, body).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
            box = SurroundingRectangle(
                content, color=color, buff=0.3, corner_radius=0.1, stroke_width=2
            )
            cards.add(VGroup(box, content))

        # 2x2 grid
        top_row = VGroup(cards[0], cards[1]).arrange(RIGHT, buff=0.5)
        bot_row = VGroup(cards[2], cards[3]).arrange(RIGHT, buff=0.5)
        grid = VGroup(top_row, bot_row).arrange(DOWN, buff=0.4)
        grid.next_to(heading, DOWN, buff=0.5)
        if grid.height > 5.6:
            grid.scale(5.6 / grid.height)

        for card in cards:
            self.play(FadeIn(card, shift=UP * 0.15), run_time=0.4)
        self.next_slide()
