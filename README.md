# Thesis Defense

Slides for my thesis defense, built with [Manim Slides](https://manim-slides.eertmans.be/).

## Setup

Managed with [`uv`](https://docs.astral.sh/uv/). Python version is pinned in `.python-version`; dependencies live in `pyproject.toml`.

```bash
# Sync .venv to match pyproject.toml + uv.lock
uv sync

# Activate the venv (optional — `uv run <cmd>` works without activation)
source .venv/bin/activate
```

To add a dependency: `uv add <package>`. To upgrade: `uv lock --upgrade`.

You will also need a working LaTeX installation for `MathTex` to render (e.g. MacTeX, TeX Live, or MiKTeX), plus `ffmpeg` (already a transitive dep of manim on most systems).

## Project layout

```
slides/
  title.py      — TitleSlide
  outline.py    — Outline
  equation.py   — Equation
```

Each file defines one `Slide` subclass. Add new slides as new files or as new classes within existing files.

## Common tasks (justfile)

Most workflows are wrapped in [`just`](https://github.com/casey/just) recipes. Run `just` for the full list.

```bash
just sync          # uv sync
just render-all    # render every scene at preview quality
just render-final  # render every scene at -qh for the defense
just present       # live presentation
just html          # export defense.html
just pdf           # export defense.pdf
just pptx          # export defense.pptx
just all           # render-final + html + pdf + pptx in one go
just clean         # wipe media output
```

When adding a new slide, update the `scenes` variable at the top of `justfile`.

> `present`, `html`, `pdf`, and `pptx` operate on already-rendered scenes (they read the per-scene `.json` metadata that `manim-slides render` produces). Run `just render-all` (or `render-final`) before exporting, or use `just all` to do it in one shot.

## Render

`manim-slides render` wraps `manim` and produces the per-slide video chunks Manim Slides needs.

```bash
uv run manim-slides render slides/title.py TitleSlide
uv run manim-slides render slides/outline.py Outline
uv run manim-slides render slides/equation.py Equation
```

Useful flags:
- `-ql` low quality (fast, for iteration)
- `-qh` high quality (final defense)
- `-p` preview after render

```bash
uv run manim-slides render -qh slides/title.py TitleSlide
```

## Present

Concatenate scenes into a live presentation. Navigate with arrow keys / space; `q` to quit.

```bash
uv run manim-slides present TitleSlide Outline Equation
```

## Export to PDF / HTML / PPTX

```bash
uv run manim-slides convert TitleSlide Outline Equation defense.html
uv run manim-slides convert --to=pdf TitleSlide Outline Equation defense.pdf
uv run manim-slides convert --to=pptx TitleSlide Outline Equation defense.pptx
```

## Adding a new slide

1. Create `slides/my_section.py`
2. Subclass `Slide`, implement `construct`, and use `self.next_slide()` to mark breaks
3. Use `self.next_slide(loop=True)` for looping animations (e.g. idle visuals while talking)
4. Render and add the class name to the `present` / `convert` list
