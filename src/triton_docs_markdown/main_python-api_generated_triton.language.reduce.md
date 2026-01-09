# triton.language.reduce¶

triton.language.reduce(_input_ , _axis_ , _combine_fn_ , _keep_dims =False_, __semantic =None_, __generator =None_)¶
    

Applies the combine_fn to all elements in `input` tensors along the provided `axis`

Parameters:
    

  * **input** (_Tensor_) – the input tensor, or tuple of tensors

  * **axis** (_int_ _|__None_) – the dimension along which the reduction should be done. If None, reduce all dimensions

  * **combine_fn** (_Callable_) – a function to combine two groups of scalar tensors (must be marked with @triton.jit)

  * **keep_dims** (_bool_) – if true, keep the reduced dimensions with length 1




This function can also be called as a member function on [`tensor`](triton.language.tensor.html#triton.language.tensor "triton.language.tensor"), as `x.reduce(...)` instead of `reduce(x, ...)`.
