# tilelang.tileop.gemm.gemm_mfmaÂ¶

## ClassesÂ¶

`GemmMFMA` |   
---|---  
  
## Module ContentsÂ¶

_class _tilelang.tileop.gemm.gemm_mfma.GemmMFMAÂ¶
    

Bases: [`tilelang.tileop.gemm.gemm_base.GemmBase`](../gemm_base/index.html#tilelang.tileop.gemm.gemm_base.GemmBase "tilelang.tileop.gemm.gemm_base.GemmBase")

infer_layout(_target_ , _thread_nums_)Â¶
    

Parameters:
    

  * **target** (_tvm.target.Target_)

  * **thread_nums** (_int_)




lower(_layout_map_ , _target_ , _thread_bounds_ , _thread_var_)Â¶
    

Parameters:
    

  * **layout_map** (_dict_)

  * **target** (_tvm.target.Target_)

  * **thread_bounds** (_tvm.ir.Range_)

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
