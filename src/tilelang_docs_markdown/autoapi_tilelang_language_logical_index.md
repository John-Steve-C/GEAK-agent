# tilelang.language.logicalÂ¶

Logical operations exposed on the TileLang language surface.

## FunctionsÂ¶

`any_of`(buffer) | Check if any element in the buffer is true.  
---|---  
`all_of`(buffer) | Check if all elements in the buffer are true.  
  
## Module ContentsÂ¶

tilelang.language.logical.any_of(_buffer_)Â¶
    

Check if any element in the buffer is true.

Parameters:
    

**buffer** (_tilelang._typing.BufferLikeType_) â Either a TVM buffer or buffer region to be checked

Returns:
    

A TVM intrinsic call that performs the any operation

Return type:
    

tvm.tir.PrimExpr

tilelang.language.logical.all_of(_buffer_)Â¶
    

Check if all elements in the buffer are true.

Parameters:
    

**buffer** (_tilelang._typing.BufferLikeType_) â Either a TVM buffer or buffer region to be checked

Returns:
    

A TVM intrinsic call that performs the any operation

Return type:
    

tvm.tir.PrimExpr
