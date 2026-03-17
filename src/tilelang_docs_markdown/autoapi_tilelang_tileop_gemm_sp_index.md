# tilelang.tileop.gemm_spÂ¶

## SubmodulesÂ¶

  * [tilelang.tileop.gemm_sp.gemm_sp_base](gemm_sp_base/index.html)
  * [tilelang.tileop.gemm_sp.gemm_sp_mma](gemm_sp_mma/index.html)



## ClassesÂ¶

`GemmSPPy` |   
---|---  
  
## FunctionsÂ¶

`gemm_sp_py_infer_layout`(gemm_sp_py, target, thread_bounds) |   
---|---  
`gemm_sp_py_lower`(gemm_sp_py, target, thread_bounds, ...) |   
  
## Package ContentsÂ¶

tilelang.tileop.gemm_sp.gemm_sp_py_infer_layout(_gemm_sp_py_ , _target_ , _thread_bounds_)Â¶
    

Parameters:
    

  * **gemm_sp_py** ([_gemm_sp_mma.GemmSPMMA_](gemm_sp_mma/index.html#tilelang.tileop.gemm_sp.gemm_sp_mma.GemmSPMMA "tilelang.tileop.gemm_sp.gemm_sp_mma.GemmSPMMA"))

  * **target** (_tvm.target.Target_)

  * **thread_bounds** (_tvm.ir.Range_)




tilelang.tileop.gemm_sp.gemm_sp_py_lower(_gemm_sp_py_ , _target_ , _thread_bounds_ , _thread_var_)Â¶
    

Parameters:
    

  * **gemm_sp_py** ([_gemm_sp_mma.GemmSPMMA_](gemm_sp_mma/index.html#tilelang.tileop.gemm_sp.gemm_sp_mma.GemmSPMMA "tilelang.tileop.gemm_sp.gemm_sp_mma.GemmSPMMA"))

  * **target** (_tvm.target.Target_)

  * **thread_bounds** (_tvm.ir.Range_)

  * **thread_var** (_tvm.tir.Var_)




_class _tilelang.tileop.gemm_sp.GemmSPPyÂ¶
    

Bases: `tvm.ir.base.Node`, `tvm.runtime.Scriptable`

A _: tvm.tir.Buffer_Â¶
    

E _: tvm.tir.Buffer_Â¶
    

B _: tvm.tir.Buffer_Â¶
    

C _: tvm.tir.Buffer_Â¶
    

APtr _: tvm.tir.PrimExpr_Â¶
    

EPtr _: tvm.tir.PrimExpr_Â¶
    

BPtr _: tvm.tir.PrimExpr_Â¶
    

CPtr _: tvm.tir.PrimExpr_Â¶
    

M _: int_Â¶
    

N _: int_Â¶
    

K _: int_Â¶
    

trans_A _: [bool](../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool")_Â¶
    

trans_B _: [bool](../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool")_Â¶
    

stride_A _: int_Â¶
    

stride_B _: int_Â¶
    

offset_A _: int_Â¶
    

offset_B _: int_Â¶
    

clear_accum _: [bool](../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool")_Â¶
    

k_pack _: int_Â¶
    

wg_wait _: int_Â¶
    

policy _: [tilelang.tileop.base.GemmWarpPolicy](../base/index.html#tilelang.tileop.base.GemmWarpPolicy "tilelang.tileop.base.GemmWarpPolicy")_Â¶
    

infer_layout(_target_ , _thread_nums_)Â¶
    

Parameters:
    

  * **target** (_tvm.target.Target_)

  * **thread_nums** (_int_)




lower(_target_ , _thread_nums_ , _thread_var_)Â¶
    

Parameters:
    

  * **target** (_tvm.target.Target_)

  * **thread_nums** (_int_)

  * **thread_var** (_tvm.tir.Var_)



