import numpy as np
from manim import *
from manim_slides import Slide

from _text import CleanText


class ShaderVsCompute(Slide):
    """Dynamic visual contrast: graphics shader (a single triangle rides the
    pipeline, shatters into fragments, lands as red pixels) vs compute shader
    (threads fire in parallel, kernel formula swaps mid-slide, output buffer
    updates).

    Sits between WebGLLimits ('WebGPU adds compute') and ComputeShader101
    ('here's how a compute shader actually works'). Goal: make the
    'fixed assembly line' vs 'you decide what each thread does' contrast
    land animation-first, before ComputeShader101 deepens the thread /
    storage-buffer story.
    """

    def construct(self):
        # ============================================================
        # Static layout: build all mobjects up-front so the geometry
        # never shifts during the animation.
        # ============================================================
        heading = CleanText(
            "Graphics shader vs Compute shader",
            font_size=36,
            weight=BOLD,
        ).to_edge(UP, buff=0.5)

        vs_pill = CleanText("vs", font_size=24, slant=ITALIC, color=GREY_B).move_to(UP * 2.2)

        # ---------- LEFT column: graphics ----------
        g_title = CleanText(
            "Graphics shader",
            font_size=26,
            weight=BOLD,
            color=RED_B,
        ).move_to(LEFT * 3.6 + UP * 2.4)
        g_subtitle = CleanText(
            "draws an image",
            font_size=16,
            slant=ITALIC,
            color=RED_B,
        ).next_to(g_title, DOWN, buff=0.08)

        triangle_spawn = LEFT * 3.6 + UP * 1.35

        # Pipeline stage boxes
        stage_labels = ["Vertex shader", "Rasteriser", "Fragment shader"]
        g_stages = VGroup()
        for label in stage_labels:
            t = CleanText(label, font_size=13, color=GREY_B)
            box = SurroundingRectangle(
                t,
                color=RED_B,
                buff=0.12,
                corner_radius=0.06,
                stroke_width=1.2,
            ).set_fill("#2a1010", opacity=0.45)
            g_stages.add(VGroup(box, t))
        g_stages.arrange(DOWN, buff=0.18).move_to(LEFT * 3.6 + UP * 0.15)

        g_stage_arrows = VGroup()
        for i in range(len(g_stages) - 1):
            g_stage_arrows.add(
                Arrow(
                    g_stages[i].get_bottom(),
                    g_stages[i + 1].get_top(),
                    buff=0.04,
                    color=RED_B,
                    stroke_width=1.2,
                    tip_length=0.1,
                )
            )

        # Pixel grid (5x5) — starts entirely dim, lights up during conveyor
        pixel_rows, pixel_cols = 5, 5
        pixel_step = 0.18
        pixel_grid = VGroup()
        lit_positions: list[tuple[int, int]] = []
        for r in range(pixel_rows):
            for c in range(pixel_cols):
                px = Square(
                    side_length=0.16,
                    stroke_width=0.5,
                    color=GREY_C,
                )
                px.set_fill("#1a1a1a", opacity=0.35)
                px.move_to(
                    RIGHT * (c - (pixel_cols - 1) / 2) * pixel_step
                    + DOWN * (r - (pixel_rows - 1) / 2) * pixel_step
                )
                pixel_grid.add(px)
                # Lower-triangular silhouette: apex at (r=2, c=2) widening downward
                inside = (r >= pixel_rows - 1 - c) and (
                    r >= pixel_rows - 1 - (pixel_cols - 1 - c)
                )
                if inside:
                    lit_positions.append((r, c))
        pixel_grid.move_to(LEFT * 3.6 + DOWN * 1.95)
        g_out_label = CleanText("pixels", font_size=14, color=GREY_B).next_to(
            pixel_grid, DOWN, buff=0.1
        )

        lit_pixels = VGroup(
            *[pixel_grid[r * pixel_cols + c] for (r, c) in lit_positions]
        )

        # ---------- RIGHT column: compute ----------
        c_title = CleanText(
            "Compute shader",
            font_size=26,
            weight=BOLD,
            color=GREEN_B,
        ).move_to(RIGHT * 3.6 + UP * 2.4)
        c_subtitle = CleanText(
            "runs your program over data",
            font_size=16,
            slant=ITALIC,
            color=GREEN_B,
        ).next_to(c_title, DOWN, buff=0.08)

        # Buffer helper — returns (cells_group, value_group)
        def make_buffer(values, fill_color, fill_opacity=0.55, num_color=WHITE):
            cells = VGroup()
            nums = VGroup()
            for v in values:
                cell = Square(side_length=0.32, stroke_width=1.0, color=GREEN_B)
                cell.set_fill(fill_color, opacity=fill_opacity)
                cells.add(cell)
            cells.arrange(RIGHT, buff=0.0)
            for cell, v in zip(cells, values):
                num = CleanText(str(v), font_size=12, color=num_color).move_to(
                    cell.get_center()
                )
                nums.add(num)
            return cells, nums

        in_values = [3, 1, 4, 1, 5, 9]
        in_cells, in_nums = make_buffer(in_values, "#0e3a18", 0.55)
        in_buffer = VGroup(in_cells, in_nums).move_to(RIGHT * 3.6 + UP * 1.35)
        in_caption = CleanText("buffer in", font_size=12, color=GREY_B).next_to(
            in_buffer, DOWN, buff=0.06
        )

        # Kernel label between buffer and threads
        kernel_v1 = CleanText(
            "out[i] = in[i] * 2",
            font_size=16,
            color=GREEN_B,
            slant=ITALIC,
        ).move_to(RIGHT * 3.6 + UP * 0.55)
        kernel_v2 = CleanText(
            "out[i] = in[i] * i",
            font_size=16,
            color=GREEN_B,
            slant=ITALIC,
        ).move_to(kernel_v1.get_center())

        # Thread grid (2x6) — only top row will fire arrows, both rows pulse
        thread_palette = [BLUE_C, TEAL_C, GREEN_C, ORANGE]
        threads = VGroup()
        t_rows, t_cols = 2, 6
        for r in range(t_rows):
            for c in range(t_cols):
                sq = Square(side_length=0.32, stroke_width=1.0, color=GREY_A)
                sq.set_fill(thread_palette[(r + c) % 4], opacity=0.65)
                tid = CleanText(f"t{r * t_cols + c}", font_size=10, color=WHITE).move_to(
                    sq.get_center()
                )
                threads.add(VGroup(sq, tid))
        threads.arrange_in_grid(rows=t_rows, cols=t_cols, buff=0.05)
        threads.move_to(RIGHT * 3.6 + DOWN * 0.25)

        # Output buffer: cells start dim, no numbers yet
        out_cells = VGroup(
            *[
                Square(
                    side_length=0.32,
                    stroke_width=1.0,
                    color=GREEN_B,
                ).set_fill("#0e3a18", opacity=0.18)
                for _ in range(len(in_values))
            ]
        )
        out_cells.arrange(RIGHT, buff=0.0).move_to(RIGHT * 3.6 + DOWN * 1.5)
        out_caption = CleanText("buffer out", font_size=12, color=GREY_B).next_to(
            out_cells, DOWN, buff=0.06
        )

        # Pre-build the two sets of output values
        out_values_v1 = [in_values[i] * 2 for i in range(len(in_values))]
        out_values_v2 = [in_values[i] * i for i in range(len(in_values))]
        out_nums_v1 = VGroup(
            *[
                CleanText(str(v), font_size=12, color=WHITE).move_to(
                    out_cells[i].get_center()
                )
                for i, v in enumerate(out_values_v1)
            ]
        )
        out_nums_v2 = VGroup(
            *[
                CleanText(str(v), font_size=12, color=WHITE).move_to(
                    out_cells[i].get_center()
                )
                for i, v in enumerate(out_values_v2)
            ]
        )

        # Write arrows from top-row threads to output cells (1:1, hidden initially)
        write_arrows = VGroup()
        for i in range(t_cols):
            arrow = Arrow(
                threads[i].get_bottom(),
                out_cells[i].get_top(),
                buff=0.04,
                color=GREEN_C,
                stroke_width=1.2,
                tip_length=0.1,
            )
            write_arrows.add(arrow)

        # ============================================================
        # BEAT 1 — heading
        # ============================================================
        self.add(heading)
        self.add(
            g_title,
            g_subtitle,
            c_title,
            c_subtitle,
            vs_pill,
        )
        self.next_slide()

        # ============================================================
        # BEAT 3 — build the infrastructure (no activity yet)
        # ============================================================
        self.play(
            # Graphics side
            LaggedStart(*[FadeIn(b) for b in g_stages], lag_ratio=0.1),
            LaggedStart(*[GrowArrow(a) for a in g_stage_arrows], lag_ratio=0.15),
            FadeIn(pixel_grid),
            FadeIn(g_out_label),
            # Compute side
            FadeIn(in_buffer),
            FadeIn(in_caption),
            Write(kernel_v1),
            FadeIn(threads),
            FadeIn(out_cells),
            FadeIn(out_caption),
            run_time=1.6,
        )
        self.next_slide()

        # ============================================================
        # BEAT 4 — GRAPHICS conveyor: one triangle through the pipeline
        # ============================================================
        triangle = (
            Polygon(
                LEFT * 0.42 + DOWN * 0.28,
                RIGHT * 0.42 + DOWN * 0.28,
                UP * 0.38,
                color=RED_B,
                stroke_width=2,
            )
            .set_fill("#3a1414", opacity=0.75)
            .move_to(triangle_spawn)
        )
        in_label_g = CleanText(
            "vertices",
            font_size=12,
            slant=ITALIC,
            color=GREY_B,
        ).next_to(triangle, RIGHT, buff=0.15)

        self.play(
            FadeIn(triangle, scale=1.15),
            FadeIn(in_label_g),
            run_time=0.5,
        )

        # 1. Triangle slides into Vertex shader
        self.play(
            triangle.animate.move_to(g_stages[0].get_center()).scale(0.5),
            FadeOut(in_label_g),
            Indicate(g_stages[0], color=RED_B, scale_factor=1.08),
            run_time=0.7,
        )
        # 2. Triangle slides into Rasteriser
        self.play(
            triangle.animate.move_to(g_stages[1].get_center()),
            run_time=0.45,
        )

        # 3. SHATTER into fragment dots clustered around rasteriser
        num_frags = len(lit_positions)  # 9
        ras_center = g_stages[1].get_center()
        cluster_radius = 0.20
        fragment_positions = [
            ras_center
            + cluster_radius
            * np.array(
                [
                    np.cos(2 * np.pi * i / num_frags),
                    np.sin(2 * np.pi * i / num_frags),
                    0.0,
                ]
            )
            for i in range(num_frags)
        ]
        fragments = VGroup(
            *[
                Dot(radius=0.055, color=GREY_C, fill_opacity=0.9).move_to(p)
                for p in fragment_positions
            ]
        )
        self.play(
            ReplacementTransform(triangle, fragments),
            Indicate(g_stages[1], color=RED_B, scale_factor=1.08),
            run_time=0.55,
        )

        # 4. Fragments slide into Fragment shader (regroup around its centre)
        frag_center = g_stages[2].get_center()
        self.play(
            AnimationGroup(
                *[
                    f.animate.move_to(
                        frag_center
                        + cluster_radius
                        * np.array(
                            [
                                np.cos(2 * np.pi * i / num_frags),
                                np.sin(2 * np.pi * i / num_frags),
                                0.0,
                            ]
                        )
                    )
                    for i, f in enumerate(fragments)
                ]
            ),
            run_time=0.55,
        )
        # 5. Fragments get coloured red
        self.play(
            AnimationGroup(
                *[
                    f.animate.set_fill(RED_B, opacity=0.95).set_stroke(RED_B, width=0.5)
                    for f in fragments
                ]
            ),
            Indicate(g_stages[2], color=RED_B, scale_factor=1.08),
            run_time=0.45,
        )
        # 6. Fragments fly to their target pixel positions; pixels light up red
        self.play(
            AnimationGroup(
                *[
                    f.animate.move_to(p.get_center()).scale(0.6)
                    for f, p in zip(fragments, lit_pixels)
                ]
            ),
            AnimationGroup(
                *[
                    p.animate.set_fill(RED_B, opacity=0.7).set_stroke(RED_B, width=0.8)
                    for p in lit_pixels
                ]
            ),
            run_time=0.8,
        )
        self.play(FadeOut(fragments, run_time=0.3))

        # ============================================================
        # BEAT 6 — COMPUTE: parallel pulse + write (v1)
        # ============================================================
        self.next_slide()
        # All threads pulse simultaneously
        self.play(
            LaggedStart(
                *[Indicate(t, color=YELLOW, scale_factor=1.18) for t in threads],
                lag_ratio=0.02,
            ),
            run_time=0.9,
        )
        # Fire write arrows + fill output cells with v1 values
        self.play(
            LaggedStart(*[GrowArrow(a) for a in write_arrows], lag_ratio=0.04),
            run_time=0.7,
        )
        self.play(
            AnimationGroup(
                *[c.animate.set_fill("#0e3a18", opacity=0.55) for c in out_cells]
            ),
            LaggedStart(
                *[FadeIn(n, scale=0.7) for n in out_nums_v1],
                lag_ratio=0.04,
            ),
            run_time=0.7,
        )
        self.next_slide()
