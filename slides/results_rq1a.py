from manim import *
from manim_slides import Slide

from _text import CleanText


class WhereTimeIsSpent(Slide):
    def construct(self):
        heading = CleanText(
            "RQ1: Where does the time go?",
            font_size=40,
            weight=BOLD,
        ).to_edge(UP, buff=0.6)
        self.add(heading)

        # Big LBVH breakdown chart on the right
        breakdown_img = ImageMobject(
            "assets/fig_lbvh_breakdown.png"
        ).scale_to_fit_height(5.2)
        breakdown_img.to_edge(RIGHT, buff=1.4).shift(DOWN * 0.3)
        self.add(breakdown_img)

        # Three headline cards stacked vertically on the LEFT
        callouts = [
            ("94 – 99 %", "force evaluation", "every tested N", RED_B),
            ("< 0.35 ms", "tree construction", "regardless of N", GREEN_B),
            ("34 – 41 %", "radix sort", "(of tree-build cost)", YELLOW_B),
        ]

        cards = VGroup()
        for big, label, sub, color in callouts:
            big_t = CleanText(big, font_size=34, weight=BOLD, color=color)
            label_t = CleanText(label, font_size=19, weight=BOLD)
            sub_t = CleanText(sub, font_size=14, color=GREY_B)
            content = VGroup(big_t, label_t, sub_t).arrange(DOWN, buff=0.1)
            box = SurroundingRectangle(
                content, color=color, buff=0.22, corner_radius=0.1, stroke_width=2
            )
            cards.add(VGroup(box, content))

        cards.arrange(DOWN, buff=0.25)
        cards.to_edge(LEFT, buff=1.4).shift(DOWN * 0.2)
        if cards.height > 5.4:
            cards.scale(5.4 / cards.height)

        for c in cards:
            self.add(c)

        self.wait(0.1)
        self.next_slide()
