# tilelang.intrinsics.mma_layoutÂ¶

## AttributesÂ¶

`shared_16x8_to_mma_32x4_layout_sr_a` |   
---|---  
`shared_16x8_to_mma_32x4_layout_sr_b` |   
`shared_16x8_to_mma_32x4_layout_rs_a` |   
`shared_16x8_to_mma_32x4_layout_rs_b` |   
`shared_16x16_to_mma_32x8_layout_sr_a` |   
`shared_16x16_to_mma_32x8_layout_sr_b` |   
`shared_16x16_to_mma_32x8_layout_rs_a` |   
`shared_16x16_to_mma_32x8_layout_rs_b` |   
`shared_16x32_to_mma_32x16_layout_sr_a` |   
`shared_16x32_to_mma_32x16_layout_sr_b` |   
`shared_16x32_to_mma_32x16_layout_rs_a` |   
`shared_16x32_to_mma_32x16_layout_rs_b` |   
  
## FunctionsÂ¶

`ldmatrix_32x4_to_shared_16x8_layout_a`(thread_id, local_id) |   
---|---  
`ldmatrix_32x4_to_shared_16x8_layout_b`(thread_id, local_id) |   
`ldmatrix_32x8_to_shared_16x16_layout`(thread_id, local_id) |   
`ldmatrix_trans_32x8_to_shared_16x16_layout`(thread_id, ...) |   
`ldmatrix_32x16_to_shared_16x32_layout_a`(thread_id, ...) |   
`ldmatrix_32x16_to_shared_16x32_layout_b`(thread_id, ...) |   
`mma_store_32x8_to_shared_16x16_layout`(thread_id, local_id) |   
`mma_store_32x2_to_shared_8x8_layout_fp64`(thread_id, ...) |   
`shared_16x8_to_mma_a_32x4_layout`(i, j) |   
`shared_16x8_to_mma_a_32x4_layout_trans`(i, j) |   
`shared_16x8_to_mma_b_32x4_layout`(i, j) |   
`shared_16x8_to_mma_b_32x4_layout_trans`(i, j) |   
`shared_16x16_to_mma_a_32x8_layout`(i, j) |   
`shared_16x16_to_mma_a_32x8_layout_trans`(i, j) |   
`shared_16x16_to_mma_b_32x8_layout`(i, j) |   
`shared_16x16_to_mma_b_32x8_layout_trans`(i, j) |   
`shared_16x32_to_mma_a_32x16_layout`(i, j) |   
`shared_32x16_to_mma_a_32x16_layout_trans`(i, j) |   
`shared_16x32_to_mma_b_32x16_layout`(i, j) |   
`shared_32x16_to_mma_b_32x16_layout_trans`(i, j) |   
`mma_32x8_to_shared_16x16_layout`(thread_id, local_id) |   
`mma_load_a_32x4_to_shared_16x8_layout`(thread_id, local_id) |   
`mma_load_b_32x4_to_shared_16x8_layout`(thread_id, local_id) |   
`mma_load_a_32x16_to_shared_16x32_layout`(thread_id, ...) |   
`mma_load_a_32x8_to_shared_16x16_layout`(thread_id, local_id) | groupID = %laneid >> 2  
`mma_load_b_32x16_to_shared_16x32_layout`(thread_id, ...) |   
`mma_load_b_32x8_to_shared_16x16_layout`(thread_id, local_id) | groupID = %laneid >> 2  
`shared_16x16_to_mma_32x8_smoothlayout`(i, j) |   
`shared_16x32_to_mma_32x16_smoothlayout`(i, j) |   
`shared_32x16_to_mma_32x16_smoothlayout`(i, j) |   
`get_swizzle_layout`(row_idx, col_idx, row_size, dtype) |   
`make_mma_swizzle_layout`(shared_buf[, is_smooth]) |   
  
## Module ContentsÂ¶

tilelang.intrinsics.mma_layout.ldmatrix_32x4_to_shared_16x8_layout_a(_thread_id_ , _local_id_)Â¶
    

tilelang.intrinsics.mma_layout.ldmatrix_32x4_to_shared_16x8_layout_b(_thread_id_ , _local_id_)Â¶
    

tilelang.intrinsics.mma_layout.ldmatrix_32x8_to_shared_16x16_layout(_thread_id_ , _local_id_)Â¶
    

tilelang.intrinsics.mma_layout.ldmatrix_trans_32x8_to_shared_16x16_layout(_thread_id_ , _local_id_)Â¶
    

tilelang.intrinsics.mma_layout.ldmatrix_32x16_to_shared_16x32_layout_a(_thread_id_ , _local_id_)Â¶
    

tilelang.intrinsics.mma_layout.ldmatrix_32x16_to_shared_16x32_layout_b(_thread_id_ , _local_id_)Â¶
    

tilelang.intrinsics.mma_layout.mma_store_32x8_to_shared_16x16_layout(_thread_id_ , _local_id_)Â¶
    

tilelang.intrinsics.mma_layout.mma_store_32x2_to_shared_8x8_layout_fp64(_thread_id_ , _local_id_)Â¶
    

tilelang.intrinsics.mma_layout.shared_16x8_to_mma_a_32x4_layout(_i_ , _j_)Â¶
    

tilelang.intrinsics.mma_layout.shared_16x8_to_mma_a_32x4_layout_trans(_i_ , _j_)Â¶
    

tilelang.intrinsics.mma_layout.shared_16x8_to_mma_b_32x4_layout(_i_ , _j_)Â¶
    

tilelang.intrinsics.mma_layout.shared_16x8_to_mma_b_32x4_layout_trans(_i_ , _j_)Â¶
    

tilelang.intrinsics.mma_layout.shared_16x8_to_mma_32x4_layout_sr_aÂ¶
    

tilelang.intrinsics.mma_layout.shared_16x8_to_mma_32x4_layout_sr_bÂ¶
    

tilelang.intrinsics.mma_layout.shared_16x8_to_mma_32x4_layout_rs_aÂ¶
    

tilelang.intrinsics.mma_layout.shared_16x8_to_mma_32x4_layout_rs_bÂ¶
    

tilelang.intrinsics.mma_layout.shared_16x16_to_mma_a_32x8_layout(_i_ , _j_)Â¶
    

tilelang.intrinsics.mma_layout.shared_16x16_to_mma_a_32x8_layout_trans(_i_ , _j_)Â¶
    

tilelang.intrinsics.mma_layout.shared_16x16_to_mma_b_32x8_layout(_i_ , _j_)Â¶
    

tilelang.intrinsics.mma_layout.shared_16x16_to_mma_b_32x8_layout_trans(_i_ , _j_)Â¶
    

tilelang.intrinsics.mma_layout.shared_16x16_to_mma_32x8_layout_sr_aÂ¶
    

tilelang.intrinsics.mma_layout.shared_16x16_to_mma_32x8_layout_sr_bÂ¶
    

tilelang.intrinsics.mma_layout.shared_16x16_to_mma_32x8_layout_rs_aÂ¶
    

tilelang.intrinsics.mma_layout.shared_16x16_to_mma_32x8_layout_rs_bÂ¶
    

tilelang.intrinsics.mma_layout.shared_16x32_to_mma_a_32x16_layout(_i_ , _j_)Â¶
    

tilelang.intrinsics.mma_layout.shared_32x16_to_mma_a_32x16_layout_trans(_i_ , _j_)Â¶
    

tilelang.intrinsics.mma_layout.shared_16x32_to_mma_b_32x16_layout(_i_ , _j_)Â¶
    

tilelang.intrinsics.mma_layout.shared_32x16_to_mma_b_32x16_layout_trans(_i_ , _j_)Â¶
    

tilelang.intrinsics.mma_layout.shared_16x32_to_mma_32x16_layout_sr_aÂ¶
    

tilelang.intrinsics.mma_layout.shared_16x32_to_mma_32x16_layout_sr_bÂ¶
    

tilelang.intrinsics.mma_layout.shared_16x32_to_mma_32x16_layout_rs_aÂ¶
    

tilelang.intrinsics.mma_layout.shared_16x32_to_mma_32x16_layout_rs_bÂ¶
    

tilelang.intrinsics.mma_layout.mma_32x8_to_shared_16x16_layout(_thread_id_ , _local_id_)Â¶
    

tilelang.intrinsics.mma_layout.mma_load_a_32x4_to_shared_16x8_layout(_thread_id_ , _local_id_)Â¶
    

tilelang.intrinsics.mma_layout.mma_load_b_32x4_to_shared_16x8_layout(_thread_id_ , _local_id_)Â¶
    

tilelang.intrinsics.mma_layout.mma_load_a_32x16_to_shared_16x32_layout(_thread_id_ , _local_id_)Â¶
    

tilelang.intrinsics.mma_layout.mma_load_a_32x8_to_shared_16x16_layout(_thread_id_ , _local_id_)Â¶
    

groupID = %laneid >> 2 threadID_in_group = %laneid % 4

row = groupID for ai where 0 <= i < 2 || 4 <= i < 6
    

groupID + 8 Otherwise

col = (threadID_in_group * 2) + (i & 0x1) for ai where i < 4 (threadID_in_group * 2) + (i & 0x1) + 8 for ai where i >= 4

tilelang.intrinsics.mma_layout.mma_load_b_32x16_to_shared_16x32_layout(_thread_id_ , _local_id_)Â¶
    

tilelang.intrinsics.mma_layout.mma_load_b_32x8_to_shared_16x16_layout(_thread_id_ , _local_id_)Â¶
    

groupID = %laneid >> 2 threadID_in_group = %laneid % 4

row = (threadID_in_group * 2) + (i & 0x1) for bi where i < 2
    

(threadID_in_group * 2) + (i & 0x1) + 8 for bi where i >= 2

col = groupID

tilelang.intrinsics.mma_layout.shared_16x16_to_mma_32x8_smoothlayout(_i_ , _j_)Â¶
    

tilelang.intrinsics.mma_layout.shared_16x32_to_mma_32x16_smoothlayout(_i_ , _j_)Â¶
    

tilelang.intrinsics.mma_layout.shared_32x16_to_mma_32x16_smoothlayout(_i_ , _j_)Â¶
    

tilelang.intrinsics.mma_layout.get_swizzle_layout(_row_idx_ , _col_idx_ , _row_size_ , _dtype_ , _swizzle_bytes =None_)Â¶
    

Parameters:
    

**dtype** (_tvm.DataType_ _|__str_)

tilelang.intrinsics.mma_layout.make_mma_swizzle_layout(_shared_buf_ , _is_smooth =False_)Â¶
    

Parameters:
    

**is_smooth** ([_bool_](../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool"))
