# tilelang.language.customizeÂ¶

Some customized operations frequently used in tensor programming, exposed on the TileLang language surface.

## FunctionsÂ¶

`dp4a`(A, B, C) | Perform a 4-element dot product with accumulation (DP4A).  
---|---  
`clamp`(dst, min_val, max_val) | Clamps the input value dst between [min_val, max_val]  
`reshape`(src, shape) | Reshapes the input buffer to the specified shape.  
`view`(src[, shape, dtype]) | Return a Tensor view of the input buffer with an optional new shape and dtype.  
`loop_break`() | Break out of the current loop.  
  
## Module ContentsÂ¶

tilelang.language.customize.dp4a(_A_ , _B_ , _C_)Â¶
    

Perform a 4-element dot product with accumulation (DP4A).

Parameters:
    

  * **A** (_Buffer_) â First input buffer

  * **B** (_Buffer_) â Second input buffer

  * **C** (_Buffer_) â Accumulation buffer



Returns:
    

Handle to the DP4A operation

Return type:
    

PrimExpr

tilelang.language.customize.clamp(_dst_ , _min_val_ , _max_val_)Â¶
    

Clamps the input value dst between [min_val, max_val]

Parameters:
    

  * **dst** (_tvm.tir.PrimExpr_) â Input value to be clamped

  * **min_val** (_tvm.tir.PrimExpr_) â Minimum value

  * **max_val** (_tvm.tir.PrimExpr_) â Maximum value



Returns:
    

Value clamped to the specified range

Return type:
    

tvm.tir.PrimExpr

tilelang.language.customize.reshape(_src_ , _shape_)Â¶
    

Reshapes the input buffer to the specified shape.

Parameters:
    

  * **src** (_Buffer_) â Input buffer to be reshaped

  * **shape** (_ShapeType_) â New shape for the buffer



Returns:
    

A new buffer view with the specified shape

Return type:
    

Buffer

tilelang.language.customize.view(_src_ , _shape =None_, _dtype =None_)Â¶
    

Return a Tensor view of the input buffer with an optional new shape and dtype.

If shape is None the source bufferâs shape is used; if dtype is None the source bufferâs dtype is used. The returned buffer shares the same underlying data as src (no copy).

Parameters:
    

  * **src** (_tvm.tir.Buffer_)

  * **shape** (_tilelang._typing.ShapeType_ _|__None_)

  * **dtype** (_tilelang._typing.DType_ _|__None_)



Return type:
    

tvm.tir.Buffer

tilelang.language.customize.loop_break()Â¶
    

Break out of the current loop.

Returns:
    

A call to the tl.loop_break intrinsic.

Return type:
    

tir.Call
