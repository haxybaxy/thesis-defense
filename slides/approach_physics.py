from manim import *
from manim_slides import Slide


class PhysicsAndIntegrator(Slide):
    def construct(self):
        heading = Text(
            "Physics + integrator",
            font_size=42,
            weight=BOLD,
        ).to_edge(UP, buff=0.6)
        self.play(Write(heading))
        self.next_slide()

        # === Softened acceleration ===
        soft_label = Text("Softened acceleration (Plummer)", font_size=22, weight=BOLD, color=BLUE_B)
        soft_eq = MathTex(
            r"\vec{a}_i = G \sum_{j \neq i} m_j \, \frac{\vec{r}_j - \vec{r}_i}"
            r"{(|\vec{r}_j - \vec{r}_i|^2 + \epsilon^2)^{3/2}}",
            font_size=30,
        )
        soft_block = VGroup(soft_label, soft_eq).arrange(DOWN, aligned_edge=LEFT, buff=0.2)

        # === Leapfrog KDK ===
        leap_label = Text("Leapfrog (kick–drift–kick)", font_size=22, weight=BOLD, color=YELLOW_B)
        leap_eqs = VGroup(
            MathTex(r"v^{n+1/2} \;=\; v^n + \frac{\Delta t}{2}\, a^n", font_size=26),
            MathTex(r"r^{n+1}   \;=\; r^n + \Delta t \, v^{n+1/2}", font_size=26),
            MathTex(r"v^{n+1}   \;=\; v^{n+1/2} + \frac{\Delta t}{2}\, a^{n+1}", font_size=26),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        leap_block = VGroup(leap_label, leap_eqs).arrange(DOWN, aligned_edge=LEFT, buff=0.2)

        # arrange the two equation blocks side by side
        eq_row = VGroup(soft_block, leap_block).arrange(RIGHT, aligned_edge=UP, buff=1.0)
        eq_row.next_to(heading, DOWN, buff=0.6)

        self.play(FadeIn(soft_block, shift=UP * 0.2))
        self.next_slide()
        self.play(FadeIn(leap_block, shift=UP * 0.2))
        self.next_slide()

        # === Parameter table ===
        param_label = Text("Defaults", font_size=22, weight=BOLD, color=GREEN_B)
        params = VGroup(
            MathTex(r"\theta = 0.75", font_size=28),
            MathTex(r"\Delta t = 10^{-3}", font_size=28),
            MathTex(r"\epsilon = 0.5", font_size=28),
            MathTex(r"G = M_{\rm tot} = L = 1", font_size=28),
        ).arrange(RIGHT, buff=0.7)
        params_block = VGroup(param_label, params).arrange(DOWN, buff=0.25)
        params_block.to_edge(DOWN, buff=0.8)

        self.play(FadeIn(params_block, shift=UP * 0.2))
        self.next_slide()

        cites = Text(
            "Verlet 1967  ·  Springel 2005 (GADGET-2)  ·  Barnes & Hut 1986",
            font_size=15,
            color=GREY_C,
        ).to_edge(DOWN, buff=0.25)
        self.play(FadeIn(cites))
        self.next_slide()
