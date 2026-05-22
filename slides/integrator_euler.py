import numpy as np

from manim import *
from manim_slides import Slide

from _text import CleanText


def _euler_trajectory(steps=650, dt=0.06):
    GM = 1.0
    r = np.array([1.4, 0.0, 0.0])
    v = np.array([0.0, 0.86, 0.0])
    pts = [r.copy()]
    for _ in range(steps):
        rel = -r
        a = GM * rel / float(np.linalg.norm(rel)) ** 3
        r = r + v * dt
        v = v + a * dt
        pts.append(r.copy())
    return pts


def _leapfrog_trajectory(steps=650, dt=0.06):
    GM = 1.0
    r = np.array([1.4, 0.0, 0.0])
    v = np.array([0.0, 0.86, 0.0])
    rel = -r
    a = GM * rel / float(np.linalg.norm(rel)) ** 3
    v = v + 0.5 * a * dt
    pts = [r.copy()]
    for _ in range(steps):
        r = r + v * dt
        rel = -r
        a = GM * rel / float(np.linalg.norm(rel)) ** 3
        v = v + a * dt
        pts.append(r.copy())
    return pts


class IntegratorOrbits(Slide):
    def construct(self):
        heading = CleanText(
            "Run them forward and watch the orbits",
            font_size=36,
            weight=BOLD,
        ).to_edge(UP, buff=0.5)

        scale = 0.95
        left_offset = LEFT * 3.4 + DOWN * 0.4
        right_offset = RIGHT * 3.4 + DOWN * 0.4
        ideal_radius = 1.4 * scale

        def build_frame(offset, name, name_color):
            ideal_circle = (
                Circle(radius=ideal_radius, color=GREEN_B, stroke_width=1.5)
                .move_to(offset)
                .set_stroke(opacity=0.4)
            )
            ideal_dashed = DashedVMobject(ideal_circle, num_dashes=36)
            central = VGroup(
                Dot(offset, radius=0.12, color=YELLOW),
                MathTex("M", color=YELLOW, font_size=22).move_to(
                    offset + DOWN * 0.32
                ),
            )
            label = CleanText(
                name, font_size=28, color=name_color, weight=BOLD
            ).move_to(offset + UP * (ideal_radius + 1.15))
            return ideal_dashed, central, label

        eul_ideal, eul_central, eul_label = build_frame(
            left_offset,
            "Euler",
            RED,
        )
        lf_ideal, lf_central, lf_label = build_frame(
            right_offset,
            "Leapfrog",
            GREEN,
        )

        eul_pts = [scale * p + left_offset for p in _euler_trajectory()]
        lf_pts = [scale * p + right_offset for p in _leapfrog_trajectory()]

        eul_orbiter = Dot(eul_pts[0], radius=0.08, color=BLUE)
        lf_orbiter = Dot(lf_pts[0], radius=0.08, color=BLUE)

        self.add(
            heading,
            eul_ideal,
            eul_central,
            eul_label,
            lf_ideal,
            lf_central,
            lf_label,
            eul_orbiter,
            lf_orbiter,
        )
        self.wait(0.1)
        self.next_slide()

        # Attach trails only now so they don't accumulate degenerate points
        # during the static slide, which exposed a 1-frame player glitch
        # at the slide-transition boundary.
        eul_trail = TracedPath(
            eul_orbiter.get_center, stroke_color=RED, stroke_width=3.0
        )
        lf_trail = TracedPath(
            lf_orbiter.get_center, stroke_color=GREEN, stroke_width=3.0
        )
        self.add(eul_trail, lf_trail)

        eul_path = VMobject()
        eul_path.set_points_as_corners(eul_pts)
        lf_path = VMobject()
        lf_path.set_points_as_corners(lf_pts)

        self.play(
            MoveAlongPath(eul_orbiter, eul_path, rate_func=linear),
            MoveAlongPath(lf_orbiter, lf_path, rate_func=linear),
            run_time=6.0,
        )

        # Freeze the trails so the drawn paths stay put while the captions appear.
        eul_trail.clear_updaters()
        lf_trail.clear_updaters()

        eul_caption = CleanText(
            "energy grows → orbit decays",
            font_size=20,
            color=RED,
        ).move_to(left_offset + DOWN * (ideal_radius + 0.55))
        lf_caption = CleanText(
            "energy bounded → orbit closes",
            font_size=20,
            color=GREEN,
        ).move_to(right_offset + DOWN * (ideal_radius + 0.55))
        self.play(
            FadeIn(eul_caption, shift=UP * 0.1),
            FadeIn(lf_caption, shift=UP * 0.1),
        )
        self.next_slide()
