# tilelang.language.symbolicsÂ¶

Symbolic variable helpers exposed on the TileLang language surface.

## FunctionsÂ¶

`dynamic`(name[, dtype]) | Create a TIR dynamic symbolic variable.  
---|---  
`symbolic`(name[, dtype]) | Deprecated alias for T.dynamic.  
  
## Module ContentsÂ¶

tilelang.language.symbolics.dynamic(_name_ , _dtype ='int32'_)Â¶
    

Create a TIR dynamic symbolic variable.

Parameters:
    

  * **name** (_str_) â Identifier for the variable in generated TIR.

  * **dtype** (_str_) â Data type string for the variable (e.g., âint32â). Defaults to âint32â.



Returns:
    

A TIR variable with the given name and dtype for use in TIR/TensorIR kernels.

Return type:
    

tir.Var

tilelang.language.symbolics.symbolic(_name_ , _dtype ='int32'_)Â¶
    

Deprecated alias for T.dynamic.

Parameters:
    

  * **name** (_str_)

  * **dtype** (_tilelang._typing.DType_)



Return type:
    

tuple[tvm.tir.Var, Ellipsis] | tvm.tir.Var
