from manim import *
from manim_slides import Slide


class LBVHConstruction(Slide):
    def construct(self):
        heading = Text(
            "Karras 2012: parallel tree construction",
            font_size=38,
            weight=BOLD,
        ).to_edge(UP, buff=0.6)
        self.play(Write(heading))
        self.next_slide()

        # Three-step flow boxes
        steps = []
        labels = [
            ("Step 1", "Particles → Morton codes", "30-bit Z-order keys"),
            ("Step 2", "Sort the codes", "topology is implicit in shared bit-prefixes"),
            ("Step 3", "δ-function builds tree", "every internal node located in parallel"),
        ]
        colors = [BLUE_B, YELLOW_B, GREEN_B]

        boxes = VGroup()
        for (tag, headline, sub), color in zip(labels, colors):
            tag_t = Text(tag, font_size=18, weight=BOLD, color=color)
            head_t = Text(headline, font_size=22, weight=BOLD)
            sub_t = Text(sub, font_size=18, color=GREY_B)
            content = VGroup(tag_t, head_t, sub_t).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
            box = SurroundingRectangle(
                content, color=color, buff=0.25, corner_radius=0.1, stroke_width=2
            )
            boxes.add(VGroup(box, content))

        boxes.arrange(RIGHT, buff=0.3).next_to(heading, DOWN, buff=0.7)
        if boxes.width > 13.0:
            boxes.scale(13.0 / boxes.width)

        for b in boxes:
            self.play(FadeIn(b, shift=UP * 0.2), run_time=0.5)
            self.next_slide()

        # Why BVH over octree
        why_label = Text("Why BVH over octree on GPU:", font_size=22, weight=BOLD, color=ORANGE)
        reasons = VGroup(
            Text("· Binary children → fewer branch decisions", font_size=20),
            Text("· Fixed 2N − 1 nodes regardless of distribution", font_size=20),
            Text("· Bottom-up parallel aggregation is clean", font_size=20),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        why = VGroup(why_label, reasons).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        why.to_edge(DOWN, buff=0.5).align_to(boxes, LEFT)

        self.play(FadeIn(why_label))
        for r in reasons:
            self.play(FadeIn(r, shift=RIGHT * 0.2), run_time=0.3)
        self.next_slide()
