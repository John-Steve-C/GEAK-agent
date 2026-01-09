# triton.language.static_print¶

triton.language.static_print(_* values_, _sep : str = ' '_, _end : str = '\n'_, _file =None_, _flush =False_, __semantic =None_)¶
    

Print the values at compile time. The parameters are the same as the builtin `print`.

NOTE: Calling the Python builtin `print` is not the same as calling this, it instead maps to `device_print`, which has special requirements for the arguments.
    
    
    tl.static_print(f"BLOCK_SIZE={BLOCK_SIZE}")
    
