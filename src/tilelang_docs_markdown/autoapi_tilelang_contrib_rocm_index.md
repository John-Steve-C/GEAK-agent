# tilelang.contrib.rocmÂ¶

Utility for ROCm backend

## FunctionsÂ¶

`find_lld`([required]) | Find ld.lld in system.  
---|---  
`rocm_link`(in_file, out_file[, lld]) | Link relocatable ELF object to shared ELF object using lld  
`callback_rocm_link`(obj_bin) | Links object file generated from LLVM to HSA Code Object  
`callback_rocm_bitcode_path`([rocdl_dir]) | Utility function to find ROCm device library bitcodes  
`parse_compute_version`(compute_version) | Parse compute capability string to divide major and minor version  
`have_matrixcore`([compute_version]) | Either MatrixCore support is provided in the compute capability or not  
`get_rocm_arch`([rocm_path]) | Utility function to get the AMD GPU architecture  
`find_rocm_path`() | Utility function to find ROCm path  
  
## Module ContentsÂ¶

tilelang.contrib.rocm.find_lld(_required =True_)Â¶
    

Find ld.lld in system.

Parameters:
    

**required** ([_bool_](../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool")) â Whether it is required, runtime error will be raised if the compiler is required.

Returns:
    

**valid_list** â List of possible paths.

Return type:
    

list of str

Note

This function will first search ld.lld that matches the major llvm version that built with tvm

tilelang.contrib.rocm.rocm_link(_in_file_ , _out_file_ , _lld =None_)Â¶
    

Link relocatable ELF object to shared ELF object using lld

Parameters:
    

  * **in_file** (_str_) â Input file name (relocatable ELF object file)

  * **out_file** (_str_) â Output file name (shared ELF object file)

  * **lld** (_str_ _,__optional_) â The lld linker, if not specified, we will try to guess the matched clang version.




tilelang.contrib.rocm.callback_rocm_link(_obj_bin_)Â¶
    

Links object file generated from LLVM to HSA Code Object

Parameters:
    

**obj_bin** (_bytearray_) â The object file

Returns:
    

**cobj_bin** â The HSA Code Object

Return type:
    

bytearray

tilelang.contrib.rocm.callback_rocm_bitcode_path(_rocdl_dir =None_)Â¶
    

Utility function to find ROCm device library bitcodes

Parameters:
    

**rocdl_dir** (_str_) â The path to rocm library directory The default value is the standard location

tilelang.contrib.rocm.parse_compute_version(_compute_version_)Â¶
    

Parse compute capability string to divide major and minor version

Parameters:
    

**compute_version** (_str_) â compute capability of a GPU (e.g. â6.0â)

Returns:
    

  * **major** (_int_) â major version number

  * **minor** (_int_) â minor version number




tilelang.contrib.rocm.have_matrixcore(_compute_version =None_)Â¶
    

Either MatrixCore support is provided in the compute capability or not

Parameters:
    

**compute_version** (_str_ _,__optional_) â compute capability of a GPU (e.g. â7.0â).

Returns:
    

**have_matrixcore** â True if MatrixCore support is provided, False otherwise

Return type:
    

[bool](../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool")

tilelang.contrib.rocm.get_rocm_arch(_rocm_path ='/opt/rocm'_)Â¶
    

Utility function to get the AMD GPU architecture

Parameters:
    

**rocm_path** (_str_) â The path to rocm installation directory

Returns:
    

**gpu_arch** â The AMD GPU architecture

Return type:
    

str

tilelang.contrib.rocm.find_rocm_path()Â¶
    

Utility function to find ROCm path

Returns:
    

**path** â Path to ROCm root.

Return type:
    

str
