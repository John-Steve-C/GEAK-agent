# triton.language.argmax¶

triton.language.argmax(_input_ , _axis_ , _tie_break_left =True_, _keep_dims =False_)¶
    

Returns the maximum index of all elements in the `input` tensor along the provided `axis`

Parameters:
    

  * **input** (_Tensor_) – the input values

  * **axis** (_int_) – the dimension along which the reduction should be done. If None, reduce all dimensions

  * **keep_dims** (_bool_) – if true, keep the reduced dimensions with length 1

  * **tie_break_left** (_bool_) – if true, in case of a tie (i.e., multiple elements have the same maximum index value), return the left-most index for values that aren’t NaN




This function can also be called as a member function on [`tensor`](triton.language.tensor.html#triton.language.tensor "triton.language.tensor"), as `x.argmax(...)` instead of `argmax(x, ...)`.
