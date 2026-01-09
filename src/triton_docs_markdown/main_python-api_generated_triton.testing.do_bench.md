# triton.testing.do_bench¶  
  
triton.testing.do_bench(_fn_ , _warmup =25_, _rep =100_, _grad_to_none =None_, _quantiles =None_, _return_mode ='mean'_)¶
    

Benchmark the runtime of the provided function. By default, return the median runtime of `fn` along with the 20-th and 80-th performance percentile.

Parameters:
    

  * **fn** (_Callable_) – Function to benchmark

  * **warmup** (_int_) – Warmup time (in ms)

  * **rep** (_int_) – Repetition time (in ms)

  * **grad_to_none** (_torch.tensor_ _,__optional_) – Reset the gradient of the provided tensor to None

  * **quantiles** (_list_ _[__float_ _]__,__optional_) – Performance percentile to return in addition to the median.

  * **return_mode** (_str_) – The statistical measure to return. Options are “min”, “max”, “mean”, “median”, or “all”. Default is “mean”.



