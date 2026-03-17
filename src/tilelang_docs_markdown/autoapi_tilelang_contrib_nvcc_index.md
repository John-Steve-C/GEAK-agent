# tilelang.contrib.nvccÂ¶

Utility to invoke nvcc compiler in the system

## FunctionsÂ¶

`compile_cuda`(code[, target_format, arch, options, ...]) | Compile cuda code with NVCC from env.  
---|---  
`default_compile_options`([compile_flags]) | Build a set of default NVCC compile options for TileLang generated sources.  
`get_ptx_from_source`(code[, compile_flags, verbose]) | Compile CUDA C++ source to PTX using NVCC and return as text.  
`get_sass_from_source`(code[, compile_flags, verbose]) | Compile CUDA C++ source to CUBIN and disassemble to SASS.  
`find_cuda_path`() | Utility function to find cuda path  
`get_cuda_version`([cuda_path]) | Utility function to get cuda version  
`get_target_compute_version`([target]) | Utility function to get compute capability of compilation target.  
`parse_compute_version`(compute_version) | Parse compute capability string to divide major and minor version  
`get_target_arch`(compute_version) |   
`have_fp16`(compute_version) | Either fp16 support is provided in the compute capability or not  
`have_int8`(compute_version) | Either int8 support is provided in the compute capability or not  
`have_tensorcore`([compute_version, target]) | Either TensorCore support is provided in the compute capability or not  
`have_cudagraph`() | Either CUDA Graph support is provided  
`have_bf16`(compute_version) | Either bf16 support is provided in the compute capability or not  
`have_fp8`(compute_version) | Whether fp8 support is provided in the specified compute capability or not  
`have_tma`(target) | Whether TMA support is provided in the specified compute capability or not  
`is_hopper`(target) |   
`have_pdl`(target) |   
`get_nvcc_compiler`() | Get the path to the nvcc compiler  
  
## Module ContentsÂ¶

tilelang.contrib.nvcc.compile_cuda(_code_ , _target_format ='ptx'_, _arch =None_, _options =None_, _path_target =None_, _verbose =False_)Â¶
    

Compile cuda code with NVCC from env.

Parameters:
    

  * **code** (_str_) â The cuda code.

  * **target_format** (_str_) â The target format of nvcc compiler.

  * **arch** (_str_) â The cuda architecture.

  * **options** (_str_ _or_ _list_ _of_ _str_) â The additional options.

  * **path_target** (_str_ _,__optional_) â Output file.



Returns:
    

**cubin** â The bytearray of the cubin

Return type:
    

bytearray

tilelang.contrib.nvcc.default_compile_options(_compile_flags =None_)Â¶
    

Build a set of default NVCC compile options for TileLang generated sources.

Includes C++ standard and common include paths (TileLang templates, CUTLASS, CUDA include). Merges user-provided compile flags if given.

Parameters:
    

**compile_flags** (_Optional_ _[__List_ _[__str_ _]__]_) â Additional flags to include. Items are split on whitespace.

Returns:
    

A list of flags suitable for NVCCâs command line.

Return type:
    

List[str]

tilelang.contrib.nvcc.get_ptx_from_source(_code_ , _compile_flags =None_, _verbose =False_)Â¶
    

Compile CUDA C++ source to PTX using NVCC and return as text.

Parameters:
    

  * **code** (_str_) â CUDA C++ kernel source code.

  * **compile_flags** (_Optional_ _[__List_ _[__str_ _]__]_) â Additional flags merged with defaults.

  * **verbose** ([_bool_](../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool")) â Print NVCC output when True.



Returns:
    

PTX text.

Return type:
    

str

tilelang.contrib.nvcc.get_sass_from_source(_code_ , _compile_flags =None_, _verbose =False_)Â¶
    

Compile CUDA C++ source to CUBIN and disassemble to SASS.

Uses nvdisasm if available; otherwise falls back to cuobjdump.

Parameters:
    

  * **code** (_str_) â CUDA C++ kernel source code.

  * **compile_flags** (_Optional_ _[__List_ _[__str_ _]__]_) â Additional flags merged with defaults.

  * **verbose** ([_bool_](../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool")) â Print tool outputs when True.



Returns:
    

SASS text.

Return type:
    

str

tilelang.contrib.nvcc.find_cuda_path()Â¶
    

Utility function to find cuda path

Returns:
    

**path** â Path to cuda root.

Return type:
    

str

tilelang.contrib.nvcc.get_cuda_version(_cuda_path =None_)Â¶
    

Utility function to get cuda version

Parameters:
    

**cuda_path** (_Optional_ _[__str_ _]_) â Path to cuda root. If None is passed, will use find_cuda_path() as default.

Returns:
    

**version** â The cuda version

Return type:
    

float

tilelang.contrib.nvcc.get_target_compute_version(_target =None_)Â¶
    

Utility function to get compute capability of compilation target.

Looks for the target arch in three different places, first in the target input, then the Target.current() scope, and finally the GPU device (if it exists).

Parameters:
    

**target** (_tvm.target.Target_ _,__optional_) â The compilation target

Returns:
    

**compute_version** â compute capability of a GPU (e.g. â8.6â or â9.0â)

Return type:
    

str

tilelang.contrib.nvcc.parse_compute_version(_compute_version_)Â¶
    

Parse compute capability string to divide major and minor version

Parameters:
    

**compute_version** (_str_) â compute capability of a GPU (e.g. â6.0â)

Returns:
    

  * **major** (_int_) â major version number

  * **minor** (_int_) â minor version number




Return type:
    

tuple[int, int]

tilelang.contrib.nvcc.get_target_arch(_compute_version_)Â¶
    

Parameters:
    

**compute_version** (_str_ _|__tuple_ _[__int_ _,__int_ _]_)

Return type:
    

str

tilelang.contrib.nvcc.have_fp16(_compute_version_)Â¶
    

Either fp16 support is provided in the compute capability or not

Parameters:
    

**compute_version** (_str_) â compute capability of a GPU (e.g. â6.0â)

tilelang.contrib.nvcc.have_int8(_compute_version_)Â¶
    

Either int8 support is provided in the compute capability or not

Parameters:
    

**compute_version** (_str_) â compute capability of a GPU (e.g. â6.1â)

tilelang.contrib.nvcc.have_tensorcore(_compute_version =None_, _target =None_)Â¶
    

Either TensorCore support is provided in the compute capability or not

Parameters:
    

  * **compute_version** (_str_ _,__optional_) â compute capability of a GPU (e.g. â7.0â).

  * **target** (_tvm.target.Target_ _,__optional_) â The compilation target, will be used to determine arch if compute_version isnât specified.




tilelang.contrib.nvcc.have_cudagraph()Â¶
    

Either CUDA Graph support is provided

tilelang.contrib.nvcc.have_bf16(_compute_version_)Â¶
    

Either bf16 support is provided in the compute capability or not

Parameters:
    

**compute_version** (_str_) â compute capability of a GPU (e.g. â8.0â)

tilelang.contrib.nvcc.have_fp8(_compute_version_)Â¶
    

Whether fp8 support is provided in the specified compute capability or not

Parameters:
    

**compute_version** (_str_) â GPU capability

tilelang.contrib.nvcc.have_tma(_target_)Â¶
    

Whether TMA support is provided in the specified compute capability or not

Parameters:
    

**target** (_tvm.target.Target_) â The compilation target

tilelang.contrib.nvcc.is_hopper(_target_)Â¶
    

tilelang.contrib.nvcc.have_pdl(_target_)Â¶
    

tilelang.contrib.nvcc.get_nvcc_compiler()Â¶
    

Get the path to the nvcc compiler

Return type:
    

str
