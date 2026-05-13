from manim import *
from manim_slides import Slide


class WebGPUPerformanceLit(Slide):
    def construct(self):
        heading = Text(
            "WebGPU performance: the budget",
            font_size=40,
            weight=BOLD,
        ).to_edge(UP, buff=0.6)
        self.play(Write(heading))
        self.next_slide()

        subhead = Text(
            "Two studies set the overhead we're working against",
            font_size=22,
            slant=ITALIC,
            color=GREY_B,
        ).next_to(heading, DOWN, buff=0.3)
        self.play(FadeIn(subhead))
        self.next_slide()

        # === Paper 1: Maczan 2026 ===
        m_title = Text("Maczan 2026", font_size=28, weight=BOLD, color=BLUE_B)
        m_topic = Text("Per-dispatch validation overhead", font_size=20, color=GREY_B)
        m_data = VGroup(
            Text("Vulkan: 24–36 µs", font_size=22),
            Text("Metal: 32–71 µs", font_size=22),
            Text("up to 2.2× vendor variation", font_size=22, color=ORANGE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        m_block = VGroup(m_title, m_topic, m_data).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        m_box = SurroundingRectangle(m_block, color=BLUE_B, buff=0.3, corner_radius=0.1, stroke_width=2)
        m_card = VGroup(m_box, m_block).move_to(LEFT * 3.2 + DOWN * 0.3)

        # === Paper 2: Sengupta et al. 2025 ===
        s_title = Text("Sengupta et al. 2025", font_size=28, weight=BOLD, color=YELLOW_B)
        s_topic = Text("WebGL → WebGPU reality check", font_size=20, color=GREY_B)
        s_data = VGroup(
            Text("1.4–2× overhead", font_size=22),
            Text("at scale, across workloads", font_size=22),
            Text("vs native execution", font_size=22, color=ORANGE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        s_block = VGroup(s_title, s_topic, s_data).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        s_box = SurroundingRectangle(s_block, color=YELLOW_B, buff=0.3, corner_radius=0.1, stroke_width=2)
        s_card = VGroup(s_box, s_block).move_to(RIGHT * 3.2 + DOWN * 0.3)

        self.play(FadeIn(m_card, shift=RIGHT * 0.2))
        self.next_slide()
        self.play(FadeIn(s_card, shift=LEFT * 0.2))
        self.next_slide()

        # interpretation
        tag = Text(
            "This is what we need to beat — or at least match.",
            font_size=22,
            slant=ITALIC,
            color=GREEN_B,
        ).to_edge(DOWN, buff=0.6)
        self.play(Write(tag))
        self.next_slide()
