# tilelang.carver.roller.policy.defaultÂ¶

Policy for cuda core schedule

## ClassesÂ¶

`DefaultPolicy` | Default Policy for fastdlight, a heuristic plan that tries to  
---|---  
  
## Module ContentsÂ¶

_class _tilelang.carver.roller.policy.default.DefaultPolicy(_arch_ , _tags =None_)Â¶
    

Default Policy for fastdlight, a heuristic plan that tries to minimize memory traffic and maximize parallelism.for BitBLAS Schedule.

Parameters:
    

  * **arch** (_tilelang.carver.arch.TileDevice_)

  * **tags** (_dict_ _|__None_)




func _: tvm.tir.PrimFunc_Â¶
    

nodes _: list[[tilelang.carver.roller.node.PrimFuncNode](../../node/index.html#tilelang.carver.roller.node.PrimFuncNode "tilelang.carver.roller.node.PrimFuncNode")]__ = []_Â¶
    

arch _: tilelang.carver.arch.TileDevice_Â¶
    

tags _: dict_Â¶
    

rasterizationÂ¶
    

_classmethod _from_prim_func(_func_ , _arch_ , _tags =None_, _name ='PrimFuncNode'_)Â¶
    

Parameters:
    

  * **func** (_tvm.tir.PrimFunc_)

  * **arch** (_tilelang.carver.arch.TileDevice_)

  * **tags** (_dict_ _|__None_)

  * **name** (_str_)




_classmethod _from_output_nodes(_nodes_ , _arch_ , _tags =None_)Â¶
    

Parameters:
    

  * **nodes** (_list_ _[_[_tilelang.carver.roller.node.OutputNode_](../../node/index.html#tilelang.carver.roller.node.OutputNode "tilelang.carver.roller.node.OutputNode") _]_)

  * **arch** (_tilelang.carver.arch.TileDevice_)

  * **tags** (_dict_ _|__None_)




emit_config(_topk_)Â¶
    

Parameters:
    

**topk** (_int_)

Return type:
    

list[[tilelang.carver.roller.hint.Hint](../../hint/index.html#tilelang.carver.roller.hint.Hint "tilelang.carver.roller.hint.Hint")]

dfs_smem_tile(_init_tile_ , _rstep_map_)Â¶
    

Return type:
    

collections.abc.Iterable[[tilelang.carver.roller.hint.TileDict](../../hint/index.html#tilelang.carver.roller.hint.TileDict "tilelang.carver.roller.hint.TileDict")]

get_base_tile()Â¶
    

Gets the minimum tile configuration that satisfies no redundancy in computation.

Returns:
    

The base tile configuration, which is a list of 1s equal in length to the space dimensions of the primary function node.

Return type:
    

List[int]

compute_workload_per_item(_output_tile_)Â¶
    

Return type:
    

float

score_block_size(_n_)Â¶
    

Scores a block size based on its efficiency and fit relative to the architectureâs warp size and SM partition.

Parameters:
    

**n** (_int_) â The block size to score.

Returns:
    

A tuple containing two scores representing efficiency and fit, respectively.

Return type:
    

Tuple[float, float]

get_block_size(_n_)Â¶
    

Determines the optimal block size for a given constraint, based on scoring various factors.

Parameters:
    

**n** (_int_) â The constraint size.

Returns:
    

The optimal block size chosen from the factors of n, constrained by a maximum of 1024 and scored by the score_block_size method.

Return type:
    

int

get_node_reduce_step_candidates(_node_)Â¶
    

Calculates reduction step candidates for each reduction axis in a PrimFuncNode. General idea : use factor first, since it does not require extra boundary check. for large prime number, which is rare case, use power of 2.

Parameters:
    

**node** ([_PrimFuncNode_](../../node/index.html#tilelang.carver.roller.node.PrimFuncNode "tilelang.carver.roller.node.PrimFuncNode")) â The node for which to calculate reduction step candidates. It contains reduction axes (raxis) with their domains (dom.extent).

Returns:
    

A dictionary mapping axis variable names to lists of step candidates. For each axis in the node, this function calculates possible step sizes. For axes with a large prime domain, it uses powers of 2 as step candidates; for others, it uses all factors of the domain.

Return type:
    

Dict[str, List[int]]

infer_node_smem_usage(_td_ , _node_)Â¶
    

Infers the shared memory usage of a node given a TileDict configuration.

Parameters:
    

  * **td** ([_TileDict_](../../hint/index.html#tilelang.carver.roller.hint.TileDict "tilelang.carver.roller.hint.TileDict")) â The TileDict object containing the tile configuration.

  * **node** ([_PrimFuncNode_](../../node/index.html#tilelang.carver.roller.node.PrimFuncNode "tilelang.carver.roller.node.PrimFuncNode")) â The node for which to infer the shared memory usage.



Returns:
    

The estimated amount of shared memory used by the node.

Return type:
    

int

compute_node_stride_map(_node_ , _td_)Â¶
    

Computes the stride map for a given node based on the TileDict configuration.

Parameters:
    

  * **node** ([_PrimFuncNode_](../../node/index.html#tilelang.carver.roller.node.PrimFuncNode "tilelang.carver.roller.node.PrimFuncNode")) â The node for which to compute the stride map.

  * **td** ([_TileDict_](../../hint/index.html#tilelang.carver.roller.hint.TileDict "tilelang.carver.roller.hint.TileDict")) â The TileDict object containing the tile configuration.



Returns:
    

A tuple of dictionaries containing the output strides and tensor strides.

Return type:
    

Tuple[Dict, Dict]

compute_tile_dict(_output_tile_ , _rstep_map_)Â¶
    

Computes and returns a TileDict object for a given output tile configuration and reduction step map.

Parameters:
    

  * **output_tile** (_List_ _[__int_ _]_) â The output tile configuration.

  * **rstep_map** (_Dict_) â The reduction step map.



Returns:
    

A TileDict object containing the computed tile configuration, memory traffic, shared memory cost, grid size, and other related parameters.

Return type:
    

[TileDict](../../hint/index.html#tilelang.carver.roller.hint.TileDict "tilelang.carver.roller.hint.TileDict")

check_tile_shape_isvalid(_td_)Â¶
    

Checks if the tile shapes in the TileDict are valid for the nodes in this context.

Parameters: \- td (TileDict): The TileDict object containing tile shapes and other configurations.

Returns: \- bool: True if all tile shapes are valid, False otherwise.

Parameters:
    

**td** ([_tilelang.carver.roller.hint.TileDict_](../../hint/index.html#tilelang.carver.roller.hint.TileDict "tilelang.carver.roller.hint.TileDict"))

Return type:
    

[bool](../../../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool")

recommend_block_size(_td_)Â¶
    

Recommends optimal block sizes based on the TileDict configuration.

Parameters:
    

**td** ([_TileDict_](../../hint/index.html#tilelang.carver.roller.hint.TileDict "tilelang.carver.roller.hint.TileDict")) â The TileDict object containing the tile configuration.

Returns:
    

A list of recommended block sizes sorted based on their score.

Return type:
    

List[int]

assign_block_size(_td_ , _topk =1_)Â¶
    

Assigns block sizes to the TileDict based on the recommended block sizes.

Parameters:
    

  * **td** ([_TileDict_](../../hint/index.html#tilelang.carver.roller.hint.TileDict "tilelang.carver.roller.hint.TileDict")) â The TileDict object to assign block sizes to.

  * **topk** (_int_ _,__optional_) â The number of top block sizes to consider.



Yields:
    

_Dict_ â The block size assignment for the primary function node.

plan_rasterization(_td_)Â¶
    

Plans the rasterization for the given TileDict. This function is not implemented yet.

Parameters:
    

**td** ([_TileDict_](../../hint/index.html#tilelang.carver.roller.hint.TileDict "tilelang.carver.roller.hint.TileDict")) â The TileDict object to plan rasterization for.

Raises:
    

**RasterRationPlan** â This function is not implemented yet.
