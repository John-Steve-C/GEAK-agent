# tilelang.language.tir.irÂ¶

## AttributesÂ¶

`abs` |   
---|---  
`acos` |   
`acosh` |   
`address_of` |   
`asin` |   
`asinh` |   
`atan` |   
`atan2` |   
`atanh` |   
`bitwise_and` |   
`bitwise_not` |   
`bitwise_or` |   
`bitwise_xor` |   
`ceil` |   
`clz` |   
`copysign` |   
`cos` |   
`cosh` |   
`erf` |   
`exp` |   
`exp2` |   
`exp10` |   
`floor` |   
`ceildiv` |   
`cdiv` |   
`floordiv` |   
`floormod` |   
`fmod` |   
`hypot` |   
`if_then_else` |   
`infinity` |   
`isfinite` |   
`isinf` |   
`isnan` |   
`isnullptr` |   
`ldexp` |   
`likely` |   
`log` |   
`log1p` |   
`log2` |   
`log10` |   
`lookup_param` |   
`max_value` |   
`min_value` |   
`nearbyint` |   
`nextafter` |   
`popcount` |   
`pow` |   
`q_multiply_shift` |   
`q_multiply_shift_per_axis` |   
`ret` |   
`round` |   
`rsqrt` |   
`shift_left` |   
`shift_right` |   
`sigmoid` |   
`sin` |   
`sinh` |   
`sqrt` |   
`tan` |   
`tanh` |   
`trunc` |   
`truncdiv` |   
`truncmod` |   
`tvm_access_ptr` |   
`tvm_throw_last_error` |   
`tvm_stack_alloca` |   
`tvm_stack_make_shape` |   
`tvm_stack_make_array` |   
`tvm_check_return` |   
`call_packed` |   
`call_cpacked` |   
`call_packed_lowered` |   
`call_cpacked_lowered` |   
`tvm_tuple` |   
`tvm_struct_set` |   
`tvm_struct_get` |   
`tvm_thread_invariant` |   
`tvm_thread_allreduce` |   
`tvm_load_matrix_sync` |   
`tvm_mma_sync` |   
`tvm_bmma_sync` |   
`tvm_fill_fragment` |   
`tvm_store_matrix_sync` |   
`tvm_storage_sync` |   
`tvm_warp_shuffle` |   
`tvm_warp_shuffle_up` |   
`tvm_warp_shuffle_down` |   
`tvm_warp_activemask` |   
`ptx_wait_group` |   
`ptx_commit_group` |   
`ptx_cp_async_barrier` |   
`ptx_init_barrier_thread_count` |   
`ptx_fence_barrier_init` |   
`ptx_arrive_barrier` |   
`ptx_arrive_barrier_expect_tx` |   
`ptx_wait_barrier` |   
`create_barriers` |   
`assume` |   
`undef` |   
`TVMBackendAllocWorkspace` |   
`TVMBackendFreeWorkspace` |   
`start_profile_intrinsic` |   
`end_profile_intrinsic` |   
`anylist_getitem` |   
`anylist_resetitem` |   
`anylist_setitem_call_packed` |   
`anylist_setitem_call_cpacked` |   
`vscale` |   
`reinterpret` |   
`call_extern` |   
`call_intrin` |   
`call_llvm_intrin` |   
`call_llvm_pure_intrin` |   
`call_pure_extern` |   
`ptx_mma` |   
`ptx_mma_sp` |   
`ptx_wgmma_ss` |   
`ptx_wgmma_rs` |   
`ptx_tcgen05_mma_ss` |   
`ptx_tcgen05_mma_ts` |   
`ptx_ldmatrix` |   
`ptx_cp_async` |   
`ptx_cp_async_bulk` |   
`mma_store` |   
`mma_fill` |   
`vectorlow` |   
`vectorhigh` |   
`vectorcombine` |   
`tvm_mfma` |   
`tvm_mfma_store` |   
`tvm_rdna_wmma` |   
`tvm_rdna_wmma_store` |   
  
## FunctionsÂ¶

`serial`(start[, stop, annotations]) | The serial For statement.  
---|---  
`parallel`(start[, stop, annotations]) | The parallel For statement.  
`vectorized`(start[, stop, annotations]) | The vectorized For statement.  
`unroll`(start[, stop, annotations]) | The unrolled For statement.  
`thread_binding`(start[, stop, thread, annotations]) | The thread-binding For statement.  
`grid`(*extents) | The grid For statement.  
  
## Module ContentsÂ¶

tilelang.language.tir.ir.serial(_start_ , _stop =None_, _*_ , _annotations =None_)Â¶
    

The serial For statement.

Parameters:
    

  * **start** (_PrimExpr_) â The minimum value of iteration.

  * **stop** (_PrimExpr_) â The maximum value of iteration.

  * **annotations** (_Dict_ _[__str_ _,__Any_ _]_) â The optional annotations of the For statement.



Returns:
    

**res** â The ForFrame.

Return type:
    

frame.ForFrame

tilelang.language.tir.ir.parallel(_start_ , _stop =None_, _*_ , _annotations =None_)Â¶
    

The parallel For statement.

Parameters:
    

  * **start** (_PrimExpr_) â The minimum value of iteration.

  * **stop** (_PrimExpr_) â The maximum value of iteration.

  * **annotations** (_Dict_ _[__str_ _,__Any_ _]_) â The optional annotations of the For statement.



Returns:
    

**res** â The ForFrame.

Return type:
    

frame.ForFrame

tilelang.language.tir.ir.vectorized(_start_ , _stop =None_, _*_ , _annotations =None_)Â¶
    

The vectorized For statement.

Parameters:
    

  * **start** (_PrimExpr_) â The minimum value of iteration.

  * **stop** (_PrimExpr_) â The maximum value of iteration.

  * **annotations** (_Dict_ _[__str_ _,__Any_ _]_) â The optional annotations of the For statement.



Returns:
    

**res** â The ForFrame.

Return type:
    

frame.ForFrame

tilelang.language.tir.ir.unroll(_start_ , _stop =None_, _*_ , _annotations =None_)Â¶
    

The unrolled For statement.

Parameters:
    

  * **start** (_PrimExpr_) â The minimum value of iteration.

  * **stop** (_PrimExpr_) â The maximum value of iteration.

  * **annotations** (_Dict_ _[__str_ _,__Any_ _]_) â The optional annotations of the For statement.



Returns:
    

**res** â The ForFrame.

Return type:
    

frame.ForFrame

tilelang.language.tir.ir.thread_binding(_start_ , _stop =None_, _thread =None_, _*_ , _annotations =None_)Â¶
    

The thread-binding For statement.

Parameters:
    

  * **start** (_PrimExpr_) â The minimum value of iteration.

  * **stop** (_PrimExpr_) â The maximum value of iteration.

  * **thread** (_str_) â The thread for loop variable to bind.

  * **annotations** (_Dict_ _[__str_ _,__Any_ _]_) â The optional annotations of the For statement.



Returns:
    

**res** â The ForFrame.

Return type:
    

frame.ForFrame

tilelang.language.tir.ir.grid(_* extents_)Â¶
    

The grid For statement.

Parameters:
    

**extents** (_PrimExpr_) â The extents of the iteration.

Returns:
    

**res** â The ForFrame.

Return type:
    

frame.ForFrame

tilelang.language.tir.ir.absÂ¶
    

tilelang.language.tir.ir.acosÂ¶
    

tilelang.language.tir.ir.acoshÂ¶
    

tilelang.language.tir.ir.address_ofÂ¶
    

tilelang.language.tir.ir.asinÂ¶
    

tilelang.language.tir.ir.asinhÂ¶
    

tilelang.language.tir.ir.atanÂ¶
    

tilelang.language.tir.ir.atan2Â¶
    

tilelang.language.tir.ir.atanhÂ¶
    

tilelang.language.tir.ir.bitwise_andÂ¶
    

tilelang.language.tir.ir.bitwise_notÂ¶
    

tilelang.language.tir.ir.bitwise_orÂ¶
    

tilelang.language.tir.ir.bitwise_xorÂ¶
    

tilelang.language.tir.ir.ceilÂ¶
    

tilelang.language.tir.ir.clzÂ¶
    

tilelang.language.tir.ir.copysignÂ¶
    

tilelang.language.tir.ir.cosÂ¶
    

tilelang.language.tir.ir.coshÂ¶
    

tilelang.language.tir.ir.erfÂ¶
    

tilelang.language.tir.ir.expÂ¶
    

tilelang.language.tir.ir.exp2Â¶
    

tilelang.language.tir.ir.exp10Â¶
    

tilelang.language.tir.ir.floorÂ¶
    

tilelang.language.tir.ir.ceildivÂ¶
    

tilelang.language.tir.ir.cdivÂ¶
    

tilelang.language.tir.ir.floordivÂ¶
    

tilelang.language.tir.ir.floormodÂ¶
    

tilelang.language.tir.ir.fmodÂ¶
    

tilelang.language.tir.ir.hypotÂ¶
    

tilelang.language.tir.ir.if_then_elseÂ¶
    

tilelang.language.tir.ir.infinityÂ¶
    

tilelang.language.tir.ir.isfiniteÂ¶
    

tilelang.language.tir.ir.isinfÂ¶
    

tilelang.language.tir.ir.isnanÂ¶
    

tilelang.language.tir.ir.isnullptrÂ¶
    

tilelang.language.tir.ir.ldexpÂ¶
    

tilelang.language.tir.ir.likelyÂ¶
    

tilelang.language.tir.ir.logÂ¶
    

tilelang.language.tir.ir.log1pÂ¶
    

tilelang.language.tir.ir.log2Â¶
    

tilelang.language.tir.ir.log10Â¶
    

tilelang.language.tir.ir.lookup_paramÂ¶
    

tilelang.language.tir.ir.max_valueÂ¶
    

tilelang.language.tir.ir.min_valueÂ¶
    

tilelang.language.tir.ir.nearbyintÂ¶
    

tilelang.language.tir.ir.nextafterÂ¶
    

tilelang.language.tir.ir.popcountÂ¶
    

tilelang.language.tir.ir.powÂ¶
    

tilelang.language.tir.ir.q_multiply_shiftÂ¶
    

tilelang.language.tir.ir.q_multiply_shift_per_axisÂ¶
    

tilelang.language.tir.ir.retÂ¶
    

tilelang.language.tir.ir.roundÂ¶
    

tilelang.language.tir.ir.rsqrtÂ¶
    

tilelang.language.tir.ir.shift_leftÂ¶
    

tilelang.language.tir.ir.shift_rightÂ¶
    

tilelang.language.tir.ir.sigmoidÂ¶
    

tilelang.language.tir.ir.sinÂ¶
    

tilelang.language.tir.ir.sinhÂ¶
    

tilelang.language.tir.ir.sqrtÂ¶
    

tilelang.language.tir.ir.tanÂ¶
    

tilelang.language.tir.ir.tanhÂ¶
    

tilelang.language.tir.ir.truncÂ¶
    

tilelang.language.tir.ir.truncdivÂ¶
    

tilelang.language.tir.ir.truncmodÂ¶
    

tilelang.language.tir.ir.tvm_access_ptrÂ¶
    

tilelang.language.tir.ir.tvm_throw_last_errorÂ¶
    

tilelang.language.tir.ir.tvm_stack_allocaÂ¶
    

tilelang.language.tir.ir.tvm_stack_make_shapeÂ¶
    

tilelang.language.tir.ir.tvm_stack_make_arrayÂ¶
    

tilelang.language.tir.ir.tvm_check_returnÂ¶
    

tilelang.language.tir.ir.call_packedÂ¶
    

tilelang.language.tir.ir.call_cpackedÂ¶
    

tilelang.language.tir.ir.call_packed_loweredÂ¶
    

tilelang.language.tir.ir.call_cpacked_loweredÂ¶
    

tilelang.language.tir.ir.tvm_tupleÂ¶
    

tilelang.language.tir.ir.tvm_struct_setÂ¶
    

tilelang.language.tir.ir.tvm_struct_getÂ¶
    

tilelang.language.tir.ir.tvm_thread_invariantÂ¶
    

tilelang.language.tir.ir.tvm_thread_allreduceÂ¶
    

tilelang.language.tir.ir.tvm_load_matrix_syncÂ¶
    

tilelang.language.tir.ir.tvm_mma_syncÂ¶
    

tilelang.language.tir.ir.tvm_bmma_syncÂ¶
    

tilelang.language.tir.ir.tvm_fill_fragmentÂ¶
    

tilelang.language.tir.ir.tvm_store_matrix_syncÂ¶
    

tilelang.language.tir.ir.tvm_storage_syncÂ¶
    

tilelang.language.tir.ir.tvm_warp_shuffleÂ¶
    

tilelang.language.tir.ir.tvm_warp_shuffle_upÂ¶
    

tilelang.language.tir.ir.tvm_warp_shuffle_downÂ¶
    

tilelang.language.tir.ir.tvm_warp_activemaskÂ¶
    

tilelang.language.tir.ir.ptx_wait_groupÂ¶
    

tilelang.language.tir.ir.ptx_commit_groupÂ¶
    

tilelang.language.tir.ir.ptx_cp_async_barrierÂ¶
    

tilelang.language.tir.ir.ptx_init_barrier_thread_countÂ¶
    

tilelang.language.tir.ir.ptx_fence_barrier_initÂ¶
    

tilelang.language.tir.ir.ptx_arrive_barrierÂ¶
    

tilelang.language.tir.ir.ptx_arrive_barrier_expect_txÂ¶
    

tilelang.language.tir.ir.ptx_wait_barrierÂ¶
    

tilelang.language.tir.ir.create_barriersÂ¶
    

tilelang.language.tir.ir.assumeÂ¶
    

tilelang.language.tir.ir.undefÂ¶
    

tilelang.language.tir.ir.TVMBackendAllocWorkspaceÂ¶
    

tilelang.language.tir.ir.TVMBackendFreeWorkspaceÂ¶
    

tilelang.language.tir.ir.start_profile_intrinsicÂ¶
    

tilelang.language.tir.ir.end_profile_intrinsicÂ¶
    

tilelang.language.tir.ir.anylist_getitemÂ¶
    

tilelang.language.tir.ir.anylist_resetitemÂ¶
    

tilelang.language.tir.ir.anylist_setitem_call_packedÂ¶
    

tilelang.language.tir.ir.anylist_setitem_call_cpackedÂ¶
    

tilelang.language.tir.ir.vscaleÂ¶
    

tilelang.language.tir.ir.reinterpretÂ¶
    

tilelang.language.tir.ir.call_externÂ¶
    

tilelang.language.tir.ir.call_intrinÂ¶
    

tilelang.language.tir.ir.call_llvm_intrinÂ¶
    

tilelang.language.tir.ir.call_llvm_pure_intrinÂ¶
    

tilelang.language.tir.ir.call_pure_externÂ¶
    

tilelang.language.tir.ir.ptx_mmaÂ¶
    

tilelang.language.tir.ir.ptx_mma_spÂ¶
    

tilelang.language.tir.ir.ptx_wgmma_ssÂ¶
    

tilelang.language.tir.ir.ptx_wgmma_rsÂ¶
    

tilelang.language.tir.ir.ptx_tcgen05_mma_ssÂ¶
    

tilelang.language.tir.ir.ptx_tcgen05_mma_tsÂ¶
    

tilelang.language.tir.ir.ptx_ldmatrixÂ¶
    

tilelang.language.tir.ir.ptx_cp_asyncÂ¶
    

tilelang.language.tir.ir.ptx_cp_async_bulkÂ¶
    

tilelang.language.tir.ir.mma_storeÂ¶
    

tilelang.language.tir.ir.mma_fillÂ¶
    

tilelang.language.tir.ir.vectorlowÂ¶
    

tilelang.language.tir.ir.vectorhighÂ¶
    

tilelang.language.tir.ir.vectorcombineÂ¶
    

tilelang.language.tir.ir.tvm_mfmaÂ¶
    

tilelang.language.tir.ir.tvm_mfma_storeÂ¶
    

tilelang.language.tir.ir.tvm_rdna_wmmaÂ¶
    

tilelang.language.tir.ir.tvm_rdna_wmma_storeÂ¶
    
