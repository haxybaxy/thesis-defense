from manim import *
from manim_slides import Slide


class IntegratorContext(Slide):
    """Handoff slide between the force half (Tree + Force eval) and the
    integrator half (½ Kick + Drift + ½ Kick) of the five-stage pipeline.

    The horizontal strip reuses the same five colour-coded stages established
    on the `PipelineOverview` roadmap, so the audience sees a familiar layout
    with the two force stages explicitly marked done.
    """

    def construct(self):
        heading = Text(
            "Force half done, now the integrator half",
            font_size=34,
            weight=BOLD,
        ).to_edge(UP, buff=0.5)
        self.play(Write(heading))
        self.next_slide()

        stages = [
            ("½ Kick", BLUE),
            ("Drift", TEAL),
            ("Tree build", GREEN),
            ("Force eval", ORANGE),
            ("½ Kick", BLUE),
        ]
        strip = VGroup()
        for name, color in stages:
            box = Rectangle(
                width=1.95, height=0.85, color=color, stroke_width=2.5
            ).set_fill(color, opacity=0.18)
            label = Text(name, font_size=20, color=color, weight=BOLD).move_to(
                box.get_center()
            )
            strip.add(VGroup(box, label))
        strip.arrange(RIGHT, buff=0.28).move_to(DOWN * 0.1)

        arrows = VGroup()
        for i in range(len(strip) - 1):
            arrows.add(
                Arrow(
                    strip[i][0].get_right(),
                    strip[i + 1][0].get_left(),
                    buff=0.05,
                    color=GRAY_B,
                    stroke_width=2,
                    tip_length=0.15,
                )
            )

        self.play(
            LaggedStart(*[FadeIn(s) for s in strip], lag_ratio=0.1),
            LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.1),
            run_time=1.6,
        )
        self.next_slide()

        # Mark the two force-half stages as completed: dim them and add a
        # small green "done" tag above each. The remaining three stages stay
        # at full opacity to pull the eye toward what's still ahead.
        done_indices = [2, 3]
        dim_anims = []
        done_markers = VGroup()
        for i in done_indices:
            dim_anims.append(
                strip[i][0].animate.set_fill(opacity=0.06).set_stroke(opacity=0.4)
            )
            dim_anims.append(strip[i][1].animate.set_opacity(0.45))
            done_markers.add(
                Text(
                    "done",
                    font_size=16,
                    color=GREEN,
                    slant=ITALIC,
                    weight=BOLD,
                ).next_to(strip[i][0], UP, buff=0.12)
            )

        self.play(
            *dim_anims,
            LaggedStart(
                *[FadeIn(m, shift=DOWN * 0.1) for m in done_markers],
                lag_ratio=0.2,
            ),
            run_time=0.9,
        )
        self.next_slide()

        caption = Text(
            "Three multiply-add updates per particle per timestep.",
            font_size=22,
            color=GRAY_A,
        ).next_to(strip, DOWN, buff=0.85)
        self.play(FadeIn(caption, shift=UP * 0.15))
        self.next_slide()

        hook = Text(
            "And yet — getting them right is the hard part.",
            font_size=24,
            color=YELLOW,
            weight=BOLD,
            slant=ITALIC,
        ).next_to(caption, DOWN, buff=0.35)
        self.play(Write(hook))
        self.next_slide()
