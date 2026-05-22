from pathlib import Path

from manim import *
from manim_slides import Slide


class ClosingSim(Slide):
    """Looping sim as the closing image — book-ends the opening `DemoVideo`.

    Played immediately after the conclusion's "Thank you. Questions?" so the
    simulation visually backdrops the Q&A.
    """

    skip_reversing = True

    def construct(self):
        self.next_slide(src=Path("assets/sim.gif"))
