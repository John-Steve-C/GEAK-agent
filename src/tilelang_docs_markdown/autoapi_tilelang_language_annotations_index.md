# tilelang.language.annotationsÂ¶

Annotation helpers exposed on the TileLang language surface.

## FunctionsÂ¶

`use_swizzle`(panel_size[, order, enable]) | Annotate a kernel to use a specific threadblock swizzle pattern.  
---|---  
`annotate_layout`(layout_map) | Annotate the layout of the buffer.  
`annotate_safe_value`(safe_value_map) | Annotate the safe value of the buffer.  
`annotate_l2_hit_ratio`(l2_hit_ratio_map) | Annotate the L2 hit ratio of the buffer.  
`annotate_restrict_buffers`(*buffers) | Mark the given buffer parameters as non-restrict.  
  
## Module ContentsÂ¶

tilelang.language.annotations.use_swizzle(_panel_size_ , _order ='row'_, _enable =True_)Â¶
    

Annotate a kernel to use a specific threadblock swizzle pattern.

Parameters:
    

  * **panel_size** (_int_)

  * **order** (_str_)

  * **enable** ([_bool_](../dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool"))




tilelang.language.annotations.annotate_layout(_layout_map_)Â¶
    

Annotate the layout of the buffer.

Parameters:
    

**layout_map** (_dict_)

tilelang.language.annotations.annotate_safe_value(_safe_value_map_)Â¶
    

Annotate the safe value of the buffer.

Parameters:
    

**safe_value_map** (_dict_)

tilelang.language.annotations.annotate_l2_hit_ratio(_l2_hit_ratio_map_)Â¶
    

Annotate the L2 hit ratio of the buffer.

Parameters:
    

**l2_hit_ratio_map** (_dict_)

tilelang.language.annotations.annotate_restrict_buffers(_* buffers_)Â¶
    

Mark the given buffer parameters as non-restrict.

This annotation tells codegen to omit the __restrict__ qualifier for the specified kernel buffer parameters. Use this when two (or more) buffers may alias, for example overlapping slices from the same base tensor.

Example
    
    
    >>> @T.prim_func
    ... def buggy_kernel(x: T.Tensor((N,), T.float32),
    ...                  y: T.Tensor((N,), T.float32)):
    ...     T.annotate_restrict_buffers(x, y)
    ...     with T.Kernel(N, threads=32) as pid:
    ...         y[pid] = x[pid] + 1
    
