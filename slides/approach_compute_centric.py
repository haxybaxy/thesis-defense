from manim import *
from manim_slides import Slide

from _text import CleanText


class ComputeCentric(Slide):
    def construct(self):
        title = CleanText("Compute Pipeline", font_size=36, weight=BOLD).to_edge(
            UP, buff=0.5
        )
        self.add(title)

        # Horizontal pipeline strip: 4 boxes, all lit.
        block_w = 2.6
        block_h = 1.1
        gap = 0.45
        labels = [
            ("Integrator", BLUE_B),
            ("Tree build", GREEN_B),
            ("Force eval", ORANGE),
            ("Render", GREY_B),
        ]

        # Build all blocks.
        blocks = []
        for i, (name, color) in enumerate(labels):
            x = -((len(labels) - 1) / 2) * (block_w + gap) + i * (block_w + gap)
            box = RoundedRectangle(
                width=block_w,
                height=block_h,
                corner_radius=0.18,
                color=color,
                stroke_width=3,
            )
            box.set_fill(color, opacity=0.22)
            txt = CleanText(
                name,
                font_size=24,
                weight=BOLD,
                color=color,
            ).move_to(box.get_center())
            block = VGroup(box, txt).move_to(RIGHT * x + UP * 0.5)
            blocks.append((block, box, color))

        # Arrows between blocks.
        arrows = VGroup()
        for i in range(len(blocks) - 1):
            a = Arrow(
                blocks[i][1].get_right(),
                blocks[i + 1][1].get_left(),
                buff=0.05,
                color=GREY_A,
                stroke_width=2,
                tip_length=0.15,
            )
            arrows.add(a)

        # Compute brace under the first three, labelled "compute shaders".
        compute_blocks = VGroup(*[b[0] for b in blocks[:3]])
        compute_brace = Brace(compute_blocks, DOWN, color=YELLOW_B)
        compute_label = CleanText(
            "compute shaders",
            font_size=24,
            weight=BOLD,
            color=YELLOW_B,
        ).next_to(compute_brace, DOWN, buff=0.15)

        # Render caption beneath the render box.
        render_caption = CleanText(
            "graphics shader",
            font_size=20,
            color=GREY_B,
            slant=ITALIC,
        ).next_to(blocks[3][0], DOWN, buff=0.25)

        # Pipeline strip present on load.
        self.add(*[b[0] for b in blocks], arrows)
        self.wait(0.1)
        self.next_slide()

        # Sequential animation: brace, label, then render caption.
        self.play(GrowFromCenter(compute_brace))
        self.play(Write(compute_label))
        self.play(FadeIn(render_caption, shift=UP * 0.15))
        self.next_slide()
