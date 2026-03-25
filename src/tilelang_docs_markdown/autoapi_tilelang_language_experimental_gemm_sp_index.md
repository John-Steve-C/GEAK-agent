# tilelang.language.experimental.gemm_spÂ¶

The language interface for tl programs.

## FunctionsÂ¶

`gemm_sp`(A_sparse, E, B, C[, transpose_A, transpose_B, ...]) | Perform a Sparse General Matrix Multiplication (GEMM-sp) operation.  
---|---  
`gemm_sp_v2`(A_sparse, E, B, C[, transpose_A, ...]) | Perform a General Matrix Multiplication (GEMM) operation.  
  
## Module ContentsÂ¶

tilelang.language.experimental.gemm_sp.gemm_sp(_A_sparse_ , _E_ , _B_ , _C_ , _transpose_A =False_, _transpose_B =False_, _policy =GemmWarpPolicy.Square_, _clear_accum =False_, _k_pack =1_, _wg_wait =0_)Â¶
    

Perform a Sparse General Matrix Multiplication (GEMM-sp) operation.

This function computes C = A @ B where A and B can optionally be transposed. The operation supports various warp policies and accumulation modes.

Parameters:
    

  * **A_sparse** (_Union_ _[__BufferLikeType_ _,__tir.Var_ _]_) â First input matrix dense values

  * **E** (_Union_ _[__BufferLikeType_ _,__tir.Var_ _]_) â First input matrix sparse metadata

  * **B** (_Union_ _[__BufferLikeType_ _,__tir.Var_ _]_) â Second input matrix

  * **C** (_Union_ _[__BufferLikeType_ _,__tir.Var_ _]_) â Output matrix for results

  * **transpose_A** ([_bool_](../../dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool") _,__optional_) â Whether to transpose matrix A. Defaults to False.

  * **transpose_B** ([_bool_](../../dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool") _,__optional_) â Whether to transpose matrix B. Defaults to False.

  * **policy** ([_GemmWarpPolicy_](../../../ir/index.html#tilelang.ir.GemmWarpPolicy "tilelang.ir.GemmWarpPolicy") _,__optional_) â Warp execution policy. Defaults to GemmWarpPolicy.Square.

  * **clear_accum** ([_bool_](../../dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool") _,__optional_) â Whether to clear accumulator before computation. Defaults to False.

  * **k_pack** (_int_ _,__optional_) â Number of k dimensions packed into a single warp. Defaults to 1.

  * **wg_wait** (_int_ _,__optional_) â Warp group wait count. Defaults to 0.



Returns:
    

A handle to the GEMM operation

Return type:
    

tir.Call

Raises:
    

**AssertionError** â If the K dimensions of matrices A and B donât match

tilelang.language.experimental.gemm_sp.gemm_sp_v2(_A_sparse_ , _E_ , _B_ , _C_ , _transpose_A =False_, _transpose_B =False_, _transpose_E =False_, _policy =GemmWarpPolicy.Square_, _clear_accum =False_, _k_pack =1_, _wg_wait =0_)Â¶
    

Perform a General Matrix Multiplication (GEMM) operation.

This function computes C = A @ B where A and B can optionally be transposed. The operation supports various warp policies and accumulation modes.

Parameters:
    

  * **A_sparse** (_Union_ _[__BufferLikeType_ _,__tir.Var_ _]_) â First input matrix, contains only non-zero elements

  * **E** (_Union_ _[__BufferLikeType_ _,__tir.Var_ _]_) â The metadata of A_sparse, noted as E

  * **B** (_Union_ _[__BufferLikeType_ _,__tir.Var_ _]_) â Second input matrix

  * **C** (_Union_ _[__BufferLikeType_ _,__tir.Var_ _]_) â Output matrix for results

  * **transpose_A** ([_bool_](../../dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool") _,__optional_) â Whether to transpose matrix A. Defaults to False.

  * **transpose_B** ([_bool_](../../dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool") _,__optional_) â Whether to transpose matrix B. Defaults to False.

  * **policy** ([_GemmWarpPolicy_](../../../ir/index.html#tilelang.ir.GemmWarpPolicy "tilelang.ir.GemmWarpPolicy") _,__optional_) â Warp execution policy. Defaults to GemmWarpPolicy.Square.

  * **clear_accum** ([_bool_](../../dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool") _,__optional_) â Whether to clear accumulator before computation. Defaults to False.

  * **k_pack** (_int_ _,__optional_) â Number of k dimensions packed into a single warp. Defaults to 1.

  * **wg_wait** (_int_ _,__optional_) â Warp group wait count. Defaults to 0.

  * **transpose_E** ([_bool_](../../dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool"))



Returns:
    

A handle to the GEMM operation

Return type:
    

tir.Call

Raises:
    

**AssertionError** â If the K dimensions of matrices A and B donât match
