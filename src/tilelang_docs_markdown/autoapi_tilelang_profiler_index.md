# tilelang.profilerÂ¶

The profiler and convert to torch utils

## SubmodulesÂ¶

  * [tilelang.profiler.bench](bench/index.html)



## ClassesÂ¶

`Profiler` | A profiler class for benchmarking and validating kernel implementations.  
---|---  
  
## Package ContentsÂ¶

_class _tilelang.profiler.ProfilerÂ¶
    

A profiler class for benchmarking and validating kernel implementations.

paramsÂ¶
    

List of kernel parameters defining the input/output specifications

result_idxÂ¶
    

Indices indicating which parameters are output tensors

supply_typeÂ¶
    

Type of tensor supply to use (e.g., random, zeros, etc.)

adapterÂ¶
    

Optional kernel adapter for interfacing with different backends

params _: list[[tilelang.engine.param.KernelParam](../engine/param/index.html#tilelang.engine.param.KernelParam "tilelang.engine.param.KernelParam")]_Â¶
    

result_idx _: list[int]_Â¶
    

supply_type _: [tilelang.utils.tensor.TensorSupplyType](../utils/tensor/index.html#tilelang.utils.tensor.TensorSupplyType "tilelang.utils.tensor.TensorSupplyType")_Â¶
    

adapter _: tilelang.jit.adapter.BaseKernelAdapter | None_ _ = None_Â¶
    

__post_init__()Â¶
    

Initialize tensor supply after dataclass initialization

with_default_adapter(_adapter_)Â¶
    

Parameters:
    

**adapter** (_tilelang.jit.adapter.BaseKernelAdapter_)

Return type:
    

Profiler

assert_allclose(_reference_program_ , _input_tensors =None_, _atol =0.01_, _rtol =0.01_, _max_mismatched_ratio =0.01_)Â¶
    

Validates kernel output against a reference implementation.

Parameters:
    

  * **reference_program** (_Callable_) â Reference implementation to compare against

  * **input_tensors** (_list_ _[__torch.Tensor_ _]__|__None_) â Optional pre-generated input tensors

  * **atol** (_float_) â Absolute tolerance for comparison

  * **rtol** (_float_) â Relative tolerance for comparison

  * **max_mismatched_ratio** â Maximum allowed ratio of mismatched elements




manual_assert_close(_reference_program_ , _input_tensors =None_, _manual_check_prog =None_)Â¶
    

Validates kernel output against a reference implementation.

Parameters:
    

  * **reference_program** (_Callable_) â Reference implementation to compare against

  * **input_tensors** (_list_ _[__torch.Tensor_ _]__|__None_) â Optional pre-generated input tensors

  * **atol** â Absolute tolerance for comparison

  * **rtol** â Relative tolerance for comparison

  * **max_mismatched_ratio** â Maximum allowed ratio of mismatched elements

  * **manual_check_prog** (_Callable_)




assert_consistent(_repeat =10_)Â¶
    

Checks for kernel consistency across multiple runs.

Parameters:
    

**repeat** â Number of times to repeat the consistency check

run_once(_func =None_)Â¶
    

Parameters:
    

**func** (_Callable_ _|__None_)

do_bench(_func =None_, _warmup =25_, _rep =100_, _n_warmup =0_, _n_repeat =0_, _input_tensors =None_, _backend ='event'_, _quantiles =None_, _return_mode ='mean'_, _dynamic_symbolic_constraints =None_)Â¶
    

Benchmarks the execution time of a given function.

Parameters:
    

  * **func** (_Callable_ _|__None_) â Function to benchmark (uses adapter if None)

  * **warmup** (_int_) â Warmup time in milliseconds

  * **rep** (_int_) â Number of repetitions for timing

  * **n_warmup** (_int_) â Number of warmup iterations

  * **n_repeat** (_int_) â Number of timing iterations

  * **backend** (_Literal_ _[__'event'__,__'cupti'__,__'cudagraph'__]_) â Which profiling backend to use - âeventâ, âcuptiâ, or âcudagraphâ

  * **input_tensors** (_list_ _[__torch.Tensor_ _]_) â Optional pre-generated input tensors

  * **dynamic_symbolic_constraints** (_dict_ _[__str_ _,__int_ _]__|__None_) â Optional dict mapping dynamic symbolic variable names to concrete int values. Use this when benchmarking kernels with dynamic shapes, e.g., {âmâ: 2048, ânâ: 1024}

  * **quantiles** (_list_ _[__float_ _]__|__None_)

  * **return_mode** (_Literal_ _[__'min'__,__'max'__,__'mean'__,__'median'__]_)



Returns:
    

Average execution time in milliseconds

Return type:
    

float

_property _funcÂ¶
    

__call__(_* args_, _** kwds_)Â¶
    

Parameters:
    

  * **args** (_Any_)

  * **kwds** (_Any_)



Return type:
    

Any
