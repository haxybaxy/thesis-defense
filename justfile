scenes := "TitleSlide Outline DirectForces BarnesHutIdea MortonCodes LBVHTraversal Pipeline Equation"

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
    uv run manim-slides render slides/forces.py DirectForces --quality l
    uv run manim-slides render slides/barnes_hut.py BarnesHutIdea --quality l
    uv run manim-slides render slides/morton.py MortonCodes --quality l
    uv run manim-slides render slides/tree.py LBVHTraversal --quality l
    uv run manim-slides render slides/pipeline.py Pipeline --quality l
    uv run manim-slides render slides/equation.py Equation --quality l

# Render all slides at high quality (for the actual defense)
render-final:
    uv run manim-slides render slides/title.py TitleSlide --quality h
    uv run manim-slides render slides/outline.py Outline --quality h
    uv run manim-slides render slides/forces.py DirectForces --quality h
    uv run manim-slides render slides/barnes_hut.py BarnesHutIdea --quality h
    uv run manim-slides render slides/morton.py MortonCodes --quality h
    uv run manim-slides render slides/tree.py LBVHTraversal --quality h
    uv run manim-slides render slides/pipeline.py Pipeline --quality h
    uv run manim-slides render slides/equation.py Equation --quality h

# Live presentation
present:
    uv run manim-slides present {{scenes}}

# Export to a single self-contained HTML file (videos embedded as base64)
html out="defense.html":
    uv run manim-slides convert --one-file {{scenes}} {{out}}

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
