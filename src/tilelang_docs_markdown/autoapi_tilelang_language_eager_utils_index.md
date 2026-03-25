# tilelang.language.eager.utilsÂ¶

## AttributesÂ¶

`CompileMethod` |   
---|---  
  
## FunctionsÂ¶

`disk_compile`(source, name) |   
---|---  
`get_func_nonlocals`(func) | A modified version of inspect.getclosurevars  
`get_ast`(func) |   
`get_compiled_object`(source, name[, filename, globals]) |   
`construct_strides`(shape[, allow_prim_expr]) | Construct row-major strides from shape.  
  
## Module ContentsÂ¶

tilelang.language.eager.utils.disk_compile(_source_ , _name_)Â¶
    

tilelang.language.eager.utils.get_func_nonlocals(_func_)Â¶
    

A modified version of inspect.getclosurevars

tilelang.language.eager.utils.get_ast(_func_)Â¶
    

Parameters:
    

**func** (_Callable_)

tilelang.language.eager.utils.CompileMethodÂ¶
    

tilelang.language.eager.utils.get_compiled_object(_source_ , _name_ , _filename =None_, _globals =None_)Â¶
    

Parameters:
    

  * **source** (_str_ _|__ast.AST_)

  * **name** (_str_)

  * **filename** (_str_)

  * **globals** (_dict_ _[__str_ _,__Any_ _]_)




tilelang.language.eager.utils.construct_strides(_shape_ , _allow_prim_expr =True_)Â¶
    

Construct row-major strides from shape.

Parameters:
    

  * **shape** (_tuple_ _[__Any_ _,__Ellipsis_ _]_)

  * **allow_prim_expr** ([_bool_](../../dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool"))



Return type:
    

tuple[Any, Ellipsis]
