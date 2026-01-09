# triton.language.reshape¶

triton.language.reshape(_input_ , _* shape_, _can_reorder =False_, __semantic =None_, __generator =None_)¶
    

Returns a tensor with the same number of elements as input but with the provided shape.

Parameters:
    

  * **input** (_Block_) – The input tensor.

  * **shape** – The new shape.




`shape` can be passed as a tuple or as individual parameters:
    
    
    # These are equivalent
    reshape(x, (32, 32))
    reshape(x, 32, 32)
    

This function can also be called as a member function on [`tensor`](triton.language.tensor.html#triton.language.tensor "triton.language.tensor"), as `x.reshape(...)` instead of `reshape(x, ...)`.
