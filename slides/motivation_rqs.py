from manim import *
from manim_slides import Slide

from _text import CleanText


class ResearchQuestions(Slide):
    """Single centred framing question: 'Is WebGPU a viable compute platform?'.

    Sits after ShaderVsCompute (establishes what a compute shader is) and
    before ComputeCentric (commits to compute as the backbone of our
    pipeline).
    """

    def construct(self):
        umbrella = CleanText(
            "Is WebGPU a viable compute platform?",
            font_size=42,
            weight=BOLD,
        ).move_to(ORIGIN)
        underline = Line(
            umbrella.get_corner(DL) + DOWN * 0.18,
            umbrella.get_corner(DR) + DOWN * 0.18,
            color=YELLOW_B,
            stroke_width=2.5,
        )

        self.add(umbrella)
        self.play(Create(underline), run_time=0.5)
        self.next_slide()
