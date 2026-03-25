# tilelang.language.atomicÂ¶

Atomic operations exposed on the TileLang language surface.

## FunctionsÂ¶

`atomic_max`(dst, value[, memory_order, return_prev]) | Perform an atomic maximum on the value stored at dst with an optional memory-order.  
---|---  
`atomic_min`(dst, value[, memory_order, return_prev]) | Atomically update the value at dst to the minimum of its current value and value.  
`atomic_add`(dst, value[, memory_order, return_prev, ...]) | Atomically add value into dst, returning a handle to the operation.  
`atomic_addx2`(dst, value[, return_prev]) | Perform an atomic addition operation with double-width operands.  
`atomic_addx4`(dst, value[, return_prev]) | Perform an atomic addition operation with quad-width operands.  
`atomic_load`(src[, memory_order]) | Load a value from the given buffer using the specified atomic memory ordering.  
`atomic_store`(dst, src[, memory_order]) | Perform an atomic store of src into dst with the given memory ordering.  
  
## Module ContentsÂ¶

tilelang.language.atomic.atomic_max(_dst_ , _value_ , _memory_order =None_, _return_prev =False_)Â¶
    

Perform an atomic maximum on the value stored at dst with an optional memory-order.

Supports scalar/addressed extern atomic max when neither argument exposes extents, or tile-region-based atomic max for Buffer/BufferRegion/BufferLoad inputs. If both arguments are plain Buffers their shapes must be structurally equal. If at least one side exposes extents, extents are aligned (missing dimensions are treated as size 1); an assertion is raised if extents cannot be deduced. The optional memory_order (one of ârelaxedâ,âconsumeâ,âacquireâ,âreleaseâ,âacq_relâ,âseq_cstâ) is used only for the direct extern AtomicMax path when no extents are available â otherwise the tile-region path ignores memory_order.

Parameters:
    

  * **dst** (_Buffer_) â Destination buffer/address to apply the atomic max.

  * **value** (_PrimExpr_) â Value to compare/store atomically.

  * **memory_order** (_Optional_ _[__str_ _]_) â Optional memory-order name (e.g. ârelaxedâ, âacquireâ, âseq_cstâ). If provided, it is translated to the corresponding numeric memory-order id before the call.

  * **return_prev** ([_bool_](../dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool")) â If True, return the previous value; if False, return handle (default False).



Returns:
    

A handle/expression representing the issued atomic maximum operation, or the previous value if return_prev is True.

Return type:
    

PrimExpr

Examples
    
    
    >>> # Basic atomic max operation
    >>> counter = T.Tensor([1], "float32", name="counter")
    >>> atomic_max(counter, 42.0)
    
    
    
    >>> # With memory ordering
    >>> atomic_max(counter, 100.0, memory_order="acquire")
    
    
    
    >>> # Get the previous value
    >>> prev_value = atomic_max(counter, 50.0, return_prev=True)
    >>> # prev_value now contains the value that was in counter before the max operation
    
    
    
    >>> # Use in parallel reduction to find global maximum
    >>> @T.prim_func
    >>> def find_max(data: T.Buffer, result: T.Buffer):
    >>>     for i in T.thread_binding(128, "threadIdx.x"):
    >>>         atomic_max(result, data[i])
    
    
    
    >>> # Tensor-to-tensor atomic max (tile-region based)
    >>> src_tensor = T.Tensor([128, 64], "float32", name="src")
    >>> dst_tensor = T.Tensor([128, 64], "float32", name="dst")
    >>> atomic_max(dst_tensor, src_tensor)  # Max entire tensors atomically
    

tilelang.language.atomic.atomic_min(_dst_ , _value_ , _memory_order =None_, _return_prev =False_)Â¶
    

Atomically update the value at dst to the minimum of its current value and value.

Supports scalar/addressed extern atomic min when neither argument exposes extents, or tile-region-based atomic min for Buffer/BufferRegion/BufferLoad inputs. If both arguments are plain Buffers their shapes must be structurally equal. If at least one side exposes extents, extents are aligned (missing dimensions are treated as size 1); an assertion is raised if extents cannot be deduced. The optional memory_order (one of ârelaxedâ,âconsumeâ,âacquireâ,âreleaseâ,âacq_relâ,âseq_cstâ) is used only for the direct extern AtomicMin path when no extents are available â otherwise the tile-region path ignores memory_order.

Parameters:
    

  * **dst** (_Buffer_) â Destination buffer/address to apply the atomic min.

  * **value** (_PrimExpr_) â Value to compare/store atomically.

  * **memory_order** (_Optional_ _[__str_ _]_) â Optional memory-order name controlling the atomic operationâs ordering.

  * **return_prev** ([_bool_](../dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool")) â If True, return the previous value; if False, return handle (default False).



Returns:
    

A handle expression representing the atomic-min operation, or the previous value if return_prev is True.

Return type:
    

PrimExpr

Examples
    
    
    >>> # Basic atomic min operation
    >>> min_val = T.Tensor([1], "int32", name="min_val")
    >>> atomic_min(min_val, 10)
    
    
    
    >>> # Find minimum across threads
    >>> @T.prim_func
    >>> def find_min(data: T.Buffer, result: T.Buffer):
    >>>     for i in T.thread_binding(256, "threadIdx.x"):
    >>>         atomic_min(result, data[i])
    
    
    
    >>> # Track minimum with previous value
    >>> threshold = T.Tensor([1], "float32", name="threshold")
    >>> old_min = atomic_min(threshold, 3.14, return_prev=True)
    >>> # old_min contains the previous minimum value
    
    
    
    >>> # With relaxed memory ordering for performance
    >>> atomic_min(min_val, 5, memory_order="relaxed")
    
    
    
    >>> # Tensor-to-tensor atomic min (tile-region based)
    >>> src_tensor = T.Tensor([128, 64], "float32", name="src")
    >>> dst_tensor = T.Tensor([128, 64], "float32", name="dst")
    >>> atomic_min(dst_tensor, src_tensor)  # Min entire tensors atomically
    

tilelang.language.atomic.atomic_add(_dst_ , _value_ , _memory_order =None_, _return_prev =False_, _use_tma =False_)Â¶
    

Atomically add value into dst, returning a handle to the operation.

Supports scalar/addressed extern atomic add when neither argument exposes extents, or tile-region-based atomic add for Buffer/BufferRegion/BufferLoad inputs. If both arguments are plain Buffers their shapes must be structurally equal. If at least one side exposes extents, extents are aligned (missing dimensions are treated as size 1); an assertion is raised if extents cannot be deduced. The optional memory_order (one of ârelaxedâ,âconsumeâ,âacquireâ,âreleaseâ,âacq_relâ,âseq_cstâ) is used only for the direct extern AtomicAdd path when no extents are available â otherwise the tile-region path ignores memory_order.

Parameters:
    

  * **dst** (_Buffer_) â Destination buffer/address to apply the atomic add.

  * **value** (_PrimExpr_) â Value to add atomically.

  * **memory_order** (_Optional_ _[__str_ _]_) â Optional memory-order name controlling the atomic operationâs ordering.

  * **return_prev** ([_bool_](../dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool")) â If True, return the previous value; if False, return handle (default False).

  * **use_tma** ([_bool_](../dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool")) â If True, use TMA (cp.reduce) to perform the atomic add. This is available only for sm90+ (default False).



Returns:
    

A handle representing the atomic addition operation, or the previous value if return_prev is True.

Return type:
    

PrimExpr

Examples
    
    
    >>> # Basic atomic addition
    >>> counter = T.Tensor([1], "int32", name="counter")
    >>> atomic_add(counter, 1)  # Increment counter by 1
    
    
    
    >>> # Parallel sum reduction
    >>> @T.prim_func
    >>> def parallel_sum(data: T.Buffer, result: T.Buffer):
    >>>     for i in T.thread_binding(1024, "threadIdx.x"):
    >>>         atomic_add(result, data[i])
    
    
    
    >>> # Get previous value for debugging
    >>> old_value = atomic_add(counter, 5, return_prev=True)
    >>> # old_value contains the value before adding 5
    
    
    
    >>> # Tensor-to-tensor atomic add (tile-region based)
    >>> src_tensor = T.Tensor([128, 64], "float32", name="src")
    >>> dst_tensor = T.Tensor([128, 64], "float32", name="dst")
    >>> atomic_add(dst_tensor, src_tensor)  # Add entire tensors atomically
    
    
    
    >>> # With memory ordering for scalar operations
    >>> atomic_add(counter, 10, memory_order="acquire")
    
    
    
    >>> # Accumulate gradients in training
    >>> gradients = T.Tensor([1000], "float32", name="gradients")
    >>> global_grad = T.Tensor([1000], "float32", name="global_grad")
    >>> atomic_add(global_grad, gradients)
    

tilelang.language.atomic.atomic_addx2(_dst_ , _value_ , _return_prev =False_)Â¶
    

Perform an atomic addition operation with double-width operands.

Parameters:
    

  * **dst** (_Buffer_) â Destination buffer where the atomic addition will be performed

  * **value** (_PrimExpr_) â Value to be atomically added (double-width)

  * **return_prev** ([_bool_](../dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool")) â If True, return the previous value; if False, return handle (default False)



Returns:
    

Handle to the double-width atomic addition operation, or the previous value if return_prev is True

Return type:
    

PrimExpr

Examples
    
    
    >>> # Atomic addition with FP16 pairs
    >>> half_dst = T.Tensor([2], "float16", name="half_dst")
    >>> half_val = T.Tensor([2], "float16", name="half_val")
    >>> atomic_addx2(half_dst, half_val)
    
    
    
    >>> # BF16 vectorized atomic add (requires CUDA Arch > 750)
    >>> bf16_dst = T.Tensor([2], "bfloat16", name="bf16_dst")
    >>> bf16_val = T.Tensor([2], "bfloat16", name="bf16_val")
    >>> atomic_addx2(bf16_dst, bf16_val)
    
    
    
    >>> # Get previous paired values
    >>> prev_values = atomic_addx2(half_dst, half_val, return_prev=True)
    >>> # prev_values is a half2 containing the two previous FP16 values
    
    
    
    >>> # Efficient gradient accumulation for mixed precision training
    >>> @T.prim_func
    >>> def accumulate_fp16_gradients(grads: T.Buffer, global_grads: T.Buffer):
    >>>     for i in T.thread_binding(128, "threadIdx.x"):
    >>>         for j in range(0, grads.shape[1], 2):  # Process in pairs
    >>>             atomic_addx2(global_grads[i, j:j+2], grads[i, j:j+2])
    

tilelang.language.atomic.atomic_addx4(_dst_ , _value_ , _return_prev =False_)Â¶
    

Perform an atomic addition operation with quad-width operands.

Parameters:
    

  * **dst** (_Buffer_) â Destination buffer where the atomic addition will be performed

  * **value** (_PrimExpr_) â Value to be atomically added (quad-width)

  * **return_prev** ([_bool_](../dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool")) â If True, return the previous value; if False, return handle (default False)



Returns:
    

Handle to the quad-width atomic addition operation, or the previous value if return_prev is True

Return type:
    

PrimExpr

Examples
    
    
    >>> # Atomic addition with float4 (requires CUDA Arch >= 900)
    >>> float4_dst = T.Tensor([4], "float32", name="float4_dst")
    >>> float4_val = T.Tensor([4], "float32", name="float4_val")
    >>> atomic_addx4(float4_dst, float4_val)
    
    
    
    >>> # Get previous float4 values
    >>> prev_float4 = atomic_addx4(float4_dst, float4_val, return_prev=True)
    >>> # prev_float4 is a float4 containing the four previous float32 values
    
    
    
    >>> # High-throughput gradient accumulation for large models
    >>> @T.prim_func
    >>> def accumulate_float4_gradients(grads: T.Buffer, global_grads: T.Buffer):
    >>>     for i in T.thread_binding(256, "threadIdx.x"):
    >>>         for j in range(0, grads.shape[1], 4):  # Process 4 floats at once
    >>>             atomic_addx4(global_grads[i, j:j+4], grads[i, j:j+4])
    
    
    
    >>> # Efficient RGBA pixel blending
    >>> rgba_dst = T.Tensor([4], "float32", name="rgba_dst")  # R, G, B, A channels
    >>> rgba_add = T.Tensor([4], "float32", name="rgba_add")
    >>> atomic_addx4(rgba_dst, rgba_add)  # Atomic blend of all 4 channels
    

tilelang.language.atomic.atomic_load(_src_ , _memory_order ='seq_cst'_)Â¶
    

Load a value from the given buffer using the specified atomic memory ordering.

Performs an atomic load from src and returns a PrimExpr representing the loaded value. memory_order selects the ordering and must be one of: ârelaxedâ, âconsumeâ, âacquireâ, âreleaseâ, âacq_relâ, or âseq_cstâ (default). Raises KeyError if an unknown memory_order is provided.

Note: atomic_load always returns the loaded value, so no return_prev parameter is needed.

Examples
    
    
    >>> # Basic atomic load
    >>> shared_var = T.Tensor([1], "int32", name="shared_var")
    >>> value = atomic_load(shared_var)
    
    
    
    >>> # Load with specific memory ordering
    >>> value = atomic_load(shared_var, memory_order="acquire")
    >>> # Ensures all subsequent memory operations happen after this load
    
    
    
    >>> # Relaxed load for performance-critical code
    >>> value = atomic_load(shared_var, memory_order="relaxed")
    
    
    
    >>> # Producer-consumer pattern
    >>> @T.prim_func
    >>> def consumer(flag: T.Buffer, data: T.Buffer, result: T.Buffer):
    >>>     # Wait until producer sets flag
    >>>     while atomic_load(flag, memory_order="acquire") == 0:
    >>>         pass  # Spin wait
    >>>     # Now safely read data
    >>>     result[0] = data[0]
    
    
    
    >>> # Load counter for statistics
    >>> counter = T.Tensor([1], "int64", name="counter")
    >>> current_count = atomic_load(counter, memory_order="relaxed")
    

Parameters:
    

  * **src** (_tvm.tir.Buffer_)

  * **memory_order** (_str_)



Return type:
    

tvm.tir.PrimExpr

tilelang.language.atomic.atomic_store(_dst_ , _src_ , _memory_order ='seq_cst'_)Â¶
    

Perform an atomic store of src into dst with the given memory ordering.

Parameters:
    

  * **dst** (_Buffer_) â Destination buffer to store into.

  * **src** (_PrimExpr_) â Value to store.

  * **memory_order** (_str_ _,__optional_) â Memory ordering name; one of ârelaxedâ, âconsumeâ, âacquireâ, âreleaseâ, âacq_relâ, or âseq_cstâ. Defaults to âseq_cstâ. The name is mapped to an internal numeric ID used by the underlying runtime.



Returns:
    

A handle representing the issued atomic store operation.

Return type:
    

PrimExpr

Raises:
    

**KeyError** â If memory_order is not one of the supported names.

Note: atomic_store doesnât return a previous value, so no return_prev parameter is needed.

Examples
    
    
    >>> # Basic atomic store
    >>> shared_var = T.Tensor([1], "int32", name="shared_var")
    >>> atomic_store(shared_var, 42)
    
    
    
    >>> # Store with release ordering to publish data
    >>> data = T.Tensor([1000], "float32", name="data")
    >>> ready_flag = T.Tensor([1], "int32", name="ready_flag")
    >>> # ... fill data ...
    >>> atomic_store(ready_flag, 1, memory_order="release")
    >>> # Ensures all previous writes are visible before flag is set
    
    
    
    >>> # Relaxed store for performance
    >>> atomic_store(shared_var, 100, memory_order="relaxed")
    
    
    
    >>> # Producer-consumer synchronization
    >>> @T.prim_func
    >>> def producer(data: T.Buffer, flag: T.Buffer):
    >>>     data[0] = 3.14159  # Write data first
    >>>     atomic_store(flag, 1, memory_order="release")
    >>>     # Consumer can now safely read data after seeing flag == 1
    
    
    
    >>> # Update configuration atomically
    >>> config = T.Tensor([1], "int32", name="config")
    >>> new_config = 0x12345678
    >>> atomic_store(config, new_config, memory_order="seq_cst")
    
    
    
    >>> # Thread-safe logging counter
    >>> log_counter = T.Tensor([1], "int64", name="log_counter")
    >>> atomic_store(log_counter, 0)  # Reset counter atomically
    
