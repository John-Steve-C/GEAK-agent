# tilelang.language.proxyÂ¶

Buffer/Tensor proxy in TileLang.

## AttributesÂ¶

`Buffer` |   
---|---  
  
## ClassesÂ¶

`BufferProxy` | Buffer proxy class for constructing tir buffer.  
---|---  
`BaseTensorProxy` | Base proxy class for tensor types with configurable defaults.  
`TensorProxy` | Main tensor proxy class for global scope buffers.  
`StridedTensorProxy` | Main tensor proxy class for global scope buffers, with strides supported.  
`FragmentBufferProxy` | Proxy class for fragment memory buffers.  
`SharedBufferProxy` | Proxy class for shared memory buffers.  
`LocalBufferProxy` | Proxy class for local memory buffers.  
`BaseTensor` |   
  
## FunctionsÂ¶

`ptr`([dtype, storage_scope, is_size_var]) | Create a TIR var that represents a pointer.  
---|---  
`make_tensor`(ptr, shape[, dtype, strides]) |   
  
## Module ContentsÂ¶

_class _tilelang.language.proxy.BufferProxyÂ¶
    

Buffer proxy class for constructing tir buffer.

__call__(_shape_ , _dtype =_dtypes.float32_, _data =None_, _strides =None_, _elem_offset =None_, _scope ='global'_, _align =0_, _offset_factor =0_, _buffer_type =''_, _axis_separators =None_)Â¶
    

Parameters:
    

  * **shape** (_tilelang._typing.ShapeType_)

  * **dtype** (_tilelang._typing.DType_)



Return type:
    

tvm.tir.Buffer

__getitem__(_keys_)Â¶
    

Return type:
    

tvm.tir.Buffer

from_ptr(_pointer_var_ , _shape_ , _dtype ='float32'_, _strides =None_)Â¶
    

Create a buffer from a pointer, shape, and data type.

Parameters:
    

  * **pointer_var** (_tvm.tir.Var_) â The pointer variable

  * **shape** (_tilelang._typing.ShapeType_) â The shape of the buffer

  * **dtype** (_tilelang._typing.DType_) â The data type of the buffer (default: float32)

  * **strides** (_tuple_ _[__tvm.tir.PrimExpr_ _,__Ellipsis_ _]__|__None_)



Returns:
    

A buffer created from the given parameters

Return type:
    

tvm.tir.Buffer

_class _tilelang.language.proxy.BaseTensorProxyÂ¶
    

Base proxy class for tensor types with configurable defaults.

This class serves as a foundation for different tensor proxy types, providing customizable default values for scope, alignment, and offset factors. It implements the core functionality for creating TIR buffers with specific memory configurations.

default_scope _ = 'global'_Â¶
    

default_align _ = 0_Â¶
    

default_offset_factor _ = 0_Â¶
    

__call__(_shape_ , _dtype ='float32'_, _data =None_, _strides =None_, _elem_offset =None_, _scope =None_, _align =None_, _offset_factor =None_, _buffer_type =''_, _axis_separators =None_)Â¶
    

Parameters:
    

  * **shape** (_tilelang._typing.ShapeType_)

  * **dtype** (_tilelang._typing.DType_)



Return type:
    

tvm.tir.Buffer

__getitem__(_keys_)Â¶
    

Return type:
    

tvm.tir.Buffer

from_ptr(_pointer_var_ , _shape_ , _dtype ='float32'_, _strides =None_)Â¶
    

Create a buffer from a pointer, shape, and data type.

Parameters:
    

  * **pointer_var** (_tvm.tir.Var_) â The pointer variable

  * **shape** (_tilelang._typing.ShapeType_) â The shape of the buffer

  * **dtype** (_tilelang._typing.DType_) â The data type of the buffer (default: float32)

  * **strides** (_tuple_ _[__tvm.tir.PrimExpr_ _,__Ellipsis_ _]__|__None_)



Returns:
    

A buffer created from the given parameters

Return type:
    

tvm.tir.Buffer

_class _tilelang.language.proxy.TensorProxyÂ¶
    

Bases: `BaseTensorProxy`

Main tensor proxy class for global scope buffers.

This class implements the default tensor proxy with global memory scope, the tensor should be by default contiguous.

__call__(_shape_ , _dtype ='float32'_, _data =None_, _scope =None_)Â¶
    

Parameters:
    

  * **shape** (_tilelang._typing.ShapeType_ _|__tvm.tir.PrimExpr_ _|__int_)

  * **dtype** (_tilelang._typing.DType_)



Return type:
    

tvm.tir.Buffer

_class _tilelang.language.proxy.StridedTensorProxyÂ¶
    

Bases: `BaseTensorProxy`

Main tensor proxy class for global scope buffers, with strides supported.

This class implements the default tensor proxy with global memory scope, with the stride information required.

__call__(_shape_ , _strides_ , _dtype ='float32'_, _scope =None_)Â¶
    

Parameters:
    

  * **shape** (_tilelang._typing.ShapeType_)

  * **strides** (_tuple_ _[__Any_ _]_)

  * **dtype** (_tilelang._typing.DType_)



Return type:
    

tvm.tir.Buffer

_class _tilelang.language.proxy.FragmentBufferProxyÂ¶
    

Bases: `BaseTensorProxy`

Proxy class for fragment memory buffers.

This class represents tensor proxies specifically for local fragment memory, typically used in GPU tensor core operations.

default_scope _ = 'local.fragment'_Â¶
    

_class _tilelang.language.proxy.SharedBufferProxyÂ¶
    

Bases: `BaseTensorProxy`

Proxy class for shared memory buffers.

This class represents tensor proxies for dynamic shared memory, commonly used in GPU shared memory operations.

default_scope _ = 'shared.dyn'_Â¶
    

_class _tilelang.language.proxy.LocalBufferProxyÂ¶
    

Bases: `BaseTensorProxy`

Proxy class for local memory buffers.

This class represents tensor proxies for local memory scope, typically used for temporary computations in GPU kernels.

default_scope _ = 'local'_Â¶
    

tilelang.language.proxy.BufferÂ¶
    

_class _tilelang.language.proxy.BaseTensor(_shape_ , _dtype ='float32'_, _data =None_, _strides =None_, _elem_offset =None_, _scope =None_, _align =None_, _offset_factor =None_, _buffer_type =''_, _axis_separators =None_)Â¶
    

Parameters:
    

  * **shape** (_tilelang._typing.ShapeType_)

  * **dtype** (_tilelang._typing.DType_)




_classmethod ___class_getitem__(_key_)Â¶
    

__getitem__(_key_)Â¶
    

Return type:
    

Any

__setitem__(_key_ , _value_)Â¶
    

Return type:
    

None

_classmethod _from_ptr(_pointer_var_ , _shape_ , _dtype ='float32'_, _strides =None_)Â¶
    

Parameters:
    

  * **pointer_var** (_tvm.tir.Var_)

  * **shape** (_tilelang._typing.ShapeType_)

  * **dtype** (_tilelang._typing.DType_)

  * **strides** (_tuple_ _[__tvm.tir.PrimExpr_ _,__Ellipsis_ _]__|__None_)



Return type:
    

typing_extensions.Self

tilelang.language.proxy.ptr(_dtype =None_, _storage_scope ='global'_, _*_ , _is_size_var =False_)Â¶
    

Create a TIR var that represents a pointer.

Parameters:
    

  * **dtype** (_DType_) â The data type of the pointer.

  * **storage_scope** (_str_) â The storage scope of the pointer.

  * **is_size_var** ([_bool_](../dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool")) â Whether or not to return a SizeVar instead of Var.



Returns:
    

**res** â The new tir.Var with type handle or casted expression with type handle.

Return type:
    

PrimExpr

tilelang.language.proxy.make_tensor(_ptr_ , _shape_ , _dtype ='float32'_, _strides =None_)Â¶
    

Parameters:
    

  * **ptr** (_tvm.tir.Var_)

  * **shape** (_tilelang._typing.ShapeType_)

  * **dtype** (_tilelang._typing.DType_)

  * **strides** (_tuple_ _[__tvm.tir.PrimExpr_ _,__Ellipsis_ _]__|__None_)



Return type:
    

tvm.tir.Buffer
