# tilelang.contrib.cutedsl.mathÂ¶

## FunctionsÂ¶

`exp10`(x[, fastmath]) | Compute 10^x using exp2(x * log2(10)).  
---|---  
`fabsf`(x[, fastmath]) |   
`divf`(x, y[, fastmath]) |   
`tanh`(x[, fastmath]) |   
  
## Module ContentsÂ¶

tilelang.contrib.cutedsl.math.exp10(_x_ , _fastmath =False_)Â¶
    

Compute 10^x using exp2(x * log2(10)).

Parameters:
    

  * **x** (_cutlass.cute.typing.Union_ _[__cutlass.cute.tensor.TensorSSA_ _,__cutlass.cute.typing.Numeric_ _]_)

  * **fastmath** ([_bool_](../../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool"))



Return type:
    

cutlass.cute.typing.Union[cutlass.cute.tensor.TensorSSA, cutlass.cute.typing.Numeric]

tilelang.contrib.cutedsl.math.fabsf(_x_ , _fastmath =False_)Â¶
    

Parameters:
    

  * **x** (_cutlass.cute.typing.Union_ _[__cutlass.cute.tensor.TensorSSA_ _,__cutlass.cute.typing.Numeric_ _]_)

  * **fastmath** ([_bool_](../../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool"))



Return type:
    

cutlass.cute.typing.Union[cutlass.cute.tensor.TensorSSA, cutlass.cute.typing.Numeric]

tilelang.contrib.cutedsl.math.divf(_x_ , _y_ , _fastmath =False_)Â¶
    

Parameters:
    

  * **x** (_cutlass.cute.typing.Union_ _[__cutlass.cute.tensor.TensorSSA_ _,__cutlass.cute.typing.Numeric_ _]_)

  * **y** (_cutlass.cute.typing.Union_ _[__cutlass.cute.tensor.TensorSSA_ _,__cutlass.cute.typing.Numeric_ _]_)

  * **fastmath** ([_bool_](../../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool"))



Return type:
    

cutlass.cute.typing.Union[cutlass.cute.tensor.TensorSSA, cutlass.cute.typing.Numeric]

tilelang.contrib.cutedsl.math.tanh(_x_ , _fastmath =False_)Â¶
    

Parameters:
    

  * **x** (_cutlass.cute.typing.Union_ _[__cutlass.cute.tensor.TensorSSA_ _,__cutlass.cute.typing.Numeric_ _]_)

  * **fastmath** ([_bool_](../../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool"))



Return type:
    

cutlass.cute.typing.Union[cutlass.cute.tensor.TensorSSA, cutlass.cute.typing.Numeric]
