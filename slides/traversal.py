from manim import *
from manim_slides import Slide

from _text import CleanText


class LBVHTraversal(Slide):
    def construct(self):
        heading = CleanText(
            "BVH Traversal with Barnes-Hutt",
            font_size=30,
            weight=BOLD,
        ).to_edge(UP, buff=0.5)
        self.add(heading)

        # Tree on the left half — 4 leaves keep the walk readable.
        tr_root = LEFT * 4.3 + UP * 1.7
        tr_L = LEFT * 5.5 + UP * 0.3
        tr_R = LEFT * 3.1 + UP * 0.3
        tr_l1 = LEFT * 6.2 + DOWN * 1.1
        tr_l2 = LEFT * 4.8 + DOWN * 1.1
        tr_l3 = LEFT * 3.8 + DOWN * 1.1
        tr_l4 = LEFT * 2.4 + DOWN * 1.1

        leaf_labels = ["p_1", "p_2", "p_3", "p_4"]

        def tree_node(pos, label, color, leaf=False):
            if leaf:
                shape = Square(side_length=0.5, color=color, stroke_width=2.5).move_to(
                    pos
                )
            else:
                shape = Circle(radius=0.28, color=color, stroke_width=2.5).move_to(pos)
            shape.set_fill(color, opacity=0.15)
            text = MathTex(label, font_size=24, color=color).move_to(pos)
            return VGroup(shape, text)

        n_root = tree_node(tr_root, r"\mathrm{root}", BLUE)
        n_L = tree_node(tr_L, "L", BLUE)
        n_R = tree_node(tr_R, "R", BLUE)
        n_l1 = tree_node(tr_l1, leaf_labels[0], GREEN, leaf=True)
        n_l2 = tree_node(tr_l2, leaf_labels[1], GREEN, leaf=True)
        n_l3 = tree_node(tr_l3, leaf_labels[2], GREEN, leaf=True)
        n_l4 = tree_node(tr_l4, leaf_labels[3], GREEN, leaf=True)
        tree_edges = VGroup(
            Line(tr_root + DOWN * 0.28, tr_L + UP * 0.28, color=GRAY_A),
            Line(tr_root + DOWN * 0.28, tr_R + UP * 0.28, color=GRAY_A),
            Line(tr_L + DOWN * 0.28, tr_l1 + UP * 0.28, color=GRAY_A),
            Line(tr_L + DOWN * 0.28, tr_l2 + UP * 0.28, color=GRAY_A),
            Line(tr_R + DOWN * 0.28, tr_l3 + UP * 0.28, color=GRAY_A),
            Line(tr_R + DOWN * 0.28, tr_l4 + UP * 0.28, color=GRAY_A),
        )
        self.play(
            Create(tree_edges),
            FadeIn(VGroup(n_root, n_L, n_R, n_l1, n_l2, n_l3, n_l4)),
        )

        # Pseudocode on the right
        pseudo_lines = [
            "stack ← {root}",
            "while stack not empty:",
            "    node ← stack.pop()",
            "    if leaf or open(node):",
            "        accumulate force",
            "    else:",
            "        push node.children",
        ]
        pseudo = (
            VGroup(*[CleanText(line, font_size=22, color=GRAY_A) for line in pseudo_lines])
            .arrange(DOWN, aligned_edge=LEFT, buff=0.18)
            .move_to(RIGHT * 2.5 + UP * 0.2)
        )
        self.play(FadeIn(pseudo, lag_ratio=0.15))
        self.next_slide()

        def visit(node_group, verdict_text, verdict_color):
            highlight = SurroundingRectangle(
                node_group[0], color=YELLOW, buff=0.08, stroke_width=4
            )
            verdict = CleanText(verdict_text, font_size=22, color=verdict_color).move_to(
                RIGHT * 2.5 + DOWN * 2.8
            )
            self.play(Create(highlight), FadeIn(verdict), run_time=0.5)
            self.next_slide()
            self.play(FadeOut(highlight), FadeOut(verdict), run_time=0.3)

        visit(n_root, "expand: push L, R", BLUE)
        visit(n_R, "small enough → accept as monopole", GREEN)
        visit(n_L, "too close → expand", BLUE)
        visit(n_l2, "leaf → accumulate", GREEN)
        visit(n_l1, "leaf → accumulate", GREEN)

        done = CleanText(
            "done — total force accumulated", font_size=22, color=YELLOW
        ).move_to(RIGHT * 2.5 + DOWN * 2.8)
        self.play(FadeIn(done))
        self.next_slide()
