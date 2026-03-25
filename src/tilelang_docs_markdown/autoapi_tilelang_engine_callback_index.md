# tilelang.engine.callbackÂ¶

## FunctionsÂ¶

`register_cuda_postproc`(func[, override]) | Register a post-processing function for CUDA code generation.  
---|---  
`register_hip_postproc`(func[, override]) | Register a post-processing function for HIP code generation.  
`register_c_postproc`(func[, override]) | Register a post-processing function for C host code generation.  
`register_metal_postproc`(func[, override]) | Register a post-processing function for Metal code generation.  
`register_cuda_postproc_callback`([func, override]) | Decorator for registering CUDA post-processing callback function.  
`register_hip_postproc_callback`([func, override]) | Decorator for registering HIP post-processing callback function.  
`register_c_postproc_callback`([func, override]) | Decorator for registering C host post-processing callback function.  
`register_metal_postproc_callback`([func, override]) | Decorator for registering Metal post-processing callback function.  
  
## Module ContentsÂ¶

tilelang.engine.callback.register_cuda_postproc(_func_ , _override =True_)Â¶
    

Register a post-processing function for CUDA code generation.

Parameters:
    

  * **func** (_Callable_ _[__[__str_ _,__tvm.target.Target_ _]__,__str_ _]_) â A callable that takes generated code (str) and target (Target) as input, and returns the processed code (str).

  * **override** ([_bool_](../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool")) â Whether to override existing registered function. Defaults to True.




tilelang.engine.callback.register_hip_postproc(_func_ , _override =True_)Â¶
    

Register a post-processing function for HIP code generation.

Parameters:
    

  * **func** (_Callable_ _[__[__str_ _,__tvm.target.Target_ _]__,__str_ _]_) â A callable that takes generated code (str) and target (Target) as input, and returns the processed code (str).

  * **override** ([_bool_](../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool")) â Whether to override existing registered function. Defaults to True.




tilelang.engine.callback.register_c_postproc(_func_ , _override =True_)Â¶
    

Register a post-processing function for C host code generation.

This callback intercepts C host code emitted by TileLang just before it is wrapped into a CSourceModule. It should take the generated code string and the Target as inputs, and return the (possibly) modified code.

Parameters:
    

  * **func** (_Callable_ _[__[__str_ _,__tvm.target.Target_ _]__,__str_ _]_) â A callable that takes generated code (str) and target (Target) as input, and returns the processed code (str).

  * **override** ([_bool_](../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool")) â Whether to override existing registered function. Defaults to True.




tilelang.engine.callback.register_metal_postproc(_func_ , _override =True_)Â¶
    

Register a post-processing function for Metal code generation.

Parameters:
    

  * **func** (_Callable_ _[__[__str_ _,__tvm.target.Target_ _]__,__str_ _]_) â A callable that takes generated code (str) and target (Target) as input, and returns the processed code (str).

  * **override** ([_bool_](../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool")) â Whether to override existing registered function. Defaults to True.




tilelang.engine.callback.register_cuda_postproc_callback(_func =None_, _override =True_)Â¶
    

Decorator for registering CUDA post-processing callback function.

Can be used with or without parentheses:
    

@register_cuda_postproc_callback def func(code, target): â¦

@register_cuda_postproc_callback() def func(code, target): â¦

@register_cuda_postproc_callback(override=False) def func(code, target): â¦

Parameters:
    

  * **func** (_Callable_ _|_[_bool_](../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool")) â The function to be decorated or a boolean override flag

  * **override** ([_bool_](../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool")) â Whether to override existing registered function. Defaults to True.




tilelang.engine.callback.register_hip_postproc_callback(_func =None_, _override =True_)Â¶
    

Decorator for registering HIP post-processing callback function.

Can be used with or without parentheses:
    

@register_hip_postproc_callback def func(code, target): â¦

@register_hip_postproc_callback() def func(code, target): â¦

@register_hip_postproc_callback(override=False) def func(code, target): â¦

Parameters:
    

  * **func** (_Callable_ _|_[_bool_](../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool")) â The function to be decorated or a boolean override flag

  * **override** ([_bool_](../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool")) â Whether to override existing registered function. Defaults to True.




tilelang.engine.callback.register_c_postproc_callback(_func =None_, _override =True_)Â¶
    

Decorator for registering C host post-processing callback function.

Can be used with or without parentheses:
    

@register_c_postproc_callback def func(code, target): â¦

@register_c_postproc_callback() def func(code, target): â¦

@register_c_postproc_callback(override=False) def func(code, target): â¦

Parameters:
    

  * **func** (_Callable_ _|_[_bool_](../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool")) â The function to be decorated or a boolean override flag

  * **override** ([_bool_](../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool")) â Whether to override existing registered function. Defaults to True.




tilelang.engine.callback.register_metal_postproc_callback(_func =None_, _override =True_)Â¶
    

Decorator for registering Metal post-processing callback function.

Can be used with or without parentheses:
    

@register_metal_postproc_callback def func(code, target): â¦

@register_metal_postproc_callback() def func(code, target): â¦

@register_metal_postproc_callback(override=False) def func(code, target): â¦

Parameters:
    

  * **func** (_Callable_ _|_[_bool_](../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool")) â The function to be decorated or a boolean override flag

  * **override** ([_bool_](../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool")) â Whether to override existing registered function. Defaults to True.



