# triton.language.broadcast_to¶

triton.language.broadcast_to(_input_ , _* shape_, __semantic =None_)¶
    

Tries to broadcast the given tensor to a new `shape`.

Parameters:
    

  * **input** (_Block_) – The input tensor.

  * **shape** – The desired shape.




`shape` can be passed as a tuple or as individual parameters:
    
    
    # These are equivalent
    broadcast_to(x, (32, 32))
    broadcast_to(x, 32, 32)
    

This function can also be called as a member function on [`tensor`](triton.language.tensor.html#triton.language.tensor "triton.language.tensor"), as `x.broadcast_to(...)` instead of `broadcast_to(x, ...)`.
