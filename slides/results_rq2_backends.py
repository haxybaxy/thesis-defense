from manim import *
from manim_slides import Slide

from _text import CleanText


class CrossBackendVariation(Slide):
    def construct(self):
        heading = CleanText(
            "RQ2: Cross-backend variation",
            font_size=40,
            weight=BOLD,
        ).to_edge(UP, buff=0.6)
        self.add(heading)

        maczan_citation_text = CleanText(
            "Maczan, 2026",
            font_size=18,
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
        maczan_citation = VGroup(maczan_citation_box, maczan_citation_text).to_corner(
            DL, buff=0.35
        )
        self.add(maczan_citation)

        subhead = CleanText(
            "Four WebGPU implementations · same Metal backend · frozen-state protocol",
            font_size=18,
            slant=ITALIC,
            color=GREY_B,
        ).next_to(heading, DOWN, buff=0.3)
        self.add(subhead)

        chart = (
            ImageMobject("assets/fig_cross_backend.png")
            .scale_to_fit_height(5.2)
            .next_to(subhead, DOWN, buff=0.35)
        )
        self.add(chart)

        self.wait(0.1)
        self.next_slide()
