# tilelang.utils.languageÂ¶

## FunctionsÂ¶

`is_global`(buffer) | Check if the buffer is in the global memory scope.  
---|---  
`is_shared`(buffer[, allow_dynamic]) | Check if the buffer is in the shared memory scope.  
`is_shared_dynamic`(buffer) | Check if the buffer is in the dynamic shared memory scope.  
`is_tensor_memory`(buffer) | Check if the buffer is in tensor memory scope (e.g., shared.tmem).  
`is_local`(buffer) | Check if the buffer is in the local memory scope.  
`is_fragment`(buffer) | Check if the buffer is a fragment (e.g., for matrix multiplication operations).  
`is_local_var`(buffer) | Check if the buffer is in the local.var memory scope.  
`get_buffer_elems`(buffer) | Get the number of elements in the buffer.  
`array_reduce`(array) | Reduce an array of integers to a single integer.  
`retrieve_func_from_module`(ir_module) | Retrieve the single PrimFunc from an IRModule.  
`to_buffer_region`(obj[, access_type, extents]) | Convert to/from the tl.region representation.  
`retrieve_shape`(obj) | Retrieve shape-like extents for a buffer-like object.  
`retrieve_stride`(obj) | Retrieve row-major strides for a buffer-like object based on its buffer.shape.  
`retrive_ptr_from_buffer_region`(buffer_or_load_or_region) |   
`retrieve_ptr`(obj[, access_type, ignore_last_ndim]) | Retrieve a pointer to the start of a (possibly sliced) buffer region.  
`retrieve_offset`(obj) | Retrieve per-dimension minima offsets.  
`retrieve_dtype`(obj) | Retrieve the dtype of a buffer-like object.  
`bits_product`(shape, dtype) | Compute the number of bits in a Buffer (shape with dtype).  
`prim_expr_equal`(lhs, rhs) | Robust equality for PrimExpr shapes/extents.  
`legalize_pairwise_extents`(src_extents, dst_extents) | Right-align and broadcast two extent lists to be mutually compatible.  
`is_full_region`(buffer_region) | Check whether a BufferRegion covers the full buffer region.  
`get_prim_func_name`(func[, default]) | Extract a humanâreadable function name from a TVM PrimFunc.  
`side_effect`(expr) |   
  
## Module ContentsÂ¶

tilelang.utils.language.is_global(_buffer_)Â¶
    

Check if the buffer is in the global memory scope.

Parameters:
    

**buffer** (_tilelang._typing.BufferLikeType_) â The TVM buffer, BufferLoad, or BufferRegion to check.

Returns:
    

True if the buffer is in global memory, False otherwise.

Return type:
    

[bool](../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool")

tilelang.utils.language.is_shared(_buffer_ , _allow_dynamic =True_)Â¶
    

Check if the buffer is in the shared memory scope.

Parameters:
    

  * **buffer** (_tilelang._typing.BufferLikeType_) â The TVM buffer, BufferLoad, or BufferRegion to check.

  * **allow_dynamic** ([_bool_](../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool"))



Returns:
    

True if the buffer is in shared memory, False otherwise.

Return type:
    

[bool](../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool")

tilelang.utils.language.is_shared_dynamic(_buffer_)Â¶
    

Check if the buffer is in the dynamic shared memory scope.

Parameters:
    

**buffer** (_tilelang._typing.BufferLikeType_) â The TVM buffer, BufferLoad, or BufferRegion to check.

Returns:
    

True if the buffer is in dynamic shared memory, False otherwise.

Return type:
    

[bool](../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool")

tilelang.utils.language.is_tensor_memory(_buffer_)Â¶
    

Check if the buffer is in tensor memory scope (e.g., shared.tmem).

Parameters:
    

**buffer** (_tilelang._typing.BufferLikeType_) â The TVM buffer, BufferLoad, or BufferRegion to check.

Returns:
    

True if the buffer is in tensor memory, False otherwise.

Return type:
    

[bool](../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool")

tilelang.utils.language.is_local(_buffer_)Â¶
    

Check if the buffer is in the local memory scope.

Parameters:
    

**buffer** (_tilelang._typing.BufferLikeType_) â The TVM buffer, BufferLoad, or BufferRegion to check.

Returns:
    

True if the buffer is in local memory, False otherwise.

Return type:
    

[bool](../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool")

tilelang.utils.language.is_fragment(_buffer_)Â¶
    

Check if the buffer is a fragment (e.g., for matrix multiplication operations).

Parameters:
    

**buffer** (_tilelang._typing.BufferLikeType_) â The TVM buffer, BufferLoad, or BufferRegion to check.

Returns:
    

True if the buffer is a fragment, False otherwise.

Return type:
    

[bool](../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool")

tilelang.utils.language.is_local_var(_buffer_)Â¶
    

Check if the buffer is in the local.var memory scope.

Parameters:
    

**buffer** (_tilelang._typing.BufferLikeType_) â The TVM buffer, BufferLoad, or BufferRegion to check.

Returns:
    

True if the buffer is in local.var memory, False otherwise.

Return type:
    

[bool](../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool")

tilelang.utils.language.get_buffer_elems(_buffer_)Â¶
    

Get the number of elements in the buffer.

Parameters:
    

**buffer** (_tvm.tir.Buffer_)

Return type:
    

int

tilelang.utils.language.array_reduce(_array_)Â¶
    

Reduce an array of integers to a single integer.

Parameters:
    

**array** (_List_ _[__int_ _]_) â The array of integers to reduce.

Returns:
    

The reduced integer.

Return type:
    

int

tilelang.utils.language.retrieve_func_from_module(_ir_module_)Â¶
    

Retrieve the single PrimFunc from an IRModule.

Parameters:
    

**ir_module** (_IRModule_) â The TVM IRModule to extract the function from. The module should contain exactly one global function.

Returns:
    

The single function contained in the module.

Return type:
    

[PrimFunc](../../language/eager/builder/index.html#tilelang.language.eager.builder.PrimFunc "tilelang.language.eager.builder.PrimFunc")

Raises:
    

  * **ValueError** â If ir_module is not an IRModule.

  * **AssertionError** â If the module contains more than one global function.




tilelang.utils.language.to_buffer_region(_obj_ , _access_type ='rw'_, _extents =None_)Â¶
    

Convert to/from the tl.region representation.

  * Buffer/BufferLoad/BufferRegion -> returns a tl.region call (PrimExpr)

  * tl.region Call -> returns the decoded BufferRegion for analysis




Parameters:
    

  * **obj** (_tilelang._typing.BufferLikeType_)

  * **access_type** (_str_)

  * **extents** (_list_ _[__tvm.tir.PrimExpr_ _]__|__None_)



Return type:
    

tvm.tir.PrimExpr | tvm.tir.BufferRegion

tilelang.utils.language.retrieve_shape(_obj_)Â¶
    

Retrieve shape-like extents for a buffer-like object.

  * Buffer -> its shape

  * BufferRegion -> list of each rangeâs extent

  * BufferLoad -> extents from get_buffer_region_from_load(obj)




Parameters:
    

**obj** (_tilelang._typing.BufferLikeType_)

Return type:
    

list

tilelang.utils.language.retrieve_stride(_obj_)Â¶
    

Retrieve row-major strides for a buffer-like object based on its buffer.shape.

For BufferRegion and BufferLoad, uses the underlying bufferâs shape.

Parameters:
    

**obj** (_tilelang._typing.BufferLikeType_)

Return type:
    

list

tilelang.utils.language.retrive_ptr_from_buffer_region(_buffer_or_load_or_region_ , _access_type ='r'_)Â¶
    

Parameters:
    

  * **buffer_or_load_or_region** (_tilelang._typing.BufferLikeType_)

  * **access_type** (_str_)



Return type:
    

tvm.tir.PrimExpr

tilelang.utils.language.retrieve_ptr(_obj_ , _access_type ='r'_, _ignore_last_ndim =0_)Â¶
    

Retrieve a pointer to the start of a (possibly sliced) buffer region.

  * Buffer -> base pointer

  * BufferRegion -> pointer with byte offset computed from region minima

  * BufferLoad -> pointer offset computed from indices or derived region




Parameters:
    

  * **obj** (_tilelang._typing.BufferLikeType_) â Buffer-like object

  * **access_type** (_str_) â TVM Buffer access mask, e.g. ârâ, âwâ, ârwâ

  * **ignore_last_ndim** (_int_) â do not offset the last N dimensions



Return type:
    

tvm.tir.PrimExpr

tilelang.utils.language.retrieve_offset(_obj_)Â¶
    

Retrieve per-dimension minima offsets.

  * Buffer -> [0, 0, â¦]

  * BufferRegion -> [r.min for r in region]

  * BufferLoad -> indices (or derived region minima)




Parameters:
    

**obj** (_tilelang._typing.BufferLikeType_)

Return type:
    

list

tilelang.utils.language.retrieve_dtype(_obj_)Â¶
    

Retrieve the dtype of a buffer-like object.

  * Buffer -> buffer.dtype

  * BufferRegion -> convert to BufferLoad with Ramp indices, then use load.dtype

  * BufferLoad -> load.dtype




Parameters:
    

**obj** (_tilelang._typing.BufferLikeType_)

Return type:
    

str

tilelang.utils.language.bits_product(_shape_ , _dtype_)Â¶
    

Compute the number of bits in a Buffer (shape with dtype).

Parameters:
    

  * **shape** (_list_ _[__tvm.tir.PrimExpr_ _]_)

  * **dtype** (_str_)



Return type:
    

tvm.tir.PrimExpr

tilelang.utils.language.prim_expr_equal(_lhs_ , _rhs_)Â¶
    

Robust equality for PrimExpr shapes/extents.

Tries structural_equal first, then falls back to expr_deep_equal. Python ints are converted to IntImm for comparison.

Return type:
    

[bool](../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool")

tilelang.utils.language.legalize_pairwise_extents(_src_extents_ , _dst_extents_)Â¶
    

Right-align and broadcast two extent lists to be mutually compatible.

Early-exit rule: \- If the number of non-1 dimensions in src_extents equals that in dst_extents,

> no adjustment is made; the original extents are returned unchanged. This preserves the per-dimension iteration mapping (one loop var per non-1 dim) and avoids creating extra varying axes on either side.

Otherwise, for each pair of tail-aligned dimensions (x, y):
    

  * if x == y: keep both

  * elif x == 1: set x = y

  * elif y == 1: set y = x

  * else: promote both to tir.max(x, y) to handle dynamic-vs-static safely




Leading unmatched dimensions are kept as-is.

Returns a tuple of new lists (src_new, dst_new).

Parameters:
    

  * **src_extents** (_list_)

  * **dst_extents** (_list_)



Return type:
    

tuple[list, list]

tilelang.utils.language.is_full_region(_buffer_region_)Â¶
    

Check whether a BufferRegion covers the full buffer region.

A full region means each dimension has start 0 and extent equal to the corresponding dimension in the bufferâs shape.

Parameters:
    

**buffer_region** (_tvm.tir.BufferRegion_) â The TVM BufferRegion to check.

Returns:
    

True if the region is full; otherwise False.

Return type:
    

[bool](../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool")

tilelang.utils.language.get_prim_func_name(_func_ , _default =None_)Â¶
    

Extract a humanâreadable function name from a TVM PrimFunc.

Prefer the global_symbol attribute set on the PrimFunc. If it is missing (e.g., private PrimFunc without a global symbol), return the provided default value.

Parameters:
    

  * **func** (_tvm.tir.PrimFunc_ _|__None_) â TVM PrimFunc instance or None.

  * **default** (_str_ _|__None_) â Fallback name to return when no name can be determined.



Returns:
    

The function name as a string, or default when unavailable.

Return type:
    

str | None

tilelang.utils.language.side_effect(_expr_)Â¶
    

Parameters:
    

**expr** (_tvm.tir.PrimExpr_)

Return type:
    

tvm.tir.expr.CallEffectKind
