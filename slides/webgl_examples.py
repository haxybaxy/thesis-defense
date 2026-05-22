from manim import *
from manim_slides import Slide


class WebGLExamples(Slide):
    def construct(self):
        logo = SVGMobject("assets/WebGL_Logo.svg").scale_to_fit_height(2.2)

        shot1 = ImageMobject("assets/webglbad1.png").scale_to_fit_height(2.2)
        shot2 = ImageMobject("assets/webglbad2.png").scale_to_fit_height(2.2)
        shots = Group(shot1, shot2).arrange(RIGHT, buff=0.6)

        content = Group(logo, shots).arrange(DOWN, buff=0.5)
        content.move_to(ORIGIN)

        self.add(content)
        self.wait(0.1)
        self.next_slide()
