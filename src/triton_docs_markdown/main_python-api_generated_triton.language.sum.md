# triton.language.sum¶

triton.language.sum(_input_ , _axis =None_, _keep_dims =False_, _dtype : constexpr | None = None_)¶
    

Returns the sum of all elements in the `input` tensor along the provided `axis`

Parameters:
    

  * **input** (_Tensor_) – the input values

  * **axis** (_int_) – the dimension along which the reduction should be done. If None, reduce all dimensions

  * **keep_dims** (_bool_) – if true, keep the reduced dimensions with length 1

  * **dtype** (_tl.dtype_) – the desired data type of the returned tensor. If specified, the input tensor is casted to `dtype` before the operation is performed. This is useful for preventing data overflows. If not specified, integer and bool dtypes are upcasted to `tl.int32` and float dtypes are upcasted to at least `tl.float32`.




This function can also be called as a member function on [`tensor`](triton.language.tensor.html#triton.language.tensor "triton.language.tensor"), as `x.sum(...)` instead of `sum(x, ...)`.
