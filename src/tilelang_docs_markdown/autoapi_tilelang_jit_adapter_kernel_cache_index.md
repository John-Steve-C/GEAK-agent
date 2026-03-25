# tilelang.jit.adapter.kernel_cacheÂ¶

## ClassesÂ¶

`TVMFFIKernelCache` | Caches compiled kernels using a class and database persistence to avoid redundant compilation.  
---|---  
  
## Module ContentsÂ¶

_class _tilelang.jit.adapter.kernel_cache.TVMFFIKernelCacheÂ¶
    

Bases: [`tilelang.cache.kernel_cache.KernelCache`](../../../cache/kernel_cache/index.html#tilelang.cache.kernel_cache.KernelCache "tilelang.cache.kernel_cache.KernelCache")

Caches compiled kernels using a class and database persistence to avoid redundant compilation. Cache files:

> kernel.cu: The compiled kernel source code wrapped_kernel.cu: The compiled wrapped kernel source code kernel_lib.so: The compiled kernel library params.pkl: The compiled kernel parameters

kernel_lib_path _ = 'executable.so'_Â¶
    
