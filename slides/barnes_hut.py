import random

import numpy as np
from manim import *
from manim_slides import Slide

from _text import CleanText


class BarnesHutIdea(Slide):
    def construct(self):
        random.seed(7)

        # === Distant cluster collapses to its centre of mass ===
        heading = CleanText(
            "Barnes–Hut: O(nlogn) Traversal",
            font_size=40,
            weight=BOLD,
        ).to_edge(UP, buff=0.5)
        self.add(heading)

        citation_text = CleanText(
            "Barnes & Hut, 1986",
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
        self.add(citation)
        self.next_slide()

        observer = Dot(LEFT * 4.5, radius=0.18, color=BLUE)
        observer_label = MathTex("i", color=BLUE, font_size=32).next_to(
            observer, DOWN, buff=0.2
        )
        self.play(FadeIn(observer), Write(observer_label))

        cluster_center = RIGHT * 2.5 + UP * 0.3
        cluster_dots = []
        for _ in range(10):
            offset = np.array(
                [random.uniform(-0.7, 0.7), random.uniform(-0.7, 0.7), 0.0]
            )
            cluster_dots.append(Dot(cluster_center + offset, radius=0.10, color=ORANGE))
        cluster = VGroup(*cluster_dots)
        self.play(LaggedStart(*[FadeIn(d, scale=0.5) for d in cluster], lag_ratio=0.05))

        force_arrows = VGroup(
            *[
                Arrow(
                    d.get_center(),
                    observer.get_center(),
                    buff=0.22,
                    color=YELLOW,
                    stroke_width=2.5,
                    tip_length=0.15,
                )
                for d in cluster
            ]
        )
        self.play(LaggedStart(*[GrowArrow(a) for a in force_arrows], lag_ratio=0.1))
        self.next_slide()

        com_dot = Dot(cluster_center, radius=0.26, color=ORANGE)
        com_label = MathTex(r"(M,\, \vec{R})", color=ORANGE, font_size=36).next_to(
            com_dot, UP, buff=0.3
        )
        single_force = Arrow(
            cluster_center,
            observer.get_center(),
            buff=0.34,
            color=YELLOW,
            stroke_width=7,
            tip_length=0.28,
        )

        self.play(
            Transform(cluster, com_dot),
            Transform(force_arrows, single_force),
            FadeIn(com_label),
            run_time=1.5,
        )

        # === Monopole acceleration ===
        accel_eq = MathTex(
            r"\vec{a}_{i,\,\mathrm{node}} = G \, M \, "
            r"\frac{\vec{R} - \vec{r}_i}"
            r"{\bigl( \lvert \vec{R} - \vec{r}_i \rvert^2 + ",
            r"\varepsilon^2",
            r"\bigr)^{3/2}}",
            font_size=42,
        ).to_edge(DOWN, buff=0.9)
        accel_eq[1].set_color(GREEN)
        self.play(Write(accel_eq))
        self.next_slide()

        soft_label = CleanText(
            "Plummer softening: smooths the 1/r² singularity",
            font_size=22,
            color=GREEN,
        ).to_edge(DOWN, buff=0.25)
        soft_arrow = Arrow(
            soft_label.get_top(),
            accel_eq[1].get_bottom(),
            color=GREEN,
            buff=0.05,
            stroke_width=3,
            tip_length=0.15,
        )
        self.play(FadeIn(soft_label, shift=UP * 0.2), GrowArrow(soft_arrow))
        self.next_slide()
