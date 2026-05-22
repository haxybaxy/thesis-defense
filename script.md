# Defense Script

Good morning everyone, and thank you for being here. I'm presenting my thesis, Hierarchical N-Body Simulation of Galactic Dynamics in WebGPU. Before I tell you what I did or why it matters, I want to show you what it actually looks like.

-play demo-

What you're watching right now is a galactic disk simulation. Tens of thousands of particles, each pulling on every other one through gravity. Integrated forward in time. Every frame on the screen is computed on this laptop right here directly from the browser in real time. No native binaries or servers needed.

The same simulation can also run on an android phone if you open the link, if you have an android phone, scan this QR Code and try it out!

This is probably the first time you see a GPU compute pipeline running end to end on the browser, because this simulation is a world's first. For years, Native GPU computation has been gated, requiring you to get the right Hardware, OS, drivers and much more. This is definitely alright in a research lab, but its not when you need your colleague to reproduce something on their laptop without any complicated setup. The world is currently moving towards enabling GPU compute to a wider consumer base, and the browser already acts as the universal runtime that we've been using to run our flash games and SaaS applications for the past decade.

And yet, when you look at browser-side GPU work for the past decade, you find almost nothing about real compute workloads. Why?

Most of the browser GPU research or literature available is mostly about graphics rendering and visual effects, where people usually assess equivalent particle simulations based on how they look rather than how accurate they are. This is because the most dominant web graphics API, WebGL, was only designed for visualizations, as it was built around vertices and pixels, forcing you to wrestle with it to no avail when you try and implement a fully fledged compute pipeline

What made this possible in the first place is the emergence of WebGPU, a brand new graphics API that allows us to write compute shaders. It introduced workgroup shared memory, storage buffers, atomics, and more. The compute pipeline that was needed was essentially impossible to express with WebGL. But now, with WebGPU, we are able to construct compute shaders.

Compute shaders are basically collections thousands of threads, where you can decide what each thread does and what memory it touches. The memory here is just a big storage buffer the GPU can read. As opposed to graphics shaders, which is more akin to a fixed assembly line, where vertices come in then go out, and the shape of the steps is locked.

A galaxy simulation is almost entirely compute work. Drawing the simulation is trivial, the expensive parts are building the spatial tree from scratch, walking the tree and stepping the integrator forward. All these parts have been constructed as compute shaders, and we could start with constructing the tree.
