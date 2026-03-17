# tilelang.jit.adapter.nvrtc.libgenÂ¶  
  
NVRTC Library Generator for TileLang.

Compiles CUDA kernels at runtime using NVRTC and manages resulting binaries.

Why NVRTC instead of nvcc: \- No offline compilation step, enables true JIT workflows \- Works without CUDA toolkit installed (only requires driver) \- Allows kernel specialization based on runtime parameters

Key responsibilities: \- Compile CUDA source to cubin using NVRTC API \- Generate accompanying Python launcher code \- Load compiled cubin and extract kernel handles \- Manage library lifecycle (load/unload)

## AttributesÂ¶

`logger` |   
---|---  
  
## ClassesÂ¶

`NVRTCLibraryGenerator` | Runtime compiler and loader for NVRTC-compiled CUDA kernels.  
---|---  
  
## Module ContentsÂ¶

tilelang.jit.adapter.nvrtc.libgen.loggerÂ¶
    

_class _tilelang.jit.adapter.nvrtc.libgen.NVRTCLibraryGenerator(_target_ , _verbose =False_)Â¶
    

Bases: [`tilelang.jit.adapter.libgen.LibraryGenerator`](../../libgen/index.html#tilelang.jit.adapter.libgen.LibraryGenerator "tilelang.jit.adapter.libgen.LibraryGenerator")

Runtime compiler and loader for NVRTC-compiled CUDA kernels.

Lifecycle:
    

  1. compile_lib(): CUDA source â cubin + Python launcher

  2. load_lib(): cubin â loaded library + kernel handles

  3. pymodule.call(): Execute kernels via Python launcher

  4. __del__: Cleanup (unload library)



Why three files (cu, cubin, py):
    

  * .cu: Source for debugging, kept in temp directory

  * .cubin: Compiled binary, loaded by CUDA driver

  * .py: Launch code, imported as Python module




Parameters:
    

  * **target** (_tvm.target.Target_)

  * **verbose** ([_bool_](../../../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool"))




host_funcÂ¶
    

Generated Python launch code (from wrapper)

culibÂ¶
    

CUDA library handle (CUlibrary)

pymoduleÂ¶
    

Imported Python module containing call() function

host_func _: str | None_ _ = None_Â¶
    

culib _: cuda.bindings.driver.CUlibrary | None_ _ = None_Â¶
    

pymodule _: types.ModuleType | None_ _ = None_Â¶
    

pypath _: str | None_ _ = None_Â¶
    

_static _import_from_file(_module_name_ , _file_path_)Â¶
    

Dynamically import Python module from file path.

Standard importlib pattern for loading modules outside sys.path. Used to import generated .py launcher code from temp directory.

Parameters:
    

  * **module_name** â Name to assign to imported module

  * **file_path** â Absolute path to .py file



Returns:
    

Imported module object

update_host_func(_host_func_)Â¶
    

Store generated Python launch code for later file write.

Called by adapter after wrapper generates the launch code. This is the bridge between code generation and file output.

Parameters:
    

**host_func** (_str_) â Python source code containing call() function

load_lib(_lib_path =None_)Â¶
    

Load compiled cubin and Python launcher into memory.

Why two loads:
    

  1. Import Python module for launch logic

  2. Load cubin via CUDA Driver API for kernel handles




Context synchronization: CUDA context must be current before loading. If not, use torch.cuda.synchronize() to establish context.

Parameters:
    

**lib_path** (_str_ _|__None_) â Path to .cubin file (optional, uses self.libpath if None)

Side effects:
    

  * Sets self.pymodule to imported Python module

  * Sets self.culib to CUDA library handle




compile_lib(_timeout =None_)Â¶
    

Compile CUDA source to cubin using NVRTC and write output files.

Output artifacts (all in temp directory):
    

  * .cu: Source code (for debugging)

  * .cubin: Compiled binary (for execution)

  * .py: Python launcher (for calling kernels)



Include paths setup:
    

  * TileLang templates: kernel primitives and utilities

  * CUTLASS: optimized GEMM/tensor ops

  * CUDA headers: driver/runtime APIs



Why architecture detection:
    

ARM64 servers (SBSA) have different header paths than x86_64.

Parameters:
    

**timeout** (_float_ _|__None_) â Compilation timeout in seconds (currently unsupported by NVRTC compiler)

Side effects:
    

  * Writes .cu, .cubin, .py files to temp directory

  * Sets self.srcpath, self.libpath, self.pypath




__del__()Â¶
    

Cleanup: unload CUDA library when object is destroyed.

Critical for resource management - CUDA libraries consume GPU memory. Failure to unload is logged but not raised (destructor canât fail).

Why explicit unload:
    

Python GC doesnât know about GPU resources, must release manually.
