# tilelang.jit.adapter.tvm_ffiÂ¶

Utilities to adapt TVM FFI kernels to Torch tensors.

This adapter intentionally captures PyTorchâs current CUDA stream and device via light-weight callables so that, when the wrapped function is invoked, the execution observes the same stream context as the active Torch code. On non-CUDA builds, the stream/device fall back to 0/CPU semantics.

## AttributesÂ¶

`COMPILE_ARGS` |   
---|---  
  
## ClassesÂ¶

`TVMFFIKernelAdapter` | Adapter that runs a TVM runtime.Executable with Torch tensors.  
---|---  
  
## Module ContentsÂ¶

tilelang.jit.adapter.tvm_ffi.COMPILE_ARGSÂ¶
    

_class _tilelang.jit.adapter.tvm_ffi.TVMFFIKernelAdapter(_params_ , _result_idx_ , _target_ , _func_or_mod_ , _host_mod =None_, _device_mod =None_, _rt_mod =None_, _host_kernel_source =None_, _device_kernel_source =None_, _verbose =False_, _pass_configs =None_, _compile_flags =None_)Â¶
    

Bases: [`tilelang.jit.adapter.base.BaseKernelAdapter`](../base/index.html#tilelang.jit.adapter.base.BaseKernelAdapter "tilelang.jit.adapter.base.BaseKernelAdapter")

Adapter that runs a TVM runtime.Executable with Torch tensors.

Notes \- We capture the âcurrentâ PyTorch CUDA stream/device as thunks (callables)

> rather than materializing them at construction time. This ensures the actual stream/device is read just-in-time when the function runs, matching the userâs current Torch context (e.g., after a stream guard/switch).

  * The stream pointer returned is a raw CUDA stream handle compatible with TVMâs device API; on CPU or when CUDA is unavailable, we return 0.




Parameters:
    

  * **params** (_list_ _[_[_tilelang.engine.param.KernelParam_](../../../engine/param/index.html#tilelang.engine.param.KernelParam "tilelang.engine.param.KernelParam") _]_)

  * **result_idx** (_list_ _[__int_ _]_)

  * **target** (_str_ _|__tvm.target.Target_)

  * **func_or_mod** (_tvm.tir.PrimFunc_ _|__tilelang.tvm.IRModule_)

  * **host_mod** (_tilelang.tvm.IRModule_ _|__None_)

  * **device_mod** (_tilelang.tvm.IRModule_ _|__None_)

  * **rt_mod** (_tilelang.tvm.runtime.Module_ _|__None_)

  * **host_kernel_source** (_str_ _|__None_)

  * **device_kernel_source** (_str_ _|__None_)

  * **verbose** ([_bool_](../../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool"))

  * **pass_configs** (_dict_ _[__str_ _,__Any_ _]__|__None_)

  * **compile_flags** (_list_ _[__str_ _]__|__None_)




target _: str | tvm.target.Target_ _ = 'cuda'_Â¶
    

ir_module _: tilelang.tvm.IRModule | None_ _ = None_Â¶
    

host_kernel_source _: str | None_ _ = None_Â¶
    

device_kernel_source _: str | None_ _ = None_Â¶
    

executable _: tilelang.tvm.runtime.Executable | None_ _ = None_Â¶
    

pass_configs _: dict[str, Any] | None_ _ = None_Â¶
    

host_mod _: tilelang.tvm.IRModule | None_ _ = None_Â¶
    

device_mod _: tilelang.tvm.IRModule | None_ _ = None_Â¶
    

rt_mod _: tilelang.tvm.runtime.Module | None_ _ = None_Â¶
    

dynamic_symbolic_map _: dict[tvm.tir.Var, tuple[int, int, int]] | None_ _ = None_Â¶
    

paramsÂ¶
    

result_idxÂ¶
    

verbose _ = False_Â¶
    

compile_flags _ = None_Â¶
    

kernel_global_source _ = None_Â¶
    

_classmethod _from_database(_params_ , _result_idx_ , _target_ , _func_or_mod_ , _host_kernel_source_ , _device_kernel_source_ , _kernel_lib_path_ , _verbose =False_, _pass_configs =None_, _compile_flags =None_)Â¶
    

Parameters:
    

  * **params** (_list_ _[__tvm.relax.TensorType_ _]_)

  * **result_idx** (_list_ _[__int_ _]_)

  * **target** (_str_)

  * **func_or_mod** (_tvm.tir.PrimFunc_ _|__tilelang.tvm.IRModule_)

  * **host_kernel_source** (_str_)

  * **device_kernel_source** (_str_)

  * **kernel_lib_path** (_str_)

  * **verbose** ([_bool_](../../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool"))

  * **pass_configs** (_dict_ _[__str_ _,__Any_ _]__|__None_)

  * **compile_flags** (_list_ _[__str_ _]__|__None_)




get_host_source()Â¶
    

Returns the source code of the host module.

get_device_source()Â¶
    

Returns the source code of the device module.

get_kernel_source(_kernel_only =False_)Â¶
    

Returns the source code of the compiled kernel.

Parameters:
    

**kernel_only** ([_bool_](../../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool"))

_property _prim_func _: tvm.tir.PrimFunc_Â¶
    

Returns the primary TIR function from the IR module.

Return type:
    

tvm.tir.PrimFunc
