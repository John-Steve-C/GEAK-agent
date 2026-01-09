# triton.heuristics¶

triton.heuristics(_values_)¶
    

Decorator for specifying how the values of certain meta-parameters may be computed. This is useful for cases where auto-tuning is prohibitively expensive, or just not applicable.
    
    
    # smallest power-of-two >= x_size
    @triton.heuristics(values={'BLOCK_SIZE': lambda args: triton.next_power_of_2(args['x_size'])})
    @triton.jit
    def kernel(x_ptr, x_size, BLOCK_SIZE: tl.constexpr):
        ...
    

Parameters:
    

**values** (_dict_ _[__str_ _,__Callable_ _[__[__dict_ _[__str_ _,__Any_ _]__]__,__Any_ _]__]_) – a dictionary of meta-parameter names and functions that compute the value of the meta-parameter. each such function takes a list of positional arguments as input.
