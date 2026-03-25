# tilelang.contrib.cutedsl.utilsÂ¶

Utility functions for CuTeDSL backend.

Provides common helpers used across the CuTeDSL codegen: bitcast, tensor construction, warp election, barrier sync, and FP16 packing.

## AttributesÂ¶

`BYTES_PER_TENSORMAP` |   
---|---  
`BYTES_PER_POINTER` |   
`type_map` |   
  
## FunctionsÂ¶

`bitcast`(value, target_dtype) | Reinterpret the bits of a value as a different type.  
---|---  
`make_filled_tensor`(shape, value) |   
`make_tensor_at_offset`(ptr, offset, shape[, div_by]) |   
`shuffle_elect`(thread_extent) |   
`sync_thread_partial`([barrier_id, thread_count]) |   
`pack_half2`(x, y) | Pack two half-precision (fp16) values into a single 32-bit value.  
  
## Module ContentsÂ¶

tilelang.contrib.cutedsl.utils.BYTES_PER_TENSORMAP _ = 128_Â¶
    

tilelang.contrib.cutedsl.utils.BYTES_PER_POINTER _ = 8_Â¶
    

tilelang.contrib.cutedsl.utils.type_mapÂ¶
    

tilelang.contrib.cutedsl.utils.bitcast(_value_ , _target_dtype_)Â¶
    

Reinterpret the bits of a value as a different type. Equivalent to Câs (*(target_type *)(&value)).

Parameters:
    

  * **value** â Source value (Numeric type from CuTeDSL)

  * **target_dtype** â Target type (CuTeDSL type like Int8, Float16, etc.)



Returns:
    

Value reinterpreted as target type

tilelang.contrib.cutedsl.utils.make_filled_tensor(_shape_ , _value_)Â¶
    

tilelang.contrib.cutedsl.utils.make_tensor_at_offset(_ptr_ , _offset_ , _shape_ , _div_by =1_)Â¶
    

Parameters:
    

**ptr** (_cutlass.cute.Pointer_)

tilelang.contrib.cutedsl.utils.shuffle_elect(_thread_extent_)Â¶
    

tilelang.contrib.cutedsl.utils.sync_thread_partial(_barrier_id =None_, _thread_count =None_)Â¶
    

tilelang.contrib.cutedsl.utils.pack_half2(_x_ , _y_)Â¶
    

Pack two half-precision (fp16) values into a single 32-bit value. Corresponds to CUDAâs __pack_half2 intrinsic.

This packs two fp16 values into a single int32 by treating the fp16 bits as raw data and concatenating them.
