# triton.language.cumsum¶

triton.language.cumsum(_input_ , _axis =0_, _reverse =False_, _dtype : constexpr | None = None_)¶
    

Returns the cumsum of all elements in the `input` tensor along the provided `axis`

Parameters:
    

  * **input** (_Tensor_) – the input values

  * **axis** (_int_) – the dimension along which the scan should be done

  * **reverse** (_bool_) – if true, the scan is performed in the reverse direction

  * **dtype** (_tl.dtype_) – the desired data type of the returned tensor. If specified, the input tensor is casted to `dtype` before the operation is performed. If not specified, small integer types (< 32 bits) are upcasted to prevent overflow. Note that `tl.bfloat16` inputs are automatically promoted to `tl.float32`.




This function can also be called as a member function on [`tensor`](triton.language.tensor.html#triton.language.tensor "triton.language.tensor"), as `x.cumsum(...)` instead of `cumsum(x, ...)`.
