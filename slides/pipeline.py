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

        stages = [
            ("½ Kick", BLUE),
            ("Drift", TEAL),
            ("LBVH Build", GREEN),
            ("BVH Force", ORANGE),
            ("½ Kick", BLUE),
        ]

        boxes = VGroup()
        for i, (title, color) in enumerate(stages):
            box = (
                Rectangle(width=2.6, height=0.7, color=color, stroke_width=3)
                .set_fill(color, opacity=0.18)
                .move_to(UP * (2.0 - i * 1.0))
            )
            title_text = Text(
                title, font_size=22, color=color, weight=BOLD
            ).move_to(box.get_center())
            boxes.add(VGroup(box, title_text))

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

        pipeline_group = VGroup(boxes, arrows).shift(LEFT * 3)

        # KDK braces — kick · drift · kick structure on the far left
        kick0_brace = Brace(boxes[0][0], direction=LEFT, color=BLUE, buff=0.18)
        kick0_label = Text("kick · v at n+½", font_size=16, color=BLUE).next_to(
            kick0_brace, LEFT, buff=0.1
        )
        drift_brace = Brace(boxes[1][0], direction=LEFT, color=TEAL, buff=0.18)
        drift_label = Text("drift · r at n+1", font_size=16, color=TEAL).next_to(
            drift_brace, LEFT, buff=0.1
        )
        kick1_brace = Brace(boxes[4][0], direction=LEFT, color=BLUE, buff=0.18)
        kick1_label = Text("kick · v at n+1", font_size=16, color=BLUE).next_to(
            kick1_brace, LEFT, buff=0.1
        )

        # LBVH 6-pass detail column on the right
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
                Rectangle(width=1.9, height=0.42, color=GREEN, stroke_width=1.5)
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

        self.add(
            heading,
            sub,
            pipeline_group,
            kick0_brace,
            kick0_label,
            drift_brace,
            drift_label,
            kick1_brace,
            kick1_label,
            sub_boxes,
            zoom_arrow,
        )
        self.wait(0.1)
        self.next_slide()
