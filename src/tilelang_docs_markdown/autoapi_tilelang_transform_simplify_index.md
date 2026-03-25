# tilelang.transform.simplifyÂ¶

## FunctionsÂ¶

`LetInline`() | LetInline  
---|---  
`Simplify`([simplify_arguments]) | Simplify  
`simplify_prim_func`(func) |   
`apply_simplify`(stmt[, inline_let]) | Apply Simplify pass to a PrimFunc or IRModule.  
  
## Module ContentsÂ¶

tilelang.transform.simplify.LetInline()Â¶
    

LetInline

Returns:
    

**fpass** â The result pass

Return type:
    

tvm.transform.Pass

tilelang.transform.simplify.Simplify(_simplify_arguments =False_)Â¶
    

Simplify

Returns:
    

**fpass** â The result pass

Return type:
    

tvm.transform.Pass

Parameters:
    

**simplify_arguments** ([_bool_](../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool"))

tilelang.transform.simplify.simplify_prim_func(_func_)Â¶
    

Parameters:
    

**func** (_Callable_)

Return type:
    

Callable

tilelang.transform.simplify.apply_simplify(_stmt_ , _inline_let =False_)Â¶
    

Apply Simplify pass to a PrimFunc or IRModule.

Parameters:
    

  * **stmt** (_tvm.tir.PrimFunc_ _|__tvm.IRModule_)

  * **inline_let** ([_bool_](../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool"))



Return type:
    

tvm.tir.PrimFunc | tvm.IRModule
