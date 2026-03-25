# tilelang.language.allocateÂ¶

Memory allocation utilities for Tile-AI programs.

This module provides a set of functions for allocating different types of memory buffers in Tile-AI programs. It wraps TVMâs buffer allocation functionality with convenient interfaces for different memory scopes.

Available allocation functions:
    

  * alloc_shared: Allocates shared memory buffers for inter-thread communication

  * alloc_local: Allocates local memory buffers for thread-private storage

  * alloc_fragment: Allocates fragment memory buffers for specialized operations

  * alloc_var: Allocates single-element variable buffers




Each function takes shape and dtype parameters and returns a TVM buffer object with the appropriate memory scope.

## AttributesÂ¶

`ReducerOp` |   
---|---  
`DescKind` |   
  
## FunctionsÂ¶

`alloc_shared`(shape, dtype[, scope]) | Allocate a shared memory buffer for inter-thread communication.  
---|---  
`alloc_local`(shape, dtype[, scope]) | Allocate a local memory buffer for thread-private storage.  
`alloc_fragment`(shape, dtype[, scope]) | Allocate a fragment memory buffer for specialized operations.  
`alloc_var`(â¦) | Allocate a single-element variable buffer.  
`alloc_barrier`(arrive_count) | Allocate a barrier buffer.  
`alloc_cluster_barrier`(arrive_count) | Allocate a cluster barrier buffer.  
`alloc_tmem`(shape, dtype) | Allocate a Tensor Memory (TMEM) buffer for use with 5th generation Tensor Core operations (e.g., TCGEN5.MMA).  
`alloc_reducer`(shape, dtype[, op, replication]) | Allocate a reducer buffer.  
`alloc_descriptor`([kind, dtype]) | Allocate a descriptor buffer for WGMMA and TCGEN5.MMA.  
`alloc_wgmma_desc`([dtype]) |   
`alloc_tcgen05_smem_desc`([dtype]) |   
`alloc_tcgen05_instruction_desc`([dtype]) |   
`alloc_tcgen05_instr_desc`([dtype]) |   
`empty`(shape[, dtype]) |   
  
## Module ContentsÂ¶

tilelang.language.allocate.alloc_shared(_shape_ , _dtype_ , _scope ='shared.dyn'_)Â¶
    

Allocate a shared memory buffer for inter-thread communication.

Parameters:
    

  * **shape** (_tuple_) â The shape of the buffer to allocate

  * **dtype** (_str_) â The data type of the buffer (e.g., âfloat32â, âint32â)

  * **scope** (_str_ _,__optional_) â The memory scope. Defaults to âshared.dynâ



Returns:
    

A TVM buffer object allocated in shared memory

Return type:
    

T.Buffer

tilelang.language.allocate.alloc_local(_shape_ , _dtype_ , _scope ='local'_)Â¶
    

Allocate a local memory buffer for thread-private storage.

Parameters:
    

  * **shape** (_tuple_) â The shape of the buffer to allocate

  * **dtype** (_str_) â The data type of the buffer (e.g., âfloat32â, âint32â)

  * **scope** (_str_ _,__optional_) â The memory scope. Defaults to âlocalâ



Returns:
    

A TVM buffer object allocated in local memory

Return type:
    

T.Buffer

tilelang.language.allocate.alloc_fragment(_shape_ , _dtype_ , _scope ='local.fragment'_)Â¶
    

Allocate a fragment memory buffer for specialized operations.

Parameters:
    

  * **shape** (_tuple_) â The shape of the buffer to allocate

  * **dtype** (_str_) â The data type of the buffer (e.g., âfloat32â, âint32â)

  * **scope** (_str_ _,__optional_) â The memory scope. Defaults to âlocal.fragmentâ



Returns:
    

A TVM buffer object allocated in fragment memory

Return type:
    

T.Buffer

tilelang.language.allocate.alloc_var(_dtype : tilelang._typing.DType_, _init : tvm.tir.PrimExpr | int | float_, _scope : str = 'local.var'_) → tvm.tir.buffer.BufferÂ¶
tilelang.language.allocate.alloc_var(_dtype : tilelang._typing.DType_, _scope : str = 'local.var'_, _*_ , _init : tvm.tir.PrimExpr | int | float | None = None_) → tvm.tir.buffer.Buffer
    

Allocate a single-element variable buffer.

Parameters:
    

  * **dtype** (_str_) â The data type of the buffer (e.g., âfloat32â, âint32â)

  * ***args** â Optional positional arguments. A single positional string is treated as the scope for backward compatibility. A single non-string positional argument (or keyword `init`) specifies the initializer. When two positional arguments are provided, they are interpreted as `(init, scope)`.

  * **scope** (_str_ _,__optional_) â The memory scope. Defaults to âlocal.varâ. Use as keyword argument for clarity when also providing an initializer.

  * **init** (_PrimExpr_ _,__optional_) â The optional initializer value. When provided, the generated code will initialize the variable with this value instead of defaulting to zero.




Examples

a = T.alloc_var(âint32â, 1) # var with init 1 a = T.alloc_var(âint32â, âlocal.varâ) # var with local.var scope a = T.alloc_var(âint32â, 1, âlocal.varâ) # var with init 1 and local.var scope a = T.alloc_var(âint32â, âlocal.varâ, init=1) # var with init 1 and local.var scope a = T.alloc_var(âint32â, init=1) # var with init 1 and local.var scope

Returns:
    

A TVM buffer object allocated as a single-element variable

Return type:
    

T.Buffer

tilelang.language.allocate.alloc_barrier(_arrive_count_)Â¶
    

Allocate a barrier buffer.

Parameters:
    

**arrive_count** (_int_ _|__list_ _[__int_ _]_) â The number of threads that need to arrive at each barrier

Returns:
    

A TVM buffer object allocated as a barrier

Return type:
    

T.Buffer

Examples
    
    
    >>> mbar = alloc_barrier(128)  # allocate a barrier with arrive count 128
    >>> mbars = alloc_barrier([128] * n)  # allocate n barriers with the same arrive count 128
    

tilelang.language.allocate.alloc_cluster_barrier(_arrive_count_)Â¶
    

Allocate a cluster barrier buffer.

Parameters:
    

**arrive_count** (_int_ _|__list_ _[__int_ _]_) â The number of threads that need to arrive at each barrier

Returns:
    

A TVM buffer object allocated as a cluster barrier

Return type:
    

T.Buffer

tilelang.language.allocate.alloc_tmem(_shape_ , _dtype_)Â¶
    

Allocate a Tensor Memory (TMEM) buffer for use with 5th generation Tensor Core operations (e.g., TCGEN5.MMA).

TMEM is a dedicated on-chip memory introduced in Hopper GPUs, designed to reduce register pressure and enable asynchronous, single-threaded MMA operations. It is organized as a 2D array of 512 columns by 128 rows (lanes), with each cell being 32 bits. Allocation is performed in units of columns, and every lane of a column is allocated together.

Key properties and requirements:
    

  * The number of columns allocated must be a power of 2 and at least 32.

  * TMEM allocations are dynamic and must be explicitly deallocated.

  * Both allocation and deallocation must be performed by the same warp.

  * The base address of the TMEM allocation is stored in shared memory and used as the offset for TCGEN5.MMA accumulator tensors.

  * Only TCGEN5.MMA and specific TMEM load/store instructions can access TMEM; all pre-processing must occur before data is loaded into TMEM, and all post-processing after data is retrieved.

  * The number of columns allocated should not increase between any two allocations in the execution order within the CTA.




Parameters:
    

  * **num_cols** (_int_) â Number of columns to allocate in TMEM. Must be a power of 2 and >= 32 but less than or equal to 512.

  * **shape** (_tilelang._typing.ShapeType_)

  * **dtype** (_tilelang._typing.DType_)



Returns:
    

A TVM buffer object allocated in TMEM scope, suitable for use as an accumulator or operand in TCGEN5.MMA operations.

Return type:
    

T.Buffer

Note

  * TMEM is only available on supported architectures (e.g., Hopper and later).

  * The buffer returned should be used according to TMEM access restrictions and deallocated appropriately.




tilelang.language.allocate.ReducerOpÂ¶
    

tilelang.language.allocate.alloc_reducer(_shape_ , _dtype_ , _op ='sum'_, _replication =None_)Â¶
    

Allocate a reducer buffer.

Modifications needs to conform with op, such as op=âsumâ requires reducer[â¦] += â¦ and op=âmaxâ requires reducer[â¦] = T.max(reducer[â¦], â¦).

Only after T.fill with proper initializer the reduction may begin; only after T.finalize_reducer the partial results will be available.

For op=âsumâ, filled value must be 0; for min and max, the filled initializer will become max or min clamper correspondingly. You may want to use T.max_value for min and T.min_value for max.

Parameters:
    

  * **shape** (_tuple_) â The shape of the buffer to allocate

  * **dtype** (_str_) â The data type of the buffer (e.g., âfloat32â, âint32â)

  * **op** (_str_) â The reduce operation corresponded with the reducer

  * **replication** (_str_ _|__None_) â Replication strategy, can be âallâ or ânoneâ. Defaults to not specified, and the compiler will do whatever it want.



Returns:
    

A TVM buffer object allocated in thread-private storage, available to reduce values in T.Parallel loops.

Return type:
    

T.Buffer

tilelang.language.allocate.DescKindÂ¶
    

tilelang.language.allocate.alloc_descriptor(_kind ='wgmma'_, _dtype =_dtypes.uint64_)Â¶
    

Allocate a descriptor buffer for WGMMA and TCGEN5.MMA.

Parameters:
    

  * **kind** (_DescKind_) â The descriptor kind, one of âwgmmaâ, âtcgen05â (âutcmmaâ as alias).

  * **dtype** (_tilelang._typing.DType_)



Returns:
    

A TVM buffer object allocated as a descriptor

Return type:
    

T.Buffer

tilelang.language.allocate.alloc_wgmma_desc(_dtype =_dtypes.uint64_)Â¶
    

Parameters:
    

**dtype** (_tilelang._typing.DType_)

Return type:
    

tvm.tir.buffer.Buffer

tilelang.language.allocate.alloc_tcgen05_smem_desc(_dtype =_dtypes.uint64_)Â¶
    

Parameters:
    

**dtype** (_tilelang._typing.DType_)

Return type:
    

tvm.tir.buffer.Buffer

tilelang.language.allocate.alloc_tcgen05_instruction_desc(_dtype =_dtypes.uint32_)Â¶
    

Parameters:
    

**dtype** (_tilelang._typing.DType_)

Return type:
    

tvm.tir.buffer.Buffer

tilelang.language.allocate.alloc_tcgen05_instr_desc(_dtype =_dtypes.uint32_)Â¶
    

Parameters:
    

**dtype** (_tilelang._typing.DType_)

Return type:
    

tvm.tir.buffer.Buffer

tilelang.language.allocate.empty(_shape_ , _dtype =_dtypes.float32_)Â¶
    

Parameters:
    

**dtype** (_tilelang._typing.DType_)

Return type:
    

tilelang.language.proxy.Tensor
