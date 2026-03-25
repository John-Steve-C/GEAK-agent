# tilelang.cacheÂ¶

The cache utils with class and database persistence - Init file

## SubmodulesÂ¶

  * [tilelang.cache.kernel_cache](kernel_cache/index.html)



## FunctionsÂ¶

`cached`([func, out_idx, target, target_host, ...]) | Caches and reuses compiled kernels (using KernelCache class).  
---|---  
`clear_cache`() | Disabled helper that previously removed the entire kernel cache.  
  
## Package ContentsÂ¶

tilelang.cache.cached(_func =None_, _out_idx =None_, _* args_, _target =None_, _target_host =None_, _execution_backend =None_, _verbose =None_, _pass_configs =None_, _compile_flags =None_)Â¶
    

Caches and reuses compiled kernels (using KernelCache class).

Parameters:
    

  * **func** (_tvm.tir.PrimFunc_)

  * **out_idx** (_list_ _[__int_ _]_)

  * **target** (_str_ _|__tvm.target.Target_ _|__None_)

  * **target_host** (_str_ _|__tvm.target.Target_ _|__None_)

  * **execution_backend** (_Literal_ _[__'auto'__,__'tvm_ffi'__,__'cython'__,__'nvrtc'__,__'torch'__,__'cutedsl'__]__|__None_)

  * **verbose** ([_bool_](../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool") _|__None_)

  * **pass_configs** (_dict_ _|__None_)

  * **compile_flags** (_list_ _[__str_ _]__|__str_ _|__None_)



Return type:
    

tilelang.jit.JITKernel

tilelang.cache.clear_cache()Â¶
    

Disabled helper that previously removed the entire kernel cache.

Raises:
    

**RuntimeError** â Always raised to warn users to clear the cache manually.
