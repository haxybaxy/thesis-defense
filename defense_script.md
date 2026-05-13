# Defense Script — Hierarchical N-Body Simulation of Galactic Dynamics in WebGPU

**Target length:** ~45 minutes at a comfortable presenter pace (~110 words / minute).
**Audience assumption:** technically literate committee — comfortable with parallel programming and basic physics, not necessarily with N-body methods or WebGPU specifics.
**How to use this script:** each slide block contains (1) the slide spec — existing or new, with a visual brief for new slides, (2) the narrator prose to read or paraphrase, (3) the citations and data anchors I lean on, and (4) a one-line transition out so the talk flows between slides.

Words in **bold** in narrator blocks are the beats I want to land — slow down on those.

---

## §0 — Opening (2 min, 2 slides)

### S0.1 — Title  *[existing: `slides/title.py`]*
**Timing:** ~30 s.
**Visual:** thesis title, your name, advisor, defense date — already animated.

**Narrator:**
> Good morning, and thank you for being here. The title is *Hierarchical N-Body Simulation of Galactic Dynamics in WebGPU*. In one sentence: I built a complete Barnes–Hut galactic-dynamics solver that runs entirely on the GPU using WebGPU, benchmarked it across four WebGPU implementations and against a native Metal baseline, and asked **how much it costs to put that solver in a browser**. Over the next forty-five minutes I'll walk you through why that question matters, how I built the solver, what the numbers look like, and what they imply for browser-based scientific computing.

**Transition:** "Here's the road map for the talk."

### S0.2 — Outline  *[existing: `slides/outline.py`]*
**Timing:** ~1 min 30 s.

**Narrator:**
> The talk has five parts. **First**, motivation — why N-body, and specifically why I think it belongs in a browser. **Second**, background and related work — the physics, the GPU algorithms this stands on, and where WebGPU fits relative to its predecessor. **Third**, the approach — the six-pass GPU pipeline at the heart of the thesis. **Fourth**, experiments and results, organised around three research questions: where the bottlenecks are, what abstraction overhead WebGPU imposes, and whether the browser is actually viable. **Fifth**, what those results mean, what they don't, and where this should go next. The three research questions are the spine of the whole talk — every result slide will tie back to one of them.

**Transition:** "Let me start with the motivation."

---

## §1 — Motivation & Problem Statement (6 min, 4 slides)

### S1.1 — What galactic dynamics computes  *[NEW]*
**Timing:** ~1 min 30 s.
**Slide file to build:** `slides/motivation_galactic.py`.
**Visual spec:** left panel — a still or short loop of a rotating disk simulation (you can reuse `assets/disk_step50.png` or render a fresh sequence from `disk_step1/5/20/50`). Right panel — three bullets: "N stars, all pulling on each other", "millions of timesteps", "spiral arms, cluster relaxation, halo dynamics". Bottom — citation chips for Binney & Tremaine 2008 and Portegies Zwart 2007.

**Narrator:**
> Everything you see on a galactic scale — spiral arms forming, star clusters relaxing, dark-matter haloes virialising — is the long-time integral of one very simple equation: Newton's law of gravity applied to a lot of particles at once. The physics is undergraduate. The **computation** is not. To resolve a single rotation of a Milky-Way-like disk, you need on the order of ten thousand timesteps at moderate resolution, and millions if you want to track relaxation timescales — that's Binney and Tremaine's textbook number. At each step, every particle feels a pull from every other one. The wall is **purely computational**: a galaxy at scientifically meaningful resolution is at least tens of thousands of particles, often millions, and you're integrating that for ten-to-the-six or ten-to-the-seven steps. So the question stops being "what's the right physics" and becomes "what's the right algorithm and the right hardware".

**Citations:** `@galacticdynamics2nded`, `@zwart_high-performance_2007`.
**Transition:** "And the algorithm question starts with a wall you hit immediately."

### S1.2 — The O(N²) wall  *[existing: `slides/forces.py`]*
**Timing:** ~1 min 30 s.
**Visual recap (already animated):** pair → all-pairs → quadratic explosion; the slide ends on N = 10⁵ → 10¹⁶ ops per step, in a pulsing red box.

**Narrator:**
> The naive approach is direct summation: for every particle, loop over every other particle and add up the contributions. It's beautifully simple and **embarrassingly parallel**, which is why it maps so well to a GPU. But it's quadratic. At a hundred thousand particles — small for modern cosmology — you're doing **ten-to-the-sixteenth operations per timestep**. That's the wall Sutter wrote about in 2005, the "free lunch is over" essay — single-thread performance flattened out, and the only way forward was parallelism. Christopher Fluke spelled out the consequence for astrophysics: if you want to keep doing science at this scale, you need to use the GPU. The whole field shifted to GPUs in the late 2000s, and the algorithm shifted too — from O(N²) direct summation to O(N log N) **hierarchical** methods. That's Barnes and Hut, 1986, which I'll get to in a moment.

**Citations:** `@freelunchover`, `@fluke2011`, `@barneshut`.
**Transition:** "But there's a second wall, separate from the algorithmic one, and it's about access."

### S1.3 — The browser-accessibility gap  *[NEW]*
**Timing:** ~1 min 30 s.
**Slide file to build:** `slides/motivation_browser.py`.
**Visual spec:** two-column comparison. Left column "WebGL" — vertex/fragment shaders only, no compute, data hidden in textures, no atomics, no recursive structures, "had to fake it". Right column "WebGPU" — compute shaders, storage buffers, atomics, workgroup memory, "actual GPGPU in the browser". Bottom — a small screenshot of a prior WebGL N-body demo with a caption noting the precision compromises.

**Narrator:**
> Here's the second wall. Native GPU codes — CUDA, Metal — are powerful but **gated**: you need the right hardware, the right OS, the right drivers, often a build system. That's fine in a research lab; it's not fine in a classroom, a public outreach setting, or anywhere you want a colleague to **click a link** and see your simulation. The browser is the universal runtime. But until very recently, the browser only had **WebGL** — which is a graphics API, not a compute API. WebGL forces every algorithm into vertex and fragment shaders, hides your data inside textures, doesn't expose atomics, and can't represent a hierarchical tree directly. Prior WebGL N-body demos exist, but they trade scientific rigor for visual plausibility: softened forces, reduced precision, no convergence check. WebGPU changes that. It's the first **GPGPU-capable** browser API: compute shaders, storage buffers, atomics, workgroup-shared memory. The same hardware, exposed honestly. That's what makes the question I'm asking actually answerable.

**Citations:** `@terascalewebviz`, `@realtimeclothsimulation`, `@realitycheck`, `@webgpu-spec`.
**Transition:** "So the question becomes: how much does WebGPU cost you, compared to going native?"

### S1.4 — Research questions  *[NEW]*
**Timing:** ~1 min 30 s.
**Slide file to build:** `slides/motivation_rqs.py`.
**Visual spec:** three RQ boxes stacked vertically, each labelled and one-line summarised. Animate them in sequentially.

**Narrator:**
> Three research questions, and the rest of the talk maps onto them.
>
> **RQ1: scalability and pipeline bottlenecks.** If you build a Barnes–Hut solver entirely on the GPU, what dominates the runtime? Tree construction? Force evaluation? Integration? You need this answered before you can optimise anything.
>
> **RQ2: WebGPU abstraction overhead.** WebGPU sits on top of the platform's native API — Metal in our case. How much does that abstraction cost you, compared to a hand-rolled Metal Barnes–Hut implementation?
>
> **RQ3: browser feasibility.** The same code, compiled once for native and once via Emscripten for the browser — how much slower is the browser, and does it stay slower as N grows or does the gap close?
>
> Three questions, three sets of experiments. Numerical quality — energy drift, momentum conservation — is a **cross-cutting concern**, not a fourth RQ. I'll touch on it where it matters, especially in the discussion.

**Transition:** "Before I get to my approach, let me situate this against the literature."

---

## §2 — Background & Related Work (10 min, 5 slides)

### S2.1 — N-body theory and the Barnes–Hut idea  *[NEW]*
**Timing:** ~2 min.
**Slide file to build:** `slides/related_bh_theory.py`.
**Visual spec:** three rows. Row 1 — Plummer softened force formula `a_i = G·Σ m_j(r_j − r_i)/(||r_j − r_i||² + ε²)^(3/2)`. Row 2 — leapfrog KDK diagram (½-kick, drift, ½-kick). Row 3 — Barnes–Hut octree with one node highlighted as a centre-of-mass replacement.

**Narrator:**
> The physics first. Newtonian gravity diverges at zero separation, so every N-body code uses **softening** — Plummer in our case — which replaces `1/r²` with `1/(r² + ε²)^(3/2)`. The softening length ε determines how close two particles can get before you stop resolving them. For the integrator, we use **leapfrog** — specifically the kick-drift-kick form. Leapfrog is **symplectic**: it preserves the symplectic structure of Hamiltonian flow, which means energy errors oscillate around zero rather than drifting monotonically the way Euler integration does. Verlet wrote this down in 1967; Springel's GADGET-2 code is the modern production reference.
>
> Now the algorithmic insight. Barnes and Hut in 1986 noticed that **distant clumps of mass look like point masses**. If you build a tree that groups particles spatially, you can replace a distant subtree with its centre of mass — that's one interaction instead of thousands. The opening criterion `maxExtent² / d² < θ²` decides whether a node is "far enough" — `θ` controls the accuracy–speed tradeoff. Salmon and Warren in 1994 proved that for `θ ≥ 1/3` you can construct adversarial particle distributions with unbounded error, which is why production codes stay below 0.7. The whole method takes you from O(N²) to **O(N log N)**.

**Citations:** `@verlet1967`, `@springel_2005`, `@barneshut`, `@skeletons_1994`.
**Transition:** "So that's the algorithm. The next question is how to run it on a GPU."

### S2.2 — GPU-accelerated Barnes–Hut  *[NEW]*
**Timing:** ~2 min.
**Slide file to build:** `slides/related_gpu_bh.py`.
**Visual spec:** timeline / table with three prior works. Columns: paper, hardware, headline number, what was limiting. Rows — Nyland 2009 (direct, GPU Gems 3, 10–30 GFLOP/s), Burtscher & Pingali 2011 (CUDA octree, ~10 ms at N=100k on GTX 280), Gaburov 2010 (CUDA octree, 15–25 % tree-build overhead).

**Narrator:**
> Three prior works set the bar.
>
> **Nyland and colleagues in 2009** showed direct O(N²) summation on the GPU in *GPU Gems 3*. It's beautifully parallel — every particle gets a thread, every thread loops over every other particle — and they hit ten to thirty GFLOP/s on commodity hardware. That's the baseline you have to beat with a tree.
>
> **Burtscher and Pingali in 2011** were the canonical GPU Barnes–Hut paper. They implemented the octree on a CUDA GTX 280 and got about ten milliseconds per step at a hundred thousand particles. Their key insight was that the **tree traversal**, not the tree construction, was the bottleneck — thread divergence within a warp is brutal when neighbouring particles take different traversal paths.
>
> **Gaburov and Bédorf in 2010** put numbers on the cost of building the tree: 15 to 25 percent of step time on their CUDA octree. That's significant. Part of the reason is that they kept the tree partially on the CPU.
>
> Three takeaways: direct GPU summation is the floor, tree traversal divergence is the ceiling, and tree construction is **not** free if you're not careful about where it lives.

**Citations:** `@fastnbody` (Nyland), `@cudabarnes` (Burtscher–Pingali), `@bedorf2010` (Bédorf et al.), `@fastalgo`.
**Transition:** "The state of the art for tree construction itself came two years later, from a different community entirely."

### S2.3 — LBVH and parallel tree construction  *[NEW]*
**Timing:** ~2 min.
**Slide file to build:** `slides/related_lbvh.py`.
**Visual spec:** three-panel flow. Panel 1 — particles in 3D space coloured by Morton-code value (Z-order curve overlaid). Panel 2 — sorted array of Morton keys, with arrows showing the Karras δ-function picking children by shared bit-prefix. Panel 3 — completed BVH with leaves at the bottom and root at the top. Bottom — citation: Karras 2012, Eurographics HPG.

**Narrator:**
> The breakthrough for GPU tree construction came from the **ray-tracing community**, not the N-body community. Tero Karras, at Eurographics 2012, showed how to build a binary radix tree in parallel: sort particles by **Morton code** — that's a 30-bit Z-order key that interleaves the bits of the x, y, and z coordinates — and then the tree's topology is implicit in the shared bit-prefixes of adjacent keys. Every internal node can be located independently, in parallel, by a δ-function comparing leading-zero counts. No locks, no recursion, no CPU.
>
> Why a **binary** tree (BVH) and not an **octree** for N-body? Three reasons. First, an octree has eight children per node, which means more branch decisions on a GPU that hates divergence. Second, a BVH has a fixed structure — exactly 2N−1 nodes for N particles — regardless of how the particles are distributed. That makes memory allocation predictable. Third, bottom-up parallel aggregation is cleaner: each node just waits for both children. Bédorf in 2010 also showed that **linearised, stackless** traversal is possible on GPU, which becomes important for the force kernel later.

**Citations:** `@maximizeparallel`, `@bedorf2010`.
**Transition:** "All of these — Karras, Burtscher, Gaburov — are CUDA. The browser question opens a whole separate platform stack."

### S2.4 — WebGPU as a compute platform  *[NEW]*
**Timing:** ~2 min.
**Slide file to build:** `slides/related_webgpu.py`.
**Visual spec:** layered diagram. Top — your C++/WGSL source. Middle layer — WebGPU API (W3C spec). Bottom — branches to native backends (Vulkan / Metal / D3D12) and to browser implementations (Dawn → Chrome, WebKit → Safari). Side callout — Maczan 2026's per-dispatch overhead numbers: 24–36 µs Vulkan, 32–71 µs Metal.

**Narrator:**
> WebGPU is the **W3C standard** that finally exposes general-purpose GPU computing in a portable way. The shading language is WGSL; the API surface is roughly analogous to Vulkan or Metal, but trimmed and made safe enough for the open web. Compute shaders. Storage buffers. Atomic operations. Workgroup-shared memory. The pieces you need.
>
> But there's a cost. Every dispatch crosses a **validation layer** — the browser has to prove that your shader can't access memory it shouldn't, can't run forever, can't crash the GPU. Maczan, in a 2026 study, measured this per-dispatch overhead across four GPU vendors and three browsers: roughly 24 to 36 microseconds on Vulkan, 32 to 71 microseconds on Metal, with up to 2.2× vendor variation. That's small if your dispatches do real work, **enormous** if they don't. Sengupta and colleagues in 2025 ran the broader "WebGL to WebGPU reality check": WebGPU is 1.4 to 2× slower than native at scale, depending on workload. Those numbers are the budget I'm working against.

**Citations:** `@webgpu-spec`, `@webgpu-gpuweb`, `@maczan2026`, `@realitycheck`.
**Transition:** "Which puts us in a very specific gap in the literature."

### S2.5 — The gap  *[NEW]*
**Timing:** ~1 min 30 s.
**Slide file to build:** `slides/related_gap.py`.
**Visual spec:** Venn-style or quadrant diagram. Axes: "full pipeline (tree+force+integrator)" vs "browser-deployable". Existing work clustered in the "full pipeline / native CUDA-Metal" quadrant. This thesis sits alone in "full pipeline / browser-capable".

**Narrator:**
> Pulling these threads together: GPU Barnes–Hut is well-established on **native CUDA and native Metal**. Browser GPU computing is documented for **isolated kernels** — vector adds, matmuls, single-pass reductions. But **no prior work**, to my knowledge, takes a complete tree-construction-plus-hierarchical-force-plus-symplectic-integration pipeline, runs it under WebGPU, benchmarks it across implementations, and compares it against a native baseline at scientifically meaningful N. That's the gap. That's what this thesis closes. And the closure is interesting precisely because the answer was not obvious before you measure it — the abstraction could have cost an order of magnitude, or it could have been free, and the result turned out to be much weirder than either.

**Transition:** "On to the actual approach."

---

## §3 — Approach (12 min, 7 slides)

### S3.1 — Physics, integrator, parameters  *[NEW]*
**Timing:** ~1 min 30 s.
**Slide file to build:** `slides/approach_physics.py`.
**Visual spec:** three small panels: (a) softened acceleration equation, (b) leapfrog KDK pseudocode with the three lines marked ½-kick / drift / ½-kick, (c) parameter table — default θ = 0.75, Δt = 10⁻³, ε = 0.5, G = 1, in N-body units.

**Narrator:**
> The starting point is the **softened acceleration** — Plummer with ε = 0.5 in our default units. Integration uses **kick-drift-kick leapfrog**: half-kick the velocity, full-drift the position, recompute forces, half-kick again. Symplectic, second-order accurate, time-reversible. Default timestep is ten-to-the-minus-three in code-units, default opening angle θ is 0.75. Those are conservative — Springel uses 0.5 to 0.7 in GADGET-2; Barnes and Hut's original 1986 paper used 1.0. Units throughout are the standard N-body convention: gravitational constant G = 1, total mass = 1, characteristic length = 1, which fixes the time unit at the system free-fall timescale.

**Citations:** `@verlet1967`, `@springel_2005`, `@barneshut`.
**Transition:** "The actual algorithmic mechanics, including the Barnes–Hut acceptance test, are next."

### S3.2 — Barnes–Hut mechanics  *[existing: `slides/barnes_hut.py`]*
**Timing:** ~1 min 30 s.
**Visual recap:** distant cluster contracting to centre-of-mass with monopole formula; opening criterion visualisation showing the θ angle and the s/d ratio; side-by-side octree vs BVH.

**Narrator:**
> The Barnes–Hut idea, visualised: a far-away clump of particles looks, to any given test particle, like a point mass at its centre of mass. The acceptance test is geometric — if `maxExtent² / d²` is less than `θ²`, accept the monopole; otherwise descend. One optimisation I added matters enough to call out: I precompute, per node, a **mass-adaptive opening radius** — `half-extent × (1 + 0.6 · log₂(max(M, 1)))`. The mass factor widens the radius for heavy nodes, which is conservative where gravity dominates, and the per-interaction test then collapses to a single distance comparison. That saved roughly **1.74× at N=100K**. On the structural side, I chose a binary BVH over an octree for the reasons in the literature review — fewer branches, predictable node count, cleaner bottom-up parallelism.

**Transition:** "Building the tree is the next piece, and that's where Morton codes come in."

### S3.3 — Morton codes and Z-order locality  *[existing: `slides/morton.py`]*
**Timing:** ~1 min 30 s.
**Visual recap:** Z-curve through a grid; bit-interleaving of three 10-bit coordinates into one 30-bit key; sorted array showing spatial neighbours becoming array neighbours.

**Narrator:**
> The Morton code is the bridge between 3D space and a 1D sort. You normalise each particle's position to the unit cube, quantise to 10 bits per axis, and **interleave** the bits — one bit of x, one of y, one of z, repeated ten times — into a single 30-bit integer. The genius of this is that **sorting** by Morton code preserves spatial locality. Particles that are close in 3D end up close in the sorted array, which means they end up close in memory, which means **cache-coherent traversal becomes essentially free** when the force kernel runs. A small but real effect: I measured roughly a 20% speedup at N=100K just from Morton-ordered particle access in the force kernel, compared to insertion order.

**Transition:** "And once the codes are sorted, you can build the tree topology in parallel."

### S3.4 — LBVH construction, six sub-passes  *[existing: `slides/tree.py`]*
**Timing:** ~2 min.
**Visual recap:** six labelled sub-passes — AABB reduce, Morton, radix sort, Karras topology, leaf init, bottom-up aggregation — plus the Karras δ-function reconstruction from sorted keys.

**Narrator:**
> Tree construction breaks into **six GPU passes**.
>
> **Pass 1: global AABB reduction.** A two-stage parallel reduction over all particle positions to find the bounding box, which you need to normalise coordinates for Morton coding.
>
> **Pass 2: Morton code generation.** Each thread computes one particle's 30-bit Morton key from its normalised position.
>
> **Pass 3: radix sort.** Codes and indices sorted together. Four passes, 8 bits each. O(N) total work. I chose radix over bitonic for the work-complexity, and over the more aggressive "onesweep" radix sort because onesweep needs fine-grained atomics that WebGPU's safety model doesn't expose efficiently.
>
> **Pass 4: Karras topology.** Each internal node found in parallel by the δ-function — comparing leading-zero counts of XOR'd adjacent keys.
>
> **Pass 5: leaf initialisation.** Each leaf gets its particle's position, mass, and a point AABB.
>
> **Pass 6: bottom-up aggregation.** Each internal node has an atomic counter that tracks child completion; the second child to arrive computes the merged AABB and the mass-weighted centre of mass. No global synchronisation — purely atomic-driven.
>
> The whole thing is **fully GPU-resident**. The tree never leaves GPU memory.

**Transition:** "The full per-timestep pipeline puts this together with the integrator."

### S3.5 — Six-pass timestep pipeline  *[existing: `slides/pipeline.py`]*
**Timing:** ~1 min 30 s.
**Visual recap:** ½-kick → drift → LBVH rebuild → BVH force → ½-kick. Expanded LBVH-rebuild box showing the six sub-passes from S3.4. Closing slide on WebGPU's structural advantage.

**Narrator:**
> Here's a full timestep. Half-kick the velocities. Drift the positions. Rebuild the LBVH from scratch — yes, every step, because particle order is fluid and rebuilding turns out to be cheap. Run the BVH force kernel: each thread, one particle, walks the tree with an explicit stack and accumulates acceleration. Half-kick the velocities again with the new acceleration. Optionally, every M steps, read positions and velocities back to the CPU for double-precision diagnostics.
>
> The structural point is that **everything except the optional diagnostics is GPU-resident**. There is no per-step CPU↔GPU transfer. That's the architectural decision that makes the WebGPU-vs-Metal comparison interesting later on — it's not that WebGPU is faster than Metal in any absolute sense, it's that this **architecture** avoids a class of overhead that the comparison baseline doesn't.

**Transition:** "Inside the force kernel, the traversal itself has its own mechanics."

### S3.6 — BVH traversal on the GPU  *[existing: `slides/tree.py`]*
**Timing:** ~1 min 30 s.
**Visual recap:** per-thread explicit stack pseudocode; trace example walking a small tree; thread-divergence callout.

**Narrator:**
> Each particle thread maintains an **explicit stack of node indices** — a fixed-depth array up to 64 entries, which is comfortably more than the tree depth at any N I tested. Pop a node; apply the opening test; if the node is far enough, accept the monopole and add its contribution; if not, push the two children. Repeat until the stack is empty.
>
> The cost — and this is exactly what Burtscher and Pingali warned about in 2011 — is **thread divergence**. Adjacent threads in the same SIMD group take different traversal paths because their particles see different geometric configurations. That's the fundamental reason force evaluation, not tree construction, ends up dominating the runtime. WGSL doesn't expose subgroup operations yet, so I can't do the divergence-reduction tricks that modern CUDA codes use. That's a limitation I'll come back to.

**Transition:** "One more piece — how this all gets packaged across native and the browser."

### S3.7 — Single codebase, four backends  *[NEW]*
**Timing:** ~1 min 30 s.
**Slide file to build:** `slides/approach_codebase.py`.
**Visual spec:** top — one box labelled "C++ / WGSL source". Four arrows down to four target boxes: wgpu-native (Rust binding, Metal underneath), Dawn (C++, Metal underneath), Chrome (WebAssembly via Emscripten), Safari (WebAssembly via Emscripten). Side box — Metal native baseline (UniSim) shown as an external comparator.

**Narrator:**
> The deployment story. **One C++/WGSL source tree** compiles to four different WebGPU targets. Native desktop uses **wgpu-native** — that's the Rust-based WebGPU implementation with Mozilla origins — and **Dawn** — Google's reference implementation, also native. Browser execution uses **Emscripten** to cross-compile the same C++ to WebAssembly, which then talks to **Chrome**'s and **Safari**'s built-in WebGPU implementations. Crucially, all four of these sit on top of **Metal** on the M2 machine I tested, so any performance variation isolates the WebGPU layer, not the GPU vendor.
>
> Separately, as a non-WebGPU reference, I use **UniSim** — an existing native Metal Barnes–Hut code, with a tree-serialisation bug patched in a fork — as the "what does a hand-rolled native code look like" comparator. That's what RQ2 is actually asking about.

**Transition:** "So that's the approach. The experiments are next."

---

## §4 — Experiments & Results (10 min, 7 slides)

### S4.1 — Experimental setup  *[NEW]*
**Timing:** ~1 min 30 s.
**Slide file to build:** `slides/results_setup.py`.
**Visual spec:** four quadrants. (a) Hardware: Apple M2, 8-core GPU, 4P+4E CPU, 16 GB unified memory, macOS 26.2. (b) Software: Apple Clang 17 with `-O3 -DNDEBUG`, wgpu-native via WebGPU-distribution v0.2.0, Dawn, Chrome 146, Safari 26.2. (c) Initial conditions: Plummer sphere, rotating exponential disk, two-body validation; N ∈ {100, 500, 1K, 2K, 5K, 10K, 25K, 50K, 100K}. (d) Protocol: 50 warm-up steps discarded, 100 steps measured, mean ± SD, 95% CI, CV-flagging.

**Narrator:**
> All measurements were taken on a single Apple M2 machine — 8-core integrated GPU, 16 GB unified memory, macOS 26.2. The build is release C++20, Clang 17, optimisation level three with assertions disabled. WebGPU implementations: wgpu-native, Dawn, Chrome 146, Safari 26.2 — all four routing through Metal on this hardware.
>
> Initial conditions: a **Plummer sphere** as the primary workload, a **rotating exponential disk** as the non-uniform stress case, and a two-body case for integrator validation. Particle counts span four orders of magnitude — a hundred up to a hundred thousand.
>
> The protocol matters: every measurement discards the first **50 timesteps** as warm-up — that's where pipeline compilation, buffer allocation, and shader caching stabilise — and reports statistics over the next **100 measured steps**. Mean and standard deviation; 95% confidence intervals via the t-distribution. Any run with a coefficient of variation above 10% gets flagged for investigation. For RQ2's cross-backend test I also use a **frozen-state protocol** — positions held constant, forces computed but not applied — which isolates per-dispatch overhead from physics-dependent variation.

**Transition:** "RQ1 first: where does the time go?"

### S4.2 — RQ1a: where time is spent  *[NEW]*
**Timing:** ~1 min 30 s.
**Slide file to build:** `slides/results_rq1a.py`.
**Visual spec:** two figures side-by-side. Left — `assets/fig_n_scaling_plummer.png` (mean runtime per timestep vs N). Right — `assets/fig_lbvh_breakdown.png` (stacked bar of the six LBVH passes at each N). Headline number boxes overlaid: "force = 94–99% of step", "tree < 0.35 ms at every N", "radix sort dominates within tree (34–41%)".

**Narrator:**
> The headline number: across **every** particle count tested, **force evaluation accounts for 94 to 99 percent of step time**. Tree construction stays below 0.35 milliseconds regardless of N. Let me put concrete numbers on it: at N = 1,000, we're at 5.86 ms per step total — 0.31 ms for the tree, 5.52 ms for the force. At N = 100,000, total is 180.11 ms per step — and the tree is still 0.28 ms. Force evaluation is 179.79 ms. The tree didn't get more expensive; the force traversal got 30 times more expensive.
>
> Inside tree construction, **radix sort** is the dominant sub-pass — 34 to 41 percent of construction time. The other five passes are roughly constant at 1.3 to 1.6 ms each. This is RQ1's answer: any optimisation effort that isn't aimed at the force traversal shader is wasted effort.

**Data anchors:** `tab:performance-summary`, `tab:lbvh-breakdown`, `results.typ:11-55`.
**Transition:** "But the force kernel has an alternative — direct summation. Is the tree even necessary?"

### S4.3 — RQ1b: direct vs tree, the real crossover  *[NEW]*
**Timing:** ~1 min 30 s.
**Slide file to build:** `slides/results_rq1b.py`.
**Visual spec:** `assets/fig_crossover.png` — dual-axis chart. Left y-axis runtime ms/step (lines for Direct and Tree). Right y-axis energy drift (log-scale, lines for both). N on x-axis. Callout box: "tree drifts 26× less at N=100K".

**Narrator:**
> Now this is the surprising one. On the Apple M2, **direct O(N²) summation is faster than the tree at every tested N**. At a hundred thousand particles, direct is 140 milliseconds per step; the tree is 180. That's because the M2's integrated GPU is small enough — eight cores — that the regular, branch-free, memory-coalesced access pattern of direct summation wins over the divergent traversal pattern of the tree.
>
> So why use a tree at all? **Energy drift**. At N=100K, direct summation accumulates an energy drift of 2.01 — which is to say, the system has effectively gained or lost more total energy than it started with. The tree, at the same N, accumulates 7.58×10⁻². That's a factor of **26× less drift**. The tree's monopole approximation produces consistent, symmetric errors that don't accumulate. Direct summation in 32-bit float — which is all WebGPU offers today — accumulates floating-point rounding catastrophically at this scale.
>
> The real crossover isn't runtime. It's **accuracy**. The tree is mandatory if you want the simulation to stay physically meaningful for more than a few hundred steps.

**Data anchors:** `tab:crossover`, `results.typ:87-108`.
**Transition:** "RQ2 next: what does WebGPU cost you relative to native Metal?"

### S4.4 — RQ2: WebGPU vs native Metal  *[NEW]*
**Timing:** ~1 min 30 s.
**Slide file to build:** `slides/results_rq2_metal.py`.
**Visual spec:** grouped bar chart, x-axis N (1K, 5K, 10K, 50K, 100K), two bars per group — WebGPU wgpu-native vs UniSim Metal. Annotate the WebGPU/Metal ratio above each pair: 2.0×, 0.73×, 0.52×, 0.54×, 0.35×. Highlight the crossover at N = 5K.

**Narrator:**
> Compared to UniSim — the patched native Metal Barnes–Hut baseline — WebGPU shows two regimes. **At N=1K, WebGPU is 2× slower than Metal** — 5.86 ms versus 2.94 ms. Per-dispatch overhead dominates at small workloads, and the WebGPU validation layer makes you pay that overhead.
>
> But the picture flips at N=5K. WebGPU is **faster than Metal** from there on out. At N=10K: 11 ms versus 21. At N=50K: 65 versus 122. At N=100K: 180 versus 517 — WebGPU is **2.9× faster than the native Metal baseline**.
>
> Here's the important caveat. This is **implementation-level**, not platform-level. My WebGPU code happens to have a fully GPU-resident pipeline; UniSim happens to have some CPU↔GPU coordination overhead in its tree-build path. Comparing them tells you that, all things considered, this WebGPU code is competitive — it does **not** tell you that WebGPU is inherently faster than Metal. What it does tell you is the abstraction is **not costing you an order of magnitude**, and at scale, the architectural decisions matter more than the API choice.

**Data anchors:** `tab:metal-comparison`, `results.typ:112-131`.
**Transition:** "WebGPU is a standard, but there are four implementations of it. How much do they vary?"

### S4.5 — RQ2: cross-backend variation  *[NEW]*
**Timing:** ~1 min 30 s.
**Slide file to build:** `slides/results_rq2_backends.py`.
**Visual spec:** `assets/fig_cross_backend.png` — grouped bar chart, four bars per N: Dawn, wgpu-native, Chrome, Safari. Highlight the 1.5× spread at N=100K.

**Narrator:**
> Frozen-state protocol again — positions constant, forces computed but not applied. This isolates per-dispatch overhead from any physics-dependent variation.
>
> Four WebGPU implementations on the **same Metal backend** show striking variation. **Dawn** has the lowest per-dispatch overhead at small N — 1.4 ms at N=1K — but scales worst, hitting 272 ms at N=100K. **wgpu-native** is the opposite: 5.9 ms at N=1K but the fastest at N=100K at 180 ms. **Chrome** sits in the middle. **Safari** is consistently the slowest. The spread at N=100K is **1.5× between fastest and slowest** — and these are all the same underlying GPU, the same shader, the same algorithm. The only difference is the WebGPU implementation. This is exactly the variation Maczan documented in the dispatch-overhead study — **backend choice alone produces substantial performance differences**, which is something every WebGPU practitioner needs to know.

**Data anchors:** `tab:cross-backend`, `results.typ:132-155`.
**Transition:** "RQ3 is the question I built this around: does it actually work in a browser?"

### S4.6 — RQ3: browser vs native  *[NEW]*
**Timing:** ~1 min 30 s.
**Slide file to build:** `slides/results_rq3.py`.
**Visual spec:** `assets/fig_web_native.png` — two lines: native wgpu-native, browser (Chrome via Emscripten). N on x-axis log-scale, ms/step on y-axis log-scale. Overlay the Chrome/native ratio at each N: 0.8×, 2.0×, 1.6×, 1.5×, 1.4×.

**Narrator:**
> Browser execution, same code, compiled through Emscripten. The story is not "browser is X percent slower" — it's **scaling-dependent**.
>
> At **N=1K, Chrome is actually faster than native wgpu-native** — 4.87 ms versus 5.86. The browser's WebGPU dispatch path has lower per-dispatch overhead than the Rust binding I was using. That was genuinely surprising; I checked it twice.
>
> Then it inverts. At **N=5K**, overhead peaks at **2.0×**. At N=10K, 1.6×. At N=50K, 1.5×. At **N=100K, the overhead narrows to 1.4×** as GPU compute time dominates both paths and the per-dispatch overhead becomes a smaller fraction of the whole.
>
> So the answer to RQ3 — is browser execution feasible at scientifically meaningful N — is **yes, with a roughly 1.4× penalty** that you can quote up front. That is, frankly, a lot less than I expected. And it's well within the range Sengupta and colleagues reported across other WebGPU workloads.

**Data anchors:** `tab:web-native`, `results.typ:156-177`.
**Transition:** "One more results slide before discussion — about precision."

### S4.7 — Numerical quality: the θ sweep  *[NEW]*
**Timing:** ~1 min.
**Slide file to build:** `slides/results_quality.py`.
**Visual spec:** small table, four rows for θ ∈ {0.3, 0.5, 0.7, 1.0}, columns ms/step and energy drift. Drift column on log scale.

**Narrator:**
> Quick precision note. Sweeping the opening angle θ at N = 5,000 shows that energy drift varies **two orders of magnitude**: 2.67×10⁻⁴ at θ=0.3 up to 3.31×10⁻² at θ=1.0. That matters because it means the precision constraint isn't **purely** 32-bit float — the **tree approximation itself** contributes substantially. If you read the early draft of this paper you'll find me claiming the 32-bit ceiling is the sole numerical constraint; that turned out to be wrong, and the θ sweep is the evidence.

**Data anchors:** `tab:theta-sweep`, results section in `discussion.typ`.
**Transition:** "Let me pull all of this together."

---

## §5 — Discussion & Future Work (5 min, 5 slides)

### S5.1 — What the results mean, per RQ  *[NEW]*
**Timing:** ~1 min 30 s.
**Slide file to build:** `slides/discussion_per_rq.py`.
**Visual spec:** three RQ boxes, each with a one-line answer underneath.

**Narrator:**
> Three RQs, three answers.
>
> **RQ1** — bottlenecks. Force evaluation is 94 to 99 percent of step time. LBVH construction is essentially free. **Optimise the traversal shader, ignore the tree.**
>
> **RQ2** — WebGPU abstraction overhead vs native Metal. Roughly 2× slower at N=1K where dispatch overhead dominates; **faster than the native Metal baseline at N≥5K** because of GPU-residency architecture; 2.9× faster at N=100K. But backend variation within WebGPU is itself 1.5× — implementation choice matters as much as the API.
>
> **RQ3** — browser feasibility. **1.4× overhead at scientifically meaningful N**, and the gap narrows as N grows. Browser deployment is viable today.

**Transition:** "Where does this sit relative to existing literature?"

### S5.2 — Agreement and disagreement with prior work  *[NEW]*
**Timing:** ~1 min 30 s.
**Slide file to build:** `slides/discussion_literature.py`.
**Visual spec:** two columns. Left: "Confirms" — Maczan 2026 (cross-backend variation), Sengupta 2025 (1.4–2× browser overhead range), Nyland 2009 (direct GPU throughput). Right: "Diverges" — Gaburov 2010 (tree-build was 15–25% there, < 0.2% here), Burtscher 2011 (their CUDA bottleneck was different).

**Narrator:**
> Three points of agreement, one of divergence.
>
> **Confirms Maczan 2026:** cross-backend dispatch overhead varies dramatically by implementation. We see the same 1.5× spread on this workload.
>
> **Confirms Sengupta 2025:** browser-vs-native WebGPU sits in the 1.4 to 2× range. We see 1.4 at the high-N end, 2.0 in the middle.
>
> **Confirms Nyland 2009:** direct GPU summation is still competitive throughput-wise; we're at 6.2×10⁹ interactions per second at N=5K on a small integrated GPU.
>
> **Diverges from Gaburov 2010:** they reported tree construction as 15 to 25 percent of step time on their CUDA octree. We're at less than 0.2 percent. The difference is **architectural** — Gaburov kept part of the tree CPU-side; we don't. The entire pipeline lives on the GPU, so there is **no per-step CPU-GPU transfer**, and the cost they were measuring simply doesn't exist in this architecture.

**Transition:** "I want to be honest about what this work doesn't do."

### S5.3 — Limitations  *[NEW]*
**Timing:** ~1 min.
**Slide file to build:** `slides/discussion_limits.py`.
**Visual spec:** bulleted list, six items.

**Narrator:**
> Six limitations I want to flag explicitly.
>
> One — **single hardware platform.** All numbers are M2-on-Metal. Discrete NVIDIA, AMD, Intel Arc are out of scope.
>
> Two — **32-bit float only.** WebGPU doesn't expose f64 in compute shaders yet.
>
> Three — **monopole only.** Production codes like GADGET-2 use quadrupole moments for better accuracy at given θ.
>
> Four — **UniSim baseline is patched.** The original had a tree-serialisation bug; we compare against a stabilised fork.
>
> Five — **no WGSL subgroup operations.** Limits the divergence-reduction tricks available in CUDA.
>
> Six — **global fixed timestep.** Production codes use per-particle adaptive timesteps.

**Transition:** "Which leads naturally to future work."

### S5.4 — Future work  *[NEW]*
**Timing:** ~1 min.
**Slide file to build:** `slides/future_work.py`.
**Visual spec:** five-item roadmap.

**Narrator:**
> Five extensions, in roughly increasing scope.
>
> **Adaptive per-particle timesteps.** Dense cores get small Δt, diffuse haloes get large Δt. Modest implementation cost, real accuracy win.
>
> **Cross-hardware and cross-browser benchmarking.** NVIDIA / Vulkan, Firefox, Intel Arc / D3D12. Test whether the M2 scaling characteristics generalise.
>
> **Quadrupole moments.** Three-by-three symmetric tensor per node. Modest storage cost, lets you push θ wider for the same accuracy.
>
> **64-bit precision** when WebGPU adds it. Would resolve the θ-vs-precision ambiguity in the energy drift data.
>
> **Multi-component galaxy models.** Bulge plus disk plus dark-matter halo. The architecture already supports heterogeneous masses.

**Transition:** "To wrap up."

### S5.5 — Conclusions and thank-you  *[NEW]*
**Timing:** ~1 min.
**Slide file to build:** `slides/conclusion.py`.
**Visual spec:** three-line summary, then a "thank you" line, then "questions?".

**Narrator:**
> One sentence per RQ.
>
> **RQ1: force evaluation dominates** — 94 to 99 percent of step time at every N. Optimise traversal.
>
> **RQ2: WebGPU's abstraction overhead is bounded and often invisible.** Faster than a native Metal baseline at N≥5K because of architectural choices, with measurable but tolerable backend variation.
>
> **RQ3: browser execution is viable** — 1.4× overhead at scientifically meaningful N, narrowing as GPU compute dominates.
>
> The bottom line: **WebGPU's abstraction overhead is low enough for interactive galactic-dynamics simulation without specialised hardware or vendor-locked APIs.** That changes who can run this code — it ships as a URL, no installation, no drivers, no containers. That's the practical contribution.
>
> Thank you to my advisor, to the committee for reading the thesis, and to anyone who's still listening at this point. I'm happy to take questions.

---

## Appendix — slide build checklist

23 new slides to build, grouped by section. Suggested filenames are placeholders; rename to match your existing `slides/` convention.

| Section | Slide ID | Suggested filename | Visual notes |
|---|---|---|---|
| §1 | S1.1 | `motivation_galactic.py` | disk evolution loop + three-bullet text |
| §1 | S1.3 | `motivation_browser.py` | WebGL vs WebGPU two-column |
| §1 | S1.4 | `motivation_rqs.py` | three RQ boxes, sequential animate-in |
| §2 | S2.1 | `related_bh_theory.py` | softened-accel formula + leapfrog + octree |
| §2 | S2.2 | `related_gpu_bh.py` | three-row prior-work table |
| §2 | S2.3 | `related_lbvh.py` | three-panel Morton-sort → Karras → BVH |
| §2 | S2.4 | `related_webgpu.py` | layered API diagram + Maczan numbers |
| §2 | S2.5 | `related_gap.py` | Venn / quadrant diagram |
| §3 | S3.1 | `approach_physics.py` | softened-accel + leapfrog KDK + parameters |
| §3 | S3.7 | `approach_codebase.py` | one source → four target boxes |
| §4 | S4.1 | `results_setup.py` | four-quadrant config card |
| §4 | S4.2 | `results_rq1a.py` | n-scaling + LBVH breakdown |
| §4 | S4.3 | `results_rq1b.py` | crossover chart (runtime + drift) |
| §4 | S4.4 | `results_rq2_metal.py` | WebGPU vs Metal grouped bars |
| §4 | S4.5 | `results_rq2_backends.py` | four-backend grouped bars |
| §4 | S4.6 | `results_rq3.py` | native vs Chrome lines |
| §4 | S4.7 | `results_quality.py` | θ sweep table |
| §5 | S5.1 | `discussion_per_rq.py` | three RQ answer boxes |
| §5 | S5.2 | `discussion_literature.py` | confirms / diverges two-column |
| §5 | S5.3 | `discussion_limits.py` | six-bullet limitations |
| §5 | S5.4 | `future_work.py` | five-item roadmap |
| §5 | S5.5 | `conclusion.py` | three-line summary + thank-you |

## Appendix — full citation list used in the script

`@galacticdynamics2nded`, `@zwart_high-performance_2007`, `@freelunchover`, `@fluke2011`, `@barneshut`, `@verlet1967`, `@springel_2005`, `@skeletons_1994`, `@fastnbody`, `@cudabarnes`, `@bedorf2010`, `@fastalgo`, `@maximizeparallel`, `@terascalewebviz`, `@realtimeclothsimulation`, `@realitycheck`, `@webgpu-spec`, `@webgpu-gpuweb`, `@maczan2026`.

Every key above corresponds to an entry I expect in `references.bib`. If any key has been renamed, search-and-replace in this script — the prose is unaffected.

## Appendix — anticipated Q&A

A short list of questions the committee is most likely to ask, with one-line crib-note answers.

1. **"Why is direct summation faster than the tree at N=100K on the M2?"** — Integrated GPU is small enough that coalesced memory access dominates. On a discrete NVIDIA GPU with many more SMs, the tree wins. The crossover is hardware-dependent.
2. **"Is the WebGPU > Metal result really about WebGPU?"** — No, it's about my pipeline being GPU-resident and UniSim's not being. The fair platform-level comparison would require a GPU-resident Metal Barnes–Hut, which is future work.
3. **"Why didn't you use subgroup operations?"** — WGSL doesn't expose them yet at the time of this work. They're in the WebGPU pipeline for a future spec revision.
4. **"How does 32-bit precision affect long-term integration?"** — Energy drift at θ=0.3 is 2.67×10⁻⁴ after 100 steps. Extrapolated to 10⁶ steps, drift becomes substantial. Adaptive timesteps and quadrupoles help; ultimately f64 is needed for cosmology-scale runs.
5. **"What's the largest N you ran?"** — 100,000 particles for full timing studies. The pipeline runs at higher N but timing CV exceeds the 10% threshold on this hardware.
6. **"Why not just use FMM?"** — Fast Multipole Method has lower asymptotic complexity (O(N)) but higher constants and more complex implementation. Barnes–Hut is the right tradeoff at the N range targeted here. FMM in WebGPU is a sensible follow-on.
