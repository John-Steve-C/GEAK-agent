# triton.language.arange¶

triton.language.arange(_start_ , _end_ , __semantic =None_)¶
    

Returns contiguous values within the half-open interval `[start, end)`. `end - start` must be less than or equal to `TRITON_MAX_TENSOR_NUMEL = 1048576`

Parameters:
    

  * **start** (_int32_) – Start of the interval. Must be a power of two.

  * **end** (_int32_) – End of the interval. Must be a power of two greater than `start`.



