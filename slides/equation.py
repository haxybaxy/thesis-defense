from manim import *
from manim_slides import Slide


class Equation(Slide):
    def construct(self):
        heading = Text("Key Result", font_size=44, weight=BOLD).to_edge(UP)
        self.play(Write(heading))
        self.next_slide()

        eq = MathTex(
            r"\mathcal{L}(\theta) = "
            r"\mathbb{E}_{x \sim \mathcal{D}} \left[ \ell(f_\theta(x), y) \right] "
            r"+ \lambda \|\theta\|_2^2",
            font_size=44,
        )
        self.play(Write(eq))
        self.next_slide()

        data_term = eq[0][:24]
        reg_term = eq[0][24:]
        data_label = Text("data loss", font_size=24, color=BLUE).next_to(data_term, DOWN, buff=0.8)
        reg_label = Text("regularizer", font_size=24, color=GREEN).next_to(reg_term, DOWN, buff=0.8)
        data_arrow = Arrow(data_label.get_top(), data_term.get_bottom(), color=BLUE, buff=0.1)
        reg_arrow = Arrow(reg_label.get_top(), reg_term.get_bottom(), color=GREEN, buff=0.1)

        self.play(
            data_term.animate.set_color(BLUE),
            GrowArrow(data_arrow),
            FadeIn(data_label),
        )
        self.next_slide()

        self.play(
            reg_term.animate.set_color(GREEN),
            GrowArrow(reg_arrow),
            FadeIn(reg_label),
        )
        self.next_slide()

        self.next_slide(loop=True)
        pulse = SurroundingRectangle(eq, color=YELLOW, buff=0.25)
        self.play(Create(pulse), run_time=1.0)
        self.play(FadeOut(pulse), run_time=1.0)
