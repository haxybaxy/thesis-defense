from manim import *
from manim_slides import Slide


class WebGPUIntro(Slide):
    def construct(self):
        heading = Text(
            "What is WebGPU?",
            font_size=42,
            weight=BOLD,
        ).to_edge(UP, buff=0.6)
        self.play(Write(heading))
        self.next_slide()

        # placeholder for a WebGPU logo / hero asset
        logo_placeholder = Rectangle(
            width=1.4, height=0.7, color=GREY_C, stroke_width=1
        ).next_to(heading, RIGHT, buff=0.5)
        logo_label = Text("[WebGPU logo]", font_size=14, color=GREY_C).move_to(
            logo_placeholder.get_center()
        )
        self.add(logo_placeholder, logo_label)

        subhead = Text(
            "The W3C standard that finally exposed GPGPU in the browser",
            font_size=22,
            slant=ITALIC,
            color=GREY_B,
        ).next_to(heading, DOWN, buff=0.4)
        self.play(FadeIn(subhead))
        self.next_slide()

        # === Layered architecture diagram on the left ===
        layer_top = Rectangle(width=3.2, height=0.7, color=BLUE_B, stroke_width=2)
        layer_top_label = Text("Your code (C++ / WGSL)", font_size=20).move_to(
            layer_top.get_center()
        )
        top_group = VGroup(layer_top, layer_top_label)

        layer_mid = Rectangle(width=3.2, height=0.7, color=YELLOW_B, stroke_width=2)
        layer_mid_label = Text("WebGPU API", font_size=20, weight=BOLD).move_to(
            layer_mid.get_center()
        )
        mid_group = VGroup(layer_mid, layer_mid_label)

        backend_w = 0.95
        backend_h = 0.6
        vulkan = VGroup(
            Rectangle(width=backend_w, height=backend_h, color=GREY_B, stroke_width=1),
            Text("Vulkan", font_size=16),
        )
        metal = VGroup(
            Rectangle(width=backend_w, height=backend_h, color=GREY_B, stroke_width=1),
            Text("Metal", font_size=16),
        )
        d3d = VGroup(
            Rectangle(width=backend_w, height=backend_h, color=GREY_B, stroke_width=1),
            Text("D3D12", font_size=16),
        )
        backends = VGroup(vulkan, metal, d3d).arrange(RIGHT, buff=0.15)

        stack = VGroup(top_group, mid_group, backends).arrange(DOWN, buff=0.25)
        stack.move_to(LEFT * 3.2 + DOWN * 0.4)

        self.play(FadeIn(top_group, shift=DOWN * 0.2))
        self.play(FadeIn(mid_group, shift=DOWN * 0.2))
        self.play(FadeIn(backends, shift=DOWN * 0.2))
        self.next_slide()

        # === Right column: four capabilities ===
        caps_title = Text("New capabilities", font_size=24, weight=BOLD, color=GREEN_B)
        caps = VGroup(
            Text("• Compute shaders", font_size=22),
            Text("• Storage buffers", font_size=22),
            Text("• Atomic operations", font_size=22),
            Text("• Workgroup memory", font_size=22),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        caps_block = VGroup(caps_title, caps).arrange(DOWN, aligned_edge=LEFT, buff=0.4)
        caps_block.move_to(RIGHT * 2.6 + DOWN * 0.4)

        self.play(FadeIn(caps_title))
        for c in caps:
            self.play(FadeIn(c, shift=RIGHT * 0.2), run_time=0.3)
        self.next_slide()

        # closing tagline
        tag = Text(
            "Same code → desktop and browser",
            font_size=26,
            slant=ITALIC,
            color=BLUE_B,
        ).to_edge(DOWN, buff=0.5)
        self.play(Write(tag))
        self.next_slide()
