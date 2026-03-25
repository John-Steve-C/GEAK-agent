# tilelang.language.reduce_opÂ¶

Reduce operations exposed on the TileLang language surface.

## AttributesÂ¶

`ReduceKind` |   
---|---  
  
## FunctionsÂ¶

`reduce`(buffer, out, reduce_type, dim, clear) | Perform a reduction operation on a buffer along a specified dimension.  
---|---  
`reduce_max`(buffer, out[, dim, clear]) | Perform reduce max on input buffer, store the result to output buffer  
`reduce_min`(buffer, out[, dim, clear]) | Perform reduce min on input buffer, store the result to output buffer.  
`reduce_sum`(buffer, out[, dim, clear]) | Perform reduce sum on input buffer, store the result to output buffer.  
`reduce_abssum`(buffer, out[, dim]) | Perform reduce absolute sum on input buffer, store the result to output buffer.  
`reduce_absmax`(buffer, out[, dim, clear]) | Perform reduce absolute max on input buffer, store the result to output buffer.  
`reduce_bitand`(buffer, out[, dim, clear]) | Perform reduce bitwise-and on input buffer, store the result to output buffer.  
`reduce_bitor`(buffer, out[, dim, clear]) | Perform reduce bitwise-or on input buffer, store the result to output buffer.  
`reduce_bitxor`(buffer, out[, dim, clear]) | Perform reduce bitwise-xor on input buffer, store the result to output buffer.  
`cumsum_fragment`(src, dst, dim, reverse) | Compute cumulative sum for fragment buffers by copying to shared memory first.  
`cumsum`(src[, dst, dim, reverse]) | Compute the cumulative sum of src along dim, writing results to dst.  
`finalize_reducer`(reducer) | Finalize a reducer buffer by emitting the tl.tileop.finalize_reducer intrinsic.  
`warp_reduce_sum`(value) | Perform warp reduction sum on a register value.  
`warp_reduce_max`(value) | Perform warp reduction max on a register value.  
`warp_reduce_min`(value) | Perform warp reduction min on a register value.  
`warp_reduce_bitand`(value) | Perform warp reduction bitwise-and on a register value.  
`warp_reduce_bitor`(value) | Perform warp reduction bitwise-or on a register value.  
  
## Module ContentsÂ¶

tilelang.language.reduce_op.ReduceKindÂ¶
    

tilelang.language.reduce_op.reduce(_buffer_ , _out_ , _reduce_type_ , _dim_ , _clear_)Â¶
    

Perform a reduction operation on a buffer along a specified dimension.

Parameters:
    

  * **buffer** (_tir.Buffer_) â Input buffer to reduce

  * **out** (_tir.Buffer_) â Output buffer to store results

  * **reduce_type** (_str_) â Type of reduction (âmaxâ, âminâ, âsumâ, âabssumâ)

  * **dim** (_int_) â Dimension along which to perform reduction

  * **clear** ([_bool_](../dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool")) â Whether to initialize the output buffer before reduction



Return type:
    

None

tilelang.language.reduce_op.reduce_max(_buffer_ , _out_ , _dim =-1_, _clear =True_)Â¶
    

Perform reduce max on input buffer, store the result to output buffer

Parameters:
    

  * **buffer** (_Buffer_) â The input buffer.

  * **out** (_Buffer_) â The output buffer.

  * **dim** (_int_) â The dimension to perform reduce on

  * **clear** ([_bool_](../dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool")) â If set to True, the output buffer will first be initialized to -inf.



Returns:
    

**handle**

Return type:
    

PrimExpr

tilelang.language.reduce_op.reduce_min(_buffer_ , _out_ , _dim =-1_, _clear =True_)Â¶
    

Perform reduce min on input buffer, store the result to output buffer.

Parameters:
    

  * **buffer** (_tir.Buffer_) â The input buffer

  * **out** (_tir.Buffer_) â The output buffer

  * **dim** (_int_) â The dimension to perform reduce on

  * **clear** ([_bool_](../dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool") _,__optional_) â If True, output buffer will be initialized to inf. Defaults to True.



Returns:
    

Handle to the reduction operation

Return type:
    

tir.Call

tilelang.language.reduce_op.reduce_sum(_buffer_ , _out_ , _dim =-1_, _clear =True_)Â¶
    

Perform reduce sum on input buffer, store the result to output buffer.

Parameters:
    

  * **buffer** (_tir.Buffer_) â The input buffer

  * **out** (_tir.Buffer_) â The output buffer

  * **dim** (_int_) â The dimension to perform reduce on

  * **clear** ([_bool_](../dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool") _,__optional_) â If True, output buffer will be cleared before reduction. If False, results will be accumulated on existing values. Defaults to True.



Return type:
    

None

Note: When clear=True, reduce_sum will not compute directly on the output buffer. This is because
    

> during warp reduction, the same value would be accumulated multiple times (number of threads in the warp). Therefore, the implementation with clear=True follows these steps:

  1. create a temp buffer with same shape and dtype as out

  2. copy out to temp buffer

  3. call reduce_sum with temp buffer and out

  4. Add temp buffer to out




Returns:
    

Handle to the reduction operation

Return type:
    

tir.Call

Parameters:
    

  * **buffer** (_tvm.tir.Buffer_)

  * **out** (_tvm.tir.Buffer_)

  * **dim** (_int_)

  * **clear** ([_bool_](../dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool"))




tilelang.language.reduce_op.reduce_abssum(_buffer_ , _out_ , _dim =-1_)Â¶
    

Perform reduce absolute sum on input buffer, store the result to output buffer.

Parameters:
    

  * **buffer** (_tir.Buffer_) â The input buffer

  * **out** (_tir.Buffer_) â The output buffer

  * **dim** (_int_) â The dimension to perform reduce on



Returns:
    

Handle to the reduction operation

Return type:
    

tir.Call

tilelang.language.reduce_op.reduce_absmax(_buffer_ , _out_ , _dim =-1_, _clear =True_)Â¶
    

Perform reduce absolute max on input buffer, store the result to output buffer.

Parameters:
    

  * **buffer** (_tir.Buffer_) â The input buffer

  * **out** (_tir.Buffer_) â The output buffer

  * **dim** (_int_) â The dimension to perform reduce on

  * **clear** ([_bool_](../dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool"))



Returns:
    

Handle to the reduction operation

Return type:
    

tir.Call

tilelang.language.reduce_op.reduce_bitand(_buffer_ , _out_ , _dim =-1_, _clear =True_)Â¶
    

Perform reduce bitwise-and on input buffer, store the result to output buffer.

Parameters:
    

  * **buffer** (_tir.Buffer_) â The input buffer

  * **out** (_tir.Buffer_) â The output buffer

  * **dim** (_int_) â The dimension to perform reduce on

  * **clear** ([_bool_](../dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool"))



Returns:
    

Handle to the reduction operation

Return type:
    

tir.Call

tilelang.language.reduce_op.reduce_bitor(_buffer_ , _out_ , _dim =-1_, _clear =True_)Â¶
    

Perform reduce bitwise-or on input buffer, store the result to output buffer.

Parameters:
    

  * **buffer** (_tir.Buffer_) â The input buffer

  * **out** (_tir.Buffer_) â The output buffer

  * **dim** (_int_) â The dimension to perform reduce on

  * **clear** ([_bool_](../dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool"))



Returns:
    

Handle to the reduction operation

Return type:
    

tir.Call

tilelang.language.reduce_op.reduce_bitxor(_buffer_ , _out_ , _dim =-1_, _clear =True_)Â¶
    

Perform reduce bitwise-xor on input buffer, store the result to output buffer.

Parameters:
    

  * **buffer** (_tir.Buffer_) â The input buffer

  * **out** (_tir.Buffer_) â The output buffer

  * **dim** (_int_) â The dimension to perform reduce on

  * **clear** ([_bool_](../dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool"))



Returns:
    

Handle to the reduction operation

Return type:
    

tir.Call

tilelang.language.reduce_op.cumsum_fragment(_src_ , _dst_ , _dim_ , _reverse_)Â¶
    

Compute cumulative sum for fragment buffers by copying to shared memory first.

This macro handles cumulative sum operations on fragment buffers by first copying the data to shared memory, performing the cumsum operation, and then copying back.

Parameters:
    

  * **src** (_tilelang._typing.BufferLikeType_) â Source buffer (Buffer, BufferRegion, or BufferLoad) containing input data.

  * **dst** (_tilelang._typing.BufferLikeType_) â Destination buffer (Buffer, BufferRegion, or BufferLoad) for output data.

  * **dim** (_int_) â Dimension along which to compute cumulative sum.

  * **reverse** ([_bool_](../dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool")) â If True, compute cumulative sum in reverse order.



Return type:
    

None

tilelang.language.reduce_op.cumsum(_src_ , _dst =None_, _dim =0_, _reverse =False_)Â¶
    

Compute the cumulative sum of src along dim, writing results to dst.

Negative dim indices are normalized (Python-style). If dst is None, the operation is performed in-place into src. Raises ValueError when dim is out of bounds for src.shape. When src.scope() == âlocal.fragmentâ, this delegates to cumsum_fragment; otherwise it emits the tl.cumsum intrinsic.

Supports Buffer, BufferRegion, and BufferLoad inputs, allowing operations on buffer slices/regions.

Examples

A 1D inclusive scan that writes the result into a separate shared-memory buffer:
    
    
    >>> import tilelang.language as T
    >>> @T.prim_func
    ... def kernel(A: T.Tensor((128,), "float32"), B: T.Tensor((128,), "float32")):
    ...     with T.Kernel(1, threads=128):
    ...         A_shared = T.alloc_shared((128,), "float32")
    ...         T.copy(A, A_shared)
    ...         T.cumsum(src=A_shared, dst=A_shared, dim=0)
    ...         T.copy(A_shared, B)
    

A 2D prefix sum along the last dimension with reverse accumulation:
    
    
    >>> import tilelang.language as T
    >>> @T.prim_func
    ... def kernel2d(A: T.Tensor((64, 64), "float16"), B: T.Tensor((64, 64), "float16")):
    ...     with T.Kernel(1, 1, threads=256):
    ...         tile = T.alloc_shared((64, 64), "float16")
    ...         T.copy(A, tile)
    ...         T.cumsum(src=tile, dim=1, reverse=True)
    ...         T.copy(tile, B)
    

Operating on a buffer region (slice):
    
    
    >>> import tilelang.language as T
    >>> @T.prim_func
    ... def kernel_region(InputG_fragment: T.Tensor((128,), "float32"), chunk_size: T.int32):
    ...     with T.Kernel(1, threads=128):
    ...         i = T.int32(0)
    ...         T.cumsum(InputG_fragment[i * chunk_size:(i + 1) * chunk_size], dim=0)
    

Returns:
    

A handle to the emitted cumulative-sum operation.

Return type:
    

tir.Call

Parameters:
    

  * **src** (_tilelang._typing.BufferLikeType_)

  * **dst** (_tilelang._typing.BufferLikeType_ _|__None_)

  * **dim** (_int_)

  * **reverse** ([_bool_](../dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool"))




tilelang.language.reduce_op.finalize_reducer(_reducer_)Â¶
    

Finalize a reducer buffer by emitting the tl.tileop.finalize_reducer intrinsic.

This returns a TVM tir.Call handle that finalizes the given reducer using its writable pointer. The call does not modify Python objects directly; it produces the low-level intrinsic call used by the IR.

Parameters:
    

**reducer** (_tir.Buffer_) â Reducer buffer whose writable pointer will be finalized.

Returns:
    

Handle to the finalize reducer intrinsic call.

Return type:
    

tir.Call

tilelang.language.reduce_op.warp_reduce_sum(_value_)Â¶
    

Perform warp reduction sum on a register value.

This function reduces a value across all threads in a warp using shuffle operations. Each thread provides a register value, and after the reduction, all threads will have the sum of all values across the warp.

Parameters:
    

**value** (_tir.PrimExpr_) â The input register value to reduce

Returns:
    

The reduced sum value (same on all threads in the warp)

Return type:
    

tir.PrimExpr

tilelang.language.reduce_op.warp_reduce_max(_value_)Â¶
    

Perform warp reduction max on a register value.

This function reduces a value across all threads in a warp using shuffle operations. Each thread provides a register value, and after the reduction, all threads will have the max of all values across the warp.

Parameters:
    

**value** (_tir.PrimExpr_) â The input register value to reduce

Returns:
    

The reduced max value (same on all threads in the warp)

Return type:
    

tir.PrimExpr

tilelang.language.reduce_op.warp_reduce_min(_value_)Â¶
    

Perform warp reduction min on a register value.

This function reduces a value across all threads in a warp using shuffle operations. Each thread provides a register value, and after the reduction, all threads will have the min of all values across the warp.

Parameters:
    

**value** (_tir.PrimExpr_) â The input register value to reduce

Returns:
    

The reduced min value (same on all threads in the warp)

Return type:
    

tir.PrimExpr

tilelang.language.reduce_op.warp_reduce_bitand(_value_)Â¶
    

Perform warp reduction bitwise-and on a register value.

This function reduces a value across all threads in a warp using shuffle operations. Each thread provides a register value, and after the reduction, all threads will have the bitwise-and of all values across the warp.

Parameters:
    

**value** (_tir.PrimExpr_) â The input register value to reduce

Returns:
    

The reduced bitwise-and value (same on all threads in the warp)

Return type:
    

tir.PrimExpr

tilelang.language.reduce_op.warp_reduce_bitor(_value_)Â¶
    

Perform warp reduction bitwise-or on a register value.

This function reduces a value across all threads in a warp using shuffle operations. Each thread provides a register value, and after the reduction, all threads will have the bitwise-or of all values across the warp.

Parameters:
    

**value** (_tir.PrimExpr_) â The input register value to reduce

Returns:
    

The reduced bitwise-or value (same on all threads in the warp)

Return type:
    

tir.PrimExpr
