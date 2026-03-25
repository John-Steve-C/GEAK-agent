# tilelang.autotuner.tunerÂ¶

The auto-tune module for tilelang programs.

This module provides functionality for auto-tuning tilelang programs, including JIT compilation and performance optimization through configuration search.

## AttributesÂ¶

`logger` |   
---|---  
  
## ExceptionsÂ¶

`TimeoutException` | Common base class for all non-exit exceptions.  
---|---  
  
## ClassesÂ¶

`AutoTuner` | Auto-tuner for tilelang programs.  
---|---  
`AutoTuneImpl` | Abstract base class for generic types.  
  
## FunctionsÂ¶

`timeout_handler`(signum, frame) |   
---|---  
`run_with_timeout`(func, timeout, *args, **kwargs) |   
`get_available_cpu_count`() | Gets the number of CPU cores available to the current process.  
`autotune`([func, warmup, rep, timeout, supply_type, ...]) | Just-In-Time (JIT) compiler decorator for TileLang functions.  
  
## Module ContentsÂ¶

_exception _tilelang.autotuner.tuner.TimeoutExceptionÂ¶
    

Bases: `Exception`

Common base class for all non-exit exceptions.

tilelang.autotuner.tuner.timeout_handler(_signum_ , _frame_)Â¶
    

tilelang.autotuner.tuner.run_with_timeout(_func_ , _timeout_ , _* args_, _** kwargs_)Â¶
    

tilelang.autotuner.tuner.loggerÂ¶
    

tilelang.autotuner.tuner.get_available_cpu_count()Â¶
    

Gets the number of CPU cores available to the current process.

Return type:
    

int

_class _tilelang.autotuner.tuner.AutoTuner(_fn_ , _configs_)Â¶
    

Auto-tuner for tilelang programs.

This class handles the auto-tuning process by testing different configurations and finding the optimal parameters for program execution.

Parameters:
    

  * **fn** (_Callable_) â The function to be auto-tuned.

  * **configs** â List of configurations to try during auto-tuning.




compile_argsÂ¶
    

profile_argsÂ¶
    

cache_dir _: pathlib.Path_Â¶
    

fnÂ¶
    

configsÂ¶
    

ref_latency_cache _ = None_Â¶
    

jit_input_tensors _ = None_Â¶
    

ref_input_tensors _ = None_Â¶
    

jit_compile _ = None_Â¶
    

_classmethod _from_kernel(_kernel_ , _configs_)Â¶
    

Create an AutoTuner instance from a kernel function.

Parameters:
    

  * **kernel** (_Callable_) â The kernel function to auto-tune.

  * **configs** â List of configurations to try.



Returns:
    

A new AutoTuner instance.

Return type:
    

AutoTuner

set_compile_args(_out_idx =None_, _target =None_, _execution_backend =None_, _target_host =None_, _verbose =None_, _pass_configs =None_)Â¶
    

Set compilation arguments for the auto-tuner.

Parameters:
    

  * **out_idx** (_list_ _[__int_ _]__|__int_ _|__None_) â List of output tensor indices.

  * **target** (_Literal_ _[__'auto'__,__'cuda'__,__'hip'__,__'metal'__]__|__None_) â Target platform. If None, reads from TILELANG_TARGET environment variable (defaults to âautoâ).

  * **execution_backend** (_Literal_ _[__'auto'__,__'tvm_ffi'__,__'cython'__,__'nvrtc'__,__'torch'__]__|__None_) â Execution backend to use for kernel execution. If None, reads from TILELANG_EXECUTION_BACKEND environment variable (defaults to âautoâ).

  * **target_host** (_str_ _|__tvm.target.Target_ _|__None_) â Target host for cross-compilation.

  * **verbose** ([_bool_](../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool") _|__None_) â Whether to enable verbose output. If None, reads from TILELANG_VERBOSE environment variable (defaults to False).

  * **pass_configs** (_dict_ _[__str_ _,__Any_ _]__|__None_) â Additional keyword arguments to pass to the Compiler PassContext.




Environment Variables:
    

TILELANG_TARGET: Default compilation target (e.g., âcudaâ, âllvmâ). Defaults to âautoâ. TILELANG_EXECUTION_BACKEND: Default execution backend. Defaults to âautoâ. TILELANG_VERBOSE: Set to â1â, âtrueâ, âyesâ, or âonâ to enable verbose compilation by default.

Returns:
    

Self for method chaining.

Return type:
    

AutoTuner

Parameters:
    

  * **out_idx** (_list_ _[__int_ _]__|__int_ _|__None_)

  * **target** (_Literal_ _[__'auto'__,__'cuda'__,__'hip'__,__'metal'__]__|__None_)

  * **execution_backend** (_Literal_ _[__'auto'__,__'tvm_ffi'__,__'cython'__,__'nvrtc'__,__'torch'__]__|__None_)

  * **target_host** (_str_ _|__tvm.target.Target_ _|__None_)

  * **verbose** ([_bool_](../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool") _|__None_)

  * **pass_configs** (_dict_ _[__str_ _,__Any_ _]__|__None_)




set_profile_args(_warmup =25_, _rep =100_, _timeout =30_, _supply_type =tilelang.TensorSupplyType.Auto_, _ref_prog =None_, _supply_prog =None_, _rtol =0.01_, _atol =0.01_, _max_mismatched_ratio =0.01_, _skip_check =False_, _manual_check_prog =None_, _cache_input_tensors =False_, _backend ='event'_)Â¶
    

Set profiling arguments for the auto-tuner.

Parameters:
    

  * **supply_type** (_tilelang.TensorSupplyType_) â Type of tensor supply mechanism. Ignored if supply_prog is provided.

  * **ref_prog** (_Callable_) â Reference program for validation.

  * **supply_prog** (_Callable_) â Supply program for input tensors.

  * **rtol** (_float_) â Relative tolerance for validation.

  * **atol** (_float_) â Absolute tolerance for validation.

  * **max_mismatched_ratio** (_float_) â Maximum allowed mismatch ratio.

  * **skip_check** ([_bool_](../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool")) â Whether to skip validation.

  * **manual_check_prog** (_Callable_) â Manual check program for validation.

  * **cache_input_tensors** ([_bool_](../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool")) â Whether to cache input tensors.

  * **warmup** (_int_) â Number of warmup iterations.

  * **rep** (_int_) â Number of repetitions for timing.

  * **timeout** (_int_) â Maximum time per configuration.

  * **backend** (_Literal_ _[__'event'__,__'cupti'__,__'cudagraph'__]_) â Profiler backend - âeventâ (CUDA events), âcuptiâ, or âcudagraphâ.



Returns:
    

Self for method chaining.

Return type:
    

AutoTuner

set_kernel_parameters(_k_parameters_ , _f_parameters_)Â¶
    

Parameters:
    

  * **k_parameters** (_tuple_ _[__str_ _,__Ellipsis_ _]_)

  * **f_parameters** (_dict_ _[__str_ _,__Any_ _]_)




generate_cache_key(_parameters_ , _extra_parameters_)Â¶
    

Generate a cache key for the auto-tuning process.

Parameters:
    

  * **parameters** (_dict_ _[__str_ _,__Any_ _]_)

  * **extra_parameters** (_dict_ _[__str_ _,__Any_ _]_)



Return type:
    

[tilelang.autotuner.param.AutotuneResult](../param/index.html#tilelang.autotuner.param.AutotuneResult "tilelang.autotuner.param.AutotuneResult") | None

run(_warmup =25_, _rep =100_, _timeout =30_)Â¶
    

Run the auto-tuning process.

Parameters:
    

  * **warmup** (_int_) â Number of warmup iterations.

  * **rep** (_int_) â Number of repetitions for timing.

  * **timeout** (_int_) â Maximum time per configuration.



Returns:
    

Results of the auto-tuning process.

Return type:
    

[AutotuneResult](../param/index.html#tilelang.autotuner.param.AutotuneResult "tilelang.autotuner.param.AutotuneResult")

__call__()Â¶
    

Make the AutoTuner callable, running the auto-tuning process.

Returns:
    

Results of the auto-tuning process.

Return type:
    

[AutotuneResult](../param/index.html#tilelang.autotuner.param.AutotuneResult "tilelang.autotuner.param.AutotuneResult")

_class _tilelang.autotuner.tuner.AutoTuneImplÂ¶
    

Bases: `Generic`[`_P`, `_T`]

Abstract base class for generic types.

A generic type is typically declared by inheriting from this class parameterized with one or more type variables. For example, a generic mapping type might be defined as:
    
    
    class Mapping(Generic[KT, VT]):
        def __getitem__(self, key: KT) -> VT:
            ...
        # Etc.
    

This class can then be used as follows:
    
    
    def lookup_name(mapping: Mapping[KT, VT], key: KT, default: VT) -> VT:
        try:
            return mapping[key]
        except KeyError:
            return default
    

jit_impl _: [tilelang.jit.JITImpl](../../jit/index.html#tilelang.jit.JITImpl "tilelang.jit.JITImpl")_Â¶
    

warmup _: int_ _ = 25_Â¶
    

rep _: int_ _ = 100_Â¶
    

timeout _: int_ _ = 100_Â¶
    

configs _: dict | Callable_ _ = None_Â¶
    

supply_type _: tilelang.TensorSupplyType_Â¶
    

ref_prog _: Callable_ _ = None_Â¶
    

supply_prog _: Callable_ _ = None_Â¶
    

rtol _: float_ _ = 0.01_Â¶
    

atol _: float_ _ = 0.01_Â¶
    

max_mismatched_ratio _: float_ _ = 0.01_Â¶
    

skip_check _: [bool](../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool")_ _ = False_Â¶
    

manual_check_prog _: Callable_ _ = None_Â¶
    

cache_input_tensors _: [bool](../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool")_ _ = False_Â¶
    

__post_init__()Â¶
    

get_tunner()Â¶
    

__call__(_* args_, _** kwargs_)Â¶
    

Parameters:
    

  * **args** (__P_)

  * **kwargs** (__P_)



Return type:
    

[tilelang.jit.kernel.JITKernel](../../jit/kernel/index.html#tilelang.jit.kernel.JITKernel "tilelang.jit.kernel.JITKernel")

tilelang.autotuner.tuner.autotune(_func =None_, _*_ , _configs_ , _warmup =25_, _rep =100_, _timeout =100_, _supply_type =tilelang.TensorSupplyType.Auto_, _ref_prog =None_, _supply_prog =None_, _rtol =0.01_, _atol =0.01_, _max_mismatched_ratio =0.01_, _skip_check =False_, _manual_check_prog =None_, _cache_input_tensors =False_)Â¶
    

Just-In-Time (JIT) compiler decorator for TileLang functions.

This decorator can be used without arguments (e.g., @tilelang.jit):
    

Applies JIT compilation with default settings.

Tips:
    

  * If you want to skip the auto-tuning process, you can set override the tunable parameters in the function signature.
    

```python
    

if enable_autotune:
    

kernel = flashattn(batch, heads, seq_len, dim, is_causal)

else:
    

kernel = flashattn(
    

batch, heads, seq_len, dim, is_causal, groups=groups, block_M=128, block_N=128, num_stages=2, threads=256)

```




Parameters:
    

  * **func_or_out_idx** (_Any_ _,__optional_) â If using @tilelang.jit(â¦) to configure, this is the out_idx parameter. If using @tilelang.jit directly on a function, this argument is implicitly the function to be decorated (and out_idx will be None).

  * **configs** (_Dict_ _or_ _Callable_) â Configuration space to explore during auto-tuning.

  * **warmup** (_int_ _,__optional_) â Number of warmup iterations before timing.

  * **rep** (_int_ _,__optional_) â Number of repetitions for timing measurements.

  * **timeout** (_int_ _,__optional_)

  * **target** (_Union_ _[__str_ _,__Target_ _]__,__optional_) â Compilation target for TVM (e.g., âcudaâ, âllvmâ). Defaults to âautoâ.

  * **target_host** (_Union_ _[__str_ _,__Target_ _]__,__optional_) â Target host for cross-compilation. Defaults to None.

  * **execution_backend** (_Literal_ _[__"auto"__,__"tvm_ffi"__,__"cython"__,__"nvrtc"__,__"torch"__]__,__optional_) â Backend for kernel execution and argument passing. Use âautoâ to pick a sensible default per target (cuda->tvm_ffi, metal->torch, others->cython).

  * **verbose** ([_bool_](../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool") _,__optional_) â Enables verbose logging during compilation. Defaults to False.

  * **pass_configs** (_Optional_ _[__Dict_ _[__str_ _,__Any_ _]__]__,__optional_) â Configurations for TVMâs pass context. Defaults to None.

  * **debug_root_path** (_Optional_ _[__str_ _]__,__optional_) â Directory to save compiled kernel source for debugging. Defaults to None.

  * **func** (_Callable_ _[___P_ _,___T_ _]__|__tvm.tir.PrimFunc_ _|__None_)

  * **supply_type** (_tilelang.TensorSupplyType_)

  * **ref_prog** (_Callable_)

  * **supply_prog** (_Callable_)

  * **rtol** (_float_)

  * **atol** (_float_)

  * **max_mismatched_ratio** (_float_)

  * **skip_check** ([_bool_](../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool"))

  * **manual_check_prog** (_Callable_)

  * **cache_input_tensors** ([_bool_](../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool"))



Returns:
    

Either a JIT-compiled wrapper around the input function, or a configured decorator instance that can then be applied to a function.

Return type:
    

Callable
