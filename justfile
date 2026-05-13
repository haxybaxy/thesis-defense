scenes := "TitleSlide Outline \
GalacticDynamics DirectForces BrowserGap WebGPUIntro ResearchQuestions \
BarnesHutTheory GPUBarnesHutPriorWork LBVHConstruction WebGPUPerformanceLit TheGap \
PhysicsAndIntegrator BarnesHutIdea MortonCodes LBVHTraversal Pipeline SingleCodebase \
ExperimentalSetup WhereTimeIsSpent DirectVsTree WebGPUvsMetal CrossBackendVariation BrowserVsNative ThetaSweep \
PerRQDiscussion LiteratureComparison Limitations FutureWork Conclusion"

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
    # §0 — opening
    uv run manim-slides render slides/title.py TitleSlide --quality l
    uv run manim-slides render slides/outline.py Outline --quality l
    # §1 — motivation
    uv run manim-slides render slides/motivation_galactic.py GalacticDynamics --quality l
    uv run manim-slides render slides/forces.py DirectForces --quality l
    uv run manim-slides render slides/motivation_browser.py BrowserGap --quality l
    uv run manim-slides render slides/motivation_webgpu.py WebGPUIntro --quality l
    uv run manim-slides render slides/motivation_rqs.py ResearchQuestions --quality l
    # §2 — background & related work
    uv run manim-slides render slides/related_bh_theory.py BarnesHutTheory --quality l
    uv run manim-slides render slides/related_gpu_bh.py GPUBarnesHutPriorWork --quality l
    uv run manim-slides render slides/related_lbvh.py LBVHConstruction --quality l
    uv run manim-slides render slides/related_webgpu_perf.py WebGPUPerformanceLit --quality l
    uv run manim-slides render slides/related_gap.py TheGap --quality l
    # §3 — approach
    uv run manim-slides render slides/approach_physics.py PhysicsAndIntegrator --quality l
    uv run manim-slides render slides/barnes_hut.py BarnesHutIdea --quality l
    uv run manim-slides render slides/morton.py MortonCodes --quality l
    uv run manim-slides render slides/tree.py LBVHTraversal --quality l
    uv run manim-slides render slides/pipeline.py Pipeline --quality l
    uv run manim-slides render slides/approach_codebase.py SingleCodebase --quality l
    # §4 — experiments & results
    uv run manim-slides render slides/results_setup.py ExperimentalSetup --quality l
    uv run manim-slides render slides/results_rq1a.py WhereTimeIsSpent --quality l
    uv run manim-slides render slides/results_rq1b.py DirectVsTree --quality l
    uv run manim-slides render slides/results_rq2_metal.py WebGPUvsMetal --quality l
    uv run manim-slides render slides/results_rq2_backends.py CrossBackendVariation --quality l
    uv run manim-slides render slides/results_rq3.py BrowserVsNative --quality l
    uv run manim-slides render slides/results_quality.py ThetaSweep --quality l
    # §5 — discussion & conclusions
    uv run manim-slides render slides/discussion_per_rq.py PerRQDiscussion --quality l
    uv run manim-slides render slides/discussion_literature.py LiteratureComparison --quality l
    uv run manim-slides render slides/discussion_limits.py Limitations --quality l
    uv run manim-slides render slides/future_work.py FutureWork --quality l
    uv run manim-slides render slides/conclusion.py Conclusion --quality l

# Render all slides at high quality (for the actual defense)
render-final:
    # §0 — opening
    uv run manim-slides render slides/title.py TitleSlide --quality h
    uv run manim-slides render slides/outline.py Outline --quality h
    # §1 — motivation
    uv run manim-slides render slides/motivation_galactic.py GalacticDynamics --quality h
    uv run manim-slides render slides/forces.py DirectForces --quality h
    uv run manim-slides render slides/motivation_browser.py BrowserGap --quality h
    uv run manim-slides render slides/motivation_webgpu.py WebGPUIntro --quality h
    uv run manim-slides render slides/motivation_rqs.py ResearchQuestions --quality h
    # §2 — background & related work
    uv run manim-slides render slides/related_bh_theory.py BarnesHutTheory --quality h
    uv run manim-slides render slides/related_gpu_bh.py GPUBarnesHutPriorWork --quality h
    uv run manim-slides render slides/related_lbvh.py LBVHConstruction --quality h
    uv run manim-slides render slides/related_webgpu_perf.py WebGPUPerformanceLit --quality h
    uv run manim-slides render slides/related_gap.py TheGap --quality h
    # §3 — approach
    uv run manim-slides render slides/approach_physics.py PhysicsAndIntegrator --quality h
    uv run manim-slides render slides/barnes_hut.py BarnesHutIdea --quality h
    uv run manim-slides render slides/morton.py MortonCodes --quality h
    uv run manim-slides render slides/tree.py LBVHTraversal --quality h
    uv run manim-slides render slides/pipeline.py Pipeline --quality h
    uv run manim-slides render slides/approach_codebase.py SingleCodebase --quality h
    # §4 — experiments & results
    uv run manim-slides render slides/results_setup.py ExperimentalSetup --quality h
    uv run manim-slides render slides/results_rq1a.py WhereTimeIsSpent --quality h
    uv run manim-slides render slides/results_rq1b.py DirectVsTree --quality h
    uv run manim-slides render slides/results_rq2_metal.py WebGPUvsMetal --quality h
    uv run manim-slides render slides/results_rq2_backends.py CrossBackendVariation --quality h
    uv run manim-slides render slides/results_rq3.py BrowserVsNative --quality h
    uv run manim-slides render slides/results_quality.py ThetaSweep --quality h
    # §5 — discussion & conclusions
    uv run manim-slides render slides/discussion_per_rq.py PerRQDiscussion --quality h
    uv run manim-slides render slides/discussion_literature.py LiteratureComparison --quality h
    uv run manim-slides render slides/discussion_limits.py Limitations --quality h
    uv run manim-slides render slides/future_work.py FutureWork --quality h
    uv run manim-slides render slides/conclusion.py Conclusion --quality h

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
