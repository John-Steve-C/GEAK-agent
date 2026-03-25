# tilelang.contrib.cutedsl.ldsmÂ¶

LDMATRIX and STMATRIX operations for CuTeDSL backend. Based on tl_templates/cuda/ldsm.h

These functions provide wrappers around PTX ldmatrix/stmatrix instructions for loading/storing 8x8 matrix fragments between shared memory and registers.

## FunctionsÂ¶

`ptx_ldmatrix_x1`(smem_ptr, local_ptr, *[, loc, ip]) | Load 1 matrix (8x8) from shared memory  
---|---  
`ptx_ldmatrix_x2`(smem_ptr, local_ptr, *[, loc, ip]) | Load 2 matrices (8x8 each) from shared memory  
`ptx_ldmatrix_x4`(smem_ptr, local_ptr, *[, loc, ip]) | Load 4 matrices (8x8 each) from shared memory  
`ptx_ldmatrix_x1_trans`(smem_ptr, local_ptr, *[, loc, ip]) | Load 1 matrix (8x8) with transpose from shared memory  
`ptx_ldmatrix_x2_trans`(smem_ptr, local_ptr, *[, loc, ip]) | Load 2 matrices (8x8 each) with transpose from shared memory  
`ptx_ldmatrix_x4_trans`(smem_ptr, local_ptr, *[, loc, ip]) | Load 4 matrices (8x8 each) with transpose from shared memory  
`ptx_stmatrix_x1`(smem_ptr, value0, *[, loc, ip]) | Store 1 matrix (8x8) to shared memory  
`ptx_stmatrix_x2`(smem_ptr, value0, value1, *[, loc, ip]) | Store 2 matrices (8x8 each) to shared memory  
`ptx_stmatrix_x4`(smem_ptr, value0, value1, value2, ...) | Store 4 matrices (8x8 each) to shared memory  
`ptx_stmatrix_x1_trans`(smem_ptr, value0, *[, loc, ip]) | Store 1 matrix (8x8) with transpose to shared memory  
`ptx_stmatrix_x2_trans`(smem_ptr, value0, value1, *[, ...]) | Store 2 matrices (8x8 each) with transpose to shared memory  
`ptx_stmatrix_x4_trans`(smem_ptr, value0, value1, ...[, ...]) | Store 4 matrices (8x8 each) with transpose to shared memory  
  
## Module ContentsÂ¶

tilelang.contrib.cutedsl.ldsm.ptx_ldmatrix_x1(_smem_ptr_ , _local_ptr_ , _*_ , _loc =None_, _ip =None_)Â¶
    

Load 1 matrix (8x8) from shared memory

Parameters:
    

  * **smem_ptr** (_cutlass.cute.typing.Pointer_)

  * **local_ptr** (_cutlass.cute.typing.Pointer_)



Return type:
    

None

tilelang.contrib.cutedsl.ldsm.ptx_ldmatrix_x2(_smem_ptr_ , _local_ptr_ , _*_ , _loc =None_, _ip =None_)Â¶
    

Load 2 matrices (8x8 each) from shared memory

Parameters:
    

  * **smem_ptr** (_cutlass.cute.typing.Pointer_)

  * **local_ptr** (_cutlass.cute.typing.Pointer_)



Return type:
    

None

tilelang.contrib.cutedsl.ldsm.ptx_ldmatrix_x4(_smem_ptr_ , _local_ptr_ , _*_ , _loc =None_, _ip =None_)Â¶
    

Load 4 matrices (8x8 each) from shared memory

Parameters:
    

  * **smem_ptr** (_cutlass.cute.typing.Pointer_)

  * **local_ptr** (_cutlass.cute.typing.Pointer_)



Return type:
    

None

tilelang.contrib.cutedsl.ldsm.ptx_ldmatrix_x1_trans(_smem_ptr_ , _local_ptr_ , _*_ , _loc =None_, _ip =None_)Â¶
    

Load 1 matrix (8x8) with transpose from shared memory

Parameters:
    

  * **smem_ptr** (_cutlass.cute.typing.Pointer_)

  * **local_ptr** (_cutlass.cute.typing.Pointer_)



Return type:
    

None

tilelang.contrib.cutedsl.ldsm.ptx_ldmatrix_x2_trans(_smem_ptr_ , _local_ptr_ , _*_ , _loc =None_, _ip =None_)Â¶
    

Load 2 matrices (8x8 each) with transpose from shared memory

Parameters:
    

  * **smem_ptr** (_cutlass.cute.typing.Pointer_)

  * **local_ptr** (_cutlass.cute.typing.Pointer_)



Return type:
    

None

tilelang.contrib.cutedsl.ldsm.ptx_ldmatrix_x4_trans(_smem_ptr_ , _local_ptr_ , _*_ , _loc =None_, _ip =None_)Â¶
    

Load 4 matrices (8x8 each) with transpose from shared memory

Parameters:
    

  * **smem_ptr** (_cutlass.cute.typing.Pointer_)

  * **local_ptr** (_cutlass.cute.typing.Pointer_)



Return type:
    

None

tilelang.contrib.cutedsl.ldsm.ptx_stmatrix_x1(_smem_ptr_ , _value0_ , _*_ , _loc =None_, _ip =None_)Â¶
    

Store 1 matrix (8x8) to shared memory

Parameters:
    

**smem_ptr** (_cutlass.cute.typing.Pointer_)

Return type:
    

None

tilelang.contrib.cutedsl.ldsm.ptx_stmatrix_x2(_smem_ptr_ , _value0_ , _value1_ , _*_ , _loc =None_, _ip =None_)Â¶
    

Store 2 matrices (8x8 each) to shared memory

Parameters:
    

**smem_ptr** (_cutlass.cute.typing.Pointer_)

Return type:
    

None

tilelang.contrib.cutedsl.ldsm.ptx_stmatrix_x4(_smem_ptr_ , _value0_ , _value1_ , _value2_ , _value3_ , _*_ , _loc =None_, _ip =None_)Â¶
    

Store 4 matrices (8x8 each) to shared memory

Parameters:
    

**smem_ptr** (_cutlass.cute.typing.Pointer_)

Return type:
    

None

tilelang.contrib.cutedsl.ldsm.ptx_stmatrix_x1_trans(_smem_ptr_ , _value0_ , _*_ , _loc =None_, _ip =None_)Â¶
    

Store 1 matrix (8x8) with transpose to shared memory

Parameters:
    

**smem_ptr** (_cutlass.cute.typing.Pointer_)

Return type:
    

None

tilelang.contrib.cutedsl.ldsm.ptx_stmatrix_x2_trans(_smem_ptr_ , _value0_ , _value1_ , _*_ , _loc =None_, _ip =None_)Â¶
    

Store 2 matrices (8x8 each) with transpose to shared memory

Parameters:
    

**smem_ptr** (_cutlass.cute.typing.Pointer_)

Return type:
    

None

tilelang.contrib.cutedsl.ldsm.ptx_stmatrix_x4_trans(_smem_ptr_ , _value0_ , _value1_ , _value2_ , _value3_ , _*_ , _loc =None_, _ip =None_)Â¶
    

Store 4 matrices (8x8 each) with transpose to shared memory

Parameters:
    

**smem_ptr** (_cutlass.cute.typing.Pointer_)

Return type:
    

None
