# tilelang.carver.template.gemvÂ¶

## ClassesÂ¶

`GEMVTemplate` | A template for Generalized Matrix-Vector Multiplication (GEMV).  
---|---  
  
## Module ContentsÂ¶

_class _tilelang.carver.template.gemv.GEMVTemplateÂ¶
    

Bases: [`tilelang.carver.template.base.BaseTemplate`](../base/index.html#tilelang.carver.template.base.BaseTemplate "tilelang.carver.template.base.BaseTemplate")

A template for Generalized Matrix-Vector Multiplication (GEMV).

This template defines the computation for a matrix-vector multiplication with configurable parameters such as transposition, data types, and bias addition.

N _: int_ _ = None_Â¶
    

K _: int_ _ = None_Â¶
    

trans_B _: [bool](../../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool")_ _ = True_Â¶
    

in_dtype _: str_ _ = 'float16'_Â¶
    

out_dtype _: str_ _ = 'float16'_Â¶
    

accum_dtype _: str_ _ = 'float16'_Â¶
    

with_bias _: [bool](../../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool")_ _ = False_Â¶
    

get_hardware_aware_configs(_arch =None_, _topk =10_)Â¶
    

Retrieves optimized hardware-aware configurations.

Parameters:
    

  * **arch** ([_TileDevice_](../../arch/arch_base/index.html#tilelang.carver.arch.arch_base.TileDevice "tilelang.carver.arch.arch_base.TileDevice") _,__optional_) â The target hardware architecture.

  * **topk** (_int_ _,__optional_) â Number of top configurations to consider.



Returns:
    

A list of optimization hints for hardware acceleration.

Return type:
    

List[[Hint](../../roller/hint/index.html#tilelang.carver.roller.hint.Hint "tilelang.carver.roller.hint.Hint")]

initialize_function()Â¶
    

Defines and initializes the GEMV computation function.

This method sets up placeholders for input matrices, computes the matrix-vector multiplication using TVMâs compute API, and optionally applies bias and type casting.

Return type:
    

None

params_as_dict()Â¶
    

Returns the template parameters as a dictionary.

Returns:
    

Dictionary containing template parameter values.

Return type:
    

dict

_property _class_attributesÂ¶
    

Returns the class attributes in dictionary form.

Returns:
    

Dictionary of class attributes.

Return type:
    

dict

__repr__()Â¶
    

Returns a string representation of the class instance.

Returns:
    

A formatted string representation of the class.

Return type:
    

str
