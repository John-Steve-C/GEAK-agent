# triton.language.static_assert¶

triton.language.static_assert(_cond_ , _msg =''_, __semantic =None_)¶
    

Assert the condition at compile time. Does not require that the `TRITON_DEBUG` environment variable is set.
    
    
    tl.static_assert(BLOCK_SIZE == 1024)
    
