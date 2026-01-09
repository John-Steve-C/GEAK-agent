# triton.language.softmax¶

triton.language.softmax(_x_ , _dim =None_, _keep_dims =False_, _ieee_rounding =False_)¶
    

Computes the element-wise softmax of `x`.

Parameters:
    

**x** (_Block_) – the input values

This function can also be called as a member function on [`tensor`](triton.language.tensor.html#triton.language.tensor "triton.language.tensor"), as `x.softmax(...)` instead of `softmax(x, ...)`.
