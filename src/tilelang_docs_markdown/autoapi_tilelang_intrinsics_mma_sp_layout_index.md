# tilelang.intrinsics.mma_sp_layoutÂ¶

## FunctionsÂ¶

`shared_16x16_to_mma_sp_layout_sr_a`(i, j) |   
---|---  
`shared_16x16_to_mma_sp_layout_sr_b`(i, j) |   
`shared_16x32_to_mma_sp_layout_sr_a`(i, j) |   
`shared_16x32_to_mma_sp_layout_sr_b`(i, j) |   
`shared_16x64_to_mma_sp_layout_sr_a`(i, j) |   
`shared_16x64_to_mma_sp_layout_sr_b`(i, j) |   
`mma_sp_load_a_32x4_to_shared_16x16_layout`(thread_id, ...) |   
`mma_sp_load_a_32x8_to_shared_16x32_layout`(thread_id, ...) |   
`mma_sp_load_a_32x16_to_shared_16x64_layout`(thread_id, ...) |   
`mma_sp_load_b_32x8_to_shared_16x16_layout`(thread_id, ...) |   
`mma_sp_load_b_32x16_to_shared_16x32_layout`(thread_id, ...) |   
`mma_sp_load_b_32x32_to_shared_16x64_layout`(thread_id, ...) |   
`get_logical_id_32bit`(thread_id) |   
`metadata_8bit_load_32x4_to_shared_16x4_layout_32bit`(...) |   
`metadata_16bit_load_32x2_to_shared_16x2_layout_32bit`(...) |   
`metadata_8bit_load_32x4_to_shared_16x4_layout_16bit`(...) |   
`metadata_16bit_load_32x2_to_shared_16x2_layout_16bit`(...) |   
`get_logical_id_8bit`(thread_id) |   
`metadata_8bit_load_32x4_to_shared_16x4_layout_8bit`(...) |   
`metadata_16bit_load_32x2_to_shared_16x4_layout_8bit`(...) |   
`metadata_32bit_load_32x1_to_shared_16x2_layout_8bit`(...) |   
`ldmatrix_trans_32x8_to_shared_16x16_layout`(thread_id, ...) |   
`ldmatrix_32x16_to_shared_32x16_layout`(thread_id, local_id) |   
`ldmatrix_trans_32x16_to_shared_16x32_layout`(thread_id, ...) |   
`ldmatrix_trans_32x32_to_shared_shared_16x64_layout`(...) |   
`get_ldmatrix_offset_b`(matrix, row_idx, col_idx, stride) |   
  
## Module ContentsÂ¶

tilelang.intrinsics.mma_sp_layout.shared_16x16_to_mma_sp_layout_sr_a(_i_ , _j_)Â¶
    

tilelang.intrinsics.mma_sp_layout.shared_16x16_to_mma_sp_layout_sr_b(_i_ , _j_)Â¶
    

tilelang.intrinsics.mma_sp_layout.shared_16x32_to_mma_sp_layout_sr_a(_i_ , _j_)Â¶
    

tilelang.intrinsics.mma_sp_layout.shared_16x32_to_mma_sp_layout_sr_b(_i_ , _j_)Â¶
    

tilelang.intrinsics.mma_sp_layout.shared_16x64_to_mma_sp_layout_sr_a(_i_ , _j_)Â¶
    

tilelang.intrinsics.mma_sp_layout.shared_16x64_to_mma_sp_layout_sr_b(_i_ , _j_)Â¶
    

tilelang.intrinsics.mma_sp_layout.mma_sp_load_a_32x4_to_shared_16x16_layout(_thread_id_ , _local_id_)Â¶
    

tilelang.intrinsics.mma_sp_layout.mma_sp_load_a_32x8_to_shared_16x32_layout(_thread_id_ , _local_id_)Â¶
    

tilelang.intrinsics.mma_sp_layout.mma_sp_load_a_32x16_to_shared_16x64_layout(_thread_id_ , _local_id_)Â¶
    

tilelang.intrinsics.mma_sp_layout.mma_sp_load_b_32x8_to_shared_16x16_layout(_thread_id_ , _local_id_)Â¶
    

tilelang.intrinsics.mma_sp_layout.mma_sp_load_b_32x16_to_shared_16x32_layout(_thread_id_ , _local_id_)Â¶
    

tilelang.intrinsics.mma_sp_layout.mma_sp_load_b_32x32_to_shared_16x64_layout(_thread_id_ , _local_id_)Â¶
    

tilelang.intrinsics.mma_sp_layout.get_logical_id_32bit(_thread_id_)Â¶
    

Parameters:
    

**thread_id** (_int_)

Return type:
    

int

tilelang.intrinsics.mma_sp_layout.metadata_8bit_load_32x4_to_shared_16x4_layout_32bit(_thread_id_ , _local_id_)Â¶
    

Parameters:
    

  * **thread_id** (_int_)

  * **local_id** (_int_)



Return type:
    

tuple[int, int]

tilelang.intrinsics.mma_sp_layout.metadata_16bit_load_32x2_to_shared_16x2_layout_32bit(_thread_id_ , _local_id_)Â¶
    

Parameters:
    

  * **thread_id** (_int_)

  * **local_id** (_int_)



Return type:
    

tuple[int, int]

tilelang.intrinsics.mma_sp_layout.metadata_8bit_load_32x4_to_shared_16x4_layout_16bit(_thread_id_ , _local_id_)Â¶
    

Parameters:
    

  * **thread_id** (_int_)

  * **local_id** (_int_)



Return type:
    

tuple[int, int]

tilelang.intrinsics.mma_sp_layout.metadata_16bit_load_32x2_to_shared_16x2_layout_16bit(_thread_id_ , _local_id_)Â¶
    

Parameters:
    

  * **thread_id** (_int_)

  * **local_id** (_int_)



Return type:
    

tuple[int, int]

tilelang.intrinsics.mma_sp_layout.get_logical_id_8bit(_thread_id_)Â¶
    

Parameters:
    

**thread_id** (_int_)

Return type:
    

int

tilelang.intrinsics.mma_sp_layout.metadata_8bit_load_32x4_to_shared_16x4_layout_8bit(_thread_id_ , _local_id_)Â¶
    

Parameters:
    

  * **thread_id** (_int_)

  * **local_id** (_int_)



Return type:
    

tuple[int, int]

tilelang.intrinsics.mma_sp_layout.metadata_16bit_load_32x2_to_shared_16x4_layout_8bit(_thread_id_ , _local_id_)Â¶
    

Parameters:
    

  * **thread_id** (_int_)

  * **local_id** (_int_)



Return type:
    

tuple[int, int]

tilelang.intrinsics.mma_sp_layout.metadata_32bit_load_32x1_to_shared_16x2_layout_8bit(_thread_id_ , _local_id_)Â¶
    

Parameters:
    

  * **thread_id** (_int_)

  * **local_id** (_int_)



Return type:
    

tuple[int, int]

tilelang.intrinsics.mma_sp_layout.ldmatrix_trans_32x8_to_shared_16x16_layout(_thread_id_ , _local_id_)Â¶
    

tilelang.intrinsics.mma_sp_layout.ldmatrix_32x16_to_shared_32x16_layout(_thread_id_ , _local_id_)Â¶
    

tilelang.intrinsics.mma_sp_layout.ldmatrix_trans_32x16_to_shared_16x32_layout(_thread_id_ , _local_id_)Â¶
    

tilelang.intrinsics.mma_sp_layout.ldmatrix_trans_32x32_to_shared_shared_16x64_layout(_thread_id_ , _local_id_)Â¶
    

tilelang.intrinsics.mma_sp_layout.get_ldmatrix_offset_b(_matrix_ , _row_idx_ , _col_idx_ , _stride_ , _dtype ='float16'_, _transposed =False_)Â¶
    

Parameters:
    

  * **matrix** (_Literal_ _[__'B'__]_)

  * **dtype** (_Literal_ _[__'float16'__,__'int8'__]_)

  * **transposed** ([_bool_](../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool"))



