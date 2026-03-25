# tilelang.intrinsics.mfma_layoutÂ¶

## AttributesÂ¶

`shared_16x16_to_local_64x4_layout_m_n` |   
---|---  
`shared_16x16_to_local_64x4_layout_n_k` |   
`shared_16x16_to_local_64x4_layout_n_m` |   
`shared_16x16_to_local_64x4_layout_k_n` |   
  
## FunctionsÂ¶

`shared_16x4_to_local_64x1_layout_A`(i, j) |   
---|---  
`thread_id_shared_access_64x1_to_16x4_layout_A`(...) |   
`shared_4x16_to_local_64x1_layout_B`(i, j) |   
`thread_id_shared_access_64x1_to_4x16_layout_B`(...) |   
`shared_16x16_to_local_64x4_layout_C`(i, j) |   
`shared_16x16_to_ldmatrix_64x4_layout`(ind) |   
`thread_id_shared_access_64x4_to_16x16_layout_A`(...) |   
`shared_16x16_to_local_64x4_layout_A`(i, j) |   
`thread_id_shared_access_64x4_to_16x16_layout_B`(...) |   
`shared_16x16_to_local_64x4_layout_B`(i, j) |   
`thread_id_shared_access_64x4_to_16x16_layout_C_m_n`(...) |   
`thread_id_shared_access_64x4_to_16x16_layout_C_n_m`(...) |   
`thread_id_shared_access_64x8_to_16x32_layout_A`(...) |   
`shared_16x32_to_local_64x8_layout_A`(i, j) |   
`thread_id_shared_access_64x8_to_16x32_layout_B`(...) |   
`shared_16x32_to_local_64x8_layout_B`(i, j) |   
`thread_id_shared_access_64x16_to_16x64_layout_A`(...) |   
`shared_16x64_to_local_64x16_layout_A`(i, j) |   
`thread_id_shared_access_64x16_to_16x64_layout_B`(...) |   
`shared_16x64_to_local_64x16_layout_B`(i, j) |   
`make_mfma_swizzle_layout`(shared_buf[, vecSize]) |   
  
## Module ContentsÂ¶

tilelang.intrinsics.mfma_layout.shared_16x4_to_local_64x1_layout_A(_i_ , _j_)Â¶
    

tilelang.intrinsics.mfma_layout.thread_id_shared_access_64x1_to_16x4_layout_A(_thread_id_ , _local_id_)Â¶
    

tilelang.intrinsics.mfma_layout.shared_4x16_to_local_64x1_layout_B(_i_ , _j_)Â¶
    

tilelang.intrinsics.mfma_layout.thread_id_shared_access_64x1_to_4x16_layout_B(_thread_id_ , _local_id_)Â¶
    

tilelang.intrinsics.mfma_layout.shared_16x16_to_local_64x4_layout_C(_i_ , _j_)Â¶
    

tilelang.intrinsics.mfma_layout.shared_16x16_to_ldmatrix_64x4_layout(_ind_)Â¶
    

tilelang.intrinsics.mfma_layout.thread_id_shared_access_64x4_to_16x16_layout_A(_thread_id_ , _local_id_)Â¶
    

tilelang.intrinsics.mfma_layout.shared_16x16_to_local_64x4_layout_A(_i_ , _j_)Â¶
    

tilelang.intrinsics.mfma_layout.thread_id_shared_access_64x4_to_16x16_layout_B(_thread_id_ , _local_id_)Â¶
    

tilelang.intrinsics.mfma_layout.shared_16x16_to_local_64x4_layout_B(_i_ , _j_)Â¶
    

tilelang.intrinsics.mfma_layout.shared_16x16_to_local_64x4_layout_m_nÂ¶
    

tilelang.intrinsics.mfma_layout.shared_16x16_to_local_64x4_layout_n_kÂ¶
    

tilelang.intrinsics.mfma_layout.shared_16x16_to_local_64x4_layout_n_mÂ¶
    

tilelang.intrinsics.mfma_layout.shared_16x16_to_local_64x4_layout_k_nÂ¶
    

tilelang.intrinsics.mfma_layout.thread_id_shared_access_64x4_to_16x16_layout_C_m_n(_thread_id_ , _local_id_)Â¶
    

tilelang.intrinsics.mfma_layout.thread_id_shared_access_64x4_to_16x16_layout_C_n_m(_thread_id_ , _local_id_)Â¶
    

tilelang.intrinsics.mfma_layout.thread_id_shared_access_64x8_to_16x32_layout_A(_thread_id_ , _local_id_)Â¶
    

tilelang.intrinsics.mfma_layout.shared_16x32_to_local_64x8_layout_A(_i_ , _j_)Â¶
    

tilelang.intrinsics.mfma_layout.thread_id_shared_access_64x8_to_16x32_layout_B(_thread_id_ , _local_id_)Â¶
    

tilelang.intrinsics.mfma_layout.shared_16x32_to_local_64x8_layout_B(_i_ , _j_)Â¶
    

tilelang.intrinsics.mfma_layout.thread_id_shared_access_64x16_to_16x64_layout_A(_thread_id_ , _local_id_)Â¶
    

tilelang.intrinsics.mfma_layout.shared_16x64_to_local_64x16_layout_A(_i_ , _j_)Â¶
    

tilelang.intrinsics.mfma_layout.thread_id_shared_access_64x16_to_16x64_layout_B(_thread_id_ , _local_id_)Â¶
    

tilelang.intrinsics.mfma_layout.shared_16x64_to_local_64x16_layout_B(_i_ , _j_)Â¶
    

tilelang.intrinsics.mfma_layout.make_mfma_swizzle_layout(_shared_buf_ , _vecSize =8_)Â¶
    
