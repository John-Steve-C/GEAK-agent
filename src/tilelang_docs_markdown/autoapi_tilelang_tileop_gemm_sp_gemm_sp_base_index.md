# tilelang.tileop.gemm_sp.gemm_sp_baseÂ¶

## ClassesÂ¶

`GemmSPBase` |   
---|---  
  
## Module ContentsÂ¶

_class _tilelang.tileop.gemm_sp.gemm_sp_base.GemmSPBaseÂ¶
    

gemm_sp_node _: tvm.ir.base.Node_Â¶
    

_abstract _infer_layout(_target_ , _thread_nums_)Â¶
    

Parameters:
    

  * **target** (_tvm.target.Target_)

  * **thread_nums** (_int_)




_abstract _lower(_target_ , _thread_nums_ , _thread_var_)Â¶
    

Parameters:
    

  * **target** (_tvm.target.Target_)

  * **thread_nums** (_int_)

  * **thread_var** (_tvm.tir.Var_)




is_gemm_ss()Â¶
    

Return type:
    

[bool](../../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool")

is_gemm_sr()Â¶
    

Return type:
    

[bool](../../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool")

is_gemm_rs()Â¶
    

Return type:
    

[bool](../../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool")

is_gemm_rr()Â¶
    

Return type:
    

[bool](../../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool")

_property _M _: int_Â¶
    

Return type:
    

int

_property _N _: int_Â¶
    

Return type:
    

int

_property _K _: int_Â¶
    

Return type:
    

int

_property _trans_A _: [bool](../../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool")_Â¶
    

Return type:
    

[bool](../../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool")

_property _trans_B _: [bool](../../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool")_Â¶
    

Return type:
    

[bool](../../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool")

_property _trans_E _: [bool](../../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool")_Â¶
    

Return type:
    

[bool](../../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool")

_property _e_dtype _: str_Â¶
    

Return type:
    

str

_property _in_dtype _: str_Â¶
    

Return type:
    

str

_property _accum_dtype _: str_Â¶
    

Return type:
    

str

_property _A _: tvm.tir.Buffer_Â¶
    

Return type:
    

tvm.tir.Buffer

_property _E _: tvm.tir.Buffer_Â¶
    

Return type:
    

tvm.tir.Buffer

_property _B _: tvm.tir.Buffer_Â¶
    

Return type:
    

tvm.tir.Buffer

_property _C _: tvm.tir.Buffer_Â¶
    

Return type:
    

tvm.tir.Buffer

_property _ARegion _: tvm.tir.PrimExpr_Â¶
    

Return type:
    

tvm.tir.PrimExpr

_property _ERegion _: tvm.tir.PrimExpr_Â¶
    

Return type:
    

tvm.tir.PrimExpr

_property _BRegion _: tvm.tir.PrimExpr_Â¶
    

Return type:
    

tvm.tir.PrimExpr

_property _CRegion _: tvm.tir.PrimExpr_Â¶
    

Return type:
    

tvm.tir.PrimExpr

_property _stride_A _: int_Â¶
    

Return type:
    

int

_property _stride_B _: int_Â¶
    

Return type:
    

int

_property _offset_A _: int_Â¶
    

Return type:
    

int

_property _offset_B _: int_Â¶
    

Return type:
    

int

_property _clear_accum _: [bool](../../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool")_Â¶
    

Return type:
    

[bool](../../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool")

_property _k_pack _: int_Â¶
    

Return type:
    

int

_property _wg_wait _: int_Â¶
    

Return type:
    

int

_property _policy _: [tilelang.tileop.base.GemmWarpPolicy](../../base/index.html#tilelang.tileop.base.GemmWarpPolicy "tilelang.tileop.base.GemmWarpPolicy")_Â¶
    

Return type:
    

[tilelang.tileop.base.GemmWarpPolicy](../../base/index.html#tilelang.tileop.base.GemmWarpPolicy "tilelang.tileop.base.GemmWarpPolicy")
