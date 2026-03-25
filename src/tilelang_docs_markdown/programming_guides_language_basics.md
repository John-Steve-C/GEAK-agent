# Language BasicsÂ¶

This page introduces the core TileLang (tileâlang) DSL that youâll use to write highâperformance kernels. It focuses on how to define a kernel, express iteration, move data across memory scopes, and run it with JIT.

The examples use the conventional aliases:
    
    
    import tilelang
    import tilelang.language as T
    from tilelang import jit
    

## 1\. Defining a Kernel with `@T.prim_func`Â¶

TileLang kernels are TIR (TVM IR) functions produced by the `@T.prim_func` decorator. Arguments are annotated with shapes and dtypes via `T.Tensor` or `T.Buffer`.

Note on dtypes

  * You can pass dtypes as a string (e.g., âfloat32â), a TileLang dtype (e.g., `T.float32`), or a framework dtype (e.g., `torch.float32`). TileLang normalizes all of these. See Type System for details.



    
    
    @T.prim_func
    def add_kernel(
        A: T.Tensor((N,), dtype),    # dtype could be 'float32' | T.float32 | torch.float32
        B: T.Tensor((N,), dtype),
        C: T.Tensor((N,), dtype),
    ):
        ...  # kernel body
    

  * Shapes may be concrete integers or symbolic. For symbolic, you can pass Python ints through the outer `@jit` wrapper (shown below), or annotate with `T.dyn` when you want a named symbolic dimension.



    
    
    # Named symbolic dimension (optional)
    K = T.dyn['K']
    @T.prim_func
    def uses_dyn(A: T.Tensor((K,), 'float32')):
        ...
    

### Dynamic symbolic dimensions: two waysÂ¶

TileLang supports two complementary ways to introduce symbolic (dynamic) dims:

  * Type-level annotations via `T.dyn[...]` (recommended for function signatures)

    * Use in `T.Tensor((T.dyn['K'], ...), dtype)` or bind once then reuse (as above).

    * Inside the kernel body, prefer reading from the bufferâs shape, e.g. `M = A.shape[0]`.

  * Term-level variables via `T.dynamic(name, dtype)`

    * Creates a TIR `tir.Var` you can use directly in expressions/loops.

    * Handy when you need to reference the dimension symbol in the body.



    
    
    # 1) Annotation-only symbol; read the bound size via shape
    K = T.dyn['K']  # dtype defaults to int32
    @T.prim_func
    def foo(A: T.Tensor((K,), 'float32')):
        N = A.shape[0]
        for i in T.serial(N):
            ...
    
    # 2) Explicit Var symbol usable in the body
    K = T.dynamic('K', 'int32')   # or T.dynamic('K') defaults to int32
    @T.prim_func
    def bar(A: T.Tensor((K,), 'float32')):
        for i in T.serial(K):
            ...
    

Notes

  * `T.symbolic(name, dtype)` is a deprecated alias of `T.dynamic`; prefer `T.dynamic`.

  * Under `@jit`, concrete sizes come from the actual tensor arguments at the first call.

  * Symbols in annotations do not need to be separate kernel arguments; TileLang binds them from argument shapes.




## 2\. Launching Work with `T.Kernel`Â¶

`with T.Kernel(...)` declares a launch context and creates block/thread bindings. For GPU backends, specify a grid and threads per block.
    
    
    with T.Kernel(grid_x, grid_y, threads=128) as (bx, by):
        ...  # bx/by are blockIdx.x/y
    

You rarely need raw thread indices; most kernels use structured loops (`T.serial`, `T.unroll`, `T.Parallel`, `T.Pipelined`) inside a `T.Kernel`.

## 3\. Loops and Control FlowÂ¶

Core loop constructs map to familiar hardware patterns:

  * `T.serial(start, stop[, step])`: plain forâloop

  * `T.unroll(start, stop[, step])`: unrolled loop

  * `T.Parallel(ext0, ext1, ...)`: nested parallel loops (elementwiseâfriendly)

  * `T.Pipelined(iters, num_stages=N)`: software pipelining for producer/consumer



    
    
    for i in T.serial(N):
        ...
    
    for i, j in T.Parallel(M, N):
        C[i, j] = A[i, j] + B[i, j]
    
    for k in T.Pipelined(T.ceildiv(K, BK), num_stages=3):
        # overlap copy/compute across stages
        ...
    

Conditionals use standard Python `if`/`else`. Guard edges with predicates when tile sizes do not divide problem sizes evenly.

## 4\. Memory Scopes and AllocationÂ¶

TileLang exposes key softwareâmanaged scopes:

  * Global: device memory (default for `T.Tensor` arguments)

  * Shared: onâchip, blockâvisible (`T.alloc_shared(shape, dtype)`)

  * Fragment and scalars: perâthread fragments and scalar vars but in Shared View (`T.alloc_fragment`, `T.alloc_var`)



    
    
    A_shared = T.alloc_shared((BM, BK), 'float16')
    B_shared = T.alloc_shared((BK, BN), 'float16')
    C_local  = T.alloc_fragment((BM, BN), 'float32')
    T.clear(C_local)  # zero accumulators
    

## 5\. Moving Data: `T.copy`Â¶

Use `T.copy(src, dst)` to move tiles between scopes. It accepts buffers, buffer regions, or buffer loads; extents are inferred or can be broadcast.
    
    
    # Global -> Shared (tile copy), extents inferred from dst
    T.copy(A[by * BM, ko * BK], A_shared)
    T.copy(B[ko * BK, bx * BN], B_shared)
    
    # Fragment -> Global (store back)
    T.copy(C_local, C[by * BM, bx * BN])
    

`T.copy` performs coalescing and scopeâspecific lowering during compilation.

If you need explicitly asynchronous global->shared prefetch for manual pipelining, use `T.async_copy(src, dst)`. Unlike `T.copy`, it does not auto-insert any wait: you must explicitly insert `T.ptx_wait_group(...)` before consuming `dst`. A shared-memory barrier is still required for cross-thread consumption, but in most TileLang programs you do not need to write it manually because `ThreadSync("shared")` will insert the necessary `T.tvm_storage_sync("shared")` before the first read from `dst`.

## 6\. A Minimal EndâtoâEnd Example (Vector Add)Â¶
    
    
    import tilelang
    import tilelang.language as T
    from tilelang import jit
    
    @jit  # infers target from tensors at first call
    def add(N: int, block: int = 256, dtype: str = 'float32'):
    
        @T.prim_func
        def add_kernel(
            A: T.Tensor((N,), dtype),
            B: T.Tensor((N,), dtype),
            C: T.Tensor((N,), dtype),
        ):
            with T.Kernel(T.ceildiv(N, block), threads=block) as bx:
                for i in T.Parallel(block):
                    gi = bx * block + i
                    # Optional â LegalizeSafeMemoryAccess inserts a guard when an access may be OOB
                    C[gi] = A[gi] + B[gi]
    
        return add_kernel
    
    # Host side (PyTorch shown; NumPy/DLPack also supported)
    import torch
    N = 1 << 20
    A = torch.randn(N, device='cuda', dtype=torch.float32)
    B = torch.randn(N, device='cuda', dtype=torch.float32)
    C = torch.empty(N, device='cuda', dtype=torch.float32)
    
    kernel = add(N)
    kernel(A, B, C)  # runs on GPU
    torch.testing.assert_close(C, A + B)
    

Notes

  * The `@jit` wrapper returns a callable kernel after the first compilation.

  * You can pass compileâtime tunables (tile sizes, dtypes) through the outer Python function and bake them into the generated TIR.




## 7\. Tiled GEMM SkeletonÂ¶

Below is a minimal pattern for a tiled GEMM using shared memory staging and a fragment accumulator. It mirrors the quickstart style found in the repository.
    
    
    @T.prim_func
    def gemm(
        A: T.Tensor((M, K), 'float16'),
        B: T.Tensor((K, N), 'float16'),
        C: T.Tensor((M, N), 'float16'),
    ):
        with T.Kernel(T.ceildiv(N, BN), T.ceildiv(M, BM), threads=128) as (bx, by):
            A_s = T.alloc_shared((BM, BK), 'float16')
            B_s = T.alloc_shared((BK, BN), 'float16')
            C_f = T.alloc_fragment((BM, BN), 'float32')
            T.clear(C_f)
    
            for ko in T.Pipelined(T.ceildiv(K, BK), num_stages=3):
                T.copy(A[by * BM, ko * BK], A_s)
                T.copy(B[ko * BK, bx * BN], B_s)
                T.gemm(A_s, B_s, C_f)  # lowered to tensorâcore/ISA specific kernels
    
            T.copy(C_f, C[by * BM, bx * BN])
    

## 8\. Debugging and PrintingÂ¶

Use `T.print` inside a kernel for quick introspection. TileLang emits printing from a single thread for shared/fragment scopes to avoid floods.
    
    
    T.print(C_f, msg='accumulator:')
    T.print(A_s, msg='A tile:')
    T.print(C[0], msg='C[0] = ')
    

## 9\. Where to Go NextÂ¶

  * Control flow details: see Programming Guides â Control Flow

  * Memory topics: see Programming Guides â (removed cache/layout); basics are covered inline

  * Autotuning tile sizes and mappings: Programming Guides â Autotuning

  * Operator examples (GEMM, GEMV, attention): see Deep Learning Operators



