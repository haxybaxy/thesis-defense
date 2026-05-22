from manim import *
from manim_slides import Slide

from _text import CleanText


class DemoPhone(Slide):
    def construct(self):
        heading = CleanText(
            "Runs on a phone!",
            font_size=34,
            weight=BOLD,
        ).to_edge(UP, buff=0.5)

        phone = (
            ImageMobject("assets/phonesim.jpeg")
            .scale_to_fit_height(4.2)
            .move_to(UP * 0.3)
        )

        qrcode = (
            ImageMobject("assets/qrcode.png")
            .scale_to_fit_height(3.0)
            .next_to(phone, RIGHT, buff=0.8)
        )

        self.add(heading, phone, qrcode)
        self.wait(0.1)
        self.next_slide()
