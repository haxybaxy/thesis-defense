from manim import *
from manim_slides import Slide


class CrossBackendVariation(Slide):
    def construct(self):
        heading = Text(
            "RQ2: Cross-backend variation",
            font_size=40,
            weight=BOLD,
        ).to_edge(UP, buff=0.6)
        self.play(Write(heading))
        self.next_slide()

        subhead = Text(
            "Four WebGPU implementations · same Metal backend · frozen-state protocol",
            font_size=18,
            slant=ITALIC,
            color=GREY_B,
        ).next_to(heading, DOWN, buff=0.3)
        self.play(FadeIn(subhead))
        self.next_slide()

        # table of backends with timings
        backends = [
            ("Dawn",         "1.40",   "8.54", "272.73",  BLUE_C),
            ("wgpu-native",  "5.86",  "11.00", "180.11",  GREEN_B),
            ("Chrome",       "4.87",  "17.81", "260.74",  YELLOW_B),
            ("Safari",       "9.52",  "20.97", "281.59",  RED_B),
        ]

        # headers
        hdr_y = 1.6
        cols_x = [LEFT * 5.0, LEFT * 2.0, ORIGIN[0], RIGHT * 3.0]
        col_labels = ["Backend", "N = 1 K", "N = 10 K", "N = 100 K"]
        hdr_objs = []
        for x_off, lbl in zip(cols_x, col_labels):
            t = Text(lbl, font_size=18, weight=BOLD, color=GREY_C)
            t.move_to([x_off if isinstance(x_off, float) else x_off[0], hdr_y, 0])
            hdr_objs.append(t)
        # the homemade x position trick — easier: just use point arithmetic
        hdr_g = VGroup()
        positions = [-5.0, -2.0, 0.5, 3.5]
        for x, lbl in zip(positions, col_labels):
            hdr_g.add(Text(lbl, font_size=18, weight=BOLD, color=GREY_C).move_to([x, hdr_y, 0]))
        self.play(FadeIn(hdr_g))
        self.next_slide()

        for i, (name, c1, c10, c100, color) in enumerate(backends):
            y = 1.0 - i * 0.55
            name_t = Text(name, font_size=20, weight=BOLD, color=color).move_to([-5.0, y, 0])
            c1_t = Text(c1, font_size=20).move_to([-2.0, y, 0])
            c10_t = Text(c10, font_size=20).move_to([0.5, y, 0])
            c100_t = Text(c100, font_size=22, weight=BOLD, color=color).move_to([3.5, y, 0])
            self.play(FadeIn(VGroup(name_t, c1_t, c10_t, c100_t), shift=UP * 0.1), run_time=0.3)
        self.next_slide()

        # headline
        tag = Text(
            "1.5× spread between fastest and slowest at N = 100 K",
            font_size=24,
            weight=BOLD,
            color=ORANGE,
        ).to_edge(DOWN, buff=0.8)
        tag_box = SurroundingRectangle(tag, color=ORANGE, buff=0.2, stroke_width=2)
        self.play(Write(tag), Create(tag_box))
        self.next_slide()

        note = Text(
            "Same hardware. Same shader. Different WebGPU implementation.",
            font_size=16,
            slant=ITALIC,
            color=GREY_B,
        ).to_edge(DOWN, buff=0.3)
        self.play(FadeIn(note))
        self.next_slide()
