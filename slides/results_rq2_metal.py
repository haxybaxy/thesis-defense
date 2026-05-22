from manim import *
from manim_slides import Slide

from _text import CleanText


class WebGPUvsMetal(Slide):
    def construct(self):
        heading = CleanText(
            "RQ2: WebGPU vs native Metal",
            font_size=40,
            weight=BOLD,
        ).to_edge(UP, buff=0.6)
        self.add(heading)
        self.wait(0.1)
        self.next_slide()

        # Bar-chart-style comparison at 5 N values
        # (placeholder layout — real chart can replace with image later)
        N_vals = [
            ("N=1K",   "5.86",   "2.94", "2.0×",  RED_B),
            ("N=5K",   "7.35",  "10.09", "0.73×", GREEN_B),
            ("N=10K",  "11.00", "21.35", "0.52×", GREEN_B),
            ("N=50K",  "65.46", "121.77", "0.54×", GREEN_B),
            ("N=100K", "180.11", "516.78", "0.35×", GREEN_B),
        ]

        # column headers
        hdr_y = 1.8
        hdr_N = CleanText("N", font_size=20, weight=BOLD, color=GREY_C).move_to(LEFT * 5.0 + UP * hdr_y)
        hdr_w = CleanText("WebGPU (ms)", font_size=18, weight=BOLD, color=BLUE_B).move_to(
            LEFT * 2.0 + UP * hdr_y
        )
        hdr_m = CleanText("Metal (ms)", font_size=18, weight=BOLD, color=ORANGE).move_to(
            RIGHT * 1.0 + UP * hdr_y
        )
        hdr_r = CleanText("WebGPU / Metal", font_size=18, weight=BOLD, color=GREY_C).move_to(
            RIGHT * 4.2 + UP * hdr_y
        )
        self.add(hdr_N, hdr_w, hdr_m, hdr_r)
        self.wait(0.1)
        self.next_slide()

        # rows
        for i, (N, w, m, r, ratio_color) in enumerate(N_vals):
            y = 1.2 - i * 0.55
            N_t = CleanText(N, font_size=20).move_to(LEFT * 5.0 + UP * y)
            w_t = CleanText(w, font_size=20, color=BLUE_C).move_to(LEFT * 2.0 + UP * y)
            m_t = CleanText(m, font_size=20, color=ORANGE).move_to(RIGHT * 1.0 + UP * y)
            r_t = CleanText(r, font_size=22, weight=BOLD, color=ratio_color).move_to(
                RIGHT * 4.2 + UP * y
            )
            self.add(N_t, w_t, m_t, r_t)
        self.wait(0.1)
        self.next_slide()

        # headline
        tag = CleanText(
            "2.0× slower at N=1K  →  2.9× FASTER at N=100K",
            font_size=24,
            weight=BOLD,
            color=YELLOW_B,
        ).to_edge(DOWN, buff=0.8)
        self.add(tag)
        self.wait(0.1)
        self.next_slide()

        caveat = CleanText(
            "Implementation-level result — our pipeline is GPU-resident; UniSim has CPU↔GPU coordination.",
            font_size=14,
            slant=ITALIC,
            color=GREY_B,
        ).to_edge(DOWN, buff=0.3)
        self.add(caveat)
        self.wait(0.1)
        self.next_slide()
