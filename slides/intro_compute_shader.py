from manim import *
from manim_slides import Slide


class ComputeShader101(Slide):
    """Define 'compute shader' intuitively, before §2 leans on the term.

    Sits between WebGLLimits ('what changed') and ComputeCentric
    ('and that's why the simulation is mostly compute'). Three beats:
    (a) graphics pipeline vs compute shader visual contrast,
    (b) thread fan-out into a storage buffer,
    (c) three tie-back examples (particle / tree node / timestep).

    Style intentionally matches `motivation_browser.py` (side-by-side
    panels, chip-style labels) and `pipeline_overview.py` (BLUE/TEAL/
    GREEN/ORANGE compute-stage colours).
    """

    def construct(self):
        heading = Text(
            "What is a compute shader?",
            font_size=36,
            weight=BOLD,
        ).to_edge(UP, buff=0.5)
        self.play(Write(heading))
        self.next_slide()

        # === Left: graphics shader pipeline (dimmed, "shape locked") ===
        graphics_title = Text(
            "Graphics shader pipeline",
            font_size=24,
            weight=BOLD,
            color=GRAY_B,
        ).move_to(LEFT * 3.6 + UP * 1.9)

        graphics_stages = [
            ("Vertices", GRAY_B),
            ("Vertex shader", GRAY_B),
            ("Rasteriser", GRAY_B),
            ("Fragment shader", GRAY_B),
            ("Pixels", GRAY_B),
        ]
        graphics_boxes = VGroup()
        for label, color in graphics_stages:
            t = Text(label, font_size=18, color=color)
            box = SurroundingRectangle(
                t,
                color=color,
                buff=0.12,
                corner_radius=0.06,
                stroke_width=1.2,
            ).set_fill("#1c1c1c", opacity=0.4)
            graphics_boxes.add(VGroup(box, t))
        graphics_boxes.arrange(DOWN, buff=0.18).next_to(
            graphics_title, DOWN, buff=0.35
        )

        graphics_arrows = VGroup()
        for i in range(len(graphics_stages) - 1):
            graphics_arrows.add(
                Arrow(
                    graphics_boxes[i][0].get_bottom(),
                    graphics_boxes[i + 1][0].get_top(),
                    buff=0.04,
                    color=GRAY_C,
                    stroke_width=1.5,
                    tip_length=0.12,
                )
            )

        graphics_caption = Text(
            "shape locked: input → pixels",
            font_size=16,
            slant=ITALIC,
            color=GRAY_C,
        ).next_to(graphics_boxes, DOWN, buff=0.3)

        # === Right: compute shader (threads → storage buffer) ===
        compute_title = Text(
            "Compute shader",
            font_size=24,
            weight=BOLD,
            color=GREEN_B,
        ).move_to(RIGHT * 3.6 + UP * 1.9)

        # 4x8 grid of thread squares — each labelled tid
        thread_colors = [BLUE_C, TEAL_C, GREEN_C, ORANGE]
        threads = VGroup()
        rows, cols = 4, 8
        for r in range(rows):
            for c in range(cols):
                sq = Square(side_length=0.22, stroke_width=1.0, color=GREY_A)
                sq.set_fill(thread_colors[(r + c) % 4], opacity=0.6)
                sq.move_to(
                    RIGHT * (2.4 + c * 0.26) + UP * (1.3 - r * 0.26)
                )
                threads.add(sq)

        tid_label = Text(
            "thousands of threads",
            font_size=14,
            slant=ITALIC,
            color=GREY_B,
        ).next_to(threads, UP, buff=0.12)

        # Storage buffer — horizontal rectangle below the threads
        buffer_rect = Rectangle(
            width=4.6,
            height=0.55,
            color=GREEN_B,
            stroke_width=2,
        ).set_fill("#0e3a18", opacity=0.45)
        buffer_rect.next_to(threads, DOWN, buff=0.7).shift(LEFT * 0.05)
        buffer_label = Text(
            "GPU memory (storage buffer)",
            font_size=15,
            color=GREEN_B,
            weight=BOLD,
        ).move_to(buffer_rect.get_center())

        # Sample arrows from a subset of threads down into the buffer
        sample_indices = [2, 7, 12, 19, 24, 30]
        thread_arrows = VGroup()
        for idx in sample_indices:
            thread_arrows.add(
                Arrow(
                    threads[idx].get_bottom(),
                    buffer_rect.get_top() + RIGHT * ((idx % cols - 3.5) * 0.4),
                    buff=0.05,
                    color=GREEN_C,
                    stroke_width=1.2,
                    tip_length=0.1,
                )
            )

        compute_caption = Text(
            "you choose what each thread does, and where it reads/writes",
            font_size=15,
            slant=ITALIC,
            color=GREEN_B,
        ).next_to(buffer_rect, DOWN, buff=0.3)

        # Reveal: graphics first, then compute side-by-side
        self.play(
            Write(graphics_title),
            LaggedStart(
                *[FadeIn(b) for b in graphics_boxes],
                lag_ratio=0.1,
            ),
            LaggedStart(
                *[GrowArrow(a) for a in graphics_arrows],
                lag_ratio=0.1,
            ),
            FadeIn(graphics_caption),
            run_time=1.8,
        )
        self.next_slide()

        self.play(
            Write(compute_title),
            FadeIn(tid_label),
            LaggedStart(
                *[FadeIn(t, scale=0.6) for t in threads],
                lag_ratio=0.02,
            ),
            run_time=1.2,
        )
        self.play(
            Create(buffer_rect),
            Write(buffer_label),
            LaggedStart(
                *[GrowArrow(a) for a in thread_arrows],
                lag_ratio=0.06,
            ),
            FadeIn(compute_caption),
            run_time=1.4,
        )
        self.next_slide()

        # === Bottom strip: three tie-back examples ===
        examples = [
            ("One thread per particle → update position", BLUE_C),
            ("One thread per tree node → aggregate centre of mass", GREEN_C),
            ("One thread per timestep → kick velocity", ORANGE),
        ]
        example_chips = VGroup()
        for label, color in examples:
            t = Text(label, font_size=16, color=color)
            box = SurroundingRectangle(
                t,
                color=color,
                buff=0.13,
                corner_radius=0.08,
                stroke_width=1.4,
            ).set_fill(color, opacity=0.18)
            example_chips.add(VGroup(box, t))
        example_chips.arrange(DOWN, buff=0.15).to_edge(DOWN, buff=0.55)

        closing = Text(
            "In this thesis, every box in the pipeline is one of these.",
            font_size=18,
            slant=ITALIC,
            weight=BOLD,
            color=WHITE,
        ).next_to(example_chips, UP, buff=0.25)

        # Dim the upper content so the bottom strip carries the eye
        upper_group = VGroup(
            graphics_title,
            graphics_boxes,
            graphics_arrows,
            graphics_caption,
            compute_title,
            tid_label,
            threads,
            buffer_rect,
            buffer_label,
            thread_arrows,
            compute_caption,
        )
        self.play(
            upper_group.animate.set_opacity(0.35),
            LaggedStart(
                *[FadeIn(c, shift=UP * 0.15) for c in example_chips],
                lag_ratio=0.15,
            ),
            run_time=1.4,
        )
        self.play(Write(closing))
        self.next_slide()
