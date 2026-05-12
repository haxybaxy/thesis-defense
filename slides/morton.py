import random

import numpy as np
from manim import *
from manim_slides import Slide

X_COLOR = ORANGE
Y_COLOR = TEAL
Z_COLOR = PURPLE


def morton_2d(x: int, y: int, bits: int) -> int:
    code = 0
    for b in range(bits):
        code |= ((x >> b) & 1) << (2 * b)
        code |= ((y >> b) & 1) << (2 * b + 1)
    return code


def morton_3d(x: int, y: int, z: int, bits: int) -> int:
    code = 0
    for b in range(bits):
        code |= ((x >> b) & 1) << (3 * b)
        code |= ((y >> b) & 1) << (3 * b + 1)
        code |= ((z >> b) & 1) << (3 * b + 2)
    return code


class MortonCodes(Slide):
    def construct(self):
        random.seed(11)

        heading = Text(
            "Morton codes: a 1-D ordering with spatial locality",
            font_size=30,
            weight=BOLD,
        ).to_edge(UP, buff=0.5)
        self.play(Write(heading))
        self.next_slide()

        # === Z-order curve through a 4×4 grid ===
        grid_size = 4
        cell_size = 0.85
        grid_origin = LEFT * 1.0 + DOWN * 0.4

        cells = VGroup()
        labels = VGroup()
        centers = {}
        for gy in range(grid_size):
            for gx in range(grid_size):
                code = morton_2d(gx, gy, bits=2)
                center = (
                    grid_origin
                    + RIGHT * (gx - 1.5) * cell_size
                    + UP * (gy - 1.5) * cell_size
                )
                cell = Square(
                    side_length=cell_size, color=GRAY_B, stroke_width=1.5
                ).move_to(center)
                label = MathTex(str(code), font_size=24, color=GRAY_A).move_to(center)
                cells.add(cell)
                labels.add(label)
                centers[code] = center

        self.play(Create(cells, lag_ratio=0.02), run_time=1.2)
        self.play(Write(labels, lag_ratio=0.04), run_time=1.4)
        self.next_slide()

        points = [centers[c] for c in range(grid_size * grid_size)]
        z_curve = VMobject(color=RED, stroke_width=4)
        z_curve.set_points_as_corners(points)
        self.play(Create(z_curve), run_time=2.5)
        self.next_slide()

        particle_positions = [
            centers[1] + np.array([-0.15, 0.10, 0]),
            centers[3] + np.array([0.10, -0.05, 0]),
            centers[6] + np.array([0.05, 0.15, 0]),
            centers[14] + np.array([-0.10, 0.0, 0]),
        ]
        particle_dots = VGroup(
            *[Dot(p, radius=0.10, color=BLUE) for p in particle_positions]
        )
        self.play(FadeIn(particle_dots, lag_ratio=0.2))

        locality_label = Text(
            "spatially close particles  →  numerically close Morton codes",
            font_size=22,
            color=BLUE,
        ).to_edge(DOWN, buff=0.6)
        self.play(FadeIn(locality_label, shift=UP * 0.2))
        self.next_slide()

        # === Bit interleaving ===
        self.play(
            FadeOut(cells),
            FadeOut(labels),
            FadeOut(z_curve),
            FadeOut(particle_dots),
            FadeOut(locality_label),
        )

        interleave_heading = Text(
            "Bit interleaving: 3 axes → one integer key",
            font_size=30,
            weight=BOLD,
        ).to_edge(UP, buff=0.5)
        self.play(Transform(heading, interleave_heading))

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
        slot_positions = [
            LEFT * 3.4 + RIGHT * i * 0.7 + DOWN * 1.8 for i in range(9)
        ]
        slots = VGroup(
            *[
                Rectangle(
                    width=0.55, height=0.65, color=GRAY_D, stroke_width=1
                ).move_to(p)
                for p in slot_positions
            ]
        )
        self.play(FadeIn(morton_label), Create(slots))
        self.next_slide()

        # Bit order MSB→LSB in the displayed Morton key: z2 y2 x2 z1 y1 x1 z0 y0 x0
        # x_digits[i] is displayed at index i (left=MSB). x_digits[0] = MSB bit (x[2]) → slot 2.
        # So x_digits[i] → slot 2 + 3*i, y_digits[i] → slot 1 + 3*i, z_digits[i] → slot 0 + 3*i.
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
        self.next_slide()

        bits_note = Text(
            "in the solver: 10 bits per axis  →  30-bit Morton key",
            font_size=22,
            color=GRAY_A,
        ).to_edge(DOWN, buff=0.4)
        self.play(FadeIn(bits_note, shift=UP * 0.2))
        self.next_slide()

        # === Sort by Morton code ===
        self.play(
            *[
                FadeOut(m)
                for m in [
                    x_label,
                    x_digits,
                    y_label,
                    y_digits,
                    z_label,
                    z_digits,
                    morton_label,
                    slots,
                    *copies,
                    bits_note,
                ]
            ]
        )

        sort_heading = Text(
            "Sort by Morton code  →  spatial neighbours become array neighbours",
            font_size=24,
            weight=BOLD,
        ).to_edge(UP, buff=0.5)
        self.play(Transform(heading, sort_heading))

        # 5 particles with 3-bit coordinates → 9-bit Morton codes
        particle_rows = [
            ("p_1", (1, 6, 2), X_COLOR),
            ("p_2", (6, 1, 5), GREEN),
            ("p_3", (2, 7, 3), X_COLOR),
            ("p_4", (5, 2, 6), GREEN),
            ("p_5", (4, 4, 4), YELLOW),
        ]
        rows_with_codes = [
            (name, coords, morton_3d(*coords, bits=3), color)
            for name, coords, color in particle_rows
        ]

        def row_mobject(name: str, coords: tuple, code: int, color) -> VGroup:
            name_tex = MathTex(name, font_size=30, color=color)
            coord_tex = MathTex(
                f"({coords[0]}, {coords[1]}, {coords[2]})",
                font_size=28,
                color=GRAY_A,
            )
            code_tex = MathTex(f"\\mathtt{{{code:09b}}}", font_size=28)
            decimal_tex = MathTex(f"= {code}", font_size=28, color=GRAY_A)
            return (
                VGroup(name_tex, coord_tex, code_tex, decimal_tex)
                .arrange(RIGHT, buff=0.5)
            )

        unsorted_rows = (
            VGroup(*[row_mobject(*r) for r in rows_with_codes])
            .arrange(DOWN, aligned_edge=LEFT, buff=0.3)
            .move_to(LEFT * 0.5 + DOWN * 0.2)
        )

        header = (
            VGroup(
                Text("particle", font_size=24, color=GRAY_A),
                Text("(x,y,z)", font_size=24, color=GRAY_A),
                Text("Morton bits", font_size=24, color=GRAY_A),
                Text("decimal", font_size=24, color=GRAY_A),
            )
            .arrange(RIGHT, buff=0.9)
            .move_to(unsorted_rows.get_top() + UP * 0.5)
        )

        self.play(FadeIn(header), FadeIn(unsorted_rows, lag_ratio=0.1))
        self.next_slide()

        sorted_data = sorted(rows_with_codes, key=lambda r: r[2])
        sorted_rows = (
            VGroup(*[row_mobject(*r) for r in sorted_data])
            .arrange(DOWN, aligned_edge=LEFT, buff=0.3)
            .move_to(unsorted_rows.get_center())
        )

        self.play(Transform(unsorted_rows, sorted_rows), run_time=1.8)
        self.next_slide()

        adjacency = Text(
            "p_1 and p_3 are spatially close  →  now adjacent in the sorted array",
            font_size=22,
            color=X_COLOR,
        ).to_edge(DOWN, buff=0.5)
        self.play(FadeIn(adjacency, shift=UP * 0.2))
        self.next_slide()
