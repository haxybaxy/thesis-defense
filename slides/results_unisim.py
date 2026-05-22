from manim import *
from manim_slides import Slide

from _text import CleanText


class UniSimBaseline(Slide):
    def construct(self):
        heading = CleanText(
            "The native Metal baseline — UniSim",
            font_size=36,
            weight=BOLD,
        ).to_edge(UP, buff=0.6)

        citation_text = CleanText(
            "UniSim",
            font_size=18,
            color=GREY_B,
            slant=ITALIC,
        )
        citation_box = SurroundingRectangle(
            citation_text,
            color=GREY_B,
            buff=0.12,
            corner_radius=0.06,
            stroke_width=1.2,
        ).set_fill(BLACK, opacity=0.35)
        citation = VGroup(citation_box, citation_text).to_corner(DL, buff=0.35)

        unisim_img = ImageMobject("assets/unisim.png").scale_to_fit_height(5.0)
        unisim_img.move_to(DOWN * 0.2)

        caption = CleanText(
            "Native Metal Barnes–Hut · no abstraction layer",
            font_size=22,
            color=GREY_A,
            slant=ITALIC,
        ).to_edge(DOWN, buff=0.5)

        self.add(heading, citation, unisim_img, caption)
        self.wait(0.1)
        self.next_slide()
