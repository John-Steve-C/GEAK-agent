# Debugging Triton¶

This tutorial provides guidance for debugging Triton programs. It is mostly documented for Triton users. Developers interested in exploring Triton’s backend, including MLIR code transformation and LLVM code generation, can refer to this [section](https://github.com/triton-lang/triton?tab=readme-ov-file#tips-for-hacking) to explore debugging options.

## Using Triton’s Debugging Operations¶

Triton includes four debugging operators that allow users to check and inspect tensor values:

  * `static_print` and `static_assert` are intended for compile-time debugging.

  * `device_print` and `device_assert` are used for runtime debugging.




`device_assert` executes only when `TRITON_DEBUG` is set to `1`. Other debugging operators execute regardless of the value of `TRITON_DEBUG`.

## Using the Interpreter¶

The interpreter is a straightforward and helpful tool for debugging Triton programs. It allows Triton users to run Triton programs on the CPU and inspect the intermediate results of each operation. To enable the interpreter mode, set the environment variable `TRITON_INTERPRET` to `1`. This setting causes all Triton kernels to bypass compilation and be simulated by the interpreter using numpy equivalents of Triton operations. The interpreter processes each Triton program instance sequentially, executing operations one at a time.

There are three primary ways to use the interpreter:

  * Print the intermediate results of each operation using the Python `print` function. To inspect an entire tensor, use `print(tensor)`. To examine individual tensor values at `idx`, use `print(tensor.handle.data[idx])`.

  * Attach `pdb` for step-by-step debugging of the Triton program:
        
        TRITON_INTERPRET=1 pdb main.py
        b main.py:<line number>
        r
        

  * Import the `pdb` package and set breakpoints in the Triton program:
        
        import triton
        import triton.language as tl
        import pdb
        
        @triton.jit
        def kernel(x_ptr, y_ptr, BLOCK_SIZE: tl.constexpr):
          pdb.set_trace()
          offs = tl.arange(0, BLOCK_SIZE)
          x = tl.load(x_ptr + offs)
          tl.store(y_ptr + offs, x)
        




### Limitations¶

The interpreter has several known limitations:

  * It does not support operations on `bfloat16` numeric types. To perform operations on `bfloat16` tensors, use `tl.cast(tensor)` to convert the tensor to `float32`.

  * It does not support indirect memory access patterns such as:
        
        ptr = tl.load(ptr)
        x = tl.load(ptr)
        




## Using Third-party Tools¶

For debugging on NVIDIA GPUs, [compute-sanitizer](https://docs.nvidia.com/cuda/compute-sanitizer/index.html) is an effective tool for checking data races and memory access issues. To use it, prepend `compute-sanitizer` to your command to run the Triton program.

For debugging on AMD GPUs, you may want to try the LLVM [AddressSanitizer](https://rocm.docs.amd.com/projects/llvm-project/en/latest/conceptual/using-gpu-sanitizer.html) for ROCm.

For detailed visualization of memory access in Triton programs, consider using the [triton-viz](https://github.com/Deep-Learning-Profiling-Tools/triton-viz) tool, which is agnostic to the underlying GPUs.
