# tilelang.contrib.dlpackÂ¶

Wrapping functions to bridge frameworks with DLPack support to TVM

## FunctionsÂ¶

`convert_func`(tvm_func, tensor_type, to_dlpack_func) | Convert a tvm function into one that accepts a tensor from another  
---|---  
  
## Module ContentsÂ¶

tilelang.contrib.dlpack.convert_func(_tvm_func_ , _tensor_type_ , _to_dlpack_func_)Â¶
    

Convert a tvm function into one that accepts a tensor from another
    

framework, provided the other framework supports DLPACK

Parameters:
    

  * **tvm_func** (_Function_) â Built tvm function operating on arrays

  * **tensor_type** (_Type_) â Type of the tensors of the target framework

  * **to_dlpack_func** (_Function_) â Function to convert the source tensors to DLPACK



