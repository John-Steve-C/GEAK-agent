# triton.language.minimum¶

triton.language.minimum(_x_ , _y_ , _propagate_nan: ~triton.language.core.constexpr = <PROPAGATE_NAN.NONE: 0>_, __semantic=None_)¶
    

Computes the element-wise minimum of `x` and `y`.

Parameters:
    

  * **x** (_Block_) – the first input tensor

  * **y** (_Block_) – the second input tensor

  * **propagate_nan** (_tl.PropagateNan_) – whether to propagate NaN values.




See also

`tl.PropagateNan`
