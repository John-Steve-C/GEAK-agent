# Programming Guides OverviewÂ¶

This section provides a practical guide to writing highâperformance kernels with Tile Language (tileâlang). It mirrors the structure of a similar guide in another project and adapts it to tileâlang concepts and APIs.

  * Audience: Developers implementing custom GPU/CPU kernels with tileâlang

  * Prereqs: Basic Python, NumPy/Tensor concepts, and familiarity with GPU programming notions

  * Scope: Language basics, control flow, instructions, autotuning, and type system




## What Youâll LearnÂ¶

  * How to structure kernels with TileLangâs core DSL constructs

  * How to move data across global/shared/fragment and pipeline compute

  * How to apply autotuning to tile sizes and schedules

  * How to specify and work with dtypes in kernels




## Suggested Reading OrderÂ¶

  1. Language Basics

  2. Control Flow

  3. Instructions

  4. Autotuning

  5. Type System




## Related DocsÂ¶

  * Tutorials: see existing guides in `tutorials/`

  * Operators: examples in `deeplearning_operators/`




> NOTE: This is a draft scaffold. Fill in code snippets and benchmarks as APIs evolve.
