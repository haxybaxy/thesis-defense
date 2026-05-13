from manim import *
from manim_slides import Slide


class WhereTimeIsSpent(Slide):
    def construct(self):
        heading = Text(
            "RQ1: Where does the time go?",
            font_size=40,
            weight=BOLD,
        ).to_edge(UP, buff=0.6)
        self.play(Write(heading))
        self.next_slide()

        # Three headline boxes
        callouts = [
            ("94 – 99 %", "force evaluation", "every tested N", RED_B),
            ("< 0.35 ms", "tree construction", "regardless of N", GREEN_B),
            ("34 – 41 %", "radix sort", "(of tree-build cost)", YELLOW_B),
        ]

        cards = VGroup()
        for big, label, sub, color in callouts:
            big_t = Text(big, font_size=44, weight=BOLD, color=color)
            label_t = Text(label, font_size=22, weight=BOLD)
            sub_t = Text(sub, font_size=16, color=GREY_B)
            content = VGroup(big_t, label_t, sub_t).arrange(DOWN, buff=0.15)
            box = SurroundingRectangle(
                content, color=color, buff=0.35, corner_radius=0.1, stroke_width=2
            )
            cards.add(VGroup(box, content))

        cards.arrange(RIGHT, buff=0.4)
        cards.next_to(heading, DOWN, buff=0.7)
        if cards.width > 13.0:
            cards.scale(13.0 / cards.width)

        for c in cards:
            self.play(FadeIn(c, shift=UP * 0.2), run_time=0.5)
            self.next_slide()

        # placeholder for the supporting figures
        fig_placeholder = Rectangle(width=10, height=1.3, color=GREY_C, stroke_width=1).to_edge(
            DOWN, buff=0.7
        )
        fig_label = Text(
            "[fig_n_scaling_plummer.png    ·    fig_lbvh_breakdown.png]",
            font_size=14,
            color=GREY_C,
        ).move_to(fig_placeholder.get_center())
        self.play(FadeIn(fig_placeholder), FadeIn(fig_label))
        self.next_slide()

        # tagline
        tag = Text(
            "Optimise the traversal shader. Ignore the tree build.",
            font_size=22,
            slant=ITALIC,
            color=ORANGE,
        ).next_to(fig_placeholder, UP, buff=0.25)
        self.play(Write(tag))
        self.next_slide()
