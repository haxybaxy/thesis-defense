from manim import *
from manim_slides import Slide


class BarnesHutTheory(Slide):
    def construct(self):
        heading = Text(
            "N-body theory: from N² to N log N",
            font_size=38,
            weight=BOLD,
        ).to_edge(UP, buff=0.6)
        self.play(Write(heading))
        self.next_slide()

        # === Step 1: softened gravity ===
        step1_label = Text("1. Softened gravity (Plummer)", font_size=24, weight=BOLD, color=BLUE_B)
        step1_eq = MathTex(
            r"\vec{a}_i = G \sum_{j \neq i} m_j \, \frac{\vec{r}_j - \vec{r}_i}"
            r"{(|\vec{r}_j - \vec{r}_i|^2 + \epsilon^2)^{3/2}}",
            font_size=32,
        )
        step1 = VGroup(step1_label, step1_eq).arrange(DOWN, aligned_edge=LEFT, buff=0.25)

        # === Step 2: symplectic integrator ===
        step2_label = Text(
            "2. Symplectic leapfrog (kick–drift–kick)", font_size=24, weight=BOLD, color=YELLOW_B
        )
        step2_eqs = VGroup(
            MathTex(r"v^{n+1/2} = v^n + \frac{\Delta t}{2} \, a^n", font_size=26),
            MathTex(r"r^{n+1}   = r^n + \Delta t \, v^{n+1/2}", font_size=26),
            MathTex(r"v^{n+1}   = v^{n+1/2} + \frac{\Delta t}{2} \, a^{n+1}", font_size=26),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        step2 = VGroup(step2_label, step2_eqs).arrange(DOWN, aligned_edge=LEFT, buff=0.25)

        # === Step 3: hierarchical force ===
        step3_label = Text(
            "3. Hierarchical force: distant clumps look like point masses",
            font_size=24,
            weight=BOLD,
            color=GREEN_B,
        )
        step3_eq = MathTex(
            r"\mathcal{O}(N^2) \;\longrightarrow\; \mathcal{O}(N \log N)",
            font_size=34,
            color=GREEN_B,
        )
        step3 = VGroup(step3_label, step3_eq).arrange(DOWN, aligned_edge=LEFT, buff=0.25)

        full = VGroup(step1, step2, step3).arrange(DOWN, aligned_edge=LEFT, buff=0.5)
        full.next_to(heading, DOWN, buff=0.5)
        if full.height > 5.6:
            full.scale(5.6 / full.height)

        for s in (step1, step2, step3):
            self.play(FadeIn(s, shift=UP * 0.2), run_time=0.7)
            self.next_slide()

        cites = Text(
            "Verlet 1967  ·  Springel 2005  ·  Barnes & Hut 1986  ·  Salmon & Warren 1994",
            font_size=16,
            color=GREY_C,
        ).to_edge(DOWN, buff=0.3)
        self.play(FadeIn(cites))
        self.next_slide()
