from manim import *
from manim_slides import Slide

from _text import CleanText


class CrossBackendVariation(Slide):
    def construct(self):
        heading = CleanText(
            "RQ2: Cross-backend variation",
            font_size=40,
            weight=BOLD,
        ).to_edge(UP, buff=0.6)
        self.add(heading)

        maczan_citation_text = CleanText(
            "Maczan, 2026",
            font_size=18,
            color=GREY_B,
            slant=ITALIC,
        )
        maczan_citation_box = SurroundingRectangle(
            maczan_citation_text,
            color=GREY_B,
            buff=0.12,
            corner_radius=0.06,
            stroke_width=1.2,
        ).set_fill(BLACK, opacity=0.35)
        maczan_citation = VGroup(maczan_citation_box, maczan_citation_text).to_corner(
            DL, buff=0.35
        )
        self.add(maczan_citation)

        self.wait(0.1)
        self.next_slide()

        subhead = CleanText(
            "Four WebGPU implementations · same Metal backend · frozen-state protocol",
            font_size=18,
            slant=ITALIC,
            color=GREY_B,
        ).next_to(heading, DOWN, buff=0.3)
        self.add(subhead)
        self.wait(0.1)
        self.next_slide()

        # table of backends with timings (and brand logos)
        backends = [
            ("Dawn", "1.40", "8.54", "272.73", BLUE_C, "assets/dawn-logo.png", False),
            (
                "wgpu-native",
                "5.86",
                "11.00",
                "180.11",
                GREEN_B,
                "assets/webgpu.svg",
                True,
            ),
            (
                "Chrome",
                "4.87",
                "17.81",
                "260.74",
                YELLOW_B,
                "assets/chrome-logo.svg",
                True,
            ),
            (
                "Safari",
                "9.52",
                "20.97",
                "281.59",
                RED_B,
                "assets/safari-icon.svg",
                True,
            ),
        ]

        # headers
        hdr_y = 1.6
        cols_x = [LEFT * 5.0, LEFT * 2.0, ORIGIN[0], RIGHT * 3.0]
        col_labels = ["Backend", "N = 1 K", "N = 10 K", "N = 100 K"]
        hdr_objs = []
        for x_off, lbl in zip(cols_x, col_labels):
            t = CleanText(lbl, font_size=18, weight=BOLD, color=GREY_C)
            t.move_to([x_off if isinstance(x_off, float) else x_off[0], hdr_y, 0])
            hdr_objs.append(t)
        # the homemade x position trick — easier: just use point arithmetic
        hdr_g = VGroup()
        positions = [-5.0, -2.0, 0.5, 3.5]
        for x, lbl in zip(positions, col_labels):
            hdr_g.add(
                CleanText(lbl, font_size=18, weight=BOLD, color=GREY_C).move_to(
                    [x, hdr_y, 0]
                )
            )
        self.add(hdr_g)
        self.wait(0.1)

        for i, (name, c1, c10, c100, color, logo_path, is_svg) in enumerate(backends):
            y = 1.0 - i * 0.55
            if is_svg:
                logo = SVGMobject(logo_path).scale_to_fit_height(0.38)
            else:
                logo = ImageMobject(logo_path).scale_to_fit_height(0.38)
            logo.move_to([-5.8, y, 0])
            name_t = CleanText(name, font_size=20, weight=BOLD, color=color).move_to(
                [-4.6, y, 0]
            )
            c1_t = CleanText(c1, font_size=20).move_to([-2.0, y, 0])
            c10_t = CleanText(c10, font_size=20).move_to([0.5, y, 0])
            c100_t = CleanText(c100, font_size=22, weight=BOLD, color=color).move_to(
                [3.5, y, 0]
            )
            self.add(logo, name_t, c1_t, c10_t, c100_t)

        # headline
        tag = CleanText(
            "1.5× spread between fastest and slowest at N = 100 K",
            font_size=24,
            weight=BOLD,
            color=ORANGE,
        ).to_edge(DOWN, buff=0.8)
        tag_box = SurroundingRectangle(tag, color=ORANGE, buff=0.2, stroke_width=2)
        self.add(tag, tag_box)

        self.wait(0.1)
        self.next_slide()
