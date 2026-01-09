# triton.testing.do_bench_cudagraph¶

triton.testing.do_bench_cudagraph(_fn_ , _rep =20_, _grad_to_none =None_, _quantiles =None_, _return_mode ='mean'_)¶
    

Benchmark the runtime of the provided function.

Parameters:
    

  * **fn** (_Callable_) – Function to benchmark

  * **rep** (_int_) – Repetition time (in ms)

  * **grad_to_none** (_torch.tensor_ _,__optional_) – Reset the gradient of the provided tensor to None

  * **return_mode** (_str_) – The statistical measure to return. Options are “min”, “max”, “mean”, “median”, or “all”. Default is “mean”.



