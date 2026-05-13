from manim import *
from manim_slides import Slide


class GPUBarnesHutPriorWork(Slide):
    def construct(self):
        heading = Text(
            "GPU Barnes–Hut: prior work",
            font_size=40,
            weight=BOLD,
        ).to_edge(UP, buff=0.6)
        self.play(Write(heading))
        self.next_slide()

        # Three-row "table" — paper | hardware | headline result
        rows = [
            (
                "Nyland et al. 2009",
                "GPU Gems 3 / direct N²",
                "10–30 GFLOP/s",
                BLUE_B,
            ),
            (
                "Burtscher & Pingali 2011",
                "CUDA octree / GTX 280",
                "~10 ms at N = 100 k",
                YELLOW_B,
            ),
            (
                "Gaburov et al. 2010",
                "CUDA octree",
                "15–25% tree-build overhead",
                ORANGE,
            ),
        ]

        row_groups = VGroup()
        for paper, hardware, result, color in rows:
            paper_t = Text(paper, font_size=24, weight=BOLD, color=color)
            hw_t = Text(hardware, font_size=20, color=GREY_B)
            res_t = Text(result, font_size=22)

            paper_t.move_to(LEFT * 4.0)
            hw_t.move_to(LEFT * 0.6)
            res_t.move_to(RIGHT * 3.5)

            row = VGroup(paper_t, hw_t, res_t)
            row_groups.add(row)

        row_groups.arrange(DOWN, buff=0.55)
        row_groups.next_to(heading, DOWN, buff=0.8)

        # column headers
        hdr = VGroup(
            Text("Paper", font_size=20, weight=BOLD, color=GREY_C),
            Text("Hardware / Method", font_size=20, weight=BOLD, color=GREY_C),
            Text("Headline result", font_size=20, weight=BOLD, color=GREY_C),
        )
        hdr[0].move_to(LEFT * 4.0)
        hdr[1].move_to(LEFT * 0.6)
        hdr[2].move_to(RIGHT * 3.5)
        hdr.next_to(heading, DOWN, buff=0.4)
        self.play(FadeIn(hdr))
        self.next_slide()

        # animate each row
        for row in row_groups:
            self.play(FadeIn(row, shift=UP * 0.2), run_time=0.5)
            self.next_slide()

        # closing takeaway
        tag = Text(
            "GPU works. But tree construction is not free.",
            font_size=24,
            slant=ITALIC,
            color=GREEN_B,
        ).to_edge(DOWN, buff=0.6)
        self.play(Write(tag))
        self.next_slide()
