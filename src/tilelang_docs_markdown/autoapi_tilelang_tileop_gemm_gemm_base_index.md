# tilelang.tileop.gemm.gemm_baseÂ¶

## ClassesÂ¶

`GemmBase` | Base class for GEMM tile operators.  
---|---  
  
## Module ContentsÂ¶

_class _tilelang.tileop.gemm.gemm_base.GemmBaseÂ¶
    

Base class for GEMM tile operators.

Classifies the GEMM variant by the memory scopes of operands A and B (SS, SR, RS, TS, RR) and provides common property accessors for the underlying `gemm_node` IR node.

gemm_node _: tvm.ir.base.Node_Â¶
    

_abstract _infer_layout(_target_ , _thread_nums_)Â¶
    

Parameters:
    

  * **target** (_tvm.target.Target_)

  * **thread_nums** (_int_)




_abstract _lower(_layout_map_ , _target_ , _thread_bounds_ , _thread_var_)Â¶
    

Parameters:
    

  * **layout_map** (_dict_)

  * **target** (_tvm.target.Target_)

  * **thread_bounds** (_tvm.ir.Range_)

  * **thread_var** (_tvm.tir.Var_)




is_gemm_ss()Â¶
    

Return True if both A and B are in shared memory (SS variant).

Return type:
    

[bool](../../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool")

is_gemm_sr()Â¶
    

Return True if A is in shared memory and B is in registers (SR variant).

Return type:
    

[bool](../../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool")

is_gemm_rs()Â¶
    

Return True if A is in registers and B is in shared memory (RS variant).

Return type:
    

[bool](../../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool")

is_gemm_ts()Â¶
    

Return True if A is in tensor memory and B is in shared memory (TS variant).

Return type:
    

[bool](../../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool")

is_gemm_rr()Â¶
    

Return True if both A and B are in registers (RR variant).

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

_property _in_dtype _: str_Â¶
    

Input data type for the multiplication.

For the TS variant, A resides in TMEM with the accumulator dtype, so the actual input dtype is derived from B.

Return type:
    

str

_property _accum_dtype _: str_Â¶
    

Return type:
    

str

_property _chunk _: int_Â¶
    

Return type:
    

int

_property _A _: tvm.tir.Buffer_Â¶
    

Return type:
    

tvm.tir.Buffer

_property _B _: tvm.tir.Buffer_Â¶
    

Return type:
    

tvm.tir.Buffer

_property _C _: tvm.tir.Buffer_Â¶
    

Return type:
    

tvm.tir.Buffer

_property _ARegionÂ¶
    

_property _BRegionÂ¶
    

_property _CRegionÂ¶
    

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

_property _clear_accum _: tvm.ir.PrimExpr_Â¶
    

Return type:
    

tvm.ir.PrimExpr

_property _k_pack _: int_Â¶
    

Return type:
    

int

_property _wg_wait _: int_Â¶
    

Return type:
    

int

_property _policy _: [tilelang.tileop.base.GemmWarpPolicy](../../base/index.html#tilelang.tileop.base.GemmWarpPolicy "tilelang.tileop.base.GemmWarpPolicy")_Â¶
    

Return type:
    

[tilelang.tileop.base.GemmWarpPolicy](../../base/index.html#tilelang.tileop.base.GemmWarpPolicy "tilelang.tileop.base.GemmWarpPolicy")

_property _mbarptr _: tvm.ir.PrimExpr_Â¶
    

Return type:
    

tvm.ir.PrimExpr

_property _mbar _: tvm.tir.BufferLoad | None_Â¶
    

Return type:
    

tvm.tir.BufferLoad | None

_property _C_coordsÂ¶
    

get_region_base_offsets(_region_)Â¶
    

Get the base offset (start index) for each dimension from a BufferRegion.

For example, if region is A_shared[ko % 2, 0:128, 0:64], this returns [ko % 2, 0, 0]

Parameters:
    

**region** â BufferRegion object

Returns:
    

List of PrimExpr representing the base offset for each dimension

_property _A_base_offsetsÂ¶
    

Get base offsets for each dimension of A region

_property _B_base_offsetsÂ¶
    

Get base offsets for each dimension of B region

_property _C_base_offsetsÂ¶
    

Get base offsets for each dimension of C region
