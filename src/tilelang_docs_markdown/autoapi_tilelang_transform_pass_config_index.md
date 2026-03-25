# tilelang.transform.pass_configÂ¶

## ClassesÂ¶

`PassConfigKey` | Pass configuration keys for TileLang compiler.  
---|---  
  
## Module ContentsÂ¶

_class _tilelang.transform.pass_config.PassConfigKeyÂ¶
    

Bases: `str`, `enum.Enum`

Pass configuration keys for TileLang compiler.

TL_SIMPLIFY _ = 'tl.Simplify'_Â¶
    

Configuration for TileLang simplification passes.

This is a dict-based config with the following options: \- transitively_prove_inequalities: bool, default False \- convert_boolean_to_and_of_ors: bool, default False \- apply_constraints_to_boolean_branches: bool, default False \- propagate_knowns_to_prove_conditional: bool, default False \- propagate_knowns_to_simplify_expressions: bool, default False \- enable_simplify_let_inline: bool, default True

Usage:
    

with tvm.transform.PassContext(config={
    

âtl.Simplifyâ: {âenable_simplify_let_inlineâ: False}

}):
    

mod = tl.transform.Simplify()(mod)

TL_SIMPLIFY_TRANSITIVELY_PROVE_INEQUALITIES _ = 'transitively_prove_inequalities'_Â¶
    

False

Type:
    

Enable transitive inequality proving in simplification. Default

TL_SIMPLIFY_CONVERT_BOOLEAN_TO_AND_OF_ORS _ = 'convert_boolean_to_and_of_ors'_Â¶
    

False

Type:
    

Convert boolean expressions to AND of ORs form. Default

TL_SIMPLIFY_APPLY_CONSTRAINTS_TO_BOOLEAN_BRANCHES _ = 'apply_constraints_to_boolean_branches'_Â¶
    

False

Type:
    

Apply constraints to simplify boolean branches. Default

TL_SIMPLIFY_PROPAGATE_KNOWNS_TO_PROVE_CONDITIONAL _ = 'propagate_knowns_to_prove_conditional'_Â¶
    

False

Type:
    

Propagate known values to prove conditionals. Default

TL_SIMPLIFY_PROPAGATE_KNOWNS_TO_SIMPLIFY_EXPRESSIONS _ = 'propagate_knowns_to_simplify_expressions'_Â¶
    

False

Type:
    

Propagate known values to simplify expressions. Default

TL_SIMPLIFY_ENABLE_LET_INLINE _ = 'enable_simplify_let_inline'_Â¶
    

True

Type:
    

Enable inlining of let statements during simplification. Default

TL_DISABLE_DATA_RACE_CHECK _ = 'tl.disable_data_race_check'_Â¶
    

False

Type:
    

Disable data race check in TileLang. Default

TL_DISABLE_WARP_SPECIALIZED _ = 'tl.disable_warp_specialized'_Â¶
    

False

Type:
    

Disable warp specialization optimization. Default

TL_ENABLE_FAST_MATH _ = 'tl.enable_fast_math'_Â¶
    

False if enabled, âuse_fast_math will be passed to nvcc

Type:
    

Enable fast math optimization. Default

TL_PTXAS_REGISTER_USAGE_LEVEL _ = 'tl.ptxas_register_usage_level'_Â¶
    

The PTXAS register usage level in [0, 10], which controls the aggressiveness of optimizations that affect register usage. Default: None

TL_ENABLE_PTXAS_VERBOSE_OUTPUT _ = 'tl.enable_ptxas_verbose_output'_Â¶
    

False

Type:
    

Enable ptxas verbose output. Default

TL_DEVICE_COMPILE_FLAGS _ = 'tl.device_compile_flags'_Â¶
    

Additional device compiler flags passed to nvcc/NVRTC.

Accepts either a string (parsed with shell-like splitting) or a list of strings. Typical usage is to provide extra include paths, defines or ptxas options, e.g.:

  * â-I/opt/include -DMY_SWITCH=1 âptxas-options=âverboseâ

  * [â-I/opt/includeâ, â-DMY_SWITCH=1â, ââptxas-options=âverboseâ]




These flags are appended to the compiler options used in the tvm_ffi CUDA compile callback. Default: None

TL_CONFIG_INDEX_BITWIDTH _ = 'tl.config_index_bitwidth'_Â¶
    

32

Type:
    

Bitwidth for configuration indices. Default

TL_DISABLE_TMA_LOWER _ = 'tl.disable_tma_lower'_Â¶
    

False

Type:
    

Disable TMA (Tensor Memory Access) lowering. Default

TL_DISABLE_SAFE_MEMORY_ACCESS _ = 'tl.disable_safe_memory_legalize'_Â¶
    

False

Type:
    

Disable safe memory access optimization. Default

TL_DISABLE_VECTORIZE_256 _ = 'tl.disable_vectorize_256'_Â¶
    

False

Type:
    

Disable usage of LDG/STG 256. Default

TL_ENABLE_ASYNC_COPY _ = 'tl.enable_async_copy'_Â¶
    

Enable lowering eligible global->shared copies to PTX cp.async.

When True (default), TileLang may lower: \- T.copy(global -> shared, â¦) to ptx_cp_async + commit + wait \- T.async_copy(global -> shared, â¦) to ptx_cp_async + commit (no wait) \- plain user-written global->shared copy stores (e.g. in T.Parallel) to

> ptx_cp_async + commit + wait

Important: Automatic cp.async lowering is gated by the surrounding loop context. TileLang will only auto-enable cp.async when the copy is observed inside a software-pipelined loop annotated with num_stages > 0 (e.g. created by T.Pipelined(â¦, num_stages=â¦) or by pipeline planning). Outside such loops, TileLang will prefer synchronous copy lowering even when this flag is True. You can request local cp.async injection on a specific parallel loop via T.Parallel(â¦, prefer_async=True).

When False, TileLang will avoid the cp.async lowering path for T.copy. Explicit T.async_copy still requires cp.async support and may error if it cannot be lowered.

Default: True

TL_ENABLE_LOWER_LDGSTG _ = 'tl.enable_lower_ldgstg'_Â¶
    

Enable non-predicated LDG/STG lowering for global memory access. When enabled, converts Ramp-based global buffer load/store to ldg/stg intrinsics. Default: False

TL_ENABLE_LOWER_LDGSTG_PREDICATED _ = 'tl.enable_lower_ldgstg_predicated'_Â¶
    

Enable predicated LDG/STG lowering. When True, predicated loads (if_then_else with else=0) and predicated stores (IfThenElse with empty then case) are lowered to ldg/stg intrinsics. Default: False

TL_ENABLE_VECTORIZE_PLANNER_VERBOSE _ = 'tl.enable_vectorize_planner_verbose'_Â¶
    

Enable verbose output for vectorize planner. When enabled, prints detailed information about each bufferâs inferred vector size and which buffer determines the final vectorization factor. Useful for debugging vectorization issues. Default: False

TL_DISABLE_WGMMA _ = 'tl.disable_wgmma'_Â¶
    

False

Type:
    

Disable usage of Hopper WGMMA. Default

TL_DEBUG_MERGE_SHARED_MEMORY_ALLOCATIONS _ = 'tl.debug_merge_shared_memory_allocations'_Â¶
    

False

Type:
    

Enable debug information for merge shared memory allocations. Default

TL_ENABLE_AGGRESSIVE_SHARED_MEMORY_MERGE _ = 'tl.enable_aggressive_shared_memory_merge'_Â¶
    

False

Type:
    

Enable aggressive merge of shared memory allocations. Default

TL_DISABLE_SHUFFLE_ELECT _ = 'tl.disable_shuffle_elect'_Â¶
    

False

Type:
    

Disable shuffle election optimization. Default

TL_DISABLE_LOOP_UNSWITCHING _ = 'tl.disable_loop_unswitching'_Â¶
    

False

Type:
    

Disable loop unswitching optimization. Default

TL_LOOP_UNSWITCHING_ALLOW_NON_TRIVIAL_ELSE _ = 'tl.loop_unswitching_allow_non_trivial_else'_Â¶
    

Allow loop unswitching even when the else-version of the loop body has side effects.

This is more aggressive and may increase code size. Default: False.

TL_DISABLE_THREAD_STORAGE_SYNC _ = 'tl.disable_thread_storage_sync'_Â¶
    

Disable thread storage synchronization pass. When enabled, disables the automatic insertion of thread synchronization barriers (e.g., __syncthreads()) for shared memory access coordination. This can be useful for performance optimization in cases where manual synchronization is preferred or when synchronization is not needed. Default: False

TL_FORCE_LET_INLINE _ = 'tl.force_let_inline'_Â¶
    

False

Type:
    

Force TileLang to inline let bindings during simplification. Default

TL_AST_PRINT_ENABLE _ = 'tl.ast_print_enable'_Â¶
    

False

Type:
    

Enable TIR AST printing for debugging purposes. Default

TL_LAYOUT_VISUALIZATION_ENABLE _ = 'tl.layout_visualization_enable'_Â¶
    

False

Type:
    

Enable layout inference visualization. Default

TL_LAYOUT_VISUALIZATION_FORMATS _ = 'tl.layout_visualization_formats'_Â¶
    

Layout visualization formats. Acceptable values: âpdfâ, âpngâ, âsvgâ, âallâ

TL_STORAGE_REWRITE_DETECT_INPLACE _ = 'tl.storage_rewrite_detect_inplace'_Â¶
    

Control StorageRewrite inplace detection.

When False (default) StorageRewrite keeps distinct temporaries for patterns such as dst[i] = f(src[i]), avoiding implicit aliasing:

`` read = T.allocate([1], T.int32, "local.var") write = T.allocate([1], T.int32, "local.var") read_buf = T.Buffer((1,), T.int32, data=read, scope="local.var") write_buf = T.Buffer((1,), T.int32, data=write, scope="local.var") write_buf[0] = read_buf[0] * 2 f(write_buf[0]) ``

Setting the flag to True allows StorageRewrite to reuse the read buffer for the write when it can prove the update is safely inplace, producing IR like:

`` read = T.allocate([1], T.int32, "local.var") read_buf = T.Buffer((1,), T.int32, data=read, scope="local.var") read_buf[0] = read_buf[0] * 2 f(read_buf[0]) ``

This reduces local memory usage but introduces aliasing between the buffers.

Usage:

```python from tilelang.transform import PassContext, PassConfigKey

with PassContext(
    

config={PassConfigKey.TL_STORAGE_REWRITE_DETECT_INPLACE.value: True}

):
    

mod = tilelang.transform.StorageRewrite()(mod)

```

TIR_ENABLE_EQUIV_TERMS_IN_CSE _ = 'tir.enable_equiv_terms_in_cse_tir'_Â¶
    

True

Type:
    

Enable equivalent terms in TIR Common Subexpression Elimination. Default

TIR_DISABLE_CSE _ = 'tir.disable_cse_tir'_Â¶
    

False

Type:
    

Disable TIR Common Subexpression Elimination. Default

TIR_SIMPLIFY _ = 'tir.Simplify'_Â¶
    

True

Type:
    

Enable/disable TIR simplification passes. Default

TIR_DISABLE_STORAGE_REWRITE _ = 'tir.disable_storage_rewrite'_Â¶
    

False

Type:
    

Disable storage rewrite optimization. Default

TIR_DISABLE_VECTORIZE _ = 'tir.disable_vectorize'_Â¶
    

False

Type:
    

Disable vectorization optimization. Default

TIR_USE_ASYNC_COPY _ = 'tir.use_async_copy'_Â¶
    

True

Type:
    

Enable asynchronous memory copy operations. Default

TIR_ENABLE_DEBUG _ = 'tir.enable_debug'_Â¶
    

False

Type:
    

Enable debug information in generated code. Default

TIR_MERGE_STATIC_SMEM _ = 'tir.merge_static_smem'_Â¶
    

True

Type:
    

Merge static shared memory allocations. Default

TIR_ADD_LOWER_PASS _ = 'tir.add_lower_pass'_Â¶
    

None

Type:
    

Additional lowering passes to be applied. Default

TIR_NOALIAS _ = 'tir.noalias'_Â¶
    

True

Type:
    

Enable pointer non-aliasing assumptions. Default

CUDA_KERNELS_OUTPUT_DIR _ = 'cuda.kernels_output_dir'_Â¶
    

empty string

Type:
    

Output directory for generated CUDA kernels. Default

TL_DISABLE_OUT_OF_BOUND_WARNING _ = 'tl.disable_out_of_bound_warning'_Â¶
    

False

Type:
    

Disable out-of-bound access warnings in safe memory access legalization. Default

TL_ENABLE_DUMP_IR _ = 'tl.enable_dump_ir'_Â¶
    

False

Type:
    

Enable dumping IR during lowering between passes. Default

TL_DUMP_IR_DIR _ = 'tl.dump_ir_path'_Â¶
    

./dump_ir/

Type:
    

Path to the directory where IR will be dumped. Default
