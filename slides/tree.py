import math

from manim import *
from manim_slides import Slide


class LBVHTraversal(Slide):
    def construct(self):
        # === 6-pass LBVH construction pipeline ===
        heading = Text(
            "Building the tree on the GPU",
            font_size=38,
            weight=BOLD,
        ).to_edge(UP, buff=0.5)
        self.play(Write(heading))
        self.next_slide()

        pass_data = [
            ("1. Global AABB reduction", "parallel min/max over positions", BLUE),
            ("2. Morton code generation", "30-bit Z-order key per particle", TEAL),
            ("3. Radix sort", "sort particles by Morton code", YELLOW),
            ("4. Karras topology", "internal-node parent/child from sorted keys", GREEN),
            ("5. Leaf initialisation", "AABB and mass per leaf", PURPLE),
            ("6. Bottom-up aggregation", "AABB + COM propagated to root", ORANGE),
        ]
        boxes = VGroup()
        captions = VGroup()
        arrows = VGroup()
        for i, (title, caption, color) in enumerate(pass_data):
            box = (
                Rectangle(width=4.8, height=0.65, color=color, stroke_width=3)
                .set_fill(color, opacity=0.15)
                .move_to(LEFT * 2.5 + UP * (2.4 - i * 0.95))
            )
            title_text = Text(title, font_size=22, color=color, weight=BOLD).move_to(
                box.get_center()
            )
            box_group = VGroup(box, title_text)
            boxes.add(box_group)

            caption_text = Text(caption, font_size=20, color=GRAY_A).next_to(
                box, RIGHT, buff=0.5
            )
            captions.add(caption_text)

            if i > 0:
                prev = boxes[i - 1][0]
                arrow = Arrow(
                    prev.get_bottom(),
                    box.get_top(),
                    buff=0.05,
                    color=GRAY_A,
                    stroke_width=2,
                    tip_length=0.15,
                )
                arrows.add(arrow)

        for i in range(len(pass_data)):
            anims = [FadeIn(boxes[i], shift=RIGHT * 0.3), FadeIn(captions[i])]
            if i > 0:
                anims.append(GrowArrow(arrows[i - 1]))
            self.play(*anims, run_time=0.45)
            self.next_slide()

        # === Karras topology from sorted Morton codes ===
        self.play(
            FadeOut(boxes),
            FadeOut(captions),
            FadeOut(arrows),
        )

        karras_heading = Text(
            "Karras: tree topology from sorted Morton keys",
            font_size=30,
            weight=BOLD,
        ).to_edge(UP, buff=0.5)
        self.play(Transform(heading, karras_heading))

        # 4 sorted Morton keys, 8 bits each
        sorted_keys = ["00010100", "00010101", "00100011", "00110011"]
        leaf_labels = ["p_1", "p_2", "p_3", "p_4"]

        key_rows = VGroup()
        for i, (key, name) in enumerate(zip(sorted_keys, leaf_labels)):
            name_tex = MathTex(name, font_size=26, color=BLUE).move_to(
                LEFT * 5.0 + DOWN * (1.6 + i * 0.55)
            )
            key_chars = VGroup()
            for j, ch in enumerate(key):
                d = MathTex(ch, font_size=32)
                d.move_to(LEFT * 3.6 + RIGHT * j * 0.45 + DOWN * (1.6 + i * 0.55))
                key_chars.add(d)
            key_rows.add(VGroup(name_tex, key_chars))

        self.play(FadeIn(key_rows, lag_ratio=0.1))
        self.next_slide()

        # Highlight common prefixes between adjacent pairs.
        # prefix[i] = number of leading bits shared by keys[i] and keys[i+1].
        def common_prefix(a: str, b: str) -> int:
            n = 0
            for ca, cb in zip(a, b):
                if ca != cb:
                    break
                n += 1
            return n

        prefix_lengths = [
            common_prefix(sorted_keys[i], sorted_keys[i + 1])
            for i in range(len(sorted_keys) - 1)
        ]
        # Visual: highlight the common prefix bits of pair (i, i+1) in YELLOW.
        all_highlights = VGroup()
        for pair_idx, prefix_len in enumerate(prefix_lengths):
            row_a = key_rows[pair_idx][1]
            row_b = key_rows[pair_idx + 1][1]
            highlights = VGroup()
            for j in range(prefix_len):
                box = SurroundingRectangle(
                    VGroup(row_a[j], row_b[j]),
                    color=YELLOW,
                    buff=0.05,
                    stroke_width=2,
                )
                highlights.add(box)
            all_highlights.add(highlights)
            self.play(Create(highlights, lag_ratio=0.1), run_time=0.6)
            self.next_slide()

        # Draw a binary tree corresponding to the Karras topology.
        # Pairs with deepest prefix are most closely related siblings.
        # Pairwise prefix lengths (above): [7, 3, 4]
        # Algorithm builds: leaf order p_1, p_2, p_3, p_4
        # Splits are at the *minimum* common prefix in each range; min(7,3,4)=3 at idx 1
        # → root splits [p_1,p_2] | [p_3,p_4]
        # Left subtree split: only pair (p_1,p_2), prefix 7
        # Right subtree split: only pair (p_3,p_4), prefix 4
        tree_root = LEFT * 2.5 + UP * 1.8
        tree_L = LEFT * 4.2 + UP * 0.6
        tree_R = LEFT * 0.8 + UP * 0.6
        tree_l1 = LEFT * 5.2 + DOWN * 0.5
        tree_l2 = LEFT * 3.2 + DOWN * 0.5
        tree_l3 = LEFT * 1.8 + DOWN * 0.5
        tree_l4 = LEFT * 0.2 + DOWN * 0.5

        def tree_node(pos, label, color, leaf=False):
            shape = Circle(radius=0.28, color=color, stroke_width=2.5).move_to(pos)
            if leaf:
                shape = Square(side_length=0.5, color=color, stroke_width=2.5).move_to(pos)
            text = MathTex(label, font_size=24, color=color).move_to(pos)
            return VGroup(shape, text)

        n_root = tree_node(tree_root, r"\mathrm{root}", BLUE)
        n_L = tree_node(tree_L, "L", BLUE)
        n_R = tree_node(tree_R, "R", BLUE)
        n_l1 = tree_node(tree_l1, leaf_labels[0], GREEN, leaf=True)
        n_l2 = tree_node(tree_l2, leaf_labels[1], GREEN, leaf=True)
        n_l3 = tree_node(tree_l3, leaf_labels[2], GREEN, leaf=True)
        n_l4 = tree_node(tree_l4, leaf_labels[3], GREEN, leaf=True)

        tree_edges = VGroup(
            Line(tree_root + DOWN * 0.28, tree_L + UP * 0.28, color=GRAY_A),
            Line(tree_root + DOWN * 0.28, tree_R + UP * 0.28, color=GRAY_A),
            Line(tree_L + DOWN * 0.28, tree_l1 + UP * 0.28, color=GRAY_A),
            Line(tree_L + DOWN * 0.28, tree_l2 + UP * 0.28, color=GRAY_A),
            Line(tree_R + DOWN * 0.28, tree_l3 + UP * 0.28, color=GRAY_A),
            Line(tree_R + DOWN * 0.28, tree_l4 + UP * 0.28, color=GRAY_A),
        )
        tree = VGroup(tree_edges, n_root, n_L, n_R, n_l1, n_l2, n_l3, n_l4)
        self.play(Create(tree_edges), FadeIn(VGroup(n_root, n_L, n_R, n_l1, n_l2, n_l3, n_l4)))
        self.next_slide()

        # === GPU traversal: explicit stack ===
        self.play(
            FadeOut(key_rows),
            FadeOut(all_highlights),
            FadeOut(tree),
        )

        traverse_heading = Text(
            "GPU traversal: an explicit stack, no recursion",
            font_size=30,
            weight=BOLD,
        ).to_edge(UP, buff=0.5)
        self.play(Transform(heading, traverse_heading))

        # Re-position a fresh tree on the LEFT
        tr_root = LEFT * 4.3 + UP * 1.7
        tr_L = LEFT * 5.5 + UP * 0.3
        tr_R = LEFT * 3.1 + UP * 0.3
        tr_l1 = LEFT * 6.2 + DOWN * 1.1
        tr_l2 = LEFT * 4.8 + DOWN * 1.1
        tr_l3 = LEFT * 3.8 + DOWN * 1.1
        tr_l4 = LEFT * 2.4 + DOWN * 1.1

        tn_root = tree_node(tr_root, r"\mathrm{root}", BLUE)
        tn_L = tree_node(tr_L, "L", BLUE)
        tn_R = tree_node(tr_R, "R", BLUE)
        tn_l1 = tree_node(tr_l1, "l_1", GREEN, leaf=True)
        tn_l2 = tree_node(tr_l2, "l_2", GREEN, leaf=True)
        tn_l3 = tree_node(tr_l3, "l_3", GREEN, leaf=True)
        tn_l4 = tree_node(tr_l4, "l_4", GREEN, leaf=True)
        tr_edges = VGroup(
            Line(tr_root + DOWN * 0.28, tr_L + UP * 0.28, color=GRAY_A),
            Line(tr_root + DOWN * 0.28, tr_R + UP * 0.28, color=GRAY_A),
            Line(tr_L + DOWN * 0.28, tr_l1 + UP * 0.28, color=GRAY_A),
            Line(tr_L + DOWN * 0.28, tr_l2 + UP * 0.28, color=GRAY_A),
            Line(tr_R + DOWN * 0.28, tr_l3 + UP * 0.28, color=GRAY_A),
            Line(tr_R + DOWN * 0.28, tr_l4 + UP * 0.28, color=GRAY_A),
        )

        traverse_tree = VGroup(
            tr_edges, tn_root, tn_L, tn_R, tn_l1, tn_l2, tn_l3, tn_l4
        )
        self.play(
            FadeOut(tree),  # remove the earlier tree
            FadeIn(traverse_tree),
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
            VGroup(*[Text(line, font_size=22, color=GRAY_A) for line in pseudo_lines])
            .arrange(DOWN, aligned_edge=LEFT, buff=0.18)
            .move_to(RIGHT * 2.5 + UP * 0.2)
        )
        self.play(FadeIn(pseudo, lag_ratio=0.15))
        self.next_slide()

        # Walk: visit root → push L, R; visit R → small enough, accept; visit L → expand; visit l2, l1 → leaves, accept
        def visit(node_group, verdict_text, verdict_color):
            highlight = SurroundingRectangle(
                node_group[0], color=YELLOW, buff=0.08, stroke_width=4
            )
            verdict = Text(verdict_text, font_size=22, color=verdict_color).move_to(
                RIGHT * 2.5 + DOWN * 2.8
            )
            self.play(Create(highlight), FadeIn(verdict), run_time=0.5)
            self.next_slide()
            self.play(FadeOut(highlight), FadeOut(verdict), run_time=0.3)

        visit(tn_root, "expand: push L, R", BLUE)
        visit(tn_R, "small enough → accept as monopole", GREEN)
        visit(tn_L, "too close → expand", BLUE)
        visit(tn_l2, "leaf → accumulate", GREEN)
        visit(tn_l1, "leaf → accumulate", GREEN)

        done = Text("done — total force accumulated", font_size=22, color=YELLOW).move_to(
            RIGHT * 2.5 + DOWN * 2.8
        )
        self.play(FadeIn(done))
        self.next_slide()

        # === Payoff: O(N²) → O(N log N) ===
        self.play(FadeOut(traverse_tree), FadeOut(pseudo), FadeOut(done))

        payoff_heading = Text(
            "The payoff: O(N²) → O(N log N)",
            font_size=36,
            weight=BOLD,
            color=GREEN,
        ).to_edge(UP, buff=0.5)
        self.play(Transform(heading, payoff_heading))

        ax = Axes(
            x_range=[0, 6, 1],
            y_range=[0, 12, 2],
            x_length=8,
            y_length=4.5,
            axis_config={"include_tip": False, "stroke_width": 2},
        ).move_to(DOWN * 0.4)
        x_label = MathTex(r"\log_{10} N", font_size=28).next_to(ax.x_axis, DOWN, buff=0.3)
        y_label = MathTex(r"\log_{10} \mathrm{work}", font_size=28).next_to(
            ax.y_axis, LEFT, buff=0.3
        )

        n2_curve = ax.plot(lambda x: 2 * x, x_range=[0.2, 6], color=RED, stroke_width=4)
        n2_label = MathTex(r"\mathcal{O}(N^2)", font_size=32, color=RED).move_to(
            ax.c2p(5, 11)
        )
        nlogn_curve = ax.plot(
            lambda x: x + math.log10(max(x * math.log(10), 1.0)),
            x_range=[0.2, 6],
            color=GREEN,
            stroke_width=4,
        )
        nlogn_label = MathTex(r"\mathcal{O}(N \log N)", font_size=32, color=GREEN).move_to(
            ax.c2p(5, 6.5)
        )

        self.play(Create(ax), Write(x_label), Write(y_label))
        self.play(Create(n2_curve), Write(n2_label))
        self.next_slide()
        self.play(Create(nlogn_curve), Write(nlogn_label))
        self.next_slide()

        gap_brace = Brace(
            Line(ax.c2p(5, 5.7), ax.c2p(5, 10)),
            RIGHT,
            color=YELLOW,
        )
        gap_label = Text(
            "gap grows with N", font_size=22, color=YELLOW
        ).next_to(gap_brace, RIGHT, buff=0.2)
        self.play(GrowFromCenter(gap_brace), Write(gap_label))
        self.next_slide()
