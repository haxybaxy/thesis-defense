from manim import *
from manim_slides import Slide

from _text import CleanText


class ExperimentalSetup(Slide):
    def construct(self):
        heading = CleanText(
            "Experimental setup",
            font_size=40,
            weight=BOLD,
        ).to_edge(UP, buff=0.5)

        maczan_citation_text = CleanText(
            "Maczan, 2026",
            font_size=16,
            color=GREY_B,
            slant=ITALIC,
        )
        maczan_citation_box = SurroundingRectangle(
            maczan_citation_text,
            color=GREY_B,
            buff=0.12,
            corner_radius=0.06,
            stroke_width=1.2,
        ).set_fill(BLACK, opacity=0.35)
        maczan_citation = VGroup(
            maczan_citation_box, maczan_citation_text
        ).to_corner(DL, buff=0.3)

        plummer_visual = ImageMobject("assets/plummer.png").scale_to_fit_height(3.8)
        plummer_label = CleanText(
            "Plummer sphere — primary IC",
            font_size=16,
            color=GREY_A,
            slant=ITALIC,
        )
        plummer_group = Group(plummer_visual, plummer_label).arrange(DOWN, buff=0.2)

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
            title_t = CleanText(title, font_size=18, weight=BOLD, color=color)
            body = VGroup(*[CleanText(f"·  {i}", font_size=13) for i in items]).arrange(
                DOWN, aligned_edge=LEFT, buff=0.1
            )
            content = VGroup(title_t, body).arrange(DOWN, aligned_edge=LEFT, buff=0.16)
            box = SurroundingRectangle(
                content, color=color, buff=0.22, corner_radius=0.08, stroke_width=2
            )
            cards.add(VGroup(box, content))

        top_row = VGroup(cards[0], cards[1]).arrange(RIGHT, buff=0.3)
        bot_row = VGroup(cards[2], cards[3]).arrange(RIGHT, buff=0.3)
        grid = VGroup(top_row, bot_row).arrange(DOWN, buff=0.25)

        layout = Group(plummer_group, grid).arrange(RIGHT, buff=0.7)
        layout.next_to(heading, DOWN, buff=0.35)

        max_h = 5.7
        if layout.height > max_h:
            layout.scale(max_h / layout.height)
        max_w = 12.5
        if layout.width > max_w:
            layout.scale(max_w / layout.width)

        self.add(heading, maczan_citation, layout)
        self.wait(0.1)
        self.next_slide()
