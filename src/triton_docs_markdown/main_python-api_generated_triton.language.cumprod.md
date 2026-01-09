# triton.language.cumprod¶

triton.language.cumprod(_input_ , _axis =0_, _reverse =False_)¶
    

Returns the cumprod of all elements in the `input` tensor along the provided `axis`

Parameters:
    

  * **input** (_Tensor_) – the input values

  * **axis** (_int_) – the dimension along which the scan should be done

  * **reverse** (_bool_) – if true, the scan is performed in the reverse direction




This function can also be called as a member function on [`tensor`](triton.language.tensor.html#triton.language.tensor "triton.language.tensor"), as `x.cumprod(...)` instead of `cumprod(x, ...)`.
