from manim import *
from manim_slides import Slide

from _text import CleanText


class ForceEvalConcept(Slide):
    def construct(self):
        block_w = 2.6
        block_h = 1.1

        integrator_box = RoundedRectangle(
            width=block_w,
            height=block_h,
            corner_radius=0.18,
            color=BLUE_B,
            stroke_width=3,
        ).set_fill(BLUE_B, opacity=0.22)
        integrator_label = CleanText(
            "Integrator",
            font_size=24,
            weight=BOLD,
            color=BLUE_B,
        ).move_to(integrator_box.get_center())
        integrator = VGroup(integrator_box, integrator_label).move_to(LEFT * 5 + UP * 0.6)

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
        tree = VGroup(tree_box, tree_label).move_to(UP * 0.6)

        force_box = RoundedRectangle(
            width=block_w,
            height=block_h,
            corner_radius=0.18,
            color=ORANGE,
            stroke_width=3,
        ).set_fill(ORANGE, opacity=0.22)
        force_label = CleanText(
            "Force eval",
            font_size=24,
            weight=BOLD,
            color=ORANGE,
        ).move_to(force_box.get_center())
        force = VGroup(force_box, force_label).move_to(RIGHT * 5 + UP * 0.6)

        integrator_arrow = Arrow(
            integrator_box.get_right(),
            tree_box.get_left(),
            buff=0.1,
            color=GREY_A,
            stroke_width=2.5,
            tip_length=0.18,
        )

        flow_arrow = Arrow(
            tree_box.get_right(),
            force_box.get_left(),
            buff=0.1,
            color=GREY_A,
            stroke_width=2.5,
            tip_length=0.18,
        )

        integrator_caption = CleanText(
            "Advance positions in time",
            font_size=20,
            color=GRAY_A,
        ).next_to(integrator, DOWN, buff=0.7)

        tree_caption = CleanText(
            "Group particles into a spatial tree",
            font_size=20,
            color=GRAY_A,
        ).next_to(tree, DOWN, buff=0.7)

        force_caption = CleanText(
            "Sum gravitational interactions",
            font_size=20,
            color=GRAY_A,
        ).next_to(force, DOWN, buff=0.7)

        self.add(
            integrator,
            tree,
            force,
            integrator_arrow,
            flow_arrow,
            integrator_caption,
            tree_caption,
            force_caption,
        )
        self.wait(0.5)
        self.next_slide()
