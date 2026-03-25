# tilelang.intrinsics.mma_sp_macro_generatorÂ¶

## AttributesÂ¶

`lift` |   
---|---  
  
## ClassesÂ¶

`SparseTensorCoreIntrinEmitter` | To eliminate Python syntax within TIR Macro.  
---|---  
  
## Module ContentsÂ¶

tilelang.intrinsics.mma_sp_macro_generator.liftÂ¶
    

_class _tilelang.intrinsics.mma_sp_macro_generator.SparseTensorCoreIntrinEmitter(_a_dtype =T.float16_, _e_dtype =T.uint8_, _b_dtype =T.float16_, _accum_dtype =T.float16_, _a_transposed =False_, _b_transposed =False_, _e_transposed =False_, _block_row_warps =2_, _block_col_warps =2_, _warp_row_tiles =8_, _warp_col_tiles =8_, _warp_k =16_, _reduce_k =1_, _num_elems_per_byte =1_, _is_m_first =False_, _thread_var =None_)Â¶
    

To eliminate Python syntax within TIR Macro.

Parameters:
    

  * **a_dtype** (_str_)

  * **e_dtype** (_str_)

  * **b_dtype** (_str_)

  * **accum_dtype** (_str_)

  * **a_transposed** ([_bool_](../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool"))

  * **b_transposed** ([_bool_](../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool"))

  * **e_transposed** ([_bool_](../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool"))

  * **block_row_warps** (_int_)

  * **block_col_warps** (_int_)

  * **warp_row_tiles** (_int_)

  * **warp_col_tiles** (_int_)

  * **warp_k** (_int_)

  * **reduce_k** (_int_)

  * **num_elems_per_byte** (_int_)

  * **is_m_first** ([_bool_](../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool"))

  * **thread_var** (_tvm.tir.Var_ _|__None_)




M_DIM _ = 16_Â¶
    

SPARSE_FACTOR _ = 2_Â¶
    

SPARSE_SELECTOR _ = 0_Â¶
    

n_dim _ = 16_Â¶
    

WARP_SIZE _ = 32_Â¶
    

dtype_abbrvÂ¶
    

E_FACTOR_MAPÂ¶
    

E_REPLICATE_FACTORÂ¶
    

is_m_first _ = False_Â¶
    

a_dtypeÂ¶
    

e_dtypeÂ¶
    

b_dtypeÂ¶
    

accum_dtypeÂ¶
    

a_transposed _ = False_Â¶
    

b_transposed _ = False_Â¶
    

e_transposed _ = False_Â¶
    

block_row_warps _ = 2_Â¶
    

block_col_warps _ = 2_Â¶
    

warp_row_tiles _ = 8_Â¶
    

warp_col_tiles _ = 8_Â¶
    

warp_k _ = 16_Â¶
    

e_factorÂ¶
    

reduce_k _ = 1_Â¶
    

threads _ = 128_Â¶
    

num_elems_per_byte _ = 1_Â¶
    

thread_var _ = None_Â¶
    

get_thread_binding()Â¶
    

get_store_index_map(_inverse =False_)Â¶
    

Parameters:
    

**inverse** ([_bool_](../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool"))

Return type:
    

tvm.tir.IndexMap

extract_thread_binding(_thread_id_ , _is_m_first =None_)Â¶
    

is_m_first: True if the thread binding is in the form of (tx, warp_n, warp_m) which represents [warp_size, block_row_warps (split n), block_col_warps (split m)] Otherwise, it is in the form of [warp_size, block_col_warps (split m), block_row_warps (split n)]

Parameters:
    

  * **thread_id** (_tvm.tir.PrimExpr_)

  * **is_m_first** ([_bool_](../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool") _|__None_)



Return type:
    

tuple[tvm.tir.PrimExpr, tvm.tir.PrimExpr, tvm.tir.PrimExpr]

ldmatrix_a(_A_local_buf_ , _A_shared_buf_ , _ki_ , _rk =0_)Â¶
    

Parameters:
    

  * **A_local_buf** (_tvm.tir.Buffer_)

  * **A_shared_buf** (_tvm.tir.Buffer_)

  * **ki** (_tvm.tir.PrimExpr_)

  * **rk** (_tvm.tir.PrimExpr_)




ldmatrix_e(_E_local_buf_ , _E_shared_buf_ , _ki_ , _rk =0_)Â¶
    

Parameters:
    

  * **E_local_buf** (_tvm.tir.Buffer_)

  * **E_shared_buf** (_tvm.tir.Buffer_)

  * **ki** (_tvm.tir.PrimExpr_)

  * **rk** (_tvm.tir.PrimExpr_)




ldmatrix_b(_B_local_buf_ , _B_shared_buf_ , _ki_ , _rk =0_)Â¶
    

Parameters:
    

  * **B_local_buf** (_tvm.tir.Buffer_)

  * **B_shared_buf** (_tvm.tir.Buffer_)

  * **ki** (_tvm.tir.PrimExpr_)

  * **rk** (_tvm.tir.PrimExpr_)




mma_sp(_A_local_buf_ , _E_local_buf_ , _B_local_buf_ , _C_local_buf_ , _k_inner =0_)Â¶
    

Parameters:
    

  * **A_local_buf** (_tvm.tir.Buffer_)

  * **E_local_buf** (_tvm.tir.Buffer_)

  * **B_local_buf** (_tvm.tir.Buffer_)

  * **C_local_buf** (_tvm.tir.Buffer_)

  * **k_inner** (_tvm.tir.PrimExpr_)




stmatrix(_C_local_buf_ , _C_buf_ , _pid_m =None_, _pid_n =None_)Â¶
    

make_mma_load_layout(_local_buf_ , _matrix ='A'_)Â¶
    

Create a layout function for storing MMA results into a fragment buffer. This layout is used in conjunction with inverse_mma_store_layout to map fragment indices to threads and local indices.

Parameters:
    

  * **local_buf** (_tir.Buffer_) â The local buffer representing a fragment of a matrix.

  * **matrix** (_Literal_ _[__'A'__,__'B'__]_)



Returns:
    

A fragment object that describes how threads and indices in local_buf are laid out.

Return type:
    

T.Fragment

Raises:
    

**AssertionError** â If local_buf is not detected to be a fragment buffer.

make_mma_store_layout(_local_buf_)Â¶
    

Create a layout function for storing MMA results into a fragment buffer. This layout is used in conjunction with inverse_mma_store_layout to map fragment indices to threads and local indices.

Parameters:
    

**local_buf** (_tir.Buffer_) â The local buffer representing a fragment of a matrix.

Returns:
    

A fragment object that describes how threads and indices in local_buf are laid out.

Return type:
    

T.Fragment

Raises:
    

**AssertionError** â If local_buf is not detected to be a fragment buffer.
