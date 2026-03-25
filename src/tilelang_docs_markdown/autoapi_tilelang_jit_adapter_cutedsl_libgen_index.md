# tilelang.jit.adapter.cutedsl.libgenÂ¶

CuTeDSL Library Generator for TileLang.

This module provides library generation functionality for the CuTeDSL backend.

## ClassesÂ¶

`CuTeDSLLibraryGenerator` |   
---|---  
  
## Module ContentsÂ¶

_class _tilelang.jit.adapter.cutedsl.libgen.CuTeDSLLibraryGenerator(_target_ , _verbose =False_)Â¶
    

Bases: [`tilelang.jit.adapter.libgen.LibraryGenerator`](../../libgen/index.html#tilelang.jit.adapter.libgen.LibraryGenerator "tilelang.jit.adapter.libgen.LibraryGenerator")

Parameters:
    

  * **target** (_tvm.target.Target_)

  * **verbose** ([_bool_](../../../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool"))




host_func _: str | None_ _ = None_Â¶
    

tma_cpp_init_code _: str | None_ _ = None_Â¶
    

tma_lib_name _: str | None_ _ = None_Â¶
    

launcher_cpp_code _: str | None_ _ = None_Â¶
    

launcher_lib_name _: str | None_ _ = None_Â¶
    

pymodule _ = None_Â¶
    

_static _import_from_file(_module_name_ , _file_path_)Â¶
    

update_host_func(_host_func_)Â¶
    

Parameters:
    

**host_func** (_str_)

update_launcher_cpp_code(_launcher_cpp_code_)Â¶
    

Parameters:
    

**launcher_cpp_code** (_str_)

update_launcher_lib_name(_launcher_lib_name_)Â¶
    

Parameters:
    

**launcher_lib_name** (_str_)

load_lib(_lib_path =None_)Â¶
    

Parameters:
    

**lib_path** (_str_ _|__None_)

compile_lib(_timeout =None_)Â¶
    

Parameters:
    

**timeout** (_float_)
