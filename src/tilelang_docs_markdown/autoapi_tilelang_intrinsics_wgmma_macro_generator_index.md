# tilelang.intrinsics.wgmma_macro_generatorÂ¶

## AttributesÂ¶

`lift` |   
---|---  
  
## ClassesÂ¶

`SwizzleMode` | Enum where members are also (and must be) ints  
---|---  
`TensorCoreIntrinEmitter` | To eliminate Python syntax within TIR Macro.  
  
## Module ContentsÂ¶

tilelang.intrinsics.wgmma_macro_generator.liftÂ¶
    

_class _tilelang.intrinsics.wgmma_macro_generator.SwizzleModeÂ¶
    

Bases: `enum.IntEnum`

Enum where members are also (and must be) ints

NONE _ = 0_Â¶
    

SWIZZLE_128B _ = 1_Â¶
    

SWIZZLE_64B _ = 2_Â¶
    

SWIZZLE_32B _ = 3_Â¶
    

is_none()Â¶
    

Return type:
    

[bool](../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool")

is_swizzle_32b()Â¶
    

Return type:
    

[bool](../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool")

is_swizzle_64b()Â¶
    

Return type:
    

[bool](../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool")

is_swizzle_128b()Â¶
    

Return type:
    

[bool](../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool")

swizzle_byte_size()Â¶
    

Return type:
    

int

swizzle_atom_size()Â¶
    

Return type:
    

int

_class _tilelang.intrinsics.wgmma_macro_generator.TensorCoreIntrinEmitter(_a_dtype =T.float16_, _b_dtype =T.float16_, _accum_dtype =T.float16_, _a_transposed =False_, _b_transposed =False_, _block_row_warps =2_, _block_col_warps =2_, _warp_row_tiles =8_, _warp_col_tiles =8_, _chunk =16_, _reduce_k =1_, _num_elems_per_byte =1_, _is_m_first =False_, _thread_var =None_)Â¶
    

Bases: [`tilelang.intrinsics.mma_macro_generator.TensorCoreIntrinEmitter`](../mma_macro_generator/index.html#tilelang.intrinsics.mma_macro_generator.TensorCoreIntrinEmitter "tilelang.intrinsics.mma_macro_generator.TensorCoreIntrinEmitter")

To eliminate Python syntax within TIR Macro.

Parameters:
    

  * **a_dtype** (_str_)

  * **b_dtype** (_str_)

  * **accum_dtype** (_str_)

  * **a_transposed** ([_bool_](../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool"))

  * **b_transposed** ([_bool_](../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool"))

  * **block_row_warps** (_int_)

  * **block_col_warps** (_int_)

  * **warp_row_tiles** (_int_)

  * **warp_col_tiles** (_int_)

  * **chunk** (_int_)

  * **reduce_k** (_int_)

  * **num_elems_per_byte** (_int_)

  * **is_m_first** ([_bool_](../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool") _|__None_)

  * **thread_var** (_tvm.tir.Var_ _|__None_)




wgmma_prefix _: str_Â¶
    

wgmma_inst_m _: int_Â¶
    

wgmma_inst_n _: int_Â¶
    

a_shared_layout _: tilelang.layout.Layout_ _ = None_Â¶
    

b_shared_layout _: tilelang.layout.Layout_ _ = None_Â¶
    

wgmma(_A_region_ , _B_region_ , _C_region_ , _clear_accum =False_, _wg_wait =0_)Â¶
    

Parameters:
    

  * **A_region** (_tvm.tir.BufferRegion_)

  * **B_region** (_tvm.tir.BufferRegion_)

  * **C_region** (_tvm.tir.BufferRegion_)

  * **clear_accum** (_tvm.tir.PrimExpr_)

  * **wg_wait** (_int_)




wgmma_rs(_A_region_ , _B_region_ , _C_region_ , _clear_accum =False_, _wg_wait =0_)Â¶
    

Parameters:
    

  * **A_region** (_tvm.tir.BufferRegion_)

  * **B_region** (_tvm.tir.BufferRegion_)

  * **C_region** (_tvm.tir.BufferRegion_)

  * **clear_accum** (_tvm.tir.PrimExpr_)

  * **wg_wait** (_int_)




make_mma_load_layout(_local_buf_ , _matrix ='A'_)Â¶
    

Create a layout function for storing MMA results into a fragment buffer. This layout is used in conjunction with inverse_mma_store_layout to map fragment indices to threads and local indices.

Parameters:
    

  * **local_buf** (_tir.Buffer_) â The local buffer representing a fragment of a matrix.

  * **matrix** (_str_)



Returns:
    

A fragment object that describes how threads and indices in local_buf are laid out.

Return type:
    

T.Fragment

Raises:
    

**AssertionError** â If local_buf is not detected to be a fragment buffer.

make_mma_store_layout(_local_buf_)Â¶
    

Create a layout function for storing MMA results into a fragment buffer. This layout is used in conjunction with inverse_mma_store_layout to map fragment indices to threads and local indices.

Parameters:
    

**local_buf** (_tir.Buffer_) â The local buffer representing a fragment of a matrix.

Returns:
    

A fragment object that describes how threads and indices in local_buf are laid out.

Return type:
    

T.Fragment

Raises:
    

**AssertionError** â If local_buf is not detected to be a fragment buffer.
