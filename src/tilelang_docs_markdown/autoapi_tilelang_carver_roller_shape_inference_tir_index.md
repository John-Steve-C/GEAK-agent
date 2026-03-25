# tilelang.carver.roller.shape_inference.tirÂ¶

## ClassesÂ¶

`Statement` |   
---|---  
`TensorDepNode` | For tensor dependency analysis.  
`DependencyAnalysis` |   
`InputShapeInference` |   
  
## FunctionsÂ¶

`region_exist_in_list`(a, list) |   
---|---  
`walk_indice`(expr) |   
`get_analyzer_by_tir`(block_analyzer, args) |   
  
## Module ContentsÂ¶

_class _tilelang.carver.roller.shape_inference.tir.Statement(_block_analyzer_ , _block_)Â¶
    

Parameters:
    

**block** (_tvm.tir.schedule.schedule.BlockRV_)

block_analyzerÂ¶
    

blockÂ¶
    

dep_nameÂ¶
    

dependent_regionÂ¶
    

reverse_bound_inferenceÂ¶
    

make_reverse(_input_name_ , _input_iter_)Â¶
    

Parameters:
    

  * **input_name** (_str_)

  * **input_iter** (_list_ _[__tvm.tir.PrimExpr_ _]_)




_class _tilelang.carver.roller.shape_inference.tir.TensorDepNode(_name_)Â¶
    

For tensor dependency analysis.

nameÂ¶
    

add_next(_node_)Â¶
    

add_prev(_node_)Â¶
    

deduplicate(_lst_)Â¶
    

__str__()Â¶
    

__repr__()Â¶
    

_class _tilelang.carver.roller.shape_inference.tir.DependencyAnalysis(_deps_)Â¶
    

depsÂ¶
    

name2depÂ¶
    

mappingÂ¶
    

get_or_create_node(_name_)Â¶
    

traverse_dependencies(_compute_)Â¶
    

analyze()Â¶
    

print_dependencies()Â¶
    

find_path_from_source(_start_name_ , _target_name_)Â¶
    

Finds the path (if it exists) from a starting node (source) to a target node. Returns the path as a list of nodes.

_class _tilelang.carver.roller.shape_inference.tir.InputShapeInference(_deps_)Â¶
    

Parameters:
    

**deps** (_list_ _[__Statement_ _]_)

depsÂ¶
    

target_mappingÂ¶
    

buffer_mappingÂ¶
    

reduce_axes _ = []_Â¶
    

dep_analysisÂ¶
    

construct_dependency_target(_targets_)Â¶
    

Parameters:
    

**targets** (_tuple_ _[__str_ _]_)

infer(_shape_ , _rstep =None_, _targets =None_)Â¶
    

Parameters:
    

  * **shape** (_dict_ _[__str_ _,__list_ _[__tvm.arith.ConstIntBound_ _]__]_)

  * **rstep** (_dict_ _[__str_ _,__int_ _]_)




get_input_exprs(_output_exprs_)Â¶
    

tilelang.carver.roller.shape_inference.tir.region_exist_in_list(_a_ , _list_)Â¶
    

Return type:
    

[bool](../../../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool")

tilelang.carver.roller.shape_inference.tir.walk_indice(_expr_)Â¶
    

tilelang.carver.roller.shape_inference.tir.get_analyzer_by_tir(_block_analyzer_ , _args_)Â¶
    

Return type:
    

InputShapeInference
