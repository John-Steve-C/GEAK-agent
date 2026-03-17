# tilelang.carver.utilsÂ¶

## AttributesÂ¶

`logger` |   
---|---  
  
## FunctionsÂ¶

`get_rasterization_code`([pannel_width]) |   
---|---  
`get_roller_hints_from_func`(func_or_module, arch[, ...]) |   
`get_roller_hints_from_output_nodes`(output_nodes, arch) |   
`retrieve_func_from_module`(ir_module) |   
  
## Module ContentsÂ¶

tilelang.carver.utils.loggerÂ¶
    

tilelang.carver.utils.get_rasterization_code(_pannel_width =8_)Â¶
    

Parameters:
    

**pannel_width** (_int_)

Return type:
    

str

tilelang.carver.utils.get_roller_hints_from_func(_func_or_module_ , _arch_ , _topk =10_, _tensorcore_only =False_, _allow_gemv =False_)Â¶
    

Parameters:
    

  * **func_or_module** (_tvm.tir.PrimFunc_ _|__tvm.IRModule_)

  * **arch** (_tilelang.carver.arch.TileDevice_)

  * **topk** (_int_)

  * **tensorcore_only** ([_bool_](../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool"))

  * **allow_gemv** ([_bool_](../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool"))



Return type:
    

list[[tilelang.carver.roller.hint.Hint](../roller/hint/index.html#tilelang.carver.roller.hint.Hint "tilelang.carver.roller.hint.Hint")] | None

tilelang.carver.utils.get_roller_hints_from_output_nodes(_output_nodes_ , _arch_ , _topk =10_, _extra_tags =None_)Â¶
    

Parameters:
    

  * **output_nodes** (_list_ _[_[_tilelang.carver.roller.node.OutputNode_](../roller/node/index.html#tilelang.carver.roller.node.OutputNode "tilelang.carver.roller.node.OutputNode") _]_)

  * **arch** (_tilelang.carver.arch.TileDevice_)

  * **topk** (_int_)

  * **extra_tags** (_list_ _[__str_ _]__|__None_)



Return type:
    

list[[tilelang.carver.roller.hint.Hint](../roller/hint/index.html#tilelang.carver.roller.hint.Hint "tilelang.carver.roller.hint.Hint")] | None

tilelang.carver.utils.retrieve_func_from_module(_ir_module_)Â¶
    

Parameters:
    

**ir_module** (_tvm.IRModule_)

Return type:
    

tvm.tir.PrimFunc
