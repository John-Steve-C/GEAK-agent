# triton.language.xor_sum¶

triton.language.xor_sum(_input_ , _axis =None_, _keep_dims =False_)¶
    

Returns the xor sum of all elements in the `input` tensor along the provided `axis`

Parameters:
    

  * **input** (_Tensor_) – the input values

  * **axis** (_int_) – the dimension along which the reduction should be done. If None, reduce all dimensions

  * **keep_dims** (_bool_) – if true, keep the reduced dimensions with length 1




This function can also be called as a member function on [`tensor`](triton.language.tensor.html#triton.language.tensor "triton.language.tensor"), as `x.xor_sum(...)` instead of `xor_sum(x, ...)`.
