from manim import *
from manim_slides import Slide

from _text import CleanText


class ThetaSweep(Slide):
    def construct(self):
        heading = CleanText(
            "Numerical quality: the θ sweep",
            font_size=40,
            weight=BOLD,
        ).to_edge(UP, buff=0.6)
        self.add(heading)
        self.wait(0.1)
        self.next_slide()

        subhead = CleanText(
            "Sweeping opening angle θ at N = 5 000",
            font_size=20,
            slant=ITALIC,
            color=GREY_B,
        ).next_to(heading, DOWN, buff=0.3)
        self.add(subhead)
        self.wait(0.1)
        self.next_slide()

        # table: theta, runtime, drift
        rows = [
            ("0.3",  "9.30 ms", "2.67 × 10⁻⁴",  GREEN_B),
            ("0.5",  "8.24 ms", "2.75 × 10⁻³",  YELLOW_B),
            ("0.7",  "7.57 ms", "9.77 × 10⁻³",  ORANGE),
            ("1.0",  "6.96 ms", "3.31 × 10⁻²",  RED_B),
        ]

        positions = [-3.5, 0.0, 3.5]
        hdr_y = 1.4
        col_labels = ["θ", "Runtime", "Energy drift"]
        hdr = VGroup()
        for x, lbl in zip(positions, col_labels):
            hdr.add(CleanText(lbl, font_size=22, weight=BOLD, color=GREY_C).move_to([x, hdr_y, 0]))
        self.add(hdr)
        self.wait(0.1)
        self.next_slide()

        for i, (theta, rt, drift, color) in enumerate(rows):
            y = 0.7 - i * 0.55
            theta_t = MathTex(rf"\theta = {theta}", font_size=28, color=color).move_to(
                [positions[0], y, 0]
            )
            rt_t = CleanText(rt, font_size=22).move_to([positions[1], y, 0])
            drift_t = CleanText(drift, font_size=22, weight=BOLD, color=color).move_to(
                [positions[2], y, 0]
            )
            self.add(theta_t, rt_t, drift_t)
        self.wait(0.1)
        self.next_slide()

        # headline
        tag = CleanText(
            "Two orders of magnitude across θ",
            font_size=24,
            weight=BOLD,
            color=ORANGE,
        ).to_edge(DOWN, buff=1.0)
        self.add(tag)
        self.wait(0.1)
        self.next_slide()

        insight = CleanText(
            "Precision isn't only 32-bit float — tree approximation contributes.",
            font_size=18,
            slant=ITALIC,
            color=YELLOW_B,
        ).to_edge(DOWN, buff=0.5)
        self.add(insight)
        self.wait(0.1)
        self.next_slide()
