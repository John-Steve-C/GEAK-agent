# triton.language.histogram¶

triton.language.histogram(_input_ , _num_bins_ , _mask =None_, __semantic =None_, __generator =None_)¶
    

computes an histogram based on input tensor with num_bins bins, the bins have a width of 1 and start at 0.

Parameters:
    

  * **input** (_Tensor_) – the input tensor

  * **num_bins** (_int_) – number of histogram bins

  * **mask** (Block of triton.int1, optional) – if mask[idx] is false, exclude input[idx] from histogram




This function can also be called as a member function on [`tensor`](triton.language.tensor.html#triton.language.tensor "triton.language.tensor"), as `x.histogram(...)` instead of `histogram(x, ...)`.
