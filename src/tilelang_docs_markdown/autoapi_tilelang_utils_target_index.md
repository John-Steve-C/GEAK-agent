# tilelang.utils.targetÂ¶

## AttributesÂ¶

`SUPPORTED_TARGETS` |   
---|---  
  
## FunctionsÂ¶

`describe_supported_targets`() | Return a mapping of supported target names to usage descriptions.  
---|---  
`check_cuda_availability`() | Check if CUDA is available on the system by locating the CUDA path.  
`check_hip_availability`() | Check if HIP (ROCm) is available on the system by locating the ROCm path.  
`check_metal_availability`() |   
`determine_fp8_type`([fp8_format]) | Select the correct FP8 dtype string for the current platform.  
`determine_torch_fp8_type`([fp8_format]) |   
`normalize_cutedsl_target`(target) |   
`determine_target`([target, return_object]) | Determine the appropriate target for compilation (CUDA, HIP, or manual selection).  
`target_is_cuda`(target) |   
`target_is_hip`(target) |   
`target_is_metal`(target) |   
`target_is_volta`(target) |   
`target_is_turing`(target) |   
`target_is_ampere`(target) |   
`target_is_hopper`(target) |   
`target_is_sm120`(target) |   
`target_is_cdna`(target) |   
`target_is_gfx950`(target) |   
`target_has_async_copy`(target) |   
`target_has_ldmatrix`(target) |   
`target_has_stmatrix`(target) |   
`target_has_bulk_copy`(target) |   
`target_get_warp_size`(target) |   
  
## Module ContentsÂ¶

tilelang.utils.target.SUPPORTED_TARGETS _: dict[str, str]_Â¶
    

tilelang.utils.target.describe_supported_targets()Â¶
    

Return a mapping of supported target names to usage descriptions.

Return type:
    

dict[str, str]

tilelang.utils.target.check_cuda_availability()Â¶
    

Check if CUDA is available on the system by locating the CUDA path. :returns: True if CUDA is available, False otherwise. :rtype: bool

Return type:
    

[bool](../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool")

tilelang.utils.target.check_hip_availability()Â¶
    

Check if HIP (ROCm) is available on the system by locating the ROCm path. :returns: True if HIP is available, False otherwise. :rtype: bool

Return type:
    

[bool](../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool")

tilelang.utils.target.check_metal_availability()Â¶
    

Return type:
    

[bool](../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool")

tilelang.utils.target.determine_fp8_type(_fp8_format ='e4m3'_)Â¶
    

Select the correct FP8 dtype string for the current platform. \- CUDA defaults to FP8 E4M3FN / E5M2. \- ROCm uses FNUZ except gfx950 (OCP), which prefers non-FNUZ when available.

Parameters:
    

**fp8_format** (_Literal_ _[__'e4m3'__,__'e5m2'__]_)

Return type:
    

str

tilelang.utils.target.determine_torch_fp8_type(_fp8_format ='e4m3'_)Â¶
    

Parameters:
    

**fp8_format** (_Literal_ _[__'e4m3'__,__'e5m2'__]_)

Return type:
    

torch.dtype

tilelang.utils.target.normalize_cutedsl_target(_target_)Â¶
    

Parameters:
    

**target** (_str_ _|__tvm.target.Target_)

Return type:
    

tvm.target.Target | None

tilelang.utils.target.determine_target(_target ='auto'_, _return_object =False_)Â¶
    

Determine the appropriate target for compilation (CUDA, HIP, or manual selection).

Parameters:
    

  * **target** (_Union_ _[__str_ _,__Target_ _,__Literal_ _[__"auto"__]__]_) â User-specified target. \- If âautoâ, the system will automatically detect whether CUDA or HIP is available. \- If a string or Target, it is directly validated.

  * **return_object** ([_bool_](../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool"))



Returns:
    

The selected target (âcudaâ, âhipâ, or a valid Target object).

Return type:
    

Union[str, Target]

Raises:
    

  * **ValueError** â If no CUDA or HIP is available and the target is âautoâ.

  * **AssertionError** â If the target is invalid.




tilelang.utils.target.target_is_cuda(_target_)Â¶
    

Parameters:
    

**target** (_tvm.target.Target_)

Return type:
    

[bool](../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool")

tilelang.utils.target.target_is_hip(_target_)Â¶
    

Parameters:
    

**target** (_tvm.target.Target_)

Return type:
    

[bool](../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool")

tilelang.utils.target.target_is_metal(_target_)Â¶
    

Parameters:
    

**target** (_tvm.target.Target_)

Return type:
    

[bool](../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool")

tilelang.utils.target.target_is_volta(_target_)Â¶
    

Parameters:
    

**target** (_tvm.target.Target_)

Return type:
    

[bool](../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool")

tilelang.utils.target.target_is_turing(_target_)Â¶
    

Parameters:
    

**target** (_tvm.target.Target_)

Return type:
    

[bool](../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool")

tilelang.utils.target.target_is_ampere(_target_)Â¶
    

Parameters:
    

**target** (_tvm.target.Target_)

Return type:
    

[bool](../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool")

tilelang.utils.target.target_is_hopper(_target_)Â¶
    

Parameters:
    

**target** (_tvm.target.Target_)

Return type:
    

[bool](../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool")

tilelang.utils.target.target_is_sm120(_target_)Â¶
    

Parameters:
    

**target** (_tvm.target.Target_)

Return type:
    

[bool](../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool")

tilelang.utils.target.target_is_cdna(_target_)Â¶
    

Parameters:
    

**target** (_tvm.target.Target_)

Return type:
    

[bool](../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool")

tilelang.utils.target.target_is_gfx950(_target_)Â¶
    

Parameters:
    

**target** (_tvm.target.Target_)

Return type:
    

[bool](../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool")

tilelang.utils.target.target_has_async_copy(_target_)Â¶
    

Parameters:
    

**target** (_tvm.target.Target_)

Return type:
    

[bool](../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool")

tilelang.utils.target.target_has_ldmatrix(_target_)Â¶
    

Parameters:
    

**target** (_tvm.target.Target_)

Return type:
    

[bool](../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool")

tilelang.utils.target.target_has_stmatrix(_target_)Â¶
    

Parameters:
    

**target** (_tvm.target.Target_)

Return type:
    

[bool](../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool")

tilelang.utils.target.target_has_bulk_copy(_target_)Â¶
    

Parameters:
    

**target** (_tvm.target.Target_)

Return type:
    

[bool](../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool")

tilelang.utils.target.target_get_warp_size(_target_)Â¶
    

Parameters:
    

**target** (_tvm.target.Target_)

Return type:
    

int
