"""Drop-in `Text` replacement that works around the manimpango kerning bug.

Cairo's SVG backend rounds glyph x-coordinates to integer pixels, which shows
up as jumbled letter spacing at small font sizes. Rendering at a larger size
and scaling down preserves the same final visual size while shrinking the
rounding error proportionally.
"""

from manim import Text

_KERNING_SCALE = 3


def CleanText(text, *, font_size=48, **kwargs):
    t = Text(text, font_size=font_size * _KERNING_SCALE, **kwargs)
    t.scale(1 / _KERNING_SCALE)
    return t
