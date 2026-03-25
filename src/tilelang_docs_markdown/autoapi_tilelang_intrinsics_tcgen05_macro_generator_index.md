# tilelang.intrinsics.tcgen05_macro_generatorÂ¶

## AttributesÂ¶

`lift` |   
---|---  
  
## ClassesÂ¶

`SwizzleMode` | Enum where members are also (and must be) ints  
---|---  
`TensorCoreIntrinEmitter` | Intrinsic emitter for Blackwell (SM100) TCGEN5MMA instructions.  
  
## Module ContentsÂ¶

tilelang.intrinsics.tcgen05_macro_generator.liftÂ¶
    

_class _tilelang.intrinsics.tcgen05_macro_generator.SwizzleModeÂ¶
    

Bases: `enum.IntEnum`

Enum where members are also (and must be) ints

NONE _ = 0_Â¶
    

SWIZZLE_128B _ = 2_Â¶
    

SWIZZLE_64B _ = 4_Â¶
    

SWIZZLE_32B _ = 6_Â¶
    

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

_class _tilelang.intrinsics.tcgen05_macro_generator.TensorCoreIntrinEmitter(_a_dtype =T.float16_, _b_dtype =T.float16_, _accum_dtype =T.float16_, _a_transposed =False_, _b_transposed =False_, _block_row_warps =2_, _block_col_warps =2_, _warp_row_tiles =8_, _warp_col_tiles =8_, _chunk =16_, _reduce_k =1_, _num_elems_per_byte =1_, _is_m_first =False_, _thread_var =None_)Â¶
    

Bases: [`tilelang.intrinsics.mma_macro_generator.TensorCoreIntrinEmitter`](../mma_macro_generator/index.html#tilelang.intrinsics.mma_macro_generator.TensorCoreIntrinEmitter "tilelang.intrinsics.mma_macro_generator.TensorCoreIntrinEmitter")

Intrinsic emitter for Blackwell (SM100) TCGEN5MMA instructions.

Generates TIR macros that lower to `tcgen05.mma` PTX instructions for both the SS (Shared-Shared) and TS (TensorMemory-Shared) GEMM variants. Also provides layout helpers for tensor-memory (TMEM) buffers.

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

  * **is_m_first** ([_bool_](../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool"))

  * **thread_var** (_tvm.tir.Var_ _|__None_)




tcgen05_prefix _: str_Â¶
    

a_shared_layout _: tilelang.layout.Layout_ _ = None_Â¶
    

b_shared_layout _: tilelang.layout.Layout_ _ = None_Â¶
    

tcgen05mma(_A_buf_ , _B_buf_ , _C_local_buf_ , _mbar_ , _clear_accum =False_)Â¶
    

Emit a TCGEN5MMA operation, dispatching to SS or TS variant based on Aâs memory scope.

If _A_buf_ resides in tensor memory (`shared.tmem`), the TS variant is emitted; otherwise the SS variant is used (both A and B from shared memory).

Parameters:
    

  * **A_buf** (_Buffer_) â Operand A â either in shared memory (SS) or tensor memory (TS).

  * **B_buf** (_Buffer_) â Operand B in shared memory.

  * **C_local_buf** (_Buffer_) â Accumulator buffer in tensor memory.

  * **mbar** (_PrimExpr_) â Memory barrier used for MMA completion signalling.

  * **clear_accum** (_PrimExpr_) â Whether to zero the accumulator before the first MMA.




tcgen05mma_ts(_A_buf_ , _B_buf_ , _C_local_buf_ , _mbar_ , _clear_accum =False_)Â¶
    

Emit the TS (TensorMemory-Shared) variant of TCGEN5MMA.

Reads operand A directly from tensor memory (TMEM) and operand B from shared memory via a descriptor. The TMEM column offset for A is computed assuming packed storage (e.g. two `bfloat16` values per `uint32` column) to match the output of `tcgen05.st`.

Parameters:
    

  * **A_buf** (_Buffer_) â Operand A residing in tensor memory (`shared.tmem`).

  * **B_buf** (_Buffer_) â Operand B in shared memory.

  * **C_local_buf** (_Buffer_) â Accumulator buffer in tensor memory.

  * **mbar** (_PrimExpr_) â Memory barrier for MMA completion signalling.

  * **clear_accum** (_PrimExpr_) â Whether to zero the accumulator before the first MMA.




_abstract _make_mma_load_layout(_local_buf_ , _matrix ='A'_)Â¶
    

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

make_mma_store_layout(_tmem_buf_)Â¶
    

Create the TCGEN5 tensor-memory layout used to store MMA accumulators.

Parameters:
    

**tmem_buf** (_tir.Buffer_) â The local buffer representing tensormemory of a mmaâs output

Returns:
    

Layout object describing how logical (i, j) coordinates map to the swizzled tensor-memory offsets required by TCGEN5MMA.

Return type:
    

[Layout](../../layout/layout/index.html#tilelang.layout.layout.Layout "tilelang.layout.layout.Layout")

Raises:
    

**AssertionError** â If tmem_buf is not detected to be a tensor-memory buffer.

get_tcgen5_mma_meta(_m_ , _n_ , _k_)Â¶
    

Query the FFI for TCGEN5MMA atom metadata (atom_m, atom_n, atom_k, enable_ws, enable_2cta).

Parameters:
    

  * **m** (_int_)

  * **n** (_int_)

  * **k** (_int_)




get_tcgen5_instr_desc(_atom_m_ , _atom_n_ , _atom_k_ , _a_is_k_major_ , _b_is_k_major_ , _scale_in_a_ , _scale_in_b_)Â¶
    

Build the 64-bit instruction descriptor for a `tcgen05.mma` PTX call.

Parameters:
    

  * **atom_m** (_int_)

  * **atom_n** (_int_)

  * **atom_k** (_int_)

  * **a_is_k_major** ([_bool_](../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool"))

  * **b_is_k_major** ([_bool_](../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool"))

  * **scale_in_a** (_int_)

  * **scale_in_b** (_int_)



Return type:
    

tvm.tir.PrimExpr
