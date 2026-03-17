# tilelang.jit.adapter.libgenÂ¶

## AttributesÂ¶

`logger` |   
---|---  
  
## ClassesÂ¶

`LibraryGenerator` |   
---|---  
  
## Module ContentsÂ¶

tilelang.jit.adapter.libgen.loggerÂ¶
    

_class _tilelang.jit.adapter.libgen.LibraryGenerator(_target_ , _verbose =False_)Â¶
    

Parameters:
    

  * **target** (_tvm.target.Target_)

  * **verbose** ([_bool_](../../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool"))




srcpath _: str | None_ _ = None_Â¶
    

libpath _: str | None_ _ = None_Â¶
    

lib_code _: str | None_ _ = None_Â¶
    

pass_configs _: dict[str, Any] | None_ _ = None_Â¶
    

compile_flags _: list[str] | None_ _ = None_Â¶
    

targetÂ¶
    

verbose _ = False_Â¶
    

assign_pass_configs(_pass_configs =None_)Â¶
    

Parameters:
    

**pass_configs** (_dict_ _[__str_ _,__Any_ _]__|__None_)

assign_compile_flags(_compile_flags =None_)Â¶
    

Parameters:
    

**compile_flags** (_list_ _[__str_ _]__|__None_)

update_lib_code(_lib_code_)Â¶
    

Parameters:
    

**lib_code** (_str_)

load_lib(_lib_path =None_)Â¶
    

Parameters:
    

**lib_path** (_str_ _|__None_)

compile_lib(_timeout =None_)Â¶
    

Parameters:
    

**timeout** (_float_)

remove_lib()Â¶
    

get_source_path()Â¶
    

get_lib_path()Â¶
    

set_lib_path(_libpath_)Â¶
    

set_src_path(_srcpath_)Â¶
    
