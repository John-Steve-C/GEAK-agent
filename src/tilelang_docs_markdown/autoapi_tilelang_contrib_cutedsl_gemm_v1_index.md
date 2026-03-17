# tilelang.contrib.cutedsl.gemm_v1Â¶

## ClassesÂ¶

`Gemm_SM80` |   
---|---  
`Gemm_SM90` |   
  
## FunctionsÂ¶

`make_aligned_tensor`(ptr, layout, align_bytes[, swizzle]) |   
---|---  
`gemm_ss`(M, N, K, warp_m, warp_n, trans_A, trans_B, ...) | GEMM with both A and B from shared memory  
`gemm_rs`(M, N, K, warp_m, warp_n, trans_A, trans_B, ...) | GEMM with A from register/fragment and B from shared memory  
`gemm_sr`(M, N, K, warp_m, warp_n, trans_A, trans_B, ...) | GEMM with A from shared memory and B from register/fragment  
`gemm_rr`(M, N, K, warp_m, warp_n, trans_A, trans_B, ...) | GEMM with both A and B from register/fragment  
  
## Module ContentsÂ¶

tilelang.contrib.cutedsl.gemm_v1.make_aligned_tensor(_ptr_ , _layout_ , _align_bytes_ , _swizzle =False_)Â¶
    

Parameters:
    

  * **ptr** (_cutlass.cute.Pointer_)

  * **layout** (_cutlass.cute.Layout_)

  * **align_bytes** (_int_)




tilelang.contrib.cutedsl.gemm_v1.gemm_ss(_M_ , _N_ , _K_ , _warp_m_ , _warp_n_ , _trans_A_ , _trans_B_ , _clear_accum_ , _stride_A_ , _stride_B_ , _offset_A_ , _offset_B_ , _use_wgmma =None_, _wg_wait =0_, _A_ptr =None_, _B_ptr =None_, _C_ptr =None_)Â¶
    

GEMM with both A and B from shared memory

Parameters:
    

  * **A_ptr** (_cutlass.cute.Pointer_)

  * **B_ptr** (_cutlass.cute.Pointer_)

  * **C_ptr** (_cutlass.cute.Pointer_)




tilelang.contrib.cutedsl.gemm_v1.gemm_rs(_M_ , _N_ , _K_ , _warp_m_ , _warp_n_ , _trans_A_ , _trans_B_ , _clear_accum_ , _stride_A_ , _stride_B_ , _offset_A_ , _offset_B_ , _use_wgmma =None_, _wg_wait =0_, _A_ptr =None_, _B_ptr =None_, _C_ptr =None_)Â¶
    

GEMM with A from register/fragment and B from shared memory

Parameters:
    

  * **A_ptr** (_cutlass.cute.Pointer_)

  * **B_ptr** (_cutlass.cute.Pointer_)

  * **C_ptr** (_cutlass.cute.Pointer_)




tilelang.contrib.cutedsl.gemm_v1.gemm_sr(_M_ , _N_ , _K_ , _warp_m_ , _warp_n_ , _trans_A_ , _trans_B_ , _clear_accum_ , _stride_A_ , _stride_B_ , _offset_A_ , _offset_B_ , _use_wgmma =None_, _wg_wait =0_, _A_ptr =None_, _B_ptr =None_, _C_ptr =None_)Â¶
    

GEMM with A from shared memory and B from register/fragment

Parameters:
    

  * **A_ptr** (_cutlass.cute.Pointer_)

  * **B_ptr** (_cutlass.cute.Pointer_)

  * **C_ptr** (_cutlass.cute.Pointer_)




tilelang.contrib.cutedsl.gemm_v1.gemm_rr(_M_ , _N_ , _K_ , _warp_m_ , _warp_n_ , _trans_A_ , _trans_B_ , _clear_accum_ , _stride_A_ , _stride_B_ , _offset_A_ , _offset_B_ , _use_wgmma =None_, _wg_wait =0_, _A_ptr =None_, _B_ptr =None_, _C_ptr =None_)Â¶
    

GEMM with both A and B from register/fragment

Parameters:
    

  * **A_ptr** (_cutlass.cute.Pointer_)

  * **B_ptr** (_cutlass.cute.Pointer_)

  * **C_ptr** (_cutlass.cute.Pointer_)




_class _tilelang.contrib.cutedsl.gemm_v1.Gemm_SM80(_M_ , _N_ , _K_ , _warp_m_ , _warp_n_ , _trans_A_ , _trans_B_ , _clear_accum_ , _stride_A_ , _stride_B_ , _offset_A_ , _offset_B_ , _A_type_ , _B_type_ , _C_type_)Â¶
    

__call__(_sA_ptr_ , _sB_ptr_ , _rC_ptr_)Â¶
    

GEMM body: both A and B from shared memory

Parameters:
    

  * **sA_ptr** (_cutlass.cute.Pointer_)

  * **sB_ptr** (_cutlass.cute.Pointer_)

  * **rC_ptr** (_cutlass.cute.Pointer_)




body_rs(_rA_ptr_ , _sB_ptr_ , _rC_ptr_)Â¶
    

GEMM body_rs: A from register, B from shared memory

Parameters:
    

  * **rA_ptr** (_cutlass.cute.Pointer_)

  * **sB_ptr** (_cutlass.cute.Pointer_)

  * **rC_ptr** (_cutlass.cute.Pointer_)




body_sr(_sA_ptr_ , _rB_ptr_ , _rC_ptr_)Â¶
    

GEMM body_sr: A from shared memory, B from register

Parameters:
    

  * **sA_ptr** (_cutlass.cute.Pointer_)

  * **rB_ptr** (_cutlass.cute.Pointer_)

  * **rC_ptr** (_cutlass.cute.Pointer_)




_class _tilelang.contrib.cutedsl.gemm_v1.Gemm_SM90(_M_ , _N_ , _K_ , _warp_m_ , _warp_n_ , _trans_A_ , _trans_B_ , _clear_accum_ , _stride_A_ , _stride_B_ , _offset_A_ , _offset_B_ , _A_type_ , _B_type_ , _C_type_)Â¶
    

_static _make_tma_atom(_tensor_ , _smem_layout_staged_ , _smem_tile_ , _mcast_dim_)Â¶
    

_static _get_tma_atom(_tensor_ , _tiler_mk_ , _stages =1_)Â¶
    

_static _make_smem_layout_AB(_dtype_ , _major_mode_ , _tiler_mk_ , _stages =1_)Â¶
    

Parameters:
    

**major_mode** (_cutlass.utils.LayoutEnum_)

__call__(_sA_ptr_ , _sB_ptr_ , _rC_ptr_ , _wg_wait =0_, _clear_accum =False_)Â¶
    

Parameters:
    

  * **sA_ptr** (_cutlass.cute.Pointer_)

  * **sB_ptr** (_cutlass.cute.Pointer_)

  * **rC_ptr** (_cutlass.cute.Pointer_)

  * **wg_wait** (_cutlass.Constexpr_)

  * **clear_accum** (_cutlass.Constexpr_)




body_rs(_rA_ptr_ , _sB_ptr_ , _rC_ptr_ , _wg_wait =0_, _clear_accum =False_)Â¶
    

GEMM body_rs for SM90/Hopper: A from register, B from shared memory. Based on cute::tl_wgmma::GemmTensorOp::body_rs from gemm_sm90.h

Parameters:
    

  * **rA_ptr** (_cutlass.cute.Pointer_)

  * **sB_ptr** (_cutlass.cute.Pointer_)

  * **rC_ptr** (_cutlass.cute.Pointer_)

  * **wg_wait** (_cutlass.Constexpr_)

  * **clear_accum** (_cutlass.Constexpr_)



