# tilelang.language.gemm_opÂ¶

GEMM (General Matrix Multiplication) operators exposed on the TileLang language surface.

## FunctionsÂ¶

`gemm_v1`(A, B, C[, transpose_A, transpose_B, policy, ...]) | GEMM v1: use op tl.gemm.  
---|---  
`gemm_v2`(A, B, C[, transpose_A, transpose_B, policy, ...]) | GEMM v2: use op tl.gemm_py.  
`gemm`(A, B, C[, transpose_A, transpose_B, policy, ...]) | TileLang GEMM operator.  
  
## Module ContentsÂ¶

tilelang.language.gemm_op.gemm_v1(_A_ , _B_ , _C_ , _transpose_A =False_, _transpose_B =False_, _policy =GemmWarpPolicy.Square_, _clear_accum =False_, _k_pack =1_, _wg_wait =0_, _mbar =None_)Â¶
    

GEMM v1: use op tl.gemm.

Parameters:
    

  * **A** (_tilelang._typing.BufferLikeType_)

  * **B** (_tilelang._typing.BufferLikeType_)

  * **C** (_tilelang._typing.BufferLikeType_)

  * **transpose_A** ([_bool_](../dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool"))

  * **transpose_B** ([_bool_](../dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool"))

  * **policy** ([_tilelang.tileop.base.GemmWarpPolicy_](../../tileop/base/index.html#tilelang.tileop.base.GemmWarpPolicy "tilelang.tileop.base.GemmWarpPolicy"))

  * **clear_accum** ([_bool_](../dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool"))

  * **k_pack** (_int_)

  * **wg_wait** (_int_)

  * **mbar** (_tilelang._typing.BarrierType_ _|__None_)



Return type:
    

tvm.tir.PrimExpr

tilelang.language.gemm_op.gemm_v2(_A_ , _B_ , _C_ , _transpose_A =False_, _transpose_B =False_, _policy =GemmWarpPolicy.Square_, _clear_accum =False_, _k_pack =1_, _wg_wait =0_, _mbar =None_)Â¶
    

GEMM v2: use op tl.gemm_py.

Parameters:
    

  * **A** (_tilelang._typing.BufferLikeType_)

  * **B** (_tilelang._typing.BufferLikeType_)

  * **C** (_tilelang._typing.BufferLikeType_)

  * **transpose_A** ([_bool_](../dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool"))

  * **transpose_B** ([_bool_](../dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool"))

  * **policy** ([_tilelang.tileop.base.GemmWarpPolicy_](../../tileop/base/index.html#tilelang.tileop.base.GemmWarpPolicy "tilelang.tileop.base.GemmWarpPolicy"))

  * **clear_accum** ([_bool_](../dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool"))

  * **k_pack** (_int_)

  * **wg_wait** (_int_)

  * **mbar** (_tilelang._typing.BarrierType_ _|__None_)



Return type:
    

tvm.tir.PrimExpr

tilelang.language.gemm_op.gemm(_A_ , _B_ , _C_ , _transpose_A =False_, _transpose_B =False_, _policy =GemmWarpPolicy.Square_, _clear_accum =False_, _k_pack =1_, _wg_wait =0_, _mbar =None_)Â¶
    

TileLang GEMM operator.

Parameters:
    

  * **A** (_BufferLikeType_ _,__i.e. Buffer_ _|__BufferLoad_ _|__BufferRegion_ _, or_ _Var_) â Input buffer A.

  * **B** (_BufferLikeType_) â Input buffer B.

  * **C** (_BufferLikeType_) â Output buffer C.

  * **transpose_A** ([_bool_](../dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool")) â Whether to transpose A. Defaults to False.

  * **transpose_B** ([_bool_](../dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool")) â Whether to transpose B. Defaults to False.

  * **policy** ([_GemmWarpPolicy_](../../ir/index.html#tilelang.ir.GemmWarpPolicy "tilelang.ir.GemmWarpPolicy")) â GEMM warp partition policy.

  * **clear_accum** ([_bool_](../dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool")) â Whether to clear the accumulator.

  * **k_pack** (_int_) â Numbers of packed matrix cores, for ROCm only. Defaults to 1.

  * **wg_wait** (_int_) â Int identifier of the warpgroup MMA batch to wait on.. Defaults to 0.

  * **mbar** (_BarrierType_ _,__i.e. Buffer_ _|__BufferLoad_ _, or_ _Var_ _,__optional_) â Mbarrier in Blackwell. Defaults to None.



Returns:
    

A handle to the GEMM operation.

Return type:
    

tir.Call
