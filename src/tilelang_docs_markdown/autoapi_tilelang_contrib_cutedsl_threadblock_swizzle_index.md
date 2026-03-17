# tilelang.contrib.cutedsl.threadblock_swizzleÂ¶

## ClassesÂ¶

`dim3` |   
---|---  
  
## FunctionsÂ¶

`ThreadIdx`() |   
---|---  
`BlockIdx`() |   
`GridDim`() |   
`rasterization2DRow`(panel_width) |   
`rasterization2DColumn`(panel_width) |   
  
## Module ContentsÂ¶

_class _tilelang.contrib.cutedsl.threadblock_swizzle.dim3Â¶
    

x _: int_Â¶
    

y _: int_Â¶
    

z _: int_Â¶
    

tilelang.contrib.cutedsl.threadblock_swizzle.ThreadIdx()Â¶
    

Return type:
    

dim3

tilelang.contrib.cutedsl.threadblock_swizzle.BlockIdx()Â¶
    

Return type:
    

dim3

tilelang.contrib.cutedsl.threadblock_swizzle.GridDim()Â¶
    

Return type:
    

dim3

tilelang.contrib.cutedsl.threadblock_swizzle.rasterization2DRow(_panel_width_)Â¶
    

Parameters:
    

**panel_width** (_cutlass.cute.typing.Constexpr_ _[__int_ _]_)

Return type:
    

dim3

tilelang.contrib.cutedsl.threadblock_swizzle.rasterization2DColumn(_panel_width_)Â¶
    

Parameters:
    

**panel_width** (_cutlass.cute.typing.Constexpr_ _[__int_ _]_)

Return type:
    

dim3
