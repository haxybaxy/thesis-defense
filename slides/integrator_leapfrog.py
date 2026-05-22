from manim import *
from manim_slides import Slide

from _text import CleanText


class IntegratorEquations(Slide):
    def construct(self):
        heading = CleanText(
            "Two integrators, two update patterns",
            font_size=36,
            weight=BOLD,
        ).to_edge(UP, buff=0.5)

        eul_label = CleanText("Forward Euler", font_size=28, color=BLUE, weight=BOLD)
        eul_caption = CleanText(
            "Update r and v every full Δt.",
            font_size=22,
            color=GRAY_A,
        )
        eul_eqs = VGroup(
            MathTex(
                r"\vec{r}^{\,n+1} \;=\; \vec{r}^{\,n} \;+\; \vec{v}^{\,n}\, \Delta t",
                font_size=34,
            ),
            MathTex(
                r"\vec{v}^{\,n+1} \;=\; \vec{v}^{\,n} \;+\; \vec{a}^{\,n}\, \Delta t",
                font_size=34,
            ),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35)
        euler_block = VGroup(eul_label, eul_caption, eul_eqs).arrange(
            DOWN, aligned_edge=LEFT, buff=0.45
        )
        euler_block.move_to(LEFT * 3.5 + DOWN * 0.2)

        lf_label = CleanText("Leapfrog (KDK)", font_size=28, color=GREEN, weight=BOLD)
        lf_caption = CleanText(
            "Half-kick → drift → half-kick.",
            font_size=22,
            color=GRAY_A,
        )
        lf_eqs = VGroup(
            MathTex(
                r"\vec{v}^{\,n+1/2} \;=\; \vec{v}^{\,n} \;+\; \tfrac{1}{2}\, \vec{a}^{\,n}\, \Delta t",
                font_size=32,
            ),
            MathTex(
                r"\vec{r}^{\,n+1} \;=\; \vec{r}^{\,n} \;+\; \vec{v}^{\,n+1/2}\, \Delta t",
                font_size=32,
            ),
            MathTex(
                r"\vec{v}^{\,n+1} \;=\; \vec{v}^{\,n+1/2} \;+\; \tfrac{1}{2}\, \vec{a}^{\,n+1}\, \Delta t",
                font_size=32,
            ),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        leapfrog_block = VGroup(lf_label, lf_caption, lf_eqs).arrange(
            DOWN, aligned_edge=LEFT, buff=0.45
        )
        leapfrog_block.move_to(RIGHT * 3.5 + DOWN * 0.2)

        self.add(heading, euler_block, leapfrog_block)
        self.wait(0.1)
        self.next_slide()
