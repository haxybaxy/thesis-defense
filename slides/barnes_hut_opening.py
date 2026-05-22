import math

from manim import *
from manim_slides import Slide


class BarnesHutOpening(Slide):
    def construct(self):
        opening_heading = Text(
            'When is a node "far enough"?',
            font_size=36,
            weight=BOLD,
        ).to_edge(UP, buff=0.5)
        self.add(opening_heading)

        p_dot = Dot(LEFT * 4.0 + UP * 0.3, radius=0.16, color=BLUE)
        p_label = MathTex("i", color=BLUE, font_size=30).next_to(p_dot, DOWN, buff=0.15)
        self.play(FadeIn(p_dot), Write(p_label))

        node_center = RIGHT * 2.5 + UP * 0.3
        node_size = 1.6
        aabb = Square(side_length=node_size, color=ORANGE, stroke_width=3).move_to(
            node_center
        )
        node_com = Dot(node_center, radius=0.08, color=ORANGE)
        self.play(Create(aabb), FadeIn(node_com))

        d_line = Line(p_dot.get_center(), node_center, color=WHITE, stroke_width=2)
        d_label = MathTex("d", font_size=32).next_to(d_line.get_center(), UP, buff=0.15)
        self.play(Create(d_line), Write(d_label))

        s_brace = Brace(aabb, UP, color=ORANGE)
        s_label = s_brace.get_tex("s")
        self.play(GrowFromCenter(s_brace), Write(s_label))

        top_corner = aabb.get_corner(UL)
        bot_corner = aabb.get_corner(DL)
        ray_top = DashedLine(
            p_dot.get_center(), top_corner, color=YELLOW, dash_length=0.1
        )
        ray_bot = DashedLine(
            p_dot.get_center(), bot_corner, color=YELLOW, dash_length=0.1
        )

        vertex = p_dot.get_center()
        v_top = top_corner - vertex
        v_bot = bot_corner - vertex
        angle_top = math.atan2(v_top[1], v_top[0])
        angle_bot = math.atan2(v_bot[1], v_bot[0])
        theta_arc = Arc(
            radius=0.9,
            start_angle=angle_bot,
            angle=angle_top - angle_bot,
            color=YELLOW,
            arc_center=vertex,
            stroke_width=4,
        )
        theta_label = MathTex(r"\theta", color=YELLOW, font_size=36).move_to(
            vertex + RIGHT * 0.9 + UP * 0.75
        )
        self.play(Create(ray_top), Create(ray_bot))
        self.play(Create(theta_arc), Write(theta_label))
        self.next_slide()

        test_eq = MathTex(
            r"\text{accept as monopole if}\quad \frac{s}{d} < ",
            r"\theta",
            font_size=40,
        ).to_edge(DOWN, buff=0.7)
        test_eq[1].set_color(YELLOW)
        self.play(Write(test_eq))
        self.next_slide()

        tradeoff = (
            VGroup(
                Text("small θ  →  accurate, slow", font_size=22, color=BLUE),
                Text("large θ  →  fast, less accurate", font_size=22, color=RED),
            )
            .arrange(DOWN, aligned_edge=LEFT, buff=0.15)
            .next_to(test_eq, UP, buff=0.4)
            .shift(LEFT * 3.5)
        )
        self.play(FadeIn(tradeoff, shift=UP * 0.2, lag_ratio=0.3))
        self.next_slide()
