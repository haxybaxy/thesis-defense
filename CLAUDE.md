# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

A Manim Slides presentation for a thesis defense ("Hierarchical N-Body Simulation of Galactic Dynamics in WebGPU"). Each slide is a Python `Slide` subclass under `slides/`. The build pipeline renders per-scene video chunks, then `manim-slides convert` stitches them into `defense.html` / `.pdf` / `.pptx`.

`defense.html` is the deploy payload — `.github/workflows/deploy.yml` publishes it to GitHub Pages on every push to `main` that touches that file. Keep it committed and up to date when finalizing.

`defense_script.md` is the spoken narration synced to slide numbers (§0 Opening, §1 Motivation, §2 Approach, §3 Results, §4 Conclusion). When adding or reordering slides, update both this script and the `scenes` variable in `justfile`.

## Common commands

All workflows go through `just` (justfile recipes). Python is managed by `uv` (3.13 pinned in `.python-version`).

```bash
just sync              # uv sync — install/update deps
just render-all        # render every active scene at -ql (preview, fast iteration)
just render-final      # render every active scene at -qh (defense quality)
just present           # live presentation (arrow keys to navigate, q to quit)
just html              # build defense.html (self-contained, base64 videos)
just pdf               # build defense.pdf
just pptx              # build defense.pptx
just all               # render-final + html + pdf + pptx in one shot
just clean             # nuke media/ slides/files/ .manim-slides/
```

Render a single scene (fastest dev loop):

```bash
just render slides/title.py TitleSlide        # -ql by default
just render slides/title.py TitleSlide h      # -qh
# or directly:
uv run manim-slides render slides/title.py TitleSlide -ql -p   # -p previews
```

`present`, `html`, `pdf`, and `pptx` read the per-scene `.json` metadata that `manim-slides render` writes next to each `.py` file. **They will fail or silently use stale output if the scene hasn't been rendered first** — run `render-all` (or `render-final`) before exporting.

Requires LaTeX (MacTeX / TeX Live / MiKTeX) installed system-wide for `MathTex` to render; `ffmpeg` comes in transitively via manim.

## Architecture

### Scene registry lives in `justfile`, not Python

The `scenes` variable at the top of `justfile` is the canonical, ordered list of slides that appear in the final presentation. `render-all` / `render-final` enumerate explicit `(file, ClassName)` pairs because file names don't always match class names (e.g. `slides/motivation_browser.py` → `BrowserGap`, `slides/related_gap.py` → `TheGap`). **When adding or renaming a slide you must update three places:**

1. The `scenes := "..."` line (controls `present` / `convert`).
2. `render-all` and `render-final` recipes (controls render).
3. `defense_script.md` (narration sync).

`slides/` contains more `.py` files than are in the active `scenes` list — files like `discussion_*.py`, `related_*.py`, `motivation_galactic.py`, `results_rq1b.py`, `future_work.py`, `outline.py` are drafts/alternates that produced `.json` metadata in earlier passes but aren't currently presented. Don't assume every file is live; check `justfile`'s `scenes` first.

### Slide conventions

- Each file defines one or more `Slide` subclasses (subclass of `manim_slides.Slide`, which extends `manim.Scene`).
- `self.next_slide()` marks a pause point — the presenter must click to advance.
- `self.next_slide(loop=True)` makes the preceding animation loop until the next click — used for idle visuals while narrating.
- Class names are PascalCase; file names are snake_case and don't have to match.

### Render output

`manim-slides render <file.py> <ClassName>` produces:
- Per-segment `.mp4` files under `media/videos/<scene_name>/<quality>/` (gitignored).
- A `<ClassName>.json` file next to the source `.py` describing slide segments — **this is what `convert` and `present` consume**, and it's committed for the active scenes (you'll see them next to the `.py` files).

If a JSON file is stale (slide source changed but you didn't re-render), exports will use old video segments. When in doubt: `just clean && just render-all`.

### Deploy path

`.github/workflows/deploy.yml` triggers only on changes to `defense.html` or the workflow itself. It copies `defense.html` → `_site/index.html` and publishes to GitHub Pages. PDFs and PPTX are gitignored — only the HTML is the deployed artifact.
