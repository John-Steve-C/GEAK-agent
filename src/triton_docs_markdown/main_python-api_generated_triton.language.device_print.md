# triton.language.device_print¶

triton.language.device_print(_prefix_ , _* args_, _hex =False_, __semantic =None_)¶
    

Print the values at runtime from the device. String formatting does not work for runtime values, so you should provide the values you want to print as arguments. The first value must be a string, all following values must be scalars or tensors.

Calling the Python builtin `print` is the same as calling this function, and the requirements for the arguments will match this function (not the normal requirements for `print`).
    
    
    tl.device_print("pid", pid)
    print("pid", pid)
    

On CUDA, printfs are streamed through a buffer of limited size (on one host, we measured the default as 6912 KiB, but this may not be consistent across GPUs and CUDA versions). If you notice some printfs are being dropped, you can increase the buffer size by calling
    
    
    triton.runtime.driver.active.utils.set_printf_fifo_size(size_bytes)
    

CUDA may raise an error if you try to change this value after running a kernel that uses printfs. The value set here may only affect the current device (so if you have multiple GPUs, you’d need to call it multiple times).

Parameters:
    

  * **prefix** – a prefix to print before the values. This is required to be a string literal.

  * **args** – the values to print. They can be any tensor or scalar.

  * **hex** – print all values as hex instead of decimal



