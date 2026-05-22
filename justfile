scenes := "TitleSlide DemoPhone WebGLExamples WebGLLimits ShaderVsCompute ResearchQuestions ComputeCentric IntegratorConcept IntegratorOrbits IntegratorEquations TreeBuildConcept MortonZCurve MortonInterleave MortonSort LBVHBuild ForceEvalConcept DirectForces AllPairsForces BarnesHutIdea LBVHTraversal ExperimentalSetup UniSimBaseline RQ1Statement NScaling WhereTimeIsSpent DirectVsTree RQ2Statement SingleCodebase CrossBackendVariation WebGPUvsMetal RQ3Statement BrowserVsNative Limitations FutureWork Conclusion BroaderImpact Pipeline ThetaSweep"

# List available recipes
default:
    @just --list

# Sync deps from pyproject.toml + uv.lock
sync:
    uv sync

# Render one scene: `just render slides/title.py TitleSlide` (optionally pass quality=h)
render file scene quality="l":
    uv run manim-slides render {{file}} {{scene}} --quality {{quality}}

# Render all active slides at preview quality (fast)
render-all:
    uv run manim-slides render slides/title.py TitleSlide --quality l
    uv run manim-slides render slides/demo_phone.py DemoPhone --quality l
    uv run manim-slides render slides/webgl_examples.py WebGLExamples --quality l
    uv run manim-slides render slides/motivation_webgl_limits.py WebGLLimits --quality l
    uv run manim-slides render slides/shader_vs_compute.py ShaderVsCompute --quality l
    uv run manim-slides render slides/motivation_rqs.py ResearchQuestions --quality l
    uv run manim-slides render slides/approach_compute_centric.py ComputeCentric --quality l
    uv run manim-slides render slides/integrator_concept.py IntegratorConcept --quality l
    uv run manim-slides render slides/integrator_euler.py IntegratorOrbits --quality l
    uv run manim-slides render slides/integrator_leapfrog.py IntegratorEquations --quality l
    uv run manim-slides render slides/approach_tree_concept.py TreeBuildConcept --quality l
    uv run manim-slides render slides/morton_zcurve.py MortonZCurve --quality l
    uv run manim-slides render slides/morton_interleave.py MortonInterleave --quality l
    uv run manim-slides render slides/morton_sort.py MortonSort --quality l
    uv run manim-slides render slides/tree.py LBVHBuild --quality l
    uv run manim-slides render slides/approach_force_eval_concept.py ForceEvalConcept --quality l
    uv run manim-slides render slides/forces.py DirectForces --quality l
    uv run manim-slides render slides/forces_all_pairs.py AllPairsForces --quality l
    uv run manim-slides render slides/barnes_hut.py BarnesHutIdea --quality l
    uv run manim-slides render slides/traversal.py LBVHTraversal --quality l
    uv run manim-slides render slides/results_setup.py ExperimentalSetup --quality l
    uv run manim-slides render slides/results_unisim.py UniSimBaseline --quality l
    uv run manim-slides render slides/rq_statements.py RQ1Statement --quality l
    uv run manim-slides render slides/results_rq1_scaling.py NScaling --quality l
    uv run manim-slides render slides/results_rq1a.py WhereTimeIsSpent --quality l
    uv run manim-slides render slides/results_rq1b.py DirectVsTree --quality l
    uv run manim-slides render slides/rq_statements.py RQ2Statement --quality l
    uv run manim-slides render slides/approach_codebase.py SingleCodebase --quality l
    uv run manim-slides render slides/results_rq2_backends.py CrossBackendVariation --quality l
    uv run manim-slides render slides/results_rq2_metal.py WebGPUvsMetal --quality l
    uv run manim-slides render slides/rq_statements.py RQ3Statement --quality l
    uv run manim-slides render slides/results_rq3.py BrowserVsNative --quality l
    uv run manim-slides render slides/discussion_limits.py Limitations --quality l
    uv run manim-slides render slides/future_work.py FutureWork --quality l
    uv run manim-slides render slides/conclusion.py Conclusion --quality l
    uv run manim-slides render slides/broader_impact.py BroaderImpact --quality l
    uv run manim-slides render slides/pipeline.py Pipeline --quality l
    uv run manim-slides render slides/results_quality.py ThetaSweep --quality l

# Render all active slides at high quality (for the actual defense)
render-final:
    uv run manim-slides render slides/title.py TitleSlide --quality h
    uv run manim-slides render slides/demo_phone.py DemoPhone --quality h
    uv run manim-slides render slides/webgl_examples.py WebGLExamples --quality h
    uv run manim-slides render slides/motivation_webgl_limits.py WebGLLimits --quality h
    uv run manim-slides render slides/shader_vs_compute.py ShaderVsCompute --quality h
    uv run manim-slides render slides/motivation_rqs.py ResearchQuestions --quality h
    uv run manim-slides render slides/approach_compute_centric.py ComputeCentric --quality h
    uv run manim-slides render slides/integrator_concept.py IntegratorConcept --quality h
    uv run manim-slides render slides/integrator_euler.py IntegratorOrbits --quality h
    uv run manim-slides render slides/integrator_leapfrog.py IntegratorEquations --quality h
    uv run manim-slides render slides/approach_tree_concept.py TreeBuildConcept --quality h
    uv run manim-slides render slides/morton_zcurve.py MortonZCurve --quality h
    uv run manim-slides render slides/morton_interleave.py MortonInterleave --quality h
    uv run manim-slides render slides/morton_sort.py MortonSort --quality h
    uv run manim-slides render slides/tree.py LBVHBuild --quality h
    uv run manim-slides render slides/approach_force_eval_concept.py ForceEvalConcept --quality h
    uv run manim-slides render slides/forces.py DirectForces --quality h
    uv run manim-slides render slides/forces_all_pairs.py AllPairsForces --quality h
    uv run manim-slides render slides/barnes_hut.py BarnesHutIdea --quality h
    uv run manim-slides render slides/traversal.py LBVHTraversal --quality h
    uv run manim-slides render slides/results_setup.py ExperimentalSetup --quality h
    uv run manim-slides render slides/results_unisim.py UniSimBaseline --quality h
    uv run manim-slides render slides/rq_statements.py RQ1Statement --quality h
    uv run manim-slides render slides/results_rq1_scaling.py NScaling --quality h
    uv run manim-slides render slides/results_rq1a.py WhereTimeIsSpent --quality h
    uv run manim-slides render slides/results_rq1b.py DirectVsTree --quality h
    uv run manim-slides render slides/rq_statements.py RQ2Statement --quality h
    uv run manim-slides render slides/approach_codebase.py SingleCodebase --quality h
    uv run manim-slides render slides/results_rq2_backends.py CrossBackendVariation --quality h
    uv run manim-slides render slides/results_rq2_metal.py WebGPUvsMetal --quality h
    uv run manim-slides render slides/rq_statements.py RQ3Statement --quality h
    uv run manim-slides render slides/results_rq3.py BrowserVsNative --quality h
    uv run manim-slides render slides/discussion_limits.py Limitations --quality h
    uv run manim-slides render slides/future_work.py FutureWork --quality h
    uv run manim-slides render slides/conclusion.py Conclusion --quality h
    uv run manim-slides render slides/broader_impact.py BroaderImpact --quality h
    uv run manim-slides render slides/pipeline.py Pipeline --quality h
    uv run manim-slides render slides/results_quality.py ThetaSweep --quality h

# Render every Slide subclass in a python file at -qh, then launch the presenter GUI.
# Usage: just preview slides/title.py
preview file:
    #!/usr/bin/env bash
    set -euo pipefail
    classes=$(grep -oE 'class [A-Za-z_][A-Za-z0-9_]*\(Slide\)' "{{file}}" | sed -E 's/^class //; s/\(Slide\)$//')
    if [ -z "$classes" ]; then
        echo "✗ no Slide subclass found in {{file}}" >&2
        exit 1
    fi
    for cls in $classes; do
        echo "→ rendering $cls from {{file}}"
        uv run manim-slides render "{{file}}" "$cls" --quality h
    done
    echo "→ presenting: $classes"
    uv run manim-slides present $classes

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
