# triton.language.trans¶

triton.language.trans(_input : [tensor](triton.language.tensor.html#triton.language.tensor "triton.language.core.tensor")_, _* dims_, __semantic =None_)¶
    

Permutes the dimensions of a tensor.

If the parameter `dims` is not specified, the function defaults to swapping the last two axes, thereby performing an (optionally batched) 2D transpose.

Parameters:
    

  * **input** – The input tensor.

  * **dims** – The desired ordering of dimensions. For example, `(2, 1, 0)` reverses the order dims in a 3D tensor.




`dims` can be passed as a tuple or as individual parameters:
    
    
    # These are equivalent
    trans(x, (2, 1, 0))
    trans(x, 2, 1, 0)
    

[`permute()`](triton.language.permute.html#triton.language.permute "triton.language.permute") is equivalent to this function, except it doesn’t have the special case when no permutation is specified.

This function can also be called as a member function on [`tensor`](triton.language.tensor.html#triton.language.tensor "triton.language.tensor"), as `x.trans(...)` instead of `trans(x, ...)`.
