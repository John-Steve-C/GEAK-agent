# triton.language.split¶

triton.language.split(_a_ , __semantic =None_, __generator =None_) → tuple[[tensor](triton.language.tensor.html#triton.language.tensor "triton.language.tensor"), [tensor](triton.language.tensor.html#triton.language.tensor "triton.language.tensor")]¶
    

Split a tensor in two along its last dim, which must have size 2.

For example, given a tensor of shape (4,8,2), produces two tensors of shape (4,8). Given a tensor of shape (2), returns two scalars.

If you want to split into more than two pieces, you can use multiple calls to this function (probably plus calling reshape). This reflects the constraint in Triton that tensors must have power-of-two sizes.

split is the inverse of join.

Parameters:
    

**a** (_Tensor_) – The tensor to split.

This function can also be called as a member function on [`tensor`](triton.language.tensor.html#triton.language.tensor "triton.language.tensor"), as `x.split()` instead of `split(x)`.
