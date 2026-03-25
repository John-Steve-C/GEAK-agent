# tilelang.carver.template.convÂ¶

## ClassesÂ¶

`ConvTemplate` | A template for convolution (Conv).  
---|---  
  
## Module ContentsÂ¶

_class _tilelang.carver.template.conv.ConvTemplateÂ¶
    

Bases: [`tilelang.carver.template.base.BaseTemplate`](../base/index.html#tilelang.carver.template.base.BaseTemplate "tilelang.carver.template.base.BaseTemplate")

A template for convolution (Conv).

This class defines the computation for a matrix-matrix convolution with configurable parameters such as transposition, data types, and bias addition.

NÂ¶
    

The number of input samples processed simultaneously in a batch.

Type:
    

int

CÂ¶
    

The number of input feature maps.

Type:
    

int

HÂ¶
    

The height of the input feature maps.

Type:
    

int

WÂ¶
    

The width of the input feature maps.

Type:
    

int

FÂ¶
    

The number of filters (kernels) applied, determining output depth.

Type:
    

int

KÂ¶
    

The spatial dimensions of each convolutional filter.

Type:
    

int

SÂ¶
    

The step size by which the kernel slides across the input.

Type:
    

int

DÂ¶
    

The spacing between kernel elements, controlling receptive field expansion.

Type:
    

int

PÂ¶
    

The number of pixels added to input borders to control output spatial dimensions.

Type:
    

int

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

N _: int_Â¶
    

C _: int_Â¶
    

H _: int_Â¶
    

W _: int_Â¶
    

F _: int_Â¶
    

K _: int_Â¶
    

S _: int_Â¶
    

D _: int_Â¶
    

P _: int_Â¶
    

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
    

Defines and initializes the convolution computation.

This method sets up placeholders for input matrices, computes the convolution using TVMâs compute API, and optionally applies bias and type casting.

Raises:
    

**AssertionError** â If N, C, H, W, F, K, S, D, P are not positive integers.

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
