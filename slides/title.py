from manim import *
from manim_slides import Slide


class TitleSlide(Slide):
    def construct(self):
        # --- The joke title (nailed to the "wall") --------------------------
        joke_text = Text(
            "A Hitchhiker's Guide to\nGalaxy Simulations",
            font_size=46,
            weight=BOLD,
        )

        sign_bg = SurroundingRectangle(
            joke_text,
            color=WHITE,
            buff=0.55,
            fill_color="#1f3a5f",
            fill_opacity=0.6,
            stroke_width=3,
            stroke_color=WHITE,
        )

        sign = VGroup(sign_bg, joke_text)

        screw_offset = 0.28
        screw_left = Dot(
            sign_bg.get_corner(UL) + RIGHT * screw_offset + DOWN * screw_offset,
            radius=0.1,
            color=GRAY_C,
        )
        screw_right = Dot(
            sign_bg.get_corner(UR) + LEFT * screw_offset + DOWN * screw_offset,
            radius=0.1,
            color=GRAY_C,
        )

        # cross marks on the screws so they read as screw heads
        def screw_cross(dot):
            r = dot.radius * 0.7
            c = dot.get_center()
            line1 = Line(c + LEFT * r, c + RIGHT * r, stroke_width=2, color=BLACK)
            line2 = Line(c + UP * r, c + DOWN * r, stroke_width=2, color=BLACK)
            return VGroup(line1, line2)

        cross_left = screw_cross(screw_left)
        cross_right = screw_cross(screw_right)
        screw_left_grp = VGroup(screw_left, cross_left)
        screw_right_grp = VGroup(screw_right, cross_right)

        # --- Reveal joke title ---------------------------------------------
        self.play(
            FadeIn(sign, scale=0.9),
            FadeIn(screw_left_grp),
            FadeIn(screw_right_grp),
            run_time=0.8,
        )

        # tiny settle wobble so it feels physical
        self.play(
            Rotate(sign, angle=-PI / 80, about_point=screw_right.get_center()),
            rate_func=there_and_back,
            run_time=0.6,
        )

        # PAUSE: hold for the laugh, then click to trigger the fall
        self.next_slide()

        # --- Right screw rattles loose and pops out -------------------------
        self.play(
            screw_right_grp.animate.shift(RIGHT * 0.04),
            rate_func=there_and_back,
            run_time=0.15,
        )
        self.play(
            screw_right_grp.animate.shift(DOWN * 5 + RIGHT * 0.4)
            .rotate(PI)
            .set_opacity(0),
            run_time=0.55,
            rate_func=rush_into,
        )

        # --- Sign swings down on the remaining left screw ------------------
        pivot_left = screw_left.get_center()
        self.play(
            Rotate(sign, angle=-PI / 2.4, about_point=pivot_left),
            rate_func=rush_into,
            run_time=0.95,
        )
        # creaky bounce as it hangs
        self.play(
            Rotate(sign, angle=PI / 14, about_point=pivot_left),
            rate_func=there_and_back,
            run_time=0.45,
        )

        # --- Left screw finally gives way, whole sign falls ----------------
        self.play(
            screw_left_grp.animate.shift(DOWN * 5 + LEFT * 0.3)
            .rotate(PI)
            .set_opacity(0),
            sign.animate.shift(DOWN * 9).rotate(-PI / 2),
            run_time=1.2,
            rate_func=rush_into,
        )
        self.remove(sign, screw_left_grp, screw_right_grp)

        # --- Reveal the actual title ---------------------------------------
        title = Text(
            "Hierarchical N-Body Simulation of\nGalactic Dynamics in WebGPU",
            font_size=42,
            weight=BOLD,
        )
        subtitle = Text(
            "Enabling Scalable and Interactive Physics Simulations\non Modern Web Platforms",
            font_size=24,
            slant=ITALIC,
        )
        author = Text("Zaid Alsaheb", font_size=32)
        advisor = Text("Advisor: Prof. Raul Pérez Peláez", font_size=24)

        title.to_edge(UP, buff=1.2)
        subtitle.next_to(title, DOWN, buff=0.4)
        author.next_to(subtitle, DOWN, buff=1.0)
        advisor.next_to(author, DOWN, buff=0.3)

        self.play(
            FadeIn(title, shift=UP * 0.2),
            FadeIn(subtitle, shift=UP * 0.2),
            FadeIn(author, shift=UP * 0.2),
            FadeIn(advisor, shift=UP * 0.2),
            run_time=0.9,
        )

        self.wait(0.1)
        self.next_slide()
