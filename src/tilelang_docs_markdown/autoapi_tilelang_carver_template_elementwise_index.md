# tilelang.carver.template.elementwiseÂ¶

## ClassesÂ¶

`ElementwiseTemplate` | A template for element-wise operations using TVM.  
---|---  
  
## Module ContentsÂ¶

_class _tilelang.carver.template.elementwise.ElementwiseTemplateÂ¶
    

Bases: [`tilelang.carver.template.base.BaseTemplate`](../base/index.html#tilelang.carver.template.base.BaseTemplate "tilelang.carver.template.base.BaseTemplate")

A template for element-wise operations using TVM.

shapeÂ¶
    

The shape of the tensor.

Type:
    

List[int]

dtypeÂ¶
    

The data type of the tensor (default: âfloat16â).

Type:
    

str

shape _: list[int]__ = None_Â¶
    

dtype _: str_ _ = 'float16'_Â¶
    

get_hardware_aware_configs(_arch =None_, _topk =10_)Â¶
    

Retrieves hardware-aware optimization configurations.

Parameters:
    

  * **arch** ([_TileDevice_](../../arch/arch_base/index.html#tilelang.carver.arch.arch_base.TileDevice "tilelang.carver.arch.arch_base.TileDevice") _,__optional_) â The target hardware architecture.

  * **topk** (_int_ _,__optional_) â Number of top configurations to consider.



Returns:
    

A list of optimization hints for the given architecture.

Return type:
    

List[[Hint](../../roller/hint/index.html#tilelang.carver.roller.hint.Hint "tilelang.carver.roller.hint.Hint")]

initialize_function()Â¶
    

Initializes the element-wise computation function.

Defines a simple element-wise computation: B = A + 1, where A is an input tensor. The computation graph is built using TVMâs tensor expressions.

Return type:
    

None

params_as_dict()Â¶
    

Returns the parameters of the template as a dictionary.

Returns:
    

A dictionary containing shape and dtype.

Return type:
    

dict

_property _class_attributesÂ¶
    

Returns class attributes as a dictionary.

Returns:
    

A dictionary representation of the class attributes.

Return type:
    

dict

__repr__()Â¶
    

Returns a string representation of the object.

Returns:
    

A string describing the instance with its parameters.

Return type:
    

str
