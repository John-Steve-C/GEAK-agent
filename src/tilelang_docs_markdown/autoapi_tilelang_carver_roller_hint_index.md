# tilelang.carver.roller.hintÂ¶

Hint definition for schedule

## ClassesÂ¶

`TensorCoreExtraConfig` | This class is used to store extra information for tensorcore  
---|---  
`Stride` | Manages stride information for a given axis of a tensor.  
`TileDict` | Manages tiling information and configurations for computational tasks.  
`IntrinInfo` | The information of tensorcore intrinsic related information  
`Hint` | Central configuration class for managing various parameters of computational tasks.  
  
## Module ContentsÂ¶

_class _tilelang.carver.roller.hint.TensorCoreExtraConfig(_AS_shape_ , _BS_shape_ , _AF_shape_ , _BF_shape_ , _tc_axis_)Â¶
    

This class is used to store extra information for tensorcore

Parameters:
    

  * **AS_shape** (_tuple_ _[__int_ _]_)

  * **BS_shape** (_tuple_ _[__int_ _]_)

  * **AF_shape** (_tuple_ _[__int_ _]_)

  * **BF_shape** (_tuple_ _[__int_ _]_)

  * **tc_axis** (_tuple_ _[__int_ _]_)




AS_shape _: tuple[int]_Â¶
    

BS_shape _: tuple[int]_Â¶
    

AF_shape _: tuple[int]_Â¶
    

BF_shape _: tuple[int]_Â¶
    

tc_axis _: tuple[int]_Â¶
    

_class _tilelang.carver.roller.hint.Stride(_stride =1_, _ax =-1_)Â¶
    

Manages stride information for a given axis of a tensor.

Parameters:
    

  * **stride** (_int_)

  * **ax** (_int_)




_property _ax _: int_Â¶
    

Return type:
    

int

_property _stride _: int_Â¶
    

Return type:
    

int

compute_strides_from_shape(_shape_)Â¶
    

Parameters:
    

**shape** (_list_ _[__int_ _]_)

Return type:
    

list[int]

compute_elements_from_shape(_shape_)Â¶
    

Parameters:
    

**shape** (_list_ _[__int_ _]_)

Return type:
    

int

is_valid()Â¶
    

Return type:
    

[bool](../../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool")

__repr__()Â¶
    

Return type:
    

str

_class _tilelang.carver.roller.hint.TileDict(_output_tile_)Â¶
    

Manages tiling information and configurations for computational tasks.

output_tileÂ¶
    

tile_mapÂ¶
    

rstep_mapÂ¶
    

cached_tensors_mapÂ¶
    

output_strides_mapÂ¶
    

tensor_strides_mapÂ¶
    

traffic _ = -1_Â¶
    

smem_cost _ = -1_Â¶
    

block_per_SM _ = -1_Â¶
    

num_wave _ = -1_Â¶
    

grid_size _ = -1_Â¶
    

valid _ = True_Â¶
    

get_tile(_func_)Â¶
    

Return type:
    

list[int]

get_rstep(_node_)Â¶
    

Return type:
    

dict[str, int]

__hash__()Â¶
    

Return type:
    

int

_class _tilelang.carver.roller.hint.IntrinInfo(_in_dtype_ , _out_dtype_ , _trans_b_ , _input_transform_kind =0_, _weight_transform_kind =0_)Â¶
    

The information of tensorcore intrinsic related information

Parameters:
    

  * **in_dtype** (_str_)

  * **out_dtype** (_str_)

  * **trans_b** ([_bool_](../../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool"))

  * **input_transform_kind** (_int_)

  * **weight_transform_kind** (_int_)




in_dtypeÂ¶
    

out_dtypeÂ¶
    

trans_a _ = False_Â¶
    

trans_bÂ¶
    

input_transform_kind _ = 0_Â¶
    

weight_transform_kind _ = 0_Â¶
    

__repr__()Â¶
    

Return type:
    

str

is_input_8bit()Â¶
    

Return type:
    

[bool](../../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool")

_property _smooth_a _: [bool](../../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool")_Â¶
    

Return type:
    

[bool](../../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool")

_property _smooth_b _: [bool](../../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool")_Â¶
    

Return type:
    

[bool](../../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool")

_property _inter_transform_a _: [bool](../../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool")_Â¶
    

Return type:
    

[bool](../../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool")

_property _inter_transform_b _: [bool](../../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool")_Â¶
    

Return type:
    

[bool](../../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool")

_class _tilelang.carver.roller.hint.HintÂ¶
    

Central configuration class for managing various parameters of computational tasks.

arch _ = None_Â¶
    

use_tc _ = None_Â¶
    

block _ = []_Â¶
    

thread _ = []_Â¶
    

warp _ = []_Â¶
    

rstep _ = []_Â¶
    

reduce_thread _ = []_Â¶
    

rasterization_planÂ¶
    

cached_tensors _ = []_Â¶
    

output_stridesÂ¶
    

schedule_stages _ = None_Â¶
    

block_reduction_depth _: int_ _ = None_Â¶
    

split_k_factor _: int_ _ = 1_Â¶
    

vectorize _: dict[str, int]_Â¶
    

pipeline_stage _ = 1_Â¶
    

use_async _ = False_Â¶
    

opt_shapes _: dict[str, int]_Â¶
    

intrin_infoÂ¶
    

shared_scope _: str_ _ = 'shared'_Â¶
    

pass_context _: dict_Â¶
    

to_dict()Â¶
    

Return type:
    

dict

_classmethod _from_dict(_dic_)Â¶
    

Parameters:
    

**dic** (_dict_)

Return type:
    

Hint

tensorcore_legalization()Â¶
    

_property _raxis_order _: list[int]_Â¶
    

Return type:
    

list[int]

_property _step _: list[int]_Â¶
    

Return type:
    

list[int]

__repr__()Â¶
    

Return type:
    

str

complete_config(_node_)Â¶
    

Parameters:
    

**node** (_tilelang.carver.roller.PrimFuncNode_)
