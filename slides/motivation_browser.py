from manim import *
from manim_slides import Slide


class BrowserGap(Slide):
    def construct(self):
        heading = Text(
            "The browser-accessibility gap",
            font_size=40,
            weight=BOLD,
        ).to_edge(UP, buff=0.6)
        self.play(Write(heading))
        self.next_slide()

        # === Two-column comparison ===
        col_y = 0.2
        webgl_title = Text("WebGL", font_size=34, weight=BOLD, color=RED_B).move_to(
            LEFT * 3.5 + UP * 2.0
        )
        webgpu_title = Text("WebGPU", font_size=34, weight=BOLD, color=GREEN_B).move_to(
            RIGHT * 3.5 + UP * 2.0
        )

        self.play(Write(webgl_title), Write(webgpu_title))
        self.next_slide()

        # Left column items (limitations)
        webgl_items = [
            "graphics pipeline only",
            "data hidden in textures",
            "no atomics",
            "no recursive trees",
            "had to fake N-body",
        ]
        webgpu_items = [
            "compute shaders",
            "storage buffers",
            "atomic operations",
            "workgroup memory",
            "actual GPGPU",
        ]

        webgl_col = VGroup(
            *[Text(f"✗  {t}", font_size=24, color=GREY_B) for t in webgl_items]
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35)
        webgl_col.next_to(webgl_title, DOWN, buff=0.5).align_to(webgl_title, LEFT).shift(LEFT * 1.0)

        webgpu_col = VGroup(
            *[Text(f"✓  {t}", font_size=24, color=WHITE) for t in webgpu_items]
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35)
        webgpu_col.next_to(webgpu_title, DOWN, buff=0.5).align_to(webgpu_title, LEFT).shift(LEFT * 1.0)

        # Animate WebGL side first (the limitations)
        for item in webgl_col:
            self.play(FadeIn(item, shift=RIGHT * 0.2), run_time=0.25)
        self.next_slide()

        # Then WebGPU side
        for item in webgpu_col:
            self.play(FadeIn(item, shift=RIGHT * 0.2), run_time=0.25)
        self.next_slide()

        # closing tagline
        tag = Text(
            "Same hardware. Exposed honestly.",
            font_size=26,
            slant=ITALIC,
            color=BLUE_B,
        ).to_edge(DOWN, buff=0.6)
        self.play(Write(tag))
        self.next_slide()
