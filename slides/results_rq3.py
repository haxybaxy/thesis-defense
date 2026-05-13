from manim import *
from manim_slides import Slide


class BrowserVsNative(Slide):
    def construct(self):
        heading = Text(
            "RQ3: Browser vs native",
            font_size=40,
            weight=BOLD,
        ).to_edge(UP, buff=0.6)
        self.play(Write(heading))
        self.next_slide()

        # table of overhead by N
        rows = [
            ("N = 1 K",   "5.86",  "4.87",  "0.8×", GREEN_B),
            ("N = 5 K",   "7.35", "14.34",  "2.0×", RED_B),
            ("N = 10 K", "11.00", "17.81",  "1.6×", YELLOW_B),
            ("N = 50 K", "65.46", "94.93",  "1.5×", YELLOW_B),
            ("N = 100 K","180.11","260.74", "1.4×", GREEN_B),
        ]

        positions = [-5.0, -2.0, 0.8, 4.0]
        hdr_y = 1.7
        col_labels = ["N", "Native (ms)", "Chrome (ms)", "Overhead"]
        hdr = VGroup()
        for x, lbl in zip(positions, col_labels):
            hdr.add(Text(lbl, font_size=18, weight=BOLD, color=GREY_C).move_to([x, hdr_y, 0]))
        self.play(FadeIn(hdr))
        self.next_slide()

        for i, (N, native, chrome, ov, color) in enumerate(rows):
            y = 1.1 - i * 0.55
            N_t = Text(N, font_size=20).move_to([positions[0], y, 0])
            n_t = Text(native, font_size=20, color=BLUE_C).move_to([positions[1], y, 0])
            c_t = Text(chrome, font_size=20, color=YELLOW_B).move_to([positions[2], y, 0])
            o_t = Text(ov, font_size=22, weight=BOLD, color=color).move_to([positions[3], y, 0])
            self.play(FadeIn(VGroup(N_t, n_t, c_t, o_t), shift=UP * 0.1), run_time=0.3)
        self.next_slide()

        # surprise at N=1K
        surprise = Text(
            "Chrome is actually faster at N = 1 K",
            font_size=20,
            slant=ITALIC,
            color=GREEN_B,
        ).to_edge(DOWN, buff=1.1)
        self.play(Write(surprise))
        self.next_slide()

        # headline
        tag = Text(
            "Overhead narrows to 1.4× at scientifically meaningful N",
            font_size=24,
            weight=BOLD,
            color=ORANGE,
        ).to_edge(DOWN, buff=0.5)
        self.play(Write(tag))
        self.next_slide()
