# Python CompatibilityÂ¶

TileLang is a Python-embedded DSL, but not all Python syntax is supported inside TileLang DSL. This guide clarifies what works, what doesnât, and how to translate common Python patterns into TileLang equivalents. Specially, we focus on the kernel part (scripts inside `with T.Kernel`) semantics. For host-side semantics when using eager-style JIT, please stay tuned for our upcoming documentation.

The following codes use the conventional aliases:
    
    
    import tilelang
    import tilelang.language as T
    from tilelang import jit
    

## Control Flow & LoopsÂ¶

Python Feature | Supported | Notes / Alternative  
---|---|---  
`for i in range(n)` | â  | Maps to `T.serial(n)`  
`for i in range(a,b,s)` | â  | Maps to `T.serial(a, b, s)`  
`for x in list` | â | Use index-based loop  
`while condition` | â  |   
`if` / `elif` / `else` | â  |   
`x if cond else y` | â  | Ternary expression  
`break` / `continue` | â  |   
`enumerate()` / `zip()` | â |   
  
## Data AccessÂ¶

Python Feature | Supported | Notes / Alternative  
---|---|---  
`a[i]` indexing | â  | Multi-dim indexing supported: `a[i, j, k]`  
`a[i:j]` slicing | â  | Creates `BufferRegion`  
`a[-1]` negative index | â  |   
  
## Assignment & Arithmetic OperationsÂ¶

Python Feature | Supported | Notes / Alternative  
---|---|---  
`x = expr` | â  |   
`+`, `-`, `*`, `/`, `%` | â  | Maps to device-side arithmetic operations  
`+=`, `-=`, `*=`, etc. | â  | Augmented assignment  
`a = b = c` | â | Use separate assignments  
  
## Functions & ClassesÂ¶

As a kernel script language, TileLang doesnât support functions or classes. You can use `@T.macro` to define reusable code blocks, which will be inlined at compile time like `__device__` function.

## Statements & Built-in FunctionsÂ¶

Python Feature | Supported | Notes / Alternative  
---|---|---  
`with` | â ï¸ | Only `T.Kernel`, `T.ws`  
`assert` | â ï¸ | Use `T.device_assert` or `T.assert`  
`print()` | â ï¸ | Use `T.print()`; `print` works for Python expressions  
`len()` | â | Use `buffer.shape[dim]`  
`type()`, `isinstance()` | â | 
