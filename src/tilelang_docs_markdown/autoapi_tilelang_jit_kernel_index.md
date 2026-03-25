# tilelang.jit.kernelÂ¶

## AttributesÂ¶

`logger` |   
---|---  
  
## ClassesÂ¶

`JITKernel` | A wrapper class for compiling and invoking TileLang (TVM TIR) functions as PyTorch-compatible functions.  
---|---  
  
## Module ContentsÂ¶

tilelang.jit.kernel.loggerÂ¶
    

_class _tilelang.jit.kernel.JITKernel(_func =None_, _out_idx =None_, _execution_backend ='tvm_ffi'_, _target ='auto'_, _target_host =None_, _verbose =False_, _pass_configs =None_, _from_database =False_, _compile_flags =None_)Â¶
    

Bases: `Generic`[`_P`, `_T`]

A wrapper class for compiling and invoking TileLang (TVM TIR) functions as PyTorch-compatible functions.

Parameters:
    

  * **func** (_tvm.tir.PrimFunc_)

  * **out_idx** (_list_ _[__int_ _]__|__int_)

  * **execution_backend** (_Literal_ _[__'tvm_ffi'__,__'cython'__,__'nvrtc'__,__'torch'__,__'cutedsl'__]_)

  * **target** (_str_ _|__tvm.target.Target_)

  * **target_host** (_str_ _|__tvm.target.Target_)

  * **verbose** ([_bool_](../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool"))

  * **pass_configs** (_dict_ _[__str_ _,__Any_ _]__|__None_)

  * **from_database** ([_bool_](../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool"))

  * **compile_flags** (_list_ _[__str_ _]__|__None_)




artifactÂ¶
    

The compiled artifact containing the runtime module and parameters.

Type:
    

[CompiledArtifact](../../engine/param/index.html#tilelang.engine.param.CompiledArtifact "tilelang.engine.param.CompiledArtifact")

adapterÂ¶
    

The adapter for the compiled function.

Type:
    

[BaseKernelAdapter](../adapter/base/index.html#tilelang.jit.adapter.base.BaseKernelAdapter "tilelang.jit.adapter.base.BaseKernelAdapter")

torch_functionÂ¶
    

The compiled function that can be invoked as a PyTorch-compatible function.

Type:
    

Callable

prim_func _: tvm.tir.PrimFunc_ _ = None_Â¶
    

artifact _: [tilelang.engine.param.CompiledArtifact](../../engine/param/index.html#tilelang.engine.param.CompiledArtifact "tilelang.engine.param.CompiledArtifact")_ _ = None_Â¶
    

adapter _: tilelang.jit.adapter.BaseKernelAdapter_ _ = None_Â¶
    

torch_function _: Callable_ _ = None_Â¶
    

latency _: float_ _ = None_Â¶
    

config _: dict[str, Any]__ = None_Â¶
    

ref_latency _: float_ _ = None_Â¶
    

execution_backend _ = 'tvm_ffi'_Â¶
    

target_host _ = None_Â¶
    

verbose _ = False_Â¶
    

pass_configs _ = None_Â¶
    

compile_flagsÂ¶
    

targetÂ¶
    

_classmethod _from_database(_func_ , _host_kernel_source_ , _device_kernel_source_ , _kernel_lib_path_ , _params_ , _target_ , _target_host_ , _out_idx_ , _execution_backend_ , _pass_configs =None_, _compile_flags =None_)Â¶
    

Alternative constructor to create a TorchFunction directly from a database.

Parameters:
    

  * **func** (_tvm.tir.PrimFunc_)

  * **host_kernel_source** (_str_)

  * **device_kernel_source** (_str_)

  * **kernel_lib_path** (_str_)

  * **params** (_list_ _[_[_tilelang.engine.param.KernelParam_](../../engine/param/index.html#tilelang.engine.param.KernelParam "tilelang.engine.param.KernelParam") _]_)

  * **target** (_str_ _|__tvm.target.Target_)

  * **target_host** (_str_ _|__tvm.target.Target_)

  * **out_idx** (_list_ _[__int_ _]__|__int_)

  * **execution_backend** (_Literal_ _[__'tvm_ffi'__,__'cython'__,__'nvrtc'__,__'torch'__]_)

  * **pass_configs** (_dict_ _[__str_ _,__Any_ _]__|__None_)

  * **compile_flags** (_list_ _[__str_ _]__|__None_)




__call__(_* args_, _** kwds_)Â¶
    

Invokes the compiled function with the given arguments.

Parameters:
    

  * ***args** (_Any_) â Positional arguments for the function.

  * ****kwds** (_Any_) â Keyword arguments for the function.



Returns:
    

The result of the function execution.

Return type:
    

Any

_classmethod _from_tilelang_function(_tilelang_func_ , _** kwargs_)Â¶
    

Alternative constructor to create a TorchFunction directly from a TileLang PrimFunc.

Parameters:
    

  * **tilelang_func** (_tvm.tir.PrimFunc_) â The TileLang (TVM TIR) function to compile.

  * ****kwargs** (_dict_) â Additional keyword arguments to pass to the constructor.



Returns:
    

An instance of TorchFunction wrapping the compiled function.

Return type:
    

TorchFunction

get_profiler(_tensor_supply_type =TensorSupplyType.Auto_)Â¶
    

Creates a profiler to benchmark the compiled runtime module.

Parameters:
    

**tensor_supply_type** ([_TensorSupplyType_](../../utils/tensor/index.html#tilelang.utils.tensor.TensorSupplyType "tilelang.utils.tensor.TensorSupplyType") _,__optional_) â The type of input tensors to supply for profiling (default: TensorSupplyType.Auto).

Returns:
    

A Profiler instance for benchmarking the runtime module.

Return type:
    

[Profiler](../../profiler/index.html#tilelang.profiler.Profiler "tilelang.profiler.Profiler")

get_kernel_source(_kernel_only =True_)Â¶
    

Returns the source code of the compiled kernel function.

Returns:
    

The source code of the compiled kernel function.

Return type:
    

str

Parameters:
    

**kernel_only** ([_bool_](../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool"))

get_host_source()Â¶
    

Returns the source code of the host function.

Return type:
    

str

run_once(_func =None_)Â¶
    

Parameters:
    

**func** (_Callable_ _|__None_)

Return type:
    

None

show_source(_which ='kernel'_)Â¶
    

Print generated source code to stdout.

Parameters:
    

**which** (_Literal_ _[__"kernel"__,__"host"__,__"both"__]__,__optional_) â Select which source to print. Defaults to âkernelâ.

Return type:
    

None

Examples
    
    
    >>> jit_kernel.show_source()            # print kernel source
    >>> jit_kernel.show_source("host")      # print host source
    >>> jit_kernel.show_source("both")      # print both sources
    

export_sources(_kernel_path =None_, _host_path =None_)Â¶
    

Export generated source code to files.

Parameters:
    

  * **kernel_path** (_Optional_ _[__str_ _]_) â Destination file path to write the kernel source. If None, skips writing kernel code.

  * **host_path** (_Optional_ _[__str_ _]_) â Destination file path to write the host source. If None, skips writing host code.



Return type:
    

None

Examples
    
    
    >>> jit_kernel.export_sources(kernel_path="/tmp/kernel.cu")
    >>> jit_kernel.export_sources(host_path="/tmp/host.cc")
    >>> jit_kernel.export_sources(
    ...     kernel_path="/tmp/kernel.cu",
    ...     host_path="/tmp/host.cc",
    ... )
    

print_source_code(_which ='kernel'_, _file =None_)Â¶
    

Deprecated: use show_source() or export_sources() instead.

Parameters:
    

  * **which** (_Literal_ _[__"kernel"__,__"host"__,__"both"__]__,__optional_) â Kept for backward compatibility with printing behavior.

  * **file** (_Optional_ _[__str_ _]_) â If provided, behaves like export_sources(kernel_path=file).



Return type:
    

None

Examples
    
    
    >>> # New API (preferred)
    >>> jit_kernel.show_source("both")
    >>> jit_kernel.export_sources(kernel_path="/tmp/kernel.cu")
    
    
    
    >>> # Old API (still works but deprecated)
    >>> jit_kernel.print_source_code(file="/tmp/kernel.cu")
    

update_tuner_result(_latency_ , _config_ , _ref_latency_)Â¶
    

Updates the tuning results for this kernel.

Parameters:
    

  * **latency** (_float_) â The measured latency of this kernel configuration.

  * **config** (_Dict_ _[__str_ _,__Any_ _]_) â The configuration parameters used for this kernel.

  * **ref_latency** (_float_) â The reference latency to compare against.



Return type:
    

None

get_tuner_result()Â¶
    

Gets the tuning results for this kernel.

Returns:
    

A dictionary containing: \- latency: The measured latency of this kernel \- config: The configuration parameters used \- ref_latency: The reference latency for comparison

Return type:
    

Dict[str, Any]

_property _out_idx _: list[int]_Â¶
    

Return type:
    

list[int]

_property _params _: list[[tilelang.engine.param.KernelParam](../../engine/param/index.html#tilelang.engine.param.KernelParam "tilelang.engine.param.KernelParam")]_Â¶
    

Return type:
    

list[[tilelang.engine.param.KernelParam](../../engine/param/index.html#tilelang.engine.param.KernelParam "tilelang.engine.param.KernelParam")]

_property _kernel_source _: str_Â¶
    

Return type:
    

str

_property _host_source _: str_Â¶
    

Return type:
    

str

export_library(_kernel_file_)Â¶
    

Exports the compiled kernel function to a shared library file.

Parameters:
    

**kernel_file** (_str_) â The path to the shared library file to create.

Return type:
    

None

show_ptx()Â¶
    

Print compiled PTX for the kernel (CUDA only).

Examples
    
    
    >>> jit_kernel.show_ptx()
    

Return type:
    

None

export_ptx(_path_)Â¶
    

Export compiled PTX to a file (CUDA only).

Parameters:
    

**path** (_str_) â Destination file path to write PTX.

Return type:
    

None

Examples
    
    
    >>> jit_kernel.export_ptx("/tmp/kernel.ptx")
    

show_sass()Â¶
    

Print disassembled SASS for the kernel (CUDA only).

Examples
    
    
    >>> jit_kernel.show_sass()
    

Return type:
    

None

export_sass(_path_)Â¶
    

Export disassembled SASS to a file (CUDA only).

Parameters:
    

**path** (_str_) â Destination file path to write SASS.

Return type:
    

None

Examples
    
    
    >>> jit_kernel.export_sass("/tmp/kernel.sass")
    
