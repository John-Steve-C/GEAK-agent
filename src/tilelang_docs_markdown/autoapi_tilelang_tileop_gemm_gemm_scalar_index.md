# tilelang.tileop.gemm.gemm_scalarÂ¶

## ClassesÂ¶

`GemmScalar` | CPU scalar fallback: triple nested loop gemm.  
---|---  
  
## Module ContentsÂ¶

_class _tilelang.tileop.gemm.gemm_scalar.GemmScalarÂ¶
    

Bases: [`tilelang.tileop.gemm.gemm_base.GemmBase`](../gemm_base/index.html#tilelang.tileop.gemm.gemm_base.GemmBase "tilelang.tileop.gemm.gemm_base.GemmBase")

CPU scalar fallback: triple nested loop gemm.

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



