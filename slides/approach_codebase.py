from manim import *
from manim_slides import Slide


class SingleCodebase(Slide):
    def construct(self):
        heading = Text(
            "One codebase, four backends",
            font_size=40,
            weight=BOLD,
        ).to_edge(UP, buff=0.6)
        self.play(Write(heading))
        self.next_slide()

        # === Top: source box ===
        source_rect = Rectangle(width=4.2, height=0.8, color=BLUE_B, stroke_width=2)
        source_text = Text("C++ / WGSL source", font_size=24, weight=BOLD).move_to(
            source_rect.get_center()
        )
        source = VGroup(source_rect, source_text).move_to(UP * 2.0)
        self.play(FadeIn(source, shift=DOWN * 0.2))
        self.next_slide()

        # === Middle: four backend boxes ===
        backend_specs = [
            ("wgpu-native", "Rust binding", BLUE_C),
            ("Dawn", "Google C++ ref", YELLOW_B),
            ("Chrome", "Wasm in browser", GREEN_B),
            ("Safari", "Wasm in browser", PURPLE_B),
        ]

        backends = VGroup()
        for name, sub, color in backend_specs:
            rect = Rectangle(width=2.4, height=1.0, color=color, stroke_width=2)
            title_t = Text(name, font_size=20, weight=BOLD).move_to(rect.get_top() + DOWN * 0.3)
            sub_t = Text(sub, font_size=14, color=GREY_B).move_to(rect.get_bottom() + UP * 0.3)
            # placeholder for a logo
            logo_ph = Text("[logo]", font_size=10, color=GREY_C).next_to(title_t, RIGHT, buff=0.1)
            backends.add(VGroup(rect, title_t, sub_t, logo_ph))

        backends.arrange(RIGHT, buff=0.25).move_to(DOWN * 0.2)
        if backends.width > 13.0:
            backends.scale(13.0 / backends.width)

        for b in backends:
            self.play(FadeIn(b, shift=UP * 0.2), run_time=0.4)
        self.next_slide()

        # arrows from source to each backend
        arrows = VGroup(
            *[
                Arrow(
                    source.get_bottom(),
                    b[0].get_top(),
                    buff=0.08,
                    color=GREY_B,
                    stroke_width=2,
                    tip_length=0.15,
                )
                for b in backends
            ]
        )
        self.play(LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.1))
        self.next_slide()

        # === Bottom: converge to Metal on M2 ===
        metal_rect = Rectangle(width=4.2, height=0.7, color=ORANGE, stroke_width=2)
        metal_text = Text("Metal — Apple M2", font_size=22, weight=BOLD).move_to(
            metal_rect.get_center()
        )
        metal = VGroup(metal_rect, metal_text).to_edge(DOWN, buff=1.2)

        merge_arrows = VGroup(
            *[
                Arrow(
                    b[0].get_bottom(),
                    metal.get_top(),
                    buff=0.08,
                    color=GREY_B,
                    stroke_width=2,
                    tip_length=0.15,
                )
                for b in backends
            ]
        )
        self.play(FadeIn(metal, shift=UP * 0.2))
        self.play(LaggedStart(*[GrowArrow(a) for a in merge_arrows], lag_ratio=0.1))
        self.next_slide()

        # baseline label off to the side
        baseline = Text(
            "Baseline: UniSim (hand-rolled native Metal)",
            font_size=18,
            slant=ITALIC,
            color=GREY_B,
        ).to_edge(DOWN, buff=0.4)
        self.play(FadeIn(baseline))
        self.next_slide()
