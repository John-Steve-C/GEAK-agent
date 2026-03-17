# tilelang.carver.arch.cudaÂ¶

## ClassesÂ¶

`CUDA` |   
---|---  
  
## FunctionsÂ¶

`is_cuda_arch`(arch) |   
---|---  
`is_volta_arch`(arch) |   
`is_ampere_arch`(arch) |   
`is_ada_arch`(arch) |   
`is_hopper_arch`(arch) |   
`has_mma_support`(arch) |   
`is_tensorcore_supported_precision`(in_dtype, ...) |   
  
## Module ContentsÂ¶

tilelang.carver.arch.cuda.is_cuda_arch(_arch_)Â¶
    

Parameters:
    

**arch** ([_tilelang.carver.arch.arch_base.TileDevice_](../arch_base/index.html#tilelang.carver.arch.arch_base.TileDevice "tilelang.carver.arch.arch_base.TileDevice"))

Return type:
    

[bool](../../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool")

tilelang.carver.arch.cuda.is_volta_arch(_arch_)Â¶
    

Parameters:
    

**arch** ([_tilelang.carver.arch.arch_base.TileDevice_](../arch_base/index.html#tilelang.carver.arch.arch_base.TileDevice "tilelang.carver.arch.arch_base.TileDevice"))

Return type:
    

[bool](../../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool")

tilelang.carver.arch.cuda.is_ampere_arch(_arch_)Â¶
    

Parameters:
    

**arch** ([_tilelang.carver.arch.arch_base.TileDevice_](../arch_base/index.html#tilelang.carver.arch.arch_base.TileDevice "tilelang.carver.arch.arch_base.TileDevice"))

Return type:
    

[bool](../../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool")

tilelang.carver.arch.cuda.is_ada_arch(_arch_)Â¶
    

Parameters:
    

**arch** ([_tilelang.carver.arch.arch_base.TileDevice_](../arch_base/index.html#tilelang.carver.arch.arch_base.TileDevice "tilelang.carver.arch.arch_base.TileDevice"))

Return type:
    

[bool](../../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool")

tilelang.carver.arch.cuda.is_hopper_arch(_arch_)Â¶
    

Parameters:
    

**arch** ([_tilelang.carver.arch.arch_base.TileDevice_](../arch_base/index.html#tilelang.carver.arch.arch_base.TileDevice "tilelang.carver.arch.arch_base.TileDevice"))

Return type:
    

[bool](../../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool")

tilelang.carver.arch.cuda.has_mma_support(_arch_)Â¶
    

Parameters:
    

**arch** ([_tilelang.carver.arch.arch_base.TileDevice_](../arch_base/index.html#tilelang.carver.arch.arch_base.TileDevice "tilelang.carver.arch.arch_base.TileDevice"))

Return type:
    

[bool](../../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool")

tilelang.carver.arch.cuda.is_tensorcore_supported_precision(_in_dtype_ , _accum_dtype_ , _arch_)Â¶
    

Parameters:
    

  * **in_dtype** (_str_)

  * **accum_dtype** (_str_)

  * **arch** ([_tilelang.carver.arch.arch_base.TileDevice_](../arch_base/index.html#tilelang.carver.arch.arch_base.TileDevice "tilelang.carver.arch.arch_base.TileDevice"))



Return type:
    

[bool](../../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool")

_class _tilelang.carver.arch.cuda.CUDA(_target_)Â¶
    

Bases: [`tilelang.carver.arch.arch_base.TileDevice`](../arch_base/index.html#tilelang.carver.arch.arch_base.TileDevice "tilelang.carver.arch.arch_base.TileDevice")

Parameters:
    

**target** (_tvm.target.Target_ _|__str_)

targetÂ¶
    

sm_versionÂ¶
    

nameÂ¶
    

device _: tvm.runtime.Device_Â¶
    

platform _: str_ _ = 'CUDA'_Â¶
    

smem_capÂ¶
    

compute_max_coreÂ¶
    

warp_sizeÂ¶
    

compute_capabilityÂ¶
    

reg_cap _: int_ _ = 65536_Â¶
    

max_smem_usage _: int_Â¶
    

sm_partition _: int_ _ = 4_Â¶
    

l2_cache_size_bytes _: int_Â¶
    

transaction_size _: list[int]__ = [32, 128]_Â¶
    

bandwidth _: list[int]__ = [750, 12080]_Â¶
    

available_tensor_instructions _: list[TensorInstruction]__ = None_Â¶
    

get_avaliable_tensorintrin_shapes()Â¶
    

__repr__()Â¶
    
