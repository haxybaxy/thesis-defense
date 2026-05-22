from manim import *
from manim_slides import Slide


class TheGap(Slide):
    def construct(self):
        heading = Text(
            "The gap in the literature",
            font_size=40,
            weight=BOLD,
        ).to_edge(UP, buff=0.6)
        self.play(Write(heading))
        self.next_slide()

        # 2×2 quadrant chart
        #   x-axis: graphics  →  general compute
        #   y-axis: isolated kernel  →  full pipeline
        origin = ORIGIN + DOWN * 0.4
        x_len = 8.0
        y_len = 4.6

        axes = VGroup(
            Arrow(
                origin + LEFT * x_len / 2,
                origin + RIGHT * x_len / 2,
                buff=0,
                color=GREY_B,
                stroke_width=2,
                tip_length=0.18,
            ),
            Arrow(
                origin + DOWN * y_len / 2,
                origin + UP * y_len / 2,
                buff=0,
                color=GREY_B,
                stroke_width=2,
                tip_length=0.18,
            ),
        )
        self.play(Create(axes))

        # Axis end-labels (left/right and bottom/top).
        x_left = Text("graphics", font_size=18, color=GREY_B).next_to(
            axes[0].get_start(), DL, buff=0.15
        )
        x_right = Text("general compute", font_size=18, color=GREY_B).next_to(
            axes[0].get_end(), DR, buff=0.15
        )
        y_bot = Text("isolated kernel", font_size=18, color=GREY_B).next_to(
            axes[1].get_start(), DOWN, buff=0.2
        )
        y_top = Text("full pipeline", font_size=18, color=GREY_B).next_to(
            axes[1].get_end(), UP, buff=0.2
        )
        self.play(FadeIn(x_left), FadeIn(x_right), FadeIn(y_bot), FadeIn(y_top))
        self.next_slide()

        # Quadrant chip helper.
        def chip(text, pos, color):
            t = Text(text, font_size=18, color=color)
            box = SurroundingRectangle(
                t,
                color=color,
                buff=0.15,
                corner_radius=0.08,
                stroke_width=1.5,
            ).set_fill(BLACK, opacity=0.35)
            return VGroup(box, t).move_to(pos)

        # Top-left: graphics, full pipeline → WebGL rendering demos.
        nw = chip(
            "WebGL rendering\ndemos",
            origin + LEFT * x_len * 0.27 + UP * y_len * 0.27,
            BLUE_B,
        )
        # Bottom-left: graphics, isolated kernel → shader benchmarks.
        sw = chip(
            "shader\nbenchmarks",
            origin + LEFT * x_len * 0.27 + DOWN * y_len * 0.27,
            YELLOW_B,
        )
        # Bottom-right: compute, isolated kernel → vector-add / matmul.
        se = chip(
            "vector-add  ·  matmul\n(isolated WebGPU kernels)",
            origin + RIGHT * x_len * 0.27 + DOWN * y_len * 0.27,
            ORANGE,
        )
        # Top-right: compute, full pipeline → this thesis (glow).
        ne_pos = origin + RIGHT * x_len * 0.27 + UP * y_len * 0.27
        glow_layers = VGroup()
        for r, opacity in [(0.95, 0.10), (0.75, 0.18), (0.55, 0.30)]:
            glow_layers.add(
                Circle(radius=r, color=GREEN_B, stroke_width=0)
                .set_fill(GREEN_B, opacity=opacity)
                .move_to(ne_pos)
            )
        thesis_dot = Dot(ne_pos, radius=0.13, color=GREEN_B)
        thesis_label = Text(
            "★ this thesis",
            font_size=22,
            weight=BOLD,
            color=GREEN_B,
        ).next_to(thesis_dot, UP, buff=0.25)

        self.play(FadeIn(nw, shift=UP * 0.15))
        self.next_slide()
        self.play(FadeIn(sw, shift=UP * 0.15))
        self.next_slide()
        self.play(FadeIn(se, shift=UP * 0.15))
        self.next_slide()
        self.play(
            FadeIn(glow_layers, scale=0.9),
            FadeIn(thesis_dot),
            FadeIn(thesis_label, shift=UP * 0.15),
            run_time=0.7,
        )
        self.next_slide()

        # Gentle pulsing glow on the thesis position to land the point.
        self.next_slide(loop=True)
        self.play(
            glow_layers.animate.scale(1.08),
            run_time=0.7,
        )
        self.play(
            glow_layers.animate.scale(1 / 1.08),
            run_time=0.7,
        )
