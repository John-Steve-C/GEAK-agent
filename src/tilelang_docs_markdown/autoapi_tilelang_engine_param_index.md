# tilelang.engine.paramÂ¶

The profiler and convert to torch utils

## ClassesÂ¶

`KernelParam` | Represents parameters for a kernel operation, storing dtype and shape information.  
---|---  
`CompiledArtifact` | Represents a compiled kernel artifact containing both host and device code.  
  
## Module ContentsÂ¶

_class _tilelang.engine.param.KernelParamÂ¶
    

Represents parameters for a kernel operation, storing dtype and shape information. Used to describe tensor or scalar parameters in TVM/PyTorch interop.

dtype _: tilelang.tvm.DataType_Â¶
    

shape _: list[int | tvm.tir.Var]_Â¶
    

_classmethod _from_buffer(_buffer_)Â¶
    

Creates a KernelParam instance from a TVM Buffer object.

Parameters:
    

**buffer** (_tvm.tir.Buffer_) â TVM Buffer object containing dtype and shape information

Returns:
    

KernelParam instance with dtype directly from buffer and shape

Raises:
    

**ValueError** â If dimension type is not supported (not IntImm or Var)

_classmethod _from_var(_var_)Â¶
    

Creates a KernelParam instance from a TVM Variable object. Used for scalar parameters.

Parameters:
    

**var** (_tvm.tir.Var_) â TVM Variable object containing dtype information

Returns:
    

KernelParam instance representing a scalar (empty shape)

is_scalar()Â¶
    

Checks if the parameter represents a scalar value.

Returns:
    

True if parameter has no dimensions (empty shape), False otherwise

Return type:
    

[bool](../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool")

is_unsigned()Â¶
    

Checks if the parameter represents an unsigned integer type.

Returns:
    

True if parameter is an unsigned integer type, False otherwise

Return type:
    

[bool](../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool")

is_float8()Â¶
    

Checks if the parameter represents a float8 type.

Returns:
    

True if parameter is a float8 type, False otherwise

Return type:
    

[bool](../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool")

is_float4()Â¶
    

Checks if the parameter represents a float4 type.

Returns:
    

True if parameter is a float4 type, False otherwise

Return type:
    

[bool](../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool")

is_boolean()Â¶
    

Checks if the parameter represents a boolean type.

Returns:
    

True if parameter is a boolean type, False otherwise

Return type:
    

[bool](../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool")

torch_dtype()Â¶
    

Converts the TVM DataType to PyTorch dtype.

This method is used when creating PyTorch tensors from KernelParam, as PyTorchâs tensor creation functions require torch.dtype.

Returns:
    

Corresponding PyTorch dtype

Return type:
    

torch.dtype

Example
    
    
    >>> param = KernelParam.from_buffer(buffer)
    >>> tensor = torch.empty(shape, dtype=param.torch_dtype())
    

tilelang_dtype()Â¶
    

Converts the TVM DataType to TileLang dtype.

Returns:
    

Corresponding TileLang dtype

Return type:
    

T.dtype

_class _tilelang.engine.param.CompiledArtifactÂ¶
    

Represents a compiled kernel artifact containing both host and device code. Stores all necessary components for kernel execution in the TVM runtime.

host_mod _: tilelang.tvm.IRModule_Â¶
    

device_mod _: tilelang.tvm.IRModule_Â¶
    

params _: list[KernelParam]_Â¶
    

kernel_source _: str_Â¶
    

rt_mod _: tilelang.tvm.runtime.Module | None_ _ = None_Â¶
    
