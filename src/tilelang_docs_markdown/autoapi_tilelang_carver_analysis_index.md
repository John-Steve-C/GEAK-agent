# tilelang.carver.analysisÂ¶

Analysis on TIR blocks, loops and functions.

## ClassesÂ¶

`IterInfo` | Information about a loop/iter var.  
---|---  
`BlockInfo` | Information about a TIR block.  
  
## FunctionsÂ¶

`normalize_prim_func`(sch) | Normalize the primfunc to normal form  
---|---  
`find_var_from_func`(func, var) |   
`check_func_with_dynamic`(func) |   
`get_max_threads_per_block`(target) |   
`get_max_shared_memory_per_block`(target) |   
`get_root_block`(sch[, func_name]) |   
`collect_block_iter_vars_used_in_access_region`(block, ...) | Collect the block iter variables used in the access region of a buffer region.  
`collect_vars_used_in_prim_expr`(expr) | Collect the variables used in the PrimExpr.  
`detect_dominant_read`(block) | Detect the dominant read indices in the block.  
`is_broadcast_epilogue`(sch, block, epilogue) | Check if the epilogue block is a broadcast pattern  
`get_reduction_blocks`(sch, blocks) |   
`get_coalesced_veclen`(block_stmt[, target_bits]) |   
  
## Module ContentsÂ¶

_class _tilelang.carver.analysis.IterInfo(_kind_ , _var_ , _dom_ , _loop_rv_)Â¶
    

Information about a loop/iter var.

Parameters:
    

  * **kind** (_typing_extensions.Literal_ _[__S_ _,__R_ _,__O_ _]_)

  * **var** (_tvm.tir.Var_)

  * **dom** (_tvm.tir.PrimExpr_)

  * **loop_rv** (_tvm.tir.schedule.LoopRV_)




kind _: typing_extensions.Literal[S, R, O]_Â¶
    

var _: tvm.tir.Var_Â¶
    

loop_rv _: tvm.tir.schedule.LoopRV_Â¶
    

_property _dom _: int | tvm.tir.PrimExpr_Â¶
    

The iteration domain of the loop.

Return type:
    

int | tvm.tir.PrimExpr

__str__()Â¶
    

Return type:
    

str

__repr__()Â¶
    

Return type:
    

str

_class _tilelang.carver.analysis.BlockInfo(_name_ , _iters_ , _block_rv_ , _reduction_block =False_)Â¶
    

Information about a TIR block.

Parameters:
    

  * **name** (_str_)

  * **iters** (_list_ _[__IterInfo_ _]_)

  * **block_rv** (_tvm.tir.schedule.BlockRV_)

  * **reduction_block** ([_bool_](../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool"))




name _: str_Â¶
    

iters _: list[IterInfo]_Â¶
    

block_rv _: tvm.tir.schedule.BlockRV_Â¶
    

dom()Â¶
    

The iteration domain of the block.

Return type:
    

list[int | tvm.tir.PrimExpr]

dom_kind()Â¶
    

The iteration domain kind of the block, for example, SSSS, SSSR.

Return type:
    

str

is_injective()Â¶
    

Whether the block is injective, i.e. all its iteration domains are injective.

Return type:
    

[bool](../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool")

is_elementwise(_sch_)Â¶
    

Whether the block is elementwise, i.e. trivial mapping between read/write region

Parameters:
    

**sch** (_tvm.tir.Schedule_)

Return type:
    

[bool](../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool")

is_reduction()Â¶
    

Whether the block is a reduction workload.

Return type:
    

[bool](../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool")

_abstract _is_gemv()Â¶
    

Whether the block is a GEMV workload.

Return type:
    

[bool](../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool")

_abstract _is_gemm()Â¶
    

Whether the block is a GEMM workload.

Return type:
    

[bool](../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool")

__str__()Â¶
    

Return type:
    

str

__repr__()Â¶
    

Return type:
    

str

tilelang.carver.analysis.normalize_prim_func(_sch_)Â¶
    

Normalize the primfunc to normal form

Parameters:
    

**sch** (_tvm.tir.Schedule_)

Return type:
    

list[BlockInfo] | None

tilelang.carver.analysis.find_var_from_func(_func_ , _var_)Â¶
    

Parameters:
    

**var** (_str_)

tilelang.carver.analysis.check_func_with_dynamic(_func_)Â¶
    

tilelang.carver.analysis.get_max_threads_per_block(_target_)Â¶
    

Parameters:
    

**target** (_tvm.target.target.Target_)

Return type:
    

int

tilelang.carver.analysis.get_max_shared_memory_per_block(_target_)Â¶
    

Parameters:
    

**target** (_tvm.target.target.Target_)

Return type:
    

int

tilelang.carver.analysis.get_root_block(_sch_ , _func_name ='main'_)Â¶
    

Parameters:
    

  * **sch** (_tvm.tir.Schedule_)

  * **func_name** (_str_)



Return type:
    

tvm.tir.schedule.BlockRV

tilelang.carver.analysis.collect_block_iter_vars_used_in_access_region(_block_ , _region_)Â¶
    

Collect the block iter variables used in the access region of a buffer region.

Parameters:
    

  * **block** (_tvm.tir.Block_)

  * **region** (_list_ _[__tvm.ir.Range_ _]_)



Return type:
    

set[tvm.tir.Var]

tilelang.carver.analysis.collect_vars_used_in_prim_expr(_expr_)Â¶
    

Collect the variables used in the PrimExpr.

Parameters:
    

**expr** (_tvm.tir.PrimExpr_)

Return type:
    

set[tvm.tir.Var]

tilelang.carver.analysis.detect_dominant_read(_block_)Â¶
    

Detect the dominant read indices in the block.

Parameters:
    

**block** (_tvm.tir.Block_)

Return type:
    

tvm.tir.PrimExpr

tilelang.carver.analysis.is_broadcast_epilogue(_sch_ , _block_ , _epilogue_)Â¶
    

Check if the epilogue block is a broadcast pattern

Parameters:
    

  * **sch** (_tvm.tir.Schedule_)

  * **block** (_tvm.tir.schedule.BlockRV_)

  * **epilogue** (_tvm.tir.schedule.BlockRV_)



Return type:
    

[bool](../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool")

tilelang.carver.analysis.get_reduction_blocks(_sch_ , _blocks_)Â¶
    

Parameters:
    

  * **sch** (_tvm.tir.Schedule_)

  * **blocks** (_list_ _[__tvm.tir.schedule.BlockRV_ _]_)



Return type:
    

list[tvm.tir.schedule.BlockRV]

tilelang.carver.analysis.get_coalesced_veclen(_block_stmt_ , _target_bits =128_)Â¶
    

Parameters:
    

  * **block_stmt** (_tvm.tir.Block_)

  * **target_bits** (_int_)



Return type:
    

int
