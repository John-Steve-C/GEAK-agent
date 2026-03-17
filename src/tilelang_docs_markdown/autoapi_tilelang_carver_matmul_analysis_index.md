# tilelang.carver.matmul_analysisÂ¶

A GEMM schedule rule for GPU operators.

## AttributesÂ¶

`logger` |   
---|---  
  
## ClassesÂ¶

`IterKind` | Iter kinds for GEMM-liked programs.  
---|---  
`IterTrait` |   
  
## FunctionsÂ¶

`collect_vars_from_expr`(prim_expr) |   
---|---  
`auto_inline_producers`(sch, block[, skip_blocks]) |   
`auto_inline_consumers`(sch, block) |   
`auto_inline_consumer_chain`(sch, block) |   
`find_first_similar_region`(regions, buffer) |   
`find_first_similar_buffer`(regions, buffer) |   
`find_last_producer_from_buffer`(sch, main_block, buffer) |   
`find_arg_idx_from_buffer_chain`(sch, main_block, buffer) | traverse to find the arg index from the buffer  
`make_iter_fusion_index_map`(traits, kind_order) |   
`detect_iter_traits`(block) | Detect iter traits based on the pattern C[S, I, J] += A[S, I, K] * B[S, J, K]  
`get_index_map`(block[, layout]) | Get index maps for the block  
`get_in_out_dtypes`(block) | Detect In/Out data types for the given block based on the analysis if read/write buffers.  
`get_dequantize_block`(sch, blocks) |   
`is_identity_or_transpose_block`(block_stmt) |   
`is_identity_block`(block_stmt) |   
`is_transpose_block`(block_stmt) |   
`inline_transpose_block`(sch, blocks) |   
`normalize_to_matmul`(sch, main_block[, layout]) |   
`get_tensorized_func_and_tags`(func, target[, layout, ...]) | transform function to matmul if necessary (e.g. transform conv2d with im2col)  
`get_propagate_map`([trans, dtype, matrix_name, index_dtype]) |   
`get_ladder_stage3_map`([dtype, index_dtype]) |   
`layout_propagate_chain`(sch, start_block, start_buffer, ...) |   
  
## Module ContentsÂ¶

tilelang.carver.matmul_analysis.loggerÂ¶
    

tilelang.carver.matmul_analysis.collect_vars_from_expr(_prim_expr_)Â¶
    

tilelang.carver.matmul_analysis.auto_inline_producers(_sch_ , _block_ , _skip_blocks =None_)Â¶
    

Parameters:
    

  * **sch** (_tvm.tir.Schedule_)

  * **block** (_tvm.tir.schedule.BlockRV_)

  * **skip_blocks** (_list_ _[__tvm.tir.schedule.BlockRV_ _]__|__None_)




tilelang.carver.matmul_analysis.auto_inline_consumers(_sch_ , _block_)Â¶
    

Parameters:
    

  * **sch** (_tvm.tir.Schedule_)

  * **block** (_tvm.tir.schedule.BlockRV_)




tilelang.carver.matmul_analysis.auto_inline_consumer_chain(_sch_ , _block_)Â¶
    

Parameters:
    

  * **sch** (_tvm.tir.Schedule_)

  * **block** (_tvm.tir.schedule.BlockRV_)




tilelang.carver.matmul_analysis.find_first_similar_region(_regions_ , _buffer_)Â¶
    

Parameters:
    

  * **regions** (_list_ _[__tvm.tir.BufferRegion_ _]_)

  * **buffer** (_tvm.tir.Buffer_)




tilelang.carver.matmul_analysis.find_first_similar_buffer(_regions_ , _buffer_)Â¶
    

Parameters:
    

  * **regions** (_list_ _[__tvm.tir.BufferRegion_ _]_)

  * **buffer** (_tvm.tir.Buffer_)




tilelang.carver.matmul_analysis.find_last_producer_from_buffer(_sch_ , _main_block_ , _buffer_)Â¶
    

Parameters:
    

**buffer** (_tvm.tir.Buffer_)

Return type:
    

tvm.tir.schedule.schedule.BlockRV | None

tilelang.carver.matmul_analysis.find_arg_idx_from_buffer_chain(_sch_ , _main_block_ , _buffer_)Â¶
    

traverse to find the arg index from the buffer

Parameters:
    

  * **sch** (_tvm.tir.Schedule_)

  * **main_block** (_tvm.tir.schedule.BlockRV_)

  * **buffer** (_tvm.tir.Buffer_)



Return type:
    

int

_class _tilelang.carver.matmul_analysis.IterKindÂ¶
    

Bases: `enum.Enum`

Iter kinds for GEMM-liked programs. We can simplify the computation to C[S, I, J] += A[S, I, K] * B[S, J, K], where I, J, K are fundamental axes for gemm and S represents all other spatial axes (e.g. batches) kIter_S: spatial axes kIter_I: I axes kIter_J: J axes kIter_K: K axes kIter_T: trivial axes (i.e. with extent 1)

kIter_S _ = 0_Â¶
    

kIter_I _ = 1_Â¶
    

kIter_J _ = 2_Â¶
    

kIter_K _ = 3_Â¶
    

kIter_T _ = 4_Â¶
    

_class _tilelang.carver.matmul_analysis.IterTraitÂ¶
    

kind _: IterKind_Â¶
    

extent _: tvm.tir.PrimExpr_Â¶
    

tilelang.carver.matmul_analysis.make_iter_fusion_index_map(_traits_ , _kind_order_)Â¶
    

Parameters:
    

  * **traits** (_list_ _[__IterTrait_ _]_)

  * **kind_order** (_list_ _[__IterKind_ _]_)



Return type:
    

tvm.tir.IndexMap

tilelang.carver.matmul_analysis.detect_iter_traits(_block_)Â¶
    

Detect iter traits based on the pattern C[S, I, J] += A[S, I, K] * B[S, J, K]

Parameters:
    

**block** (_tir.Block_) â The block to be analyzed

Returns:
    

**traits** â The detected iter traits for axes in A, B and C. None if the block does not match the pattern.

Return type:
    

Optional[Tuple[List[IterTrait]]]

tilelang.carver.matmul_analysis.get_index_map(_block_ , _layout =None_)Â¶
    

Get index maps for the block

Parameters:
    

  * **block** (_tir.Block_) â The block to be analyzed

  * **layout** (_List_ _[__str_ _]_) â the target layout index map to be used. ânâ for [i, k] layout âtâ for [k, j] layout âaâ for auto inference based on whether the last axis is reduction.



Returns:
    

**index_maps** â The index maps for the block, or None if the block is not a gemm-liked kernel

Return type:
    

Optional[Tuple[tir.IndexMap]]

tilelang.carver.matmul_analysis.get_in_out_dtypes(_block_)Â¶
    

Detect In/Out data types for the given block based on the analysis if read/write buffers.

Parameters:
    

**block** (_tvm.tir.Block_)

Return type:
    

tuple[str]

tilelang.carver.matmul_analysis.get_dequantize_block(_sch_ , _blocks_)Â¶
    

Return type:
    

tvm.tir.schedule.schedule.BlockRV | None

tilelang.carver.matmul_analysis.is_identity_or_transpose_block(_block_stmt_)Â¶
    

Parameters:
    

**block_stmt** (_tvm.tir.Block_)

Return type:
    

[bool](../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool")

tilelang.carver.matmul_analysis.is_identity_block(_block_stmt_)Â¶
    

Parameters:
    

**block_stmt** (_tvm.tir.Block_)

Return type:
    

[bool](../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool")

tilelang.carver.matmul_analysis.is_transpose_block(_block_stmt_)Â¶
    

Parameters:
    

**block_stmt** (_tvm.tir.Block_)

Return type:
    

[bool](../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool")

tilelang.carver.matmul_analysis.inline_transpose_block(_sch_ , _blocks_)Â¶
    

Parameters:
    

  * **sch** (_tvm.tir.Schedule_)

  * **blocks** (_list_ _[__tvm.tir.schedule.BlockRV_ _]_)




tilelang.carver.matmul_analysis.normalize_to_matmul(_sch_ , _main_block_ , _layout =None_)Â¶
    

Parameters:
    

  * **sch** (_tvm.tir.Schedule_)

  * **main_block** (_tvm.tir.schedule.schedule.BlockRV_)

  * **layout** (_list_ _[__str_ _]__|__None_)



Return type:
    

tvm.tir.Schedule | None

tilelang.carver.matmul_analysis.get_tensorized_func_and_tags(_func_ , _target_ , _layout =None_, _skip_normalize =False_, _allow_gemv =False_)Â¶
    

transform function to matmul if necessary (e.g. transform conv2d with im2col)

Parameters:
    

  * **func** (_tvm.tir.PrimFunc_)

  * **target** (_tvm.target.target.Target_)

  * **layout** (_list_ _[__str_ _]__|__None_)

  * **skip_normalize** ([_bool_](../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool"))

  * **allow_gemv** ([_bool_](../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool"))



Return type:
    

tuple[tvm.tir.PrimFunc, dict[str, list[int] | int]]

tilelang.carver.matmul_analysis.get_propagate_map(_trans =True_, _dtype ='float16'_, _matrix_name ='A'_, _index_dtype ='int32'_)Â¶
    

Parameters:
    

**trans** ([_bool_](../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool"))

tilelang.carver.matmul_analysis.get_ladder_stage3_map(_dtype ='float16'_, _index_dtype ='int32'_)Â¶
    

tilelang.carver.matmul_analysis.layout_propagate_chain(_sch_ , _start_block_ , _start_buffer_ , _end_block_ , _index_map_)Â¶
    

Parameters:
    

  * **sch** (_tvm.tir.Schedule_)

  * **start_block** (_tvm.tir.schedule.schedule.BlockRV_)

  * **start_buffer** (_tvm.tir.Buffer_)

  * **end_block** (_tvm.tir.schedule.schedule.BlockRV_)

  * **index_map** (_tvm.tir.IndexMap_)



