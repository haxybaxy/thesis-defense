import math
import random

from manim import *
from manim_slides import Slide


class GalacticDynamics(Slide):
    def construct(self):
        random.seed(7)

        heading = Text(
            "Simulating a galaxy",
            font_size=40,
            weight=BOLD,
        ).to_edge(UP, buff=0.6)
        self.play(Write(heading))
        self.next_slide()

        # === Left: a swirling disk of particles ===
        disk_center = LEFT * 3.2 + DOWN * 0.3
        N = 90
        dots = VGroup()
        for _ in range(N):
            r = random.uniform(0.25, 2.1)
            theta = random.uniform(0, 2 * math.pi)
            z_jitter = random.uniform(-0.15, 0.15)
            color = interpolate_color(BLUE_C, YELLOW, max(0.0, 1.0 - r / 2.1))
            pos = disk_center + RIGHT * (r * math.cos(theta)) + UP * (r * math.sin(theta) + z_jitter)
            dots.add(Dot(pos, radius=0.05, color=color))

        self.play(
            LaggedStart(*[FadeIn(d, scale=0.3) for d in dots], lag_ratio=0.01),
            run_time=1.5,
        )
        self.next_slide()

        # gentle rotation around the disk centre, looped
        self.next_slide(loop=True)
        self.play(
            Rotate(dots, angle=2 * math.pi / 6, about_point=disk_center),
            run_time=2.5,
            rate_func=linear,
        )

        # === Right: the three things this computes ===
        bullets = VGroup(
            Text("N stars, all pulling on each other", font_size=28),
            Text(r"10^4 – 10^7 timesteps per simulation", font_size=28),
            Text("Spiral arms, cluster relaxation,\nhalo virialisation", font_size=28),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.7)
        bullets.move_to(RIGHT * 2.6)

        for b in bullets:
            self.play(FadeIn(b, shift=RIGHT * 0.3), run_time=0.5)
            self.next_slide()

        # closing tagline
        tag = Text(
            "The physics is undergraduate. The computation is not.",
            font_size=24,
            slant=ITALIC,
            color=GREY_B,
        ).to_edge(DOWN, buff=0.6)
        self.play(Write(tag))
        self.next_slide()
