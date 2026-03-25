# tilelang.jit.adapter.cutedsl.checksÂ¶

## FunctionsÂ¶

`check_cutedsl_available`() | Fail fast if the CuTeDSL backend cannot be used in this Python environment.  
---|---  
  
## Module ContentsÂ¶

tilelang.jit.adapter.cutedsl.checks.check_cutedsl_available()Â¶
    

Fail fast if the CuTeDSL backend cannot be used in this Python environment.

Policy: \- If the public distribution nvidia-cutlass-dsl is installed, require version >= a minimum supported version. \- Regardless of distribution metadata, require that cutlass.cute is importable.

This intentionally does not mention or special-case any internal distributions.

Return type:
    

None
