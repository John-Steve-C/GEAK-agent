# triton.language.permute¶

triton.language.permute(_input_ , _* dims_, __semantic =None_)¶
    

Permutes the dimensions of a tensor.

Parameters:
    

  * **input** (_Block_) – The input tensor.

  * **dims** – The desired ordering of dimensions. For example, `(2, 1, 0)` reverses the order dims in a 3D tensor.




`dims` can be passed as a tuple or as individual parameters:
    
    
    # These are equivalent
    permute(x, (2, 1, 0))
    permute(x, 2, 1, 0)
    

[`trans()`](triton.language.trans.html#triton.language.trans "triton.language.trans") is equivalent to this function, except when `dims` is empty, it tries to swap the last two axes.

This function can also be called as a member function on [`tensor`](triton.language.tensor.html#triton.language.tensor "triton.language.tensor"), as `x.permute(...)` instead of `permute(x, ...)`.
