# tilelang.carver.template.matmulÂ¶

## ClassesÂ¶

`MatmulTemplate` | A template for matrix multiplication (MatMul).  
---|---  
  
## Module ContentsÂ¶

_class _tilelang.carver.template.matmul.MatmulTemplateÂ¶
    

Bases: [`tilelang.carver.template.base.BaseTemplate`](../base/index.html#tilelang.carver.template.base.BaseTemplate "tilelang.carver.template.base.BaseTemplate")

A template for matrix multiplication (MatMul).

This class defines the computation for a matrix-matrix multiplication with configurable parameters such as transposition, data types, and bias addition.

MÂ¶
    

Number of rows in matrix A and matrix C.

Type:
    

int

NÂ¶
    

Number of columns in matrix B and matrix C.

Type:
    

int

KÂ¶
    

Number of columns in matrix A and rows in matrix B.

Type:
    

int

trans_AÂ¶
    

Whether to transpose matrix A before multiplication.

Type:
    

[bool](../../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool")

trans_BÂ¶
    

Whether to transpose matrix B before multiplication.

Type:
    

[bool](../../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool")

in_dtypeÂ¶
    

Data type of input matrices.

Type:
    

str

out_dtypeÂ¶
    

Data type of output matrix.

Type:
    

str

accum_dtypeÂ¶
    

Data type used for accumulation.

Type:
    

str

with_biasÂ¶
    

Whether to add a bias term.

Type:
    

[bool](../../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool")

M _: int_ _ = None_Â¶
    

N _: int_ _ = None_Â¶
    

K _: int_ _ = None_Â¶
    

trans_A _: [bool](../../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool")_ _ = False_Â¶
    

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
    

Defines and initializes the matrix multiplication computation.

This method sets up placeholders for input matrices, computes the matrix multiplication using TVMâs compute API, and optionally applies bias and type casting.

Raises:
    

**AssertionError** â If M, N, or K are not positive integers.

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
