# triton.language.expand_dims¶

triton.language.expand_dims(_input_ , _axis_ , __semantic =None_)¶
    

Expand the shape of a tensor, by inserting new length-1 dimensions.

Axis indices are with respect to the resulting tensor, so `result.shape[axis]` will be 1 for each axis.

Parameters:
    

  * **input** (_tl.tensor_) – The input tensor.

  * **axis** (_int_ _|__Sequence_ _[__int_ _]_) – The indices to add new axes




This function can also be called as a member function on [`tensor`](triton.language.tensor.html#triton.language.tensor "triton.language.tensor"), as `x.expand_dims(...)` instead of `expand_dims(x, ...)`.
