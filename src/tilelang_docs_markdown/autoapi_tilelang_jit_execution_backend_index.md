# tilelang.jit.execution_backendÂ¶

## FunctionsÂ¶

`allowed_backends_for_target`(target, *[, ...]) | Return allowed execution backends for a given TVM target kind.  
---|---  
`resolve_execution_backend`(requested, target) | Resolve an execution backend string to a concrete backend.  
  
## Module ContentsÂ¶

tilelang.jit.execution_backend.allowed_backends_for_target(_target_ , _*_ , _include_unavailable =True_)Â¶
    

Return allowed execution backends for a given TVM target kind.

include_unavailable: if False, this will filter out backends that are known to be unavailable at runtime (e.g., NVRTC without cuda-python installed).

Parameters:
    

  * **target** (_tvm.target.Target_)

  * **include_unavailable** ([_bool_](../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool"))



Return type:
    

list[str]

tilelang.jit.execution_backend.resolve_execution_backend(_requested_ , _target_)Â¶
    

Resolve an execution backend string to a concrete backend.

  * Supports the alias âdlpackâ -> âtvm_ffiâ.

  * Supports the sentinel âautoâ which selects a sensible default per target.

  * Validates the combination (target, backend) and raises with helpful alternatives when invalid.




Parameters:
    

  * **requested** (_str_ _|__None_)

  * **target** (_tvm.target.Target_)



Return type:
    

str
