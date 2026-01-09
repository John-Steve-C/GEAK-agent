# triton.language.clamp¶

triton.language.clamp(_x_ , _min_ , _max_ , _propagate_nan: ~triton.language.core.constexpr = <PROPAGATE_NAN.NONE: 0>_, __semantic=None_)¶
    

Clamps the input tensor `x` within the range [min, max]. Behavior when `min` > `max` is undefined.

Parameters:
    

  * **x** (_Block_) – the input tensor

  * **min** (_Block_) – the lower bound for clamping

  * **max** (_Block_) – the upper bound for clamping

  * **propagate_nan** (_tl.PropagateNan_) – whether to propagate NaN values. Applies only to the `x` tensor. If either `min` or `max` is NaN, the result is undefined.




See also

`tl.PropagateNan`
