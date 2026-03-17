# tilelang.language.tir.entryÂ¶

## FunctionsÂ¶

`prim_func`([func, private, check_well_formed]) | The parsing method for tir prim func, by using @prim_func as decorator.  
---|---  
`macro`(*args[, hygienic]) | Decorator for macro definitions.  
  
## Module ContentsÂ¶

tilelang.language.tir.entry.prim_func(_func =None_, _private =False_, _check_well_formed =False_)Â¶
    

The parsing method for tir prim func, by using @prim_func as decorator.

Parameters:
    

  * **func** (_Callable_) â The function to be parsed as prim func. (Listed as optional to allow the decorator to be used without arguments, like @prim_func, or with an argument, @prim_func(private=True))

  * **private** ([_bool_](../../dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool") _,__optional_) â Whether the function should be treated as private. A private function has no global symbol attribute; if the function is not private, it will have a global symbol matching the function name.

  * **check_well_formed** ([_bool_](../../dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool"))



Returns:
    

**res** â The parsed tir prim func.

Return type:
    

Union[[PrimFunc](../../eager/builder/index.html#tilelang.language.eager.builder.PrimFunc "tilelang.language.eager.builder.PrimFunc"), Callable]

tilelang.language.tir.entry.macro(_* args_, _hygienic =True_)Â¶
    

Decorator for macro definitions.

Parameters:
    

**hygienic** â 

Specifies whether the macro is hygienic or not. A macro is hygienic if all symbols used in the macroâs body are resolved to values from the location of the macro definition. A non-hygienic macro will have its symbols resolved to values at the time of the macroâs use.

Example: ``` import tvm from tvm.script import tir as T

x_value = 128

@T.macro(hygienic=True) def static_capture(A, B):

> B[()] = A[x_value] ### x_value binds to 128

@T.macro(hygienic=False) def dynamic_capture(A, B):

> B[()] = A[x_value] ### x_value will bind at the time of use

Return type:
    

Callable
