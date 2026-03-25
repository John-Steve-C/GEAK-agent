# tilelang.tileop.gemmÂ¶

## SubmodulesÂ¶

  * [tilelang.tileop.gemm.gemm_base](gemm_base/index.html)
  * [tilelang.tileop.gemm.gemm_mfma](gemm_mfma/index.html)
  * [tilelang.tileop.gemm.gemm_mma](gemm_mma/index.html)
  * [tilelang.tileop.gemm.gemm_mma_sm70](gemm_mma_sm70/index.html)
  * [tilelang.tileop.gemm.gemm_scalar](gemm_scalar/index.html)
  * [tilelang.tileop.gemm.gemm_tcgen05](gemm_tcgen05/index.html)
  * [tilelang.tileop.gemm.gemm_wgmma](gemm_wgmma/index.html)
  * [tilelang.tileop.gemm.inst](inst/index.html)



## ClassesÂ¶

`GemmPy` |   
---|---  
  
## FunctionsÂ¶

`gemm_py_infer_layout`(gemm_py, target, thread_bounds) |   
---|---  
`gemm_py_lower`(gemm_py, layout_map, target, ...) |   
  
## Package ContentsÂ¶

tilelang.tileop.gemm.gemm_py_infer_layout(_gemm_py_ , _target_ , _thread_bounds_)Â¶
    

Parameters:
    

  * **gemm_py** ([_gemm_mma.GemmMMA_](gemm_mma/index.html#tilelang.tileop.gemm.gemm_mma.GemmMMA "tilelang.tileop.gemm.gemm_mma.GemmMMA"))

  * **target** (_tvm.target.Target_)

  * **thread_bounds** (_tvm.ir.Range_)




tilelang.tileop.gemm.gemm_py_lower(_gemm_py_ , _layout_map_ , _target_ , _thread_bounds_ , _thread_var_)Â¶
    

Parameters:
    

  * **gemm_py** ([_gemm_mma.GemmMMA_](gemm_mma/index.html#tilelang.tileop.gemm.gemm_mma.GemmMMA "tilelang.tileop.gemm.gemm_mma.GemmMMA"))

  * **target** (_tvm.target.Target_)

  * **thread_bounds** (_tvm.ir.Range_)

  * **thread_var** (_tvm.tir.Var_)




_class _tilelang.tileop.gemm.GemmPyÂ¶
    

Bases: `tvm.ir.base.Node`, `tvm.runtime.Scriptable`

_property _AÂ¶
    

_property _BÂ¶
    

_property _CÂ¶
    

_property _APtrÂ¶
    

_property _BPtrÂ¶
    

_property _CPtrÂ¶
    

_property _MÂ¶
    

_property _NÂ¶
    

_property _KÂ¶
    

_property _trans_AÂ¶
    

_property _trans_BÂ¶
    

_property _stride_AÂ¶
    

_property _stride_BÂ¶
    

_property _offset_AÂ¶
    

_property _offset_BÂ¶
    

_property _clear_accumÂ¶
    

_property _k_packÂ¶
    

_property _wg_waitÂ¶
    

infer_layout(_target_ , _thread_nums_)Â¶
    

Infer the layout for the GEMM operation based on target architecture.

Parameters:
    

  * **target** (_tvm.target.Target_)

  * **thread_nums** (_int_)




lower(_layout_map_ , _target_ , _thread_bounds_ , _thread_var_)Â¶
    

Lower the GEMM operation to TIR statements based on target architecture.

Parameters:
    

  * **layout_map** (_dict_)

  * **target** (_tvm.target.Target_)

  * **thread_bounds** (_tvm.ir.Range_)

  * **thread_var** (_tvm.tir.Var_)



