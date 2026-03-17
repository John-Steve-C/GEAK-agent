# tilelang.jit.adapter.cutedsl.adapterÂ¶

## AttributesÂ¶

`logger` |   
---|---  
  
## ClassesÂ¶

`CuTeDSLKernelAdapter` | Helper class that provides a standard way to create an ABC using  
---|---  
  
## Module ContentsÂ¶

tilelang.jit.adapter.cutedsl.adapter.loggerÂ¶
    

_class _tilelang.jit.adapter.cutedsl.adapter.CuTeDSLKernelAdapter(_params_ , _result_idx_ , _target_ , _func_or_mod_ , _host_mod =None_, _device_mod =None_, _host_kernel_source =None_, _device_kernel_source =None_, _verbose =False_, _pass_configs =None_, _compile_flags =None_)Â¶
    

Bases: [`tilelang.jit.adapter.base.BaseKernelAdapter`](../../base/index.html#tilelang.jit.adapter.base.BaseKernelAdapter "tilelang.jit.adapter.base.BaseKernelAdapter")

Helper class that provides a standard way to create an ABC using inheritance.

Parameters:
    

  * **params** (_list_ _[_[_tilelang.engine.param.KernelParam_](../../../../engine/param/index.html#tilelang.engine.param.KernelParam "tilelang.engine.param.KernelParam") _]_)

  * **result_idx** (_list_ _[__int_ _]_)

  * **target** (_str_ _|__tvm.target.Target_)

  * **func_or_mod** (_tvm.tir.PrimFunc_ _|__tilelang.tvm.IRModule_)

  * **host_mod** (_tilelang.tvm.IRModule_ _|__None_)

  * **device_mod** (_tilelang.tvm.IRModule_ _|__None_)

  * **host_kernel_source** (_str_ _|__None_)

  * **device_kernel_source** (_str_ _|__None_)

  * **verbose** ([_bool_](../../../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool"))

  * **pass_configs** (_dict_ _[__str_ _,__Any_ _]__|__None_)

  * **compile_flags** (_list_ _[__str_ _]__|__None_)




pymodule _ = None_Â¶
    

paramsÂ¶
    

result_idxÂ¶
    

host_kernel_source _ = None_Â¶
    

device_kernel_source _ = None_Â¶
    

param_dtypesÂ¶
    

param_shapes _ = []_Â¶
    

targetÂ¶
    

verbose _ = False_Â¶
    

wrapperÂ¶
    

host_funcÂ¶
    

function_namesÂ¶
    

launcher_cpp_codeÂ¶
    

launcher_lib_nameÂ¶
    

lib_generatorÂ¶
    

libpathÂ¶
    

kernel_global_source _ = None_Â¶
    

_classmethod _from_database(_params_ , _result_idx_ , _target_ , _func_or_mod_ , _host_kernel_source_ , _device_kernel_source_ , _kernel_lib_path_ , _verbose =False_, _pass_configs =None_, _compile_flags =None_)Â¶
    

Parameters:
    

  * **params** (_list_ _[_[_tilelang.engine.param.KernelParam_](../../../../engine/param/index.html#tilelang.engine.param.KernelParam "tilelang.engine.param.KernelParam") _]_)

  * **result_idx** (_list_ _[__int_ _]_)

  * **target** (_str_)

  * **func_or_mod** (_tvm.tir.PrimFunc_ _|__tilelang.tvm.IRModule_)

  * **host_kernel_source** (_str_)

  * **device_kernel_source** (_str_)

  * **kernel_lib_path** (_str_)

  * **verbose** ([_bool_](../../../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool"))

  * **pass_configs** (_dict_ _[__str_ _,__Any_ _]__|__None_)

  * **compile_flags** (_list_ _[__str_ _]__|__None_)




get_kernel_source(_kernel_only =True_)Â¶
    

Get the CUDA kernel source code.

Returns:
    

The kernel source code, or None if not available

Return type:
    

str | None

Parameters:
    

**kernel_only** ([_bool_](../../../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool"))

cleanup()Â¶
    

Explicitly cleanup this adapterâs CUDA resources.

This method can be called explicitly to immediately release CUDA resources without waiting for garbage collection. Useful in Jupyter notebooks or tests.

Note: This is safe to call multiple times as the C++ implementation is idempotent.

_property _prim_func _: tvm.tir.PrimFunc_Â¶
    

Returns the primary TIR function from the IR module.

Return type:
    

tvm.tir.PrimFunc
