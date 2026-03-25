# tilelang.carver.roller.nodeÂ¶

PrimFunc Wrapper and Block information Analaysis

## ClassesÂ¶

`BlockAnalyzer` |   
---|---  
`Edge` |   
`Node` |   
`PlaceHolderNode` |   
`PrimFuncNode` |   
`OutputNode` |   
  
## FunctionsÂ¶

`pre_order_traverse`(block_analyzer, blocks, func) |   
---|---  
`topo_order`(list_of_nodes) |   
`find_topo_sort_priority`(output_node_list) |   
`find_topo_sort`(output_node_list) |   
  
## Module ContentsÂ¶

tilelang.carver.roller.node.pre_order_traverse(_block_analyzer_ , _blocks_ , _func_)Â¶
    

_class _tilelang.carver.roller.node.BlockAnalyzer(_sch_)Â¶
    

sch _: tvm.tir.Schedule_Â¶
    

block_infos _: list[[tilelang.carver.analysis.BlockInfo](../../analysis/index.html#tilelang.carver.analysis.BlockInfo "tilelang.carver.analysis.BlockInfo")]__ = None_Â¶
    

get_block_name(_block_)Â¶
    

Parameters:
    

**block** (_tvm.tir.schedule.schedule.BlockRV_)

Return type:
    

str

get_block_info(_block_)Â¶
    

Parameters:
    

**block** (_tvm.tir.schedule.schedule.BlockRV_)

Return type:
    

[tilelang.carver.analysis.BlockInfo](../../analysis/index.html#tilelang.carver.analysis.BlockInfo "tilelang.carver.analysis.BlockInfo")

get_spatial_axis(_block_)Â¶
    

Parameters:
    

**block** (_tvm.tir.schedule.schedule.BlockRV_)

Return type:
    

list[tvm.tir.IterVar]

get_reduce_axis(_block_)Â¶
    

Parameters:
    

**block** (_tvm.tir.schedule.schedule.BlockRV_)

Return type:
    

list[tvm.tir.IterVar]

get_input_buffers(_block_)Â¶
    

Parameters:
    

**block** (_tvm.tir.schedule.schedule.BlockRV_)

Return type:
    

list[tvm.tir.Buffer]

get_output_buffers(_block_)Â¶
    

Parameters:
    

**block** (_tvm.tir.schedule.schedule.BlockRV_)

Return type:
    

list[tvm.tir.Buffer]

get_buffers(_block_)Â¶
    

Parameters:
    

**block** (_tvm.tir.schedule.schedule.BlockRV_)

Return type:
    

list[tvm.tir.Buffer]

get_producer_blocks(_block_)Â¶
    

Parameters:
    

**block** (_tvm.tir.schedule.schedule.BlockRV_)

Return type:
    

list[tvm.tir.schedule.schedule.BlockRV]

get_consumer_blocks(_block_)Â¶
    

Parameters:
    

**block** (_tvm.tir.schedule.schedule.BlockRV_)

Return type:
    

list[tvm.tir.schedule.schedule.BlockRV]

_class _tilelang.carver.roller.node.EdgeÂ¶
    

src_node _: Node_Â¶
    

dst_node _: Node_Â¶
    

src_id _: int_Â¶
    

dst_id _: int_Â¶
    

_class _tilelang.carver.roller.node.Node(_tags =None_, _name ='Node'_)Â¶
    

Parameters:
    

  * **tags** (_dict_ _|__None_)

  * **name** (_str_)




name _ = 'Node'_Â¶
    

update_tags(_tags_)Â¶
    

Parameters:
    

**tags** (_dict_)

Return type:
    

None

set_tag(_k_ , _v =True_)Â¶
    

Parameters:
    

  * **k** (_str_)

  * **v** (_Any_)



Return type:
    

None

add_tag(_k_ , _v =True_)Â¶
    

Parameters:
    

  * **k** (_str_)

  * **v** (_Any_)



Return type:
    

None

get_tag(_k_)Â¶
    

Parameters:
    

**k** (_str_)

Return type:
    

Any

is_placeholder()Â¶
    

is_output()Â¶
    

_property _inputs _: list[Edge]_Â¶
    

Return type:
    

list[Edge]

_property _outputs _: list[Edge]_Â¶
    

Return type:
    

list[Edge]

set_inputs(_i_ , _edge_)Â¶
    

Parameters:
    

  * **i** (_int_)

  * **edge** (_Edge_)




set_outputs(_i_ , _edge_)Â¶
    

Parameters:
    

  * **i** (_int_)

  * **edge** (_Edge_)




get_dtype(_id =0_)Â¶
    

Return type:
    

tvm.DataType

set_dtype(_dtype_ , _id =0_)Â¶
    

Parameters:
    

**dtype** (_tvm.DataType_)

Return type:
    

None

get_shape(_id =0_)Â¶
    

Parameters:
    

**id** (_int_)

Return type:
    

list[int]

set_shape(_shape_ , _id =0_, _overwrite =False_)Â¶
    

Parameters:
    

**shape** (_list_ _[__int_ _]_)

Return type:
    

None

num_outputs()Â¶
    

Return type:
    

int

_abstract _get_ir()Â¶
    

Return type:
    

str

__repr__()Â¶
    

Return type:
    

str

_class _tilelang.carver.roller.node.PlaceHolderNode(_name =''_)Â¶
    

Bases: `Node`

is_placeholder()Â¶
    

get_ir()Â¶
    

Return type:
    

str

_class _tilelang.carver.roller.node.PrimFuncNode(_prim_func_ , _tags =None_, _name ='PrimFuncNode'_)Â¶
    

Bases: `Node`

Parameters:
    

  * **prim_func** (_tvm.tir.PrimFunc_)

  * **tags** (_dict_ _|__None_)

  * **name** (_str_)




prim_funcÂ¶
    

sch _: tvm.tir.Schedule_Â¶
    

block_analyzer _: BlockAnalyzer_Â¶
    

schedule_stages _: list[tvm.tir.schedule.schedule.BlockRV]__ = []_Â¶
    

blocks _: list[tvm.tir.schedule.schedule.BlockRV]__ = []_Â¶
    

output_blocks _: list[tvm.tir.schedule.schedule.BlockRV]__ = None_Â¶
    

reduction_block _: tvm.tir.schedule.schedule.BlockRV_ _ = None_Â¶
    

raxis _ = []_Â¶
    

input_buffers _ = []_Â¶
    

output_buffers _ = []_Â¶
    

buffers _ = []_Â¶
    

args _ = []_Â¶
    

anaÂ¶
    

get_opt_shape(_name_)Â¶
    

Return type:
    

int

extent_wrapper(_value_)Â¶
    

Return type:
    

int

get_space_dim()Â¶
    

Return type:
    

list[int]

set_dtype(_dtype_ , _id =0_)Â¶
    

Parameters:
    

**dtype** (_tvm.DataType_)

Return type:
    

None

get_buffer_dtype(_buffer_)Â¶
    

Parameters:
    

**buffer** (_tvm.tir.Buffer_)

Return type:
    

tvm.DataType

propagate(_tile_ , _rstep =None_, _targets =None_)Â¶
    

Parameters:
    

**rstep** (_dict_ _|__None_)

propagate_inputs(_tile_ , _rstep =None_)Â¶
    

Parameters:
    

**rstep** (_dict_ _|__None_)

Return type:
    

list[list[int]]

propagate_inputs_on_reduction(_tile_ , _rstep =None_)Â¶
    

Parameters:
    

**rstep** (_dict_ _|__None_)

Return type:
    

list[list[int]]

propagate_outputs(_tile_ , _rstep =None_)Â¶
    

Parameters:
    

**rstep** (_dict_ _|__None_)

Return type:
    

list[list[int]]

propagate_reduction_inputs(_shape_ , _rstep =None_)Â¶
    

Parameters:
    

**rstep** (_dict_ _|__None_)

Return type:
    

dict[str, list[int]]

get_reduce_inputs_dtype()Â¶
    

infer_tensorcore_axis()Â¶
    

Return type:
    

tuple[int]

footprint(_shape_ , _rstep_ , _stride_map =None_)Â¶
    

Parameters:
    

**stride_map** (_dict_ _|__None_)

Return type:
    

int

get_input_buffers()Â¶
    

Return type:
    

list[tvm.tir.Buffer]

_class _tilelang.carver.roller.node.OutputNode(_node_ , _id =0_)Â¶
    

Bases: `Node`

is_output()Â¶
    

get_ir()Â¶
    

Return type:
    

str

tilelang.carver.roller.node.topo_order(_list_of_nodes_)Â¶
    

Return type:
    

list[Node]

tilelang.carver.roller.node.find_topo_sort_priority(_output_node_list_)Â¶
    

Return type:
    

list[Node]

tilelang.carver.roller.node.find_topo_sort(_output_node_list_)Â¶
    

Return type:
    

list[Node]
