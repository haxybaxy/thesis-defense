from manim import *
from manim_slides import Slide


class Pipeline(Slide):
    def construct(self):
        heading = Text(
            "One timestep, end to end",
            font_size=36,
            weight=BOLD,
        ).to_edge(UP, buff=0.5)
        sub = Text(
            "Leapfrog (KDK) + LBVH, all on the GPU",
            font_size=22,
            color=GRAY_A,
        ).next_to(heading, DOWN, buff=0.15)
        self.play(Write(heading), FadeIn(sub, shift=UP * 0.2))
        self.next_slide()

        stages = [
            ("½ Kick", r"v \leftarrow v + \tfrac{1}{2}\, a \, \Delta t", BLUE),
            ("Drift", r"r \leftarrow r + v \, \Delta t", TEAL),
            ("LBVH Build", r"\text{6-pass tree construction}", GREEN),
            ("BVH Force", r"a \leftarrow F_{\mathrm{tree}} / m", ORANGE),
            ("½ Kick", r"v \leftarrow v + \tfrac{1}{2}\, a \, \Delta t", BLUE),
        ]

        boxes = VGroup()
        maths = VGroup()
        for i, (title, latex, color) in enumerate(stages):
            box = (
                Rectangle(width=2.6, height=0.7, color=color, stroke_width=3)
                .set_fill(color, opacity=0.18)
                .move_to(LEFT * 4 + UP * (2.0 - i * 1.0))
            )
            title_text = Text(
                title, font_size=22, color=color, weight=BOLD
            ).move_to(box.get_center())
            boxes.add(VGroup(box, title_text))

            math_eq = MathTex(latex, font_size=28).next_to(box, RIGHT, buff=0.5)
            maths.add(math_eq)

        arrows = VGroup()
        for i in range(len(stages) - 1):
            a = Arrow(
                boxes[i][0].get_bottom(),
                boxes[i + 1][0].get_top(),
                buff=0.05,
                color=GRAY_A,
                stroke_width=2,
                tip_length=0.15,
            )
            arrows.add(a)

        for i in range(len(stages)):
            anims = [FadeIn(boxes[i], shift=RIGHT * 0.2), FadeIn(maths[i])]
            if i > 0:
                anims.append(GrowArrow(arrows[i - 1]))
            self.play(*anims, run_time=0.5)
            self.next_slide()

        # === Expand the LBVH Build box ===
        lbvh_box = boxes[2][0]
        sub_passes = [
            "1. AABB reduce",
            "2. Morton codes",
            "3. Radix sort",
            "4. Karras topology",
            "5. Leaf init",
            "6. Aggregation",
        ]
        sub_boxes = VGroup()
        for i, name in enumerate(sub_passes):
            mini_box = (
                Rectangle(width=1.8, height=0.42, color=GREEN, stroke_width=1.5)
                .set_fill(GREEN, opacity=0.12)
            )
            mini_text = Text(name, font_size=15, color=GREEN).move_to(
                mini_box.get_center()
            )
            mini = VGroup(mini_box, mini_text).move_to(
                RIGHT * 3.8 + UP * (1.4 - i * 0.55)
            )
            sub_boxes.add(mini)

        zoom_arrow = Arrow(
            lbvh_box.get_right(),
            sub_boxes.get_left(),
            color=GREEN,
            stroke_width=3,
            buff=0.3,
            tip_length=0.2,
        )
        self.play(
            FadeOut(maths),
            GrowArrow(zoom_arrow),
            FadeIn(sub_boxes, lag_ratio=0.12),
            run_time=1.2,
        )
        self.next_slide()

        # === Closing: the WebGPU advantage ===
        self.play(
            FadeOut(boxes),
            FadeOut(arrows),
            FadeOut(sub_boxes),
            FadeOut(zoom_arrow),
            FadeOut(sub),
        )

        closing_heading = Text(
            "The WebGPU advantage",
            font_size=40,
            weight=BOLD,
            color=YELLOW,
        ).to_edge(UP, buff=0.5)
        self.play(Transform(heading, closing_heading))

        bullets = (
            VGroup(
                Text("• Fully GPU-resident — tree + integration", font_size=28),
                Text("• No per-step CPU ↔ GPU transfers", font_size=28),
                Text("• One command buffer per timestep", font_size=28),
                Text(
                    "• Same code: native desktop and browser",
                    font_size=28,
                    color=GREEN,
                ),
            )
            .arrange(DOWN, aligned_edge=LEFT, buff=0.45)
            .move_to(ORIGIN)
        )

        for b in bullets:
            self.play(FadeIn(b, shift=RIGHT * 0.2))
            self.next_slide()

        final_box = SurroundingRectangle(
            bullets[-1], color=GREEN, buff=0.2, stroke_width=4
        )
        self.play(Create(final_box))
        self.next_slide()

        self.next_slide(loop=True)
        self.play(final_box.animate.set_stroke(width=9), run_time=0.6)
        self.play(final_box.animate.set_stroke(width=4), run_time=0.6)
