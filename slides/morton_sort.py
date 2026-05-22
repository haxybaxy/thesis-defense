import numpy as np
from manim import *
from manim_slides import Slide

from _text import CleanText

X_COLOR = ORANGE


def morton_3d(x: int, y: int, z: int, bits: int) -> int:
    code = 0
    for b in range(bits):
        code |= ((x >> b) & 1) << (3 * b)
        code |= ((y >> b) & 1) << (3 * b + 1)
        code |= ((z >> b) & 1) << (3 * b + 2)
    return code


class MortonSort(Slide):
    def construct(self):
        heading = CleanText(
            "Sort by Morton code  →  spatial neighbours become array neighbours",
            font_size=24,
            weight=BOLD,
        ).to_edge(UP, buff=0.5)
        self.add(heading)
        self.wait(0.1)
        self.next_slide()

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
            return VGroup(name_tex, coord_tex, code_tex, decimal_tex).arrange(
                RIGHT, buff=0.5
            )

        unsorted_rows = (
            VGroup(*[row_mobject(*r) for r in rows_with_codes])
            .arrange(DOWN, aligned_edge=LEFT, buff=0.3)
            .move_to(LEFT * 0.5 + DOWN * 0.2)
        )

        header = (
            VGroup(
                CleanText("particle", font_size=24, color=GRAY_A),
                CleanText("(x,y,z)", font_size=24, color=GRAY_A),
                CleanText("Morton bits", font_size=24, color=GRAY_A),
                CleanText("decimal", font_size=24, color=GRAY_A),
            )
            .arrange(RIGHT, buff=0.9)
            .move_to(unsorted_rows.get_top() + UP * 0.5)
        )

        self.play(FadeIn(header), FadeIn(unsorted_rows, lag_ratio=0.1))
        self.next_slide()

        sorted_data = sorted(rows_with_codes, key=lambda r: r[2])
        target_idx = [sorted_data.index(r) for r in rows_with_codes]
        slot_y = [unsorted_rows[i].get_center()[1] for i in range(5)]
        moved_indices = [i for i in range(5) if target_idx[i] != i]

        swap_highlights = VGroup(
            *[
                SurroundingRectangle(
                    unsorted_rows[i],
                    color=rows_with_codes[i][3],
                    buff=0.08,
                    stroke_width=3,
                    corner_radius=0.06,
                )
                for i in moved_indices
            ]
        )
        self.play(Create(swap_highlights, lag_ratio=0.15), run_time=0.6)
        self.next_slide()

        swap_anims = []
        for k, i in enumerate(moved_indices):
            new_y = slot_y[target_idx[i]]
            row_center = unsorted_rows[i].get_center()
            target = np.array([row_center[0], new_y, 0])
            swap_anims.append(unsorted_rows[i].animate(path_arc=PI / 3).move_to(target))
            swap_anims.append(
                swap_highlights[k].animate(path_arc=PI / 3).move_to(target)
            )
        self.play(*swap_anims, run_time=2.0)

        self.play(FadeOut(swap_highlights))

        adjacency_p1 = MathTex("p_1", font_size=28, color=X_COLOR)
        adjacency_and = CleanText("and", font_size=22, color=X_COLOR)
        adjacency_p3 = MathTex("p_3", font_size=28, color=X_COLOR)
        adjacency_rest = CleanText(
            "are spatially close  →  now adjacent in the sorted array",
            font_size=22,
            color=X_COLOR,
        )
        adjacency = (
            VGroup(adjacency_p1, adjacency_and, adjacency_p3, adjacency_rest)
            .arrange(RIGHT, buff=0.18)
            .to_edge(DOWN, buff=0.5)
        )
        self.play(FadeIn(adjacency, shift=UP * 0.2))
        self.next_slide()
