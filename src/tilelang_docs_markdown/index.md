# ð Welcome to Tile LanguageÂ¶

[GitHub](https://github.com/tile-ai/tilelang)

Tile Language (tile-lang) is a concise domain-specific language designed to streamline the development of high-performance GPU/CPU kernels (e.g., GEMM, Dequant GEMM, FlashAttention, LinearAttention). By employing a Pythonic syntax with an underlying compiler infrastructure on top of TVM, tile-lang allows developers to focus on productivity without sacrificing the low-level optimizations necessary for state-of-the-art performance.

GET STARTED

  * [Installation Guide](get_started/Installation.html)
    * [Installing with pip](get_started/Installation.html#installing-with-pip)
    * [Building from Source](get_started/Installation.html#building-from-source)
    * [Install Using Docker](get_started/Installation.html#install-using-docker)
    * [Install with Nightly Version](get_started/Installation.html#install-with-nightly-version)
    * [Install Configs](get_started/Installation.html#install-configs)
    * [Other Tips](get_started/Installation.html#other-tips)
  * [The Tile Language: A Brief Introduction](get_started/overview.html)
    * [Programming Interface](get_started/overview.html#programming-interface)
    * [Programming Interfaces](get_started/overview.html#programming-interfaces)
    * [Compilation Flow](get_started/overview.html#compilation-flow)
    * [Tile-based Programming Model](get_started/overview.html#tile-based-programming-model)
  * [Understanding Targets](get_started/targets.html)
    * [Common target strings](get_started/targets.html#common-target-strings)
    * [Creating targets programmatically](get_started/targets.html#creating-targets-programmatically)
    * [Discovering supported targets in code](get_started/targets.html#discovering-supported-targets-in-code)
    * [Troubleshooting tips](get_started/targets.html#troubleshooting-tips)



TUTORIALS

  * [Debugging Tile Language Programs](tutorials/debug_tools_for_tilelang.html)
  * [Auto-Tuning Techniques for Performance Optimization](tutorials/auto_tuning.html)
  * [Logging in Tilelang/TVM](tutorials/logging.html)



PROGRAMMING GUIDES

  * [Programming Guides Overview](programming_guides/overview.html)
  * [Language Basics](programming_guides/language_basics.html)
  * [Instructions](programming_guides/instructions.html)
  * [Control Flow](programming_guides/control_flow.html)
  * [Python Compatibility](programming_guides/python_compatibility.html)
  * [Autotuning](programming_guides/autotuning.html)
  * [Type System](programming_guides/type_system.html)



DEEP LEARNING OPERATORS

  * [ElementWise Operators](deeplearning_operators/elementwise.html)
  * [General Matrix-Vector Multiplication (GEMV)](deeplearning_operators/gemv.html)
  * [General Matrix-Matrix Multiplication with Tile Library](deeplearning_operators/matmul.html)
  * [Sparse Matrix-Matrix Multiplication with Tile Library](deeplearning_operators/matmul_sparse.html)
  * [ð Write High Performance FlashMLA with TileLang on Hopper](deeplearning_operators/deepseek_mla.html)



COMPILER INTERNALS

  * [LetStmt Inlining in TileLang](compiler_internals/letstmt_inline.html)
  * [InjectFenceProxy Pass](compiler_internals/inject_fence_proxy.html)
  * [Tensor Checks (Host-Side Auto-Validation)](compiler_internals/tensor_checks.html)



API Reference

  * [tilelang](autoapi/tilelang/index.html)



Privacy

  * [Privacy](privacy.html)


