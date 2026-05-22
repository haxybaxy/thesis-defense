from manim import *
from manim_slides import Slide

from _text import CleanText


class TreeBuildConcept(Slide):
    def construct(self):
        block_w = 2.6
        block_h = 1.1

        int_box = RoundedRectangle(
            width=block_w,
            height=block_h,
            corner_radius=0.18,
            color=BLUE_B,
            stroke_width=3,
        ).set_fill(BLUE_B, opacity=0.22)
        int_label = CleanText(
            "Integrator",
            font_size=24,
            weight=BOLD,
            color=BLUE_B,
        ).move_to(int_box.get_center())
        integrator = VGroup(int_box, int_label).move_to(LEFT * 3.5 + UP * 0.6)

        tree_box = RoundedRectangle(
            width=block_w,
            height=block_h,
            corner_radius=0.18,
            color=GREEN_B,
            stroke_width=3,
        ).set_fill(GREEN_B, opacity=0.22)
        tree_label = CleanText(
            "Tree build",
            font_size=24,
            weight=BOLD,
            color=GREEN_B,
        ).move_to(tree_box.get_center())
        tree = VGroup(tree_box, tree_label).move_to(RIGHT * 3.5 + UP * 0.6)

        flow_arrow = Arrow(
            int_box.get_right(),
            tree_box.get_left(),
            buff=0.1,
            color=GREY_A,
            stroke_width=2.5,
            tip_length=0.18,
        )

        int_caption = CleanText(
            "Continuous time → Discrete steps",
            font_size=20,
            color=GRAY_A,
        ).next_to(integrator, DOWN, buff=0.7)

        tree_caption = CleanText(
            "Group particles into a spatial tree",
            font_size=20,
            color=GRAY_A,
        ).next_to(tree, DOWN, buff=0.7)

        self.add(integrator, tree, flow_arrow, int_caption, tree_caption)
        self.wait(0.5)
        self.next_slide()
