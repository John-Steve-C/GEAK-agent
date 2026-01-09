# triton.language.gather¶

triton.language.gather(_src_ , _index_ , _axis_ , __semantic =None_)¶
    

Gather from a tensor along a given dimension.

Parameters:
    

  * **src** (_Tensor_) – the source tensor

  * **index** (_Tensor_) – the index tensor

  * **axis** (_int_) – the dimension to gather along




This function can also be called as a member function on [`tensor`](triton.language.tensor.html#triton.language.tensor "triton.language.tensor"), as `x.gather(...)` instead of `gather(x, ...)`.
