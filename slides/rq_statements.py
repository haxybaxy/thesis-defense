from manim import *
from manim_slides import Slide

from _text import CleanText


def _build_rq_slide(scene, tag, title, lines, color):
    tag_text = CleanText(tag, font_size=84, weight=BOLD, color=color)
    em_dash = CleanText("—", font_size=52, color=GREY_B)
    title_text = CleanText(title, font_size=46, weight=BOLD)
    header = VGroup(tag_text, em_dash, title_text).arrange(
        RIGHT, buff=0.4, aligned_edge=DOWN
    )
    em_dash.set_y(title_text.get_center()[1])
    header.to_edge(UP, buff=1.4)

    underline = Line(
        header.get_corner(DL) + DOWN * 0.18 + RIGHT * 0.0,
        header.get_corner(DR) + DOWN * 0.18,
        color=color,
        stroke_width=2.5,
    )

    body = VGroup(
        *[CleanText(line, font_size=26, color=GREY_A) for line in lines]
    ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)

    max_w = 11.0
    if body.width > max_w:
        body.scale(max_w / body.width)

    body.next_to(underline, DOWN, buff=0.7).align_to(header, LEFT)

    scene.add(header, underline, body)
    scene.wait(0.1)
    scene.next_slide()


class RQ1Statement(Slide):
    def construct(self):
        _build_rq_slide(
            self,
            "RQ1",
            "Scalability",
            [
                "How does runtime per timestep scale with N for a WebGPU",
                "Barnes–Hut implementation, and where are the bottlenecks",
                "within the GPU pipeline?",
            ],
            BLUE_B,
        )


class RQ2Statement(Slide):
    def construct(self):
        _build_rq_slide(
            self,
            "RQ2",
            "Abstraction overhead",
            [
                "What performance cost does the WebGPU abstraction layer impose",
                "relative to Apple's native Metal, and how does this vary across",
                "WebGPU implementations (wgpu-native, Dawn, browser)?",
            ],
            YELLOW_B,
        )


class RQ3Statement(Slide):
    def construct(self):
        _build_rq_slide(
            self,
            "RQ3",
            "Browser feasibility",
            [
                "Can the same codebase, compiled to WebAssembly and running in",
                "a browser, achieve acceptable throughput and numerical",
                "consistency compared to native execution?",
            ],
            GREEN_B,
        )
