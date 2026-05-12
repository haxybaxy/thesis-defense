scenes := "TitleSlide Outline Equation"

# List available recipes
default:
    @just --list

# Sync deps from pyproject.toml + uv.lock
sync:
    uv sync

# Render one scene: `just render slides/title.py TitleSlide` (optionally pass quality=h)
render file scene quality="l":
    uv run manim-slides render {{file}} {{scene}} --quality {{quality}}

# Render all slides at preview quality (fast)
render-all:
    uv run manim-slides render slides/title.py TitleSlide --quality l
    uv run manim-slides render slides/outline.py Outline --quality l
    uv run manim-slides render slides/equation.py Equation --quality l

# Render all slides at high quality (for the actual defense)
render-final:
    uv run manim-slides render slides/title.py TitleSlide --quality h
    uv run manim-slides render slides/outline.py Outline --quality h
    uv run manim-slides render slides/equation.py Equation --quality h

# Live presentation
present:
    uv run manim-slides present {{scenes}}

# Export to standalone HTML
html out="defense.html":
    uv run manim-slides convert {{scenes}} {{out}}

# Export to PDF
pdf out="defense.pdf":
    uv run manim-slides convert --to=pdf {{scenes}} {{out}}

# Export to PowerPoint
pptx out="defense.pptx":
    uv run manim-slides convert --to=pptx {{scenes}} {{out}}

# Render at -qh then export every format (full defense build)
all: render-final html pdf pptx

# Remove rendered media
clean:
    rm -rf media slides/files .manim-slides
