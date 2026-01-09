# triton.language.device_assert¶

triton.language.device_assert(_cond_ , _msg =''_, _mask =None_, __semantic =None_)¶
    

Assert the condition at runtime from the device. Requires that the environment variable `TRITON_DEBUG` is set to a value besides `0` in order for this to have any effect.

Using the Python `assert` statement is the same as calling this function, except that the second argument must be provided and must be a string, e.g. `assert pid == 0, "pid != 0"`. The environment variable must be set for this `assert` statement to have any effect.
    
    
    tl.device_assert(pid == 0)
    assert pid == 0, f"pid != 0"
    

Parameters:
    

  * **cond** – the condition to assert. This is required to be a boolean tensor.

  * **msg** – the message to print if the assertion fails. This is required to be a string literal.



