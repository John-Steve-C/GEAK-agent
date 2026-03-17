# tilelang.contrib.cutedsl.gemm_v2Â¶

## ClassesÂ¶

`GmmaDescriptor` |   
---|---  
  
## FunctionsÂ¶

`initialize_wgmma_descriptor`(layout_type, ...) |   
---|---  
`increase_descriptor_offset`(desc, offset) |   
`warpgroup_fence_operand`(*args) |   
`warpgroup_arrive`() |   
`warpgroup_commit_batch`() |   
`warpgroup_wait`(N) |   
`wgmma_ss`(A_dtype, B_dtype, C_dtype, M, N, K, tnspA, ...) |   
`wgmma_rs`(A_dtype, B_dtype, C_dtype, M, N, K, tnspB, ...) | WGMMA register-shared variant using PTX inline asm.  
  
## Module ContentsÂ¶

_class _tilelang.contrib.cutedsl.gemm_v2.GmmaDescriptor(_desc_64 =None_)Â¶
    

Parameters:
    

**desc_64** (_cutlass.cute.Int64_)

descÂ¶
    

desc_i64Â¶
    

__add__(_offset_)Â¶
    

tilelang.contrib.cutedsl.gemm_v2.initialize_wgmma_descriptor(_layout_type_ , _leading_byte_offset_ , _stride_byte_offset_ , _desc_ , _start_address_)Â¶
    

Parameters:
    

  * **desc** (_GmmaDescriptor_)

  * **start_address** (_cutlass.cute.Pointer_)




tilelang.contrib.cutedsl.gemm_v2.increase_descriptor_offset(_desc_ , _offset_)Â¶
    

Parameters:
    

**desc** (_GmmaDescriptor_)

tilelang.contrib.cutedsl.gemm_v2.warpgroup_fence_operand(_* args_)Â¶
    

tilelang.contrib.cutedsl.gemm_v2.warpgroup_arrive()Â¶
    

tilelang.contrib.cutedsl.gemm_v2.warpgroup_commit_batch()Â¶
    

tilelang.contrib.cutedsl.gemm_v2.warpgroup_wait(_N_)Â¶
    

tilelang.contrib.cutedsl.gemm_v2.wgmma_ss(_A_dtype_ , _B_dtype_ , _C_dtype_ , _M_ , _N_ , _K_ , _tnspA_ , _tnspB_ , _scaleA_ , _scaleB_ , _desc_a_ , _desc_b_ , _C_ptr_ , _scale_out_)Â¶
    

Parameters:
    

  * **A_dtype** (_str_)

  * **B_dtype** (_str_)

  * **C_dtype** (_str_)

  * **M** (_cutlass.cutlass_dsl.Constexpr_ _[__int_ _]_)

  * **N** (_cutlass.cutlass_dsl.Constexpr_ _[__int_ _]_)

  * **K** (_cutlass.cutlass_dsl.Constexpr_ _[__int_ _]_)

  * **tnspA** ([_bool_](../../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool"))

  * **tnspB** ([_bool_](../../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool"))

  * **scaleA** (_int_)

  * **scaleB** (_int_)

  * **desc_a** (_GmmaDescriptor_)

  * **desc_b** (_GmmaDescriptor_)

  * **C_ptr** (_cutlass.cute.Pointer_)

  * **scale_out** (_cutlass.cutlass_dsl.Constexpr_ _[__int_ _]_)




tilelang.contrib.cutedsl.gemm_v2.wgmma_rs(_A_dtype_ , _B_dtype_ , _C_dtype_ , _M_ , _N_ , _K_ , _tnspB_ , _scaleA_ , _scaleB_ , _A_ptr_ , _desc_b_ , _C_ptr_ , _scale_out_)Â¶
    

WGMMA register-shared variant using PTX inline asm.

A operand comes from registers, B from shared memory descriptor. M is always 64. A is always K-major (not transposed).

Parameters:
    

  * **A_dtype** (_str_)

  * **B_dtype** (_str_)

  * **C_dtype** (_str_)

  * **M** (_cutlass.cutlass_dsl.Constexpr_ _[__int_ _]_)

  * **N** (_cutlass.cutlass_dsl.Constexpr_ _[__int_ _]_)

  * **K** (_cutlass.cutlass_dsl.Constexpr_ _[__int_ _]_)

  * **tnspB** (_cutlass.cutlass_dsl.Constexpr_ _[_[_bool_](../../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool") _]_)

  * **scaleA** (_cutlass.cutlass_dsl.Constexpr_ _[__int_ _]_)

  * **scaleB** (_cutlass.cutlass_dsl.Constexpr_ _[__int_ _]_)

  * **A_ptr** (_cutlass.cute.Pointer_)

  * **desc_b** (_GmmaDescriptor_)

  * **C_ptr** (_cutlass.cute.Pointer_)

  * **scale_out** (_cutlass.cutlass_dsl.Constexpr_ _[__int_ _]_)



