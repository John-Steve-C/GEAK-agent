# tilelang.contrib.cutedsl.atomicÂ¶

Atomic operations for CuTeDSL backend.

This module provides implementations of atomic operations using NVVM and LLVM dialects.

## FunctionsÂ¶

`AtomicAdd`(ptr, value, *[, loc, ip]) | Perform atomic addition on a pointer.  
---|---  
`AtomicAddRet`(ptr, value, *[, loc, ip]) | Perform atomic addition and return the previous value.  
`AtomicAddx2`(dst_ptr, src_values, *[, loc, ip]) | Vectorized atomic add for 2 consecutive elements.  
`AtomicAddx4`(dst_ptr, src_values, *[, loc, ip]) | Vectorized atomic add for 4 consecutive float32 elements.  
`AtomicMax`(ptr, value, *[, loc, ip]) | Perform atomic maximum operation.  
`AtomicMaxRet`(ptr, value, *[, loc, ip]) | Perform atomic maximum and return the previous value.  
`AtomicMin`(ptr, value, *[, loc, ip]) | Perform atomic minimum operation.  
`AtomicMinRet`(ptr, value, *[, loc, ip]) | Perform atomic minimum and return the previous value.  
`AtomicLoad`(ptr, memory_order, *[, loc, ip]) | Perform atomic load with specified memory ordering.  
`AtomicStore`(ptr, value, memory_order, *[, loc, ip]) | Perform atomic store with specified memory ordering.  
  
## Module ContentsÂ¶

tilelang.contrib.cutedsl.atomic.AtomicAdd(_ptr_ , _value_ , _*_ , _loc =None_, _ip =None_)Â¶
    

Perform atomic addition on a pointer.

Supports float16, float32, int32, and int64 types. Returns the old value before addition (atomicrmw semantics).

Parameters:
    

  * **ptr** (_cutlass.cute.Pointer_)

  * **value** (_Numeric_)




tilelang.contrib.cutedsl.atomic.AtomicAddRet(_ptr_ , _value_ , _*_ , _loc =None_, _ip =None_)Â¶
    

Perform atomic addition and return the previous value.

This is the same as AtomicAdd since nvvm.atomicrmw always returns old value.

Parameters:
    

  * **ptr** (_cutlass.cute.Pointer_)

  * **value** (_Numeric_)




tilelang.contrib.cutedsl.atomic.AtomicAddx2(_dst_ptr_ , _src_values_ , _*_ , _loc =None_, _ip =None_)Â¶
    

Vectorized atomic add for 2 consecutive elements.

Uses PTX atom.add.v2.f32 for float32 or atom.add.noftz.v2.f16 for float16.

Parameters:
    

  * **dst_ptr** (_cutlass.cute.Pointer_) â Pointer to destination (2 consecutive elements)

  * **src_values** â Source values - can be TensorSSA (loaded tensor) or Pointer




tilelang.contrib.cutedsl.atomic.AtomicAddx4(_dst_ptr_ , _src_values_ , _*_ , _loc =None_, _ip =None_)Â¶
    

Vectorized atomic add for 4 consecutive float32 elements.

Uses PTX atom.global.add.v4.f32 for true vectorized atomic operation on SM90+.

Parameters:
    

  * **dst_ptr** (_cutlass.cute.Pointer_) â Pointer to destination (4 consecutive float32 elements)

  * **src_values** â Source values - can be TensorSSA (loaded tensor) or Pointer




tilelang.contrib.cutedsl.atomic.AtomicMax(_ptr_ , _value_ , _*_ , _loc =None_, _ip =None_)Â¶
    

Perform atomic maximum operation.

For integers, uses nvvm.atomicrmw with MAX. For floats, uses CAS loop since PTX doesnât have atomic max for float32.

Parameters:
    

  * **ptr** (_cutlass.cute.Pointer_)

  * **value** (_Numeric_)




tilelang.contrib.cutedsl.atomic.AtomicMaxRet(_ptr_ , _value_ , _*_ , _loc =None_, _ip =None_)Â¶
    

Perform atomic maximum and return the previous value.

Parameters:
    

  * **ptr** (_cutlass.cute.Pointer_)

  * **value** (_Numeric_)




tilelang.contrib.cutedsl.atomic.AtomicMin(_ptr_ , _value_ , _*_ , _loc =None_, _ip =None_)Â¶
    

Perform atomic minimum operation.

For integers, uses nvvm.atomicrmw with MIN. For floats, uses CAS loop since PTX doesnât have atomic min for float32.

Parameters:
    

  * **ptr** (_cutlass.cute.Pointer_)

  * **value** (_Numeric_)




tilelang.contrib.cutedsl.atomic.AtomicMinRet(_ptr_ , _value_ , _*_ , _loc =None_, _ip =None_)Â¶
    

Perform atomic minimum and return the previous value.

Parameters:
    

  * **ptr** (_cutlass.cute.Pointer_)

  * **value** (_Numeric_)




tilelang.contrib.cutedsl.atomic.AtomicLoad(_ptr_ , _memory_order_ , _*_ , _loc =None_, _ip =None_)Â¶
    

Perform atomic load with specified memory ordering.

Parameters:
    

  * **ptr** (_cutlass.cute.Pointer_) â Pointer to load from

  * **memory_order** (_int_) â TileLang memory order ID (0=relaxed, 2=acquire, 5=seq_cst, etc.)



Returns:
    

The loaded value

PTX mapping (per NVIDIA ABI):
    

relaxed: ld.relaxed.<scope> acquire: ld.acquire.<scope> seq_cst: fence.sc.<scope>; ld.relaxed.<scope>

tilelang.contrib.cutedsl.atomic.AtomicStore(_ptr_ , _value_ , _memory_order_ , _*_ , _loc =None_, _ip =None_)Â¶
    

Perform atomic store with specified memory ordering.

Parameters:
    

  * **ptr** (_cutlass.cute.Pointer_) â Pointer to store to

  * **value** (_Numeric_) â Value to store

  * **memory_order** (_int_) â TileLang memory order ID (0=relaxed, 3=release, 5=seq_cst, etc.)




PTX mapping (per NVIDIA ABI):
    

relaxed: st.relaxed.<scope> release: st.release.<scope> seq_cst: fence.sc.<scope>; st.relaxed.<scope>
