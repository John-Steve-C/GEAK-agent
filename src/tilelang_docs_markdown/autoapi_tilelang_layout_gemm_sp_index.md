# tilelang.layout.gemm_spÂ¶

Wrapping Layouts.

## FunctionsÂ¶

`decompose_col_major`(index_1d, basis) |   
---|---  
`make_cutlass_metadata_layout_sm90`(buffer, mma_dtype, ...) | Make a layout of metadata that is compatible with cutlass sm90 compression kernel. Note that layout atom is the same for smem and gmem.  
`make_cutlass_metadata_layout_sm8x`(buffer, mma_dtype) | Make a layout of metadata that is compatible with cutlass sm8x compression kernel. Note that layout atom is the same for smem and gmem.  
`make_cutlass_metadata_layout`(buffer[, mma_dtype, arch]) |   
  
## Module ContentsÂ¶

tilelang.layout.gemm_sp.decompose_col_major(_index_1d_ , _basis_)Â¶
    

Parameters:
    

  * **index_1d** (_int_)

  * **basis** (_list_ _[__int_ _]_)



Return type:
    

list[int]

tilelang.layout.gemm_sp.make_cutlass_metadata_layout_sm90(_buffer_ , _mma_dtype_ , _block_k_)Â¶
    

Make a layout of metadata that is compatible with cutlass sm90 compression kernel. Note that layout atom is the same for smem and gmem.

Parameters:
    

  * **buffer** (_tvm.tir.Buffer_) â metadata buffer shape, for sm90 it should be a 8-bit type

  * **mma_dtype** (_str_) â dtype of mma operand A, different dtypes result in different layout atom

  * **block_k** (_int_) â tiling size along K dim, different block_ks results in different layout atom.




tilelang.layout.gemm_sp.make_cutlass_metadata_layout_sm8x(_buffer_ , _mma_dtype_)Â¶
    

Make a layout of metadata that is compatible with cutlass sm8x compression kernel. Note that layout atom is the same for smem and gmem.
    

ref: <https://github.com/pytorch/pytorch/blob/d0c24b392cbb7b213d22e42c52c6c2d1ac2da1bd/torch/sparse/_semi_structured_conversions.py#L5>

Parameters:
    

  * **buffer** (_tvm.tir.Buffer_) â metadata buffer shape, for sm80 it should be a 16bit type

  * **mma_dtype** (_str_)




tilelang.layout.gemm_sp.make_cutlass_metadata_layout(_buffer_ , _mma_dtype =T.float16_, _arch =None_, _** extra_args_)Â¶
    

Parameters:
    

  * **buffer** (_tvm.tir.Buffer_)

  * **mma_dtype** (_str_)

  * **arch** (_str_ _|__None_)



