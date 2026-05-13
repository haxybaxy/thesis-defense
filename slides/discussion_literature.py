from manim import *
from manim_slides import Slide


class LiteratureComparison(Slide):
    def construct(self):
        heading = Text(
            "How this compares to prior work",
            font_size=40,
            weight=BOLD,
        ).to_edge(UP, buff=0.6)
        self.play(Write(heading))
        self.next_slide()

        confirms_title = Text("Confirms", font_size=28, weight=BOLD, color=GREEN_B).move_to(
            LEFT * 3.5 + UP * 1.8
        )
        diverges_title = Text("Diverges", font_size=28, weight=BOLD, color=RED_B).move_to(
            RIGHT * 3.5 + UP * 1.8
        )
        self.play(Write(confirms_title), Write(diverges_title))
        self.next_slide()

        # confirms column
        confirms = [
            ("Maczan 2026", "1.5× backend spread"),
            ("Sengupta 2025", "1.4–2× browser overhead"),
            ("Nyland 2009", "GPU direct sum throughput"),
        ]
        confirms_block = VGroup()
        for paper, finding in confirms:
            p_t = Text(paper, font_size=20, weight=BOLD, color=GREEN_B)
            f_t = Text(finding, font_size=17, color=GREY_B)
            entry = VGroup(p_t, f_t).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
            confirms_block.add(entry)
        confirms_block.arrange(DOWN, aligned_edge=LEFT, buff=0.5).next_to(
            confirms_title, DOWN, buff=0.5
        ).align_to(confirms_title, LEFT).shift(LEFT * 0.7)

        diverges = [
            ("Gaburov 2010", "Tree build 15–25% there  ·  < 0.2% here"),
        ]
        diverges_block = VGroup()
        for paper, finding in diverges:
            p_t = Text(paper, font_size=20, weight=BOLD, color=RED_B)
            f_t = Text(finding, font_size=17, color=GREY_B)
            entry = VGroup(p_t, f_t).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
            diverges_block.add(entry)
        diverges_block.arrange(DOWN, aligned_edge=LEFT, buff=0.5).next_to(
            diverges_title, DOWN, buff=0.5
        ).align_to(diverges_title, LEFT).shift(LEFT * 0.7)

        for c in confirms_block:
            self.play(FadeIn(c, shift=RIGHT * 0.2), run_time=0.4)
        self.next_slide()

        for d in diverges_block:
            self.play(FadeIn(d, shift=LEFT * 0.2), run_time=0.4)
        self.next_slide()

        # reason for divergence
        reason = Text(
            "The difference is architectural — full GPU-residency,\nno per-step CPU↔GPU transfer.",
            font_size=18,
            slant=ITALIC,
            color=YELLOW_B,
        ).to_edge(DOWN, buff=0.5)
        self.play(Write(reason))
        self.next_slide()
