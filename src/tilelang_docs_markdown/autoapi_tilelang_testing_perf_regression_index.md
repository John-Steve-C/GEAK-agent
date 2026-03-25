# tilelang.testing.perf_regressionÂ¶

## ClassesÂ¶

`PerfResult` |   
---|---  
  
## FunctionsÂ¶

`process_func`(func[, name]) | Execute a single perf function and record its latency.  
---|---  
`regression`([prefixes, verbose]) | Run entrypoints in the caller module and print a markdown table.  
  
## Module ContentsÂ¶

_class _tilelang.testing.perf_regression.PerfResultÂ¶
    

name _: str_Â¶
    

latency _: float_Â¶
    

tilelang.testing.perf_regression.process_func(_func_ , _name =None_, _/_ , _** kwargs_)Â¶
    

Execute a single perf function and record its latency.

func is expected to return a positive latency scalar (seconds or ms; we treat it as an opaque number, only ratios matter for regression).

Parameters:
    

  * **func** (_Callable_ _[__Ellipsis_ _,__float_ _]_)

  * **name** (_str_ _|__None_)

  * **kwargs** (_Any_)



Return type:
    

None

tilelang.testing.perf_regression.regression(_prefixes =('regression_',)_, _verbose =True_)Â¶
    

Run entrypoints in the caller module and print a markdown table.

This is invoked by many example scripts.

Parameters:
    

  * **prefixes** (_collections.abc.Sequence_ _[__str_ _]_)

  * **verbose** ([_bool_](../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool"))



Return type:
    

None
