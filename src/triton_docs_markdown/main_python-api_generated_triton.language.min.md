# triton.language.min¶

triton.language.min(_input_ , _axis =None_, _return_indices =False_, _return_indices_tie_break_left =True_, _keep_dims =False_)¶
    

Returns the minimum of all elements in the `input` tensor along the provided `axis`

Parameters:
    

  * **input** (_Tensor_) – the input values

  * **axis** (_int_) – the dimension along which the reduction should be done. If None, reduce all dimensions

  * **keep_dims** (_bool_) – if true, keep the reduced dimensions with length 1

  * **return_indices** (_bool_) – if true, return index corresponding to the minimum value

  * **return_indices_tie_break_left** (_bool_) – if true, in case of a tie (i.e., multiple elements have the same minimum value), return the left-most index for values that aren’t NaN




This function can also be called as a member function on [`tensor`](triton.language.tensor.html#triton.language.tensor "triton.language.tensor"), as `x.min(...)` instead of `min(x, ...)`.
