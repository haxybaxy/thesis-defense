from manim import *
from manim_slides import Slide


class PipelineOverview(Slide):
    """Roadmap shown right after Compute-Centric, before any deep dive.

    Same five-box visual language as `slides/pipeline.py` so the audience
    recognises the layout when the synthesis slide arrives later in the talk.
    No equations and no LBVH zoom-in — those belong to the synthesis.
    """

    def construct(self):
        heading = Text(
            "Inside one timestep",
            font_size=36,
            weight=BOLD,
        ).to_edge(UP, buff=0.5)
        sub = Text(
            "Five stages, all GPU compute",
            font_size=22,
            color=GRAY_A,
        ).next_to(heading, DOWN, buff=0.15)
        self.play(Write(heading), FadeIn(sub, shift=UP * 0.2))
        self.next_slide()

        stages = [
            ("½ Kick", BLUE),
            ("Drift", TEAL),
            ("Tree build", GREEN),
            ("Force eval", ORANGE),
            ("½ Kick", BLUE),
        ]

        boxes = VGroup()
        for i, (title, color) in enumerate(stages):
            box = (
                Rectangle(width=2.6, height=0.7, color=color, stroke_width=3)
                .set_fill(color, opacity=0.18)
                .move_to(UP * (2.0 - i * 1.0))
            )
            label = Text(title, font_size=22, color=color, weight=BOLD).move_to(
                box.get_center()
            )
            boxes.add(VGroup(box, label))

        arrows = VGroup()
        for i in range(len(stages) - 1):
            arrows.add(
                Arrow(
                    boxes[i][0].get_bottom(),
                    boxes[i + 1][0].get_top(),
                    buff=0.05,
                    color=GRAY_A,
                    stroke_width=2,
                    tip_length=0.15,
                )
            )

        self.play(
            LaggedStart(
                *[FadeIn(b, shift=RIGHT * 0.2) for b in boxes],
                lag_ratio=0.12,
            ),
            LaggedStart(
                *[GrowArrow(a) for a in arrows],
                lag_ratio=0.12,
            ),
            run_time=2.0,
        )
        self.next_slide()

        # Grouping label 1: the integrator — stages 1, 2, 5 (non-contiguous).
        # Sits on the left; dashed lines fan rightward into the three half-kick / drift boxes.
        integrator_label = Text(
            "the integrator",
            font_size=30,
            color=BLUE,
            weight=BOLD,
        ).move_to(LEFT * 4.5 + UP * 0.3)
        integrator_indices = [0, 1, 4]
        integrator_lines = VGroup(
            *[
                DashedLine(
                    integrator_label.get_right() + RIGHT * 0.1,
                    boxes[i][0].get_left(),
                    color=BLUE,
                    stroke_width=1.5,
                    dash_length=0.1,
                )
                for i in integrator_indices
            ]
        )
        self.play(
            Write(integrator_label),
            Create(integrator_lines, lag_ratio=0.2),
        )
        self.next_slide()

        # Grouping label 2: the Barnes-Hut tree — stages 3, 4 (contiguous).
        # Sits on the right; dashed lines fan leftward into the two middle boxes.
        # Positioned symmetrically with the integrator label on the left.
        tree_label = Text(
            "Barnes–Hut tree",
            font_size=30,
            color=GREEN,
            weight=BOLD,
        ).move_to(RIGHT * 4.5 + DOWN * 0.5)
        tree_indices = [2, 3]
        tree_lines = VGroup(
            *[
                DashedLine(
                    tree_label.get_left() + LEFT * 0.1,
                    boxes[i][0].get_right(),
                    color=GREEN,
                    stroke_width=1.5,
                    dash_length=0.1,
                )
                for i in tree_indices
            ]
        )
        self.play(
            Write(tree_label),
            Create(tree_lines, lag_ratio=0.2),
        )
        self.next_slide()

        caption = Text(
            "Tree first, then integrator, then everything together.",
            font_size=22,
            color=GRAY_A,
        ).to_edge(DOWN, buff=0.7)
        self.play(FadeIn(caption, shift=UP * 0.15))
        self.next_slide()
