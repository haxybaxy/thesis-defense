import math
import random

import numpy as np
from manim import *
from manim_slides import Slide


class BarnesHutIdea(Slide):
    def construct(self):
        random.seed(7)

        # === Distant cluster collapses to its centre of mass ===
        heading = Text(
            "The Barnes–Hut idea",
            font_size=40,
            weight=BOLD,
        ).to_edge(UP, buff=0.5)
        self.play(Write(heading))
        self.next_slide()

        observer = Dot(LEFT * 4.5, radius=0.18, color=BLUE)
        observer_label = MathTex("i", color=BLUE, font_size=32).next_to(
            observer, DOWN, buff=0.2
        )
        self.play(FadeIn(observer), Write(observer_label))

        cluster_center = RIGHT * 2.5 + UP * 0.3
        cluster_dots = []
        for _ in range(10):
            offset = np.array(
                [random.uniform(-0.7, 0.7), random.uniform(-0.7, 0.7), 0.0]
            )
            cluster_dots.append(Dot(cluster_center + offset, radius=0.10, color=ORANGE))
        cluster = VGroup(*cluster_dots)
        self.play(LaggedStart(*[FadeIn(d, scale=0.5) for d in cluster], lag_ratio=0.05))
        self.next_slide()

        force_arrows = VGroup(
            *[
                Arrow(
                    d.get_center(),
                    observer.get_center(),
                    buff=0.22,
                    color=YELLOW,
                    stroke_width=2.5,
                    tip_length=0.15,
                )
                for d in cluster
            ]
        )
        self.play(LaggedStart(*[GrowArrow(a) for a in force_arrows], lag_ratio=0.1))
        self.next_slide()

        com_dot = Dot(cluster_center, radius=0.26, color=ORANGE)
        com_label = MathTex(r"(M,\, \vec{R})", color=ORANGE, font_size=36).next_to(
            com_dot, UP, buff=0.3
        )
        single_force = Arrow(
            cluster_center,
            observer.get_center(),
            buff=0.34,
            color=YELLOW,
            stroke_width=7,
            tip_length=0.28,
        )

        self.play(
            Transform(cluster, com_dot),
            Transform(force_arrows, single_force),
            FadeIn(com_label),
            run_time=1.5,
        )
        self.next_slide()

        # === Monopole acceleration ===
        accel_eq = MathTex(
            r"\vec{a}_{i,\,\mathrm{node}} = G \, M \, "
            r"\frac{\vec{R} - \vec{r}_i}"
            r"{\bigl( \lvert \vec{R} - \vec{r}_i \rvert^2 + ",
            r"\varepsilon^2",
            r"\bigr)^{3/2}}",
            font_size=42,
        ).to_edge(DOWN, buff=0.9)
        accel_eq[1].set_color(GREEN)
        self.play(Write(accel_eq))
        self.next_slide()

        soft_label = Text(
            "Plummer softening: smooths the 1/r² singularity",
            font_size=22,
            color=GREEN,
        ).to_edge(DOWN, buff=0.25)
        soft_arrow = Arrow(
            soft_label.get_top(),
            accel_eq[1].get_bottom(),
            color=GREEN,
            buff=0.05,
            stroke_width=3,
            tip_length=0.15,
        )
        self.play(FadeIn(soft_label, shift=UP * 0.2), GrowArrow(soft_arrow))
        self.next_slide()

        # === Opening criterion (paper Fig 1) ===
        self.play(
            FadeOut(cluster),
            FadeOut(force_arrows),
            FadeOut(com_label),
            FadeOut(observer),
            FadeOut(observer_label),
            FadeOut(accel_eq),
            FadeOut(soft_label),
            FadeOut(soft_arrow),
        )

        opening_heading = Text(
            'When is a node "far enough"?',
            font_size=36,
            weight=BOLD,
        ).to_edge(UP, buff=0.5)
        self.play(Transform(heading, opening_heading))

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
        self.next_slide()

        d_line = Line(
            p_dot.get_center(), node_center, color=WHITE, stroke_width=2
        )
        d_label = MathTex("d", font_size=32).next_to(
            d_line.get_center(), UP, buff=0.15
        )
        self.play(Create(d_line), Write(d_label))
        self.next_slide()

        s_brace = Brace(aabb, UP, color=ORANGE)
        s_label = s_brace.get_tex("s")
        self.play(GrowFromCenter(s_brace), Write(s_label))
        self.next_slide()

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
            vertex + RIGHT * 1.2 + UP * 0.05
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

        # === Octree vs BVH ===
        self.play(
            *[
                FadeOut(m)
                for m in [
                    p_dot,
                    p_label,
                    aabb,
                    node_com,
                    d_line,
                    d_label,
                    s_brace,
                    s_label,
                    ray_top,
                    ray_bot,
                    theta_arc,
                    theta_label,
                    test_eq,
                    tradeoff,
                ]
            ]
        )

        vs_heading = Text(
            "Octree vs BVH on the GPU", font_size=36, weight=BOLD
        ).to_edge(UP, buff=0.5)
        self.play(Transform(heading, vs_heading))

        # Left: a 2D "quadtree" stand-in for the octree
        oct_title = Text("Octree (quadtree in 2D)", font_size=24, color=RED).move_to(
            LEFT * 3.5 + UP * 2.4
        )
        oct_outer = Square(side_length=2.4, color=RED, stroke_width=3).move_to(
            LEFT * 3.5 + UP * 0.7
        )
        oct_subs = VGroup()
        for dx in (-0.6, 0.6):
            for dy in (-0.6, 0.6):
                sub = Square(side_length=1.2, color=RED, stroke_width=2).move_to(
                    LEFT * 3.5 + UP * 0.7 + RIGHT * dx + UP * dy
                )
                oct_subs.add(sub)

        oct_bullets = (
            VGroup(
                Text("• 8 children per node", font_size=20),
                Text("• many empty cells", font_size=20),
                Text("• serial top-down build", font_size=20, color=RED),
            )
            .arrange(DOWN, aligned_edge=LEFT, buff=0.18)
            .next_to(oct_outer, DOWN, buff=0.5)
        )

        # Right: a small binary BVH
        bvh_title = Text("BVH (binary)", font_size=24, color=GREEN).move_to(
            RIGHT * 3.5 + UP * 2.4
        )
        root = Square(side_length=0.5, color=GREEN, stroke_width=3).move_to(
            RIGHT * 3.5 + UP * 1.7
        )
        l1 = Square(side_length=0.5, color=GREEN, stroke_width=3).move_to(
            RIGHT * 2.7 + UP * 0.7
        )
        r1 = Square(side_length=0.5, color=GREEN, stroke_width=3).move_to(
            RIGHT * 4.3 + UP * 0.7
        )
        leaves = VGroup(
            *[
                Square(side_length=0.4, color=GREEN, stroke_width=2).move_to(
                    RIGHT * x + DOWN * 0.3
                )
                for x in (2.3, 3.1, 3.9, 4.7)
            ]
        )
        edges = VGroup(
            Line(root.get_bottom(), l1.get_top(), color=GREEN),
            Line(root.get_bottom(), r1.get_top(), color=GREEN),
            Line(l1.get_bottom(), leaves[0].get_top(), color=GREEN),
            Line(l1.get_bottom(), leaves[1].get_top(), color=GREEN),
            Line(r1.get_bottom(), leaves[2].get_top(), color=GREEN),
            Line(r1.get_bottom(), leaves[3].get_top(), color=GREEN),
        )
        bvh_tree = VGroup(root, l1, r1, leaves, edges)

        bvh_bullets = (
            VGroup(
                Text("• exactly 2 children", font_size=20, color=GREEN),
                Text("• fixed 2N−1 nodes", font_size=20, color=GREEN),
                Text("• parallel bottom-up build", font_size=20, color=GREEN),
            )
            .arrange(DOWN, aligned_edge=LEFT, buff=0.18)
            .next_to(bvh_tree, DOWN, buff=0.5)
        )

        self.play(Write(oct_title), Write(bvh_title))
        self.play(Create(oct_outer), Create(oct_subs), Create(bvh_tree))
        self.next_slide()
        self.play(
            FadeIn(oct_bullets, lag_ratio=0.2),
            FadeIn(bvh_bullets, lag_ratio=0.2),
        )
        self.next_slide()
