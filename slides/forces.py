import math
import random

from manim import *
from manim_slides import Slide


class DirectForces(Slide):
    def construct(self):
        random.seed(42)

        # === Newton's law: the pair force ===
        heading = Text(
            "Newton's law of gravitation",
            font_size=36,
            weight=BOLD,
        ).to_edge(UP, buff=0.6)
        self.play(Write(heading))
        self.next_slide()

        dot_i = Dot(LEFT * 2.8 + UP * 0.8, radius=0.20, color=BLUE)
        dot_j = Dot(RIGHT * 2.8 + UP * 0.8, radius=0.20, color=ORANGE)
        label_i = MathTex("m_i", color=BLUE, font_size=40).next_to(dot_i, UP, buff=0.2)
        label_j = MathTex("m_j", color=ORANGE, font_size=40).next_to(dot_j, UP, buff=0.2)

        self.play(
            FadeIn(dot_i, scale=0.5),
            FadeIn(dot_j, scale=0.5),
            Write(label_i),
            Write(label_j),
        )
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

        # === Total force = sum over all other particles ===
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
        self.next_slide()

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
        self.next_slide()

        sum_eq = MathTex(
            r"\vec{F}_i = ",
            r"\sum_{j \neq i}",
            r"G \, m_i \, m_j \, \frac{\vec{r}_j - \vec{r}_i}{|\vec{r}_j - \vec{r}_i|^3}",
            font_size=44,
        ).to_edge(DOWN, buff=1.0)
        sum_eq[1].set_color(YELLOW)
        self.play(Transform(pair_eq, sum_eq))
        self.next_slide()

        # === Scale: every pair interacts ===
        self.play(
            FadeOut(arrows_to_i),
            FadeOut(dot_i),
            FadeOut(all_others),
            FadeOut(label_i),
            FadeOut(pair_eq),
        )

        new_heading = Text(
            "Every particle interacts with every other",
            font_size=32,
            weight=BOLD,
        ).to_edge(UP, buff=0.6)
        self.play(Transform(heading, new_heading))

        N = 12
        positions = []
        for _ in range(N):
            r = random.uniform(0.4, 2.4)
            theta = random.uniform(0, 2 * math.pi)
            positions.append([r * math.cos(theta), r * math.sin(theta) - 0.2, 0])

        particles = VGroup(*[Dot(p, radius=0.10, color=BLUE_C) for p in positions])
        self.play(
            LaggedStart(*[FadeIn(d, scale=0.5) for d in particles], lag_ratio=0.05),
            run_time=1.2,
        )
        self.next_slide()

        lines = VGroup()
        for a in range(N):
            for b in range(a + 1, N):
                line = Line(
                    particles[a].get_center(),
                    particles[b].get_center(),
                    stroke_width=1.0,
                    color=YELLOW_E,
                ).set_opacity(0.45)
                lines.add(line)
        self.play(Create(lines, lag_ratio=0.005), run_time=2.5)
        self.next_slide()

        count_label = MathTex(
            rf"\binom{{{N}}}{{2}} = \frac{{{N} \cdot {N - 1}}}{{2}} = {N * (N - 1) // 2} \text{{ interactions}}",
            font_size=36,
        ).to_edge(DOWN, buff=0.8)
        self.play(Write(count_label))
        self.next_slide()

        general_label = MathTex(
            r"\binom{N}{2} = \frac{N(N-1)}{2} \;\sim\; \mathcal{O}(N^2)",
            font_size=44,
            color=RED,
        ).to_edge(DOWN, buff=0.8)
        self.play(Transform(count_label, general_label))
        self.next_slide()

        # === The quadratic wall ===
        self.play(FadeOut(lines), FadeOut(particles), FadeOut(count_label))

        wall_heading = Text(
            "The quadratic wall",
            font_size=44,
            weight=BOLD,
            color=RED,
        ).to_edge(UP, buff=0.6)
        self.play(Transform(heading, wall_heading))

        numbers = (
            VGroup(
                MathTex(r"N = 10^5 \text{ particles}", font_size=40),
                MathTex(
                    r"\Rightarrow \; \sim 10^{10} \text{ interactions per timestep}",
                    font_size=40,
                ),
                MathTex(
                    r"\times \; 10^6 \text{ timesteps to evolve a galaxy}",
                    font_size=40,
                ),
                MathTex(r"= \; 10^{16} \text{ operations}", font_size=46, color=RED),
            )
            .arrange(DOWN, aligned_edge=LEFT, buff=0.5)
            .move_to(ORIGIN)
        )

        for n in numbers[:-1]:
            self.play(FadeIn(n, shift=UP * 0.2))
            self.next_slide()

        self.play(Write(numbers[-1]))
        bottleneck_box = SurroundingRectangle(
            numbers[-1], color=RED, buff=0.2, stroke_width=4
        )
        self.play(Create(bottleneck_box))
        self.next_slide()

        self.next_slide(loop=True)
        self.play(bottleneck_box.animate.set_stroke(width=9), run_time=0.6)
        self.play(bottleneck_box.animate.set_stroke(width=4), run_time=0.6)
