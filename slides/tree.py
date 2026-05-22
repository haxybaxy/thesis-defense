from manim import *
from manim_slides import Slide

from _text import CleanText


SUB = "₁₂₃₄₅₆₇₈₉"  # Unicode subscript digits, 1-indexed access via SUB[i-1]


def p_label(i: int) -> str:
    return f"p{SUB[i - 1]}"


class LBVHBuild(Slide):
    def construct(self):
        heading = CleanText(
            "Building the tree: recursive subdivision",
            font_size=32,
            weight=BOLD,
        ).to_edge(UP, buff=0.4)
        self.add(heading)

        citation_text = CleanText(
            "Karras, 2012",
            font_size=18,
            color=GREY_B,
            slant=ITALIC,
        )
        citation_box = SurroundingRectangle(
            citation_text,
            color=GREY_B,
            buff=0.12,
            corner_radius=0.06,
            stroke_width=1.2,
        ).set_fill(BLACK, opacity=0.35)
        citation = VGroup(citation_box, citation_text).to_corner(DL, buff=0.35)
        self.add(citation)
        self.next_slide()

        # 8 particles in a 2x4 grid, laid out so z-order = quad-by-quad scan.
        #   p1 p2 | p5 p6   (top row)
        #   p3 p4 | p7 p8   (bottom row)
        col_x = [-5.6, -4.6, -3.2, -2.2]
        row_y = [1.7, 0.1]
        spatial_pos = [
            (col_x[0], row_y[0]),
            (col_x[1], row_y[0]),  # p1, p2
            (col_x[0], row_y[1]),
            (col_x[1], row_y[1]),  # p3, p4
            (col_x[2], row_y[0]),
            (col_x[3], row_y[0]),  # p5, p6
            (col_x[2], row_y[1]),
            (col_x[3], row_y[1]),  # p7, p8
        ]

        particles = VGroup()
        plabels = VGroup()
        for i, (x, y) in enumerate(spatial_pos):
            dot = Dot(point=[x, y, 0], radius=0.10, color=YELLOW)
            lbl = CleanText(p_label(i + 1), font_size=18, color=GRAY_A).next_to(
                dot, UR, buff=0.04
            )
            particles.add(dot)
            plabels.add(lbl)

        self.play(
            FadeIn(particles, lag_ratio=0.05),
            FadeIn(plabels, lag_ratio=0.05),
        )
        # Sorted list (bottom of left half)
        cell_w = 0.5
        list_y = -2.5
        list_x0 = -5.75
        list_cells = VGroup()
        for i in range(8):
            cell = Rectangle(
                width=cell_w,
                height=0.55,
                color=GRAY_A,
                stroke_width=2,
            ).move_to([list_x0 + i * cell_w, list_y, 0])
            txt = CleanText(p_label(i + 1), font_size=20).move_to(cell.get_center())
            list_cells.add(VGroup(cell, txt))

        list_cap = CleanText(
            "sorted by Morton code",
            font_size=18,
            color=GRAY_B,
            slant=ITALIC,
        ).next_to(list_cells, DOWN, buff=0.15)

        self.play(FadeIn(list_cells, lag_ratio=0.08), FadeIn(list_cap))
        self.next_slide()

        # Spatial bounds and split coordinates
        bbox_l = col_x[0] - 0.4
        bbox_r = col_x[3] + 0.4
        bbox_t = row_y[0] + 0.4
        bbox_b = row_y[1] - 0.4
        s1x = (col_x[1] + col_x[2]) / 2  # vertical split (root)
        s2y = (row_y[0] + row_y[1]) / 2  # horizontal split (level 2)
        s3x_L = (col_x[0] + col_x[1]) / 2  # vertical split inside left half
        s3x_R = (col_x[2] + col_x[3]) / 2  # vertical split inside right half

        def make_box(l, r, t, b, color, fill_opacity=0.08, stroke=2.5):
            return (
                Rectangle(
                    width=r - l,
                    height=t - b,
                    color=color,
                    stroke_width=stroke,
                )
                .move_to([(l + r) / 2, (t + b) / 2, 0])
                .set_fill(color, opacity=fill_opacity)
            )

        def make_node(pos, label, color, font_size=18, leaf=False):
            if leaf:
                shape = Square(side_length=0.5, color=color, stroke_width=2.5).move_to(
                    pos
                )
            else:
                shape = Circle(radius=0.32, color=color, stroke_width=2.5).move_to(pos)
            shape.set_fill(color, opacity=0.15)
            t = CleanText(label, font_size=font_size, color=color).move_to(pos)
            return VGroup(shape, t)

        # Tree node positions (right half of screen)
        root_pos = [3.8, 2.5, 0]
        L1_pos = [[2.2, 1.1, 0], [5.4, 1.1, 0]]
        L2_pos = [[1.4, -0.3, 0], [3.0, -0.3, 0], [4.6, -0.3, 0], [6.2, -0.3, 0]]
        leaf_pos = [
            [1.0, -1.7, 0],
            [1.8, -1.7, 0],
            [2.6, -1.7, 0],
            [3.4, -1.7, 0],
            [4.2, -1.7, 0],
            [5.0, -1.7, 0],
            [5.8, -1.7, 0],
            [6.6, -1.7, 0],
        ]

        # Root: bounding box around everything + root tree node
        root_bbox = make_box(bbox_l, bbox_r, bbox_t, bbox_b, BLUE)
        root_node = make_node(root_pos, "[1..8]", BLUE)
        self.play(FadeIn(root_bbox), FadeIn(root_node))
        self.next_slide()

        # Split 1: vertical cut → root has two children
        split1 = DashedLine(
            [s1x, bbox_t + 0.05, 0],
            [s1x, bbox_b - 0.05, 0],
            color=YELLOW,
            stroke_width=3,
            dash_length=0.1,
        )
        L_box = make_box(bbox_l, s1x, bbox_t, bbox_b, GREEN)
        R_box = make_box(s1x, bbox_r, bbox_t, bbox_b, PURPLE)
        L_list_hl = SurroundingRectangle(
            VGroup(list_cells[0], list_cells[3]),
            color=GREEN,
            stroke_width=3,
            buff=0.03,
        )
        R_list_hl = SurroundingRectangle(
            VGroup(list_cells[4], list_cells[7]),
            color=PURPLE,
            stroke_width=3,
            buff=0.03,
        )
        L_node = make_node(L1_pos[0], "[1..4]", GREEN)
        R_node = make_node(L1_pos[1], "[5..8]", PURPLE)
        e_root_L = Line(
            root_node[0].get_bottom(),
            L_node[0].get_top(),
            color=GRAY_A,
            stroke_width=2,
        )
        e_root_R = Line(
            root_node[0].get_bottom(),
            R_node[0].get_top(),
            color=GRAY_A,
            stroke_width=2,
        )

        self.play(
            Create(split1),
            FadeOut(root_bbox),
            FadeIn(L_box),
            FadeIn(R_box),
            FadeIn(L_list_hl),
            FadeIn(R_list_hl),
            Create(e_root_L),
            Create(e_root_R),
            FadeIn(L_node),
            FadeIn(R_node),
            run_time=1.0,
        )
        self.next_slide()

        # Split 2: horizontal cut inside each half → four quadrants
        split2L = DashedLine(
            [bbox_l - 0.05, s2y, 0],
            [s1x, s2y, 0],
            color=YELLOW,
            stroke_width=3,
            dash_length=0.1,
        )
        split2R = DashedLine(
            [s1x, s2y, 0],
            [bbox_r + 0.05, s2y, 0],
            color=YELLOW,
            stroke_width=3,
            dash_length=0.1,
        )
        LL_box = make_box(bbox_l, s1x, bbox_t, s2y, TEAL)
        LR_box = make_box(bbox_l, s1x, s2y, bbox_b, ORANGE)
        RL_box = make_box(s1x, bbox_r, bbox_t, s2y, PINK)
        RR_box = make_box(s1x, bbox_r, s2y, bbox_b, MAROON)
        LL_hl = SurroundingRectangle(
            VGroup(list_cells[0], list_cells[1]),
            color=TEAL,
            stroke_width=3,
            buff=0.02,
        )
        LR_hl = SurroundingRectangle(
            VGroup(list_cells[2], list_cells[3]),
            color=ORANGE,
            stroke_width=3,
            buff=0.02,
        )
        RL_hl = SurroundingRectangle(
            VGroup(list_cells[4], list_cells[5]),
            color=PINK,
            stroke_width=3,
            buff=0.02,
        )
        RR_hl = SurroundingRectangle(
            VGroup(list_cells[6], list_cells[7]),
            color=MAROON,
            stroke_width=3,
            buff=0.02,
        )
        LL_node = make_node(L2_pos[0], "[1,2]", TEAL, font_size=16)
        LR_node = make_node(L2_pos[1], "[3,4]", ORANGE, font_size=16)
        RL_node = make_node(L2_pos[2], "[5,6]", PINK, font_size=16)
        RR_node = make_node(L2_pos[3], "[7,8]", MAROON, font_size=16)
        e_L_LL = Line(
            L_node[0].get_bottom(), LL_node[0].get_top(), color=GRAY_A, stroke_width=2
        )
        e_L_LR = Line(
            L_node[0].get_bottom(), LR_node[0].get_top(), color=GRAY_A, stroke_width=2
        )
        e_R_RL = Line(
            R_node[0].get_bottom(), RL_node[0].get_top(), color=GRAY_A, stroke_width=2
        )
        e_R_RR = Line(
            R_node[0].get_bottom(), RR_node[0].get_top(), color=GRAY_A, stroke_width=2
        )

        self.play(
            Create(split2L),
            Create(split2R),
            FadeOut(L_box),
            FadeOut(R_box),
            FadeOut(L_list_hl),
            FadeOut(R_list_hl),
            FadeIn(LL_box),
            FadeIn(LR_box),
            FadeIn(RL_box),
            FadeIn(RR_box),
            FadeIn(LL_hl),
            FadeIn(LR_hl),
            FadeIn(RL_hl),
            FadeIn(RR_hl),
            Create(e_L_LL),
            Create(e_L_LR),
            Create(e_R_RL),
            Create(e_R_RR),
            FadeIn(LL_node),
            FadeIn(LR_node),
            FadeIn(RL_node),
            FadeIn(RR_node),
            run_time=1.2,
        )
        self.next_slide()

        # Split 3: vertical cut inside each quadrant → eight singleton cells
        split3_lines = VGroup(
            DashedLine(
                [s3x_L, bbox_t + 0.05, 0],
                [s3x_L, s2y, 0],
                color=YELLOW,
                stroke_width=2.5,
                dash_length=0.08,
            ),
            DashedLine(
                [s3x_L, s2y, 0],
                [s3x_L, bbox_b - 0.05, 0],
                color=YELLOW,
                stroke_width=2.5,
                dash_length=0.08,
            ),
            DashedLine(
                [s3x_R, bbox_t + 0.05, 0],
                [s3x_R, s2y, 0],
                color=YELLOW,
                stroke_width=2.5,
                dash_length=0.08,
            ),
            DashedLine(
                [s3x_R, s2y, 0],
                [s3x_R, bbox_b - 0.05, 0],
                color=YELLOW,
                stroke_width=2.5,
                dash_length=0.08,
            ),
        )

        # Map each particle to the (col, row) of its final cell
        leaf_x_bounds = [
            (bbox_l, s3x_L),  # col 0
            (s3x_L, s1x),  # col 1
            (s1x, s3x_R),  # col 2
            (s3x_R, bbox_r),  # col 3
        ]
        leaf_y_bounds = [
            (s2y, bbox_t),  # row 0 (top)
            (bbox_b, s2y),  # row 1 (bot)
        ]
        particle_cell = [
            (0, 0),
            (1, 0),  # p1, p2
            (0, 1),
            (1, 1),  # p3, p4
            (2, 0),
            (3, 0),  # p5, p6
            (2, 1),
            (3, 1),  # p7, p8
        ]

        leaf_boxes = VGroup()
        for c, r in particle_cell:
            xl, xr = leaf_x_bounds[c]
            yb, yt = leaf_y_bounds[r]
            leaf_boxes.add(
                make_box(xl, xr, yt, yb, BLUE_C, fill_opacity=0.18, stroke=1.8)
            )

        leaf_hls = VGroup(
            *[
                SurroundingRectangle(cell, color=BLUE_C, stroke_width=2.5, buff=0.02)
                for cell in list_cells
            ]
        )

        leaf_nodes = VGroup(
            *[
                make_node(leaf_pos[i], p_label(i + 1), BLUE_C, font_size=18, leaf=True)
                for i in range(8)
            ]
        )

        leaf_parents = [
            LL_node,
            LL_node,
            LR_node,
            LR_node,
            RL_node,
            RL_node,
            RR_node,
            RR_node,
        ]
        leaf_edges = VGroup(
            *[
                Line(
                    leaf_parents[i][0].get_bottom(),
                    leaf_nodes[i][0].get_top(),
                    color=GRAY_A,
                    stroke_width=2,
                )
                for i in range(8)
            ]
        )

        self.play(
            Create(split3_lines),
            FadeOut(LL_box),
            FadeOut(LR_box),
            FadeOut(RL_box),
            FadeOut(RR_box),
            FadeOut(LL_hl),
            FadeOut(LR_hl),
            FadeOut(RL_hl),
            FadeOut(RR_hl),
            FadeIn(leaf_boxes, lag_ratio=0.08),
            FadeIn(leaf_hls, lag_ratio=0.08),
            Create(leaf_edges, lag_ratio=0.08),
            FadeIn(leaf_nodes, lag_ratio=0.08),
            run_time=1.5,
        )
        self.next_slide()

        concl = CleanText(
            "every leaf region holds exactly one particle",
            font_size=22,
            color=YELLOW,
        ).move_to([0, -3.5, 0])
        self.play(FadeIn(concl))
        self.next_slide()
