import numpy as np

from manim import *
from manim_slides import Slide


class IntegratorEnergy(Slide):
    def construct(self):
        heading = Text(
            "Energy: the sanity check",
            font_size=36,
            weight=BOLD,
        ).to_edge(UP, buff=0.5)
        sub = Text(
            "How do you know the integrator is honest? Track the total energy and see if it stays put.",
            font_size=20,
            color=GRAY_A,
        ).next_to(heading, DOWN, buff=0.15)
        self.play(Write(heading), FadeIn(sub, shift=UP * 0.2))
        self.next_slide()

        # === Beat 1: T + U = E, plain-English first ===
        plain_t = Text(
            "Kinetic energy T — energy of motion. Sum of ½ m v² over every particle.",
            font_size=20,
            color=GRAY_A,
        )
        eq_t = MathTex(
            r"T \;=\; \tfrac{1}{2} \sum_i m_i \, |\vec{v}_i|^2",
            font_size=36,
        )

        plain_u = Text(
            "Potential energy U — energy stored in the field. One term per particle pair.",
            font_size=20,
            color=GRAY_A,
        )
        eq_u = MathTex(
            r"U \;=\; -\tfrac{1}{2}\, G \sum_{i \neq j} \frac{m_i \, m_j}{|\vec{r}_i - \vec{r}_j|}",
            font_size=36,
        )

        row_t = VGroup(plain_t, eq_t).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        row_u = VGroup(plain_u, eq_u).arrange(DOWN, aligned_edge=LEFT, buff=0.18)

        VGroup(row_t, row_u).arrange(DOWN, aligned_edge=LEFT, buff=0.4).move_to(
            ORIGIN + UP * 0.3
        )

        self.play(FadeIn(plain_t, shift=UP * 0.1))
        self.play(Write(eq_t))
        self.next_slide()

        self.play(FadeIn(plain_u, shift=UP * 0.1))
        self.play(Write(eq_u))
        self.next_slide()

        total_line = Text(
            "Total energy E = T + U. In a closed gravitational system this cannot change.",
            font_size=22,
            color=BLUE,
            weight=BOLD,
        ).to_edge(DOWN, buff=1.0)
        total_box = SurroundingRectangle(
            total_line, color=BLUE, buff=0.18, stroke_width=2
        )
        self.play(Write(total_line), Create(total_box))
        self.next_slide()

        # === Beat 2: The drift plot ===
        self.play(
            FadeOut(plain_t),
            FadeOut(eq_t),
            FadeOut(plain_u),
            FadeOut(eq_u),
            FadeOut(total_line),
            FadeOut(total_box),
            FadeOut(sub),
        )

        plot_heading = Text(
            "What conservation looks like — and what it doesn't",
            font_size=28,
            weight=BOLD,
        ).to_edge(UP, buff=0.5)
        self.play(Transform(heading, plot_heading))

        ax = Axes(
            x_range=[0, 10, 2],
            y_range=[-7, 0, 1],
            x_length=8.5,
            y_length=4.2,
            tips=False,
            axis_config={"color": GRAY_B, "stroke_width": 2},
        ).move_to(DOWN * 0.4)
        x_lbl = Text("time", font_size=18, color=GRAY_A).next_to(
            ax.x_axis, DOWN, buff=0.2
        )
        y_lbl = (
            MathTex(
                r"\log_{10}\!\left( |E(t) - E_0| / |E_0| \right)",
                font_size=22,
            )
            .next_to(ax.y_axis, LEFT, buff=0.2)
            .rotate(PI / 2)
            .shift(LEFT * 0.05)
        )
        self.play(Create(ax), FadeIn(x_lbl), FadeIn(y_lbl))
        self.next_slide()

        # Pre-compute curves so we can use VMobject path-tracing.
        ts = np.linspace(0.05, 10, 200)
        # Euler: drift grows roughly linearly with time → log10(slope * t)
        euler_y = np.log10(0.003 * ts + 1e-6) + 2.2 * (
            ts / 10
        )  # extra growth so it climbs
        # Cap below 0 so it stays inside the plot
        euler_y = np.clip(euler_y, -7, -0.1)
        # Leapfrog: small bounded oscillation around -5.2
        leap_y = -5.2 + 0.35 * np.sin(2.3 * ts) + 0.15 * np.cos(0.9 * ts)

        euler_path = VMobject(color=RED, stroke_width=3)
        euler_path.set_points_as_corners([ax.c2p(t, y) for t, y in zip(ts, euler_y)])
        leap_path = VMobject(color=GREEN, stroke_width=3)
        leap_path.set_points_as_corners([ax.c2p(t, y) for t, y in zip(ts, leap_y)])

        euler_label = Text("Euler", font_size=22, color=RED, weight=BOLD).next_to(
            ax.c2p(10, euler_y[-1]), RIGHT, buff=0.15
        )
        euler_cap = Text(
            "drift grows step after step",
            font_size=16,
            color=RED,
        ).next_to(euler_label, DOWN, buff=0.15, aligned_edge=LEFT)
        self.play(Create(euler_path, run_time=2.5))
        self.play(FadeIn(euler_label), FadeIn(euler_cap))
        self.next_slide()

        leap_label = Text("Leapfrog", font_size=22, color=GREEN, weight=BOLD).next_to(
            ax.c2p(10, leap_y[-1]), RIGHT, buff=0.15
        )
        leap_cap = Text(
            "bounded — wobbles, doesn't drift",
            font_size=16,
            color=GREEN,
        ).next_to(leap_label, DOWN, buff=0.15, aligned_edge=LEFT)
        self.play(Create(leap_path, run_time=2.5))
        self.play(FadeIn(leap_label), FadeIn(leap_cap))
        self.next_slide()

        # === Beat 3: The validation metric, boxed ===
        self.play(
            FadeOut(ax),
            FadeOut(x_lbl),
            FadeOut(y_lbl),
            FadeOut(euler_path),
            FadeOut(leap_path),
            FadeOut(euler_label),
            FadeOut(euler_cap),
            FadeOut(leap_label),
            FadeOut(leap_cap),
        )

        metric_heading = Text(
            "The validation metric",
            font_size=32,
            weight=BOLD,
        ).to_edge(UP, buff=0.5)
        self.play(Transform(heading, metric_heading))

        metric_plain = Text(
            "Relative energy drift — the one number we report to say the integrator works.",
            font_size=22,
            color=GRAY_A,
        ).move_to(UP * 1.2)
        metric_eq = MathTex(
            r"\Delta E \,/\, E_0 \;=\; \frac{|E(t) - E(0)|}{|E(0)|}",
            font_size=44,
        ).next_to(metric_plain, DOWN, buff=0.5)
        metric_box = SurroundingRectangle(
            metric_eq, color=BLUE, buff=0.25, stroke_width=3
        )
        self.play(FadeIn(metric_plain, shift=UP * 0.1))
        self.play(Write(metric_eq))
        self.play(Create(metric_box))
        self.next_slide()

        # === Beat 4: Tie-back to force-approximation error ===
        tie_back = (
            VGroup(
                Text(
                    "Integration error and force-approximation error compound.",
                    font_size=22,
                    color=GRAY_A,
                ),
                Text(
                    "A poor integrator dominates, no matter what θ you pick.",
                    font_size=24,
                    color=YELLOW,
                    weight=BOLD,
                ),
            )
            .arrange(DOWN, aligned_edge=LEFT, buff=0.25)
            .to_edge(DOWN, buff=0.8)
        )

        for line in tie_back:
            self.play(FadeIn(line, shift=UP * 0.1))
            self.next_slide()

        self.next_slide(loop=True)
        self.play(metric_box.animate.set_stroke(width=7), run_time=0.6)
        self.play(metric_box.animate.set_stroke(width=3), run_time=0.6)
