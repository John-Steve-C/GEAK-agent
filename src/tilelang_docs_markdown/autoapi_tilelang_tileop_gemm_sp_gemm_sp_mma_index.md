# tilelang.tileop.gemm_sp.gemm_sp_mmaÂ¶

## ClassesÂ¶

`GemmSPMMA` |   
---|---  
  
## Module ContentsÂ¶

_class _tilelang.tileop.gemm_sp.gemm_sp_mma.GemmSPMMAÂ¶
    

Bases: [`tilelang.tileop.gemm_sp.gemm_sp_base.GemmSPBase`](../gemm_sp_base/index.html#tilelang.tileop.gemm_sp.gemm_sp_base.GemmSPBase "tilelang.tileop.gemm_sp.gemm_sp_base.GemmSPBase")

infer_layout(_target_ , _thread_nums_)Â¶
    

Parameters:
    

  * **target** (_tvm.target.Target_)

  * **thread_nums** (_int_)




lower(_target_ , _thread_nums_ , _thread_var_)Â¶
    

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
