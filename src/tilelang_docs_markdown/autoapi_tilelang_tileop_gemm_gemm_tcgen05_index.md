# tilelang.tileop.gemm.gemm_tcgen05Â¶

## ClassesÂ¶

`GemmTCGEN5` | GEMM operator for Blackwell (SM100) TCGEN5MMA instructions.  
---|---  
  
## Module ContentsÂ¶

_class _tilelang.tileop.gemm.gemm_tcgen05.GemmTCGEN5Â¶
    

Bases: [`tilelang.tileop.gemm.gemm_base.GemmBase`](../gemm_base/index.html#tilelang.tileop.gemm.gemm_base.GemmBase "tilelang.tileop.gemm.gemm_base.GemmBase")

GEMM operator for Blackwell (SM100) TCGEN5MMA instructions.

Supports the SS (Shared-Shared) and TS (TensorMemory-Shared) variants. Layout inference and lowering are dispatched based on the memory scopes of operands A and B.

infer_layout(_target_ , _thread_nums_)Â¶
    

Infer swizzled layouts for operands and accumulator.

For SS: both A and B get swizzled shared-memory layouts. For TS: A and C get TMEM store layouts, B gets a swizzled shared-memory layout.

Parameters:
    

  * **target** (_tvm.target.Target_)

  * **thread_nums** (_int_)




lower(_layout_map_ , _target_ , _thread_bounds_ , _thread_var_)Â¶
    

Lower the GEMM tile-op into a TIR prim_func containing TCGEN5MMA calls.

Parameters:
    

  * **layout_map** (_dict_)

  * **target** (_tvm.target.Target_)

  * **thread_bounds** (_tvm.ir.Range_)

  * **thread_var** (_tvm.tir.Var_)



