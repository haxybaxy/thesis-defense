from manim import *
from manim_slides import Slide


class BrowserGap(Slide):
    def construct(self):
        heading = Text(
            "Why GPU compute belongs in the browser",
            font_size=36,
            weight=BOLD,
        ).to_edge(UP, buff=0.55)

        # === Left: native friction stack ===
        native_title = Text(
            "Native GPU code", font_size=26, weight=BOLD, color=RED_B
        ).move_to(LEFT * 3.6 + UP * 2.1)

        friction = [
            "right hardware",
            "right OS",
            "drivers",
            "build system",
            "container",
            "lab access",
        ]
        friction_rows = VGroup()
        for label in friction:
            t = Text(label, font_size=20, color=RED_B)
            box = SurroundingRectangle(
                t,
                color=RED_B,
                buff=0.13,
                corner_radius=0.06,
                stroke_width=1.5,
            ).set_fill("#3a1414", opacity=0.4)
            row = VGroup(box, t)
            friction_rows.add(row)

        friction_rows.arrange(DOWN, buff=0.13).next_to(native_title, DOWN, buff=0.4)

        # === Right: browser "click a link" ===
        browser_title = Text(
            "Browser GPU code", font_size=26, weight=BOLD, color=GREEN_B
        ).move_to(RIGHT * 3.6 + UP * 2.1)

        link_text = Text(
            "click a link",
            font_size=34,
            weight=BOLD,
            color=GREEN_B,
        )
        link_box = SurroundingRectangle(
            link_text,
            color=GREEN_B,
            buff=0.45,
            corner_radius=0.55,
            stroke_width=3,
        ).set_fill("#0e3a18", opacity=0.55)
        click_pill = VGroup(link_box, link_text).next_to(
            browser_title, DOWN, buff=1.0
        )

        vs_text = Text("vs", font_size=28, slant=ITALIC, color=GREY_B).move_to(
            ORIGIN + UP * 0.3
        )

        # === Bottom row: three audiences ===
        audience_labels = ["classroom", "outreach", "cross-platform research"]
        audience_chips = VGroup()
        for label in audience_labels:
            t = Text(label, font_size=20, color=BLUE_B)
            box = SurroundingRectangle(
                t,
                color=BLUE_B,
                buff=0.18,
                corner_radius=0.1,
                stroke_width=1.5,
            ).set_fill("#0e1f3a", opacity=0.45)
            audience_chips.add(VGroup(box, t))
        audience_chips.arrange(RIGHT, buff=0.55).to_edge(DOWN, buff=0.55)

        audience_label = Text(
            "who this unlocks:",
            font_size=18,
            slant=ITALIC,
            color=GREY_B,
        ).next_to(audience_chips, UP, buff=0.2)

        self.add(
            heading,
            native_title,
            friction_rows,
            browser_title,
            click_pill,
            vs_text,
            audience_label,
            audience_chips,
        )
        self.wait(0.1)
        self.next_slide()
