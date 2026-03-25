# tilelang.contrib.nvrtcÂ¶

## FunctionsÂ¶

`get_nvrtc_version`() |   
---|---  
`compile_cuda`(code[, target_format, arch, options, verbose]) | Compile cuda code with NVRTC.  
  
## Module ContentsÂ¶

tilelang.contrib.nvrtc.get_nvrtc_version()Â¶
    

Return type:
    

tuple[int, int]

tilelang.contrib.nvrtc.compile_cuda(_code_ , _target_format ='ptx'_, _arch =None_, _options =None_, _verbose =False_)Â¶
    

Compile cuda code with NVRTC.

Parameters:
    

  * **code** (_str_) â The cuda code.

  * **target_format** (_Literal_ _[__"ptx"__,__"cubin"__]_) â The target format of nvrtc compiler.

  * **arch** (_Optional_ _[__int_ _]_) â The cuda architecture code.

  * **options** (_Optional_ _[__Union_ _[__str_ _,__List_ _[__str_ _]__]__]_) â The additional options.

  * **verbose** ([_bool_](../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool")) â Whether to print the verbose output.



Returns:
    

**result_bytes** â The bytearray of the cubin or ptx code.

Return type:
    

bytearray
