# tilelang.contrib.ccÂ¶

Util to invoke C/C++ compilers in the system.

## FunctionsÂ¶

`get_cc`() | Return the path to the default C/C++ compiler.  
---|---  
`get_cplus_compiler`() | Return the path to the default C/C++ compiler.  
`is_darwin`() |   
`create_shared`(output, objects[, options, cc, cwd, ...]) | Create shared library.  
`create_staticlib`(output, inputs[, ar]) | Create static library.  
`create_executable`(output, objects[, options, cc, cwd, ...]) | Create executable binary.  
`get_global_symbol_section_map`(path, *[, nm]) | Get global symbols from a library via nm -g  
`get_target_by_dump_machine`(compiler) | Functor of get_target_triple that can get the target triple using compiler.  
`cross_compiler`(compile_func[, options, output_format, ...]) | Create a cross compiler function by specializing compile_func with options.  
  
## Module ContentsÂ¶

tilelang.contrib.cc.get_cc()Â¶
    

Return the path to the default C/C++ compiler.

Returns:
    

**out** â The path to the default C/C++ compiler, or None if none was found.

Return type:
    

Optional[str]

tilelang.contrib.cc.get_cplus_compiler()Â¶
    

Return the path to the default C/C++ compiler.

Returns:
    

**out** â The path to the default C/C++ compiler, or None if none was found.

Return type:
    

Optional[str]

tilelang.contrib.cc.is_darwin()Â¶
    

tilelang.contrib.cc.create_shared(_output_ , _objects_ , _options =None_, _cc =None_, _cwd =None_, _ccache_env =None_)Â¶
    

Create shared library.

Parameters:
    

  * **output** (_str_) â The target shared library.

  * **objects** (_List_ _[__str_ _]_) â List of object files.

  * **options** (_List_ _[__str_ _]_) â The list of additional options string.

  * **cc** (_Optional_ _[__str_ _]_) â The compiler command.

  * **cwd** (_Optional_ _[__str_ _]_) â The current working directory.

  * **ccache_env** (_Optional_ _[__Dict_ _[__str_ _,__str_ _]__]_) â The environment variable for ccache. Set None to disable ccache by default.




tilelang.contrib.cc.create_staticlib(_output_ , _inputs_ , _ar =None_)Â¶
    

Create static library.

Parameters:
    

  * **output** (_str_) â The target shared library.

  * **inputs** (_List_ _[__str_ _]_) â List of inputs files. Each input file can be a tarball of objects or an object file.

  * **ar** (_Optional_ _[__str_ _]_) â Path to the ar command to be used




tilelang.contrib.cc.create_executable(_output_ , _objects_ , _options =None_, _cc =None_, _cwd =None_, _ccache_env =None_)Â¶
    

Create executable binary.

Parameters:
    

  * **output** (_str_) â The target executable.

  * **objects** (_List_ _[__str_ _]_) â List of object files.

  * **options** (_List_ _[__str_ _]_) â The list of additional options string.

  * **cc** (_Optional_ _[__str_ _]_) â The compiler command.

  * **cwd** (_Optional_ _[__str_ _]_) â The urrent working directory.

  * **ccache_env** (_Optional_ _[__Dict_ _[__str_ _,__str_ _]__]_) â The environment variable for ccache. Set None to disable ccache by default.




tilelang.contrib.cc.get_global_symbol_section_map(_path_ , _*_ , _nm =None_)Â¶
    

Get global symbols from a library via nm -g

Parameters:
    

  * **path** (_str_) â The library path

  * **nm** (_str_) â The path to nm command



Returns:
    

**symbol_section_map** â A map from defined global symbol to their sections

Return type:
    

Dict[str, str]

tilelang.contrib.cc.get_target_by_dump_machine(_compiler_)Â¶
    

Functor of get_target_triple that can get the target triple using compiler.

Parameters:
    

**compiler** (_Optional_ _[__str_ _]_) â The compiler.

Returns:
    

**out** â A function that can get target triple according to dumpmachine option of compiler.

Return type:
    

Callable

tilelang.contrib.cc.cross_compiler(_compile_func_ , _options =None_, _output_format =None_, _get_target_triple =None_, _add_files =None_)Â¶
    

Create a cross compiler function by specializing compile_func with options.

This function can be used to construct compile functions that can be passed to AutoTVM measure or export_library.

Parameters:
    

  * **compile_func** (_Union_ _[__str_ _,__Callable_ _[__[__str_ _,__str_ _,__Optional_ _[__str_ _]__]__,__None_ _]__]_) â Function that performs the actual compilation

  * **options** (_Optional_ _[__List_ _[__str_ _]__]_) â List of additional optional string.

  * **output_format** (_Optional_ _[__str_ _]_) â Library output format.

  * **get_target_triple** (_Optional_ _[__Callable_ _]_) â Function that can target triple according to dumpmachine option of compiler.

  * **add_files** (_Optional_ _[__List_ _[__str_ _]__]_) â List of paths to additional object, source, library files to pass as part of the compilation.



Returns:
    

**fcompile** â A compilation function that can be passed to export_library.

Return type:
    

Callable[[str, str, Optional[str]], None]

Examples
    
    
    from tvm.contrib import cc, ndk
    # export using arm gcc
    mod = build_runtime_module()
    mod.export_library(path_dso,
                       fcompile=cc.cross_compiler("arm-linux-gnueabihf-gcc"))
    # specialize ndk compilation options.
    specialized_ndk = cc.cross_compiler(
        ndk.create_shared,
        ["--sysroot=/path/to/sysroot", "-shared", "-fPIC", "-lm"])
    mod.export_library(path_dso, fcompile=specialized_ndk)
    
