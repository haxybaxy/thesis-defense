import math

from manim import *
from manim_slides import Slide


class TreePayoff(Slide):
    def construct(self):
        heading = Text(
            "The payoff: O(N²) → O(N log N)",
            font_size=36,
            weight=BOLD,
            color=GREEN,
        ).to_edge(UP, buff=0.5)
        self.play(Write(heading))
        self.next_slide()

        def n2_fn(x):
            return x * x

        def nlogn_fn(x):
            return x * math.log(max(x, 1.0))

        # (x_max, y_max) per stage — both axes grow together so the gap explodes.
        stages = [
            (20, 500),
            (100, 12000),
            (500, 300000),
            (2500, 6500000),
        ]

        def make_axes(x_max, y_max):
            return Axes(
                x_range=[0, x_max, x_max / 4],
                y_range=[0, y_max, y_max / 4],
                x_length=8,
                y_length=4.5,
                tips=False,
                axis_config={"stroke_width": 2, "include_numbers": False},
            ).move_to(DOWN * 0.4)

        ax = make_axes(*stages[0])
        x_label = Text("N (particles)", font_size=22, color=GRAY_A).next_to(
            ax.x_axis, DOWN, buff=0.3
        )
        y_label = Text("work", font_size=22, color=GRAY_A).next_to(
            ax.y_axis, LEFT, buff=0.3
        )
        self.play(Create(ax), Write(x_label), Write(y_label))

        def make_n2_label(ax, x_max, y_max):
            y_pos = min(n2_fn(x_max) * 1.06, y_max * 0.96)
            return MathTex(
                r"\mathcal{O}(N^2)", font_size=32, color=RED
            ).move_to(ax.c2p(x_max * 0.82, y_pos))

        def make_nlogn_label(ax, x_max, y_max):
            y_pos = max(nlogn_fn(x_max) * 2.2, y_max * 0.10)
            return MathTex(
                r"\mathcal{O}(N \log N)", font_size=30, color=GREEN
            ).move_to(ax.c2p(x_max * 0.65, y_pos))

        def gap_brace(ax, x):
            return Brace(
                Line(ax.c2p(x, nlogn_fn(x)), ax.c2p(x, n2_fn(x))),
                RIGHT,
                color=YELLOW,
            )

        x_max0, y_max0 = stages[0]
        n2_curve = ax.plot(n2_fn, x_range=[0, x_max0], color=RED, stroke_width=4)
        nlogn_curve = ax.plot(nlogn_fn, x_range=[1, x_max0], color=GREEN, stroke_width=4)
        n2_label = make_n2_label(ax, x_max0, y_max0)
        nlogn_label = make_nlogn_label(ax, x_max0, y_max0)
        brace = gap_brace(ax, x_max0)

        self.play(
            Create(n2_curve),
            Create(nlogn_curve),
            Write(n2_label),
            Write(nlogn_label),
        )
        self.play(GrowFromCenter(brace))
        self.next_slide()

        for x_max, y_max in stages[1:]:
            new_ax = make_axes(x_max, y_max)
            new_n2 = new_ax.plot(n2_fn, x_range=[0, x_max], color=RED, stroke_width=4)
            new_nlogn = new_ax.plot(nlogn_fn, x_range=[1, x_max], color=GREEN, stroke_width=4)
            new_n2_label = make_n2_label(new_ax, x_max, y_max)
            new_nlogn_label = make_nlogn_label(new_ax, x_max, y_max)
            new_brace = gap_brace(new_ax, x_max)
            new_x_label = Text(
                "N (particles)", font_size=22, color=GRAY_A
            ).next_to(new_ax.x_axis, DOWN, buff=0.3)
            new_y_label = Text(
                "work", font_size=22, color=GRAY_A
            ).next_to(new_ax.y_axis, LEFT, buff=0.3)
            self.play(
                Transform(ax, new_ax),
                Transform(n2_curve, new_n2),
                Transform(nlogn_curve, new_nlogn),
                Transform(n2_label, new_n2_label),
                Transform(nlogn_label, new_nlogn_label),
                Transform(brace, new_brace),
                Transform(x_label, new_x_label),
                Transform(y_label, new_y_label),
                run_time=1.2,
            )
            self.next_slide()

        gap_label = Text(
            "gap grows with N", font_size=22, color=YELLOW, weight=BOLD
        ).next_to(brace, RIGHT, buff=0.2)
        self.play(Write(gap_label))
        self.next_slide()
