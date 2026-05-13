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
        # x-axis: complete pipeline (no → yes)
        # y-axis: browser-deployable (no → yes)
        origin = ORIGIN + DOWN * 0.4
        x_len = 6.0
        y_len = 4.0

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

        x_label = Text("complete pipeline", font_size=20, color=GREY_B).next_to(
            axes[0], DOWN, buff=0.15
        )
        y_label = (
            Text("browser-deployable", font_size=20, color=GREY_B)
            .rotate(PI / 2)
            .next_to(axes[1], LEFT, buff=0.15)
        )
        self.play(FadeIn(x_label), FadeIn(y_label))
        self.next_slide()

        # Quadrant chip helper
        def chip(text, pos, color):
            t = Text(text, font_size=18, color=color)
            box = SurroundingRectangle(
                t, color=color, buff=0.15, corner_radius=0.08, stroke_width=1.5
            )
            return VGroup(box, t).move_to(pos)

        # Existing native GPU work: complete pipeline, NOT browser
        ne_native = chip(
            "Burtscher 2011\nGaburov 2010\n(CUDA / Metal)",
            origin + RIGHT * x_len * 0.27 + DOWN * y_len * 0.27,
            BLUE_B,
        )
        # Isolated browser kernels: browser, NOT complete pipeline
        nw_browser_kernels = chip(
            "Browser GPU kernels\n(matmul, reductions)",
            origin + LEFT * x_len * 0.27 + UP * y_len * 0.27,
            YELLOW_B,
        )
        # This thesis: both
        ne_us = chip(
            "★ This thesis",
            origin + RIGHT * x_len * 0.27 + UP * y_len * 0.27,
            GREEN_B,
        )

        self.play(FadeIn(ne_native, shift=UP * 0.2))
        self.next_slide()
        self.play(FadeIn(nw_browser_kernels, shift=UP * 0.2))
        self.next_slide()
        self.play(FadeIn(ne_us, shift=UP * 0.2))

        # highlight us
        pulse = SurroundingRectangle(ne_us, color=GREEN_B, buff=0.05, stroke_width=3)
        self.play(Create(pulse))
        self.next_slide()

        self.next_slide(loop=True)
        self.play(pulse.animate.set_stroke(width=6), run_time=0.6)
        self.play(pulse.animate.set_stroke(width=3), run_time=0.6)
