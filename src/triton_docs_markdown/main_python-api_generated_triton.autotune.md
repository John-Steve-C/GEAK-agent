# triton.autotune¶  
  
triton.autotune(_configs_ , _key_ , _prune_configs_by =None_, _reset_to_zero =None_, _restore_value =None_, _pre_hook =None_, _post_hook =None_, _warmup =None_, _rep =None_, _use_cuda_graph =False_, _do_bench =None_, _cache_results =False_)¶
    

Decorator for auto-tuning a `triton.jit`’d function.
    
    
    @triton.autotune(configs=[
        triton.Config(kwargs={'BLOCK_SIZE': 128}, num_warps=4),
        triton.Config(kwargs={'BLOCK_SIZE': 1024}, num_warps=8),
      ],
      key=['x_size'] # the two above configs will be evaluated anytime
                     # the value of x_size changes
    )
    @triton.jit
    def kernel(x_ptr, x_size, BLOCK_SIZE: tl.constexpr):
        ...
    

Note:
    

When all the configurations are evaluated, the kernel will run multiple times. This means that whatever value the kernel updates will be updated multiple times. To avoid this undesired behavior, you can use the reset_to_zero argument, which resets the value of the provided tensor to zero before running any configuration.

If the environment variable `TRITON_PRINT_AUTOTUNING` is set to `"1"`, Triton will print a message to stdout after autotuning each kernel, including the time spent autotuning and the best configuration.

Parameters:
    

  * **configs** (_list_ _[_[_triton.Config_](triton.Config.html#triton.Config "triton.Config") _]_) – a list of `triton.Config` objects

  * **key** (_list_ _[__str_ _]_) – a list of argument names whose change in value will trigger the evaluation of all provided configs.

  * **prune_configs_by** – 

a dict of functions that are used to prune configs, fields: ‘perf_model’: performance model used to predicate running time with different configs, returns running time ‘top_k’: number of configs to bench ‘early_config_prune’: a function used to prune configs. It should have the signature

> prune_configs_by( configs: List[triton.Config], named_args: Dict[str, Any], **kwargs: Dict[str, Any]) -> List[triton.Config]: and return pruned configs. It should return at least one config.

  * **reset_to_zero** (_list_ _[__str_ _]_) – a list of argument names whose value will be reset to zero before evaluating any configs.

  * **restore_value** (_list_ _[__str_ _]_) – a list of argument names whose value will be restored after evaluating any configs.

  * **pre_hook** (_lambda args_ _,__reset_only_) – a function that will be called before the kernel is called. This overrides the default pre_hook used for ‘reset_to_zero’ and ‘restore_value’. ‘kwargs’: a dict of all arguments passed to the kernel. ‘reset_only’: a boolean indicating whether the pre_hook is called to reset the values only, without a corresponding post_hook.

  * **post_hook** (_lambda args_ _,__exception_) – a function that will be called after the kernel is called. This overrides the default post_hook used for ‘restore_value’. ‘kwargs’: a dict of all arguments passed to the kernel. ‘exception’: the exception raised by the kernel in case of a compilation or runtime error.

  * **warmup** (_int_) – warmup time (in ms) to pass to benchmarking (deprecated).

  * **rep** (_int_) – repetition time (in ms) to pass to benchmarking (deprecated).

  * **do_bench** (_lambda fn_ _,__quantiles_) – a benchmark function to measure the time of each run.

  * **cache_results** – whether to cache autotune timings to disk. Defaults to False.




“type cache_results: bool
