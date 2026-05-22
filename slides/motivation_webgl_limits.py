from manim import *
from manim_slides import Slide

from _text import CleanText


class WebGLLimits(Slide):
    def construct(self):
        heading = CleanText(
            "Why this wasn't possible before WebGPU",
            font_size=36,
            weight=BOLD,
        ).to_edge(UP, buff=0.55)

        webgl_title = CleanText("WebGL", font_size=34, weight=BOLD, color=RED_B).move_to(
            LEFT * 3.7 + UP * 2.0
        )
        webgpu_title = CleanText(
            "WebGPU", font_size=34, weight=BOLD, color=GREEN_B
        ).move_to(RIGHT * 3.3 + UP * 2.0)
        webgl_logo = (
            SVGMobject("assets/WebGL_Logo.svg")
            .scale_to_fit_height(0.55)
            .next_to(webgl_title, RIGHT, buff=0.25)
        )
        webgpu_logo = (
            SVGMobject("assets/webgpu.svg")
            .scale_to_fit_height(0.55)
            .next_to(webgpu_title, LEFT, buff=0.25)
        )
        sub_webgl = CleanText(
            "graphics API", font_size=18, color=GREY_B, slant=ITALIC
        ).next_to(webgl_title, DOWN, buff=0.1)
        sub_webgpu = CleanText(
            "compute + graphics", font_size=18, color=GREEN_B, slant=ITALIC
        ).next_to(webgpu_title, DOWN, buff=0.1)

        webgl_items = [
            "graphics pipeline only",
            "data hidden in textures",
            "no atomics",
            "no workgroup memory",
            "no storage buffers",
            "had to fake compute",
        ]
        webgpu_items = [
            "compute shaders",
            "storage buffers",
            "atomic operations",
            "workgroup-shared memory",
            "real GPGPU",
        ]

        webgl_col = (
            VGroup(*[CleanText(f"✗  {t}", font_size=22, color=GREY_B) for t in webgl_items])
            .arrange(DOWN, aligned_edge=LEFT, buff=0.28)
            .next_to(sub_webgl, DOWN, buff=0.45)
            .shift(LEFT * 0.6)
        )
        webgpu_col = (
            VGroup(*[CleanText(f"✓  {t}", font_size=22, color=WHITE) for t in webgpu_items])
            .arrange(DOWN, aligned_edge=LEFT, buff=0.28)
            .next_to(sub_webgpu, DOWN, buff=0.45)
            .shift(LEFT * 0.6)
        )

        self.add(
            heading,
            webgl_title,
            webgpu_title,
            webgl_logo,
            webgpu_logo,
            sub_webgl,
            sub_webgpu,
            webgl_col,
            webgpu_col,
        )
        self.wait(0.5)
        self.next_slide()
