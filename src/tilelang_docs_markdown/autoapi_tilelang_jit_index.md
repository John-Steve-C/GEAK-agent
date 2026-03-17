# tilelang.jitÂ¶

This module provides an auto-tuning infrastructure for TileLang (tl) programs. It includes functionality to JIT-compile TileLang programs into a runnable kernel adapter using TVM.

## SubmodulesÂ¶

  * [tilelang.jit.adapter](adapter/index.html)
  * [tilelang.jit.env](env/index.html)
  * [tilelang.jit.exceptions](exceptions/index.html)
  * [tilelang.jit.execution_backend](execution_backend/index.html)
  * [tilelang.jit.kernel](kernel/index.html)
  * [tilelang.jit.param](param/index.html)



## AttributesÂ¶

`logger` |   
---|---  
`ExecutionBackend` |   
  
## ClassesÂ¶

`JITImpl` | Just-In-Time compilation wrapper for TileLang programs.  
---|---  
  
## FunctionsÂ¶

`compile`([func, out_idx, execution_backend, target, ...]) | Compile the given TileLang PrimFunc with TVM and build a JITKernel.  
---|---  
`par_compile`(funcs[, out_idx, execution_backend, ...]) | Parallel compile multiple TileLang PrimFunc with TVM and build JITKernels.  
`jit`(â¦) | JIT compiler decorator for TileLang functions.  
  
## Package ContentsÂ¶

tilelang.jit.loggerÂ¶
    

tilelang.jit.compile(_func =None_, _out_idx =None_, _execution_backend =None_, _target =None_, _target_host =None_, _verbose =None_, _pass_configs =None_, _compile_flags =None_)Â¶
    

Compile the given TileLang PrimFunc with TVM and build a JITKernel.

Parameters:
    

  * **func** (_tvm.tir.PrimFunc_ _,__optional_) â The TileLang TIR function to compile and wrap.

  * **out_idx** (_Union_ _[__List_ _[__int_ _]__,__int_ _]__,__optional_) â Index(es) of the output tensors to return (default: None).

  * **execution_backend** (_Literal_ _[__"auto"__,__"dlpack"__,__"tvm_ffi"__,__"cython"__,__"nvrtc"__,__"torch"__,__"cutedsl"__]__,__optional_) â Execution backend to use for kernel execution. If None, reads from TILELANG_EXECUTION_BACKEND environment variable (defaults to âautoâ).

  * **target** (_Union_ _[__str_ _,__Target_ _]__,__optional_) â Compilation target, either as a string or a TVM Target object. If None, reads from TILELANG_TARGET environment variable (defaults to âautoâ).

  * **target_host** (_Union_ _[__str_ _,__Target_ _]__,__optional_) â Target host for cross-compilation (default: None).

  * **verbose** ([_bool_](../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool") _,__optional_) â Whether to enable verbose output. If None, reads from TILELANG_VERBOSE environment variable (defaults to False).

  * **pass_configs** (_dict_ _,__optional_) â Additional keyword arguments to pass to the Compiler PassContext. Refer to tilelang.transform.PassConfigKey for supported options.

  * **Variables** ([_Environment_](../env/index.html#tilelang.env.Environment "tilelang.env.Environment"))

  * **\---------------------**

  * **TILELANG_TARGET** (_str_) â Default compilation target (e.g., âcudaâ, âllvmâ). Defaults to âautoâ.

  * **TILELANG_EXECUTION_BACKEND** (_str_) â Default execution backend. Defaults to âautoâ.

  * **TILELANG_VERBOSE** (_str_) â Set to â1â, âtrueâ, âyesâ, or âonâ to enable verbose compilation by default.

  * **compile_flags** (_list_ _[__str_ _]__|__str_ _|__None_)



Return type:
    

[kernel.JITKernel](kernel/index.html#tilelang.jit.kernel.JITKernel "tilelang.jit.kernel.JITKernel")[_KP, _T]

tilelang.jit.par_compile(_funcs_ , _out_idx =None_, _execution_backend =None_, _target =None_, _target_host =None_, _verbose =None_, _pass_configs =None_, _compile_flags =None_, _num_workers =None_, _ignore_error =False_)Â¶
    

Parallel compile multiple TileLang PrimFunc with TVM and build JITKernels.

Parameters:
    

  * **funcs** (_Iterable_ _[__tvm.tir.PrimFunc_ _]_) â The TileLang TIR functions to compile and wrap.

  * **out_idx** (_Union_ _[__List_ _[__int_ _]__,__int_ _]__,__optional_) â Index(es) of the output tensors to return (default: None).

  * **execution_backend** (_Literal_ _[__"auto"__,__"dlpack"__,__"tvm_ffi"__,__"cython"__,__"nvrtc"__,__"torch"__,__"cutedsl"__]__,__optional_) â Execution backend to use for kernel execution. If None, reads from TILELANG_EXECUTION_BACKEND environment variable (defaults to âautoâ).

  * **target** (_Union_ _[__str_ _,__Target_ _]__,__optional_) â Compilation target, either as a string or a TVM Target object. If None, reads from TILELANG_TARGET environment variable (defaults to âautoâ).

  * **target_host** (_Union_ _[__str_ _,__Target_ _]__,__optional_) â Target host for cross-compilation (default: None).

  * **verbose** ([_bool_](../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool") _,__optional_) â Whether to enable verbose output. If None, reads from TILELANG_VERBOSE environment variable (defaults to False).

  * **pass_configs** (_dict_ _,__optional_) â Additional keyword arguments to pass to the Compiler PassContext. Refer to tilelang.transform.PassConfigKey for supported options.

  * **Variables** ([_Environment_](../env/index.html#tilelang.env.Environment "tilelang.env.Environment"))

  * **\---------------------**

  * **TILELANG_TARGET** (_str_) â Default compilation target (e.g., âcudaâ, âllvmâ). Defaults to âautoâ.

  * **TILELANG_EXECUTION_BACKEND** (_str_) â Default execution backend. Defaults to âautoâ.

  * **TILELANG_VERBOSE** (_str_) â Set to â1â, âtrueâ, âyesâ, or âonâ to enable verbose compilation by default.

  * **compile_flags** (_list_ _[__str_ _]__|__str_ _|__None_)

  * **num_workers** (_int_ _|__None_)

  * **ignore_error** ([_bool_](../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool"))



Return type:
    

list[[kernel.JITKernel](kernel/index.html#tilelang.jit.kernel.JITKernel "tilelang.jit.kernel.JITKernel")[_KP, _T]]

_class _tilelang.jit.JITImplÂ¶
    

Bases: `Generic`[`_P`, `_KP`, `_T`, `_Ret`]

Just-In-Time compilation wrapper for TileLang programs.

This class provides a unified interface for compiling and executing TileLang kernels. It supports two execution modes that are automatically inferred:

### Execution ModesÂ¶

  * **lazy** : The decorated function returns a PrimFunc explicitly. Calling the JIT wrapper returns a compiled kernel object, which can be invoked separately. This mode is useful when you want to inspect or reuse the kernel object.

Example (lazy mode):
        
        @tilelang.jit(out_idx=[-1])
        def matmul(M, N, K, block_M, block_N, block_K):
            @T.prim_func
            def kernel(A: T.Tensor((M, K), dtype), ...):
                ...
            return kernel  # explicitly return PrimFunc
        
        kernel = matmul(1024, 1024, 1024, 128, 128, 32)  # returns kernel
        result = kernel(a, b)  # execute separately
        

  * **eager** : The decorated function uses the DSL builder pattern with tensor type annotations. Calling the JIT wrapper compiles and immediately executes the kernel, returning the result directly.

Example (eager mode):
        
        @tilelang.jit
        def gemm(A, B, C, block_M: int = 64):
            M, N, K = T.const("M N K")
            A: T.Tensor[[M, K], dtype]  # tensor shape via annotation
            B: T.Tensor[[K, N], dtype]
            C: T.Tensor[[M, N], dtype]
            with T.Kernel(...):
                ...
        
        gemm(A, B, C)  # compiles and executes immediately
        




The mode is automatically inferred based on whether the function returns a PrimFunc (lazy) or uses the builder pattern (eager).

out_idxÂ¶
    

Index(es) of output tensor(s) to return (lazy mode only).

Type:
    

list[int] | int | None

execution_backendÂ¶
    

Backend for kernel execution (âautoâ, âdlpackâ, âtvm_ffiâ, etc.).

Type:
    

str | None

targetÂ¶
    

TVM compilation target (e.g., âcudaâ, âllvmâ, âautoâ).

Type:
    

str | Target | None

target_hostÂ¶
    

Host target for cross-compilation.

Type:
    

str | Target | None

verboseÂ¶
    

Enable verbose compilation output.

Type:
    

[bool](../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool") | None

pass_configsÂ¶
    

TVM pass configuration options.

Type:
    

dict[str, Any] | None

debug_root_pathÂ¶
    

Directory to save compiled kernel source for debugging.

Type:
    

str | None

compile_flagsÂ¶
    

Additional compiler flags.

Type:
    

list[str] | str | None

func_sourceÂ¶
    

Original Python source code of the decorated function.

Type:
    

str

signatureÂ¶
    

Function signature of the original function.

Type:
    

inspect.Signature

modeÂ¶
    

Execution mode. âautoâ infers from function behavior.

Type:
    

Literal[âautoâ, âlazyâ, âeagerâ]

funcÂ¶
    

The wrapped function object.

Type:
    

[JITFunc](../language/eager/builder/index.html#tilelang.language.eager.builder.JITFunc "tilelang.language.eager.builder.JITFunc")

out_idx _: list[int] | int | None_Â¶
    

execution_backend _: Literal['auto', 'dlpack', 'tvm_ffi', 'cython', 'nvrtc', 'torch', 'cutedsl'] | None_Â¶
    

target _: str | tvm.target.Target | None_Â¶
    

target_host _: str | tvm.target.Target | None_Â¶
    

verbose _: [bool](../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool") | None_Â¶
    

pass_configs _: dict[str, Any] | None_Â¶
    

debug_root_path _: str | None_Â¶
    

compile_flags _: list[str] | str | None_Â¶
    

func_source _: str_Â¶
    

signature _: inspect.Signature_Â¶
    

mode _: Literal['auto', 'lazy', 'eager']_Â¶
    

func _: tilelang.language.eager.JITFunc[_KP, _T]_Â¶
    

__post_init__()Â¶
    

get_tir(_* args_, _** kwargs_)Â¶
    

Retrieve a TIR (Tensor Intermediate Representation) PrimFunc from the stored callable or object.

Parameters:
    

  * **args** (__P_)

  * **kwargs** (__P_)



Return type:
    

tilelang.language.eager.PrimFunc[_KP, _T]

initialize_jit_mode(_* args_, _** kwargs_)Â¶
    

Parameters:
    

  * **args** (__P_)

  * **kwargs** (__P_)



Return type:
    

Literal[âlazyâ, âeagerâ]

par_compile(_configs_ , _num_workers =None_, _ignore_error =False_)Â¶
    

Parallel compile multiple TileLang PrimFunc with TVM and build JITKernels. :param configs: The configurations to elaborate and compile. Each config can be either

> a dictionary mapping keyword arguments to values, or a tuple of positional arguments.

Parameters:
    

  * **num_workers** (_int_ _,__optional_) â Number of parallel workers to use for compilation. Defaults to None, which lets the system decide.

  * **ignore_error** ([_bool_](../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool") _,__optional_) â If True, compilation errors for individual configs will be logged as warnings and the corresponding result will be None. If False, any compilation error will raise an exception. Defaults to False.

  * **configs** (_Iterable_ _[__Union_ _[__dict_ _[__str_ _,__Any_ _]__,__tuple_ _[__Any_ _,__...__]__]__]_)



Returns:
    

A list of compiled JITKernel objects corresponding to the provided configs.

Return type:
    

List[[JITKernel](kernel/index.html#tilelang.jit.kernel.JITKernel "tilelang.jit.kernel.JITKernel")]

compile(_* args_, _** kwargs_)Â¶
    

Parameters:
    

  * **args** (__P_)

  * **kwargs** (__P_)



Return type:
    

_Ret

parse_cache_key(_* args_, _** kwargs_)Â¶
    

Parameters:
    

  * **args** (__P_)

  * **kwargs** (__P_)




get_kernel_source(_* args_, _** kwargs_)Â¶
    

Parameters:
    

  * **args** (__P_)

  * **kwargs** (__P_)



Return type:
    

str

__call__(_* args_, _** kwargs_)Â¶
    

Parameters:
    

  * **args** (__P_)

  * **kwargs** (__P_)



Return type:
    

_Ret

tilelang.jit.ExecutionBackendÂ¶
    

tilelang.jit.jit(_func : Callable[_KP, _T]_) → JITImpl[_KP, _KP, _T, _T]Â¶
tilelang.jit.jit(_*_ , _out_idx : Any = None_, _target : str | tvm.target.Target | None = None_, _target_host : str | tvm.target.Target | None = None_, _execution_backend : ExecutionBackend | None = None_, _verbose : [bool](../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool") | None = None_, _pass_configs : dict[str, Any] | None = None_, _debug_root_path : str | None = None_, _compile_flags : list[str] | str | None = None_) → Callable[[Callable[_KP, _T]], JITImpl[_KP, _KP, _T, _T]]
    

JIT compiler decorator for TileLang functions.

Supports two execution modes (automatically inferred): \- **lazy** : Function returns PrimFunc explicitly. Returns compiled kernel object. \- **eager** : Function uses DSL builder pattern. Executes kernel immediately.

Parameters:
    

  * **out_idx** (_list_ _[__int_ _]__|__int_ _|__None_) â Output tensor index(es). Only supported in lazy mode.

  * **target** (_str_ _|__Target_ _|__None_) â TVM compilation target (e.g., âcudaâ, âllvmâ, âautoâ).

  * **target_host** (_str_ _|__Target_ _|__None_) â Host target for cross-compilation.

  * **execution_backend** (_ExecutionBackend_ _|__None_) â Backend for kernel execution.

  * **verbose** ([_bool_](../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool") _|__None_) â Enable verbose compilation output.

  * **pass_configs** (_dict_ _[__str_ _,__Any_ _]__|__None_) â TVM pass configuration options.

  * **debug_root_path** (_str_ _|__None_) â Directory to save compiled kernel source for debugging.

  * **compile_flags** (_list_ _[__str_ _]__|__str_ _|__None_) â Additional compiler flags.



