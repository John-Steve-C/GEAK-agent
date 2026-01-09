# triton.language.join¶

triton.language.join(_a_ , _b_ , __semantic =None_)¶
    

Join the given tensors in a new, minor dimension.

For example, given two tensors of shape (4,8), produces a new tensor of shape (4,8,2). Given two scalars, returns a tensor of shape (2).

The two inputs are broadcasted to be the same shape.

If you want to join more than two elements, you can use multiple calls to this function. This reflects the constraint in Triton that tensors must have power-of-two sizes.

join is the inverse of split.

Parameters:
    

  * **a** (_Tensor_) – The first input tensor.

  * **b** (_Tensor_) – The second input tensor.



