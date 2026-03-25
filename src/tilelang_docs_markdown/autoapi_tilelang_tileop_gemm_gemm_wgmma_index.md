# tilelang.tileop.gemm.gemm_wgmmaÂ¶

## ClassesÂ¶

`GemmWGMMA` | Base class for GEMM tile operators.  
---|---  
  
## Module ContentsÂ¶

_class _tilelang.tileop.gemm.gemm_wgmma.GemmWGMMAÂ¶
    

Bases: [`tilelang.tileop.gemm.gemm_base.GemmBase`](../gemm_base/index.html#tilelang.tileop.gemm.gemm_base.GemmBase "tilelang.tileop.gemm.gemm_base.GemmBase")

Base class for GEMM tile operators.

Classifies the GEMM variant by the memory scopes of operands A and B (SS, SR, RS, TS, RR) and provides common property accessors for the underlying `gemm_node` IR node.

infer_shared_layout(_continuity_)Â¶
    

Infer the swizzle layout for shared memory based on continuity.

WGMMA can directly use shared memory as input, so the swizzle layout must match the tensor coreâs access pattern. The swizzle granularity is determined by the continuous dimension size:

>   * 128B swizzle (Full): continuity % (vectorized_size * 8) == 0
> 
>   * 64B swizzle (Half): continuity % (vectorized_size * 4) == 0
> 
>   * 32B swizzle (Quarter): continuity % (vectorized_size * 2) == 0
> 
>   * Linear (no swizzle): otherwise
> 
> 


See: <https://docs.nvidia.com/cuda/cuda-driver-api/group__CUDA__TENSOR__MEMORY.html>

Parameters:
    

**continuity** (_int_)

Return type:
    

Callable[[tvm.tir.Buffer], tilelang.layout.Layout]

infer_layout(_target_ , _thread_nums_)Â¶
    

Parameters:
    

  * **target** (_tvm.target.Target_)

  * **thread_nums** (_int_)




lower(_layout_map_ , _target_ , _thread_bounds_ , _thread_var_)Â¶
    

Parameters:
    

  * **layout_map** (_dict_)

  * **target** (_tvm.target.Target_)

  * **thread_bounds** (_tvm.ir.Range_)

  * **thread_var** (_tvm.tir.Var_)




is_gemm_ss()Â¶
    

Return True if both A and B are in shared memory (SS variant).

Return type:
    

[bool](../../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool")

is_gemm_sr()Â¶
    

Return True if A is in shared memory and B is in registers (SR variant).

Return type:
    

[bool](../../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool")

is_gemm_rs()Â¶
    

Return True if A is in registers and B is in shared memory (RS variant).

Return type:
    

[bool](../../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool")

is_gemm_rr()Â¶
    

Return True if both A and B are in registers (RR variant).

Return type:
    

[bool](../../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool")
