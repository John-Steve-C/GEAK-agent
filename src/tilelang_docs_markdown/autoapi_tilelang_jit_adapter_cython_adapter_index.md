# tilelang.jit.adapter.cython.adapterÂ¶

The profiler and convert to torch utils

## AttributesÂ¶

`logger` |   
---|---  
  
## ClassesÂ¶

`CythonKernelAdapter` | Adapter class that converts TVM/TIR functions to callable CUDA kernels using cython.  
---|---  
  
## FunctionsÂ¶

`is_symbolic_expr`(expr) | Check if the expression is a symbolic expression.  
---|---  
  
## Module ContentsÂ¶

tilelang.jit.adapter.cython.adapter.loggerÂ¶
    

tilelang.jit.adapter.cython.adapter.is_symbolic_expr(_expr_)Â¶
    

Check if the expression is a symbolic expression. A symbolic expression can be a simple tvm.Var, or an tvm.PrimExpr containing tvm.Var.

Return type:
    

[bool](../../../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool")

_class _tilelang.jit.adapter.cython.adapter.CythonKernelAdapter(_params_ , _result_idx_ , _target_ , _func_or_mod_ , _host_mod =None_, _device_mod =None_, _device_kernel_source =None_, _verbose =False_, _pass_configs =None_, _compile_flags =None_)Â¶
    

Bases: [`tilelang.jit.adapter.base.BaseKernelAdapter`](../../base/index.html#tilelang.jit.adapter.base.BaseKernelAdapter "tilelang.jit.adapter.base.BaseKernelAdapter")

Adapter class that converts TVM/TIR functions to callable CUDA kernels using cython.

This adapter handles: 1\. Converting TIR functions to compiled CUDA libraries 2\. Managing dynamic shapes in tensor operations 3\. Wrapping C++ kernels for Python/PyTorch usage

Parameters:
    

  * **params** (_list_ _[_[_tilelang.engine.param.KernelParam_](../../../../engine/param/index.html#tilelang.engine.param.KernelParam "tilelang.engine.param.KernelParam") _]_)

  * **result_idx** (_list_ _[__int_ _]_)

  * **target** (_str_ _|__tvm.target.Target_)

  * **func_or_mod** (_tvm.tir.PrimFunc_ _|__tilelang.tvm.IRModule_)

  * **host_mod** (_tilelang.tvm.IRModule_ _|__None_)

  * **device_mod** (_tilelang.tvm.IRModule_ _|__None_)

  * **device_kernel_source** (_str_ _|__None_)

  * **verbose** ([_bool_](../../../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool"))

  * **pass_configs** (_dict_ _[__str_ _,__Any_ _]__|__None_)

  * **compile_flags** (_list_ _[__str_ _]__|__None_)




target _: str | tvm.target.Target_ _ = 'cuda'_Â¶
    

ir_module _: tilelang.tvm.IRModule | None_ _ = None_Â¶
    

host_kernel_source _: str | None_ _ = None_Â¶
    

device_kernel_source _: str | None_ _ = None_Â¶
    

kernel_global_source _: str | None_ _ = None_Â¶
    

lib _: ctypes.CDLL | None_ _ = None_Â¶
    

dynamic_symbolic_map _: dict[tvm.tir.Var, tuple[int, int]] | None_ _ = None_Â¶
    

ptr_map _: dict[int, str] | None_ _ = None_Â¶
    

buffer_dtype_map _: dict[tvm.tir.Var, tuple[int, torch.dtype]] | None_ _ = None_Â¶
    

static_shape_map _: dict[tvm.tir.Var, tuple[int, list[tuple[int, int]]]] | None_ _ = None_Â¶
    

static_strides_map _: dict[tvm.tir.Var, tuple[int, list[tuple[int, int]]]] | None_ _ = None_Â¶
    

static_contiguous_list _: list[tvm.tir.Var] | None_ _ = None_Â¶
    

buffer_device_map _: dict[tvm.tir.Var, tuple[int, torch.device]] | None_ _ = None_Â¶
    

pass_configs _: dict[str, Any] | None_ _ = None_Â¶
    

paramsÂ¶
    

result_idxÂ¶
    

verbose _ = False_Â¶
    

wrapperÂ¶
    

lib_generatorÂ¶
    

cython_wrapperÂ¶
    

_classmethod _from_database(_params_ , _result_idx_ , _target_ , _func_or_mod_ , _host_kernel_source_ , _device_kernel_source_ , _kernel_lib_path_ , _verbose =False_, _pass_configs =None_, _compile_flags =None_)Â¶
    

Parameters:
    

  * **params** (_list_ _[__tvm.relax.TensorType_ _]_)

  * **result_idx** (_list_ _[__int_ _]_)

  * **target** (_str_)

  * **func_or_mod** (_tvm.tir.PrimFunc_ _|__tilelang.tvm.IRModule_)

  * **host_kernel_source** (_str_)

  * **device_kernel_source** (_str_)

  * **kernel_lib_path** (_str_)

  * **verbose** ([_bool_](../../../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool"))

  * **pass_configs** (_dict_ _[__str_ _,__Any_ _]__|__None_)

  * **compile_flags** (_list_ _[__str_ _]__|__None_)




_property _prim_func _: tvm.tir.PrimFunc_Â¶
    

Returns the primary TIR function from the IR module.

Return type:
    

tvm.tir.PrimFunc

_property _srcpathÂ¶
    

Returns the source path of the compiled library.

_property _libpathÂ¶
    

Returns the path to the compiled library.

_property _lib_codeÂ¶
    

Returns the code of the compiled library.

_property _is_dynamicÂ¶
    

Indicates whether the kernel handles dynamic shapes.

get_kernel_source(_kernel_only =False_)Â¶
    

Returns the source code of the compiled kernel.

Parameters:
    

**kernel_only** ([_bool_](../../../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool"))

get_host_source()Â¶
    

Returns the source code of the host function.
