from manim import *
from manim_slides import Slide

from _text import CleanText


class DirectForces(Slide):
    def construct(self):
        heading = CleanText(
            "Newton's law of gravitation",
            font_size=36,
            weight=BOLD,
        ).to_edge(UP, buff=0.6)
        self.add(heading)

        dot_i = Dot(LEFT * 2.8 + UP * 0.8, radius=0.20, color=BLUE)
        dot_j = Dot(RIGHT * 2.8 + UP * 0.8, radius=0.20, color=ORANGE)
        label_i = MathTex("m_i", color=BLUE, font_size=40).next_to(dot_i, UP, buff=0.2)
        label_j = MathTex("m_j", color=ORANGE, font_size=40).next_to(
            dot_j, UP, buff=0.2
        )

        self.add(dot_i, dot_j, label_i, label_j)
        self.wait(0.1)
        self.next_slide()

        force_on_i = Arrow(
            dot_i.get_center(),
            dot_j.get_center(),
            buff=0.28,
            color=YELLOW,
            stroke_width=6,
            tip_length=0.25,
        )
        force_on_j = Arrow(
            dot_j.get_center(),
            dot_i.get_center(),
            buff=0.28,
            color=YELLOW,
            stroke_width=6,
            tip_length=0.25,
        )
        self.play(GrowArrow(force_on_i), GrowArrow(force_on_j))
        self.next_slide()

        pair_eq = MathTex(
            r"\vec{F}_{ij} = G \,",
            r"m_i",
            r"\,",
            r"m_j",
            r"\, \frac{\vec{r}_j - \vec{r}_i}{|\vec{r}_j - \vec{r}_i|^3}",
            font_size=44,
        ).to_edge(DOWN, buff=1.0)
        pair_eq[1].set_color(BLUE)
        pair_eq[3].set_color(ORANGE)
        self.play(Write(pair_eq))
        self.next_slide()

        # Total force = sum over all other particles
        self.play(FadeOut(force_on_i), FadeOut(force_on_j), FadeOut(label_j))

        peer_positions = [
            RIGHT * 1.4 + UP * 1.6,
            RIGHT * 3.6 + DOWN * 0.4,
            RIGHT * 0.6 + DOWN * 1.0,
            RIGHT * 2.7 + UP * 0.2,
            RIGHT * 1.9 + DOWN * 1.3,
        ]
        peer_dots = VGroup(*[Dot(p, radius=0.14, color=ORANGE) for p in peer_positions])
        all_others = VGroup(dot_j, *peer_dots)
        self.play(FadeIn(peer_dots, lag_ratio=0.1))

        arrows_to_i = VGroup(
            *[
                Arrow(
                    d.get_center(),
                    dot_i.get_center(),
                    buff=0.22,
                    color=YELLOW,
                    stroke_width=4,
                    tip_length=0.18,
                )
                for d in all_others
            ]
        )
        self.play(
            LaggedStart(*[GrowArrow(a) for a in arrows_to_i], lag_ratio=0.15),
            run_time=1.5,
        )

        sum_eq = MathTex(
            r"\vec{F}_i = ",
            r"\sum_{j \neq i}",
            r"G \, m_i \, m_j \, \frac{\vec{r}_j - \vec{r}_i}{|\vec{r}_j - \vec{r}_i|^3}",
            font_size=44,
        ).to_edge(DOWN, buff=1.0)
        sum_eq[1].set_color(YELLOW)
        self.play(Transform(pair_eq, sum_eq))
        self.next_slide()
