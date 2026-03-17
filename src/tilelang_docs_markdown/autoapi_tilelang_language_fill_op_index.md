# tilelang.language.fill_opÂ¶

Fill operations exposed on the TileLang language surface.

## FunctionsÂ¶

`fill`(buffer, value) | Fill a buffer or buffer region with a specified value.  
---|---  
`clear`(buffer) | Clear a buffer by filling it with zeros.  
  
## Module ContentsÂ¶

tilelang.language.fill_op.fill(_buffer_ , _value_)Â¶
    

Fill a buffer or buffer region with a specified value.

Parameters:
    

  * **buffer** (_tilelang._typing.BufferLikeType_) â Either a TVM buffer or buffer region to be filled

  * **value** (_tvm.tir.PrimExpr_) â The value to fill the buffer with



Returns:
    

A TVM intrinsic call that performs the fill operation

Return type:
    

tvm.tir.PrimExpr

tilelang.language.fill_op.clear(_buffer_)Â¶
    

Clear a buffer by filling it with zeros.

Parameters:
    

**buffer** (_tilelang._typing.BufferLikeType_) â Either a TVM buffer or a variable that contains a buffer region

Returns:
    

A fill operation that sets the buffer contents to zero

Raises:
    

**ValueError** â If the buffer variable contains an invalid buffer region

Return type:
    

tvm.tir.PrimExpr
