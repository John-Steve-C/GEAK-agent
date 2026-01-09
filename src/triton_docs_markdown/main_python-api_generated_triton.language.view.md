# triton.language.view¶  
  
triton.language.view(_input_ , _* shape_, __semantic =None_)¶
    

Returns a tensor with the same elements as input but a different shape. The order of the elements may not be preserved.

Parameters:
    

  * **input** (_Block_) – The input tensor.

  * **shape** – The desired shape.




`shape` can be passed as a tuple or as individual parameters:
    
    
    # These are equivalent
    view(x, (32, 32))
    view(x, 32, 32)
    

This function can also be called as a member function on [`tensor`](triton.language.tensor.html#triton.language.tensor "triton.language.tensor"), as `x.view(...)` instead of `view(x, ...)`.
