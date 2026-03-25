# tilelang.language.builtinÂ¶

Builtin operations exposed on the TileLang language surface.

## FunctionsÂ¶

`access_ptr`(base[, access_type, offset, extent, ...]) | Create a TileLang tl.access_ptr from a buffer-like base location.  
---|---  
`create_tma_descriptor`(*args) | Create a Tensor Memory Access (TMA) descriptor.  
`tma_load`(*args) | Perform a Tensor Memory Access (TMA) load operation.  
`fence_proxy_async`(*args) | Create a fence for asynchronous proxy operations.  
`tma_store_arrive`(*args) | Signal the arrival of a TMA store operation.  
`tma_store_wait`(*args) | Wait for completion of TMA store operations.  
`set_max_nreg`(reg_count, is_inc) | Set the maximum number of registers to use.  
`inc_max_nreg`(reg_count) | Increment the maximum number of registers to use.  
`dec_max_nreg`(reg_count) | Decrement the maximum number of registers to use.  
`annotate_producer_reg_dealloc`([reg_count]) | Annotate the producer reg dealloc.  
`annotate_consumer_reg_alloc`([reg_count]) | Annotate the consumer reg alloc.  
`no_set_max_nreg`() | Disable the maximum register limit setting.  
`disable_warp_group_reg_alloc`() | Disable the warp group reg alloc.  
`ptx_arrive_cluster_barrier`(mbarrier, cta_id) | Arrive at a shared barrier in cluster.  
`mbarrier_wait_parity`(mbarrier, parity) | Wait for memory barrier parity condition.  
`mbarrier_arrive`(mbarrier[, cta_id]) | Arrive at memory barrier.  
`mbarrier_expect_tx`(mbarrier, tx) | Set expected transaction count for memory barrier.  
`warpgroup_arrive`() | Signal warpgroup readiness for subsequent WGMMA operations.  
`warpgroup_commit_batch`() | Commit the current warpgroup batch for WGMMA operations.  
`warpgroup_wait`(num_mma) | Wait for completion of the specified warpgroup batch.  
`get_lane_idx`([warp_size]) | Return the logical lane index of the calling thread within a warp.  
`get_warp_idx_sync`([warp_size]) | Return the canonical warp index, assuming the warp's threads are converged.  
`get_warp_idx`([warp_size]) | Return the canonical warp index without synchronizing the warp.  
`get_warp_group_idx`([warp_size, warps_per_group]) | Return the canonical warp group index for the calling thread.  
`shuffle_elect`(thread_extent) | Elect exactly one lane within a logical thread group.  
`warpgroup_fence_operand`(buffer_or_ptr[, offset, ...]) | Insert a warpgroup fence for the destination accumulator registers.  
`wait_wgmma`(id) | Wait for WGMMA (Warp Group Matrix Multiply-Accumulate) operations to complete.  
`barrier_wait`(mbarrier, parity) | Wait for a memory barrier to complete.  
`barrier_arrive`(mbarrier) | Arrive at a memory barrier.  
`shfl_xor`(value, offset) | Perform a shuffle operation with XOR offset.  
`shfl_down`(value, offset) | Perform a shuffle operation with down offset.  
`shfl_up`(value, offset) | Perform a shuffle operation with up offset.  
`sync_threads`([barrier_id, arrive_count]) | Synchronize all threads in a block.  
`sync_warp`([mask]) | Synchronize all threads in a warp.  
`shfl_sync`(mask, value, srcLane[, width]) | Receives data from a thread in the same warp.  
`sync_global`() | Synchronize all threads in the entire grid.  
`sync_grid`() | Synchronize all threads in a grid.  
`initialize_wgmma_descriptor`(descriptor, start_address) | Initialize a WGMMA/UTCMMA shared-memory descriptor.  
`initialize_tcgen05_descriptor`(descriptor, ...[, ...]) | Initialize a TCGEN05 shared-memory descriptor.  
`increase_descriptor_offset`(descriptor, offset) | Increase the offset of a memory descriptor.  
`loop_break`() | Break out of the innermost loop.  
`cp_async_barrier_noinc`(barrier) | Perform a ptx async copy barrier using cp.async.mbarrier.arrive.noinc.  
`tcgen05_mma_arrive`(mbar) | Signal UMMA (TCGEN05) barrier arrival for a shared-memory mbarrier pointer.  
`ptx_mma_sm70`(shape, A_layout, B_layout, A_dtype, ...) | TVM intrinsic for ptx tensor core mma instructions on SM70 (Volta).  
`ldg32`(src[, pred]) | Load 32 bits (4 bytes) from global memory using explicit PTX instructions.  
`ldg64`(src[, pred]) | Load 64 bits (8 bytes) from global memory using explicit PTX instructions.  
`ldg128`(src[, pred]) | Load 128 bits (16 bytes) from global memory using explicit PTX instructions.  
`ldg256`(src[, pred]) | Load 256 bits (32 bytes) from global memory using explicit PTX instructions.  
`stg32`(dst, value[, pred]) | Store 32 bits (4 bytes) to global memory using explicit PTX instructions.  
`stg64`(dst, value[, pred]) | Store 64 bits (8 bytes) to global memory using explicit PTX instructions.  
`stg128`(dst, value[, pred]) | Store 128 bits (16 bytes) to global memory using explicit PTX instructions.  
`stg256`(dst, value[, pred]) | Store 256 bits (32 bytes) to global memory using explicit PTX instructions.  
  
## Module ContentsÂ¶

tilelang.language.builtin.access_ptr(_base_ , _access_type ='r'_, _* extents_, _offset =0_, _extent =None_, _ignore_last_ndim =0_)Â¶
    

Create a TileLang tl.access_ptr from a buffer-like base location.

This is a frontend convenience wrapper that keeps a BufferLoad argument in the resulting call so downstream passes can recover the referenced tir.Buffer (including strides/storage scope) _and_ the rw_mask (read/write intent) required by synchronization and safety checks.

The returned tl.access_ptr is expected to be lowered to tir.builtin.tvm_access_ptr later in the TileLang compilation pipeline.

Parameters:
    

  * **base** (_BufferLikeType_) â The base location to take the address of. Supported: \- tir.BufferLoad (e.g. A[i, j]): pointer to that element \- tir.BufferRegion: pointer to the region minima \- tir.Buffer: pointer to the beginning of the buffer \- tir.Var with let-binding to one of the above (inside TileLang frame)

  * **access_type** (_str_ _|__int_) â Access mask for the pointer. Common string forms: ârâ, âwâ, ârwâ. Integer bitmask is also accepted (1=read, 2=write, 3=read-write).

  * ***extents** (_PrimExpr_ _|__int_) â 

Optional per-axis extents. When provided and extent is not specified, the 1D extent passed to tvm_access_ptr is computed as the product of the provided extents (padding leading dimensions with 1 if needed).

For example: \- T.access_ptr(A[i], ârâ) -> extent defaults to 1 (element pointer) \- T.access_ptr(A[i], ârâ, 16) -> extent=16 \- T.access_ptr(A[i, j], ârâ, m, n) -> extent=m*n

  * **offset** (_PrimExpr_ _|__int_) â Additional element offset from the base location.

  * **extent** (_PrimExpr_ _|__int_ _|__None_) â Optional explicit 1D extent override (in elements). If provided, it takes precedence over *extents.

  * **ignore_last_ndim** (_int_) â If non-zero, the base linear offset is computed only over the leading dimensions, ignoring the last ignore_last_ndim axes. This is useful when treating an N-D buffer as a view of its trailing sub-tensor.



Returns:
    

**ptr** â A handle-typed tir.Call to tl.access_ptr.

Return type:
    

PrimExpr

tilelang.language.builtin.create_tma_descriptor(_* args_)Â¶
    

Create a Tensor Memory Access (TMA) descriptor.

Parameters:
    

***args** â Variable arguments defining the TMA descriptor configuration

Returns:
    

A handle to the created TMA descriptor

Return type:
    

tir.Call

tilelang.language.builtin.tma_load(_* args_)Â¶
    

Perform a Tensor Memory Access (TMA) load operation.

Parameters:
    

***args** â Variable arguments specifying the TMA load parameters

Returns:
    

A handle to the TMA load operation

Return type:
    

tir.Call

tilelang.language.builtin.fence_proxy_async(_* args_)Â¶
    

Create a fence for asynchronous proxy operations.

Parameters:
    

***args** â Variable arguments for fence configuration

Returns:
    

A handle to the fence operation

Return type:
    

tir.Call

tilelang.language.builtin.tma_store_arrive(_* args_)Â¶
    

Signal the arrival of a TMA store operation.

Parameters:
    

***args** â Variable arguments for the store arrival operation

Returns:
    

A handle to the store arrive operation

Return type:
    

tir.Call

tilelang.language.builtin.tma_store_wait(_* args_)Â¶
    

Wait for completion of TMA store operations.

Parameters:
    

***args** â Variable arguments specifying which store operations to wait for

Returns:
    

A handle to the store wait operation

Return type:
    

tir.Call

tilelang.language.builtin.set_max_nreg(_reg_count_ , _is_inc_)Â¶
    

Set the maximum number of registers to use. Detailed Documentation: <https://docs.nvidia.com/cuda/parallel-thread-execution/#miscellaneous-instructions-setmaxnreg>

Parameters:
    

  * **reg_count** (_int_) â int The number of registers to allocate

  * **is_inc** (_int_) â int Whether to increment or decrement the register count 0 if decrement, 1 if increment



Returns:
    

A handle to the register setting operation

Return type:
    

tir.Call

tilelang.language.builtin.inc_max_nreg(_reg_count_)Â¶
    

Increment the maximum number of registers to use.

Parameters:
    

**reg_count** (_int_)

tilelang.language.builtin.dec_max_nreg(_reg_count_)Â¶
    

Decrement the maximum number of registers to use.

Parameters:
    

**reg_count** (_int_)

tilelang.language.builtin.annotate_producer_reg_dealloc(_reg_count =24_)Â¶
    

Annotate the producer reg dealloc.

Parameters:
    

**reg_count** (_int_)

tilelang.language.builtin.annotate_consumer_reg_alloc(_reg_count =240_)Â¶
    

Annotate the consumer reg alloc.

Parameters:
    

**reg_count** (_int_)

tilelang.language.builtin.no_set_max_nreg()Â¶
    

Disable the maximum register limit setting.

tilelang.language.builtin.disable_warp_group_reg_alloc()Â¶
    

Disable the warp group reg alloc.

tilelang.language.builtin.ptx_arrive_cluster_barrier(_mbarrier_ , _cta_id_)Â¶
    

Arrive at a shared barrier in cluster.

Parameters:
    

  * **mbarrier** (_tilelang._typing.BarrierType_) â BarrierType The memory barrier to arrive at

  * **cta_id** (_int_ _|__tvm.tir.Var_) â int | Var The peer CTA rank in cluster to arrive at.




tilelang.language.builtin.mbarrier_wait_parity(_mbarrier_ , _parity_)Â¶
    

Wait for memory barrier parity condition.

Parameters:
    

  * **mbarrier** (_tilelang._typing.BarrierType_) â BarrierType

  * **on** (_The memory barrier to wait_) â 

parity: int | Var
    

The parity value to wait for

  * **parity** (_int_ _|__tvm.tir.Var_)




Examples
    
    
    mbar = T.alloc_barrier(1)
    # Wait for parity 0 on a single mbarrier
    T.mbarrier_wait_parity(mbar, 0)
    
    mbars = T.alloc_barrier([128] * n)
    # Wait for parity value on one of the mbarriers
    T.mbarrier_wait_parity(mbars[ko], ko)
    
    # Common usage in pipelined kernels:
    for ko in range(num_stages):
        # Producer waits for consumer to finish previous iteration
        T.mbarrier_wait_parity(mbars[1], ko ^ 1)
        # Producer copies data
        T.copy(A_global, A_shared)
        # Producer signals data ready
        T.mbarrier_arrive(mbars[0])
    
        # Consumer waits for producer data
        T.mbarrier_wait_parity(mbars[0], ko)
        # Consumer computes
        T.gemm(A_shared, B_shared, C_local)
        # Consumer signals completion
        T.mbarrier_arrive(mbars[1])
    

Returns:
    

A handle to the barrier wait operation

Return type:
    

tir.Call

Parameters:
    

  * **mbarrier** (_tilelang._typing.BarrierType_)

  * **parity** (_int_ _|__tvm.tir.Var_)




tilelang.language.builtin.mbarrier_arrive(_mbarrier_ , _cta_id =None_)Â¶
    

Arrive at memory barrier.

Parameters:
    

  * **mbarrier** (_tilelang._typing.BarrierType_) â BarrierType The memory barrier to arrive at

  * **cta_id** (_int_ _|__tvm.tir.Var_ _|__None_) â int | Var | None The peer CTA rank in cluster to arrive at. (Only valid for cluster barriers) If not provided, will arrive on current CTAâs barrier.




tilelang.language.builtin.mbarrier_expect_tx(_mbarrier_ , _tx_)Â¶
    

Set expected transaction count for memory barrier.

Parameters:
    

  * **mbarrier** (_tilelang._typing.BarrierType_) â BarrierType The memory barrier to expect transaction count for

  * **tx** (_int_) â int The expected transaction count



Returns:
    

A handle to the barrier expectation operation

Return type:
    

tir.Call

tilelang.language.builtin.warpgroup_arrive()Â¶
    

Signal warpgroup readiness for subsequent WGMMA operations.

Returns:
    

A handle to the warpgroup arrive operation.

Return type:
    

tir.Call

tilelang.language.builtin.warpgroup_commit_batch()Â¶
    

Commit the current warpgroup batch for WGMMA operations.

Returns:
    

A handle to the warpgroup commit batch operation.

Return type:
    

tir.Call

tilelang.language.builtin.warpgroup_wait(_num_mma_)Â¶
    

Wait for completion of the specified warpgroup batch.

Parameters:
    

**num_mma** (_int_) â int Identifier of the warpgroup MMA batch to wait on.

Returns:
    

A handle to the warpgroup wait operation.

Return type:
    

tir.Call

tilelang.language.builtin.get_lane_idx(_warp_size =None_)Â¶
    

Return the logical lane index of the calling thread within a warp.

Parameters:
    

**warp_size** (_Optional_ _[__int_ _,__PrimExpr_ _]_) â Logical warp (or wavefront) size. Defaults to 32 on NVIDIA and 64 on AMD.

Return type:
    

tvm.tir.PrimExpr

Example
    
    
    >>> lane = T.get_lane_idx()
    >>> custom_lane = T.get_lane_idx(64)  # override warp size explicitly
    

### Implementation NotesÂ¶

Lowers to the CUDA helper tl::get_lane_idx(warp_size) defined in src/tl_templates/cuda/intrin.h, which computes the lane index from the linear thread id using the provided warp_size.

tilelang.language.builtin.get_warp_idx_sync(_warp_size =None_)Â¶
    

Return the canonical warp index, assuming the warpâs threads are converged.

Parameters:
    

**warp_size** (_Optional_ _[__int_ _,__PrimExpr_ _]_) â Logical warp size used for the index calculation.

Return type:
    

tvm.tir.PrimExpr

Example
    
    
    >>> warp = T.get_warp_idx_sync()
    >>> custom_warp = T.get_warp_idx_sync(64)
    

### Implementation NotesÂ¶

Emits tl::get_warp_idx_sync(warp_size) which divides the block-linear thread id by warp_size, matching the semantics of CUTLASSâ canonical helpers.

tilelang.language.builtin.get_warp_idx(_warp_size =None_)Â¶
    

Return the canonical warp index without synchronizing the warp.

Parameters:
    

**warp_size** (_Optional_ _[__int_ _,__PrimExpr_ _]_) â Logical warp size used for the index calculation.

Return type:
    

tvm.tir.PrimExpr

Example
    
    
    >>> warp = T.get_warp_idx()
    >>> custom_warp = T.get_warp_idx(64)
    

### Implementation NotesÂ¶

Lowers to tl::get_warp_idx(warp_size) which divides the block-linear thread id by the provided warp_size without requiring warp convergence.

tilelang.language.builtin.get_warp_group_idx(_warp_size =None_, _warps_per_group =None_)Â¶
    

Return the canonical warp group index for the calling thread.

Parameters:
    

  * **warp_size** (_Optional_ _[__int_ _,__PrimExpr_ _]_) â Logical warp size to use (defaults to 32 on NVIDIA / 64 on AMD).

  * **warps_per_group** (_Optional_ _[__int_ _,__PrimExpr_ _]_) â Number of warps per warp-group. Defaults to 4 on NVIDIA architectures.



Return type:
    

tvm.tir.PrimExpr

Example
    
    
    >>> group = T.get_warp_group_idx()
    >>> custom_group = T.get_warp_group_idx(32, 6)  # treat 6 warps as a group
    

### Implementation NotesÂ¶

Generates tl::get_warp_group_idx(warp_size, warps_per_group) which divides the block-linear thread id by warp_size * warps_per_group, matching the canonical ordering while allowing architecture-specific overrides.

tilelang.language.builtin.shuffle_elect(_thread_extent_)Â¶
    

Elect exactly one lane within a logical thread group.

Parameters:
    

**thread_extent** (_int_) â Size (in threads) of the group in which a single lane should be elected. Passing 0 elects a single lane in the entire thread block.

Return type:
    

tvm.tir.PrimExpr

Example
    
    
    >>> is_leader = T.shuffle_elect(64)
    >>> T.if_then_else(is_leader, do_leader_work(), T.evaluate(0))
    

### Implementation NotesÂ¶

Lowered to the CUDA helper tl::tl_shuffle_elect<thread_extent>() defined in src/tl_templates/cuda/intrin.h, which relies on cutlass::canonical_warp_idx_sync() and cute::elect_one_sync() (or __shfl_sync) to pick one lane per group.

tilelang.language.builtin.warpgroup_fence_operand(_buffer_or_ptr_ , _offset =0_, _num_regs =None_, _dtype =None_)Â¶
    

Insert a warpgroup fence for the destination accumulator registers.

This prevents NVCC from sinking uses of accumulator fragments past the corresponding WGMMA operations by issuing an empty inline assembly barrier on every register.

Parameters:
    

  * **buffer_or_ptr** (_tilelang._typing.BufferLikeType_ _|__tvm.tir.PrimExpr_) â BufferLikeType | PrimExpr A buffer representing the accumulator fragment, a buffer load/region that identifies a starting element within the fragment, or a pointer expression (e.g., tvm_access_ptr/address_of/typed Var).

  * **offset** (_int_ _|__tvm.tir.PrimExpr_) â int | PrimExpr Element offset from the start of the accumulator fragment.

  * **num_regs** (_int_ _|__tvm.tir.PrimExpr_ _|__None_) â int | PrimExpr | None Number of 32-bit registers to fence. If None and a Buffer is provided, it will be derived from the buffer shape and dtype.

  * **dtype** (_tilelang._typing.DType_ _|__None_) â DType | None Data type string of the accumulator elements. When passing a buffer or buffer-derived expression, dtype is inferred. It is required only when passing a raw pointer expression that cannot be inferred.



Returns:
    

A handle to the warpgroup fence operation.

Return type:
    

tir.Call

tilelang.language.builtin.wait_wgmma(_id_)Â¶
    

Wait for WGMMA (Warp Group Matrix Multiply-Accumulate) operations to complete.

Parameters:
    

**id** (_int_) â int The id of the WGMMA operation to wait for

Returns:
    

A handle to the WGMMA wait operation

Return type:
    

tir.Call

tilelang.language.builtin.barrier_wait(_mbarrier_ , _parity_)Â¶
    

Wait for a memory barrier to complete.

Parameters:
    

  * **mbarrier** (_tilelang._typing.BarrierType_) â BarrierType The memory barrier to wait on

  * **parity** (_int_ _|__tvm.tir.Var_) â int | Var The parity value to wait for



Returns:
    

A handle to the barrier wait operation

Return type:
    

tir.Call

Current implementation is a sugar syntax for mbarrier_wait_parity, as we only support parity 0 and 1.

tilelang.language.builtin.barrier_arrive(_mbarrier_)Â¶
    

Arrive at a memory barrier.

Parameters:
    

**mbarrier** (_tilelang._typing.BarrierType_) â BarrierType The memory barrier to arrive at

tilelang.language.builtin.shfl_xor(_value_ , _offset_)Â¶
    

Perform a shuffle operation with XOR offset.

Parameters:
    

  * **value** (_int_ _|__tvm.tir.PrimExpr_ _|__tvm.tir.Call_) â Optional[int, PrimExpr] The value to shuffle

  * **offset** (_int_ _|__tvm.tir.PrimExpr_ _|__tvm.tir.Call_) â Optional[int, PrimExpr] The offset for the shuffle operation



Returns:
    

A handle to the shuffle operation

Return type:
    

tir.Call

tilelang.language.builtin.shfl_down(_value_ , _offset_)Â¶
    

Perform a shuffle operation with down offset.

Parameters:
    

  * **value** (_int_ _|__tvm.tir.PrimExpr_ _|__tvm.tir.Call_) â Optional[int, PrimExpr] The value to shuffle

  * **offset** (_int_ _|__tvm.tir.PrimExpr_ _|__tvm.tir.Call_)




tilelang.language.builtin.shfl_up(_value_ , _offset_)Â¶
    

Perform a shuffle operation with up offset.

Parameters:
    

  * **value** (_int_ _|__tvm.tir.PrimExpr_ _|__tvm.tir.Call_) â Optional[int, PrimExpr] The value to shuffle

  * **offset** (_int_ _|__tvm.tir.PrimExpr_ _|__tvm.tir.Call_)




tilelang.language.builtin.sync_threads(_barrier_id =None_, _arrive_count =None_)Â¶
    

Synchronize all threads in a block.

Parameters:
    

  * **barrier_id** (_int_)

  * **arrive_count** (_int_)




tilelang.language.builtin.sync_warp(_mask =None_)Â¶
    

Synchronize all threads in a warp.

Parameters:
    

**mask** (_int_)

tilelang.language.builtin.shfl_sync(_mask_ , _value_ , _srcLane_ , _width =None_)Â¶
    

Receives data from a thread in the same warp.

Parameters:
    

  * **mask** (_int_)

  * **value** (_int_ _|__tvm.tir.PrimExpr_)

  * **srcLane** (_int_)

  * **width** (_int_)




tilelang.language.builtin.sync_global()Â¶
    

Synchronize all threads in the entire grid.

tilelang.language.builtin.sync_grid()Â¶
    

Synchronize all threads in a grid.

tilelang.language.builtin.initialize_wgmma_descriptor(_descriptor_ , _start_address_ , _layout_type_ =0_, _leading_byte_offset =0_, _stride_byte_offset =0_)Â¶
    

Initialize a WGMMA/UTCMMA shared-memory descriptor.

Parameters:
    

  * **descriptor** (_tvm.tir.Buffer_)

  * **start_address** (_tvm.tir.PrimExpr_)

  * **layout_type_** (_int_)

  * **leading_byte_offset** (_int_)

  * **stride_byte_offset** (_int_)



Return type:
    

tvm.tir.PrimExpr

tilelang.language.builtin.initialize_tcgen05_descriptor(_descriptor_ , _start_address_ , _leading_byte_offset_ , _stride_byte_offset_ , _base_offset =0_, _leading_is_absolute =False_, _swizzle_mode =0_)Â¶
    

Initialize a TCGEN05 shared-memory descriptor.

Parameters:
    

  * **descriptor** (_tvm.tir.Buffer_)

  * **start_address** (_tvm.tir.PrimExpr_)

  * **leading_byte_offset** (_int_)

  * **stride_byte_offset** (_int_)

  * **base_offset** (_int_)

  * **leading_is_absolute** ([_bool_](../dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool"))

  * **swizzle_mode** (_int_)



Return type:
    

tvm.tir.PrimExpr

tilelang.language.builtin.increase_descriptor_offset(_descriptor_ , _offset_)Â¶
    

Increase the offset of a memory descriptor.

Parameters:
    

  * **descriptor** (_PrimExpr_) â The memory descriptor to modify.

  * **offset** (_PrimExpr_) â The offset value to increase.



Returns:
    

A handle representing the modified descriptor.

Return type:
    

PrimExpr

tilelang.language.builtin.loop_break()Â¶
    

Break out of the innermost loop.

tilelang.language.builtin.cp_async_barrier_noinc(_barrier_)Â¶
    

Perform a ptx async copy barrier using cp.async.mbarrier.arrive.noinc.

Parameters:
    

**barrier** (_tilelang._typing.BarrierType_)

tilelang.language.builtin.tcgen05_mma_arrive(_mbar_)Â¶
    

Signal UMMA (TCGEN05) barrier arrival for a shared-memory mbarrier pointer.

Parameters:
    

**mbar** (_tir.Buffer_ _|__BufferLoad_ _|__PrimExpr_) â The mbarrier object in shared memory (e.g., Barrier*) or its address.

tilelang.language.builtin.ptx_mma_sm70(_shape_ , _A_layout_ , _B_layout_ , _A_dtype_ , _B_dtype_ , _C_dtype_ , _multiplicand_a_ , _a_index_ , _multiplicand_b_ , _b_index_ , _accumulator_ , _c_index_)Â¶
    

TVM intrinsic for ptx tensor core mma instructions on SM70 (Volta).

This intrinsic provides SM70-specific MMA operations that support m16n16k4 shape with FP16 inputs and FP16/FP32 accumulation.

Parameters:
    

  * **shape** (_str_) â The shape of mma fragment (e.g., âm16n16k4â).

  * **A_layout** (_str_) â The layout of multiplicand fragment A (ârowâ or âcolâ).

  * **B_layout** (_str_) â The layout of multiplicand fragment B (ârowâ or âcolâ).

  * **A_dtype** (_str_) â The data type of multiplicand fragment A (typically âfp16â).

  * **B_dtype** (_str_) â The data type of multiplicand fragment B (typically âfp16â).

  * **C_dtype** (_str_) â The data type of accumulator fragment C (âfp16â or âfp32â).

  * **multiplicand_a** (_Var_) â The multiplicand fragment A variable.

  * **a_index** (_Expr_) â The index of multiplicand fragment A.

  * **multiplicand_b** (_Var_) â The multiplicand fragment B variable.

  * **b_index** (_Expr_) â The index of multiplicand fragment B.

  * **accumulator** (_Var_) â The accumulator fragment C variable.

  * **c_index** (_Expr_) â The index of accumulator fragment C.



Returns:
    

**call** â The call expression.

Return type:
    

PrimExpr

Examples
    
    
    >>> T.ptx_mma_sm70(
    ...     "float16",
    ...     "m16n16k4",
    ...     "row",
    ...     "col",
    ...     "fp16",
    ...     "fp16",
    ...     "fp16",
    ...     A_local.data,
    ...     0,
    ...     B_local.data,
    ...     0,
    ...     C_local.data,
    ...     0,
    ... )
    

tilelang.language.builtin.ldg32(_src_ , _pred =None_)Â¶
    

Load 32 bits (4 bytes) from global memory using explicit PTX instructions.

Usage: T.ldg32(x[i]) or T.ldg32(x[i:i+2]) emits tl::ldg32(ptr).

Parameters:
    

  * **src** (_tilelang._typing.BufferLikeType_) â A Buffer, BufferRegion, or BufferLoad.

  * **pred** (_tvm.tir.PrimExpr_) â Optional predicate condition. If False, the load is skipped.



Returns:
    

The loaded 32-bit value.

Return type:
    

PrimExpr

Example
    
    
    >>> val = T.ldg32(x[i])
    >>> val = T.ldg32(x[i:i+2])  # load 2 x fp16
    >>> val = T.ldg32(x[i], pred=i < N)  # predicated load
    

tilelang.language.builtin.ldg64(_src_ , _pred =None_)Â¶
    

Load 64 bits (8 bytes) from global memory using explicit PTX instructions.

Usage: T.ldg64(x[i]) or T.ldg64(x[i:i+4]) emits tl::ldg64(ptr).

Parameters:
    

  * **src** (_tilelang._typing.BufferLikeType_) â A Buffer, BufferRegion, or BufferLoad.

  * **pred** (_tvm.tir.PrimExpr_) â Optional predicate condition. If False, the load is skipped.



Returns:
    

The loaded 64-bit value.

Return type:
    

PrimExpr

Example
    
    
    >>> val = T.ldg64(x[i])
    >>> val = T.ldg64(x[i:i+4])  # load 4 x fp16
    >>> val = T.ldg64(x[i], pred=i < N)  # predicated load
    

tilelang.language.builtin.ldg128(_src_ , _pred =None_)Â¶
    

Load 128 bits (16 bytes) from global memory using explicit PTX instructions.

Usage: T.ldg128(x[i]) or T.ldg128(x[i:i+8]) emits tl::ldg128(ptr).

Parameters:
    

  * **src** (_tilelang._typing.BufferLikeType_) â A Buffer, BufferRegion, or BufferLoad.

  * **pred** (_tvm.tir.PrimExpr_) â Optional predicate condition. If False, the load is skipped.



Returns:
    

The loaded 128-bit value.

Return type:
    

PrimExpr

Example
    
    
    >>> val = T.ldg128(x[i])
    >>> val = T.ldg128(x[i:i+8])  # load 8 x fp16
    >>> val = T.ldg128(x[i], pred=i < N)  # predicated load
    

tilelang.language.builtin.ldg256(_src_ , _pred =None_)Â¶
    

Load 256 bits (32 bytes) from global memory using explicit PTX instructions.

Usage: T.ldg256(x[i]) or T.ldg256(x[i:i+16]) emits tl::ldg256(ptr).

Parameters:
    

  * **src** (_tilelang._typing.BufferLikeType_) â A Buffer, BufferRegion, or BufferLoad.

  * **pred** (_tvm.tir.PrimExpr_) â Optional predicate condition. If False, the load is skipped.



Returns:
    

The loaded 256-bit value.

Return type:
    

PrimExpr

Example
    
    
    >>> val = T.ldg256(x[i])
    >>> val = T.ldg256(x[i:i+16])  # load 16 x fp16
    >>> val = T.ldg256(x[i], pred=i < N)  # predicated load
    

tilelang.language.builtin.stg32(_dst_ , _value_ , _pred =None_)Â¶
    

Store 32 bits (4 bytes) to global memory using explicit PTX instructions.

Usage: T.stg32(y[i], value) emits tl::stg32(ptr, value).

Parameters:
    

  * **dst** (_tilelang._typing.BufferLikeType_) â A Buffer, BufferRegion, or BufferLoad indicating the destination.

  * **value** (_tvm.tir.PrimExpr_) â The 32-bit value to store.

  * **pred** (_tvm.tir.PrimExpr_) â Optional predicate condition. If False, the store is skipped.



Return type:
    

None

Example
    
    
    >>> T.stg32(y[i], val)
    >>> T.stg32(y[i], val, pred=i < N)  # predicated store
    

tilelang.language.builtin.stg64(_dst_ , _value_ , _pred =None_)Â¶
    

Store 64 bits (8 bytes) to global memory using explicit PTX instructions.

Usage: T.stg64(y[i:i+2], value) emits tl::stg64(ptr, value).

Parameters:
    

  * **dst** (_tilelang._typing.BufferLikeType_) â A Buffer, BufferRegion, or BufferLoad indicating the destination.

  * **value** (_tvm.tir.PrimExpr_) â The 64-bit value to store (e.g., uint2).

  * **pred** (_tvm.tir.PrimExpr_) â Optional predicate condition. If False, the store is skipped.



Return type:
    

None

Example
    
    
    >>> T.stg64(y[i:i+2], val)
    >>> T.stg64(y[i:i+2], val, pred=i < N)  # predicated store
    

tilelang.language.builtin.stg128(_dst_ , _value_ , _pred =None_)Â¶
    

Store 128 bits (16 bytes) to global memory using explicit PTX instructions.

Usage: T.stg128(y[i:i+4], value) emits tl::stg128(ptr, value).

Parameters:
    

  * **dst** (_tilelang._typing.BufferLikeType_) â A Buffer, BufferRegion, or BufferLoad indicating the destination.

  * **value** (_tvm.tir.PrimExpr_) â The 128-bit value to store (e.g., uint4).

  * **pred** (_tvm.tir.PrimExpr_) â Optional predicate condition. If False, the store is skipped.



Return type:
    

None

Example
    
    
    >>> T.stg128(y[i:i+4], val)
    >>> T.stg128(y[i:i+4], val, pred=i < N)  # predicated store
    

tilelang.language.builtin.stg256(_dst_ , _value_ , _pred =None_)Â¶
    

Store 256 bits (32 bytes) to global memory using explicit PTX instructions.

Usage: T.stg256(y[i:i+8], value) emits tl::stg256(ptr, value).

Parameters:
    

  * **dst** (_tilelang._typing.BufferLikeType_) â A Buffer, BufferRegion, or BufferLoad indicating the destination.

  * **value** (_tvm.tir.PrimExpr_) â The 256-bit value to store (e.g., ulonglong4).

  * **pred** (_tvm.tir.PrimExpr_) â Optional predicate condition. If False, the store is skipped.



Return type:
    

None

Example
    
    
    >>> T.stg256(y[i:i+8], val)
    >>> T.stg256(y[i:i+8], val, pred=i < N)  # predicated store
    
