# triton.language.where¶

triton.language.where(_condition_ , _x_ , _y_ , __semantic =None_)¶
    

Returns a tensor of elements from either `x` or `y`, depending on `condition`.

Note that `x` and `y` are always evaluated regardless of the value of `condition`.

If you want to avoid unintended memory operations, use the `mask` arguments in triton.load and triton.store instead.

The shape of `x` and `y` are both broadcast to the shape of `condition`. `x` and `y` must have the same data type.

Parameters:
    

  * **condition** (_Block_ _of_ _triton.bool_) – When True (nonzero), yield x, otherwise yield y.

  * **x** – values selected at indices where condition is True.

  * **y** – values selected at indices where condition is False.



