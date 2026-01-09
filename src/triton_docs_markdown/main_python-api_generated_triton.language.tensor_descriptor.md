# triton.language.tensor_descriptor¶

_class _triton.language.tensor_descriptor(_self_ , _handle_ , _shape : List[[tensor](triton.language.tensor.html#triton.language.tensor "triton.language.core.tensor")]_, _strides : List[[tensor](triton.language.tensor.html#triton.language.tensor "triton.language.core.tensor")]_, _block_type : block_type_)¶
    

A descriptor representing a tensor in global memory.

__init__(_self_ , _handle_ , _shape : List[[tensor](triton.language.tensor.html#triton.language.tensor "triton.language.core.tensor")]_, _strides : List[[tensor](triton.language.tensor.html#triton.language.tensor "triton.language.core.tensor")]_, _block_type : block_type_)¶
    

Not called by user code.

Methods

`__init__`(self, handle, shape, strides, ...) | Not called by user code.  
---|---  
`atomic_add`(self, offsets, value[, _semantic]) |   
`atomic_and`(self, offsets, value[, _semantic]) |   
`atomic_max`(self, offsets, value[, _semantic]) |   
`atomic_min`(self, offsets, value[, _semantic]) |   
`atomic_or`(self, offsets, value[, _semantic]) |   
`atomic_xor`(self, offsets, value[, _semantic]) |   
`gather`(self, *args[, _semantic]) | Gather multiple descriptors worth of data  
`load`(self, offsets[, _semantic]) | Load a block from the descriptor starting at the given element offsets.  
`scatter`(self, value, *args[, _semantic]) | Scatter multiple descriptors worth of data  
`store`(self, offsets, value[, _semantic]) | Store a block from the descriptor starting at the given element offsets.  
  
Attributes

`block_shape` |   
---|---  
`block_type` |   
`dtype` |   
`type` | 
