# tilelang.profiler.benchÂ¶

Profiler and benchmarking utilities for PyTorch functions.

## AttributesÂ¶

`IS_CUDA` |   
---|---  
`device` |   
`Event` |   
  
## ClassesÂ¶

`suppress_stdout_stderr` | Context manager to suppress stdout and stderr output.  
---|---  
  
## FunctionsÂ¶

`do_bench`(fn[, warmup, rep, _n_warmup, _n_repeat, ...]) | Benchmark the runtime of a PyTorch function with L2 cache management.  
---|---  
  
## Module ContentsÂ¶

_class _tilelang.profiler.bench.suppress_stdout_stderrÂ¶
    

Context manager to suppress stdout and stderr output.

Source: <https://github.com/deepseek-ai/DeepGEMM/blob/main/deep_gemm/testing/bench.py>

__enter__()Â¶
    

__exit__(_* __)Â¶
    

tilelang.profiler.bench.IS_CUDAÂ¶
    

tilelang.profiler.bench.device _ = 'cuda:0'_Â¶
    

tilelang.profiler.bench.EventÂ¶
    

tilelang.profiler.bench.do_bench(_fn_ , _warmup =25_, _rep =100_, __n_warmup =0_, __n_repeat =0_, _quantiles =None_, _fast_flush =True_, _backend ='event'_, _return_mode ='mean'_)Â¶
    

Benchmark the runtime of a PyTorch function with L2 cache management.

This function provides accurate GPU kernel timing by: \- Clearing L2 cache between runs for consistent measurements \- Auto-calculating warmup and repeat counts based on kernel runtime \- Supporting multiple profiling backends (CUDA events, CUPTI, or CUDA graph replay) \- Offering flexible result aggregation (mean/median/min/max/quantiles)

Parameters:
    

  * **fn** (_Callable_) â Function to benchmark

  * **warmup** (_float_) â Target warmup time in milliseconds (default: 25)

  * **rep** (_float_) â Target total benchmark time in milliseconds (default: 100)

  * **_n_warmup** (_int_) â Manual override for warmup iterations (default: 0 = auto)

  * **_n_repeat** (_int_) â Manual override for benchmark iterations (default: 0 = auto)

  * **quantiles** (_list_ _[__float_ _]__|__None_) â Performance percentiles to compute (e.g., [0.5, 0.95])

  * **fast_flush** ([_bool_](../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool")) â Use faster L2 cache flush with int32 vs int8 (default: True)

  * **backend** (_Literal_ _[__'event'__,__'cupti'__,__'cudagraph'__]_) â Profiler backend - âeventâ (CUDA events), âcuptiâ, or âcudagraphâ (default: âeventâ)

  * **return_mode** (_Literal_ _[__'min'__,__'max'__,__'mean'__,__'median'__]_) â Result aggregation method - âmeanâ, âmedianâ, âminâ, or âmaxâ



Returns:
    

Runtime in milliseconds (float) or list of quantile values if quantiles specified

Return type:
    

float | list[float]
