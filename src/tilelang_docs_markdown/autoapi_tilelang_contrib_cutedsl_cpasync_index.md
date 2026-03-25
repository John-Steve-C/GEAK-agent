# tilelang.contrib.cutedsl.cpasyncÂ¶

## FunctionsÂ¶

`cp_async_gs`(size, dst, src) |   
---|---  
`cp_async_gs_conditional`(size, dst, src, cond) |   
`extract_tensormap_ptr`(tma_atom, *[, loc, ip]) | extract the tensormap pointer from a TMA Copy Atom.  
`tma_load`(tma_desc, mbar, smem_ptr, crd, *[, loc, ip]) | Load data from global memory to shared memory using TMA (Tensor Memory Access).  
`tma_store`(tma_desc, smem_ptr, crd, *[, loc, ip]) | Store data from shared memory to global memory using TMA (Tensor Memory Access).  
`tma_reduce`(tma_desc, smem_ptr, crd, *[, loc, ip]) | Reduce data from shared memory to global memory using TMA with atomic ADD reduction.  
`tma_store_arrive`(*[, loc, ip]) | Indicate arrival of warp issuing TMA_STORE.  
`tma_store_wait`(count, *[, read, loc, ip]) | Wait for TMA_STORE operations to complete.  
`cp_async_shared_global`(dst, src, cp_size, modifier, *) | Asynchronously copy data from global memory to shared memory.  
`prefetch_tma_descriptor`(tma_desc, *[, loc, ip]) | Prefetch a TMA descriptor.  
`mbarrier_wait`(mbar_ptr, phase[, timeout_ns, loc, ip]) | Waits on a mbarrier with a specified phase (blocking loop).  
`mbarrier_cp_async_arrive`(mbar_ptr, *[, loc, ip]) |   
`fence_proxy_async`() |   
`fence_barrier_init`() |   
  
## Module ContentsÂ¶

tilelang.contrib.cutedsl.cpasync.cp_async_gs(_size_ , _dst_ , _src_)Â¶
    

tilelang.contrib.cutedsl.cpasync.cp_async_gs_conditional(_size_ , _dst_ , _src_ , _cond_)Â¶
    

tilelang.contrib.cutedsl.cpasync.extract_tensormap_ptr(_tma_atom_ , _*_ , _loc =None_, _ip =None_)Â¶
    

extract the tensormap pointer from a TMA Copy Atom. :param tma_atom: The TMA Copy Atom :type tma_atom: CopyAtom

Parameters:
    

**tma_atom** (_cutlass.cute.CopyAtom_)

Return type:
    

cutlass.cute.Pointer

tilelang.contrib.cutedsl.cpasync.tma_load(_tma_desc_ , _mbar_ , _smem_ptr_ , _crd_ , _*_ , _loc =None_, _ip =None_)Â¶
    

Load data from global memory to shared memory using TMA (Tensor Memory Access).

Parameters:
    

  * **tma_desc** (_CopyAtom_ _or_ _tensormap_ptr_ _or_ _Tensor_ _of_ _tensormap_ptr_) â TMA descriptor for the tensor

  * **mbar** (_Pointer_) â Mbarrier pointer in shared memory

  * **smem_ptr** (_Pointer_) â Destination pointer in shared memory

  * **crd** (_tuple_ _[__Int_ _,__...__]_) â Coordinates tuple for the tensor access



Return type:
    

None

tilelang.contrib.cutedsl.cpasync.tma_store(_tma_desc_ , _smem_ptr_ , _crd_ , _*_ , _loc =None_, _ip =None_)Â¶
    

Store data from shared memory to global memory using TMA (Tensor Memory Access).

Parameters:
    

  * **tma_desc** (_TMA descriptor_) â TMA descriptor for the tensor

  * **smem_ptr** (_Pointer_) â Source pointer in shared memory

  * **crd** (_tuple_ _[__Int_ _,__...__]_) â Coordinates tuple for the tensor access



Return type:
    

None

tilelang.contrib.cutedsl.cpasync.tma_reduce(_tma_desc_ , _smem_ptr_ , _crd_ , _*_ , _loc =None_, _ip =None_)Â¶
    

Reduce data from shared memory to global memory using TMA with atomic ADD reduction.

This performs an atomic add of shared memory data to global memory using the TMA unitâs reduce capability.

Parameters:
    

  * **tma_desc** (_TMA descriptor_) â TMA descriptor for the tensor

  * **smem_ptr** (_Pointer_) â Source pointer in shared memory

  * **crd** (_tuple_ _[__Int_ _,__...__]_) â Coordinates tuple for the tensor access



Return type:
    

None

tilelang.contrib.cutedsl.cpasync.tma_store_arrive(_*_ , _loc =None_, _ip =None_)Â¶
    

Indicate arrival of warp issuing TMA_STORE. Corresponds to PTX instruction: cp.async.bulk.commit_group;

Return type:
    

None

tilelang.contrib.cutedsl.cpasync.tma_store_wait(_count_ , _*_ , _read =None_, _loc =None_, _ip =None_)Â¶
    

Wait for TMA_STORE operations to complete. Corresponds to PTX instruction: cp.async.bulk.wait_group.read <count>;

Parameters:
    

**count** (_Int_) â The number of outstanding bulk async groups to wait for

Return type:
    

None

tilelang.contrib.cutedsl.cpasync.cp_async_shared_global(_dst_ , _src_ , _cp_size_ , _modifier_ , _*_ , _src_size =None_, _loc =None_, _ip =None_)Â¶
    

Asynchronously copy data from global memory to shared memory.

Parameters:
    

  * **dst** (_Pointer_) â Destination pointer in shared memory

  * **src** (_Pointer_) â Source pointer in global memory

  * **size** (_Int_) â Size of the copy in bytes

  * **modifier** (_Int_) â Cache modifier

  * **cp_size** (_Int_) â Optional copy size override

  * **src_size** (_cutlass.cute.typing.Int_)



Return type:
    

None

tilelang.contrib.cutedsl.cpasync.prefetch_tma_descriptor(_tma_desc_ , _*_ , _loc =None_, _ip =None_)Â¶
    

Prefetch a TMA descriptor. Corresponds to PTX instruction: prefetch.tensormap;

Return type:
    

None

tilelang.contrib.cutedsl.cpasync.mbarrier_wait(_mbar_ptr_ , _phase_ , _timeout_ns =10000000_, _*_ , _loc =None_, _ip =None_)Â¶
    

Waits on a mbarrier with a specified phase (blocking loop).

Uses inline PTX to loop until the try_wait succeeds. The CUDA backend does: while (!mbar.try_wait(parity)) {}

Parameters:
    

  * **mbar_ptr** (_cutlass.cute.typing.Pointer_)

  * **phase** (_cutlass.cute.typing.Int_)

  * **timeout_ns** (_cutlass.cute.typing.Int_)



Return type:
    

None

tilelang.contrib.cutedsl.cpasync.mbarrier_cp_async_arrive(_mbar_ptr_ , _*_ , _loc =None_, _ip =None_)Â¶
    

Parameters:
    

**mbar_ptr** (_cutlass.cute.typing.Pointer_)

Return type:
    

None

tilelang.contrib.cutedsl.cpasync.fence_proxy_async()Â¶
    

tilelang.contrib.cutedsl.cpasync.fence_barrier_init()Â¶
    
