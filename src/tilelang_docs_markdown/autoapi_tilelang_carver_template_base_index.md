# tilelang.carver.template.baseÂ¶

## ClassesÂ¶

`BaseTemplate` | Base class template for hardware-aware configurations.  
---|---  
  
## Module ContentsÂ¶

_class _tilelang.carver.template.base.BaseTemplateÂ¶
    

Bases: `abc.ABC`

Base class template for hardware-aware configurations. This serves as an abstract base class (ABC) that defines the structure for subclasses implementing hardware-specific optimizations.

_abstract _get_hardware_aware_configs(_arch =None_, _topk =10_)Â¶
    

Abstract method that must be implemented by subclasses. It should return a list of hardware-aware configurations (hints) based on the specified architecture.

Parameters:
    

  * **arch** ([_TileDevice_](../../arch/arch_base/index.html#tilelang.carver.arch.arch_base.TileDevice "tilelang.carver.arch.arch_base.TileDevice") _,__optional_) â The target architecture. Defaults to None.

  * **topk** (_int_ _,__optional_) â Number of top configurations to return. Defaults to 10.



Returns:
    

A list of recommended hardware-aware configurations.

Return type:
    

List[[Hint](../../roller/hint/index.html#tilelang.carver.roller.hint.Hint "tilelang.carver.roller.hint.Hint")]

with_arch(_arch_)Â¶
    

Sets the architecture for this template and returns itself.

Parameters:
    

**arch** ([_TileDevice_](../../arch/arch_base/index.html#tilelang.carver.arch.arch_base.TileDevice "tilelang.carver.arch.arch_base.TileDevice")) â The architecture to set.

Returns:
    

The instance with the updated architecture.

Return type:
    

BaseTemplate

has_arch()Â¶
    

Checks whether the architecture is set.

Returns:
    

True if the architecture is set, False otherwise.

Return type:
    

[bool](../../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool")

is_volta_arch()Â¶
    

Checks if the current architecture is a Volta architecture.

Returns:
    

True if the architecture is Volta, False otherwise.

Return type:
    

[bool](../../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool")

is_ampere_arch()Â¶
    

Checks if the current architecture is an Ampere architecture.

Returns:
    

True if the architecture is Ampere, False otherwise.

Return type:
    

[bool](../../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool")

is_cdna_arch()Â¶
    

Checks if the current architecture is a CDNA architecture.

Returns:
    

True if the architecture is CDNA, False otherwise.

Return type:
    

[bool](../../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool")

equivalent_function()Â¶
    

Returns the function associated with this template.

Returns:
    

The stored function.

Return type:
    

[PrimFunc](../../../language/eager/builder/index.html#tilelang.language.eager.builder.PrimFunc "tilelang.language.eager.builder.PrimFunc")

_abstract _initialize_function()Â¶
    

Placeholder method that should be implemented by subclasses. This method is responsible for initializing the function.

Raises:
    

**NotImplementedError** â If not implemented in the subclass.

Return type:
    

None

set_function(_func_)Â¶
    

Sets the function for this template and returns itself.

Parameters:
    

**func** ([_PrimFunc_](../../../language/eager/builder/index.html#tilelang.language.eager.builder.PrimFunc "tilelang.language.eager.builder.PrimFunc")) â The function to associate with this template.

Returns:
    

The instance with the updated function.

Return type:
    

BaseTemplate

set_output_nodes(_output_nodes_)Â¶
    

Sets the output nodes for this template and returns itself.

Parameters:
    

**output_nodes** (_List_ _[_[_OutputNode_](../../roller/node/index.html#tilelang.carver.roller.node.OutputNode "tilelang.carver.roller.node.OutputNode") _]_) â The output nodes to associate with this template.

Returns:
    

The instance with the updated output nodes.

Return type:
    

BaseTemplate

recommend_hints(_topk =10_)Â¶
    

Provides a list of recommended hardware-aware configurations.

Parameters:
    

**topk** (_int_ _,__optional_) â Number of top configurations to return. Defaults to 10.

Returns:
    

A list of recommended configurations.

Return type:
    

List[[Hint](../../roller/hint/index.html#tilelang.carver.roller.hint.Hint "tilelang.carver.roller.hint.Hint")]

_property _arch _: tilelang.carver.arch.TileDevice_Â¶
    

Returns the current architecture.

Returns:
    

The architecture of this template.

Return type:
    

[TileDevice](../../arch/arch_base/index.html#tilelang.carver.arch.arch_base.TileDevice "tilelang.carver.arch.arch_base.TileDevice")

_property _output_nodes _: list[[tilelang.carver.roller.node.OutputNode](../../roller/node/index.html#tilelang.carver.roller.node.OutputNode "tilelang.carver.roller.node.OutputNode")]_Â¶
    

Returns the output nodes associated with this template.

Returns:
    

The output nodes.

Return type:
    

List[[OutputNode](../../roller/node/index.html#tilelang.carver.roller.node.OutputNode "tilelang.carver.roller.node.OutputNode")]

__post_init__()Â¶
    

Post-initialization method that is called after the data class is created. Ensures that the function is initialized.
