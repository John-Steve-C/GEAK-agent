# triton.jit¶

triton.jit(_fn : T_) → JITFunction[T]¶
triton.jit(_*_ , _version =None_, _repr : Callable | None = None_, _launch_metadata : Callable | None = None_, _do_not_specialize : Iterable[int | str] | None = None_, _do_not_specialize_on_alignment : Iterable[int | str] | None = None_, _debug : bool | None = None_, _noinline : bool | None = None_) → Callable[[T], JITFunction[T]]
    

Decorator for JIT-compiling a function using the Triton compiler.

Note:
    

When a jit’d function is called, arguments are implicitly converted to pointers if they have a `.data_ptr()` method and a .dtype attribute.

Note:
    

This function will be compiled and run on the GPU. It will only have access to:

  * python primitives,

  * builtins within the triton package,

  * arguments to this function,

  * other jit’d functions



Parameters:
    

**fn** (_Callable_) – the function to be jit-compiled
