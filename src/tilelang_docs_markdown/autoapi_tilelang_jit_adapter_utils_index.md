# tilelang.jit.adapter.utilsÂ¶

## ClassesÂ¶

`TMADescriptorParams` | Parsed TMA descriptor parameters.  
---|---  
  
## FunctionsÂ¶

`match_global_kernel`(source[, annotation]) |   
---|---  
`match_declare_kernel`(source[, annotation]) |   
`match_declare_kernel_cutedsl`(source[, annotation]) |   
`extract_python_func_declaration`(source, func_name) | Extract the full Python function declaration from decorator to colon.  
`match_declare_kernel_cpu`(source[, annotation]) |   
`is_cuda_target`(target) |   
`is_hip_target`(target) |   
`is_cpu_target`(target) |   
`is_metal_target`(target) |   
`is_cutedsl_target`(target) |   
`get_annotated_mod`(func_or_mod[, target, target_host, ...]) |   
`pythonic_expr`(expr[, dtype_map, ignore_cast, floor_div_op]) | Converts a TVM PrimExpr into a Python-style string, correctly handling operator precedence.  
`maybe_desc_name`(name, matches, i[, desc_name_map]) | Check if a parameter name corresponds to a TMA descriptor.  
`parse_function_call_args`(declaration, function_args, ...) | Parse function call arguments from a kernel declaration.  
`parse_tma_descriptor_args`(tma_descriptor_args, ...) | Parse TMA descriptor arguments into structured parameters.  
  
## Module ContentsÂ¶

tilelang.jit.adapter.utils.match_global_kernel(_source_ , _annotation ='__global__'_)Â¶
    

Parameters:
    

  * **source** (_str_)

  * **annotation** (_str_)



Return type:
    

int

tilelang.jit.adapter.utils.match_declare_kernel(_source_ , _annotation ='__global__'_)Â¶
    

Parameters:
    

  * **source** (_str_)

  * **annotation** (_str_)



Return type:
    

int

tilelang.jit.adapter.utils.match_declare_kernel_cutedsl(_source_ , _annotation ='@cute.kernel'_)Â¶
    

Parameters:
    

  * **source** (_str_)

  * **annotation** (_str_)



Return type:
    

int

tilelang.jit.adapter.utils.extract_python_func_declaration(_source_ , _func_name_)Â¶
    

Extract the full Python function declaration from decorator to colon.

Parameters:
    

  * **source** (_str_) â Source code containing the function

  * **func_name** (_str_) â Name of the function to extract (can include â(â suffix)



Returns:
    

â, including parameters

Return type:
    

The function declaration from âdefâ to â

Example

For code:
    

@cute.kernel def kernel(arg1: cute.Tensor, arg2: int):

> â¦

Returns: âdef kernel(arg1: cute.Tensor, arg2: int)â

tilelang.jit.adapter.utils.match_declare_kernel_cpu(_source_ , _annotation ='int32_t'_)Â¶
    

Parameters:
    

  * **source** (_str_)

  * **annotation** (_str_)



Return type:
    

int

tilelang.jit.adapter.utils.is_cuda_target(_target_)Â¶
    

Parameters:
    

**target** (_tvm.target.Target_)

Return type:
    

[bool](../../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool")

tilelang.jit.adapter.utils.is_hip_target(_target_)Â¶
    

Parameters:
    

**target** (_tvm.target.Target_)

Return type:
    

[bool](../../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool")

tilelang.jit.adapter.utils.is_cpu_target(_target_)Â¶
    

Parameters:
    

**target** (_tvm.target.Target_)

Return type:
    

[bool](../../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool")

tilelang.jit.adapter.utils.is_metal_target(_target_)Â¶
    

Parameters:
    

**target** (_tvm.target.Target_)

Return type:
    

[bool](../../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool")

tilelang.jit.adapter.utils.is_cutedsl_target(_target_)Â¶
    

Parameters:
    

**target** (_tvm.target.Target_)

Return type:
    

[bool](../../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool")

tilelang.jit.adapter.utils.get_annotated_mod(_func_or_mod_ , _target ='auto'_, _target_host =None_, _model_type ='all'_)Â¶
    

Parameters:
    

  * **func_or_mod** (_tvm.tir.PrimFunc_ _|__tilelang.tvm.IRModule_)

  * **target** (_str_ _|__tvm.target.Target_)

  * **target_host** (_str_ _|__tvm.target.Target_ _|__None_)

  * **model_type** (_Literal_ _[__'device'__,__'host'__,__'all'__]_)



Return type:
    

tvm.IRModule | tuple[tvm.IRModule, tvm.IRModule]

tilelang.jit.adapter.utils.pythonic_expr(_expr_ , _dtype_map =None_, _ignore_cast =False_, _floor_div_op ='/'_)Â¶
    

Converts a TVM PrimExpr into a Python-style string, correctly handling operator precedence.

Parameters:
    

  * **expr** (_tilelang.tvm.tir.PrimExpr_) â The TVM PrimExpr to convert.

  * **dtype_map** (_dict_ _[__str_ _,__str_ _]__|__None_) â A dictionary mapping data types to their string representations.

  * **ignore_cast** ([_bool_](../../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool")) â Whether to ignore the cast operator and return the string representation of the value without the cast.

  * **floor_div_op** (_str_) â Operator to use for tvm.tir.FloorDiv. Default â/â preserves prior behavior (suitable for generating C/C++ expressions). For generating Python code where integer division is required (e.g. grid/block), pass â//â explicitly.



Returns:
    

A string representation of the expression.

Return type:
    

str

tilelang.jit.adapter.utils.maybe_desc_name(_name_ , _matches_ , _i_ , _desc_name_map =None_)Â¶
    

Check if a parameter name corresponds to a TMA descriptor.

Parameters:
    

  * **name** (_str_) â The parameter name to check.

  * **matches** (_list_ _[__str_ _]_) â List of all matched parameter names.

  * **i** (_int_) â Index of the current match.

  * **desc_name_map** (_dict_ _[__str_ _,__str_ _]__|__None_) â Optional mapping to store descriptor name relationships.



Returns:
    

True if the parameter is a TMA descriptor.

Return type:
    

[bool](../../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool")

tilelang.jit.adapter.utils.parse_function_call_args(_declaration_ , _function_args_ , _function_params_ , _desc_name_map =None_, _desc_name_var_map =None_, _transform_arg =None_)Â¶
    

Parse function call arguments from a kernel declaration.

Parameters:
    

  * **declaration** (_str_) â The kernel function declaration string.

  * **function_args** (_list_ _[__dict_ _[__str_ _,__str_ _]__]_) â List of function argument specifications.

  * **function_params** (_list_ _[__Any_ _]_) â List of function parameters from TVM IR.

  * **desc_name_map** (_dict_ _[__str_ _,__str_ _]__|__None_) â Optional mapping for descriptor names.

  * **desc_name_var_map** (_dict_ _[__str_ _,__tilelang.tvm.tir.Var_ _]__|__None_) â Optional mapping from descriptor names to TVM variables.

  * **transform_arg** (_Callable_ _[__[__str_ _,__str_ _]__,__Any_ _]__|__None_) â Optional function to transform each argument (name, type) -> result.



Returns:
    

List of parsed call arguments.

Return type:
    

list[Any]

_class _tilelang.jit.adapter.utils.TMADescriptorParams(_handle_name_ , _dtype_ , _tensor_rank_ , _global_address_ , _is_img2col =False_)Â¶
    

Parsed TMA descriptor parameters.

Parameters:
    

  * **handle_name** (_str_)

  * **dtype** (_str_)

  * **tensor_rank** (_int_)

  * **global_address** (_Any_)

  * **is_img2col** ([_bool_](../../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool"))




handle_nameÂ¶
    

dtypeÂ¶
    

tensor_rankÂ¶
    

global_addressÂ¶
    

is_img2col _ = False_Â¶
    

global_dim _: list[str]__ = []_Â¶
    

global_stride _: list[str]__ = []_Â¶
    

element_strides _: list[str]__ = []_Â¶
    

interleave _: str_ _ = ''_Â¶
    

swizzle _: str_ _ = ''_Â¶
    

l2_promotion _: str_ _ = ''_Â¶
    

oob_fill _: str_ _ = ''_Â¶
    

box_dim _: list[str]__ = []_Â¶
    

lower_corner _: list[str]__ = []_Â¶
    

upper_corner _: list[str]__ = []_Â¶
    

smem_box_channel _: str_ _ = ''_Â¶
    

smem_box_pixel _: str_ _ = ''_Â¶
    

tilelang.jit.adapter.utils.parse_tma_descriptor_args(_tma_descriptor_args_ , _desc_name_map_ , _desc_name_var_map_ , _pythonic_expr_func_)Â¶
    

Parse TMA descriptor arguments into structured parameters.

Parameters:
    

  * **tma_descriptor_args** (_dict_ _[__tilelang.tvm.tir.Var_ _,__list_ _[__Any_ _]__]_) â Dictionary mapping TMA descriptor variables to their arguments.

  * **desc_name_map** (_dict_ _[__str_ _,__str_ _]_) â Mapping from descriptor handles to parameter names.

  * **desc_name_var_map** (_dict_ _[__str_ _,__tilelang.tvm.tir.Var_ _]_) â Mapping from descriptor handles to TVM variables.

  * **pythonic_expr_func** (_Callable_ _[__[__Any_ _]__,__str_ _]_) â Function to convert TVM expressions to strings.



Returns:
    

List of parsed TMA descriptor parameters.

Return type:
    

list[TMADescriptorParams]
