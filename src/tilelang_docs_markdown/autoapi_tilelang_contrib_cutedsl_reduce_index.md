# tilelang.contrib.cutedsl.reduceÂ¶

Reduce operations for CuTeDSL backend. Based on tl_templates/cuda/reduce.h

## ClassesÂ¶

`SumOp` | Sum reduction operator  
---|---  
`MaxOp` | Max reduction operator  
`MinOp` | Min reduction operator  
`BitAndOp` | Bitwise AND reduction operator  
`BitOrOp` | Bitwise OR reduction operator  
`BitXorOp` | Bitwise XOR reduction operator  
`CumSum1D` | 1D cumulative sum operation.  
`CumSum2D` | 2D cumulative sum operation.  
`NamedBarrier` | Named barrier policy for AllReduce, uses bar.sync instead of __syncthreads.  
  
## FunctionsÂ¶

`min`(a, b[, c]) | Type-aware min: uses arith.minsi for integers, nvvm.fmin for floats.  
---|---  
`max`(a, b[, c]) | Type-aware max: uses arith.maxsi for integers, nvvm.fmax for floats.  
`bar_sync`(barrier_id, number_of_threads) |   
`bar_sync_ptx`(barrier_id, number_of_threads) |   
`AllReduce`(reducer, threads, scale, thread_offset[, ...]) | AllReduce operation implementing warp/block-level reduction.  
  
## Module ContentsÂ¶

tilelang.contrib.cutedsl.reduce.min(_a_ , _b_ , _c =None_)Â¶
    

Type-aware min: uses arith.minsi for integers, nvvm.fmin for floats. Falls back to integer path if float conversion fails (signless int types).

tilelang.contrib.cutedsl.reduce.max(_a_ , _b_ , _c =None_)Â¶
    

Type-aware max: uses arith.maxsi for integers, nvvm.fmax for floats. Falls back to integer path if float conversion fails (signless int types).

_class _tilelang.contrib.cutedsl.reduce.SumOpÂ¶
    

Sum reduction operator

_static ___call__(_x_ , _y_)Â¶
    

_class _tilelang.contrib.cutedsl.reduce.MaxOpÂ¶
    

Max reduction operator

_static ___call__(_x_ , _y_)Â¶
    

_class _tilelang.contrib.cutedsl.reduce.MinOpÂ¶
    

Min reduction operator

_static ___call__(_x_ , _y_)Â¶
    

_class _tilelang.contrib.cutedsl.reduce.BitAndOpÂ¶
    

Bitwise AND reduction operator

_static ___call__(_x_ , _y_)Â¶
    

_class _tilelang.contrib.cutedsl.reduce.BitOrOpÂ¶
    

Bitwise OR reduction operator

_static ___call__(_x_ , _y_)Â¶
    

_class _tilelang.contrib.cutedsl.reduce.BitXorOpÂ¶
    

Bitwise XOR reduction operator

_static ___call__(_x_ , _y_)Â¶
    

tilelang.contrib.cutedsl.reduce.bar_sync(_barrier_id_ , _number_of_threads_)Â¶
    

tilelang.contrib.cutedsl.reduce.bar_sync_ptx(_barrier_id_ , _number_of_threads_)Â¶
    

_class _tilelang.contrib.cutedsl.reduce.CumSum1D(_threads_ , _reverse_)Â¶
    

1D cumulative sum operation. Based on tl::CumSum1D from reduce.h

Template params:
    

threads: Number of threads reverse: Whether to cumsum in reverse order

Parameters:
    

  * **threads** (_cutlass.Constexpr_ _[__int_ _]_)

  * **reverse** (_cutlass.Constexpr_ _[_[_bool_](../../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool") _]_)




threadsÂ¶
    

reverseÂ¶
    

SEG _ = 32_Â¶
    

run(_src_ , _dst_ , _N_)Â¶
    

Perform 1D cumulative sum.

Parameters:
    

  * **src** (_cutlass.cute.Pointer_) â Source pointer

  * **dst** (_cutlass.cute.Pointer_) â Destination pointer

  * **N** â Number of elements (must be compile-time constant or small)




_class _tilelang.contrib.cutedsl.reduce.CumSum2D(_threads_ , _dim_ , _reverse_)Â¶
    

2D cumulative sum operation. Based on tl::CumSum2D from reduce.h

Template params:
    

threads: Number of threads (must be power of 2, 32-1024) dim: Axis along which to cumsum (0 or 1) reverse: Whether to cumsum in reverse order

Parameters:
    

  * **threads** (_cutlass.Constexpr_ _[__int_ _]_)

  * **dim** (_cutlass.Constexpr_ _[__int_ _]_)

  * **reverse** (_cutlass.Constexpr_ _[_[_bool_](../../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool") _]_)




threadsÂ¶
    

dimÂ¶
    

reverseÂ¶
    

SEG _ = 32_Â¶
    

TILE_HÂ¶
    

run(_src_ , _dst_ , _H_ , _W_)Â¶
    

Perform 2D cumulative sum.

Parameters:
    

  * **src** (_cutlass.cute.Pointer_) â Source pointer

  * **dst** (_cutlass.cute.Pointer_) â Destination pointer

  * **H** â Number of rows

  * **W** â Number of columns (should be <= 32 for single-segment case)




_class _tilelang.contrib.cutedsl.reduce.NamedBarrier(_all_threads_)Â¶
    

Named barrier policy for AllReduce, uses bar.sync instead of __syncthreads. Based on tl::NamedBarrier<all_threads> from reduce.h

all_threadsÂ¶
    

tilelang.contrib.cutedsl.reduce.AllReduce(_reducer_ , _threads_ , _scale_ , _thread_offset_ , _all_threads =None_)Â¶
    

AllReduce operation implementing warp/block-level reduction. Based on tl::AllReduce from reduce.h

Parameters:
    

  * **reducer** â Reducer operator class (SumOp, MaxOp, etc.)

  * **threads** â Number of threads participating in reduction

  * **scale** â Reduction scale factor

  * **thread_offset** â Thread ID offset

  * **all_threads** â Total number of threads in block



Returns:
    

A callable object with run() and run_hopper() methods
