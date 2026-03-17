# tilelang.carver.roller.policy.tensorcoreÂ¶

Policy for tensorcore schedule

## AttributesÂ¶

`logger` |   
---|---  
  
## ClassesÂ¶

`TensorCorePolicy` |   
---|---  
  
## Module ContentsÂ¶

tilelang.carver.roller.policy.tensorcore.loggerÂ¶
    

_class _tilelang.carver.roller.policy.tensorcore.TensorCorePolicyÂ¶
    

Bases: [`tilelang.carver.roller.policy.default.DefaultPolicy`](../default/index.html#tilelang.carver.roller.policy.default.DefaultPolicy "tilelang.carver.roller.policy.default.DefaultPolicy")

wmma_k _: int_ _ = 16_Â¶
    

pipeline_stage _: int_ _ = 1_Â¶
    

use_async_copy _: [bool](../../../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool")_ _ = False_Â¶
    

block_reduction_depth _: int | None_ _ = None_Â¶
    

infer_node_smem_usage(_td_ , _node_)Â¶
    

Parameters:
    

  * **td** ([_tilelang.carver.roller.hint.TileDict_](../../hint/index.html#tilelang.carver.roller.hint.TileDict "tilelang.carver.roller.hint.TileDict"))

  * **node** ([_tilelang.carver.roller.node.PrimFuncNode_](../../node/index.html#tilelang.carver.roller.node.PrimFuncNode "tilelang.carver.roller.node.PrimFuncNode"))




get_node_reduce_step_candidates(_node_)Â¶
    

check_tile_shape_isvalid(_td_)Â¶
    

Parameters:
    

**td** ([_tilelang.carver.roller.hint.TileDict_](../../hint/index.html#tilelang.carver.roller.hint.TileDict "tilelang.carver.roller.hint.TileDict"))

compute_node_stride_map(_node_ , _td_)Â¶
    

Parameters:
    

  * **node** ([_tilelang.carver.roller.node.PrimFuncNode_](../../node/index.html#tilelang.carver.roller.node.PrimFuncNode "tilelang.carver.roller.node.PrimFuncNode"))

  * **td** ([_tilelang.carver.roller.hint.TileDict_](../../hint/index.html#tilelang.carver.roller.hint.TileDict "tilelang.carver.roller.hint.TileDict"))




plan_rasterization(_td_)Â¶
    

Parameters:
    

**td** ([_tilelang.carver.roller.hint.TileDict_](../../hint/index.html#tilelang.carver.roller.hint.TileDict "tilelang.carver.roller.hint.TileDict"))
