from manim import *
from manim_slides import Slide


class DirectVsTree(Slide):
    def construct(self):
        heading = Text(
            "RQ1: Direct vs Tree — the real crossover",
            font_size=36,
            weight=BOLD,
        ).to_edge(UP, buff=0.6)
        self.play(Write(heading))
        self.next_slide()

        # Two-column comparison
        direct_title = Text("Direct  O(N²)", font_size=28, weight=BOLD, color=BLUE_B)
        direct_pts = VGroup(
            Text("✓  Faster runtime", font_size=22),
            Text("✗  Energy drift = 2.01  at N=100K", font_size=22, color=RED_B),
            Text("·  Coalesced, branch-free", font_size=20, color=GREY_B),
            Text("·  But 32-bit float bites at scale", font_size=20, color=GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        direct_block = VGroup(direct_title, direct_pts).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        direct_box = SurroundingRectangle(
            direct_block, color=BLUE_B, buff=0.3, corner_radius=0.1, stroke_width=2
        )
        direct_card = VGroup(direct_box, direct_block).move_to(LEFT * 3.4 + DOWN * 0.2)

        tree_title = Text("Tree  O(N log N)", font_size=28, weight=BOLD, color=GREEN_B)
        tree_pts = VGroup(
            Text("✗  Slower runtime (on M2)", font_size=22),
            Text("✓  Drift = 7.58×10⁻²  at N=100K", font_size=22, color=GREEN_B),
            Text("·  Traversal divergence on GPU", font_size=20, color=GREY_B),
            Text("·  Symmetric, bounded errors", font_size=20, color=GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        tree_block = VGroup(tree_title, tree_pts).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        tree_box = SurroundingRectangle(
            tree_block, color=GREEN_B, buff=0.3, corner_radius=0.1, stroke_width=2
        )
        tree_card = VGroup(tree_box, tree_block).move_to(RIGHT * 3.4 + DOWN * 0.2)

        self.play(FadeIn(direct_card, shift=RIGHT * 0.2))
        self.next_slide()
        self.play(FadeIn(tree_card, shift=LEFT * 0.2))
        self.next_slide()

        # headline ratio
        ratio = Text(
            "Tree drifts 26× less at N = 100 K",
            font_size=28,
            weight=BOLD,
            color=ORANGE,
        ).to_edge(DOWN, buff=0.9)
        ratio_box = SurroundingRectangle(ratio, color=ORANGE, buff=0.2, stroke_width=2)
        self.play(Write(ratio), Create(ratio_box))
        self.next_slide()

        # closing tagline
        tag = Text(
            "The crossover is accuracy, not runtime.",
            font_size=22,
            slant=ITALIC,
            color=YELLOW_B,
        ).to_edge(DOWN, buff=0.35)
        self.play(Write(tag))
        self.next_slide()
