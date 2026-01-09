# triton.language.cast¶

triton.language.cast(_input_ , _dtype : dtype_, _fp_downcast_rounding : str | None = None_, _bitcast : bool = False_, __semantic =None_)¶
    

Casts a tensor to the given `dtype`.

Parameters:
    

  * **dtype** (_tl.dtype_) – The target data type.

  * **fp_downcast_rounding** (_str_ _,__optional_) – The rounding mode for downcasting floating-point values. This parameter is only used when self is a floating-point tensor and dtype is a floating-point type with a smaller bitwidth. Supported values are `"rtne"` (round to nearest, ties to even) and `"rtz"` (round towards zero).

  * **bitcast** (_bool_ _,__optional_) – If true, the tensor is bitcasted to the given `dtype`, instead of being numerically casted.




This function can also be called as a member function on [`tensor`](triton.language.tensor.html#triton.language.tensor "triton.language.tensor"), as `x.cast(...)` instead of `cast(x, ...)`.
