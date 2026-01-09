# triton.language.interleave¶

triton.language.interleave(_a_ , _b_)¶
    

Interleaves the values of two tensors along their last dimension. The two tensors must have the same shape. Equivalent to tl.join(a, b).reshape(a.shape[:-1] + [2 * a.shape[-1]])

Parameters:
    

  * **a** (_Tensor_) – The first input tensor.

  * **b** (_Tensor_) – The second input tensor.



