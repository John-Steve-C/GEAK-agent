# tilelang.irÂ¶

## ClassesÂ¶

`Fill` |   
---|---  
`AtomicAdd` |   
`Copy` |   
`Conv2DIm2ColOp` |   
`GemmWarpPolicy` |   
`GemmSPWarpPolicy` |   
`Gemm` |   
`GemmSP` |   
`FinalizeReducerOp` |   
`ParallelOp` |   
`ReduceOp` |   
`CumSumOp` |   
`RegionOp` |   
`ReduceType` |   
  
## Module ContentsÂ¶

_class _tilelang.ir.FillÂ¶
    

Bases: `tvm.ir.base.Node`, `tvm.runtime.Scriptable`

_class _tilelang.ir.AtomicAddÂ¶
    

Bases: `tvm.ir.base.Node`, `tvm.runtime.Scriptable`

_class _tilelang.ir.CopyÂ¶
    

Bases: `tvm.ir.base.Node`, `tvm.runtime.Scriptable`

_class _tilelang.ir.Conv2DIm2ColOpÂ¶
    

Bases: `tvm.ir.base.Node`, `tvm.runtime.Scriptable`

_class _tilelang.ir.GemmWarpPolicyÂ¶
    

Bases: `tvm.ir.base.Node`, `tvm.runtime.Scriptable`

policy_type _: int_Â¶
    

m_warp _: int_Â¶
    

n_warp _: int_Â¶
    

compute_warp_partition(_M_ , _N_ , _block_size_ , _target_ , _gemm_inst_)Â¶
    

Parameters:
    

  * **M** (_int_)

  * **N** (_int_)

  * **block_size** (_int_)

  * **target** (_tvm.target.Target_)

  * **gemm_inst** ([_tilelang.tileop.gemm.inst.GemmInst_](../tileop/gemm/inst/index.html#tilelang.tileop.gemm.inst.GemmInst "tilelang.tileop.gemm.inst.GemmInst"))




_class _tilelang.ir.GemmSPWarpPolicyÂ¶
    

Bases: `tvm.ir.base.Node`, `tvm.runtime.Scriptable`

policy_type _: int_Â¶
    

m_warp _: int_Â¶
    

n_warp _: int_Â¶
    

compute_warp_partition(_M_ , _N_ , _block_size_ , _target_ , _gemm_inst_ , _bits_)Â¶
    

Parameters:
    

  * **M** (_int_)

  * **N** (_int_)

  * **block_size** (_int_)

  * **target** (_tvm.target.Target_)

  * **gemm_inst** ([_tilelang.tileop.gemm.inst.GemmInst_](../tileop/gemm/inst/index.html#tilelang.tileop.gemm.inst.GemmInst "tilelang.tileop.gemm.inst.GemmInst"))

  * **bits** (_int_)




_class _tilelang.ir.GemmÂ¶
    

Bases: `tvm.ir.base.Node`, `tvm.runtime.Scriptable`

_class _tilelang.ir.GemmSPÂ¶
    

Bases: `tvm.ir.base.Node`, `tvm.runtime.Scriptable`

_class _tilelang.ir.FinalizeReducerOpÂ¶
    

Bases: `tvm.ir.base.Node`, `tvm.runtime.Scriptable`

_class _tilelang.ir.ParallelOpÂ¶
    

Bases: `tvm.ir.base.Node`, `tvm.runtime.Scriptable`

_class _tilelang.ir.ReduceOpÂ¶
    

Bases: `tvm.ir.base.Node`, `tvm.runtime.Scriptable`

_class _tilelang.ir.CumSumOpÂ¶
    

Bases: `tvm.ir.base.Node`, `tvm.runtime.Scriptable`

_class _tilelang.ir.RegionOpÂ¶
    

Bases: `tvm.ir.base.Node`, `tvm.runtime.Scriptable`

_class _tilelang.ir.ReduceTypeÂ¶
    

Bases: `tvm.ir.base.Node`, `tvm.runtime.Scriptable`
