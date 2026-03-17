# tilelang.intrinsics.utilsÂ¶

## FunctionsÂ¶

`get_ldmatrix_offset`(matrix, row_idx, col_idx, stride) |   
---|---  
`shared_16x16_to_mma_32x8_layout`(i, j) |   
`shared_16x32_to_mma_32x16_layout`(i, j) |   
`shared_32x16_to_mma_32x16_layout`(i, j) |   
`mma_store_index_map`(thread_id, local_id) |   
`mma_store_index_map_fp64`(thread_id, local_id) |   
`mfma_store_index_map`(thread_id, local_id) |   
`get_mma_micro_size`(dtype) | Return the MMA (Tensor Core) micro-tile dimensions for a given data type.  
  
## Module ContentsÂ¶

tilelang.intrinsics.utils.get_ldmatrix_offset(_matrix_ , _row_idx_ , _col_idx_ , _stride_ , _dtype ='float16'_, _transposed =False_)Â¶
    

Parameters:
    

  * **matrix** (_Literal_ _[__'A'__,__'B'__]_)

  * **dtype** (_Literal_ _[__'float16'__,__'int8'__]_)

  * **transposed** ([_bool_](../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool"))




tilelang.intrinsics.utils.shared_16x16_to_mma_32x8_layout(_i_ , _j_)Â¶
    

tilelang.intrinsics.utils.shared_16x32_to_mma_32x16_layout(_i_ , _j_)Â¶
    

tilelang.intrinsics.utils.shared_32x16_to_mma_32x16_layout(_i_ , _j_)Â¶
    

tilelang.intrinsics.utils.mma_store_index_map(_thread_id_ , _local_id_)Â¶
    

tilelang.intrinsics.utils.mma_store_index_map_fp64(_thread_id_ , _local_id_)Â¶
    

tilelang.intrinsics.utils.mfma_store_index_map(_thread_id_ , _local_id_)Â¶
    

tilelang.intrinsics.utils.get_mma_micro_size(_dtype_)Â¶
    

Return the MMA (Tensor Core) micro-tile dimensions for a given data type.

This function returns the micro tile sizes (x, y, k) used by MMA/Tensor Core operations. \- x: tile width in the output/result dimension \- y: tile height in the output/result dimension \- k: tile depth in the reduction/K dimension

Accepted dtype strings include âfloat16â, âint8â and some FP8 identifiers (âfloat8_e4m3â, âfloat8_e5m2â). For FP8 and int8 types the reduction depth (k) is 32; for float16 it is 16.

Returns:
    

(micro_size_x, micro_size_y, micro_size_k)

Return type:
    

tuple[int, int, int]

Parameters:
    

**dtype** (_Literal_ _[__'float16'__,__'int8'__]_)
