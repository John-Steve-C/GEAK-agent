# tilelang.layout.swizzleÂ¶

Wrapping Layouts.

## FunctionsÂ¶

`make_swizzled_layout`(buffer[, k_major, allow_pad]) |   
---|---  
`make_volta_swizzled_layout`(buffer[, is_a, k_inner]) |   
`make_wgmma_swizzled_layout`(buffer[, continuity, k_major]) |   
`make_tcgen05mma_swizzled_layout`(buffer[, continuity, ...]) |   
`make_full_bank_swizzled_layout`(buffer) |   
`make_half_bank_swizzled_layout`(buffer) |   
`make_quarter_bank_swizzled_layout`(buffer) |   
`make_linear_layout`(buffer_or_load_or_region) | Create a row-major linear layout for any dimension.  
`make_gemm_fragment_8x8`() | Create a standard 8x8 GEMM fragment layout for ldmatrix/stmatrix.  
`make_gemm_fragment_8x8_transposed`() | Create a transposed 8x8 GEMM fragment layout for ldmatrix/stmatrix.  
`make_fully_replicated_layout_fragment`(buffer, threads) | Create a fully replicated layout for a fragment buffer.  
  
## Module ContentsÂ¶

tilelang.layout.swizzle.make_swizzled_layout(_buffer_ , _k_major =True_, _allow_pad =True_)Â¶
    

Parameters:
    

  * **buffer** (_tilelang._typing.BufferLikeType_)

  * **k_major** ([_bool_](../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool"))

  * **allow_pad** ([_bool_](../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool"))




tilelang.layout.swizzle.make_volta_swizzled_layout(_buffer_ , _is_a =True_, _k_inner =True_)Â¶
    

Parameters:
    

  * **buffer** (_tilelang._typing.BufferLikeType_)

  * **is_a** ([_bool_](../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool"))

  * **k_inner** ([_bool_](../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool"))




tilelang.layout.swizzle.make_wgmma_swizzled_layout(_buffer_ , _continuity =None_, _k_major =True_)Â¶
    

Parameters:
    

  * **buffer** (_tilelang._typing.BufferLikeType_)

  * **continuity** (_int_)

  * **k_major** ([_bool_](../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool"))




tilelang.layout.swizzle.make_tcgen05mma_swizzled_layout(_buffer_ , _continuity =None_, _k_major =True_)Â¶
    

Parameters:
    

  * **buffer** (_tilelang._typing.BufferLikeType_)

  * **continuity** (_int_)

  * **k_major** ([_bool_](../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool"))




tilelang.layout.swizzle.make_full_bank_swizzled_layout(_buffer_)Â¶
    

Parameters:
    

**buffer** (_tilelang._typing.BufferLikeType_) â BufferLikeType

Examples

make_full_bank_swizzled_layout(buffer)

tilelang.layout.swizzle.make_half_bank_swizzled_layout(_buffer_)Â¶
    

Parameters:
    

**buffer** (_tilelang._typing.BufferLikeType_) â BufferLikeType

Examples

make_half_bank_swizzled_layout(buffer)

tilelang.layout.swizzle.make_quarter_bank_swizzled_layout(_buffer_)Â¶
    

Parameters:
    

**buffer** (_tilelang._typing.BufferLikeType_) â BufferLikeType

Examples

make_quarter_bank_swizzled_layout(buffer)

tilelang.layout.swizzle.make_linear_layout(_buffer_or_load_or_region_)Â¶
    

Create a row-major linear layout for any dimension.

Parameters:
    

**buffer_or_load_or_region** (_tilelang._typing.BufferLikeType_) â BufferLikeType

Returns:
    

A row-major linear layout

Return type:
    

[Layout](../layout/index.html#tilelang.layout.layout.Layout "tilelang.layout.layout.Layout")

tilelang.layout.swizzle.make_gemm_fragment_8x8()Â¶
    

Create a standard 8x8 GEMM fragment layout for ldmatrix/stmatrix.

This layout matches the warp-level matrix multiplication pattern used in tensor cores.

Returns:
    

An 8x8 fragment layout

Return type:
    

[Fragment](../fragment/index.html#tilelang.layout.fragment.Fragment "tilelang.layout.fragment.Fragment")

tilelang.layout.swizzle.make_gemm_fragment_8x8_transposed()Â¶
    

Create a transposed 8x8 GEMM fragment layout for ldmatrix/stmatrix.

This layout is the transposed version of make_gemm_fragment_8x8, useful for different access patterns in matrix operations.

Returns:
    

A transposed 8x8 fragment layout

Return type:
    

[Fragment](../fragment/index.html#tilelang.layout.fragment.Fragment "tilelang.layout.fragment.Fragment")

tilelang.layout.swizzle.make_fully_replicated_layout_fragment(_buffer_ , _threads_)Â¶
    

Create a fully replicated layout for a fragment buffer.

A fully replicated fragment means all threads hold identical copies of the entire buffer. This is useful for index buffers or masks that need to be accessed uniformly across all threads.

Parameters:
    

  * **buffer** (_tilelang._typing.BufferLikeType_) â BufferLikeType to get shape information

  * **threads** (_int_) â Number of threads (replicate extent)



Returns:
    

A fully replicated layout where each thread has a complete copy

Return type:
    

[Fragment](../fragment/index.html#tilelang.layout.fragment.Fragment "tilelang.layout.fragment.Fragment")

Example
    
    
    >>> C_local = T.alloc_fragment((2,), T.float32)
    >>> layout = make_fully_replicated_layout_fragment(C_local, 256)
    >>> T.annotate_layout({C_local: layout})
    
