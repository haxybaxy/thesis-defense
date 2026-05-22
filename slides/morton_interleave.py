from manim import *
from manim_slides import Slide

from _text import CleanText

X_COLOR = ORANGE
Y_COLOR = TEAL
Z_COLOR = PURPLE


class MortonInterleave(Slide):
    def construct(self):
        heading = CleanText(
            "Bit interleaving: 3 axes → one integer key",
            font_size=30,
            weight=BOLD,
        ).to_edge(UP, buff=0.5)
        self.add(heading)
        self.wait(0.1)
        self.next_slide()

        # Sample 3-bit coordinates: x=5, y=3, z=6
        # bits[i] is the i-th bit (i=0 is LSB)
        x_bits = [1, 0, 1]
        y_bits = [1, 1, 0]
        z_bits = [0, 1, 1]

        def make_row(axis_name: str, bits: list[int], color, y_pos: float):
            label = MathTex(f"{axis_name} =", font_size=32, color=color).move_to(
                LEFT * 5.5 + UP * y_pos
            )
            digits = VGroup()
            # Display MSB → LSB left-to-right; bits list is LSB-first → reverse
            for i, b in enumerate(reversed(bits)):
                d = MathTex(str(b), font_size=44, color=color).move_to(
                    LEFT * 3.6 + RIGHT * i * 0.7 + UP * y_pos
                )
                digits.add(d)
            return label, digits

        x_label, x_digits = make_row("x", x_bits, X_COLOR, 2.0)
        y_label, y_digits = make_row("y", y_bits, Y_COLOR, 1.0)
        z_label, z_digits = make_row("z", z_bits, Z_COLOR, 0.0)

        self.play(
            FadeIn(x_label),
            Write(x_digits, lag_ratio=0.15),
        )
        self.play(
            FadeIn(y_label),
            Write(y_digits, lag_ratio=0.15),
        )
        self.play(
            FadeIn(z_label),
            Write(z_digits, lag_ratio=0.15),
        )
        self.next_slide()

        morton_label = MathTex(r"\mathrm{Morton} =", font_size=32).move_to(
            LEFT * 5.5 + DOWN * 1.8
        )
        slot_positions = [LEFT * 3.4 + RIGHT * i * 0.7 + DOWN * 1.8 for i in range(9)]
        slots = VGroup(
            *[
                Rectangle(
                    width=0.55, height=0.65, color=GRAY_D, stroke_width=1
                ).move_to(p)
                for p in slot_positions
            ]
        )
        self.play(FadeIn(morton_label), Create(slots))

        # Bit order MSB→LSB in the displayed Morton key: z2 y2 x2 z1 y1 x1 z0 y0 x0
        copies = []
        animations = []
        for i, d in enumerate(x_digits):
            c = d.copy()
            copies.append(c)
            animations.append(c.animate.move_to(slot_positions[2 + 3 * i]))
        for i, d in enumerate(y_digits):
            c = d.copy()
            copies.append(c)
            animations.append(c.animate.move_to(slot_positions[1 + 3 * i]))
        for i, d in enumerate(z_digits):
            c = d.copy()
            copies.append(c)
            animations.append(c.animate.move_to(slot_positions[0 + 3 * i]))

        self.add(*copies)
        self.play(LaggedStart(*animations, lag_ratio=0.08), run_time=2.5)

        bits_note = CleanText(
            "in the solver: 10 bits per axis  →  30-bit Morton key",
            font_size=22,
            color=GRAY_A,
        ).to_edge(DOWN, buff=0.4)
        self.play(FadeIn(bits_note, shift=UP * 0.2))
        self.next_slide()
