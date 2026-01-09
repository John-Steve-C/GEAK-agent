# triton.language.associative_scan¶

triton.language.associative_scan(_input_ , _axis_ , _combine_fn_ , _reverse =False_, __semantic =None_, __generator =None_)¶
    

Applies the combine_fn to each elements with a carry in `input` tensors along the provided `axis` and update the carry

Parameters:
    

  * **input** (_Tensor_) – the input tensor, or tuple of tensors

  * **axis** (_int_) – the dimension along which the reduction should be done

  * **combine_fn** (_Callable_) – a function to combine two groups of scalar tensors (must be marked with @triton.jit)

  * **reverse** (_bool_) – whether to apply the associative scan in the reverse direction along axis




This function can also be called as a member function on [`tensor`](triton.language.tensor.html#triton.language.tensor "triton.language.tensor"), as `x.associative_scan(...)` instead of `associative_scan(x, ...)`.
