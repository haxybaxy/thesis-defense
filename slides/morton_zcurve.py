import random

import numpy as np
from manim import *
from manim_slides import Slide

from _text import CleanText


def morton_2d(x: int, y: int, bits: int) -> int:
    code = 0
    for b in range(bits):
        code |= ((x >> b) & 1) << (2 * b)
        code |= ((y >> b) & 1) << (2 * b + 1)
    return code


class MortonZCurve(Slide):
    def construct(self):
        random.seed(11)

        heading = CleanText(
            "Morton codes: a 1-D ordering with spatial locality",
            font_size=30,
            weight=BOLD,
        ).to_edge(UP, buff=0.5)
        self.add(heading)
        self.wait(0.1)
        self.next_slide()

        grid_size = 4
        cell_size = 0.85
        grid_origin = LEFT * 1.0 + DOWN * 0.4

        centers = {}
        for gy in range(grid_size):
            for gx in range(grid_size):
                code = morton_2d(gx, gy, bits=2)
                centers[code] = (
                    grid_origin
                    + RIGHT * (gx - 1.5) * cell_size
                    + UP * (gy - 1.5) * cell_size
                )

        particle_positions = [centers[1], centers[3], centers[6], centers[14]]
        particle_dots = VGroup(
            *[Dot(p, radius=0.10, color=BLUE) for p in particle_positions]
        )
        self.play(FadeIn(particle_dots, lag_ratio=0.2))

        cells = VGroup()
        labels = VGroup()
        label_inset = 0.16
        for gy in range(grid_size):
            for gx in range(grid_size):
                code = morton_2d(gx, gy, bits=2)
                center = centers[code]
                cell = Square(
                    side_length=cell_size, color=GRAY_B, stroke_width=1.5
                ).move_to(center)
                label = MathTex(str(code), font_size=18, color=GRAY_A).move_to(
                    center
                    + np.array(
                        [-cell_size / 2 + label_inset, cell_size / 2 - label_inset, 0]
                    )
                )
                cells.add(cell)
                labels.add(label)

        self.play(Create(cells, lag_ratio=0.02), run_time=1.2)
        self.play(Write(labels, lag_ratio=0.04), run_time=1.4)
        self.next_slide()

        points = [centers[c] for c in range(grid_size * grid_size)]
        z_curve = VMobject(color=RED, stroke_width=4)
        z_curve.set_points_as_corners(points)
        self.play(Create(z_curve), run_time=2.5)
        self.next_slide()

        locality_label = CleanText(
            "spatially close particles  →  numerically close Morton codes",
            font_size=22,
            color=BLUE,
        ).to_edge(DOWN, buff=0.6)
        self.play(FadeIn(locality_label, shift=UP * 0.2))
        self.next_slide()
