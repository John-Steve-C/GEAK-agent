# tilelang.jit.adapter.torch.metalÂ¶

## ClassesÂ¶

`MetalKernelAdapter` | Helper class that provides a standard way to create an ABC using  
---|---  
  
## Module ContentsÂ¶

_class _tilelang.jit.adapter.torch.metal.MetalKernelAdapter(_params_ , _result_idx_ , _func_or_mod_ , _device_mod =None_, _kernel_global_source =None_, _verbose =False_)Â¶
    

Bases: [`tilelang.jit.adapter.base.BaseKernelAdapter`](../../base/index.html#tilelang.jit.adapter.base.BaseKernelAdapter "tilelang.jit.adapter.base.BaseKernelAdapter")

Helper class that provides a standard way to create an ABC using inheritance.

Parameters:
    

  * **params** (_list_ _[_[_tilelang.engine.param.KernelParam_](../../../../engine/param/index.html#tilelang.engine.param.KernelParam "tilelang.engine.param.KernelParam") _]_)

  * **result_idx** (_list_ _[__int_ _]_)

  * **func_or_mod** (_tvm.tir.PrimFunc_ _|__tilelang.tvm.IRModule_)

  * **device_mod** (_tilelang.tvm.IRModule_ _|__None_)

  * **kernel_global_source** (_str_ _|__None_)

  * **verbose** ([_bool_](../../../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool"))




kernel_global_source _ = None_Â¶
    

kernel_nameÂ¶
    

verbose _ = False_Â¶
    

block_info _ = [1, 1, 1]_Â¶
    

grid_info _ = [1, 1, 1]_Â¶
    
